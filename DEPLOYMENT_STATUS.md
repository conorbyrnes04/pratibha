# Pratibha Deployment Status

**Date**: Sunday, Aug 30, 2026, 3:28 PM UTC  
**Build Fix**: Merged to main (commit `e5b262f7`)  
**Site URL**: https://pratibha.agniagama.com

---

## ✅ What's Working

### 1. Build & Deployment
- **Fixed**: Next.js 16 Suspense boundary error in `/read` page
- **Status**: Successfully built and deployed to Vercel
- **PR**: [#5 - Fix Next.js 16 build error](https://github.com/conorbyrnes04/pratibha/pull/5)

### 2. Infrastructure
- **Frontend**: Vercel ✅ (auto-deploys from `main` branch)
- **Backend**: Render API ✅ (responding after cold start)
- **DNS**: Squarespace → Vercel CNAME ✅ (pratibha.agniagama.com resolves correctly)

### 3. Pages Tested
- ✅ Homepage: https://pratibha.agniagama.com
- ✅ Library/Read page: https://pratibha.agniagama.com/read (fixed!)
- ✅ Backend health: https://pratibha-api.onrender.com/health

---

## ⚠️ Action Required: Corpus Ingest

The backend API is running but shows:
```json
{
  "ok": true,
  "ready": false,
  "items": 0
}
```

**This means the database doesn't have the corpus loaded yet.**

### To Fix (One-Time Setup):

Run the corpus ingest script against the production Render database:

```bash
cd /workspace

# You'll need these from Render dashboard:
# 1. Go to https://dashboard.render.com
# 2. Find pratibha-db → Connection → External connection string

export PG_SSL=true
export DATABASE_URL="postgresql://USER:PASSWORD@EXTERNAL_HOST/DBNAME"
export OPENAI_API_KEY="sk-..."  # Or OPENROUTER_API_KEY

python scripts/ingest_pgvector.py --dir data/canonical
```

**Expected output**: `Inserted N chunks ... from 906 files.`

After ingest completes:
- `/health` will show `"ready": true, "items": 906`
- Library page will show passages
- Chat will work with RAG retrieval

---

## 🧪 Full Test Plan (After Corpus Ingest)

### Frontend Tests
- [ ] Homepage loads
- [ ] Library page shows passage list
- [ ] Click a passage → layers render
- [ ] Search/filter works
- [ ] Theme filtering works
- [ ] Daily passage loads
- [ ] Learning paths work

### Backend Tests
```bash
# 1. Health check shows ready
curl https://pratibha-api.onrender.com/health | jq '.ready, .items'

# 2. Verses endpoint returns data
curl https://pratibha-api.onrender.com/verses | jq 'length'

# 3. Daily passage works
curl https://pratibha-api.onrender.com/daily | jq '.title'

# 4. RAG chat works
curl -X POST https://pratibha-api.onrender.com/chat \
  -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"What does Heraclitus say about change?"}],"use_rag":true}' \
  | jq '.answer'
```

### Integration Tests
- [ ] No CORS errors in browser console
- [ ] Chat responses include source citations
- [ ] Journal saves to localStorage
- [ ] All navigation links work

---

## 📝 Deployment Architecture

```
┌─────────────────────────────────────────┐
│  pratibha.agniagama.com (Squarespace)   │
│  CNAME → cname.vercel-dns.com           │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  Vercel (Frontend - Next.js)            │
│  Auto-deploys from main branch          │
│  Root: /workspace/web                   │
└────────────────┬────────────────────────┘
                 │
                 │ NEXT_PUBLIC_API_BASE
                 ▼
┌─────────────────────────────────────────┐
│  Render (Backend - FastAPI)             │
│  https://pratibha-api.onrender.com      │
│  Dockerfile build                       │
└────────────────┬────────────────────────┘
                 │
                 │ DATABASE_URL (internal)
                 ▼
┌─────────────────────────────────────────┐
│  Render Postgres + pgvector             │
│  ⚠️ Free tier (expires ~30 days)        │
│  Status: Empty (needs ingest)           │
└─────────────────────────────────────────┘
```

---

## 💰 Current Tier

**Free Trial** - $0/month with caveats:
- ✅ Vercel Hobby: Generous, no expiry
- ⚠️ Render Free Web: Cold starts after 15min idle (~1min wake)
- ⚠️ Render Free DB: **Expires after 30 days**, no backups

**Upgrade Path** (~$13/month for production):
- Edit `render.yaml`: Change `plan: free` → `plan: starter` (web) and `plan: basic-256mb` (DB)
- Redeploy via Render dashboard

---

## 🎉 Summary

✅ **Build fixed and deployed!**  
✅ **All infrastructure running**  
⚠️ **Next step**: Run corpus ingest to populate the database

Once the corpus is ingested, the full app will be operational with:
- 906 passages across 15 wisdom traditions
- RAG-powered study chat
- Daily passages, learning paths, and journal
