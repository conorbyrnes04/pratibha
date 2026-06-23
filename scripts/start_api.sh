#!/bin/sh
# Render/Railway inject $PORT; default 8000 for local docker run.
set -e
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
