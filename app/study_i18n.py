"""On-demand study-layer translation. Original / IAST stay in source script."""

from __future__ import annotations

import hashlib
import json
import logging
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

from .llm import smart_chat

logger = logging.getLogger("pratibha.study_i18n")

LOCALES = {
    "fr": "French",
    "es": "Spanish",
    "pt-BR": "Brazilian Portuguese",
    "zh": "Simplified Chinese",
    "ru": "Russian",
    "ja": "Japanese",
    "ar": "Modern Standard Arabic",
}

SOURCE_KINDS = frozenset({"original", "iast"})
VERSE_BODY_KINDS = frozenset({"translation", "commentary", "practice"})
_CHUNK_CHARS = 7000

_CACHE_DIR = Path(__file__).resolve().parent.parent / "data" / "cache" / "study_i18n"
_memory: dict[str, str] = {}

_JSON_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.I)


def is_locale(value: str | None) -> bool:
    return bool(value) and value in LOCALES


def _cache_key(locale: str, kind: str, text: str) -> str:
    digest = hashlib.sha256(f"{locale}\n{kind}\n{text}".encode("utf-8")).hexdigest()
    return f"{locale}:{kind}:{digest}"


def _cache_path(key: str) -> Path:
    digest = key.rsplit(":", 1)[-1]
    return _CACHE_DIR / key.split(":", 1)[0] / f"{digest}.json"


def _read_cache(key: str) -> str | None:
    if key in _memory:
        return _memory[key]
    path = _cache_path(key)
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        text = str(payload.get("text") or "").strip()
    except (OSError, json.JSONDecodeError, TypeError):
        return None
    if text:
        _memory[key] = text
    return text or None


def _write_cache(key: str, text: str) -> None:
    _memory[key] = text
    path = _cache_path(key)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"text": text}, ensure_ascii=False), encoding="utf-8")
    except OSError as err:
        logger.warning("study i18n cache write failed: %s", err)


def _parse_object(raw: str) -> dict[str, str]:
    cleaned = _JSON_FENCE.sub("", raw.strip()).strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start < 0 or end <= start:
        return {}
    try:
        data = json.loads(cleaned[start : end + 1])
    except json.JSONDecodeError:
        return {}
    if not isinstance(data, dict):
        return {}
    out: dict[str, str] = {}
    for key, value in data.items():
        if isinstance(key, str) and isinstance(value, str) and value.strip():
            out[key] = value.strip()
    return out


def _system_prompt(locale: str) -> str:
    language = LOCALES[locale]
    return f"""You translate Pratibha study text into {language} for a living manuscript of world wisdom.

Rules:
- Write in {language} at the same register: precise, present-tense where the English is, readable aloud.
- Keep Sanskrit, Greek, Chinese, Arabic, Hebrew, and IAST terms in their scholarly form (ātman, pratyabhijñā, dao, logos). If the English already glosses a term, gloss it in {language}.
- Preserve markdown, italics, line breaks, verse numbers, and citations.
- Do not invent claims. Commentary must stay a philosophical claim, not a restatement of the translation.
- Practice stays an instruction the reader can do today.
- Titles stay titles: same length and pedagogical force, not explanations.
- Key-term heads that are already IAST or source script stay as they are; translate the gloss.
- Citations stay in scholarly form; translate the resonance and divergence sentences.
- Do not translate source-script or IAST-only strings if they appear.
- Return JSON only: an object whose keys match the input keys exactly."""


async def translate_fields(locale: str, fields: dict[str, str]) -> dict[str, str]:
    """Translate named study fields. Unknown locales or empty maps return as-is."""
    if not is_locale(locale) or not fields:
        return {key: value for key, value in fields.items() if value.strip()}

    pending: dict[str, str] = {}
    resolved: dict[str, str] = {}
    for key, value in fields.items():
        text = (value or "").strip()
        if not text:
            continue
        kind = key.split(":", 1)[0] if ":" in key else key
        if kind in SOURCE_KINDS:
            resolved[key] = text
            continue
        cache_key = _cache_key(locale, kind, text)
        cached = _read_cache(cache_key)
        if cached:
            resolved[key] = cached
        else:
            pending[key] = text

    if not pending:
        return resolved

    translated: dict[str, str] = {}
    for chunk in _chunks(pending):
        translated.update(await _translate_chunk(locale, chunk))

    for key, source in pending.items():
        text = translated.get(key, "").strip()
        if not text:
            resolved[key] = source
            continue
        kind = key.split(":", 1)[0] if ":" in key else key
        _write_cache(_cache_key(locale, kind, source), text)
        resolved[key] = text
    return resolved


def _chunks(pending: dict[str, str]) -> list[dict[str, str]]:
    chunks: list[dict[str, str]] = []
    current: dict[str, str] = {}
    size = 0
    for key, text in pending.items():
        extra = len(key) + len(text) + 8
        if current and size + extra > _CHUNK_CHARS:
            chunks.append(current)
            current = {}
            size = 0
        current[key] = text
        size += extra
    if current:
        chunks.append(current)
    return chunks


async def _translate_chunk(locale: str, pending: dict[str, str]) -> dict[str, str]:
    try:
        raw = await smart_chat(
            [
                {"role": "system", "content": _system_prompt(locale)},
                {"role": "user", "content": json.dumps(pending, ensure_ascii=False)},
            ],
            temperature=0.2,
            max_tokens=3500,
        )
        return _parse_object(raw)
    except Exception:
        logger.exception("study i18n failed for %s (%s fields)", locale, len(pending))
        return {}


def extract_verse_fields(verse: dict[str, Any]) -> dict[str, str]:
    fields: dict[str, str] = {}
    title = str(verse.get("title") or "").strip()
    if title:
        fields["title"] = title
    thesis = str(verse.get("thesis") or "").strip()
    if thesis:
        fields["thesis"] = thesis
    layers = verse.get("pratibha_layers")
    term_i = 0
    res_i = 0
    app_i = 0
    if isinstance(layers, list):
        for layer in layers:
            if not isinstance(layer, dict):
                continue
            kind = str(layer.get("kind") or "")
            if kind in SOURCE_KINDS:
                continue
            if kind in VERSE_BODY_KINDS:
                body = str(layer.get("body") or "").strip()
                if body:
                    fields[kind] = body
                provenance = str(layer.get("layer_provenance") or "").strip()
                if provenance:
                    fields[f"provenance:{kind}"] = provenance
                continue
            items = layer.get("items")
            if kind == "key_terms" and isinstance(items, list):
                for entry in items:
                    if not isinstance(entry, dict):
                        continue
                    definition = str(entry.get("definition") or "").strip()
                    if definition:
                        fields[f"key_term:{term_i}"] = definition
                        term_i += 1
            elif kind == "resonances" and isinstance(items, list):
                for entry in items:
                    if not isinstance(entry, dict):
                        continue
                    resonance = str(entry.get("resonance") or "").strip()
                    divergence = str(entry.get("divergence") or "").strip()
                    if resonance:
                        fields[f"resonance:{res_i}"] = resonance
                    if divergence:
                        fields[f"divergence:{res_i}"] = divergence
                    res_i += 1
            elif kind == "appendix":
                body = str(layer.get("body") or "").strip()
                if body:
                    fields[f"appendix:{app_i}"] = body
                    app_i += 1
    if "translation" not in fields:
        text = str(verse.get("translation") or "").strip()
        if text:
            fields["translation"] = text
    if "commentary" not in fields:
        text = str(verse.get("commentary") or "").strip()
        if text:
            fields["commentary"] = text
    if "practice" not in fields:
        text = str(verse.get("practice") or verse.get("abhyasa") or "").strip()
        if text:
            fields["practice"] = text
    themes = verse.get("themes")
    if isinstance(themes, list):
        for idx, theme in enumerate(themes):
            text = str(theme or "").strip()
            if text:
                fields[f"theme:{idx}"] = text
    return fields


def apply_verse_fields(verse: dict[str, Any], fields: dict[str, str]) -> dict[str, Any]:
    out = deepcopy(verse)
    if fields.get("title"):
        out["title"] = fields["title"]
    if fields.get("thesis"):
        out["thesis"] = fields["thesis"]
    if fields.get("translation"):
        out["translation"] = fields["translation"]
    if fields.get("commentary"):
        out["commentary"] = fields["commentary"]
    if fields.get("practice"):
        out["practice"] = fields["practice"]
        if out.get("abhyasa"):
            out["abhyasa"] = fields["practice"]
    themes = out.get("themes")
    if isinstance(themes, list):
        out["themes"] = [fields.get(f"theme:{idx}") or theme for idx, theme in enumerate(themes)]
    layers = out.get("pratibha_layers")
    term_i = 0
    res_i = 0
    app_i = 0
    if isinstance(layers, list):
        for layer in layers:
            if not isinstance(layer, dict):
                continue
            kind = str(layer.get("kind") or "")
            if kind in SOURCE_KINDS:
                continue
            if kind in VERSE_BODY_KINDS:
                if fields.get(kind):
                    layer["body"] = fields[kind]
                if fields.get(f"provenance:{kind}"):
                    layer["layer_provenance"] = fields[f"provenance:{kind}"]
                continue
            items = layer.get("items")
            if kind == "key_terms" and isinstance(items, list):
                for entry in items:
                    if not isinstance(entry, dict) or not str(entry.get("definition") or "").strip():
                        continue
                    text = fields.get(f"key_term:{term_i}")
                    term_i += 1
                    if text:
                        entry["definition"] = text
            elif kind == "resonances" and isinstance(items, list):
                for entry in items:
                    if not isinstance(entry, dict):
                        continue
                    if fields.get(f"resonance:{res_i}"):
                        entry["resonance"] = fields[f"resonance:{res_i}"]
                    if fields.get(f"divergence:{res_i}"):
                        entry["divergence"] = fields[f"divergence:{res_i}"]
                    res_i += 1
            elif kind == "appendix":
                text = fields.get(f"appendix:{app_i}")
                if str(layer.get("body") or "").strip():
                    if text:
                        layer["body"] = text
                    app_i += 1
    return out


async def localize_verse(verse: dict[str, Any], locale: str) -> dict[str, Any]:
    if not is_locale(locale):
        return verse
    fields = extract_verse_fields(verse)
    if not fields:
        return verse
    translated = await translate_fields(locale, fields)
    return apply_verse_fields(verse, translated)
