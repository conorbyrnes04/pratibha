import datetime
import glob
import hashlib
import logging
import os
import ast
import re
from typing import Any

import pytz
import yaml

logger = logging.getLogger("pratibha.data_loader")

ROOT = os.path.dirname(os.path.dirname(__file__))

MATURITY_ORDER = {
    "structural_draft": 0,
    "needs_rewrite": 1,
    "strong_draft": 2,
    "publishable": 3,
}

# Generic placeholder practices that signal an un-edited stub unit. These are
# pure boilerplate stamped onto hundreds of units; they carry no real guidance.
GENERIC_PRACTICE_MARKERS = (
    "read this passage slowly three times",
    "read this fragment three times slowly",
    "read once slowly, then pause",
    "read the excerpt slowly, pause at one striking line",
    "read the passage slowly, pause for one minute",
    "choose one ordinary action today and perform it",
    "for 2 minutes, observe inner speech",
    "sit for 3 minutes with natural breathing",
)

# Commentary openings produced by a bulk auto-enrichment pass and duplicated
# verbatim across many units. Treated as non-authored filler.
TEMPLATE_COMMENTARY_MARKERS = (
    "the emphasis turns inward",
    "this fragment invites direct contemplation",
    "read this line as a contemplative pointer",
    "the fragment points to a wisdom",
    "the line turns inquiry inward",
    "here change is not chaos but lawful transformation",
    "the teaching frames",
)

# Fully-authored collections whose units are publishable as written.
PUBLISHABLE_COLLECTIONS = (
    "zhuangzi", "chuang", "phaedo", "tao te ching", "epictetus", "svetasvatara", "isavasya",
)

# Diagnostics populated by load_all() so callers can inspect corpus health.
LOAD_STATS: dict[str, Any] = {
    "files_seen": 0,
    "loaded": 0,
    "parse_errors": 0,
    "duplicate_ids": [],
}


def _as_text(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, dict):
        for key in ("title", "translation", "transliteration", "devanagari", "text", "name"):
            val = v.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()
        return ""
    if isinstance(v, list):
        return "\n".join(_as_text(x) for x in v if _as_text(x)).strip()
    if isinstance(v, str):
        s = v.strip()
        # Some legacy fields were stringified dicts; recover the useful title text.
        if s.startswith("{") and s.endswith("}"):
            try:
                parsed = ast.literal_eval(s)
                if isinstance(parsed, dict):
                    recovered = _as_text(parsed)
                    if recovered:
                        return recovered
            except Exception:
                pass
        return s
    return str(v).strip()


def _humanize_collection(v: str) -> str:
    s = v.strip()
    if not s:
        return "Unknown Collection"
    if "_" in s and s.lower() == s:
        s = s.replace("_", " ")
    s = " ".join(s.split())
    return s.title() if s == s.lower() else s


_UNIT_TYPE_SECTIONS = frozenset({"chapter_section", "teaching_passage", "sutra", "verse", "chapter_summary"})


def _resolve_section(item: dict[str, Any]) -> str:
    """Prefer explicit section, then provenance fascicle/chapter label, then unit_type."""
    direct = _as_text(item.get("section"))
    if direct:
        token = direct.lower().replace(" ", "_")
        return _pretty_section(direct) if token in _UNIT_TYPE_SECTIONS else " ".join(direct.split()).strip()
    provenance = item.get("provenance")
    if isinstance(provenance, dict):
        prov = _as_text(provenance.get("section"))
        if prov:
            return " ".join(prov.split()).strip()
    unit_type = _as_text(item.get("unit_type"))
    return _pretty_section(unit_type) if unit_type else ""


def _pretty_section(v: str) -> str:
    s = " ".join(v.split()).strip().lower()
    if not s:
        return ""
    if s == "chapter_section":
        return "Chapter"
    if s == "teaching_passage":
        return "Teaching Passage"
    if s == "sutra":
        return "Sutra"
    if s == "verse":
        return "Verse"
    return s.capitalize()


def normalize_maturity(value: Any) -> str:
    raw = _as_text(value).lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "publishable": "publishable",
        "published": "publishable",
        "ready": "publishable",
        "strong": "strong_draft",
        "strong_draft": "strong_draft",
        "draft": "strong_draft",
        "needs_rewrite": "needs_rewrite",
        "rewrite": "needs_rewrite",
        "needs_rewrite_pass": "needs_rewrite",
        "structural": "structural_draft",
        "structural_draft": "structural_draft",
        "schema_only": "structural_draft",
    }
    return aliases.get(raw, "")


def _practice_is_generic(practice: str) -> bool:
    p = (practice or "").strip().lower()
    return bool(p) and any(marker in p for marker in GENERIC_PRACTICE_MARKERS)


def _commentary_is_authored(commentary: str) -> bool:
    """True only when commentary is real editorial work, not template filler.

    The bulk auto-enrichment pass produced two kinds of slop: short verbatim
    openers duplicated across hundreds of units, and per-unit one-liners. Both
    are rejected here so they never render or get embedded."""
    c = (commentary or "").strip()
    if not c:
        return False
    lowered = c.lower()
    if any(lowered.startswith(marker) for marker in TEMPLATE_COMMENTARY_MARKERS):
        return False
    # Structured layers (key terms / resonances) are a strong authored signal.
    if re.search(r"(?i)key terms|cross-tradition resonance", c):
        return True
    # Otherwise require enough substance to be more than a generated one-liner.
    return len(c) >= 220


def _looks_like_stub(out: dict[str, Any]) -> bool:
    """A unit with no authored commentary is a schema-only stub."""
    return not _commentary_is_authored(str(out.get("commentary", "")))


def _infer_maturity(item: dict[str, Any], out: dict[str, Any]) -> str:
    explicit = normalize_maturity(
        item.get("editorial_maturity") or item.get("maturity") or item.get("content_maturity")
    )
    if explicit:
        return explicit

    # Content signal drives maturity. A unit without authored commentary is a
    # structural draft no matter how strong its source tradition is.
    if not _commentary_is_authored(str(out.get("commentary", ""))):
        return "structural_draft"

    collection = str(out.get("collection", "")).lower()
    unit_id = str(out.get("_id", "")).lower()
    source = " ".join([collection, unit_id, str(out.get("title", "")).lower()])

    if any(name in source for name in PUBLISHABLE_COLLECTIONS):
        return "publishable"
    if "vijnana bhairava" in source or "vijñana bhairava" in source:
        match = re.search(r"yukti[_ ]?(\d{1,3})", unit_id)
        if match and int(match.group(1)) >= 38:
            return "needs_rewrite"
    # Authored content from any other collection is at least a strong draft.
    return "strong_draft"


def maturity_meets(value: Any, minimum: Any) -> bool:
    min_value = normalize_maturity(minimum)
    if not min_value:
        return True
    current = normalize_maturity(value) or "strong_draft"
    return MATURITY_ORDER.get(current, 0) >= MATURITY_ORDER[min_value]


def filter_by_maturity(items: list[dict[str, Any]], minimum: Any = None) -> list[dict[str, Any]]:
    if not normalize_maturity(minimum):
        return items
    return [v for v in items if maturity_meets(v.get("editorial_maturity"), minimum)]


_SUMMARY_SOURCE_RE = re.compile(r"^(?:ASG|PHR)_SUM_", re.I)
_SUMMARY_UNIT_RE = re.compile(r"(?:^|\.)(?:asg_sum|phr_sum)(?:_|\.|$)", re.I)


def is_chapter_summary_meta_unit(item: dict[str, Any]) -> bool:
    """True for chapter-range overview meta-units (not reader-facing verses)."""
    section = _as_text(item.get("section")).lower().replace(" ", "_")
    if section == "chapter_summary":
        return True
    provenance = item.get("provenance")
    if isinstance(provenance, dict):
        prov_section = _as_text(provenance.get("section")).lower().replace(" ", "_")
        if prov_section == "chapter_summary":
            return True
    for key in ("sutra_id", "source_id", "_id", "unit_id"):
        val = _as_text(item.get(key))
        if not val:
            continue
        if _SUMMARY_SOURCE_RE.match(val) or _SUMMARY_UNIT_RE.search(val):
            return True
    return False


def is_reader_facing_unit(item: dict[str, Any]) -> bool:
    return not is_chapter_summary_meta_unit(item)


def filter_reader_facing(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [v for v in items if is_reader_facing_unit(v)]


# Headings accept optional markdown prefixes ("###") and singular/plural and
# the trailing colon may or may not be present.
_KEY_TERMS_HEADING = r"key terms?"
_RESONANCE_HEADING = r"cross-tradition resonances?"
_PRACTICE_HEADING = r"practice(?:\s*\(abhyasa\))?|abhyasa"


def _strip_layer_tail(commentary: str) -> str:
    if not commentary:
        return ""
    match = re.search(
        rf"(?im)^\s*#*\s*(?:{_KEY_TERMS_HEADING}|{_RESONANCE_HEADING})\s*:?\s*$",
        commentary,
    )
    return commentary[: match.start()].strip() if match else commentary.strip()


def _extract_section(text: str, heading: str, next_headings: tuple[str, ...]) -> str:
    if not text:
        return ""
    next_pattern = "|".join(next_headings)
    pattern = (
        rf"(?ims)^\s*#*\s*(?:{heading})\s*:?\s*$\s*(.*?)"
        rf"(?=^\s*#*\s*(?:{next_pattern})\s*:?\s*$|\Z)"
    )
    match = re.search(pattern, text)
    return match.group(1).strip() if match else ""


def _parse_key_terms(text: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    if not text:
        return items
    # Accept "**term** — def", "**term** - def", and "**term:** def"; also
    # tolerate a leading bullet ("- " / "* ").
    for match in re.finditer(
        r"(?ms)^\s*[-*]?\s*\*\*(.+?)\*\*\s*[:—-]\s*(.*?)(?=\n\s*[-*]?\s*\*\*|\Z)", text
    ):
        term = " ".join(match.group(1).split()).rstrip(":")
        definition = match.group(2).strip()
        if term and definition:
            items.append({"term": term, "definition": definition})
    return items


def _parse_resonances(text: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    if not text:
        return items
    # Bold-citation style: "**Citation:** body" (also "**Citation**: body").
    for match in re.finditer(
        r"(?ms)^\s*[-*]?\s*\*\*(.+?)\*\*\s*:?\s*(.*?)(?=\n\s*[-*]?\s*\*\*|\Z)", text
    ):
        citation = " ".join(match.group(1).split()).rstrip(":")
        body = match.group(2).strip()
        parts = re.split(r"(?i)\*?Divergence:\*?", body, maxsplit=1)
        resonance = parts[0].strip()
        divergence = parts[1].strip() if len(parts) > 1 else ""
        if citation and resonance:
            items.append({"citation": citation, "resonance": resonance, "divergence": divergence})
    if items:
        return items
    # Bullet-list style (legacy Indic units): "- Author, *Text* Ref: body".
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith(("-", "*")):
            continue
        body = line.lstrip("-* ").strip()
        if ":" not in body:
            continue
        citation, _, rest = body.partition(":")
        citation = citation.replace("*", "").strip()
        rest = rest.strip()
        if citation and rest:
            items.append({"citation": citation, "resonance": rest, "divergence": ""})
    return items


_IAST_PLACEHOLDER_MARKERS = (
    "source-language basis",
    "no sanskrit",
    "not in corpus",
    "chinese text",
    "chinese source",
    "greek original",
    "greek text",
    "the enchiridion is a greek",
    "not applicable",
    "pending dedicated sanskrit",
)


def _has_real_transliteration(text: Any) -> bool:
    clean = _as_text(text)
    if not clean:
        return False
    if re.match(r"^\*\([^)]+\)\*\.?$", clean.strip()):
        return False
    if clean.startswith("*Source-language basis:*"):
        return False
    lowered = clean.lower()
    return not any(marker in lowered for marker in _IAST_PLACEHOLDER_MARKERS)


def _layer(kind: str, label: str, body: str, **extra: Any) -> dict[str, Any] | None:
    clean = _as_text(body)
    if kind == "iast" and not _has_real_transliteration(clean):
        clean = ""
    if not clean and not extra.get("items"):
        return None
    return {"kind": kind, "label": label, "body": clean, **extra}


def _finalize_layers(layers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Normalize display labels and drop IAST layers with no real transliteration."""
    out: list[dict[str, Any]] = []
    for layer in layers:
        kind = layer.get("kind")
        if kind == "iast":
            body = _as_text(layer.get("body"))
            items = layer.get("items") or []
            if not _has_real_transliteration(body) and not items:
                continue
            layer = {**layer, "label": "IAST"}
        elif kind == "original":
            layer = {**layer, "label": "Original"}
        out.append(layer)
    return out


def _derive_layers(out: dict[str, Any], raw_commentary: str = "") -> list[dict[str, Any]]:
    """Build the canonical layer set from flat fields + commentary parsing."""
    commentary = out.get("commentary", "")
    parse_source = raw_commentary or commentary
    key_terms_text = _extract_section(
        parse_source, _KEY_TERMS_HEADING, (_RESONANCE_HEADING, _PRACTICE_HEADING)
    )
    resonances_text = _extract_section(parse_source, _RESONANCE_HEADING, (_PRACTICE_HEADING,))
    key_terms = _parse_key_terms(key_terms_text)
    resonances = _parse_resonances(resonances_text)
    clean_commentary = _strip_layer_tail(parse_source) if parse_source else commentary

    candidates = [
        _layer("original", "Original", out.get("sanskrit", "")),
        _layer("iast", "IAST", out.get("transliteration", "")),
        _layer("translation", "Pratibha Translation", out.get("translation", "")),
        _layer("commentary", "Pratibha Commentary", clean_commentary),
        _layer("key_terms", "Key Terms", key_terms_text, items=key_terms),
        _layer("resonances", "Cross-Tradition Resonances", resonances_text, items=resonances),
        _layer("practice", "Practice (Abhyasa)", out.get("abhyasa", "")),
    ]
    for idx, appendix in enumerate(out.get("appendixes", [])):
        if isinstance(appendix, dict):
            label = _as_text(appendix.get("commentator")) or f"Appendix {idx + 1}"
            candidates.append(_layer("appendix", label, _as_text(appendix.get("text"))))
        else:
            candidates.append(_layer("appendix", f"Appendix {idx + 1}", _as_text(appendix)))
    return _finalize_layers([c for c in candidates if c is not None])


def _build_layers(item: dict[str, Any], out: dict[str, Any], raw_commentary: str = "") -> list[dict[str, Any]]:
    derived = _derive_layers(out, raw_commentary=raw_commentary)
    explicit = item.get("pratibha_layers")
    if not isinstance(explicit, list):
        return derived

    explicit_layers = [x for x in explicit if isinstance(x, dict) and x.get("kind")]
    if not explicit_layers:
        return derived

    # Merge: explicit layers win per-kind, derived layers fill the gaps. Strip
    # Key Terms / Resonances tails from explicit commentary so study view stays
    # readable; parsed structured layers from derived fill in when missing.
    by_kind = {layer["kind"]: layer for layer in derived}
    for layer in explicit_layers:
        kind = str(layer.get("kind") or "")
        merged = dict(layer)
        if kind == "commentary":
            merged["body"] = _strip_layer_tail(str(layer.get("body") or ""))
        by_kind[kind] = merged
    order = ["original", "iast", "translation", "commentary", "key_terms", "resonances", "practice", "appendix"]
    merged = sorted(by_kind.values(), key=lambda layer: order.index(layer["kind"]) if layer["kind"] in order else 99)
    return _finalize_layers(merged)


def _default_data_roots() -> list[str]:
    canonical = os.path.join(ROOT, "data", "canonical")
    legacy = os.path.join(ROOT, "data", "yaml")
    data_dir = os.environ.get("DATA_DIR", "").strip()
    if data_dir:
        return [os.path.join(ROOT, data_dir) if not os.path.isabs(data_dir) else data_dir]
    # Prefer canonical corpus if present.
    if os.path.isdir(canonical):
        return [canonical]
    return [legacy]


def _collection_label(item: dict[str, Any]) -> str:
    """Prefer canonical collection slug from provenance over per-treatise work_title."""
    provenance = item.get("provenance")
    if isinstance(provenance, dict):
        prov_coll = _as_text(provenance.get("collection"))
        if prov_coll:
            return prov_coll
    return _as_text(item.get("collection") or item.get("work_title") or item.get("work_id") or "Unknown Collection")


def _normalize(item: dict[str, Any], path: str) -> dict[str, Any]:
    out = dict(item)
    out["_id"] = _as_text(item.get("_id") or item.get("unit_id") or item.get("sutra_id") or os.path.splitext(os.path.basename(path))[0])
    out["collection"] = _humanize_collection(_collection_label(item))
    out["section"] = _resolve_section(item)
    out["sutra_id"] = _as_text(item.get("sutra_id") or item.get("source_id") or out["_id"])
    out["translation"] = _as_text(item.get("translation") or item.get("translation_literal"))
    raw_commentary = _as_text(item.get("commentary"))
    out["commentary"] = _strip_layer_tail(raw_commentary) if _commentary_is_authored(raw_commentary) else ""
    out["sanskrit"] = _as_text(item.get("sanskrit") or item.get("sanskrit_devanagari"))
    out["transliteration"] = _as_text(item.get("transliteration") or item.get("sanskrit_iast"))
    out["title"] = _as_text(item.get("title") or item.get("unit_label") or item.get("sutra") or out["sutra_id"])
    out["themes"] = item.get("themes") if isinstance(item.get("themes"), list) else []
    out["appendixes"] = item.get("appendixes") if isinstance(item.get("appendixes"), list) else []
    out["anchor_chapter"] = _as_text(item.get("anchor_chapter"))
    out["abhyasa"] = _as_text(item.get("abhyasa") or item.get("practice"))
    out["editorial_maturity"] = _infer_maturity(item, out)
    out["editorial_score"] = item.get("editorial_score") or item.get("content_score") or item.get("quality_score") or item.get("quality_score_unit") or 0
    # De-slop: drop template/filler commentary and boilerplate practice so the
    # app never renders fake insight and ingestion never embeds duplicate
    # near-identical chunks. The source text and translation are preserved.
    if not _commentary_is_authored(out["commentary"]):
        out["commentary"] = ""
    if _practice_is_generic(out["abhyasa"]):
        out["abhyasa"] = ""
    out["pratibha_layers"] = _build_layers(item, out, raw_commentary=raw_commentary)
    from .ttc_refs import humanize_ttc_unit, is_tao_te_ching
    from .ys_refs import enrich_patanjali_unit

    if is_tao_te_ching(out):
        out = humanize_ttc_unit(out)
    out = enrich_patanjali_unit(out)
    return out


def normalize_unit(item: dict[str, Any], path: str = "") -> dict[str, Any]:
    """Public entry point so ingestion/scripts share the API's normalization
    (editorial_maturity, pratibha_layers, etc.) instead of re-deriving it."""
    return _normalize(item, path)


def load_all() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    files_seen = 0
    parse_errors = 0
    duplicates: list[str] = []
    patterns = ["**/*.yml", "**/*.yaml"]
    for root in _default_data_roots():
        for pattern in patterns:
            for path in sorted(glob.glob(os.path.join(root, pattern), recursive=True)):
                if os.path.basename(path) == "_work.yml":
                    continue
                files_seen += 1
                try:
                    with open(path, "r", encoding="utf-8", errors="replace") as f:
                        item = yaml.safe_load(f)
                    if not isinstance(item, dict):
                        logger.warning("Skipping %s: top-level YAML is not a mapping", path)
                        parse_errors += 1
                        continue
                    norm = _normalize(item, path)
                    _id = norm["_id"]
                    if _id in seen:
                        duplicates.append(_id)
                        logger.warning("Duplicate unit id %r (from %s) ignored", _id, path)
                        continue
                    seen.add(_id)
                    out.append(norm)
                except Exception:  # noqa: BLE001 - keep loading the rest of the corpus
                    parse_errors += 1
                    logger.exception("Failed to load corpus file %s", path)
                    continue
    LOAD_STATS.update(
        {
            "files_seen": files_seen,
            "loaded": len(out),
            "parse_errors": parse_errors,
            "duplicate_ids": duplicates,
        }
    )
    logger.info(
        "Loaded %d verses from %d files (%d parse errors, %d duplicates)",
        len(out),
        files_seen,
        parse_errors,
        len(duplicates),
    )
    return out


_cached_verses: list[dict[str, Any]] | None = None
_cached_verse_by_id: dict[str, dict[str, Any]] | None = None


def corpus_ready() -> bool:
    """True once the on-disk corpus has been loaded into memory."""
    return _cached_verses is not None


def get_all_verses() -> list[dict[str, Any]]:
    """Load and cache the corpus on first access (keeps deploy health checks fast)."""
    global _cached_verses, _cached_verse_by_id
    if _cached_verses is None:
        _cached_verses = load_all()
        _cached_verse_by_id = {v["_id"]: v for v in _cached_verses}
    return _cached_verses


def __getattr__(name: str) -> Any:
    if name == "ALL_VERSES":
        return get_all_verses()
    if name == "VERSE_BY_ID":
        get_all_verses()
        assert _cached_verse_by_id is not None
        return _cached_verse_by_id
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def get_verse_by_id(verse_id: str) -> dict[str, Any] | None:
    get_all_verses()
    assert _cached_verse_by_id is not None
    return _cached_verse_by_id.get(verse_id)


def pick_daily(user_id: str = "guest", tz: str = "Europe/Paris", min_maturity: str | None = None):
    """Return one publishable passage for the current calendar day.

    Same verse for all visitors on a given date: SHA-1 of ``YYYY-M-D-guest`` picks
    a stable index into the maturity-filtered corpus. The day boundary follows
    ``tz`` (default Europe/Paris), so the passage changes at local midnight there.
    """
    items = filter_reader_facing(filter_by_maturity(get_all_verses(), min_maturity))
    if not items:
        # Do not silently fall back to the full (unfiltered) corpus: that would
        # surface unreviewed drafts on a curated surface. Signal "no match".
        logger.warning("pick_daily: no verses satisfy min_maturity=%r", min_maturity)
        return None
    now = datetime.datetime.now(pytz.timezone(tz))
    key = f"{now.year}-{now.month}-{now.day}-{user_id}"
    h = hashlib.sha1(key.encode()).hexdigest()
    idx = int(h, 16) % len(items)
    return items[idx]
