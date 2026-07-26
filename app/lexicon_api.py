"""Lexicon API helpers: cache, search, passage lookup.

Prefers ``load_lexicon`` from ``app.lexicon_schema`` (Agent A). Falls back to a
compatible interim YAML loader if that module is unavailable. Missing on-disk
lexicon data yields an empty cache so the API stays up.
"""

from __future__ import annotations

import logging
import os
import threading
import unicodedata
from pathlib import Path
from typing import Any, Callable

import yaml

from .data_loader import get_all_verses

logger = logging.getLogger("pratibha.lexicon_api")

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_LEXICON_ROOT = ROOT / "data" / "lexicon"

try:
    from .lexicon_schema import load_lexicon as _schema_load_lexicon

    _USING_SCHEMA_LOADER = True
except ImportError:  # pragma: no cover - Agent A module not yet present
    _schema_load_lexicon = None  # type: ignore[assignment]
    _USING_SCHEMA_LOADER = False

_load_lock = threading.Lock()
_cached: dict[str, Any] | None = None


def fold_text(value: str) -> str:
    """Casefold + strip combining marks for diacritic-insensitive search."""
    if not value:
        return ""
    decomposed = unicodedata.normalize("NFKD", str(value))
    stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return stripped.casefold()


def _read_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _interim_load_lexicon(root: Path | str | None = None) -> dict[str, Any]:
    """Compatible interim loader when ``lexicon_schema`` is unavailable."""
    lex_root = Path(root) if root is not None else DEFAULT_LEXICON_ROOT
    lemmas_dir = lex_root / "lemmas"
    if not lemmas_dir.is_dir():
        return {
            "root": str(lex_root),
            "index": [],
            "lemmas": {},
            "errors": [f"lexicon lemmas directory not found: {lemmas_dir}"],
        }

    lemmas: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    paths = sorted(lemmas_dir.glob("*.yml")) + sorted(lemmas_dir.glob("*.yaml"))
    for path in paths:
        try:
            data = _read_yaml(path)
        except Exception as exc:
            errors.append(f"{path.name}: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{path.name}: not a mapping")
            continue
        lid = str(data.get("id") or path.stem).strip().lower()
        if not lid:
            errors.append(f"{path.name}: missing id")
            continue
        if path.stem != lid:
            errors.append(f"{path.name}: stem {path.stem!r} != id {lid!r}")
            continue
        if lid in lemmas:
            errors.append(f"duplicate lemma id {lid!r}")
            continue
        senses = data.get("senses") if isinstance(data.get("senses"), list) else []
        lemmas[lid] = {
            "id": lid,
            "maturity": str(data.get("maturity") or "structural_draft"),
            "scripts": data.get("scripts") if isinstance(data.get("scripts"), dict) else {},
            "aliases": list(data.get("aliases") or []) if isinstance(data.get("aliases"), list) else [],
            "traditions": [
                str(t).strip().lower().replace(" ", "_")
                for t in (data.get("traditions") or [])
                if str(t).strip()
            ],
            "related": list(data.get("related") or []) if isinstance(data.get("related"), list) else [],
            "senses": [s for s in senses if isinstance(s, dict)],
        }

    index: list[dict[str, Any]] = []
    index_path = lex_root / "index.yml"
    if index_path.is_file():
        try:
            raw = _read_yaml(index_path) or {}
            if isinstance(raw, dict) and isinstance(raw.get("lemmas"), list):
                for item in raw["lemmas"]:
                    if not isinstance(item, dict):
                        continue
                    iid = str(item.get("id") or "").strip().lower()
                    if iid and iid in lemmas:
                        index.append(
                            {
                                "id": iid,
                                "short": str(item.get("short") or ""),
                                "traditions": [
                                    str(t).strip().lower().replace(" ", "_")
                                    for t in (item.get("traditions") or [])
                                    if str(t).strip()
                                ],
                            }
                        )
        except Exception as exc:
            errors.append(f"index.yml: {exc}")

    if not index:
        index = [
            {
                "id": lid,
                "short": (lemmas[lid]["senses"][0].get("short") or "") if lemmas[lid]["senses"] else "",
                "traditions": list(lemmas[lid].get("traditions") or []),
            }
            for lid in sorted(lemmas)
        ]

    return {
        "root": str(lex_root),
        "index": index,
        "lemmas": lemmas,
        "errors": errors,
    }


def _empty_payload(root: Path | str, errors: list[str] | None = None) -> dict[str, Any]:
    return {
        "root": str(root),
        "index": [],
        "lemmas": {},
        "errors": list(errors or []),
    }


def _call_loader(root: Path | str | None = None) -> dict[str, Any]:
    lex_root = Path(root) if root is not None else DEFAULT_LEXICON_ROOT
    loader: Callable[[Path | str | None], dict[str, Any]] | None
    if _USING_SCHEMA_LOADER and _schema_load_lexicon is not None:
        loader = _schema_load_lexicon
    else:
        loader = _interim_load_lexicon

    try:
        payload = loader(lex_root if root is not None else None)
    except FileNotFoundError as exc:
        logger.info("Lexicon not on disk yet: %s", exc)
        return _empty_payload(lex_root, [str(exc)])
    except Exception as exc:
        # Schema loader is strict (index mismatch, validation). Soften for API.
        logger.warning("load_lexicon failed (%s); falling back to interim: %s", type(exc).__name__, exc)
        if loader is not _interim_load_lexicon:
            try:
                return _interim_load_lexicon(lex_root)
            except Exception as inner:
                logger.exception("Interim lexicon load failed")
                return _empty_payload(lex_root, [str(exc), str(inner)])
        return _empty_payload(lex_root, [str(exc)])

    if not isinstance(payload, dict):
        return _empty_payload(lex_root, ["load_lexicon returned non-dict"])
    payload.setdefault("index", [])
    payload.setdefault("lemmas", {})
    payload.setdefault("errors", [])
    payload.setdefault("root", str(lex_root))
    return payload


def _lemmas_on_disk() -> bool:
    lemmas_dir = DEFAULT_LEXICON_ROOT / "lemmas"
    if not lemmas_dir.is_dir():
        return False
    return any(lemmas_dir.glob("*.yml")) or any(lemmas_dir.glob("*.yaml"))


def get_lexicon(force_reload: bool = False) -> dict[str, Any]:
    """Cached lexicon payload (index + lemmas dicts)."""
    global _cached
    if _cached is not None and not force_reload:
        # Allow a late-arriving data/lexicon/ (e.g. seeded after startup) to load.
        if (_cached.get("lemmas") or {}) or not _lemmas_on_disk():
            return _cached
        force_reload = True
    with _load_lock:
        if _cached is not None and not force_reload:
            if (_cached.get("lemmas") or {}) or not _lemmas_on_disk():
                return _cached
        _cached = _call_loader()
        n = len(_cached.get("lemmas") or {})
        logger.info(
            "Lexicon loaded: %d lemmas (schema_loader=%s)",
            n,
            _USING_SCHEMA_LOADER,
        )
        return _cached


def clear_lexicon_cache() -> None:
    """Test helper."""
    global _cached
    with _load_lock:
        _cached = None


def _lemma_short(lemma: dict[str, Any], index_by_id: dict[str, dict[str, Any]]) -> str:
    idx = index_by_id.get(str(lemma.get("id") or ""))
    if idx and idx.get("short"):
        return str(idx["short"])
    senses = lemma.get("senses") or []
    if isinstance(senses, list) and senses and isinstance(senses[0], dict):
        return str(senses[0].get("short") or "")
    return ""


def lemma_list_item(
    lemma: dict[str, Any],
    index_by_id: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    index_by_id = index_by_id or {}
    return {
        "id": str(lemma.get("id") or ""),
        "short": _lemma_short(lemma, index_by_id),
        "traditions": list(lemma.get("traditions") or []),
        "scripts": dict(lemma.get("scripts") or {}) if isinstance(lemma.get("scripts"), dict) else {},
        "maturity": str(lemma.get("maturity") or ""),
        "aliases": list(lemma.get("aliases") or []) if isinstance(lemma.get("aliases"), list) else [],
    }


def _search_haystack(lemma: dict[str, Any]) -> str:
    parts: list[str] = [str(lemma.get("id") or "")]
    aliases = lemma.get("aliases") or []
    if isinstance(aliases, list):
        parts.extend(str(a) for a in aliases)
    scripts = lemma.get("scripts") or {}
    if isinstance(scripts, dict):
        parts.extend(str(v) for v in scripts.values() if v)
    for sense in lemma.get("senses") or []:
        if not isinstance(sense, dict):
            continue
        parts.append(str(sense.get("label") or ""))
        parts.append(str(sense.get("short") or ""))
    return " ".join(fold_text(p) for p in parts if p)


def list_lemmas(
    q: str | None = None,
    tradition: str | None = None,
    limit: int = 100,
) -> dict[str, Any]:
    payload = get_lexicon()
    lemmas: dict[str, dict[str, Any]] = payload.get("lemmas") or {}
    index_list: list[dict[str, Any]] = payload.get("index") or []
    index_by_id = {str(item.get("id")): item for item in index_list if item.get("id")}

    # Prefer index order when available; append any lemmas missing from index.
    ordered_ids = [str(item["id"]) for item in index_list if item.get("id") in lemmas]
    seen = set(ordered_ids)
    for lid in sorted(lemmas):
        if lid not in seen:
            ordered_ids.append(lid)

    needle = fold_text(q or "")
    trad = fold_text(tradition or "").replace(" ", "_")

    matched: list[dict[str, Any]] = []
    for lid in ordered_ids:
        lemma = lemmas[lid]
        if trad:
            traditions = [fold_text(str(t)).replace(" ", "_") for t in (lemma.get("traditions") or [])]
            if trad not in traditions:
                continue
        if needle and needle not in _search_haystack(lemma):
            continue
        matched.append(lemma_list_item(lemma, index_by_id))

    total = len(matched)
    lim = max(0, int(limit))
    return {"items": matched[:lim], "total": total}


def get_lemma(lemma_id: str) -> dict[str, Any] | None:
    lid = (lemma_id or "").strip().lower()
    if not lid:
        return None
    lemmas = get_lexicon().get("lemmas") or {}
    lemma = lemmas.get(lid)
    return dict(lemma) if isinstance(lemma, dict) else None


def _lemma_match_terms(lemma: dict[str, Any]) -> set[str]:
    terms = {fold_text(str(lemma.get("id") or ""))}
    for alias in lemma.get("aliases") or []:
        folded = fold_text(str(alias))
        if folded:
            terms.add(folded)
    scripts = lemma.get("scripts") or {}
    if isinstance(scripts, dict):
        for val in scripts.values():
            folded = fold_text(str(val))
            if folded:
                terms.add(folded)
    for sense in lemma.get("senses") or []:
        if isinstance(sense, dict):
            for key in ("label", "short"):
                folded = fold_text(str(sense.get(key) or ""))
                if folded:
                    terms.add(folded)
    return {t for t in terms if t}


def _iter_key_term_items(verse: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    layers = verse.get("pratibha_layers")
    if isinstance(layers, list):
        for layer in layers:
            if not isinstance(layer, dict) or layer.get("kind") != "key_terms":
                continue
            layer_items = layer.get("items") or []
            if isinstance(layer_items, list):
                items.extend(x for x in layer_items if isinstance(x, dict))
    # Legacy flat glossary / key_terms fields.
    for key in ("glossary", "key_terms"):
        raw = verse.get(key)
        if isinstance(raw, list):
            items.extend(x for x in raw if isinstance(x, dict))
    return items


def find_lemma_passages(lemma_id: str, limit: int = 30) -> list[dict[str, Any]]:
    """Scan corpus key_terms for lemma_id pointers or term/alias hits."""
    lemma = get_lemma(lemma_id)
    if not lemma:
        return []
    match_terms = _lemma_match_terms(lemma)
    lid = str(lemma.get("id") or "").strip().lower()
    cap = max(0, min(int(limit), 30))
    out: list[dict[str, Any]] = []

    for verse in get_all_verses():
        if len(out) >= cap:
            break
        for item in _iter_key_term_items(verse):
            item_lemma = str(item.get("lemma_id") or "").strip().lower()
            term = str(item.get("term") or item.get("word") or "").strip()
            definition = str(item.get("definition") or item.get("meaning") or "").strip()
            hit = False
            if item_lemma and item_lemma == lid:
                hit = True
            elif term and fold_text(term) in match_terms:
                hit = True
            if not hit:
                continue
            out.append(
                {
                    "id": str(verse.get("_id") or ""),
                    "title": str(verse.get("title") or ""),
                    "collection": str(verse.get("collection") or ""),
                    "term": term,
                    "definition": definition,
                }
            )
            if len(out) >= cap:
                break
    return out
