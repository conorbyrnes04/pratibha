# Collaborator setup

Quick path for someone joining the project. The **code and corpus** live on GitHub; **pre-built embeddings** are shared separately (AirDrop / Drive) so you can skip ingest.

## 1. Clone the repo

```bash
git clone <repository-url>
cd pratibha
cp .env.example .env
```

Edit `.env`:

- `OPENROUTER_API_KEY` — required for chat
- `OPENAI_API_KEY` or keep OpenRouter only — needed only if you **re-run ingest** later
- `USE_RAG=true` — if you restored the embeddings bundle (step 3)

## 2. App dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd web && npm install && cd ..
```

## 3. Embeddings (pick one)

### Option A — Restore the AirDrop bundle (fast)

See **`INSTALL.md`** inside `pratibha-embeddings-bundle.zip`.

Summary:

```bash
docker compose up -d
# from the unzipped bundle folder:
./restore.sh
```

Then set `USE_RAG=true` in `.env`.

### Option B — Rebuild embeddings yourself

```bash
docker compose up -d
source .env
python scripts/ingest_pgvector.py --dir data/canonical
```

Uses `text-embedding-3-small` via OpenRouter or OpenAI (whichever key is set). Takes longer and uses API credits, but stays in sync if the corpus changed after the bundle was made.

## 4. Run locally

```bash
./scripts/dev.sh
```

- API: http://127.0.0.1:8000  
- Web: http://localhost:3000  

## 5. After you pull corpus changes

If YAML under `data/canonical/` changed:

- **Re-ingest** the affected collection, or run full ingest again, **or**
- Ask for an updated embeddings bundle.

Ingest is idempotent per file (safe to re-run).

## Verify RAG

With the API running and `USE_RAG=true`:

```bash
curl -s http://127.0.0.1:8000/admin/corpus-status | python3 -m json.tool
```

You should see `pgvector_chunks_per_collection` populated (admin token only if `ADMIN_TOKEN` is set in `.env`).
