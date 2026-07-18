#!/usr/bin/env bash
# Sync local .env secrets to the Render API service and trigger a deploy.
# Usage:
#   export RENDER_API_KEY=rnd_...   # Dashboard → Account Settings → API Keys
#   ./scripts/sync_render_env.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="${ROOT}/.env"
: "${RENDER_API_KEY:?Set RENDER_API_KEY (Dashboard → Account Settings → API Keys)}"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing $ENV_FILE" >&2
  exit 1
fi

SERVICE_ID="$(
  curl -sS -H "Authorization: Bearer ${RENDER_API_KEY}" \
    "https://api.render.com/v1/services?limit=50" \
  | python3 -c '
import json, sys
rows = json.load(sys.stdin)
for row in rows:
    svc = row.get("service", row)
    name = svc.get("name") or ""
    if name in ("pratibha-1", "pratibha-api", "pratibha"):
        print(svc["id"])
        break
else:
    raise SystemExit("Could not find pratibha / pratibha-1 service in this Render account")
'
)"
echo "Using Render service: ${SERVICE_ID}"

ENV_JSON="$(
  ENV_FILE="$ENV_FILE" python3 - <<'PY'
import json, os
from pathlib import Path

vals = {}
for line in Path(os.environ["ENV_FILE"]).read_text().splitlines():
    if not line.strip() or line.strip().startswith("#") or "=" not in line:
        continue
    k, v = line.split("=", 1)
    vals[k.strip()] = v.strip().strip('"').strip("'")

for required in ("DATABASE_URL", "OPENROUTER_API_KEY", "OPENAI_API_KEY"):
    if not vals.get(required):
        raise SystemExit(f"Missing {required} in .env")

need = [
    {"key": "USE_RAG", "value": "true"},
    {"key": "PG_SSL", "value": "true"},
    {"key": "VECTOR_BACKEND", "value": "pgvector"},
    {"key": "EMBEDDING_MODEL", "value": vals.get("EMBEDDING_MODEL", "text-embedding-3-small")},
    {"key": "DEFAULT_MODEL", "value": vals.get("DEFAULT_MODEL", "openrouter/anthropic/claude-haiku-4.5")},
    {"key": "OPENROUTER_MODEL", "value": vals.get("OPENROUTER_MODEL", "openrouter/anthropic/claude-haiku-4.5")},
    {"key": "OPENROUTER_APP_NAME", "value": vals.get("OPENROUTER_APP_NAME", "Pratibha")},
    {"key": "CHAT_RATE_MAX_PER_MIN", "value": "20"},
    {
        "key": "CORS_ALLOW_ORIGINS",
        "value": "https://pratibha.agniagama.com,https://pratibha.conorbyrnes04.workers.dev",
    },
    {"key": "DATABASE_URL", "value": vals["DATABASE_URL"]},
    {"key": "OPENROUTER_API_KEY", "value": vals["OPENROUTER_API_KEY"]},
    {"key": "OPENAI_API_KEY", "value": vals["OPENAI_API_KEY"]},
]
print(json.dumps(need))
PY
)"

curl -sS -X PUT "https://api.render.com/v1/services/${SERVICE_ID}/env-vars" \
  -H "Authorization: Bearer ${RENDER_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "${ENV_JSON}" \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); print("env vars updated:", len(d) if isinstance(d, list) else d)'

curl -sS -X POST "https://api.render.com/v1/services/${SERVICE_ID}/deploys" \
  -H "Authorization: Bearer ${RENDER_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{}' \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); print("deploy started:", d.get("id") or d)'

echo "Wait 2–5 minutes, then:"
echo "  curl -sS https://pratibha-1.onrender.com/health"
echo "  curl -sS 'https://pratibha-1.onrender.com/verse/heart_sutra.hs_001/related?limit=6'"
