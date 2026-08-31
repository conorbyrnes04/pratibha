#!/usr/bin/env python3
"""Split buried Key Terms / Resonances out of living-tradition commentary.

Writes canonical YAML only (no staging, no pgvector). English-source works keep
Original and do not invent a duplicate Translation; Ellis òwe keep Translation
and do not invent a Yoruba original.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.data_loader import (  # noqa: E402
    _KEY_TERMS_HEADING,
    _PRACTICE_HEADING,
    _RESONANCE_HEADING,
    _extract_section,
    _parse_key_terms,
    _parse_resonances,
    _strip_layer_tail,
)

CANONICAL = ROOT / "data" / "canonical"
COLLECTIONS = (
    "yoruba_proverbs",
    "johnson_yoruba_religion",
    "eastman_soul_of_the_indian",
    "zitkala_sa_old_indian_legends",
)
ENGLISH_SOURCE = {
    "johnson_yoruba_religion",
    "eastman_soul_of_the_indian",
    "zitkala_sa_old_indian_legends",
}
LAYER_ORDER = ("original", "translation", "commentary", "key_terms", "resonances", "practice")
KEY_ORDER = (
    "source_id",
    "category",
    "work_id",
    "work_title",
    "unit_id",
    "unit_label",
    "title",
    "unit_type",
    "original",
    "translation",
    "commentary",
    "practice",
    "abhyasa",
    "themes",
    "tags",
    "quality_score",
    "editorial_score",
    "editorial_maturity",
    "translation_provenance",
    "pratibha_layers",
    "provenance",
)


def _first_sentence(text: str) -> str:
    compact = " ".join((text or "").split())
    if not compact:
        return ""
    parts = re.split(r"(?<=[.!?])\s+", compact, maxsplit=1)
    return parts[0].strip()


_DANGLING_TAIL = re.compile(
    r"\b(and|the|of|a|an|to|toward|for|with|from|that|which|was|were|whose|"
    r"then|yet|by|is|or|our|i|finally|being|brought|not)$",
    re.I,
)


def untruncate_title(title: str, source: str) -> str:
    raw = (title or "").replace("...", "…").strip()
    src = " ".join((source or "").split())
    if not raw.endswith("…") or not src:
        return (title or "").strip()
    stem = raw[:-1].rstrip()
    if len(stem) < 12 or not src.lower().startswith(stem[:24].lower()):
        return title.strip()
    if len(src) <= 110:
        return src.rstrip(".")
    first = _first_sentence(src)
    if 12 <= len(first) <= 110:
        return first.rstrip(".")
    filled = src[:110]
    cut = filled.rsplit(" ", 1)[0].rstrip(",;:")
    return cut or stem


def polish_long_title(title: str, source: str) -> str:
    """Complete-clause titles for English originals that were cut mid-phrase."""
    src = " ".join((source or "").split())
    first = _first_sentence(src) or src
    current = " ".join((title or "").split()).rstrip(".")
    if not current:
        current = title.strip()
    is_prefix = bool(src) and len(current) >= 20 and src.lower().startswith(current[:40].lower())
    dangling = bool(_DANGLING_TAIL.search(current)) or current.endswith((",", ";", "—", "–", "“", '"'))
    if not is_prefix and not dangling:
        return current
    if 20 <= len(first) <= 90:
        return first.rstrip(".!")
    prefixes: list[str] = []
    for match in re.finditer(r"[,;—]|\s+--\s+", first):
        prefix = first[: match.start()].strip().rstrip(" “\"'")
        if 36 <= len(prefix) <= 90 and not _DANGLING_TAIL.search(prefix):
            prefixes.append(prefix)
    if prefixes:
        return max(prefixes, key=len)
    window = first[:80].rsplit(" ", 1)[0] if first else current
    cleaned = window.rstrip(" ,;:—-“\"'")
    while cleaned and _DANGLING_TAIL.search(cleaned):
        cleaned = cleaned.rsplit(" ", 1)[0].rstrip(" ,;:—-“\"'")
    return cleaned if len(cleaned) >= 28 else current


def organized_layers(data: dict[str, Any], collection: str) -> list[dict[str, Any]]:
    raw_commentary = str(data.get("commentary") or "")
    commentary = _strip_layer_tail(raw_commentary)
    key_text = _extract_section(
        raw_commentary, _KEY_TERMS_HEADING, (_RESONANCE_HEADING, _PRACTICE_HEADING)
    )
    res_text = _extract_section(raw_commentary, _RESONANCE_HEADING, (_PRACTICE_HEADING,))
    key_items = _parse_key_terms(key_text)
    res_items = _parse_resonances(res_text)
    existing: dict[str, dict[str, Any]] = {}
    for layer in data.get("pratibha_layers") or []:
        if isinstance(layer, dict) and layer.get("kind"):
            existing[str(layer["kind"])] = layer
    if not key_text and existing.get("key_terms"):
        key_text = str(existing["key_terms"].get("body") or "")
        key_items = list(existing["key_terms"].get("items") or []) or _parse_key_terms(key_text)
    if not res_text and existing.get("resonances"):
        res_text = str(existing["resonances"].get("body") or "")
        res_items = list(existing["resonances"].get("items") or []) or _parse_resonances(res_text)
    practice = str(data.get("practice") or data.get("abhyasa") or "").strip()
    original = str(data.get("original") or "").strip()
    translation = str(data.get("translation") or "").strip()
    if not original or not translation:
        for layer in data.get("pratibha_layers") or []:
            if not isinstance(layer, dict):
                continue
            kind = layer.get("kind")
            body = str(layer.get("body") or "").strip()
            if kind == "original" and not original:
                original = body
            elif kind == "translation" and not translation:
                translation = body

    layers: list[dict[str, Any]] = []
    if collection in ENGLISH_SOURCE:
        if original:
            layers.append({"kind": "original", "label": "Original", "body": original})
    else:
        if translation:
            trans = {"kind": "translation", "label": "Translation", "body": translation}
            prov = str(data.get("translation_provenance") or "").strip()
            if prov:
                trans["layer_provenance"] = prov
            layers.append(trans)
    if commentary:
        layers.append({"kind": "commentary", "label": "Pratibha Commentary", "body": commentary})
    if key_items or key_text:
        kt: dict[str, Any] = {"kind": "key_terms", "label": "Key Terms"}
        if key_text:
            kt["body"] = key_text
        if key_items:
            kt["items"] = key_items
        layers.append(kt)
    if res_items or res_text:
        rs: dict[str, Any] = {"kind": "resonances", "label": "Cross-Tradition Resonances"}
        if res_text:
            rs["body"] = res_text
        if res_items:
            rs["items"] = [
                {
                    "citation": item["citation"],
                    "resonance": item["resonance"],
                    "divergence": item.get("divergence") or "",
                }
                for item in res_items
            ]
        layers.append(rs)
    if practice:
        layers.append({"kind": "practice", "label": "Practice (Abhyasa)", "body": practice})
    return layers


def ordered(data: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    skip = {"enriched"}
    for key in KEY_ORDER:
        if key in data and key not in skip:
            out[key] = data[key]
    for key, value in data.items():
        if key not in out and key not in skip:
            out[key] = value
    return out


def organize_one(path: Path, collection: str) -> bool:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return False
    raw_commentary = str(data.get("commentary") or "")
    commentary = _strip_layer_tail(raw_commentary)
    if not commentary:
        return False
    layers = organized_layers(data, collection)
    original = str(data.get("original") or "").strip()
    translation = str(data.get("translation") or "").strip()
    for layer in layers:
        if layer["kind"] == "original":
            original = str(layer.get("body") or "").strip()
        elif layer["kind"] == "translation":
            translation = str(layer.get("body") or "").strip()
    source = translation or original
    title = untruncate_title(str(data.get("title") or ""), source)
    unit_label = untruncate_title(str(data.get("unit_label") or title), source)
    if collection == "eastman_soul_of_the_indian":
        title = polish_long_title(title, source)
        unit_label = polish_long_title(unit_label, source)
    practice = str(data.get("practice") or data.get("abhyasa") or "").strip()

    data["commentary"] = commentary
    data["title"] = title
    data["unit_label"] = unit_label
    data["pratibha_layers"] = layers
    data["editorial_maturity"] = "strong_draft"
    if practice:
        data["practice"] = practice
        data["abhyasa"] = practice
    if collection in ENGLISH_SOURCE:
        if original:
            data["original"] = original
        data.pop("translation", None)
    else:
        if translation:
            data["translation"] = translation
        data.pop("original", None)
    data.pop("enriched", None)

    path.write_text(
        yaml.safe_dump(ordered(data), allow_unicode=True, sort_keys=False, width=100),
        encoding="utf-8",
    )
    return True


def main() -> int:
    wrote = 0
    skipped = 0
    for collection in COLLECTIONS:
        folder = CANONICAL / collection
        if not folder.is_dir():
            print(f"missing collection dir: {folder}")
            skipped += 1
            continue
        for path in sorted(folder.glob("*.yml")):
            if path.name == "_work.yml":
                continue
            if organize_one(path, collection):
                wrote += 1
            else:
                skipped += 1
                print(f"skip: {path.relative_to(ROOT)}")
    print(f"organized {wrote}; skipped {skipped}")
    return 0 if wrote else 1


if __name__ == "__main__":
    raise SystemExit(main())
