# Handover — Related passages precomputed (and what's left for you)

**Branch:** `cursor/study-notes-layer-labels-chuang-cleanup`
**Commits:** `756f6fbb`, `37fb0996`, `be605761` (on top of your `73376975`)
**Date:** 13 Sep 2026

---

## TL;DR

`GET /verse/{id}/related` took **26–43 seconds** per request. It now reads a
precomputed table: **0.08 µs**, with results verified *identical* (same ids,
same order) to the exact query it replaces.

**Prod DB changes are already applied. The code is committed but NOT deployed.**

---

## ⚠️ Read this first: the African collections

**The live API serves 3,891 units. This branch had 3,693.** The 198 missing ones
are 7 African-tradition collections:

```
senegalese_animism (32)   pulaar_texts (28)      pulaar_tradition (28)
animismo_fetichista (28)  myths_of_ife (28)      os_africanos_no_brasil (28)
futa_jalon_fulde (26)
```

They exist on `feature/monad-phase2-chrome`, not here. I extracted them into
this branch (commit `756f6fbb`) so the corpus matches production — otherwise
those 198 units would have been permanently baked in with **no resonances at
all**, which is exactly the trap your 1 Aug session warned about ("doing the
precompute before re-embedding would just bake in the gap").

**This means your branches have diverged in both directions:**

| | has | missing |
|---|---|---|
| this branch (before my commit) | 111 files `monad-phase2-chrome` lacks | the 198 African ones |
| `feature/monad-phase2-chrome` | the 198 African ones | patañjali (43), rūmī (26), chāndogya (25), dōgen (17) |

`3,693 + 198 = 3,891` = the live count exactly, so the 111 files unique to this
branch **are** already in production. Only the African direction was missing.

**Decide where the corpus lives before the next corpus change**, or this repeats.
If `monad-phase2-chrome` is the real source of truth, my commit `756f6fbb` is
redundant there and should be dropped when merging.

---

## ⚠️ Second thing I could not resolve: which branch does Render build?

`render.yaml:16` says:

```yaml
branch: cursor/study-notes-layer-labels-chuang-cleanup
```

But that branch's committed HEAD had **zero** African units, while the live API
serves them. Both can't be true. Either the Render dashboard points somewhere
else (dashboard settings override the blueprint after creation), or the API gets
its corpus from outside the repo.

**Check the Render dashboard.** Whatever branch it actually builds from is where
these commits need to land, or you'll deploy and nothing will change.

---

## What changed in prod (already done, no action needed)

| change | state |
|---|---|
| Embedded 960 previously-unembedded units (762 + 198) | done, ~$0.06, 0 errors |
| Deleted 118 orphaned chunk rows from collection renames | done, backup on disk |
| Built HNSW index, dropped the old ivfflat | done |
| Applied `db/migrations/002_chunks_metadata_indexes.sql` | done |

Prod DB now: **3,891 units / 40,501 chunks / 700 MB**, one HNSW index, zero orphans.

The orphan delete is reversible — `data/_orphan_chunks_backup.json` holds all 118
rows including embeddings (gitignored, on my machine; ask if you want it).

---

## What changed in the code

### The actual fix
Resonances are a pure function of corpus + embeddings, so they're computed once
offline and read from `data/resonances.json` (2.7 MB). `/verse/{id}/related`
falls back to the live kNN if the artefact is missing, so **nothing breaks if you
deploy the code without the file** — it just stays slow. The response now carries
`"source": "precomputed" | "live"` so you can tell which path served it.

### Three faults were behind the latency

1. **The vector index was never used.** `app/rag.py` ordered by `<->` (L2) while
   the only index was `vector_cosine_ops`, which serves `<=>`. pgvector only uses
   an index when the ORDER BY operator matches the opclass — so every call
   sequentially scanned the whole 572 MB table.
   Prod EXPLAIN: **59,498 ms seq scan → 790 ms index scan.**

   *Not a correctness bug.* `text-embedding-3-small` returns unit vectors, and
   for unit vectors L2 and cosine rank identically. The old results were right,
   just slow.

2. **No index on `metadata`.** The seed lookup filters `metadata->>'_id'` with no
   index, seq-scanning the same table *again* before the kNN ran. Migration 002
   fixes it: **55 ms, Index Scan**.

3. **ivfflat had no usable operating point.** Measured on the real corpus:

   | index | recall | latency |
   |---|---|---|
   | ivfflat probes=1 (default) | 19.4% | 377 ms |
   | ivfflat probes=32 | 84.8% | 13,670 ms |
   | **HNSW ef_search=200** | **94.1%** | **182 ms** |

   Replaced with HNSW and dropped the old index — with both present the planner
   costed ivfflat cheaper and left HNSW unused, so dropping it was required, not
   cleanup.

   **`hnsw.ef_search` must exceed the query's LIMIT** or recall collapses (27% at
   the default 40 against `LIMIT 144`). `_tune_ann_search()` in `app/rag.py`
   handles this — don't remove it.

### New tooling

| script | purpose |
|---|---|
| `scripts/precompute_resonances.py` | regenerates the artefact; **re-run after any re-embed** |
| `scripts/prune_orphan_chunks.py` | removes rows whose YAML was renamed away; dry run by default, backs up first |
| `scripts/ingest_pgvector.py --only <list>` | backfill specific files without re-embedding indexed units |

---

## To deploy

1. **Confirm the Render build branch** (see above), and push these commits there.
2. Deploy the API. `data/resonances.json` ships via the Dockerfile — I added a
   deliberate hard `COPY` for it, because without it the endpoint silently
   degrades to the 30 s path and looks like the fix simply didn't work.
3. Verify: `curl .../verse/bhagavad_gita.bg_01_47/related` should return
   instantly with `"source": "precomputed"`.

### Whenever the corpus changes

```bash
# 1. embed any new/changed units
uv run python scripts/ingest_pgvector.py --dir data/canonical

# 2. regenerate the artefact  (~15 min: 3 min fetch, 12 min exact matmul)
uv run python scripts/precompute_resonances.py --out data/resonances.json

# 3. commit data/resonances.json and redeploy
```

Skipping step 2 doesn't break anything — new units just fall back to the live
kNN — but they'll be slow and the artefact will be stale.

---

## Still open (not done, deliberately)

- **Connection pooling.** Five call sites still open a fresh connection per
  request (`rag.py:833/894/967/1076`, `main.py:378`) at **391 ms each** — measured.
  With the scan cost gone this is now the dominant remaining latency on the chat
  path. It changes app lifecycle, so it wants its own pass.
- **The `/verses` payload.** Your `73376975` adds `collection`/`limit`/`offset`,
  which is the right direction. The unbounded default still returns **15 MB**
  (3,497 items, ~5 KB each) — worth capping server-side so a missing `limit`
  can't dump the corpus. See `pratibha-ui-audit.html` finding B-03.
- **iOS bundling.** Your original 1 Aug scope was baking resonances into
  `corpus.json` for offline/instant map rendering. Serving from the API gets the
  speed but still needs the network. `data/resonances.json` is the same data in
  the same shape, so bundling it is a small step from here.

---

## Honest note on how this went

The fix you'd scoped on 1 Aug — precompute instead of computing live — was
correct and simple. I spent a long detour optimising the live query before
reading that session, and then ran the first embedding pass against this
branch's data without checking it matched production, which cost a second pass.

What the detour did earn: the `<->` → `<=>` fix is real and still needed for
chat, and it's what makes the precompute a 15-minute job instead of a 12-hour
one (1,457 calls × 30 s).
