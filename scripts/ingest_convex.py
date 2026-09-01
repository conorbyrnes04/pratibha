#!/usr/bin/env python3
"""Embed corpus YAML chunks and write them to the Convex `rag_chunks` table —
the Convex-native replacement for scripts/ingest_pgvector.py.

Reuses the exact chunking / section / embedding logic from the pgvector ingest so
retrieval quality is identical; only the sink changes (Convex HTTP action instead
of asyncpg). Idempotent per source file (Convex replaceSource does DELETE+INSERT).

Env:
  CONVEX_SITE_URL      https://<deployment>.convex.site  (HTTP actions domain)
  RAG_INGEST_TOKEN     shared secret, also set in the Convex deployment env
  OPENAI_API_KEY       real sk-proj key (embeddings)  — pass explicitly to avoid
                       the sk-or-v1 shell shadow.

Usage:
  OPENAI_API_KEY=$(grep ^OPENAI_API_KEY= .env|cut -d= -f2-) \
  RAG_INGEST_TOKEN=... CONVEX_SITE_URL=https://xxx.convex.site \
  .venv/bin/python scripts/ingest_convex.py --dir data/canonical/hatha_yoga_pradipika
"""
import argparse, asyncio, glob, os, sys
from pathlib import Path
import yaml
import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import datetime
from app.data_loader import normalize_unit  # noqa: E402
from app.collection_aliases import canonical_slug  # noqa: E402
# Reuse the pgvector ingest's chunking/section/embedding helpers verbatim.
from scripts.ingest_pgvector import (  # noqa: E402
    _split_chunks, _build_sections, _should_skip_rag_ingest,
    _embedding_client_and_model, _with_chunk_context, _infer_collection, EMBED_BATCH,
)


def _site_url() -> str:
    url = (os.getenv("CONVEX_SITE_URL") or "").strip().rstrip("/")
    if not url:
        raise SystemExit("CONVEX_SITE_URL (https://<deployment>.convex.site) is required")
    return url


async def _embed(client, model, inputs: list[str]) -> list[list[float]]:
    vectors: list[list[float]] = []
    for start in range(0, len(inputs), EMBED_BATCH):
        resp = await client.embeddings.create(model=model, input=inputs[start:start + EMBED_BATCH])
        for item in sorted(resp.data, key=lambda d: d.index):
            vectors.append(list(item.embedding))
    return vectors


async def main(dir_path: str, limit: int = 0):
    files = sorted(glob.glob(os.path.join(dir_path, "**", "*.yml"), recursive=True))
    if limit:
        files = files[:limit]
    if not files:
        print(f"No YAML under {dir_path}")
        return
    client, model = _embedding_client_and_model()
    token = (os.getenv("RAG_INGEST_TOKEN") or "").strip()
    if not token:
        raise SystemExit("RAG_INGEST_TOKEN is required")
    endpoint = f"{_site_url()}/rag/ingest"
    headers = {"authorization": f"Bearer {token}", "content-type": "application/json"}

    total = 0
    async with httpx.AsyncClient(timeout=60) as http:
        for fp in files:
            path = Path(fp)
            try:
                y = yaml.safe_load(path.read_text(encoding="utf-8", errors="replace")) or {}
                if not isinstance(y, dict):
                    continue
                norm = normalize_unit(y, path.as_posix())
                collection = canonical_slug(
                    norm.get("collection") or y.get("collection") or _infer_collection(path),
                    path.as_posix(),
                )
                base_meta = {
                    "source_file": path.as_posix(),
                    "_id": norm.get("_id") or y.get("_id") or y.get("unit_id"),
                    "title": norm.get("title") or y.get("title") or y.get("unit_label"),
                    "sutra_id": norm.get("sutra_id") or y.get("sutra_id") or y.get("source_id"),
                    "collection": collection,
                    "type": y.get("type") or y.get("unit_type"),
                    "themes": norm.get("themes") if isinstance(norm.get("themes"), list) else [],
                    "quality_score": y.get("quality_score") or 0,
                    "editorial_maturity": norm.get("editorial_maturity") or "needs_rewrite",
                    "editorial_score": norm.get("editorial_score") or 0,
                    "ingested_at": datetime.datetime.utcnow().isoformat() + "Z",
                }
                skip = _should_skip_rag_ingest(norm, collection)
                if skip:
                    # still clear any stale chunks for this file
                    await http.post(endpoint, headers=headers,
                                    json={"sourceFile": path.as_posix(), "chunks": []})
                    continue

                embed_inputs, pending = [], []
                for section_name, text, layer_kind, layer_prov in _build_sections(norm):
                    for chunk_idx, chunk in enumerate(_split_chunks(text), start=1):
                        meta = {**base_meta, "section": section_name,
                                "layer_kind": layer_kind, "chunk_index": chunk_idx}
                        if layer_prov:
                            meta["layer_provenance"] = layer_prov
                        embed_inputs.append(_with_chunk_context(chunk, meta))
                        pending.append((chunk.strip(), meta, section_name))

                vectors = await _embed(client, model, embed_inputs) if embed_inputs else []
                chunks = [
                    {"body": body, "embedding": vec, "collection": collection,
                     "section": section, "sourceFile": path.as_posix(),
                     "unitId": str(meta.get("_id") or "") or None, "meta": meta}
                    for (body, meta, section), vec in zip(pending, vectors)
                ]
                r = await http.post(endpoint, headers=headers,
                                    json={"sourceFile": path.as_posix(), "chunks": chunks})
                r.raise_for_status()
                total += r.json().get("inserted", 0)
            except Exception as e:
                print(f"Skipping {path.name}: {str(e)[:160]}")
                continue
    print(f"Ingested {total} chunks into Convex rag_chunks from {len(files)} files.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    asyncio.run(main(args.dir, args.limit))
