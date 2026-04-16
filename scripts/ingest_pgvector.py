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
from pathlib import Path

import asyncpg
import yaml
from openai import AsyncOpenAI


def _as_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n".join(str(v).strip() for v in value if str(v).strip())
    return str(value).strip()


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
            carry = current[-overlap:].strip()
            current = f"{carry}\n\n{para}".strip() if carry else para
        else:
            # Extremely long single paragraph fallback.
            start = 0
            while start < len(para):
                end = min(len(para), start + target)
                chunks.append(para[start:end])
                start = max(start + target - overlap, end)
            current = ""
    if current:
        chunks.append(current)
    return chunks


def _build_sections(y: dict) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    for key in [
        "sanskrit",
        "transliteration",
        "translation",
        "translation_literal",
        "commentary",
        "voice_of_siva",
        "sadhana",
    ]:
        text = _as_text(y.get(key))
        if text:
            sections.append((key, text))

    modes = y.get("modes") or {}
    if isinstance(modes, dict):
        for mk, mv in modes.items():
            text = _as_text(mv)
            if text:
                sections.append((f"mode:{mk}", text))

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
                sections.append((f"appendix:{label}", text))
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
    conn = await asyncpg.connect(
        user=os.getenv("PG_USER", "postgres"),
        password=os.getenv("PG_PASSWORD", "postgres"),
        database=os.getenv("PG_DB", "pratibha"),
        host=os.getenv("PG_HOST", "localhost"),
        port=int(os.getenv("PG_PORT", "5432")),
    )

    total = 0
    for fp in files:
        path = Path(fp)
        try:
            y = yaml.safe_load(path.read_text(encoding="utf-8", errors="replace")) or {}
            if not isinstance(y, dict):
                continue
            # Idempotent per source file.
            await conn.execute("DELETE FROM chunks WHERE metadata->>'source_file' = $1", path.as_posix())
            base_meta = {
                "source_file": path.as_posix(),
                "_id": y.get("_id") or y.get("unit_id"),
                "title": y.get("title") or y.get("unit_label"),
                "sutra_id": y.get("sutra_id") or y.get("source_id"),
                "collection": y.get("collection") or y.get("work_title") or _infer_collection(path),
                "type": y.get("type") or y.get("unit_type"),
                "themes": y.get("themes") if isinstance(y.get("themes"), list) else [],
                "quality_score": y.get("quality_score") or y.get("quality_score_unit") or 0,
                "ingested_at": datetime.datetime.utcnow().isoformat() + "Z",
            }
            sections = _build_sections(y)
            for section_name, text in sections:
                for chunk_idx, chunk in enumerate(_split_chunks(text), start=1):
                    chunk_text = _with_chunk_context(chunk, {**base_meta, "section": section_name})
                    emb = (await client.embeddings.create(model=embedding_model, input=chunk_text)).data[0].embedding
                    vector_str = f"[{','.join(map(str, emb))}]"
                    meta = {**base_meta, "section": section_name, "chunk_index": chunk_idx}
                    await conn.execute(
                        "INSERT INTO chunks (body, embedding, metadata) VALUES ($1, $2, $3)",
                        chunk_text,
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
