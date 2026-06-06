#!/usr/bin/env python3
"""Replace copyrighted anchor English with public-domain translations in YAML units.

Usage:
  python scripts/swap_pd_anchors.py heraclitus [--min-score 0.12]
  python scripts/swap_pd_anchors.py chuang-tzu
  python scripts/swap_pd_anchors.py all
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from pd_anchor_sources import (  # noqa: E402
    load_giles_chuang_tzu,
    load_patrick_text,
    parse_giles_chuang_tzu,
    parse_patrick_heraclitus,
    patrick_for_corpus_number,
)


def title_from_text(text: str, fallback: str) -> str:
    s = re.sub(r"\s+", " ", text).strip()
    if not s:
        return fallback
    parts = re.split(r"(?<=[.!?])\s+", s)
    first = parts[0].strip()
    if len(first) > 92:
        return first[:89].rstrip() + "..."
    return first or fallback


def swap_heraclitus(min_score: float) -> int:
    patrick = parse_patrick_heraclitus(load_patrick_text())
    frag_dir = ROOT / "data" / "yaml" / "fragments"
    updated = 0
    skipped = 0

    for path in sorted(frag_dir.glob("fragment_*.yml")):
        m = re.search(r"fragment_(\d+)\.yml$", path.name)
        corpus_n = int(m.group(1)) if m else 0
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        old = str(data.get("translation") or "").strip()
        if not old:
            continue
        n, new_text, score = patrick_for_corpus_number(corpus_n, patrick, old)
        if not new_text or score < min_score:
            skipped += 1
            print(f"  skip {path.name}: best Patrick #{n} score={score:.2f}")
            continue
        data["translation"] = new_text
        data["title"] = title_from_text(new_text, data.get("title") or path.stem)
        path.write_text(
            yaml.safe_dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )
        updated += 1

    print(f"Heraclitus: updated {updated} fragments ({skipped} skipped, {len(patrick)} Patrick units parsed)")
    return updated


def swap_chuang_tzu() -> int:
    chapters = parse_giles_chuang_tzu(load_giles_chuang_tzu())
    ch_dir = ROOT / "data" / "yaml" / "the_book_of_chuang_tzu"
    updated = 0
    missing = 0

    for path in sorted(ch_dir.glob("ch_*.yml")):
        m = re.search(r"ch_(\d+)\.yml$", path.name)
        if not m:
            continue
        n = int(m.group(1))
        giles = chapters.get(n)
        if not giles:
            missing += 1
            print(f"  skip {path.name}: no Giles chapter {n}")
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["title"] = giles["title"]
        data["translation"] = giles["excerpt"]
        data["commentary"] = giles["body"]
        path.write_text(
            yaml.safe_dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120),
            encoding="utf-8",
        )
        updated += 1

    print(f"Chuang Tzu: updated {updated} chapter YAML files ({missing} missing Giles chapters, {len(chapters)} parsed)")
    return updated


def recanonicalize(collections: list[str]) -> None:
    py = sys.executable
    subprocess.run([py, str(ROOT / "scripts" / "canonicalize_texts.py")], check=True)
    for coll in collections:
        slug_map = {
            "heraclitus": "heraclitus_fragments",
            "chuang_tzu": "the_book_of_chuang_tzu",
        }
        slug = slug_map.get(coll)
        if slug:
            out = ROOT / "data" / "canonical" / slug
            if out.exists():
                print(f"Re-canonicalized {out.relative_to(ROOT)}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Swap anchor YAML to public-domain translations.")
    ap.add_argument("target", choices=["heraclitus", "chuang-tzu", "all"])
    ap.add_argument("--min-score", type=float, default=0.12, help="Min fuzzy match score for Heraclitus")
    ap.add_argument("--no-canonicalize", action="store_true")
    args = ap.parse_args()

    touched: list[str] = []
    if args.target in ("heraclitus", "all"):
        if swap_heraclitus(args.min_score):
            touched.append("heraclitus")
    if args.target in ("chuang-tzu", "all"):
        if swap_chuang_tzu():
            touched.append("chuang_tzu")

    if touched and not args.no_canonicalize:
        recanonicalize(touched)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
