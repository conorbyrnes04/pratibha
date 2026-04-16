from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Any, List
import json
import os
import random
import re
import asyncpg

from .config import settings
from .llm import chat_completion, smart_chat
from .rag import retrieve_context, retrieve_context_compare
from .data_loader import ALL_VERSES, pick_daily
from .collection_aliases import (
    belongs_to_selection,
    meta_collection_slug,
    validate_registered_collections,
)

app = FastAPI(title="Pratibha API", version="0.9")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_missing_aliases = validate_registered_collections(
    str(v.get("collection", "")).strip() for v in ALL_VERSES if str(v.get("collection", "")).strip()
)
if _missing_aliases:
    raise RuntimeError(
        "Missing collection alias entries for loaded collections: " + ", ".join(sorted(_missing_aliases))
    )

# ---- Data endpoints ----
@app.get("/health")
async def health():
    return {"ok": True, "items": len(ALL_VERSES)}


@app.get("/verses")
async def list_verses():
    return {"items": ALL_VERSES}

@app.get("/verse/{sid}")
async def get_verse(sid: str):
    for v in ALL_VERSES:
        if v.get("_id")==sid:
            return v
    raise HTTPException(404, "Not found")

@app.get("/daily")
async def daily():
    v = pick_daily()
    return v or {}


@app.get("/random")
async def random_verse(collection: str | None = None):
    items = ALL_VERSES
    if collection:
        needle = collection.strip().lower()
        items = [v for v in ALL_VERSES if str(v.get("collection", "")).strip().lower() == needle]
    if not items:
        return {}
    return random.choice(items)


@app.get("/collections")
async def collections():
    names = sorted(
        {
            str(v.get("collection", "")).strip()
            for v in ALL_VERSES
            if str(v.get("collection", "")).strip()
        }
    )
    return {"items": names}


@app.get("/admin/corpus-status")
async def corpus_status(request: Request):
    host = (request.client.host if request.client else "") or ""
    if host not in {"127.0.0.1", "::1", "localhost"}:
        raise HTTPException(403, "Forbidden")

    loaded_counts: dict[str, int] = {}
    for v in ALL_VERSES:
        slug = meta_collection_slug(v)
        if slug:
            loaded_counts[slug] = loaded_counts.get(slug, 0) + 1

    pg_counts: dict[str, int] = {}
    last_ingestion: dict[str, str] = {}
    error: str | None = None
    conn: asyncpg.Connection | None = None
    try:
        conn = await asyncpg.connect(
            user=settings.PG_USER,
            password=settings.PG_PASSWORD,
            database=settings.PG_DB,
            host=settings.PG_HOST,
            port=settings.PG_PORT,
        )
        rows = await conn.fetch("SELECT metadata FROM chunks")
        for row in rows:
            meta = row.get("metadata") or {}
            if isinstance(meta, str):
                try:
                    meta = json.loads(meta)
                except Exception:
                    meta = {}
            coll = meta_collection_slug(meta if isinstance(meta, dict) else {})
            if not coll:
                continue
            pg_counts[coll] = pg_counts.get(coll, 0) + 1
            ts = str((meta or {}).get("ingested_at", "")).strip()
            if ts and (coll not in last_ingestion or ts > last_ingestion[coll]):
                last_ingestion[coll] = ts
    except Exception as e:
        error = str(e)
    finally:
        if conn is not None:
            await conn.close()

    yaml_collections: set[str] = set()
    yaml_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "yaml")
    if os.path.isdir(yaml_root):
        for name in os.listdir(yaml_root):
            p = os.path.join(yaml_root, name)
            if os.path.isdir(p):
                yaml_collections.add(meta_collection_slug({"collection": name}))

    absent_from_pgvector = sorted([c for c in yaml_collections if c and c not in pg_counts])
    return {
        "loaded_units_per_collection": dict(sorted(loaded_counts.items())),
        "pgvector_chunks_per_collection": dict(sorted(pg_counts.items())),
        "last_ingestion_timestamp_per_collection": dict(sorted(last_ingestion.items())),
        "yaml_collections_absent_from_pgvector": absent_from_pgvector,
        "pgvector_error": error,
    }


# ---- Chat ----
class ChatReq(BaseModel):
    messages: List[dict]
    model: str | None = None
    temperature: float = 0.2
    use_rag: bool | None = None
    compare_mode: bool = False
    compare_collections: list[str] = []

def persona():
    return {
        "role": "system",
        "content": (
            "You are Pratibha, a luminous and practical study companion for spiritual texts. "
            "Be clear, grounded, and kind. If context is provided, prioritize it and avoid hallucinations. "
            "If the user asks multiple questions, or asks a follow-up/paradoxical question, answer the most recent explicit question first. "
            "Start with a short '## Direct answer' section before the structured sections. "
            "Answer in markdown with this exact structure:\n"
            "## Plain-language explanation\n"
            "## Source-grounded insight\n"
            "## Concrete practice suggestion\n"
            "## Reflection question\n\n"
            "In 'Source-grounded insight', cite source numbers like [1], [2] when context is available. "
            "If context is weak or missing, clearly say what is uncertain instead of guessing."
        ),
    }


def _use_rag_flag(req: ChatReq) -> bool:
    return settings.USE_RAG if req.use_rag is None else req.use_rag


def _llm_configured() -> bool:
    return bool(
        (settings.OPENAI_API_KEY or "").strip()
        or (settings.GROQ_API_KEY or "").strip()
        or (settings.OPENROUTER_API_KEY or "").strip()
    )


@app.post("/chat")
async def chat(req: ChatReq):
    msgs = [persona(), *req.messages]
    latest_user = next((m["content"] for m in reversed(req.messages) if m["role"] == "user"), "")
    if latest_user:
        q_count = len(re.findall(r"\?", latest_user))
        if q_count >= 1:
            msgs.append(
                {
                    "role": "system",
                    "content": (
                        "Respond directly to the user's latest explicit question first in 1-3 sentences, "
                        "then continue with the full structured response."
                    ),
                }
            )
    sources: list[dict[str, Any]] = []
    compare_warning = ""
    if _use_rag_flag(req):
        q = next((m["content"] for m in reversed(req.messages) if m["role"]=="user"), "")
        compare_cols = [c.strip() for c in (req.compare_collections or []) if c and c.strip()]
        compare_enabled = bool(
            req.compare_mode
            and len(compare_cols) >= 2
            and compare_cols[0].lower() != compare_cols[1].lower()
        )
        if compare_enabled:
            ctx = await retrieve_context_compare(q, collections=compare_cols[:2], per_collection=2)
        else:
            ctx = await retrieve_context(q, k=4)
        if ctx:
            if compare_enabled:
                msgs.append(
                    {
                        "role": "system",
                        "content": (
                            f"Comparative mode is active between '{compare_cols[0]}' and '{compare_cols[1]}'. "
                            "Present both voices faithfully before synthesis. "
                            "Use this structure:\n"
                            "## Direct answer\n"
                            "## Voice A\n"
                            "## Voice B\n"
                            "## Convergences\n"
                            "## Tensions\n"
                            "## Practical synthesis\n"
                            "## Reflection question\n"
                            "In Voice A/Voice B, cite source numbers like [1], [2]."
                        ),
                    }
                )
            ctx_txt = "\n\n".join([f"[{i+1}] {t}" for i,(t,_,_) in enumerate(ctx)])
            msgs.append({"role":"system","content":f"Context:\n{ctx_txt}\nUse only if relevant."})
            for i, (text, metadata, score) in enumerate(ctx, start=1):
                meta = metadata or {}
                side = ""
                if compare_enabled and len(compare_cols) >= 2:
                    if belongs_to_selection(meta, compare_cols[0]):
                        side = "A"
                    elif belongs_to_selection(meta, compare_cols[1]):
                        side = "B"
                sources.append({
                    "rank": i,
                    "score": score,
                    "text": text,
                    "metadata": {**meta, "compare_side": side} if side else meta,
                })
            if compare_enabled:
                a = sum(1 for s in sources if str((s.get("metadata") or {}).get("compare_side", "")) == "A")
                b = sum(1 for s in sources if str((s.get("metadata") or {}).get("compare_side", "")) == "B")
                if a == 0 or b == 0:
                    missing = compare_cols[0] if a == 0 else compare_cols[1]
                    compare_warning = f"Insufficient source material found for {missing} on this question."
                elif a < 2 or b < 2:
                    compare_warning = "One voice has sparse direct evidence for this question."
        elif compare_enabled:
            msgs.append(
                {
                    "role": "system",
                    "content": (
                        "Comparative retrieval returned sparse evidence for one or both selected texts. "
                        "Acknowledge this clearly and provide a cautious high-level comparison only."
                    ),
                }
            )
    if not _llm_configured():
        fallback = (
            "Study chat is not fully configured yet because no LLM API key is set. "
            "Add OPENAI_API_KEY, GROQ_API_KEY, or OPENROUTER_API_KEY in your .env file, then restart the backend. "
        )
        if sources:
            fallback += "\n\nMeanwhile, here is a relevant source passage:\n\n" + (sources[0].get("text") or "")
        else:
            fallback += "\n\nYou can still use Read/Random pages to study the imported texts."
        return {"answer": fallback, "sources": sources, "compare_warning": compare_warning}
    try:
        text = await smart_chat(msgs, primary_model=req.model or settings.DEFAULT_MODEL)
        return {"answer": text, "sources": sources, "compare_warning": compare_warning}
    except Exception as e:
        err = str(e)
        lower = err.lower()
        if "free-models-per-day" in lower or ("429" in lower and "openrouter" in lower):
            fallback = (
                "OpenRouter free-tier daily limit is currently exhausted for this key. "
                "Add credits in OpenRouter, or set GROQ_API_KEY/OPENAI_API_KEY in .env, then retry."
            )
        else:
            fallback = (
                "I could not reach the configured chat model right now. "
                "Please check your API key/model settings in .env and try again."
            )
        return {"answer": fallback, "sources": sources, "compare_warning": compare_warning, "error": str(e)}

@app.post("/chat.stream")
async def chat_stream(req: ChatReq):
    msgs = [persona(), *req.messages]
    if _use_rag_flag(req):
        q = next((m["content"] for m in reversed(req.messages) if m["role"]=="user"), "")
        compare_cols = [c.strip() for c in (req.compare_collections or []) if c and c.strip()]
        compare_enabled = bool(
            req.compare_mode
            and len(compare_cols) >= 2
            and compare_cols[0].lower() != compare_cols[1].lower()
        )
        if compare_enabled:
            ctx = await retrieve_context_compare(q, collections=compare_cols[:2], per_collection=2)
        else:
            ctx = await retrieve_context(q, k=4)
        if ctx:
            if compare_enabled:
                msgs.append(
                    {
                        "role": "system",
                        "content": (
                            f"Comparative mode is active between '{compare_cols[0]}' and '{compare_cols[1]}'. "
                            "Present both voices faithfully before synthesis."
                        ),
                    }
                )
            ctx_txt = "\n\n".join([f"[{i+1}] {t}" for i,(t,_,_) in enumerate(ctx)])
            msgs.append({"role":"system","content":f"Context:\n{ctx_txt}\nUse only if relevant."})
    if not _llm_configured():
        async def no_key_gen():
            payload = {
                "object": "chat.error",
                "message": "Missing OPENAI_API_KEY/GROQ_API_KEY/OPENROUTER_API_KEY for streaming chat.",
            }
            yield f"data: {json.dumps(payload)}\n\n"

        return StreamingResponse(no_key_gen(), media_type="text/event-stream")
    try:
        resp = await chat_completion(msgs, model=req.model or settings.DEFAULT_MODEL, temperature=req.temperature, stream=True)
    except Exception as e:
        raise HTTPException(500, str(e))
    async def gen():
        async for line in resp.aiter_lines():
            if line and line.startswith("data: "):
                yield line + "\n"
    return StreamingResponse(gen(), media_type="text/event-stream")
