# Web frontend

Next.js app for Pratibha. **Setup and run instructions:** see the root [README](../README.md).

```bash
# From repo root (recommended)
./scripts/dev.sh

# Or web only (API must already be running)
cd web && npm install && npm run dev
```

App routes: `/` (home), `/read`, `/chat`, `/learn`, `/journal`, `/daily`, `/random`, `/sources`.

API base URL: `NEXT_PUBLIC_API_BASE` (default `http://127.0.0.1:8000`, set by `dev.sh`).
