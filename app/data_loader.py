import datetime
import glob
import hashlib
import json
import logging
import os
import ast
import re
from typing import Any

import pytz
import yaml

logger = logging.getLogger("pratibha.data_loader")

ROOT = os.path.dirname(os.path.dirname(__file__))

# Graded maturity ladder, keyed to the richness framework: a passage's tier is
# derived from the layers it actually carries, not from a collection allowlist.
#   seed     — source present, but no authored elaboration yet
#   draft    — authored commentary, but the scaffold is incomplete
#   rich     — full scaffold (original + translation + commentary + key terms +
#              ≥2 resonances + practice): ready to elaborate / daily-eligible
#   polished — rich AND editorially blessed
# The retired labels (structural_draft / needs_rewrite / strong_draft /
# publishable) live on only as input aliases in normalize_maturity().
MATURITY_ORDER = {
    "seed": 0,
    "draft": 1,
    "rich": 2,
    "polished": 3,
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


_UNIT_TYPE_SECTIONS = frozenset({"chapter_section", "teaching_passage", "sutra", "verse", "chapter_summary", "chapter"})


def _location_from_sutra_id(item: dict[str, Any]) -> str:
    """Derive a reader-facing verse/chapter label from sutra_id / _id patterns."""
    sid = _as_text(item.get("sutra_id") or item.get("source_id") or item.get("_id") or item.get("unit_id"))
    if not sid:
        return ""
    m = re.match(r"^TTC(?:_MD)?_(\d+)$", sid, re.I)
    if m:
        return f"Chapter {int(m.group(1))}"
    m = re.match(r"^BG_(\d+)_(\d+)(?:_(\d+))?$", sid, re.I)
    if m:
        ch, a = int(m.group(1)), int(m.group(2))
        b = int(m.group(3)) if m.group(3) else None
        return f"{ch}.{a}–{b}" if b is not None else f"{ch}.{a}"
    m = re.match(r"^ASG_(\d+)_(\d+)$", sid, re.I)
    if m:
        return f"Verse {int(m.group(1))}.{int(m.group(2))}"
    m = re.match(r"^YS_(\d+)_(\d+)(?:_(\d+))?$", sid, re.I)
    if m:
        pada, a = int(m.group(1)), int(m.group(2))
        b = int(m.group(3)) if m.group(3) else None
        # Clustered units span several sūtras — show the full range (e.g. 2.4–2.6).
        return f"{pada}.{a}–{pada}.{b}" if b is not None else f"{pada}.{a}"
    m = re.match(r"^AN_(\d+)_(\d+)$", sid, re.I)
    if m:
        return f"{int(m.group(1))}.{int(m.group(2))}"
    return ""


def _resolve_section(item: dict[str, Any]) -> str:
    """Prefer numbered citation, then explicit section, then provenance, then unit_type."""
    from_id = _location_from_sutra_id(item)
    direct = _as_text(item.get("section"))
    if direct:
        token = direct.lower().replace(" ", "_")
        if token in _UNIT_TYPE_SECTIONS:
            # Schema token like chapter_section — never show raw; prefer numbered id.
            return from_id or _pretty_section(direct)
        # chapter_01 → Chapter 1 when we lack a finer verse id
        if token.startswith("chapter_") and token[8:].isdigit():
            return from_id or f"Chapter {int(token[8:])}"
        return " ".join(direct.split()).strip()
    if from_id:
        return from_id
    provenance = item.get("provenance")
    if isinstance(provenance, dict):
        prov = _as_text(provenance.get("section"))
        if prov:
            return " ".join(prov.split()).strip()
    unit_type = _as_text(item.get("unit_type"))
    return from_id or (_pretty_section(unit_type) if unit_type else "")


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
        # New graded ladder
        "seed": "seed",
        "draft": "draft",
        "rich": "rich",
        "polished": "polished",
        # Retired labels kept as back-compat input aliases (old API params,
        # stored yml values) → mapped onto the graded ladder.
        "structural_draft": "seed",
        "structural": "seed",
        "schema_only": "seed",
        "unreviewed": "seed",
        "needs_rewrite": "draft",
        "needs_rewrite_pass": "draft",
        "rewrite": "draft",
        "strong_draft": "draft",
        "strong": "draft",
        "publishable": "polished",
        "published": "polished",
        "ready": "polished",
        "canonical": "polished",
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
    if "in giles's 1889 rendering" in lowered or "display layers do not reproduce giles" in lowered:
        return False
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
    """Grade a fully-built unit onto the seed/draft/rich/polished ladder from the
    content it actually carries. Any explicit ``polished``/``publishable`` flag
    (or a passage from a hand-blessed collection) can only *promote* a unit that
    already clears the ``rich`` bar — it can no longer mint quality on its own,
    the way the old collection allowlist did."""
    has_commentary = _commentary_is_authored(str(out.get("commentary", "")))
    present = _daily_present_layers(out)
    has_source = bool({"original", "translation"} & present)

    if _is_daily_rich(out):
        explicit = normalize_maturity(
            item.get("editorial_maturity") or item.get("maturity") or item.get("content_maturity")
        )
        source = " ".join([
            str(out.get("collection", "")).lower(),
            str(out.get("_id", "")).lower(),
            str(out.get("title", "")).lower(),
        ])
        blessed = explicit == "polished" or any(name in source for name in PUBLISHABLE_COLLECTIONS)
        return "polished" if blessed else "rich"
    if has_commentary:
        return "draft"
    if has_source:
        return "seed"
    return "seed"


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
    "chinese source text tradition",
    "greek original",
    "greek text",
    "greek original not in corpus",
    "the enchiridion is a greek",
    "not applicable",
    "pending dedicated sanskrit",
    "n/a, as the key",
)

_NON_SANSKRIT_COLLECTION = re.compile(
    r"heraclitus|fragment|epictetus|enchiridion|meditations|phaedo|plato|plotinus|ennead|"
    r"eckhart|ibn.?arabi|know.?yourself|balyani|rumi|mathnawi|"
    r"tao|te.?ching|zhuang|chuang|lao.?tzu|confucius|analect|"
    r"milarepa|jetsun|tibet|dogen|dōgen|shobogenzo|shōbōgenzō",
    re.I,
)

_SANSKRIT_COLLECTION = re.compile(
    r"upanishad|upaniṣad|chandogya|isavasya|svetasvatara|mandukya|bhagavad.?gita|"
    r"astavakra|ashtavakra|aṣṭāvakra|patanjali|patañjali|yoga.?s[uū]tra|"
    r"vijnana|bhairava|shiva|siva|tantra|spanda|yogin[iī]|pratyabhij|kashmir|"
    r"nagarjuna|madhyamaka|mmk|shantideva|śāntideva|bodhicary|"
    r"heart.?s[uū]tra|prajnaparamita|tilopa|maha.?mudra",
    re.I,
)


def _contains_devanagari(text: str) -> bool:
    return bool(re.search(r"[\u0900-\u097F]", text))


def _contains_tibetan(text: str) -> bool:
    return bool(re.search(r"[\u0F00-\u0FFF]", text))


# Any recognized source script \u2014 Devan\u0101gar\u012B, Tibetan, Greek, Hebrew, Arabic,
# Coptic, CJK, Kana \u2014 so the Original layer surfaces the real script universally,
# not just for Sanskrit/Tibetan.
_SOURCE_SCRIPT_RE = re.compile(
    r"[\u0900-\u097F\u0F00-\u0FFF\u0370-\u03FF\u1F00-\u1FFF"
    r"\u0590-\u05FF\u0600-\u06FF\u2C80-\u2CFF\u3040-\u30FF\u4E00-\u9FFF]"
)


def _contains_source_script(text: str) -> bool:
    return bool(_SOURCE_SCRIPT_RE.search(text))


def _raw_source_script(item: dict[str, Any]) -> str:
    """Best available raw source script for the Original layer.

    The authored `pratibha_layers` "original" body is sometimes a romanization
    (Wylie for the Tibetan songs) or a "*Source-language basis:*" note, while
    the actual script sits unused in `tibetan_uchen` / `sanskrit_devanagari`.
    Prefer real script (Tibetan Uchen, then Devanagari) over any romanized or
    placeholder body so the Original layer shows the source, not a transcription.
    """
    for key in ("tibetan_uchen", "sanskrit_devanagari", "sanskrit"):
        value = _as_text(item.get(key))
        if value and _contains_source_script(value):
            return value
    return ""


_ORIGINAL_PLACEHOLDER_RE = re.compile(
    r"(?i)source-language basis|not in corpus|no sanskrit|greek (?:original|text)|"
    r"chinese source|not applicable|see original|romanization|refer to|original layer|"
    r"pending dedicated|source text (?:not|tradition)"
)


def _is_placeholder_original(text: str) -> bool:
    """A note like '*Source-language basis: …*' parked in the original slot — not a
    real original. Real script or genuine romanized text never matches."""
    clean = text.strip()
    if not clean or _contains_source_script(clean):
        return False
    return clean.startswith("*") or bool(_ORIGINAL_PLACEHOLDER_RE.search(clean))


def _passage_uses_iast(out: dict[str, Any]) -> bool:
    collection = _as_text(out.get("collection"))
    if collection and _NON_SANSKRIT_COLLECTION.search(collection):
        return False
    if collection and _SANSKRIT_COLLECTION.search(collection):
        return True
    original = _as_text(out.get("sanskrit"))
    return _contains_devanagari(original)


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


_EDITORIAL_ASIDE_RES = (
    re.compile(r"\[[^\]]{0,160}(?:supplementary|spurious)[^\]]*\]", re.I),
    re.compile(r"The above is from[^.!?]{0,180}[.!?]", re.I),
    re.compile(r"It is interesting to note[^.!?]{0,280}[.!?]", re.I),
    re.compile(r"These words help to elucidate[^.!?]{0,280}[.!?]", re.I),
    re.compile(r"This is an anachronism\.[^.!?]{0,220}(?:\.[^.!?]{0,200}\.)?", re.I),
    re.compile(r"Tota formatio[^.!?]{0,220}[.!?]", re.I),
    re.compile(r"\bSwedenborg\.?"),
    re.compile(r"Whose tutor he was\.", re.I),
    re.compile(r"See (?:ch\.|chapter|p\.)\s*[\divx]+\.?", re.I),
    re.compile(r"These [\"“]poles[\"”] are[^.!?]{0,220}[.!?]", re.I),
)


def _strip_editorial_asides(text: str) -> str:
    out = text or ""
    for rx in _EDITORIAL_ASIDE_RES:
        out = rx.sub(" ", out)
    return re.sub(r"[ \t]+", " ", out).replace(" \n", "\n").strip()


def _study_excerpt(text: str, max_len: int = 900) -> str:
    compact = re.sub(r"\s+", " ", (text or "")).strip()
    if len(compact) <= max_len:
        return compact
    slice_ = compact[:max_len]
    end = max(slice_.rfind(".”"), slice_.rfind(". "), slice_.rfind("? "), slice_.rfind("! "))
    return (slice_[: end + 1] if end > 220 else slice_).strip()


def _is_wholesale_pd_translation(layer: dict[str, Any], out: dict[str, Any] | None) -> bool:
    prov = _as_text(layer.get("layer_provenance")).lower()
    body = _as_text(layer.get("body"))
    if "giles" in prov:
        return True
    if "normalized from" in prov and re.search(r"\bpd\b|public domain", prov) and len(body) > 900:
        return True
    blob = " ".join(
        [
            _as_text((out or {}).get("_id")),
            _as_text((out or {}).get("sutra_id")),
            _as_text((out or {}).get("work_id")),
            _as_text((out or {}).get("collection")),
        ]
    )
    if re.search(r"\.ctz_\d+", blob, re.I):
        return True
    if re.search(r"chuang|zhuang", blob, re.I) and re.search(
        r"Do-nothing Say-nothing|Tao-Tê-Ching|cogitations|Tzŭ|Chuang Tzŭ", body
    ):
        return True
    return False


def _finalize_layers(layers: list[dict[str, Any]], out: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Normalize display labels and drop IAST layers for non-Sanskrit passages."""
    uses_iast = _passage_uses_iast(out) if out else True
    result: list[dict[str, Any]] = []
    for layer in layers:
        kind = layer.get("kind")
        if kind == "iast":
            if not uses_iast:
                continue
            body = _as_text(layer.get("body"))
            items = layer.get("items") or []
            if not _has_real_transliteration(body) and not items:
                continue
            layer = {**layer, "label": "IAST"}
        elif kind == "original":
            body = _as_text(layer.get("body"))
            # Suppress placeholder-only originals ("*Source-language basis:* …")
            # when no real script backs them — showing an editorial note as the
            # Original layer is misleading (e.g. Bhagavad Gita has no Devanagari
            # in the corpus yet). Genuine non-Devanagari originals (Chinese,
            # Greek, romanized Pali) carry no such marker and are kept.
            if body.startswith("*Source-language basis:*") and not (
                _contains_devanagari(body) or _contains_tibetan(body)
            ):
                continue
            layer = {**layer, "label": "Original"}
        elif kind == "commentary":
            if not _commentary_is_authored(_as_text(layer.get("body"))):
                continue
        elif kind == "practice":
            if _practice_is_generic(_as_text(layer.get("body"))):
                continue
        elif kind == "translation" and _is_wholesale_pd_translation(layer, out):
            layer = {**layer, "body": _study_excerpt(_strip_editorial_asides(_as_text(layer.get("body"))))}
        result.append(layer)
    return result


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
    return _finalize_layers([c for c in candidates if c is not None], out)


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
    raw_script = _as_text(out.get("sanskrit"))
    raw_script_is_script = _contains_tibetan(raw_script) or _contains_devanagari(raw_script)
    for layer in explicit_layers:
        kind = str(layer.get("kind") or "")
        merged = dict(layer)
        if kind == "commentary":
            merged["body"] = _strip_layer_tail(str(layer.get("body") or ""))
            if not _commentary_is_authored(merged["body"]):
                continue
        if kind == "original" and raw_script_is_script:
            # Never let an authored romanization / "*Source-language basis:*"
            # note occupy the Original slot when actual source script exists.
            body = _as_text(layer.get("body"))
            if not (_contains_tibetan(body) or _contains_devanagari(body)):
                merged["body"] = raw_script
        by_kind[kind] = merged
    order = ["original", "iast", "translation", "commentary", "key_terms", "resonances", "practice", "appendix"]
    merged = sorted(by_kind.values(), key=lambda layer: order.index(layer["kind"]) if layer["kind"] in order else 99)
    return _finalize_layers(merged, out)


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
    out["sanskrit"] = _raw_source_script(item) or _as_text(item.get("sanskrit") or item.get("sanskrit_devanagari"))
    # Never surface a "*Source-language basis: …*" placeholder as the Original — show
    # real source text or nothing, so the Original layer is consistent across the corpus.
    if _is_placeholder_original(out["sanskrit"]):
        out["sanskrit"] = ""
    out["transliteration"] = _as_text(item.get("transliteration") or item.get("sanskrit_iast"))
    out["title"] = _as_text(item.get("title") or item.get("unit_label") or item.get("sutra") or out["sutra_id"])
    out["themes"] = item.get("themes") if isinstance(item.get("themes"), list) else []
    out["appendixes"] = item.get("appendixes") if isinstance(item.get("appendixes"), list) else []
    out["anchor_chapter"] = _as_text(item.get("anchor_chapter"))
    out["abhyasa"] = _as_text(item.get("abhyasa") or item.get("practice"))
    out["editorial_score"] = item.get("editorial_score") or item.get("content_score") or item.get("quality_score") or item.get("quality_score_unit") or 0
    # De-slop: drop template/filler commentary and boilerplate practice so the
    # app never renders fake insight and ingestion never embeds duplicate
    # near-identical chunks. The source text and translation are preserved.
    if not _commentary_is_authored(out["commentary"]):
        out["commentary"] = ""
    if _practice_is_generic(out["abhyasa"]):
        out["abhyasa"] = ""
        out["practice"] = ""
    out["pratibha_layers"] = _build_layers(item, out, raw_commentary=raw_commentary)
    from .ttc_refs import humanize_ttc_unit, is_tao_te_ching
    from .ys_refs import enrich_patanjali_unit

    if is_tao_te_ching(out):
        out = humanize_ttc_unit(out)
    out = enrich_patanjali_unit(out)
    # Grade maturity last, once every layer (and any enrichment) is in place, so
    # the graded tier reflects the fully-built unit.
    out["editorial_maturity"] = _infer_maturity(item, out)
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


import threading

_cached_verses: list[dict[str, Any]] | None = None
_cached_verse_by_id: dict[str, dict[str, Any]] | None = None
# Guards the one-time load so the startup warm task and the first request can't
# both parse the ~900-file corpus concurrently (double work + a window where the
# id index is inconsistent).
_load_lock = threading.Lock()


def corpus_ready() -> bool:
    """True once the on-disk corpus has been loaded into memory."""
    return _cached_verses is not None


def get_all_verses() -> list[dict[str, Any]]:
    """Load and cache the corpus on first access (keeps deploy health checks fast)."""
    global _cached_verses, _cached_verse_by_id
    if _cached_verses is not None:
        return _cached_verses
    with _load_lock:
        # Re-check inside the lock: another thread may have finished loading
        # while we were blocked.
        if _cached_verses is None:
            verses = load_all()
            _cached_verse_by_id = {v["_id"]: v for v in verses}
            _cached_verses = verses  # publish last so readers never see a partial index
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


# A daily passage is scaffolding for further elaboration (chat, lexicon, threads,
# practice), so it must carry the hooks each of those needs. Require the full
# layered scaffold before a passage is eligible to be the verse of the day.
_DAILY_MIN_RESONANCES = 2
_DAILY_MIN_TRANSLATION_CHARS = 120
_DAILY_PER_COLLECTION_CAP = 12  # keep any one tradition from dominating the rotation
_DAILY_EPOCH = datetime.date(2001, 1, 1)


def _daily_present_layers(v: dict[str, Any]) -> set[str]:
    """Layer kinds that actually carry content (non-empty body or items)."""
    present: set[str] = set()
    for layer in v.get("pratibha_layers", []):
        if not isinstance(layer, dict):
            continue
        if _as_text(layer.get("body")).strip() or layer.get("items"):
            present.add(str(layer.get("kind")))
    return present


def _daily_resonance_count(v: dict[str, Any]) -> int:
    return sum(
        len(layer.get("items") or [])
        for layer in v.get("pratibha_layers", [])
        if isinstance(layer, dict) and layer.get("kind") == "resonances"
    )


def _daily_translation_len(v: dict[str, Any]) -> int:
    for layer in v.get("pratibha_layers", []):
        if isinstance(layer, dict) and layer.get("kind") == "translation":
            return len(_as_text(layer.get("body")))
    return 0


def _is_daily_rich(v: dict[str, Any]) -> bool:
    """True when a passage carries every hook elaboration builds on: a source
    Original, a substantive translation, commentary, key terms (lexicon),
    cross-tradition resonances (threads), and a practice (embodiment)."""
    present = _daily_present_layers(v)
    if not {"original", "translation", "commentary", "key_terms", "practice"} <= present:
        return False
    if _daily_resonance_count(v) < _DAILY_MIN_RESONANCES:
        return False
    if _daily_translation_len(v) < _DAILY_MIN_TRANSLATION_CHARS:
        return False
    return True


def _daily_richness_score(v: dict[str, Any]) -> tuple:
    """Rank within a collection when capping: publishable first, then reach."""
    return (
        1 if v.get("editorial_maturity") == "publishable" else 0,
        min(_daily_resonance_count(v), 4),
        _daily_translation_len(v),
        # stable tiebreak so the cap is deterministic across processes
        hashlib.sha1(_as_text(v.get("_id")).encode()).hexdigest(),
    )


def _daily_order(pool: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Deterministic rotation over the rich pool that (a) caps each collection so
    no tradition dominates and (b) spreads every collection evenly across the
    cycle, so consecutive days rarely repeat a tradition and no passage recurs
    until the whole cycle is exhausted."""
    by_coll: dict[str, list[dict[str, Any]]] = {}
    for v in pool:
        by_coll.setdefault(_as_text(v.get("collection")), []).append(v)

    capped: list[tuple[float, str, dict[str, Any]]] = []
    for coll, members in by_coll.items():
        members = sorted(members, key=_daily_richness_score, reverse=True)[:_DAILY_PER_COLLECTION_CAP]
        size = len(members)
        for i, v in enumerate(members):
            # Even-spread position in [0,1): interleaves large and small
            # collections uniformly across the rotation.
            frac = (i + 0.5) / size
            tie = hashlib.sha1((coll + _as_text(v.get("_id"))).encode()).hexdigest()
            capped.append((frac, tie, v))
    capped.sort(key=lambda t: (t[0], t[1]))
    return [t[2] for t in capped]


def _load_daily_anchors() -> set[str]:
    """Approved curated anchor _ids (data/daily_anchors.json), or empty set.

    Kept intentionally cheap and forgiving: a missing or malformed file simply
    means "no curated override yet", so the gate-only rotation stays in effect.
    """
    path = os.path.join(ROOT, "data", "daily_anchors.json")
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, dict):
            data = data.get("anchors", [])
        return {str(x) for x in data} if isinstance(data, list) else set()
    except (OSError, ValueError):
        return set()


def pick_daily(user_id: str = "guest", tz: str = "Europe/Paris", min_maturity: str | None = None):
    """Return one rich, self-contained passage for the current calendar day.

    The verse of the day is scaffolding for elaboration and, for logged-out
    visitors, the whole taste of the manuscript — so it is drawn from a
    richness-gated pool (full layered scaffold), balanced across traditions and
    spread so the same passage never recurs until the rotation is exhausted.
    Same verse for every visitor on a given date; the day boundary follows ``tz``.
    """
    items = filter_reader_facing(filter_by_maturity(get_all_verses(), min_maturity))
    if not items:
        # Do not silently fall back to the full (unfiltered) corpus: that would
        # surface unreviewed drafts on a curated surface. Signal "no match".
        logger.warning("pick_daily: no verses satisfy min_maturity=%r", min_maturity)
        return None

    # Prefer the richness-gated pool; degrade gracefully if it is ever empty
    # (e.g. a very narrow maturity filter) rather than returning nothing.
    rich = [v for v in items if _is_daily_rich(v)]

    # Optional editorial override: once a curated anchor set is approved (a JSON
    # array of unit _ids at data/daily_anchors.json), the rotation draws only
    # from those iconic passages. Absent/empty file → gate-only behaviour.
    anchors = _load_daily_anchors()
    if anchors:
        anchored = [v for v in rich if _as_text(v.get("_id")) in anchors]
        if anchored:
            rich = anchored

    order = _daily_order(rich) if rich else items
    if not order:
        order = items

    now = datetime.datetime.now(pytz.timezone(tz))
    epoch_day = (now.date() - _DAILY_EPOCH).days
    return order[epoch_day % len(order)]
