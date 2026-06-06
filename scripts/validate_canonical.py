#!/usr/bin/env python3
"""
Validate canonical units for the two-category model.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parent.parent
CANONICAL_ROOT_DEFAULT = ROOT / "data" / "canonical"


REQ_COMMON = ["category", "work_id", "work_title", "unit_id", "unit_type"]
REQ_ROOT = ["translation_literal"]
REQ_COMMENTARY = ["thesis", "source_excerpt"]
LAYER_ORDER = ["original", "iast", "translation", "commentary", "key_terms", "resonances", "practice", "appendix"]


def load(path: Path) -> dict[str, Any] | None:
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
        y = yaml.safe_load(raw)
        return y if isinstance(y, dict) else None
    except Exception:
        return None


def nonempty(v: Any) -> bool:
    if v is None:
        return False
    if isinstance(v, list):
        return len(v) > 0
    return str(v).strip() != ""


def _norm_tokens(s: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", str(s or "").lower())


def _token_overlap(a: str, b: str) -> float:
    ta = _norm_tokens(a)
    tb = _norm_tokens(b)
    if not ta or not tb:
        return 0.0
    sa, sb = set(ta), set(tb)
    return len(sa & sb) / max(1, len(sa | sb))


def _first_sentence(s: str) -> str:
    t = str(s or "").strip()
    if not t:
        return ""
    parts = re.split(r"(?<=[.!?])\s+", t, maxsplit=1)
    return parts[0].strip() if parts else t


def validate_one(path: Path, y: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warns: list[str] = []
    for k in REQ_COMMON:
        if not nonempty(y.get(k)):
            errors.append(f"missing/empty `{k}`")

    cat = str(y.get("category") or "")
    if cat == "root_text":
        for k in REQ_ROOT:
            if not nonempty(y.get(k)):
                warns.append(f"root_text missing `{k}`")
    elif cat == "commentary_text":
        for k in REQ_COMMENTARY:
            if not nonempty(y.get(k)):
                errors.append(f"commentary_text missing `{k}`")
        if y.get("themes") is None:
            errors.append("commentary_text missing `themes`")
        elif isinstance(y.get("themes"), list) and len(y.get("themes")) == 0:
            warns.append("commentary_text has empty `themes`")
    else:
        errors.append("category must be `root_text` or `commentary_text`")

    if nonempty(y.get("sanskrit_devanagari")) and not nonempty(y.get("sanskrit_iast")):
        warns.append("has Devanagari but missing IAST")

    layers = y.get("pratibha_layers")
    if layers is not None:
        if not isinstance(layers, list):
            errors.append("`pratibha_layers` must be a list")
        else:
            seen_order = -1
            for idx, layer in enumerate(layers):
                if not isinstance(layer, dict):
                    errors.append(f"`pratibha_layers[{idx}]` must be an object")
                    continue
                kind = str(layer.get("kind") or "").strip()
                if kind not in LAYER_ORDER:
                    errors.append(f"`pratibha_layers[{idx}].kind` must be one of {', '.join(LAYER_ORDER)}")
                    continue
                order = LAYER_ORDER.index(kind)
                if order < seen_order and kind != "appendix":
                    warns.append("`pratibha_layers` are not in canonical display order")
                seen_order = max(seen_order, order)
                if not nonempty(layer.get("body")) and not nonempty(layer.get("items")):
                    warns.append(f"`pratibha_layers[{idx}]` has no body/items")

    maturity = str(y.get("editorial_maturity") or "").strip()
    if maturity and maturity not in {"publishable", "strong_draft", "needs_rewrite", "structural_draft"}:
        errors.append("`editorial_maturity` must be publishable, strong_draft, needs_rewrite, or structural_draft")

    themes = y.get("themes")
    if themes is not None and not isinstance(themes, list):
        errors.append("`themes` must be a list")
    tags = y.get("tags")
    if tags is not None and not isinstance(tags, list):
        errors.append("`tags` must be a list")
    prov = y.get("provenance")
    if prov is not None and not isinstance(prov, dict):
        errors.append("`provenance` must be an object")

    title = str(y.get("title") or "").strip()
    body = str(y.get("translation_literal") or "").strip()
    if title and body and len(_norm_tokens(title)) >= 3:
        first = _first_sentence(body)
        overlap = _token_overlap(title, first)
        if overlap >= 0.85:
            warns.append("possible title/body bleed: first body sentence near-duplicates title")

    return errors, warns


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate canonical root_text/commentary_text units.")
    ap.add_argument("--root", type=Path, default=CANONICAL_ROOT_DEFAULT)
    args = ap.parse_args()

    files = sorted([p for p in args.root.glob("**/*.yml") if p.name != "_work.yml"])
    if not files:
        print(f"No canonical files under {args.root}")
        return 1

    errors = 0
    warns = 0
    by_cat = {"root_text": 0, "commentary_text": 0}
    for fp in files:
        y = load(fp)
        if y is None:
            print(f"ERROR {fp}: unreadable/non-object yaml")
            errors += 1
            continue
        cat = str(y.get("category") or "")
        if cat in by_cat:
            by_cat[cat] += 1
        e, w = validate_one(fp, y)
        for msg in e:
            print(f"ERROR {fp}: {msg}")
        for msg in w:
            print(f"WARN  {fp}: {msg}")
        errors += len(e)
        warns += len(w)

    print(f"checked={len(files)} errors={errors} warnings={warns}")
    print(f"root_text={by_cat['root_text']} commentary_text={by_cat['commentary_text']}")
    return 0 if errors == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())

