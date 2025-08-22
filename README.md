# Pratibha — Personal Śāstra & Meditation (FastAPI + pgvector + Web UI)

Welcome to your luminous study space. This repo is **beginner-friendly** and ships a working model:
- Web UI with Tantrik aesthetic (indigo + gold, yantra header)
- FastAPI backend with Groq fast-path + OpenAI fallback
- Optional RAG using **pgvector** (Postgres) + simple ingest script
- Sample Śiva Sūtra YAML corpus (several complete + safe stubs)
- EPUB/PDF → YAML helpers (best-effort draft makers)

## Quick start (no RAG, just chat + daily verse)
```bash
pip install -r requirements.txt
cp .env.example .env
# paste your keys in .env (Groq required for chat)
uvicorn app.main:app --reload
# open http://127.0.0.1:8000/
```

## Add pgvector RAG (optional, recommended)
1) Start Postgres with pgvector:
```bash
docker compose up -d
# Adminer UI: http://127.0.0.1:8081  (user: postgres, pass: postgres, db: pratibha)
```

2) Create tables (docker compose already runs init SQL).

3) Embed and ingest YAML into pgvector (requires OpenAI key for embeddings):
```bash
export USE_RAG=true
python scripts/ingest_pgvector.py --dir data/yaml/siva_sutra
```

4) Now the `/chat` endpoint can include RAG context when you send `use_rag: true`.
The Web UI toggle “Use RAG” also sends this flag.

## What’s in here
```
app/        # FastAPI app (LLM wrapper, RAG helpers, routes)
web/        # Elegant front-end (static)
data/yaml/  # Your corpus (Śiva Sūtra starter)
scripts/    # Importers + EPUB/PDF → YAML helpers + pgvector ingest
db/         # docker-compose and init SQL for pgvector
```

## Env vars
Copy `.env.example` → `.env` and fill:
- `GROQ_API_KEY` (required for fast replies)
- `OPENAI_API_KEY` (optional but needed for embeddings/RAG)
- You can tweak defaults like model names and timeouts.

## Notes
- The YAML stubs for additional sūtras are **placeholders** so the app lists the whole text tree.
  Fill the Sanskrit/transliteration/translation when you’re ready; the app won’t break.
- All code files include gentle comments so you can understand the flow.
- Images in `web/assets` are from your uploads and set as header/texture.

May Pratibha speak clearly ✨
