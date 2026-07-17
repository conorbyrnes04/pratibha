# Pratibha

Pratibha is a multi-tradition wisdom study platform: layered canonical texts (translation, commentary, key terms, practice), a chat interface with optional semantic retrieval, and clients for web and mobile.

**Stack:** FastAPI backend · Next.js web · Expo (React Native) mobile · PostgreSQL + pgvector (optional, for RAG)

---

## Quick start

After cloning, a colleague can run the web app locally in a few minutes. RAG and mobile on a physical device need extra steps below.

**Collaborators:** see **[COLLABORATOR_SETUP.md](COLLABORATOR_SETUP.md)** (GitHub + optional embeddings bundle via AirDrop).

### Prerequisites

| Tool | Notes |
|------|--------|
| **Python 3.11+** | Backend and corpus scripts |
| **Node.js 18+** | Web and mobile |
| **Docker** | Only if you enable RAG (`USE_RAG=true`) |
| **LLM API key** | At least one of OpenRouter, Groq, or OpenAI (see `.env.example`) |

### 1. Environment

```bash
git clone <repository-url>
cd pratibha
cp .env.example .env
```

Edit `.env` and set at least one chat provider key. Defaults work without Postgres: `USE_RAG=false` loads the corpus from disk and chat uses the configured LLM.

### 2. Python backend

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Web frontend

```bash
cd web && npm install && cd ..
```

### 4. Run API + web

```bash
./scripts/dev.sh
```

- **Web:** [http://localhost:3000](http://localhost:3000)
- **API:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Health check:** `curl http://127.0.0.1:8000/health`

`dev.sh` starts uvicorn (reload watches `app/` only) and Next.js. It expects a `.venv` in the repo root. Override ports with `API_PORT` / `WEB_PORT` if needed.

**Alternative:** `python scripts/start_app.py` (same idea, uses your active Python instead of `.venv/bin/uvicorn`).

---

## Optional: RAG (pgvector)

Chat works without a database. Enable RAG when you want retrieval over embedded passage chunks.

```bash
docker compose up -d          # Postgres + pgvector on :5432; Adminer UI on :8081
```

In `.env`:

```bash
USE_RAG=true
OPENAI_API_KEY=...          # required for embeddings
```

Ingest the canonical corpus:

```bash
source .env
python scripts/ingest_pgvector.py --dir data/canonical
```

---

## Mobile (Expo Go on iPhone)

See **[mobile/README.md](mobile/README.md)** for full detail. Summary:

1. Start the API so your phone can reach it (LAN IP, not `127.0.0.1`):

   ```bash
   source .env
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir app
   ```

2. In another terminal:

   ```bash
   cd mobile
   npm install
   EXPO_PUBLIC_API_BASE=http://YOUR_LAN_IP:8000 npx expo start --port 8082
   ```

   Use `--port 8082` because Docker Adminer binds **8081** on the host. Scan the QR code with Expo Go.

3. Or set the API URL in the app **Settings** screen (persisted on device).

---

## Repository layout

```
pratibha/
├── app/                 # FastAPI: /verses, /chat, /daily, /sources, …
├── web/                 # Next.js UI (chat, read, learn, journal, sources)
├── mobile/              # Expo app (Expo Router)
├── data/
│   ├── canonical/       # Live corpus (~890 units); API loads this by default
│   ├── yaml/            # Legacy / pipeline YAML (used if canonical/ missing)
│   ├── raw_texts/       # Source extracts and PD anchors
│   │   └── pd/          # Public-domain reference archive — see pd/README.md
│   └── pratibha_md/     # Intermediate Pratibha markdown (authoring)
├── scripts/             # Ingestion, validation, collection pilots
├── db/init/             # Postgres schema (pgvector)
└── references/          # Editorial standards (editorial-standards.md)
```

The API reads YAML from `data/canonical/` when that directory exists (`app/data_loader.py`). Units expose `pratibha_layers` (original, translation, commentary, key terms, resonances, practice) and `editorial_maturity` (`publishable` → `structural_draft`).

**Pilot collections (recent):**

| Collection | Status |
|------------|--------|
| **Milarepa — Songs** | 8 songs in canonical (`milarepa_songs/`) |
| **Plotinus Enneads** | Pilot treatises I.6, V.1, VI.9 (`plotinus_enneads/`) |
| **Chāndogya Upaniṣad** | Pilot units in `data/yaml/` and raw extracts; promotion to canonical in progress |

Attribution and licensing notes: `GET /sources` and `app/sources_registry.py`.

---

## Common commands

| Task | Command |
|------|---------|
| Dev servers | `./scripts/dev.sh` |
| Validate canonical YAML | `python scripts/validate_canonical.py` |
| Ingest vectors | `python scripts/ingest_pgvector.py --dir data/canonical` |
| Fetch PD texts from manifest | `python scripts/fetch_pd_sources.py` |
| Web lint | `cd web && npm run lint` |

Corpus validation:

```bash
python scripts/validate_canonical.py
```

Script catalog (maintainers): [scripts/README.md](scripts/README.md).

---

## Configuration

Copy [.env.example](.env.example). Important variables:

- **Chat:** `OPENROUTER_API_KEY`, `GROQ_API_KEY`, or `OPENAI_API_KEY` — first configured provider wins
- **Model:** `DEFAULT_MODEL` (e.g. `openrouter/meta-llama/llama-3.3-70b-instruct`)
- **RAG:** `USE_RAG`, `EMBEDDING_MODEL`, `PG_*` / `PG_DSN`
- **Web → API:** `NEXT_PUBLIC_API_BASE` (set automatically by `dev.sh`)

Editorial contract and maturity levels: [references/editorial-standards.md](references/editorial-standards.md).

---

## API (sketch)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Liveness + corpus load stats |
| GET | `/verses` | List units (`?min_maturity=strong_draft`) |
| GET | `/verse/{id}` | Single unit |
| GET | `/daily`, `/random` | Curated / random unit |
| GET | `/collections`, `/sources` | Browse metadata |
| POST | `/chat`, `/chat.stream` | LLM chat; optional RAG context |

---

## Troubleshooting

**`dev.sh`: `.venv/bin/uvicorn` not found** — Create the venv and install requirements (step 2 above).

**Chat returns errors** — Confirm at least one LLM key in `.env` and run `source .env` before starting the API.

**RAG returns nothing** — Postgres must be up, `USE_RAG=true`, and ingest completed with a valid `OPENAI_API_KEY`.

**Mobile cannot reach API** — Use `--host 0.0.0.0`, set `EXPO_PUBLIC_API_BASE` to your machine's LAN IP (not `127.0.0.1`), same Wi‑Fi as the phone.

**Expo port conflict** — Adminer uses host port **8081**; start Metro with `--port 8082`.

**Database reset** — `docker compose down -v && docker compose up -d`, then re-run ingest.

---

## License

MIT — see [LICENSE](LICENSE).
