# Deploying Pratibha (public MVP)

This guide deploys the **full** app for a public launch:

- **Frontend** — Next.js (`web/`) on **Vercel**
- **Backend** — FastAPI (`app/`) on **Render** (Docker)
- **Database** — Render Postgres with the **pgvector** extension (powers the live Study chat / RAG)

Everything lives in this one repo. You will **not** commit secrets — keys are set in each platform's dashboard.

---

## Recommended host & why

**Render (backend + Postgres) + Vercel (frontend).**

Why Render over Railway for this app:

| | Render | Railway |
|---|---|---|
| pgvector | Built into **managed** Postgres — `CREATE EXTENSION vector;` just works, with a real DB UI + backups (paid) | Requires deploying a **pgvector container template** (no managed-DB UI, you own more ops) |
| Infra-as-code | `render.yaml` blueprint provisions web **and** DB together and auto-wires `DATABASE_URL` | Per-service config; DB wired manually |
| App↔DB networking | Private internal connection string, no SSL fuss | Private networking available, similar |
| Pricing | Fixed, predictable monthly | Usage-based |
| Free trial | Genuine free web + free Postgres (caveats below) | Trial credits only |

Vercel is the obvious frontend choice (it builds Next.js natively, generous free "Hobby" tier).

> Railway is a perfectly good alternative and is documented at the end ([Appendix A](#appendix-a-deploy-the-backend-on-railway-instead)).

### Rough monthly cost

| Tier | Frontend | Backend | Database | Total |
|---|---|---|---|---|
| **Free trial** (testing only) | Vercel Hobby $0 | Render Free web $0 (cold starts) | Render Free PG $0 (**expires 30 days, no backups**) | **$0** |
| **Recommended launch** | Vercel Hobby $0 | Render Starter ~$7/mo | Render Basic-256mb ~$6/mo | **~$13/mo** |

Plus **LLM usage** (pay-as-you-go to OpenRouter/OpenAI — typically a few dollars/mo at low traffic).

> The free tier is fine to validate the deploy, but the free Postgres **expires after 30 days and has no backups**, and the free web service cold-starts (~1 min) after ~15 min idle — bad for a chat app. For a real public launch use the paid tiers (flip the two `plan:` lines in `render.yaml`).

### Free-tier reality check (this is the plan you're starting with)

You're launching on **Render Free** (backend + Postgres) and **Vercel Hobby** (frontend) — **$0**, for testing. Know the caveats up front:

- **Free Render Postgres expires ~30 days after creation** and has **no backups**. When it expires you lose the DB (and the ingested corpus). Plan to either upgrade to a paid DB or re-provision + re-ingest before day 30.
- **Free Render web service cold-starts**: it spins down after ~15 min idle, so the first request after idle takes ~1 min (the chat will feel slow on the first hit). Subsequent requests are fast.
- **The one-time corpus ingest must run against the production DB before chat or Read works.** A fresh Render Postgres is empty — until you run `scripts/ingest_pgvector.py` against it (see [One-time corpus ingest](#one-time-corpus-ingest-into-prod-db)), `/chat` and retrieval return nothing. Re-run it any time you re-provision the free DB.
- Vercel Hobby has no such expiry and is fine to keep.

> When you're ready for a real launch, flip the two `plan:` lines in [`render.yaml`](render.yaml) (`free` → `starter` for web, `free` → `basic-256mb` for the DB) and redeploy.

### LLM keys: the simple default

The simplest path is a **single `OPENROUTER_API_KEY`**, set in the **Render dashboard** (never in the repo). It powers **both chat and RAG embeddings**, so you don't need anything else to go live.

- **Optional:** add an `OPENAI_API_KEY` too for **higher-quality embeddings** (`text-embedding-3-small`). If you set it, use the **same** key/model for the one-time ingest and the running API so the vectors match.

---

## Prerequisites

1. Accounts: [Vercel](https://vercel.com), [Render](https://render.com), and this repo pushed to GitHub.
2. **At least one LLM API key.** Simplest: a single **OpenRouter** key powers both chat *and* RAG embeddings.
   - Chat: first match wins → `OPENROUTER_API_KEY` > `GROQ_API_KEY` > `OPENAI_API_KEY`.
   - RAG embeddings: `OPENAI_API_KEY` (preferred) **or** `OPENROUTER_API_KEY`. Groq cannot do embeddings.
   - Without any chat key, the app still runs and **chat fails gracefully** (an error message), while Read/Paths/Daily keep working.
3. `psql` (or any Postgres client) and a local Python env to run the one-time corpus ingest.

---

## Environment variables

### Backend (Render / Railway)

| Var | Required | Example / default | Notes |
|---|---|---|---|
| `USE_RAG` | yes | `true` | Must be `true` for live Study chat with retrieval. |
| `DATABASE_URL` | yes | auto-wired by blueprint | Single Postgres connection string; parsed into `PG_*`. |
| `PG_SSL` | only for external DB | `false` | Auto-on if URL has `?sslmode=require`. Internal Render networking doesn't need it. |
| `CORS_ALLOW_ORIGINS` | yes | `https://pratibha.vercel.app,https://pratibha.agniagama.com` | Comma-separated. Locks the API to your frontend (Vercel default URL + custom domain). |
| `OPENROUTER_API_KEY` | one chat key | `sk-or-...` | Powers chat **and** can power embeddings. |
| `GROQ_API_KEY` | optional | `gsk_...` | Chat only (no embeddings). |
| `OPENAI_API_KEY` | recommended | `sk-...` | Best embeddings for RAG; also a chat fallback. |
| `DEFAULT_MODEL` | optional | `openrouter/meta-llama/llama-3.3-70b-instruct` | |
| `EMBEDDING_MODEL` | optional | `text-embedding-3-small` | **Must match** what you ingest with (1536-dim). |
| `PORT` | injected | — | Render/Railway set this automatically. |

### Frontend (Vercel)

| Var | Required | Example | Notes |
|---|---|---|---|
| `NEXT_PUBLIC_API_BASE` | yes | `https://pratibha-api.onrender.com` | Render backend URL, **no trailing slash**. Read at **build time** — redeploy after changing. |

---

## Part A — Backend + Database on Render

### Option 1: Blueprint (recommended, one click)

1. Push this repo to GitHub.
2. Render dashboard → **New → Blueprint** → select this repo. Render reads [`render.yaml`](render.yaml) and creates:
   - `pratibha-api` (Docker web service, health check `/health`)
   - `pratibha-db` (Postgres 16)
   `DATABASE_URL` is wired automatically from the DB to the API.
3. When prompted, fill the secret env vars (they're marked `sync: false`):
   - `OPENROUTER_API_KEY` (and/or `OPENAI_API_KEY`)
   - `CORS_ALLOW_ORIGINS` — you can leave a placeholder now and set the real Vercel URL after Part B.
4. Click **Apply**. Wait for the API to go live; note its URL, e.g. `https://pratibha-api.onrender.com`.

### Option 2: Manual

1. **New → Postgres** (version 16). After it's ready, copy both the **Internal** and **External** connection strings.
2. **New → Web Service** → this repo → Runtime **Docker** (uses [`Dockerfile`](Dockerfile)). Health check path `/health`.
3. Add env vars from the [backend table](#backend-render--railway). For `DATABASE_URL` use the **Internal** string (same-region, no SSL).

### Enable pgvector + create the schema (once)

Render's managed Postgres supports pgvector; you just enable it and create the table. Run the bundled schema against the DB (use the **External** connection string from your laptop):

```bash
psql "postgresql://USER:PASSWORD@EXTERNAL_HOST/DBNAME?sslmode=require" -f db/init/01_init.sql
```

This runs [`db/init/01_init.sql`](db/init/01_init.sql): `CREATE EXTENSION IF NOT EXISTS vector;` + the `chunks` table + an ivfflat index.

### One-time corpus ingest (into prod DB)

Embed the canonical corpus into pgvector. Run locally (the corpus lives in this repo); point it at the **External** prod DB. `PG_SSL=true` because you're connecting over the public internet:

```bash
# from repo root, with your venv active and deps installed
PG_SSL=true \
DATABASE_URL="postgresql://USER:PASSWORD@EXTERNAL_HOST/DBNAME" \
OPENAI_API_KEY="sk-..." \
python scripts/ingest_pgvector.py --dir data/canonical
```

> Use the **same** embedding key/model here as the running API (`text-embedding-3-small`, 1536-dim). If you only have an OpenRouter key, set `OPENROUTER_API_KEY` instead of `OPENAI_API_KEY` — ingestion supports it. Expect output like `Inserted N chunks ... from 906 files.`

---

## Part B — Frontend on Vercel

1. Vercel dashboard → **Add New → Project** → import this repo.
2. **Root Directory** → set to **`web`** (important — this is a monorepo). Vercel auto-detects Next.js; [`web/vercel.json`](web/vercel.json) pins the build.
3. **Environment Variables** → add:
   - `NEXT_PUBLIC_API_BASE` = your Render backend URL (e.g. `https://pratibha-api.onrender.com`, no trailing slash).
4. **Deploy.** Note the resulting URL, e.g. `https://pratibha.vercel.app`. (The custom domain `https://pratibha.agniagama.com` is added in [Part C](#part-c--custom-domain-on-squarespace-pratibhaagniagamacom).)

### Close the loop (CORS)

Back in Render, set the backend's `CORS_ALLOW_ORIGINS` to **both** the Vercel default URL and your custom domain (comma-separated, no spaces), and let it redeploy:

```
CORS_ALLOW_ORIGINS=https://pratibha.vercel.app,https://pratibha.agniagama.com
```

Include both so the app works whether visitors hit the raw Vercel URL or `pratibha.agniagama.com`. If you change `NEXT_PUBLIC_API_BASE` later, **redeploy the Vercel project** (the value is baked in at build time).

---

## Part C — Custom domain on Squarespace (`pratibha.agniagama.com`)

You already own **agniagama.com** as a Squarespace site. The app stays hosted on **Vercel**; Squarespace is used **only** to point a subdomain at it via DNS. Squarespace **cannot host the Next.js app itself** — it just resolves `pratibha.agniagama.com` to Vercel.

The flow: tell Vercel about the domain → add the matching DNS record in Squarespace → wait for propagation → verify in Vercel.

1. **Vercel → your project → Settings → Domains → Add.** Enter `pratibha.agniagama.com`. Vercel will show it as *Invalid Configuration / Pending* and give you a **target value to point a CNAME at** — typically `cname.vercel-dns.com` (copy the exact value Vercel shows you).
2. **Squarespace → Settings → Domains →** open **agniagama.com → DNS Settings** (Squarespace-managed domain) — *or*, if the domain's nameservers point elsewhere, manage DNS there. Under **Custom Records**, add:

   | Type | Host / Name | Value / Data |
   |---|---|---|
   | `CNAME` | `pratibha` | `cname.vercel-dns.com` *(use the exact target Vercel gave you)* |

   - **Host** is just the subdomain label `pratibha` (Squarespace appends `.agniagama.com` automatically — do **not** type the full domain).
   - **Value** is the Vercel target with **no trailing dot** unless Squarespace requires one.
   - Leave the existing root `agniagama.com` records (your Squarespace site) untouched — you're only adding the `pratibha` subdomain.
3. **Wait for DNS to propagate** — usually minutes, up to ~48h. Check with `dig pratibha.agniagama.com CNAME +short` (should return the Vercel target) or [dnschecker.org](https://dnschecker.org).
4. **Verify in Vercel.** When DNS resolves, the domain flips to **Valid Configuration** and Vercel auto-issues an HTTPS certificate. `https://pratibha.agniagama.com` now serves your app.
5. **Update CORS** (if not already): the backend's `CORS_ALLOW_ORIGINS` on Render must include `https://pratibha.agniagama.com` (see the [close-the-loop](#close-the-loop-cors) step). Redeploy the API if you change it.

> **Squarespace is DNS-only here.** It does not run the app, build Next.js, or proxy traffic — it simply maps the subdomain to Vercel. If `agniagama.com` is on Squarespace's *built-in* DNS, add the CNAME there; if you previously pointed the domain's nameservers at another provider, add the record in that provider instead.

---

## Smoke test checklist

```bash
# 1. Backend liveness + corpus loaded
curl https://pratibha-api.onrender.com/health
# -> {"ok":true,"items":906,...}

# 2. Content endpoints
curl "https://pratibha-api.onrender.com/verses" | head -c 300
curl "https://pratibha-api.onrender.com/daily"

# 3. Chat (RAG end to end — needs DB ingested + an LLM key)
curl -X POST https://pratibha-api.onrender.com/chat \
  -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"What does Heraclitus say about change?"}],"use_rag":true}'
# -> {"answer":"...","sources":[...]}

# 4. CORS lock (should echo your origin, and NOT echo a random one)
curl -s -i -H "Origin: https://pratibha.agniagama.com" https://pratibha-api.onrender.com/health | grep -i access-control-allow-origin
```

In the browser:
- [ ] Load the Vercel URL — **Read** page lists passages.
- [ ] Open a passage — layers render.
- [ ] **Daily** and **Paths/Learn** pages load.
- [ ] **Study chat** — send a message and get a grounded answer with sources.
- [ ] No CORS errors in the browser console.

---

## How chat degrades without a key

The backend treats empty/placeholder keys as unset. With **no** chat provider key, `/chat` returns a graceful error and the UI shows a failure message; **Read, Daily, Paths, and Sources keep working**. With a chat key but **no** embeddings key, chat still answers but RAG retrieval falls back to keyword/lexical search.

---

## Known follow-ups (not blockers)

- **TypeScript debt:** the web app ships with `typescript.ignoreBuildErrors` + `eslint.ignoreDuringBuilds` in [`web/next.config.mjs`](web/next.config.mjs) because the existing codebase has a few pre-existing type errors (the runtime bundle compiles fine). Clean these up later and remove the flags so type checks guard future deploys.
- **pgvector index:** `01_init.sql` uses `ivfflat (lists=100)`. Fine for this corpus; revisit if the corpus grows a lot.
- **`web/.env.local`** (gitignored, dev-only) sets an unused `NEXT_PUBLIC_API_URL`; the code reads `NEXT_PUBLIC_API_BASE`. Harmless locally.

---

## Appendix A — Deploy the backend on Railway instead

1. **New Project → Deploy a Postgres + pgvector template** (Railway's standard Postgres does *not* include pgvector). Note its `DATABASE_URL`.
2. Connect to it once and run the schema: `psql "$DATABASE_URL" -f db/init/01_init.sql` (it enables the extension + creates `chunks`).
3. **New → GitHub Repo** → this repo. Railway reads [`railway.json`](railway.json) (Dockerfile build, start `uvicorn app.main:app --host 0.0.0.0 --port $PORT`, health check `/health`).
4. In the service **Variables**: reference `DATABASE_URL` from the pgvector service, set `USE_RAG=true`, `CORS_ALLOW_ORIGINS`, and your LLM key(s).
5. **Settings → Networking → Generate Domain** for a public URL; use it as `NEXT_PUBLIC_API_BASE` on Vercel.
6. Run the one-time ingest as in Part A (use the public `DATABASE_URL` with `PG_SSL=true`).

Rough cost: Railway Hobby ~$5/mo (usage-based, covers a small API + Postgres at low traffic) + Vercel $0.
