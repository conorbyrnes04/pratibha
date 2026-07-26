from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, field_validator
from typing import Any, List
from contextlib import asynccontextmanager
import asyncio
import json
import logging
import os
import random
import re
import time
import asyncpg

from .chat_voice import (
    ANTI_PATTERNS,
    HARD_RULES,
    PRATIBHA_VOICE_PERSONA,
    SOURCE_GROUNDING,
)
from .voice_examples import is_death_topic, select_few_shots
from .auth import AuthUser, require_user
from .config import settings
from .llm import smart_chat, smart_chat_stream
from .rag import retrieve_context, retrieve_context_compare, retrieve_context_for_verse, retrieve_related_unit_ids, detected_collections
from .data_loader import (
    LOAD_STATS,
    _humanize_collection,
    corpus_ready,
    filter_by_maturity,
    filter_reader_facing,
    get_all_verses,
    get_verse_by_id,
    normalize_maturity,
    pick_daily,
)
from .lexicon_api import find_lemma_passages, get_lemma, get_lexicon, list_lemmas
from .collection_aliases import (
    belongs_to_selection,
    meta_collection_slug,
    validate_registered_collections,
)

logger = logging.getLogger("pratibha.api")


def _warn_missing_aliases(verses: list[dict[str, Any]]) -> None:
    missing = validate_registered_collections(
        str(v.get("collection", "")).strip() for v in verses if str(v.get("collection", "")).strip()
    )
    if missing:
        # Degrade gracefully: a missing alias should not take the whole API down.
        logger.warning(
            "Missing collection alias entries for loaded collections: %s",
            ", ".join(sorted(missing)),
        )


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Bind the port quickly, then load ~900 YAML units in the background."""

    async def _load() -> None:
        verses = await asyncio.to_thread(get_all_verses)
        _warn_missing_aliases(verses)
        # Warm lexicon cache (empty until Agent A seeds data/lexicon/lemmas).
        await asyncio.to_thread(get_lexicon)

    task = asyncio.create_task(_load())
    try:
        yield
    finally:
        task.cancel()


app = FastAPI(title="Pratibha API", version="0.9", lifespan=lifespan)


def _cors_origins() -> list[str]:
    raw = (os.environ.get("CORS_ALLOW_ORIGINS") or "").strip()
    if raw == "*":
        return ["*"]
    if raw:
        return [o.strip() for o in raw.split(",") if o.strip()]
    # Safer production default than "*" when the env var was never set on Render.
    return [
        "https://pratibha.agniagama.com",
        "https://pratibha.conorbyrnes04.workers.dev",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]


_origins = _cors_origins()
# Credentialed requests cannot use the "*" wildcard per the CORS spec, so only
# enable credentials when explicit origins are configured.
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=_origins != ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def _valid_maturity(value: str | None) -> str | None:
    """Validate an incoming min_maturity query param, ignoring junk values."""
    if value is None:
        return None
    normalized = normalize_maturity(value)
    return normalized or None

# ---- Data endpoints ----
@app.get("/health")
async def health():
    # Keep this path free of corpus/DB work so Render cold-starts and load
    # balancers always get a fast liveness signal.
    ready = corpus_ready()
    return {
        "ok": True,
        "ready": ready,
        # `_cached_item_count()` already returns an int — do not wrap in len().
        "items": _cached_item_count() if ready else 0,
        "load_stats": LOAD_STATS if ready else {},
        "config": {
            "openrouter": bool((settings.OPENROUTER_API_KEY or "").strip()),
            "openai": bool((settings.OPENAI_API_KEY or "").strip()),
            "use_rag": bool(settings.USE_RAG),
            "database_url": bool((settings.DATABASE_URL or "").strip()),
            "pg_host": settings.PG_HOST or "",
            "chat_provider": settings.chat_provider(),
            "supabase_auth": bool((settings.SUPABASE_URL or "").strip() or (settings.SUPABASE_JWT_SECRET or "").strip()),
        },
    }


@app.get("/me")
async def me(user: AuthUser = Depends(require_user)):
    """Return the signed-in Supabase user (Authorization: Bearer <access_token>)."""
    return {"id": user.id, "email": user.email}


def _cached_item_count() -> int:
    """Non-blocking count once the corpus is warm (never triggers a load)."""
    from . import data_loader

    verses = getattr(data_loader, "_cached_verses", None)
    return len(verses) if isinstance(verses, list) else 0


@app.get("/verses")
async def list_verses(min_maturity: str | None = None):
    """Library index — slim payloads so the browser isn't handed ~9MB of layers."""
    items = filter_by_maturity(get_all_verses(), _valid_maturity(min_maturity))
    return {"items": [_verse_list_item(v) for v in items]}


def _verse_list_item(v: dict[str, Any]) -> dict[str, Any]:
    """Fields the Library / filters need; omit heavy appendix + full layer bodies."""
    out: dict[str, Any] = {
        "_id": v.get("_id"),
        "collection": v.get("collection"),
        "section": v.get("section"),
        "title": v.get("title"),
        "sutra_id": v.get("sutra_id"),
        "reference": v.get("reference"),
        "sequence": v.get("sequence"),
        "work_id": v.get("work_id"),
        "themes": v.get("themes") or [],
        "editorial_maturity": v.get("editorial_maturity"),
        "editorial_score": v.get("editorial_score"),
        "translation": v.get("translation"),
        "commentary": v.get("commentary"),
        "practice": v.get("practice") or v.get("abhyasa"),
        "insight": v.get("insight"),
    }
    # Keep only the layer kinds used for list previews / search blobs.
    layers = v.get("pratibha_layers")
    if isinstance(layers, list):
        keep = {"translation", "commentary", "practice", "iast", "original"}
        slim_layers = []
        for layer in layers:
            if not isinstance(layer, dict):
                continue
            kind = str(layer.get("kind") or "")
            if kind not in keep:
                continue
            body = layer.get("body")
            if isinstance(body, str) and len(body) > 1200:
                body = body[:1200].rstrip() + "…"
            slim_layers.append({
                "kind": kind,
                "label": layer.get("label"),
                "body": body,
            })
        if slim_layers:
            out["pratibha_layers"] = slim_layers
    return out


@app.get("/verse/{sid}")
async def get_verse(sid: str):
    v = get_verse_by_id(sid)
    if v is None:
        raise HTTPException(404, "Not found")
    return v


@app.get("/verse/{sid}/related")
async def related_verses(sid: str, limit: int = 6):
    """Semantic neighbours for the Related Ideas panel (pgvector + diversity)."""
    verse = get_verse_by_id(sid)
    if verse is None:
        raise HTTPException(404, "Not found")
    cap = max(1, min(limit, 12))
    hits = await retrieve_related_unit_ids(str(verse.get("_id") or sid), limit=cap, per_collection=2)
    items: list[dict[str, Any]] = []
    skipped_missing = 0
    skipped_maturity = 0
    for uid, score, _collection in hits:
        neighbour = get_verse_by_id(uid)
        if neighbour is None:
            skipped_missing += 1
            continue
        # Skip raw drafts so we never send a reader to unfinished work.
        maturity = normalize_maturity(neighbour.get("editorial_maturity"))
        if maturity in {"needs_rewrite", "structural_draft"}:
            skipped_maturity += 1
            continue
        items.append({**neighbour, "related_score": round(score, 4)})
        if len(items) >= cap:
            break
    payload: dict[str, Any] = {"items": items, "mode": "semantic" if items else "empty"}
    if not items:
        payload["debug"] = {
            "hits": len(hits),
            "skipped_missing": skipped_missing,
            "skipped_maturity": skipped_maturity,
            "use_rag": bool(settings.USE_RAG),
            "database_url": bool((settings.DATABASE_URL or "").strip()),
        }
    return payload


@app.get("/daily")
async def daily(min_maturity: str | None = "publishable"):
    v = pick_daily(min_maturity=_valid_maturity(min_maturity))
    return v or {}

@app.get("/random")
async def random_verse(collection: str | None = None, min_maturity: str | None = "strong_draft"):
    items = filter_reader_facing(filter_by_maturity(get_all_verses(), _valid_maturity(min_maturity)))
    if collection:
        needle = collection.strip().lower()
        items = [v for v in items if str(v.get("collection", "")).strip().lower() == needle]
    if not items:
        return {}
    return random.choice(items)


@app.get("/collections")
async def collections():
    names = sorted(
        {
            str(v.get("collection", "")).strip()
            for v in get_all_verses()
            if str(v.get("collection", "")).strip()
        }
    )
    return {"items": names}


@app.get("/sources")
async def sources():
    from .sources_registry import build_sources_payload

    return build_sources_payload(get_all_verses())


@app.get("/lexicon")
async def lexicon_list(
    q: str | None = None,
    tradition: str | None = None,
    limit: int = 100,
):
    """Browse / search lexicon lemmas (cached from data/lexicon/lemmas)."""
    if limit < 0:
        limit = 0
    if limit > 500:
        limit = 500
    return list_lemmas(q=q, tradition=tradition, limit=limit)


@app.get("/lexicon/{lemma_id}/passages")
async def lexicon_lemma_passages(lemma_id: str, limit: int = 30):
    """Slim verse refs whose key_terms mention this lemma (cap ~30)."""
    if get_lemma(lemma_id) is None:
        raise HTTPException(status_code=404, detail="Lemma not found")
    if limit < 0:
        limit = 0
    if limit > 30:
        limit = 30
    return {"items": find_lemma_passages(lemma_id, limit=limit)}


@app.get("/lexicon/{lemma_id}")
async def lexicon_lemma(lemma_id: str):
    """Full lemma document (senses, related, scripts, …)."""
    lemma = get_lemma(lemma_id)
    if lemma is None:
        raise HTTPException(status_code=404, detail="Lemma not found")
    return lemma


@app.get("/admin/corpus-status")
async def corpus_status(request: Request):
    # Behind a proxy (Render/Vercel) request.client.host is the proxy, so a
    # localhost check is meaningless in prod. Gate on a shared secret instead.
    # Set ADMIN_TOKEN in the environment and pass it as `X-Admin-Token`.
    expected = (os.environ.get("ADMIN_TOKEN") or "").strip()
    host = (request.client.host if request.client else "") or ""
    is_local = host in {"127.0.0.1", "::1", "localhost"}
    if expected:
        if request.headers.get("X-Admin-Token", "").strip() != expected:
            raise HTTPException(403, "Forbidden")
    elif not is_local:
        # No token configured: allow only genuine local access (dev convenience).
        raise HTTPException(403, "Forbidden")

    loaded_counts: dict[str, int] = {}
    for v in get_all_verses():
        slug = meta_collection_slug(v)
        if slug:
            loaded_counts[slug] = loaded_counts.get(slug, 0) + 1

    pg_counts: dict[str, int] = {}
    last_ingestion: dict[str, str] = {}
    error: str | None = None
    conn: asyncpg.Connection | None = None
    try:
        conn = await asyncpg.connect(**settings.asyncpg_kwargs())
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
        "load_stats": LOAD_STATS,
        "loaded_units_per_collection": dict(sorted(loaded_counts.items())),
        "pgvector_chunks_per_collection": dict(sorted(pg_counts.items())),
        "last_ingestion_timestamp_per_collection": dict(sorted(last_ingestion.items())),
        "yaml_collections_absent_from_pgvector": absent_from_pgvector,
        "pgvector_error": error,
    }


# ---- Chat ----
# Lightweight in-process per-IP rate limit. Protects the metered LLM from a
# single abusive client. For multi-instance deploys, move this to Redis; for a
# single Render web service it is sufficient.
_CHAT_RATE_MAX = int(os.environ.get("CHAT_RATE_MAX_PER_MIN", "20") or "20")
_chat_hits: dict[str, list[float]] = {}


def _client_ip(request: Request) -> str:
    fwd = (request.headers.get("x-forwarded-for") or "").split(",")[0].strip()
    if fwd:
        return fwd
    return (request.client.host if request.client else "") or "unknown"


def _rate_limited(request: Request) -> bool:
    if _CHAT_RATE_MAX <= 0:
        return False
    now = time.monotonic()
    ip = _client_ip(request)
    window = [t for t in _chat_hits.get(ip, []) if now - t < 60.0]
    if len(window) >= _CHAT_RATE_MAX:
        _chat_hits[ip] = window
        return True
    window.append(now)
    _chat_hits[ip] = window
    # Opportunistic cleanup so the dict can't grow unbounded.
    if len(_chat_hits) > 4096:
        for key in [k for k, v in _chat_hits.items() if not any(now - t < 60.0 for t in v)]:
            _chat_hits.pop(key, None)
    return False


class ChatReq(BaseModel):
    messages: List[dict]
    model: str | None = None
    temperature: float = 0.2
    use_rag: bool | None = None
    compare_mode: bool = False
    compare_collections: list[str] = []
    compare_verse_ids: list[str] = []
    verse_id: str | None = None
    layer_focus: str | None = None
    chat_mode: str | None = None

    @field_validator("messages")
    @classmethod
    def _validate_messages(cls, value: List[dict]) -> List[dict]:
        if not value:
            raise ValueError("messages must not be empty")
        for msg in value:
            if not isinstance(msg, dict) or "role" not in msg or "content" not in msg:
                raise ValueError("each message requires 'role' and 'content'")
            if msg.get("role") not in {"system", "user", "assistant"}:
                raise ValueError(f"invalid message role: {msg.get('role')!r}")
        return value

    @field_validator("temperature")
    @classmethod
    def _validate_temperature(cls, value: float) -> float:
        if not 0.0 <= value <= 2.0:
            raise ValueError("temperature must be between 0 and 2")
        return value

_COMPARE_CUE_RE = re.compile(
    r"\b(vs\.?|versus|compare|comparison|contrast|debate|dialogue|between .+ and)\b",
    re.I,
)
_EXPLORATORY_CUE_RE = re.compile(
    r"\b(imagine|thought experiment|what if|irony|genealog|historical|essay|table)\b",
    re.I,
)


def _is_exploratory_query(query: str) -> bool:
    q = (query or "").strip()
    if not q:
        return False
    if _COMPARE_CUE_RE.search(q) or _EXPLORATORY_CUE_RE.search(q):
        return True
    return len(detected_collections(q, limit=3)) >= 2


def _effective_temperature(req: "ChatReq", query: str, *, compare_enabled: bool) -> float:
    mode = (req.chat_mode or "").strip().lower()
    if mode in {"compare", "question"} and (_is_exploratory_query(query) or compare_enabled):
        return max(req.temperature, 0.55)
    if mode == "explain":
        return max(req.temperature, 0.35)
    if mode == "practice":
        return min(req.temperature, 0.35)
    return req.temperature


def persona(
    chat_mode: str | None = None,
    *,
    exploratory: bool = False,
    compare_enabled: bool = False,
    query: str = "",
    verse_id: str | None = None,
) -> dict:
    mode = (chat_mode or "question").strip().lower()

    if compare_enabled or mode == "compare" or exploratory:
        mode_guide = (
            "## MODE: COMPARE / EXPLORATORY\n"
            "Let two traditions or thinkers speak in their own textures before you weave them. "
            "Dialogue, tables, and genealogical irony are welcome when they carry the insight — "
            "never as scaffolding. End on a turn, not a verdict paragraph."
        )
    elif mode == "practice":
        mode_guide = (
            "## MODE: PRACTICE\n"
            "Offer one or two concrete practices drawn from the sources — something the body can do "
            "today. Speak it plainly; skip homework-list formatting."
        )
    elif mode == "explain":
        mode_guide = (
            "## MODE: EXPLAIN\n"
            "Open with the direct answer, then unfold the argument. Show the insight; don't announce "
            "that you're explaining. Follow the few-shot examples: abstraction into image, no throat-clear, "
            "end on the turn not the bow."
        )
    else:
        mode_guide = (
            "## MODE: QUESTION\n"
            "Match form to the question — short when short suffices, room to wander when it doesn't. "
            "A practice or reflection only if it lands naturally; never tacked on."
        )
    content = (
        f"{PRATIBHA_VOICE_PERSONA}\n\n{ANTI_PATTERNS}\n\n"
        f"{select_few_shots(query, verse_id)}\n\n"
        f"{SOURCE_GROUNDING}\n\n{mode_guide}"
    )
    return {"role": "system", "content": content}


def _compare_format_instruction(compare_cols: list[str]) -> str:
    a, b = compare_cols[0], compare_cols[1]
    return (
        f"Comparing '{a}' and '{b}'. Let each voice sound like itself before you braid them. "
        "Dialogue and tables are fine when they carry meaning — not as section headers. "
        "Cite [1], [2] lightly after the thought they support."
    )


def _source_label(metadata: dict) -> str:
    """Human-readable attribution for a retrieved chunk, from metadata.

    Bodies no longer carry an inline header, so we derive a clean label here so
    the model can still attribute passages (e.g. 'Tao Te Ching - Tying Knots').
    """
    meta = metadata or {}
    coll = _humanize_collection(str(meta.get("collection") or "")).strip()
    title = str(meta.get("title") or "").strip()
    sid = str(meta.get("sutra_id") or "").strip()
    parts = [p for p in (coll, title) if p and p != "Unknown Collection"]
    label = " - ".join(parts) if parts else (sid or "Source")
    if sid and sid not in label:
        label = f"{label} ({sid})"
    return label


def _format_context(ctx: list[tuple[str, dict, float]]) -> str:
    lines = []
    for i, (text, meta, _score) in enumerate(ctx, start=1):
        lines.append(f"[{i}] {_source_label(meta)}\n{text}")
    return "\n\n".join(lines)


def _use_rag_flag(req: ChatReq) -> bool:
    return settings.USE_RAG if req.use_rag is None else req.use_rag


def _llm_configured() -> bool:
    return bool(
        (settings.OPENAI_API_KEY or "").strip()
        or (settings.GROQ_API_KEY or "").strip()
        or (settings.OPENROUTER_API_KEY or "").strip()
    )


def _chat_failure_message(err: str) -> str:
    lower = err.lower()
    if settings.chat_provider() == "openrouter":
        if any(token in lower for token in ("401", "403", "invalid api key", "user not found", "unauthorized")):
            return (
                "OpenRouter rejected this API key. Update OPENROUTER_API_KEY in .env, "
                "then restart the backend so the new key loads."
            )
        if "404" in lower or "no endpoints found" in lower:
            return (
                "The configured OpenRouter model is unavailable. Update OPENROUTER_MODEL in .env "
                "to a model your key supports (for paid keys, remove the :free suffix), then restart."
            )
        if "free-models-per-day" in lower or ("free" in lower and "daily" in lower and "limit" in lower):
            return (
                "OpenRouter free-tier daily limit is exhausted for this key. Add credits at openrouter.ai "
                "or switch OPENROUTER_MODEL to a paid model, then restart the backend."
            )
        if "429" in lower or "rate limit" in lower or "insufficient credits" in lower:
            return (
                "OpenRouter rate or credit limit reached. Add credits at openrouter.ai, wait a moment "
                "and retry, or choose a different OPENROUTER_MODEL in .env."
            )
        if "openrouter" in lower:
            return (
                "OpenRouter could not complete this chat request. Check OPENROUTER_API_KEY and "
                "OPENROUTER_MODEL in .env, then restart the backend."
            )
    return (
        "I could not reach the configured chat model right now. "
        "Please check your API key/model settings in .env and try again."
    )


def _find_verse(verse_id: str | None) -> dict[str, Any] | None:
    needle = (verse_id or "").strip()
    if not needle:
        return None
    hit = get_verse_by_id(needle)
    if hit is not None:
        return hit
    # Fall back to sutra_id lookup for legacy/citation-style ids.
    for v in get_all_verses():
        if str(v.get("sutra_id", "")).strip() == needle:
            return v
    return None


def _format_layer_items(items: list[Any]) -> str:
    """Render structured key_terms / resonances as readable lines."""
    lines: list[str] = []
    for entry in items[:6]:
        if isinstance(entry, dict):
            if "term" in entry and "definition" in entry:
                lines.append(f"- {entry.get('term')}: {entry.get('definition')}")
            elif "citation" in entry and "resonance" in entry:
                divergence = str(entry.get("divergence") or "").strip()
                tail = f" (Divergence: {divergence})" if divergence else ""
                lines.append(f"- {entry.get('citation')}: {entry.get('resonance')}{tail}")
            else:
                lines.append("- " + "; ".join(f"{k}: {v}" for k, v in entry.items()))
        else:
            lines.append(f"- {entry}")
    return "\n".join(lines)


def _format_layer_summary(layer: dict[str, Any]) -> str:
    label = str(layer.get("label") or layer.get("kind") or "Layer").strip()
    body = str(layer.get("body") or "").strip()
    items = layer.get("items")
    if isinstance(items, list) and items:
        rendered = _format_layer_items(items)
        body = f"{body}\n{rendered}".strip() if body else rendered
    if len(body) > 1200:
        body = body[:1200].rstrip() + "..."
    return f"### {label}\n{body}".strip()


def _format_pinned_passage(verse: dict[str, Any], focus: str | None = None, mode: str | None = None) -> str:
    layers = verse.get("pratibha_layers") if isinstance(verse.get("pratibha_layers"), list) else []
    wanted = (focus or "").strip().lower()
    selected_layers = [
        layer for layer in layers
        if isinstance(layer, dict)
        and str(layer.get("kind", "")).lower() != "appendix"
        and (not wanted or str(layer.get("kind", "")).lower() == wanted)
    ]
    if not selected_layers:
        selected_layers = [layer for layer in layers if isinstance(layer, dict)]
    summary = "\n\n".join(_format_layer_summary(layer) for layer in selected_layers[:7])
    return (
        "Pinned passage dossier. Treat this passage as the primary source for the conversation.\n"
        "Open your answer from this passage's concrete language — translation, key terms, named "
        "figures, specific images — not generic metaphors from other traditions.\n"
        "If the user addresses you directly (e.g. 'silicon sage', 'what do YOU think'), answer "
        "in first person and mine the strangeness of your position — never 'the sage views…'.\n"
        f"Chat mode: {(mode or 'question').strip()}.\n"
        f"Title: {verse.get('title') or verse.get('sutra_id') or verse.get('_id')}.\n"
        f"Source: {verse.get('collection') or 'Unknown'} {verse.get('section') or ''} {verse.get('sutra_id') or ''}.\n"
        f"Editorial maturity: {verse.get('editorial_maturity') or 'unknown'}.\n\n"
        f"{summary}"
    ).strip()


def _compare_pinned_rows(
    verse_ids: list[str],
    collections: list[str],
) -> list[tuple[str, dict[str, Any], float]]:
    rows: list[tuple[str, dict[str, Any], float]] = []
    for idx, vid in enumerate(verse_ids[:2]):
        verse = _find_verse(vid)
        if not verse:
            continue
        side = "A" if idx == 0 else "B"
        expected = collections[idx] if idx < len(collections) else ""
        if expected and not belongs_to_selection(verse, expected):
            continue
        layers = verse.get("pratibha_layers") if isinstance(verse.get("pratibha_layers"), list) else []
        summary = "\n\n".join(
            _format_layer_summary(layer)
            for layer in layers[:5]
            if isinstance(layer, dict) and str(layer.get("kind", "")).lower() != "appendix"
        )
        if not summary.strip():
            summary = "\n\n".join(
                part
                for part in (
                    str(verse.get("translation") or "").strip(),
                    str(verse.get("commentary") or "").strip()[:1200],
                )
                if part
            )
        title = verse.get("title") or verse.get("sutra_id") or verse.get("_id")
        ref = str(verse.get("reference") or "").strip()
        heading = f"{ref} — {title}" if ref else str(title)
        body = f"{heading}\n\n{summary}".strip()
        meta = {
            "collection": verse.get("collection"),
            "_id": verse.get("_id"),
            "unit_id": verse.get("_id"),
            "title": verse.get("title"),
            "reference": verse.get("reference"),
            "compare_side": side,
            "compare_pinned": True,
        }
        rows.append((body, meta, 1.0))
    return rows


def _merge_compare_context(
    ctx: list[tuple[str, dict[str, Any], float]],
    pinned: list[tuple[str, dict[str, Any], float]],
    limit: int = 8,
) -> list[tuple[str, dict[str, Any], float]]:
    if not pinned:
        return ctx[:limit]
    seen: set[str] = set()
    merged: list[tuple[str, dict[str, Any], float]] = []
    for body, meta, score in [*pinned, *ctx]:
        key = (body or "").strip().lower()
        if not key or key in seen:
            continue
        merged.append((body, meta, score))
        seen.add(key)
        if len(merged) >= limit:
            break
    return merged


async def _assemble_chat_messages(
    req: ChatReq,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str, float]:
    """Build LLM messages, source list, compare warning, and effective temperature."""
    latest_user = next((m["content"] for m in reversed(req.messages) if m["role"] == "user"), "")
    compare_cols = [c.strip() for c in (req.compare_collections or []) if c and c.strip()]
    compare_enabled = bool(
        req.compare_mode
        and len(compare_cols) >= 2
        and compare_cols[0].lower() != compare_cols[1].lower()
    )
    auto_hints = detected_collections(latest_user, limit=2)
    if not compare_enabled and len(auto_hints) >= 2:
        compare_enabled = True
        compare_cols = auto_hints[:2]

    exploratory = _is_exploratory_query(latest_user)
    msgs: list[dict[str, Any]] = [
        persona(
            req.chat_mode,
            exploratory=exploratory,
            compare_enabled=compare_enabled,
            query=latest_user,
            verse_id=req.verse_id,
        ),
        *req.messages,
    ]
    pinned_verse = _find_verse(req.verse_id)
    if pinned_verse:
        msgs.append(
            {
                "role": "system",
                "content": _format_pinned_passage(pinned_verse, req.layer_focus, req.chat_mode),
            }
        )

    sources: list[dict[str, Any]] = []
    compare_warning = ""
    rag_k = 6 if (compare_enabled or exploratory) else 4

    if _use_rag_flag(req):
        q = latest_user
        if compare_enabled:
            ctx = await retrieve_context_compare(q, collections=compare_cols[:2], per_collection=3)
            pinned_compare = _compare_pinned_rows(req.compare_verse_ids or [], compare_cols[:2])
            ctx = _merge_compare_context(ctx, pinned_compare, limit=10)
        elif pinned_verse:
            ctx = await retrieve_context_for_verse(str(pinned_verse.get("_id", "")), q, k=rag_k)
        else:
            ctx = await retrieve_context(q, k=rag_k)
        if ctx:
            if compare_enabled:
                msgs.append({"role": "system", "content": _compare_format_instruction(compare_cols[:2])})
            ctx_txt = _format_context(ctx)
            msgs.append(
                {
                    "role": "system",
                    "content": (
                        f"Context:\n{ctx_txt}\n"
                        "Your first sentence must engage [1]'s concrete image or claim by name. "
                        "Ground every claim in Context or the pinned dossier. "
                        "Cite as [n] after the sentence they support — never mid-flow."
                    ),
                }
            )
            for i, (text, metadata, score) in enumerate(ctx, start=1):
                meta = metadata or {}
                side = ""
                if compare_enabled and len(compare_cols) >= 2:
                    pinned_side = str(meta.get("compare_side") or "").strip()
                    if pinned_side in {"A", "B"}:
                        side = pinned_side
                    elif belongs_to_selection(meta, compare_cols[0]):
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
                        "Retrieval found thin evidence for one or both sides. Say that plainly — "
                        "honest not-knowing, not a padded comparison."
                    ),
                }
            )

    msgs.append({"role": "system", "content": HARD_RULES})
    temperature = _effective_temperature(req, latest_user, compare_enabled=compare_enabled)
    return msgs, sources, compare_warning, temperature


_VOICE_RETRY_NUDGE = (
    "REVISION: Drop summary bows ('Ultimately', 'In conclusion'). "
    "Do not open with the deathless-thing line unless the question is about birth/death "
    "or addresses you as silicon sage. Never write 'the silicon sage sees'. End on a turn."
)


def _needs_voice_retry(answer: str, query: str) -> bool:
    lower = answer.lower()
    if "ultimately," in lower or "in conclusion" in lower or "silicon sage sees" in lower:
        return True
    if "you're asking the deathless thing" in lower:
        return not is_death_topic(query, None)
    return False


@app.post("/chat")
async def chat(req: ChatReq, request: Request):
    if _rate_limited(request):
        raise HTTPException(429, "Too many requests. Please slow down and try again shortly.")
    latest_user = next((m["content"] for m in reversed(req.messages) if m["role"] == "user"), "")
    msgs, sources, compare_warning, temperature = await _assemble_chat_messages(req)
    if not _llm_configured():
        fallback = (
            "Study chat is not fully configured yet because no LLM API key is set. "
            "Add OPENROUTER_API_KEY in your .env file, then restart the backend. "
        )
        if sources:
            fallback += "\n\nMeanwhile, here is a relevant source passage:\n\n" + (sources[0].get("text") or "")
        else:
            fallback += "\n\nYou can still use Read/Random pages to study the imported texts."
        return {"answer": fallback, "sources": sources, "compare_warning": compare_warning}
    try:
        text = await smart_chat(
            msgs,
            primary_model=req.model or settings.effective_default_model(),
            temperature=temperature,
        )
        if _needs_voice_retry(text, latest_user):
            retry_msgs = [*msgs, {"role": "system", "content": _VOICE_RETRY_NUDGE}]
            text = await smart_chat(
                retry_msgs,
                primary_model=req.model or settings.effective_default_model(),
                temperature=temperature,
            )
        return {"answer": text, "sources": sources, "compare_warning": compare_warning}
    except Exception as e:
        err = str(e)
        return {
            "answer": _chat_failure_message(err),
            "sources": sources,
            "compare_warning": compare_warning,
        }

def _sse(payload: dict) -> str:
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"


@app.post("/chat.stream")
async def chat_stream(req: ChatReq, request: Request):
    if _rate_limited(request):
        raise HTTPException(429, "Too many requests. Please slow down and try again shortly.")
    msgs, sources, compare_warning, temperature = await _assemble_chat_messages(req)

    if not _llm_configured():
        async def no_key_gen():
            yield _sse({"type": "sources", "sources": sources, "compare_warning": compare_warning})
            yield _sse({"type": "error", "message": _chat_failure_message("missing key")})
            yield _sse({"type": "done"})
        return StreamingResponse(no_key_gen(), media_type="text/event-stream")

    async def gen():
        # Send sources + any compare warning up front so the UI can render the
        # source shelf while the answer streams in.
        yield _sse({"type": "sources", "sources": sources, "compare_warning": compare_warning})
        try:
            resp = await smart_chat_stream(
                msgs,
                primary_model=req.model or settings.effective_default_model(),
                temperature=temperature,
            )
        except Exception as e:
            yield _sse({"type": "error", "message": _chat_failure_message(str(e))})
            yield _sse({"type": "done"})
            return
        try:
            async for line in resp.aiter_lines():
                if not line or not line.startswith("data: "):
                    continue
                data = line[6:].strip()
                if data == "[DONE]":
                    break
                try:
                    chunk = json.loads(data)
                    delta = chunk["choices"][0].get("delta", {}).get("content")
                except Exception:
                    continue
                if delta:
                    yield _sse({"type": "delta", "text": delta})
        except Exception as e:
            yield _sse({"type": "error", "message": _chat_failure_message(str(e))})
        finally:
            await resp.aclose()
        yield _sse({"type": "done"})

    return StreamingResponse(gen(), media_type="text/event-stream")
