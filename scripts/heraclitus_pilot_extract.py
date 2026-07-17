#!/usr/bin/env python3
"""Extract pilot Heraclitus fragments from Patrick (1889) PD text.

Reads data/raw_texts/heraclitus_pilot/manifest.json and writes one .txt per unit
under data/raw_texts/heraclitus_pilot/.

Usage:
  python scripts/heraclitus_pilot_extract.py
  python scripts/heraclitus_pilot_extract.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from pd_anchor_sources import load_patrick_text, parse_patrick_heraclitus  # noqa: E402

MANIFEST = ROOT / "data" / "raw_texts" / "heraclitus_pilot" / "manifest.json"
OUT_DIR = ROOT / "data" / "raw_texts" / "heraclitus_pilot"

# Manual overrides when Patrick OCR / parser yields a truncated or noisy chunk.
# Text must match Patrick (1889) PD; these are cleaned excerpts from the archive file.
CLEAN_ANCHORS: dict[str, str] = {
    "HFR_P030": (
        "This world, the same for all, neither any of the gods nor any man has made; "
        "but it always was, and is, and shall be, an ever living fire, "
        "kindled in due measure, and in due measure extinguished."
    ),
    "HFR_P041": (
        "Into the same river you could not step twice, for other and still other waters are flowing. "
        "To those who step into the same rivers, other and still other waters flow."
    ),
    "HFR_P090": (
        "Into the same river we both step and do not step. We both are and are not."
    ),
    "HFR_P066": (
        "The name of the bow is life, but its work is death."
    ),
    "HFR_P074": "The dry soul is the wisest and best.",
}


def _clean_patrick(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"[‘’]", "'", s)
    s = re.sub(r"\s*[+{};]+\s*$", "", s)
    return s


def anchor_for_entry(entry: dict, patrick: dict[int, str]) -> str:
    sid = entry["sutra_id"]
    if sid in CLEAN_ANCHORS:
        return CLEAN_ANCHORS[sid]
    n = int(entry["patrick_frag"])
    raw = patrick.get(n)
    if not raw:
        raise ValueError(f"No Patrick fragment {n} for {sid}")
    return _clean_patrick(raw)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    patrick = parse_patrick_heraclitus(load_patrick_text())

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    for entry in manifest:
        sid = entry["sutra_id"]
        slug = entry["slug"]
        text = anchor_for_entry(entry, patrick)
        out = OUT_DIR / f"{slug}.txt"
        if args.dry_run:
            print(f"  {sid} -> {out.name} ({len(text)} chars)")
            continue
        out.write_text(text + "\n", encoding="utf-8")
        written += 1
        print(f"Wrote {out.relative_to(ROOT)} ({len(text)} chars)")

    if not args.dry_run:
        print(f"\nExtracted {written} pilot fragments to {OUT_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
