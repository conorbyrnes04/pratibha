# Pratibha FastAPI backend — production image.
# Builds the API plus the canonical corpus it serves from disk.
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install dependencies first so layer caching survives code edits.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Application code.
COPY app ./app

# The API loads the corpus from disk (data/canonical preferred). Only the
# canonical corpus is baked in; the larger raw_texts/yaml/pratibha_md trees are
# authoring inputs and are not needed at runtime.
COPY data/canonical ./data/canonical

# Ingest script + DB schema (handy for one-off jobs / reference inside the image).
COPY scripts/ingest_pgvector.py ./scripts/ingest_pgvector.py
COPY db ./db

# Railway/Render inject $PORT; default to 8000 for local `docker run`.
ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
