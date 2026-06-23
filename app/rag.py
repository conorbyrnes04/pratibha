import asyncio
import logging
import re
import json
from typing import List, Tuple

import asyncpg
from openai import AsyncOpenAI

from .config import settings
from .collection_aliases import aliases_for_selection, meta_collection_slug

logger = logging.getLogger("pratibha.rag")

# Tie-break only — does not override vector/lexical relevance scores.
IMAGERY_BIAS_WEIGHT = 0.08

_ABSTRACT_NOMINALS = re.compile(
    r"\b("
    r"manifestation|framework|principle|interconnectedness|emergence|paradigm|"
    r"dimension|ontology|epistemology|self-ordering|collaboration|vibration|"
    r"implications|perspective|alignment|cultivat\w+|fundamental"
    r")\b",
    re.I,
)
_CONCRETE_NOUNS = re.compile(
    r"\b("
    r"water|wheel|cup|stone|wood|breath|hand|river|valley|block|bowl|fire|earth|"
    r"sky|body|eye|mouth|feet|seed|tree|bird|fish|mountain|shadow|light|sound|"
    r"silence|spoke|clay|room|hub|tea|kettle|fan|dust|hearth|log|mountain|bowl|"
    r"syllable|akṣara|akshara|oṃ|om"
    r")\b",
    re.I,
)

_ROOT_LAYER_KINDS = frozenset({"translation", "original", "iast"})
_COMMENTARY_LIKE = frozenset({"commentary", "key_terms", "resonances", "insight", "appendix"})

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
    "yoginihrdaya": [
        "yoginihrdaya",
        "yogini hrdaya",
        "heart of the yogini",
        "sricakra",
        "sri cakra",
        "tripura",
        "tripurasundari",
        "sri vidya",
        "srividya",
        "khecara",
        "kamakala",
    ],
    "tantrasara": [
        "tantrasara",
        "tantrasāra",
        "abhinavagupta",
        "anupaya",
        "sambhava",
        "saktopaya",
        "anavopaya",
        "prakasha",
        "svatantrya",
        "trika",
    ],
    "patanjali_yoga_sutras": [
        "patanjali",
        "yoga sutras",
        "yoga sūtras",
        "raja yoga",
        "ashtanga",
        "citta vrtti",
        "samadhi pada",
        "yamas",
        "niyamas",
    ],
    "milarepa_songs": [
        "milarepa",
        "mila repa",
        "jetsun kahbum",
        "jetsün kahbum",
        "great yogi milarepa",
        "tibet's great yogi",
    ],
    "dogen_shobogenzo": [
        "dogen",
        "dōgen",
        "shobogenzo",
        "shōbōgenzō",
        "genjokoan",
        "genjōkōan",
        "bendowa",
        "bendōwa",
        "fukanzazengi",
        "uji",
        "bussho",
        "soto zen",
    ],
    "plotinus_enneads": [
        "plotinus",
        "enneads",
        "ennead",
        "neoplaton",
    ],
    "heraclitus_fragments": [
        "heraclitus",
        "heracleitus",
        "fragments of heraclitus",
        "logos",
        "panta rhei",
        "ever-living fire",
        "pre-socratic",
    ],
    "chandogya_upanishad": [
        "chandogya",
        "chāndogya",
        "khandogya",
        "khândogya",
        "tat tvam asi",
        "tat tvam",
        "uddalaka",
        "svetaketu",
        "sandilya",
        "sāṇḍilya",
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
    hits = detected_collections(query, limit=1)
    return hits[0] if hits else None


def detected_collections(query: str, limit: int = 4) -> list[str]:
    """Return canonical collection slugs mentioned in the query (order preserved)."""
    q = (query or "").lower()
    hits: list[str] = []
    for slug, aliases in _COLLECTION_HINTS.items():
        if any(alias in q for alias in aliases):
            hits.append(slug)
            if len(hits) >= limit:
                break
    return hits


def _slugish(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", (value or "").lower()).strip("_")


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
    # Hints are slugs (e.g. "tao_te_ching"); compare against both the raw
    # haystack and a slugified version so "Tao Te Ching" still matches.
    return hint in hay or hint in _slugish(hay)


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


def _verse_chunk_body(verse: dict) -> str:
    parts: list[str] = []
    title = str(verse.get("title") or "").strip()
    ref = str(verse.get("reference") or "").strip()
    if ref and title:
        parts.append(f"{ref} — {title}")
    elif title:
        parts.append(title)
    for key in ("translation", "commentary", "abhyasa"):
        text = str(verse.get(key) or "").strip()
        if not text:
            continue
        parts.append(text[:1200] if key == "commentary" else text)
    return "\n\n".join(parts).strip()


def _verse_chunk_meta(verse: dict) -> dict:
    return {
        "collection": verse.get("collection"),
        "_id": verse.get("_id"),
        "unit_id": verse.get("_id"),
        "title": verse.get("title"),
        "sutra_id": verse.get("sutra_id"),
        "reference": verse.get("reference"),
        "themes": verse.get("themes"),
        "corpus_fallback": True,
    }


def _corpus_lexical_candidates(
    query: str,
    aliases: set[str],
    limit: int,
) -> list[tuple[str, dict, float]]:
    """Lexical search over in-memory corpus when pgvector lacks a collection."""
    from .data_loader import ALL_VERSES

    tokens = set(_tokenize(query))
    scored: list[tuple[str, dict, float]] = []
    for verse in ALL_VERSES:
        if meta_collection_slug(verse) not in aliases:
            continue
        body = _verse_chunk_body(verse)
        if not body:
            continue
        blob_tokens = _token_set(body)
        score = _jaccard(tokens, blob_tokens) if tokens else 0.5
        if tokens and score < 0.04:
            continue
        scored.append((body, _verse_chunk_meta(verse), max(score, settings.COMPARE_MIN_SCORE)))
    scored.sort(key=lambda row: (row[2], str((row[1] or {}).get("reference") or "")))
    return scored[: max(2, limit)]


def _corpus_collection_candidates(
    aliases: set[str],
    limit: int,
) -> list[tuple[str, dict, float]]:
    """Return representative corpus units when pgvector has no indexed chunks."""
    from .data_loader import ALL_VERSES

    rows: list[tuple[str, dict, float]] = []
    for verse in ALL_VERSES:
        if meta_collection_slug(verse) not in aliases:
            continue
        body = _verse_chunk_body(verse)
        if not body:
            continue
        rows.append((body, _verse_chunk_meta(verse), float(settings.COMPARE_MIN_SCORE)))
    rows.sort(
        key=lambda row: (
            int((row[1] or {}).get("sequence") or 0),
            str((row[1] or {}).get("reference") or ""),
            str((row[1] or {}).get("_id") or ""),
        )
    )
    return rows[: max(2, limit)]


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


def _imagery_score(body: str) -> float:
    """Higher when text carries concrete/sensory nouns vs abstract nominal piles."""
    if not body:
        return 0.0
    abstract = len(_ABSTRACT_NOMINALS.findall(body))
    concrete = len(_CONCRETE_NOUNS.findall(body))
    return float(concrete - abstract)


def _rank_by_relevance_and_imagery(
    candidates: list[tuple[str, dict, float]],
) -> list[tuple[str, dict, float]]:
    """Primary sort: retrieval score. Tie-break: image-bearing chunks."""
    return sorted(
        candidates,
        key=lambda row: (row[2], IMAGERY_BIAS_WEIGHT * _imagery_score(row[0])),
        reverse=True,
    )


def _unit_id_from_meta(metadata: dict) -> str:
    meta = metadata or {}
    for key in ("_id", "unit_id", "sutra_id"):
        val = str(meta.get(key) or "").strip()
        if val:
            return val
    return ""


def _verse_root_chunks(verse: dict) -> list[tuple[str, dict, float]]:
    """Root verse / translation rows for a unit — concrete language the model can use."""
    rows: list[tuple[str, dict, float]] = []
    base_meta = {
        "collection": verse.get("collection"),
        "_id": verse.get("_id"),
        "unit_id": verse.get("_id"),
        "title": verse.get("title"),
        "sutra_id": verse.get("sutra_id"),
        "reference": verse.get("reference"),
        "root_companion": True,
    }
    layers = verse.get("pratibha_layers") or []
    if isinstance(layers, list):
        for layer in layers:
            if not isinstance(layer, dict):
                continue
            kind = str(layer.get("kind") or "").strip().lower()
            if kind not in _ROOT_LAYER_KINDS:
                continue
            body = str(layer.get("body") or "").strip()
            if body:
                meta = {**base_meta, "layer_kind": kind, "section": layer.get("label") or kind}
                rows.append((body, meta, 0.95))
    if rows:
        return rows
    for key, kind in (
        ("translation", "translation"),
        ("translation_literal", "translation"),
        ("sanskrit_devanagari", "original"),
        ("sanskrit_iast", "iast"),
    ):
        text = str(verse.get(key) or "").strip()
        if text:
            meta = {**base_meta, "layer_kind": kind, "section": key}
            rows.append((text, meta, 0.95))
    return rows


def _ensure_root_companions(
    selected: list[tuple[str, dict, float]],
    k: int,
) -> list[tuple[str, dict, float]]:
    """When commentary chunks are selected, prepend root translation/original from the same unit."""
    from .data_loader import get_verse_by_id

    if not selected:
        return selected

    out = list(selected)
    seen_body = {(body or "").strip().lower() for body, _, _ in out}
    present_by_unit: dict[str, set[str]] = {}
    units_needing_root: set[str] = set()

    for _, meta, _ in out:
        uid = _unit_id_from_meta(meta)
        if not uid:
            continue
        kind = str(meta.get("layer_kind") or "").strip().lower()
        present_by_unit.setdefault(uid, set()).add(kind)
        if kind not in _ROOT_LAYER_KINDS:
            units_needing_root.add(uid)

    prepend: list[tuple[str, dict, float]] = []
    for uid in sorted(units_needing_root):
        kinds = present_by_unit.get(uid, set())
        if kinds & _ROOT_LAYER_KINDS:
            continue
        verse = get_verse_by_id(uid)
        if not verse:
            continue
        for body, meta, score in _verse_root_chunks(verse):
            key = body.strip().lower()
            if not key or key in seen_body:
                continue
            prepend.append((body, meta, score))
            seen_body.add(key)
            break

    if not prepend:
        return out[:k]
    merged = [*prepend, *out]
    return merged[: max(k, len(prepend) + min(len(out), k))]


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
    candidates = _rank_by_relevance_and_imagery(_dedupe_argument_redundancy(candidates))
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


async def _embed_query(client: AsyncOpenAI, model: str, query: str, attempts: int = 3) -> list[float]:
    """Embed the query with bounded exponential backoff.

    A single transient failure (e.g. OpenRouter free-tier rate limiting) must
    not silently demote retrieval to lexical fallback, so we retry briefly
    before letting the exception propagate.
    """
    last_exc: Exception | None = None
    for attempt in range(attempts):
        try:
            resp = await client.embeddings.create(model=model, input=query)
            return resp.data[0].embedding
        except Exception as exc:  # noqa: BLE001 - retry transient embedding failures
            last_exc = exc
            if attempt + 1 < attempts:
                await asyncio.sleep(0.5 * (2 ** attempt))
    raise last_exc if last_exc else RuntimeError("embedding failed")


async def _vector_candidates(conn: asyncpg.Connection, query: str, fetch_k: int) -> list[tuple[str, dict, float]]:
    client, model = _embedding_client_and_model()
    if client is None:
        return []
    emb = await _embed_query(client, model, query)
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
        conn = await asyncpg.connect(**settings.asyncpg_kwargs())
        vector = []
        if settings.OPENAI_API_KEY or settings.OPENROUTER_API_KEY:
            try:
                vector = await _vector_candidates(conn, query, fetch_k=fetch_k)
            except Exception:
                # Fall through to lexical search if embeddings are unavailable at runtime.
                logger.warning("Vector retrieval failed; falling back to lexical search", exc_info=True)
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
                return _ensure_root_companions(uniq, k)
        return _ensure_root_companions(_diversify(merged, k), k)
    except Exception:
        logger.error("retrieve_context failed (returning empty context)", exc_info=True)
        return []
    finally:
        if conn is not None:
            await conn.close()


async def retrieve_context_for_verse(verse_id: str, query: str, k: int = 4) -> List[Tuple[str, dict, float]]:
    """
    Prefer chunks already indexed for the pinned verse, then top up with normal retrieval.
    """
    needle = (verse_id or "").strip()
    if not needle:
        return await retrieve_context(query, k=k)

    conn: asyncpg.Connection | None = None
    pinned: list[tuple[str, dict, float]] = []
    try:
        conn = await asyncpg.connect(**settings.asyncpg_kwargs())
        rows = await conn.fetch(
            """
            SELECT body, metadata
            FROM chunks
            WHERE metadata->>'_id' = $1 OR metadata->>'unit_id' = $1 OR metadata->>'sutra_id' = $1
            ORDER BY
              CASE metadata->>'layer_kind'
                WHEN 'translation' THEN 1
                WHEN 'commentary' THEN 2
                WHEN 'key_terms' THEN 3
                WHEN 'resonances' THEN 4
                WHEN 'practice' THEN 5
                ELSE 6
              END,
              COALESCE((metadata->>'chunk_index')::int, 999)
            LIMIT $2
            """,
            needle,
            max(k, 8),
        )
        pinned = [(r["body"], _normalize_meta(r["metadata"]), 1.0) for r in rows]
    except Exception:
        logger.warning("Pinned-verse retrieval failed for %r; using general retrieval", needle, exc_info=True)
        pinned = []
    finally:
        if conn is not None:
            await conn.close()

    if len(pinned) >= k:
        return _ensure_root_companions(pinned[:k], k)

    supplemental = await retrieve_context(query, k=max(k, 4))
    seen = {(body or "").strip().lower() for body, _, _ in pinned}
    for body, meta, score in supplemental:
        key = (body or "").strip().lower()
        if not key or key in seen:
            continue
        pinned.append((body, meta, score))
        seen.add(key)
        if len(pinned) >= k:
            break
    return _ensure_root_companions(pinned[:k], k)


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
        conn = await asyncpg.connect(**settings.asyncpg_kwargs())
        vector: list[tuple[str, dict, float]] = []
        if settings.OPENAI_API_KEY or settings.OPENROUTER_API_KEY:
            try:
                vector = await _vector_candidates(conn, query, fetch_k=fetch_k)
            except Exception:
                logger.warning("Vector retrieval failed in compare mode; using lexical only", exc_info=True)
                vector = []
        lexical = await _keyword_candidates(conn, query, fetch_k=fetch_k)
        merged = sorted([*vector, *lexical], key=lambda x: x[2], reverse=True)
        merged = _filter_by_collections(merged, collections)
        if not merged:
            fallback_rows: list[tuple[str, dict, float]] = []
            for collection_name in selected:
                aliases = aliases_for_selection(collection_name)
                lexical_rows = _corpus_lexical_candidates(query, aliases, per_collection * 2)
                if not lexical_rows:
                    lexical_rows = _corpus_collection_candidates(aliases, per_collection * 2)
                fallback_rows.extend(lexical_rows)
            return fallback_rows[:total_k]

        selected_rows: list[tuple[str, dict, float]] = []
        seen: set[str] = set()
        for collection_name in selected:
            aliases = aliases_for_selection(collection_name)
            pool = [c for c in merged if meta_collection_slug(c[1]) in aliases and float(c[2]) >= settings.COMPARE_MIN_SCORE]
            # If strict compare retrieval misses a side, fall back to collection-scoped fetch.
            if not pool:
                pool = await _collection_fallback_candidates(conn, aliases, per_collection)
                pool = [c for c in pool if float(c[2]) >= settings.COMPARE_MIN_SCORE]
            if not pool:
                pool = _corpus_lexical_candidates(query, aliases, per_collection * 3)
            if not pool:
                pool = _corpus_collection_candidates(aliases, per_collection * 2)
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
        logger.error("retrieve_context_compare failed (returning empty context)", exc_info=True)
        return []
    finally:
        if conn is not None:
            await conn.close()
