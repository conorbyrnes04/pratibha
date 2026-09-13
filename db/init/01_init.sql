-- Enable pgvector extension and create chunks table
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS chunks (
  id SERIAL PRIMARY KEY,
  body TEXT NOT NULL,
  embedding VECTOR(1536) NOT NULL,
  metadata JSONB DEFAULT '{}'::jsonb
);
-- Vector index.
--
-- IMPORTANT: the opclass (vector_cosine_ops) only serves the cosine operator
-- `<=>`. Queries MUST `ORDER BY embedding <=> ...` or this index is ignored and
-- pgvector falls back to a sequential scan of the whole table. Measured on prod
-- with 31k chunks: seq scan 59,498 ms vs index scan 790 ms.
--
-- HNSW rather than ivfflat. Measured on the real corpus at LIMIT 144:
--   ivfflat(lists=100) probes=32 -> 84.8% recall, 13,670 ms
--   hnsw               ef=200    -> 94.1% recall,    182 ms
-- Callers must also raise `hnsw.ef_search` above the query LIMIT — see
-- _tune_ann_search() in app/rag.py.
CREATE INDEX IF NOT EXISTS idx_chunks_embedding_hnsw
  ON chunks USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);

-- Metadata lookups used by the Related-passages seed query. Without these the
-- seed resolution seq-scans the whole chunks table on every request.
-- Existing deployments: see db/migrations/002_chunks_metadata_indexes.sql
CREATE INDEX IF NOT EXISTS idx_chunks_meta_id ON chunks ((metadata->>'_id'));
CREATE INDEX IF NOT EXISTS idx_chunks_meta_layer_kind ON chunks ((metadata->>'layer_kind'));
