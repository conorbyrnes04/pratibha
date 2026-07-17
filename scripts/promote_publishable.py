#!/usr/bin/env python3
"""Promote already-authored units in target collections to `publishable`.

Several high-traffic collections (Tao Te Ching, Heraclitus, Patanjali, Astavakra)
are fully authored — translation + substantial commentary + a concrete practice —
but carry an explicit `editorial_maturity: strong_draft` in their YAML, which the
loader honors first. This script re-stamps units that pass a quality gate to
`publishable`, editing only the maturity line so diffs stay minimal.

Units that fail the gate are left untouched (deferred), so promotion never
surfaces a half-finished unit. Dry-run by default; pass --write to apply.

    python scripts/promote_publishable.py                 # dry run, all targets
    python scripts/promote_publishable.py --write         # apply
    python scripts/promote_publishable.py --collection tao_te_ching --write
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.data_loader import _commentary_is_authored, _practice_is_generic  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directory names under data/canonical/ to promote.
TARGET_DIRS = [
    "tao_te_ching",
    "heraclitus_fragments",
    "patañjali_yoga_sūtras",
    "astavakra_gita",
]

_MATURITY_LINE = re.compile(r"^(editorial_maturity:).*$", re.M)


def _translation_text(item: dict) -> str:
    for key in ("translation", "translation_literal"):
        v = item.get(key)
        if isinstance(v, str) and v.strip():
            return v.strip()
    layers = item.get("pratibha_layers")
    if isinstance(layers, list):
        for layer in layers:
            if isinstance(layer, dict) and str(layer.get("kind")) == "translation":
                body = str(layer.get("body") or "").strip()
                if body:
                    return body
    return ""


def _practice_text(item: dict) -> str:
    for key in ("abhyasa", "practice"):
        v = item.get(key)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def passes_gate(item: dict) -> tuple[bool, str]:
    """Publishable bar: real translation + authored commentary + a concrete practice."""
    if not _translation_text(item):
        return False, "no translation"
    commentary = str(item.get("commentary") or "")
    if not _commentary_is_authored(commentary):
        return False, "commentary not authored"
    practice = _practice_text(item)
    if not practice or _practice_is_generic(practice):
        return False, "practice missing/generic"
    return True, "ok"


def promote_file(path: str, write: bool) -> str:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    item = yaml.safe_load(text)
    if not isinstance(item, dict):
        return "skip: not a mapping"
    current = str(item.get("editorial_maturity") or "").strip().lower()
    if current == "publishable":
        return "already publishable"
    ok, reason = passes_gate(item)
    if not ok:
        return f"deferred ({reason})"
    if not write:
        return "would promote"
    if _MATURITY_LINE.search(text):
        new_text = _MATURITY_LINE.sub("editorial_maturity: publishable", text, count=1)
    else:
        new_text = text.rstrip() + "\neditorial_maturity: publishable\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)
    return "promoted"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="apply changes (default: dry run)")
    ap.add_argument("--collection", help="limit to one target dir")
    args = ap.parse_args()

    dirs = [args.collection] if args.collection else TARGET_DIRS
    totals: dict[str, int] = {}
    for d in dirs:
        files = sorted(glob.glob(os.path.join(ROOT, "data", "canonical", d, "**", "*.yml"), recursive=True))
        counts: dict[str, int] = {}
        for path in files:
            result = promote_file(path, args.write)
            key = result.split(" (")[0]
            counts[key] = counts.get(key, 0) + 1
            totals[key] = totals.get(key, 0) + 1
        summary = ", ".join(f"{k}={v}" for k, v in sorted(counts.items()))
        print(f"{d:26s} files={len(files):4d}  {summary}")
    print("-" * 60)
    print("TOTAL:", ", ".join(f"{k}={v}" for k, v in sorted(totals.items())))
    if not args.write:
        print("\n(dry run — re-run with --write to apply)")


if __name__ == "__main__":
    main()
