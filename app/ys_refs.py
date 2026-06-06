"""Patañjali Yoga Sūtras reference extraction for API responses."""

from __future__ import annotations

import re
from typing import Any

_PATANJALI_MARKERS = ("patanjali", "patañjali", "yoga_sūtras", "yoga_sutras")
_REF_FROM_SOURCE = re.compile(r"Yoga S[uū]tras\s+(\d+)\.(\d+)", re.I)
_REF_FROM_ID = re.compile(r"ys[_\.\s](\d+)[_\.\s](\d+)", re.I)
_REF_FROM_SUTRA_ID = re.compile(r"YS_(\d+)_(\d+)", re.I)
_REF_PLAIN = re.compile(r"^(\d+)\.(\d+)")


def is_patanjali_yoga_sutras(item: dict[str, Any]) -> bool:
    blob = " ".join(
        str(item.get(key) or "")
        for key in ("work_id", "collection", "_id", "unit_id", "source_file")
    ).lower()
    if not any(marker in blob for marker in _PATANJALI_MARKERS):
        return False
    return "yoga" in blob or "sutra" in blob or "sūtra" in blob


def parse_pada_num(item: dict[str, Any]) -> tuple[int, int] | None:
    ref = str(item.get("reference") or "").strip()
    match = _REF_PLAIN.match(ref)
    if match:
        return int(match.group(1)), int(match.group(2))

    for key in ("source_reference",):
        text = str(item.get(key) or "")
        match = _REF_FROM_SOURCE.search(text)
        if match:
            return int(match.group(1)), int(match.group(2))

    provenance = item.get("provenance")
    if isinstance(provenance, dict):
        text = str(provenance.get("source_reference") or "")
        match = _REF_FROM_SOURCE.search(text)
        if match:
            return int(match.group(1)), int(match.group(2))

    for key in ("sutra_id", "source_id", "unit_id", "_id"):
        text = str(item.get(key) or "")
        for pattern in (_REF_FROM_SUTRA_ID, _REF_FROM_ID):
            match = pattern.search(text)
            if match:
                return int(match.group(1)), int(match.group(2))

    return None


def enrich_patanjali_unit(out: dict[str, Any]) -> dict[str, Any]:
    if not is_patanjali_yoga_sutras(out):
        return out

    parsed = parse_pada_num(out)
    if parsed:
        pada, num = parsed
        out["reference"] = f"{pada}.{num}"
        out["sequence"] = pada * 100 + num

    provenance = out.get("provenance")
    if isinstance(provenance, dict) and provenance.get("section"):
        if str(out.get("section") or "").strip().lower() in ("", "sutra"):
            out["section"] = str(provenance["section"])

    return out
