#!/usr/bin/env python3
"""Pratibha corpus coverage audit (READ-ONLY).

Tabulates units-per-work and theme distribution across the whole corpus by
reading data/canonical/index.jsonl (one JSON unit per line).

Usage:
    python scripts/audit/coverage.py
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "data" / "canonical" / "index.jsonl"


def load_units() -> list[dict]:
    units: list[dict] = []
    with INDEX.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            units.append(json.loads(line))
    return units


def main() -> None:
    units = load_units()
    total = len(units)

    by_work: Counter[str] = Counter()
    by_collection: Counter[str] = Counter()
    theme_counts: Counter[str] = Counter()
    themes_per_work: dict[str, Counter] = {}

    for u in units:
        wid = u.get("work_id") or "(none)"
        by_work[wid] += 1
        coll = ((u.get("provenance") or {}).get("collection")) or "(none)"
        by_collection[coll] += 1
        wt = themes_per_work.setdefault(wid, Counter())
        for t in (u.get("themes") or []):
            theme_counts[t] += 1
            wt[t] += 1

    print(f"TOTAL UNITS: {total}")
    print(f"DISTINCT WORKS: {len(by_work)}")
    print(f"DISTINCT THEMES: {len(theme_counts)}\n")

    print("=== UNITS PER WORK (desc) ===")
    for wid, n in by_work.most_common():
        print(f"{n:5d}  {wid}")

    print("\n=== TOP 30 THEMES (corpus-wide) ===")
    for t, n in theme_counts.most_common(30):
        print(f"{n:5d}  {t}")

    print("\n=== THINNEST THEMES (count <= 3) ===")
    thin = [(t, n) for t, n in theme_counts.items() if n <= 3]
    for t, n in sorted(thin, key=lambda x: (x[1], x[0])):
        print(f"{n:5d}  {t}")


if __name__ == "__main__":
    main()
