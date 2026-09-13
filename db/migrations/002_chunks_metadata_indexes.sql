-- 002: index the metadata lookups used by the Related-passages seed query.
--
-- WHY: app/rag.py's retrieve_related_unit_ids() first resolves a seed chunk with
--   WHERE metadata->>'_id' = $1
-- On a 31k-row / 572 MB chunks table with no index on that expression, this is a
-- full sequential scan of the whole table — and it runs BEFORE the kNN query on
-- every single /verse/{id}/related request.
--
-- Apply to any environment that predates this file (Supabase prod included);
-- db/init/01_init.sql only runs on a fresh container, so prod never got it.
--
-- CONCURRENTLY so it does not lock the table. Must run outside a transaction.

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_chunks_meta_id
  ON chunks ((metadata->>'_id'));

-- layer_kind is used to rank which chunk of a unit becomes the seed vector,
-- and to filter elsewhere. Cheap and small.
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_chunks_meta_layer_kind
  ON chunks ((metadata->>'layer_kind'));

ANALYZE chunks;
