"""Embed YAML chunks and insert into pgvector.

Requires OPENAI_API_KEY and Postgres+pgvector.
Usage:
  python scripts/ingest_pgvector.py --dir data/canonical
"""

import argparse
import asyncio
import datetime
import glob
import json
import os
import re
import sys
from pathlib import Path

import asyncpg
import yaml
from openai import AsyncOpenAI

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.data_loader import normalize_unit  # noqa: E402  (path set up above)
from app.collection_aliases import canonical_slug  # noqa: E402
from app.config import settings  # noqa: E402

# Number of chunks embedded per API request (the embeddings endpoint accepts a
# list input; batching is dramatically faster than one call per chunk).
EMBED_BATCH = 96


def _as_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n".join(str(v).strip() for v in value if str(v).strip())
    return str(value).strip()


def _word_safe_overlap(text: str, overlap: int) -> str:
    """Return a trailing slice of ~overlap chars that begins at a word boundary."""
    if overlap <= 0 or not text:
        return ""
    tail = text[-overlap:]
    if len(text) > overlap:
        # We cut into the middle of `text`; drop the partial leading word.
        space = tail.find(" ")
        tail = tail[space + 1:] if space != -1 else ""
    return tail.strip()


def _split_long_paragraph(para: str, target: int, overlap: int) -> list[str]:
    """Slice an over-long paragraph on whitespace so words are never split."""
    pieces: list[str] = []
    start = 0
    n = len(para)
    while start < n:
        end = min(n, start + target)
        if end < n:
            # Back up to the last whitespace so we break between words.
            space = para.rfind(" ", start, end)
            if space > start:
                end = space
        pieces.append(para[start:end].strip())
        if end >= n:
            break
        # Step back by ~overlap, snapped to a word boundary.
        next_start = max(end - overlap, start + 1)
        space = para.find(" ", next_start, end)
        start = (space + 1) if space != -1 else end
    return [p for p in pieces if p]


def _split_chunks(text: str, target: int = 700, overlap: int = 120) -> list[str]:
    text = (text or "").strip()
    if not text:
        return []
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if not paragraphs:
        paragraphs = [text]

    # Break very large paragraphs into sentence-ish segments first.
    normalized: list[str] = []
    for para in paragraphs:
        if len(para) <= target * 2:
            normalized.append(para)
            continue
        pieces = re.split(r"(?<=[.!?])\s+", para)
        cur = ""
        for piece in pieces:
            piece = piece.strip()
            if not piece:
                continue
            candidate = f"{cur} {piece}".strip() if cur else piece
            if len(candidate) <= target:
                cur = candidate
            else:
                if cur:
                    normalized.append(cur)
                # A single sentence longer than target is split on word
                # boundaries rather than mid-word.
                if len(piece) > target:
                    normalized.extend(_split_long_paragraph(piece, target, overlap))
                    cur = ""
                else:
                    cur = piece
        if cur:
            normalized.append(cur)
    paragraphs = normalized

    chunks: list[str] = []
    current = ""
    for para in paragraphs:
        candidate = f"{current}\n\n{para}".strip() if current else para
        if len(candidate) <= target:
            current = candidate
            continue
        if current:
            chunks.append(current)
            carry = _word_safe_overlap(current, overlap)
            current = f"{carry}\n\n{para}".strip() if carry else para
        else:
            # Extremely long single paragraph fallback (word-boundary aware).
            chunks.extend(_split_long_paragraph(para, target, overlap))
            current = ""
    if current:
        chunks.append(current)
    return chunks


def _layer_text(layer: dict) -> str:
    body = _as_text(layer.get("body"))
    items = layer.get("items")
    if not isinstance(items, list) or not items:
        return body
    rendered: list[str] = []
    for item in items:
        if isinstance(item, dict):
            if item.get("term"):
                rendered.append(f"{_as_text(item.get('term'))}: {_as_text(item.get('definition'))}")
            elif item.get("citation"):
                divergence = _as_text(item.get("divergence"))
                suffix = f"\nDivergence: {divergence}" if divergence else ""
                rendered.append(f"{_as_text(item.get('citation'))}: {_as_text(item.get('resonance'))}{suffix}")
            else:
                rendered.append(json.dumps(item, ensure_ascii=False))
        else:
            rendered.append(_as_text(item))
    combined = "\n\n".join([x for x in [body, *rendered] if x])
    return combined.strip()


RAG_HARD_GATE_COLLECTIONS = frozenset({"rumi_mathnawi"})
RAG_BLOCK_MARKER = "DO NOT ingest to RAG"


def _layer_provenance(layer: dict) -> str:
    for key in ("layer_provenance", "provenance", "method"):
        val = _as_text(layer.get(key))
        if val:
            return val
    return ""


def _should_skip_rag_ingest(norm: dict, collection: str) -> str | None:
    """Return a skip reason when this unit must not be embedded for RAG."""
    maturity = _as_text(norm.get("editorial_maturity"))
    if collection in RAG_HARD_GATE_COLLECTIONS and maturity == "structural_draft":
        return f"collection {collection} at structural_draft"

    layers = norm.get("pratibha_layers")
    if isinstance(layers, list):
        for layer in layers:
            if not isinstance(layer, dict) or _as_text(layer.get("kind")) != "translation":
                continue
            if RAG_BLOCK_MARKER in _layer_provenance(layer):
                return "translation layer_provenance contains DO NOT ingest to RAG"
    return None


def _build_sections(y: dict) -> list[tuple[str, str, str, str]]:
    sections: list[tuple[str, str, str, str]] = []
    layers = y.get("pratibha_layers")
    if isinstance(layers, list):
        for idx, layer in enumerate(layers):
            if not isinstance(layer, dict):
                continue
            kind = _as_text(layer.get("kind")) or f"layer_{idx + 1}"
            label = _as_text(layer.get("label")) or kind
            text = _layer_text(layer)
            if text:
                sections.append((label, text, kind, _layer_provenance(layer)))
        if sections:
            return sections

    for key in [
        "sanskrit",
        "sanskrit_devanagari",
        "transliteration",
        "sanskrit_iast",
        "translation",
        "translation_literal",
        "commentary",
        "voice_of_siva",
        "sadhana",
        "practice",
        "abhyasa",
    ]:
        text = _as_text(y.get(key))
        if text:
            layer_kind = {
                "sanskrit": "original",
                "sanskrit_devanagari": "original",
                "transliteration": "iast",
                "sanskrit_iast": "iast",
                "translation": "translation",
                "translation_literal": "translation",
                "commentary": "commentary",
                "practice": "practice",
                "abhyasa": "practice",
            }.get(key, key)
            sections.append((key, text, layer_kind, ""))

    modes = y.get("modes") or {}
    if isinstance(modes, dict):
        for mk, mv in modes.items():
            text = _as_text(mv)
            if text:
                sections.append((f"mode:{mk}", text, f"mode:{mk}", ""))

    appendixes = y.get("appendixes") or []
    if isinstance(appendixes, list):
        for idx, item in enumerate(appendixes):
            if isinstance(item, dict):
                label = _as_text(item.get("commentator")) or f"appendix_{idx + 1}"
                text = _as_text(item.get("text"))
            else:
                label = f"appendix_{idx + 1}"
                text = _as_text(item)
            if text:
                sections.append((f"appendix:{label}", text, "appendix", ""))
    return sections


def _with_chunk_context(chunk: str, meta: dict) -> str:
    context_parts = [
        str(meta.get("collection") or "").strip(),
        str(meta.get("title") or "").strip(),
        str(meta.get("section") or "").strip(),
        str(meta.get("sutra_id") or "").strip(),
    ]
    context = " | ".join([p for p in context_parts if p])
    if not context:
        return chunk
    return f"[{context}]\n\n{chunk}"


def _infer_collection(path: Path) -> str:
    # Expected canonical layout: data/canonical/<collection_slug>/<file>.yml
    return path.parent.name.strip()


def _embedding_client_and_model() -> tuple[AsyncOpenAI, str]:
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small").strip() or "text-embedding-3-small"
    if openai_key:
        return AsyncOpenAI(api_key=openai_key), model

    openrouter_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if openrouter_key:
        if "/" not in model:
            model = f"openai/{model}"
        headers = {}
        site = os.getenv("OPENROUTER_SITE_URL", "").strip()
        app = os.getenv("OPENROUTER_APP_NAME", "").strip()
        if site:
            headers["HTTP-Referer"] = site
        if app:
            headers["X-Title"] = app
        client = AsyncOpenAI(
            api_key=openrouter_key,
            base_url="https://openrouter.ai/api/v1",
            default_headers=headers or None,
        )
        return client, model

    raise RuntimeError("Either OPENAI_API_KEY or OPENROUTER_API_KEY is required for ingestion embeddings.")


async def main(dir_path: str):
    patterns = [
        os.path.join(dir_path, "**", "*.yml"),
        os.path.join(dir_path, "**", "*.yaml"),
    ]
    files = sorted({fp for pattern in patterns for fp in glob.glob(pattern, recursive=True)})
    if not files:
        print(f"No YAML files found under: {dir_path}")
        return

    client, embedding_model = _embedding_client_and_model()
    # Shares the API's connection settings so a single DATABASE_URL (and TLS)
    # works for both the running app and this one-time ingest.
    conn = await asyncpg.connect(**settings.asyncpg_kwargs())

    total = 0
    for fp in files:
        path = Path(fp)
        try:
            y = yaml.safe_load(path.read_text(encoding="utf-8", errors="replace")) or {}
            if not isinstance(y, dict):
                continue
            # Reuse the API's normalization so DB metadata (maturity, layers)
            # matches exactly what the running app serves and filters on.
            norm = normalize_unit(y, path.as_posix())
            # Idempotent per source file.
            await conn.execute("DELETE FROM chunks WHERE metadata->>'source_file' = $1", path.as_posix())
            base_meta = {
                "source_file": path.as_posix(),
                "_id": norm.get("_id") or y.get("_id") or y.get("unit_id"),
                "title": norm.get("title") or y.get("title") or y.get("unit_label"),
                "sutra_id": norm.get("sutra_id") or y.get("sutra_id") or y.get("source_id"),
                "collection": canonical_slug(norm.get("collection") or y.get("collection") or _infer_collection(path), path.as_posix()),
                "type": y.get("type") or y.get("unit_type"),
                "themes": norm.get("themes") if isinstance(norm.get("themes"), list) else [],
                "quality_score": y.get("quality_score") or y.get("quality_score_unit") or 0,
                "editorial_maturity": norm.get("editorial_maturity") or "needs_rewrite",
                "editorial_score": norm.get("editorial_score") or 0,
                "ingested_at": datetime.datetime.utcnow().isoformat() + "Z",
            }
            skip_reason = _should_skip_rag_ingest(norm, base_meta["collection"])
            if skip_reason:
                print(f"Skipping RAG ingest for {path.name}: {skip_reason}")
                continue

            # Build sections from the normalized record so ingestion and the API
            # use the identical pratibha_layers (single source of truth).
            sections = _build_sections(norm)
            # Gather every chunk for this file, then embed in batches. Embedding
            # uses a context header (better recall) while we store the clean
            # body so retrieved sources read as pure teaching text.
            embed_inputs: list[str] = []
            pending_rows: list[tuple[str, dict]] = []
            for section_name, text, layer_kind, layer_prov in sections:
                for chunk_idx, chunk in enumerate(_split_chunks(text), start=1):
                    meta = {**base_meta, "section": section_name, "layer_kind": layer_kind, "chunk_index": chunk_idx}
                    if layer_prov:
                        meta["layer_provenance"] = layer_prov
                    embed_inputs.append(_with_chunk_context(chunk, meta))
                    pending_rows.append((chunk.strip(), meta))

            for start in range(0, len(embed_inputs), EMBED_BATCH):
                batch = embed_inputs[start:start + EMBED_BATCH]
                resp = await client.embeddings.create(model=embedding_model, input=batch)
                for item in sorted(resp.data, key=lambda d: d.index):
                    body, meta = pending_rows[start + item.index]
                    vector_str = f"[{','.join(map(str, item.embedding))}]"
                    await conn.execute(
                        "INSERT INTO chunks (body, embedding, metadata) VALUES ($1, $2, $3)",
                        body,
                        vector_str,
                        json.dumps(meta),
                    )
                    total += 1
        except Exception as e:
            print(f"Skipping {path.name}: {e}")
            continue

    await conn.close()
    print(f"Inserted {total} chunks into pgvector from {len(files)} files.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="data/canonical")
    args = ap.parse_args()
    asyncio.run(main(args.dir))
