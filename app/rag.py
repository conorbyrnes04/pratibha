import re
import json
from typing import List, Tuple

import asyncpg
from openai import AsyncOpenAI

from .config import settings
from .collection_aliases import aliases_for_selection, meta_collection_slug

_STOPWORDS = {
    "the", "and", "for", "that", "with", "this", "from", "into", "your", "what",
    "when", "where", "which", "about", "have", "will", "would", "could", "should",
    "then", "than", "they", "them", "their", "there", "here", "also", "just",
}

_COLLECTION_HINTS = {
    "tao_te_ching": ["tao te ching", "dao de jing", "lao tzu", "laozi"],
    "the_book_of_chuang_tzu": ["chuang tzu", "zhuangzi", "zhuang zi"],
    "siva_sutra": ["siva sutra", "shiva sutra"],
    "pratyabhijnahrdayam": ["pratyabhijna hrdayam", "pratyabhijnahrdayam", "heart of recognition"],
    "astavakra_gita": ["astavakra gita", "ashtavakra gita", "song of astavakra"],
    "mandukya_upanishad_karika": [
        "mandukya",
        "mandukya upanishad",
        "gaudapada",
        "gaudapada karika",
        "ajativada",
        "turya",
    ],
    "svetasvatara_upanishad": [
        "svetasvatara",
        "svetasvatara upanishad",
        "svetasvatara upanisad",
        "rudra",
        "mahesvara",
    ],
    "isavasya_upanishad": [
        "isavasya",
        "isha upanishad",
        "isa upanishad",
        "isavasyam",
        "vidya and avidya",
    ],
    "senegalese_animism": [
        "senegalese animism",
        "serer",
        "sérère",
        "roog",
        "pangool",
        "takhar",
        "tiurakh",
        "cosaan",
        "lasnet",
        "delafosse",
    ],
    "pulaar_tradition": [
        "pulaar",
        "fulbe",
        "fulɓe",
        "peul",
        "foulah",
        "fulani",
        "boolatrie",
        "yettode",
        "pulaaku",
        "crozals",
        "reclus",
    ],
}


def _embedding_client_and_model() -> tuple[AsyncOpenAI | None, str]:
    model = settings.EMBEDDING_MODEL
    if settings.OPENAI_API_KEY:
        return AsyncOpenAI(api_key=settings.OPENAI_API_KEY), model
    if settings.OPENROUTER_API_KEY:
        headers = {}
        if settings.OPENROUTER_SITE_URL:
            headers["HTTP-Referer"] = settings.OPENROUTER_SITE_URL
        if settings.OPENROUTER_APP_NAME:
            headers["X-Title"] = settings.OPENROUTER_APP_NAME
        if "/" not in model:
            model = f"openai/{model}"
        return (
            AsyncOpenAI(
                api_key=settings.OPENROUTER_API_KEY,
                base_url="https://openrouter.ai/api/v1",
                default_headers=headers or None,
            ),
            model,
        )
    return None, model


def _tokenize(query: str) -> list[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z'-]{2,}", query.lower())
    return [w for w in words if w not in _STOPWORDS][:10]


def _collection_hint(query: str) -> str | None:
    q = (query or "").lower()
    for slug, aliases in _COLLECTION_HINTS.items():
        if any(alias in q for alias in aliases):
            return slug
    return None


def _matches_hint(metadata: dict, hint: str) -> bool:
    meta = _normalize_meta(metadata)
    hay = " ".join(
        [
            str(meta.get("collection", "")),
            str(meta.get("source_file", "")),
            str(meta.get("title", "")),
            str(meta.get("sutra_id", "")),
        ]
    ).lower()
    return hint in hay


def _filter_by_collections(
    candidates: list[tuple[str, dict, float]],
    include_collections: list[str] | None,
) -> list[tuple[str, dict, float]]:
    if not include_collections:
        return candidates
    wanted: set[str] = set()
    for c in include_collections:
        if c and c.strip():
            wanted.update(aliases_for_selection(c))
    if not wanted:
        return candidates
    return [c for c in candidates if meta_collection_slug(c[1]) in wanted]


async def _collection_fallback_candidates(
    conn: asyncpg.Connection,
    aliases: set[str],
    limit: int,
) -> list[tuple[str, dict, float]]:
    if not aliases:
        return []
    pats = [f"%{a}%" for a in sorted(aliases)]
    rows = await conn.fetch(
        """
        SELECT body, metadata
        FROM chunks
        WHERE lower(COALESCE(metadata::text, '')) LIKE ANY($1::text[])
        LIMIT $2
        """,
        pats,
        max(4, limit * 4),
    )
    out: list[tuple[str, dict, float]] = []
    for r in rows:
        out.append((r["body"], _normalize_meta(r["metadata"]), float(settings.COMPARE_MIN_SCORE)))
    return out[: max(2, limit)]


def _token_set(text: str) -> set[str]:
    return set(re.findall(r"[a-z]{3,}", (text or "").lower()))


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / max(1, len(a | b))


def _quality_of(metadata: dict) -> float:
    try:
        return float((metadata or {}).get("quality_score", 0.0) or 0.0)
    except Exception:
        return 0.0


def _dedupe_argument_redundancy(candidates: list[tuple[str, dict, float]]) -> list[tuple[str, dict, float]]:
    ranked = sorted(candidates, key=lambda x: (_quality_of(_normalize_meta(x[1])), x[2]), reverse=True)
    kept: list[tuple[str, dict, float]] = []
    kept_tokens: list[set[str]] = []
    kept_collections: list[str] = []
    for body, metadata, score in ranked:
        meta = _normalize_meta(metadata)
        coll = meta_collection_slug(meta)
        tokens = _token_set(body)
        duplicate = False
        for idx, prev_tokens in enumerate(kept_tokens):
            if kept_collections[idx] != coll:
                continue
            if _jaccard(tokens, prev_tokens) >= 0.88:
                duplicate = True
                break
        if duplicate:
            continue
        kept.append((body, meta, score))
        kept_tokens.append(tokens)
        kept_collections.append(coll)
    return kept


def _normalize_meta(value) -> dict:
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, dict) else {}
        except Exception:
            return {}
    return {}


def _diversify(candidates: list[tuple[str, dict, float]], k: int) -> list[tuple[str, dict, float]]:
    candidates = _dedupe_argument_redundancy(candidates)
    # First pass: prefer one chunk per logical source/section.
    selected: list[tuple[str, dict, float]] = []
    seen_source: set[tuple[str, str, str]] = set()
    seen_body: set[str] = set()
    for body, metadata, score in candidates:
        meta = _normalize_meta(metadata)
        source_key = (
            str(meta.get("collection", "")),
            str(meta.get("sutra_id", "")),
            str(meta.get("section", "")),
        )
        body_key = body.strip().lower()
        if not body_key or body_key in seen_body:
            continue
        if source_key in seen_source:
            continue
        selected.append((body, meta, score))
        seen_source.add(source_key)
        seen_body.add(body_key)
        if len(selected) >= k:
            return selected

    # Second pass: fill remaining slots with highest-scoring leftovers.
    for body, metadata, score in candidates:
        body_key = body.strip().lower()
        if not body_key or body_key in seen_body:
            continue
        selected.append((body, metadata or {}, score))
        seen_body.add(body_key)
        if len(selected) >= k:
            break
    return selected


async def _vector_candidates(conn: asyncpg.Connection, query: str, fetch_k: int) -> list[tuple[str, dict, float]]:
    client, model = _embedding_client_and_model()
    if client is None:
        return []
    emb = (await client.embeddings.create(model=model, input=query)).data[0].embedding
    vector_str = f"[{','.join(map(str, emb))}]"
    rows = await conn.fetch(
        """
        SELECT body, metadata, 1 - (embedding <=> $1::vector) AS score
        FROM chunks
        ORDER BY embedding <-> $1::vector
        LIMIT $2
        """,
        vector_str,
        fetch_k,
    )
    out: list[tuple[str, dict, float]] = []
    for r in rows:
        score = float(r["score"])
        if score >= settings.RAG_MIN_SCORE:
            out.append((r["body"], _normalize_meta(r["metadata"]), score))
    return out


async def _keyword_candidates(conn: asyncpg.Connection, query: str, fetch_k: int) -> list[tuple[str, dict, float]]:
    tokens = _tokenize(query)
    if not tokens:
        return []
    patterns = [f"%{t}%" for t in tokens]
    rows = await conn.fetch(
        """
        SELECT body, metadata
        FROM chunks
        WHERE lower(body) LIKE ANY($1::text[])
        LIMIT $2
        """,
        patterns,
        max(fetch_k * 2, 30),
    )
    scored: list[tuple[str, dict, float]] = []
    for r in rows:
        body = (r["body"] or "").lower()
        hits = sum(1 for t in tokens if t in body)
        if hits == 0:
            continue
        # Heuristic score range ~[0.2, 0.8] for lexical fallback.
        score = 0.2 + min(0.6, hits / max(1, len(tokens)))
        scored.append((r["body"], _normalize_meta(r["metadata"]), score))
    scored.sort(key=lambda x: x[2], reverse=True)
    return scored[:fetch_k]


async def retrieve_context(query: str, k: int = 4) -> List[Tuple[str, dict, float]]:
    fetch_k = max(k, settings.RAG_FETCH_K)
    conn: asyncpg.Connection | None = None
    try:
        conn = await asyncpg.connect(
            user=settings.PG_USER,
            password=settings.PG_PASSWORD,
            database=settings.PG_DB,
            host=settings.PG_HOST,
            port=settings.PG_PORT,
        )
        vector = []
        if settings.OPENAI_API_KEY or settings.OPENROUTER_API_KEY:
            try:
                vector = await _vector_candidates(conn, query, fetch_k=fetch_k)
            except Exception:
                # Fall through to lexical search if embeddings are unavailable at runtime.
                vector = []
        lexical = await _keyword_candidates(conn, query, fetch_k=fetch_k)
        merged = sorted([*vector, *lexical], key=lambda x: x[2], reverse=True)
        hinted = _collection_hint(query)
        if hinted:
            matching = [c for c in merged if _matches_hint(c[1], hinted)]
            if matching:
                chosen = _diversify(matching, k)
                if len(chosen) < k:
                    chosen.extend(_diversify(merged, k))
                # Deduplicate while preserving order.
                uniq: list[tuple[str, dict, float]] = []
                seen: set[str] = set()
                for body, meta, score in chosen:
                    key = (body or "").strip().lower()
                    if not key or key in seen:
                        continue
                    uniq.append((body, meta, score))
                    seen.add(key)
                    if len(uniq) >= k:
                        break
                return uniq
        return _diversify(merged, k)
    except Exception:
        return []
    finally:
        if conn is not None:
            await conn.close()


async def retrieve_context_compare(
    query: str,
    collections: list[str],
    per_collection: int = 2,
) -> list[tuple[str, dict, float]]:
    """
    Retrieve balanced context from each requested collection.
    """
    if not collections:
        return await retrieve_context(query, k=max(2, per_collection))

    selected = [c.strip() for c in collections if c and c.strip()]
    if len(selected) < 2:
        return await retrieve_context(query, k=max(2, per_collection))
    selected = selected[:2]

    total_k = max(4, per_collection * len(selected))
    fetch_k = max(settings.RAG_FETCH_K, total_k * 12)

    conn: asyncpg.Connection | None = None
    try:
        conn = await asyncpg.connect(
            user=settings.PG_USER,
            password=settings.PG_PASSWORD,
            database=settings.PG_DB,
            host=settings.PG_HOST,
            port=settings.PG_PORT,
        )
        vector: list[tuple[str, dict, float]] = []
        if settings.OPENAI_API_KEY or settings.OPENROUTER_API_KEY:
            try:
                vector = await _vector_candidates(conn, query, fetch_k=fetch_k)
            except Exception:
                vector = []
        lexical = await _keyword_candidates(conn, query, fetch_k=fetch_k)
        merged = sorted([*vector, *lexical], key=lambda x: x[2], reverse=True)
        merged = _filter_by_collections(merged, collections)
        if not merged:
            return []

        selected_rows: list[tuple[str, dict, float]] = []
        seen: set[str] = set()
        for collection_name in selected:
            aliases = aliases_for_selection(collection_name)
            pool = [c for c in merged if meta_collection_slug(c[1]) in aliases and float(c[2]) >= settings.COMPARE_MIN_SCORE]
            # If strict compare retrieval misses a side, fall back to collection-scoped fetch.
            if not pool:
                pool = await _collection_fallback_candidates(conn, aliases, per_collection)
                pool = [c for c in pool if float(c[2]) >= settings.COMPARE_MIN_SCORE]
            for body, meta, score in _diversify(pool, per_collection):
                key = (body or "").strip().lower()
                if not key or key in seen:
                    continue
                selected_rows.append((body, _normalize_meta(meta), score))
                seen.add(key)

        # If one side is sparse, top up from all requested collections.
        if len(selected_rows) < total_k:
            for body, meta, score in _diversify(
                [c for c in merged if float(c[2]) >= settings.COMPARE_MIN_SCORE], total_k
            ):
                key = (body or "").strip().lower()
                if not key or key in seen:
                    continue
                selected_rows.append((body, _normalize_meta(meta), score))
                seen.add(key)
                if len(selected_rows) >= total_k:
                    break
        return selected_rows[:total_k]
    except Exception:
        return []
    finally:
        if conn is not None:
            await conn.close()
