#!/usr/bin/env bash
# Stable local dev: API + Next.js. Uvicorn reload watches app/ only (not data/, scripts/, web/).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

API_PORT="${API_PORT:-8000}"
WEB_PORT="${WEB_PORT:-3000}"
RELOAD="${RELOAD:-1}"

echo "Stopping stale dev servers on :${API_PORT} and :${WEB_PORT}..."
pkill -f "uvicorn app.main:app" 2>/dev/null || true
if lsof -tiTCP:"${WEB_PORT}" -sTCP:LISTEN >/dev/null 2>&1; then
  lsof -tiTCP:"${WEB_PORT}" -sTCP:LISTEN | xargs kill -9 2>/dev/null || true
fi
sleep 1

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

export NEXT_PUBLIC_API_BASE="${NEXT_PUBLIC_API_BASE:-http://127.0.0.1:${API_PORT}}"

API_HOST="${API_HOST:-127.0.0.1}"
UVICORN=(.venv/bin/uvicorn app.main:app --host "${API_HOST}" --port "${API_PORT}")
if [[ "${RELOAD}" == "1" ]]; then
  UVICORN+=(--reload --reload-dir app)
else
  echo "RELOAD=0 — API will not auto-restart on file changes."
fi

echo "Starting API on http://${API_HOST}:${API_PORT} (reload: app/ only)..."
"${UVICORN[@]}" &
BACKEND_PID=$!

echo "Starting web on http://localhost:${WEB_PORT}..."
(
  cd web
  npm run dev -- --port "${WEB_PORT}"
) &
WEB_PID=$!

cleanup() {
  kill "${BACKEND_PID}" "${WEB_PID}" 2>/dev/null || true
  wait "${BACKEND_PID}" "${WEB_PID}" 2>/dev/null || true
}
trap cleanup INT TERM EXIT

echo "Dev servers running (Ctrl+C to stop)."
wait
