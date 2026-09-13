"""Precompute the Related-passages ("resonance") neighbours for every unit.

WHY THIS EXISTS
---------------
`GET /verse/{id}/related` runs a pgvector kNN on every request. That output is a
*pure function of the corpus + embeddings* — nothing per-user, per-session or
time-varying — so it only changes when the corpus is re-embedded. Computing it
live buys zero freshness and costs a round trip (and a stall, and an offline
failure on the map).

This script computes the same answer once, EXACTLY (brute-force cosine over the
full chunk matrix — no ANN index, no recall loss), and writes it to a lookup
that clients read directly.

FIDELITY
--------
Mirrors `retrieve_related_unit_ids()` in app/rag.py:
  * seed vector = the unit's preferred layer, in the same priority order
    (translation > commentary > practice > resonances > other), tie-broken by
    chunk_index — see SEED_LAYER_PRIORITY below;
  * candidates are scored against ALL chunks of other units, keeping each
    unit's best-scoring chunk (so a match on any layer counts);
  * drops anything below RAG_MIN_SCORE;
  * caps each collection at `per_collection` so one large text cannot flood
    the panel, then tops up ignoring the cap if the neighbourhood was sparse.

The maturity skip (`needs_rewrite` / `structural_draft`) is deliberately NOT
applied here — app/main.py applies it at serve time against the live corpus, so
baking it in would freeze an editorial decision into the artefact.

USAGE
-----
    uv run python scripts/precompute_resonances.py --out data/resonances.json
    uv run python scripts/precompute_resonances.py --out data/resonances.json --limit 12
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from collections import defaultdict
from pathlib import Path

import asyncpg
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.config import settings  # noqa: E402

# Same order app/rag.py uses when choosing which chunk represents a unit.
SEED_LAYER_PRIORITY = {"translation": 1, "commentary": 2, "practice": 3, "resonances": 4}
DEFAULT_OTHER_PRIORITY = 5
# numpy block size for the similarity matmul — bounds peak RAM.
SEED_BLOCK = 512


FETCH_PAGE = 2000


async def fetch_chunks(dsn_kwargs: dict) -> tuple[list[dict], np.ndarray]:
    """Pull every chunk's metadata + embedding once, in pages.

    `embedding::text` is ~18 KB per row, so a single fetch of ~39k rows would
    buffer several hundred MB of Python strings at once. Paging keeps peak
    memory flat: each page is parsed straight into the preallocated float32
    array and the strings are released immediately.
    """
    conn = await asyncpg.connect(command_timeout=600, **dsn_kwargs)
    try:
        await conn.execute("SET statement_timeout = 0")
        total = await conn.fetchval("SELECT count(*) FROM chunks")
        print(f"  fetching {total:,} chunk embeddings in pages of {FETCH_PAGE:,} ...", flush=True)

        meta: list[dict] = []
        vecs = np.empty((total, 1536), dtype=np.float32)
        n = 0
        last_id = 0
        t0 = time.time()
        while True:
            rows = await conn.fetch(
                """
                SELECT id,
                       metadata->>'_id'          AS unit_id,
                       metadata->>'collection'   AS collection,
                       metadata->>'layer_kind'   AS layer_kind,
                       COALESCE((metadata->>'chunk_index')::int, 999) AS chunk_index,
                       embedding::text           AS emb
                FROM chunks
                WHERE id > $1
                ORDER BY id
                LIMIT $2
                """,
                last_id,
                FETCH_PAGE,
            )
            if not rows:
                break
            for r in rows:
                last_id = r["id"]
                if r["unit_id"] is None or not r["emb"]:
                    continue
                meta.append(
                    {
                        "unit_id": r["unit_id"],
                        "collection": (r["collection"] or "").strip(),
                        "layer_kind": (r["layer_kind"] or "").strip(),
                        "chunk_index": r["chunk_index"],
                    }
                )
                # np.fromstring's text mode is deprecated; split explicitly so a
                # future numpy cannot fail this mid-run.
                vecs[n] = np.array(r["emb"].strip("[]").split(","), dtype=np.float32)
                n += 1
            del rows
            print(f"    {n:,}/{total:,}  ({time.time()-t0:.0f}s)", flush=True)
    finally:
        await conn.close()
    return meta, vecs[:n]


def pick_seeds(meta: list[dict]) -> dict[str, int]:
    """unit_id -> row index of the chunk that represents it (same rule as rag.py)."""
    best: dict[str, tuple[tuple[int, int], int]] = {}
    for i, m in enumerate(meta):
        key = (SEED_LAYER_PRIORITY.get(m["layer_kind"], DEFAULT_OTHER_PRIORITY), m["chunk_index"])
        prev = best.get(m["unit_id"])
        if prev is None or key < prev[0]:
            best[m["unit_id"]] = (key, i)
    return {uid: idx for uid, (_, idx) in best.items()}


def compute(meta, vecs, seeds, limit, per_collection, min_score):
    # Embeddings from text-embedding-3-* are unit-norm, but normalise defensively
    # so the dot product is exactly cosine similarity even if that ever changes.
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    V = vecs / norms

    unit_ids = np.array([m["unit_id"] for m in meta])
    collections = np.array([m["collection"] for m in meta])
    seed_uids = sorted(seeds)
    seed_rows = np.array([seeds[u] for u in seed_uids])

    out: dict[str, list[dict]] = {}
    t0 = time.time()
    for start in range(0, len(seed_rows), SEED_BLOCK):
        block = seed_rows[start : start + SEED_BLOCK]
        sims = V[block] @ V.T                       # (block, n_chunks) cosine similarity
        for bi, gi in enumerate(block):
            uid = meta[gi]["unit_id"]
            row = sims[bi]
            # best score per *other* unit
            best: dict[str, float] = {}
            idx = np.flatnonzero(row >= min_score)
            for j in idx:
                other = unit_ids[j]
                if other == uid:
                    continue
                s = float(row[j])
                if s > best.get(other, -1.0):
                    best[other] = s
            ranked = sorted(best.items(), key=lambda kv: kv[1], reverse=True)

            picked, per_col = [], defaultdict(int)
            coll_of = {}
            for other, s in ranked:
                if other not in coll_of:
                    coll_of[other] = collections[np.flatnonzero(unit_ids == other)[0]]
            for other, s in ranked:
                if len(picked) >= limit:
                    break
                c = coll_of[other]
                if per_col[c] >= per_collection:
                    continue
                per_col[c] += 1
                picked.append({"id": other, "score": round(s, 4)})
            if len(picked) < limit:                 # top up ignoring the cap
                chosen = {p["id"] for p in picked}
                for other, s in ranked:
                    if len(picked) >= limit:
                        break
                    if other in chosen:
                        continue
                    picked.append({"id": other, "score": round(s, 4)})
                    chosen.add(other)
            out[uid] = picked
        done = min(start + SEED_BLOCK, len(seed_rows))
        print(f"  {done:,}/{len(seed_rows):,} units  ({time.time()-t0:.0f}s)", flush=True)
    return out


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/resonances.json")
    ap.add_argument("--limit", type=int, default=12, help="neighbours stored per unit")
    ap.add_argument("--per-collection", type=int, default=2)
    ap.add_argument("--min-score", type=float, default=settings.RAG_MIN_SCORE)
    args = ap.parse_args()

    print("precompute resonances (exact, brute-force cosine)")
    meta, vecs = await fetch_chunks(settings.asyncpg_kwargs())
    print(f"  {len(meta):,} chunks  |  {vecs.nbytes/1048576:.0f} MB", flush=True)

    seeds = pick_seeds(meta)
    print(f"  {len(seeds):,} units have a seed chunk", flush=True)

    res = compute(meta, vecs, seeds, args.limit, args.per_collection, args.min_score)

    empty = sum(1 for v in res.values() if not v)
    payload = {
        "version": 1,
        "generated_from_chunks": len(meta),
        "units": len(res),
        "limit": args.limit,
        "per_collection": args.per_collection,
        "min_score": args.min_score,
        "exact": True,
        "resonances": res,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    size = out.stat().st_size / 1048576
    print(f"\nwrote {out}  ({size:.2f} MB)")
    print(f"  units with neighbours: {len(res)-empty:,}   empty: {empty:,}")


if __name__ == "__main__":
    asyncio.run(main())
