"""Slim Library catalog — live YAML or a Docker-baked JSON snapshot.

The snapshot lets /verses answer while the full corpus is still loading
after a Render wake. Once YAML is in memory, live data takes over.
"""
from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any

from . import tts as listen_tts
from .data_loader import corpus_ready, filter_by_maturity, get_all_verses

logger = logging.getLogger("pratibha.catalog")

_SLIM_PREVIEW_CHARS = 280
_CATALOG_MEMO_TTL = 60.0
_ROOT = Path(__file__).resolve().parent.parent
_BAKE_DIR = _ROOT / "data" / "catalog"
_catalog_memo: dict[str, tuple[float, list[dict[str, Any]]]] = {}
_baked_memo: dict[str, list[dict[str, Any]]] = {}


def text_preview(value: Any, limit: int = _SLIM_PREVIEW_CHARS) -> str | None:
    if not isinstance(value, str):
        return None
    text = " ".join(value.split())
    if not text:
        return None
    if len(text) <= limit:
        return text
    clipped = text[:limit].rsplit(" ", 1)[0].rstrip(".,;:—-")
    return (clipped or text[:limit]).rstrip() + "…"


def _layer_or_field(v: dict[str, Any], kind: str) -> Any:
    field = v.get(kind)
    if isinstance(field, str) and field.strip():
        return field
    if kind == "practice":
        abhyasa = v.get("abhyasa")
        if isinstance(abhyasa, str) and abhyasa.strip():
            return abhyasa
    layers = v.get("pratibha_layers")
    if not isinstance(layers, list):
        return None
    for layer in layers:
        if isinstance(layer, dict) and str(layer.get("kind") or "") == kind:
            return layer.get("body")
    return None


def verse_list_item(v: dict[str, Any]) -> dict[str, Any]:
    """Index card only — previews, not full layers. Folio still uses /verse/{id}."""
    out: dict[str, Any] = {"_id": v.get("_id")}
    for key in (
        "collection",
        "section",
        "title",
        "sutra_id",
        "reference",
        "sequence",
        "work_id",
        "editorial_maturity",
        "editorial_score",
    ):
        value = v.get(key)
        if value is not None and value != "":
            out[key] = value
    themes = [theme for theme in (v.get("themes") or []) if str(theme).strip()]
    if themes:
        out["themes"] = themes
    translation = text_preview(_layer_or_field(v, "translation"))
    commentary = text_preview(_layer_or_field(v, "commentary"))
    practice = text_preview(_layer_or_field(v, "practice"))
    if translation:
        out["translation"] = translation
    if commentary:
        out["commentary"] = commentary
    if practice:
        out["practice"] = practice
    sections = listen_tts.archived_sections(v)
    if sections:
        out["listen_sections"] = sections
    return out


def _bake_name(min_maturity: str | None) -> str:
    return "strong_draft" if min_maturity == "strong_draft" else "all"


def bake_path(min_maturity: str | None) -> Path:
    return _BAKE_DIR / f"verses_{_bake_name(min_maturity)}.json"


def build_catalog(min_maturity: str | None) -> list[dict[str, Any]]:
    return [verse_list_item(v) for v in filter_by_maturity(get_all_verses(), min_maturity)]


def write_baked_catalog(min_maturity: str | None, items: list[dict[str, Any]] | None = None) -> Path:
    rows = items if items is not None else build_catalog(min_maturity)
    path = bake_path(min_maturity)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return path


def load_baked_catalog(min_maturity: str | None) -> list[dict[str, Any]] | None:
    key = _bake_name(min_maturity)
    cached = _baked_memo.get(key)
    if cached is not None:
        return cached
    path = bake_path(min_maturity)
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        logger.warning("Baked catalog unreadable: %s", path, exc_info=True)
        return None
    if not isinstance(data, list):
        return None
    _baked_memo[key] = data
    return data


def catalog_items(min_maturity: str | None) -> list[dict[str, Any]]:
    key = min_maturity or ""
    if corpus_ready():
        now = time.monotonic()
        hit = _catalog_memo.get(key)
        if hit and now - hit[0] < _CATALOG_MEMO_TTL:
            return hit[1]
        items = build_catalog(min_maturity)
        _catalog_memo[key] = (now, items)
        return items
    baked = load_baked_catalog(min_maturity)
    if baked is not None:
        return baked
    items = build_catalog(min_maturity)
    _catalog_memo[key] = (time.monotonic(), items)
    return items


def warm_catalog() -> None:
    for key in (None, "strong_draft"):
        catalog_items(key)
