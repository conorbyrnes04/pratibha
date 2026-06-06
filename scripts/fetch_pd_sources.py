#!/usr/bin/env python3
"""Download or refresh Project Gutenberg PD texts into data/raw_texts/pd/."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PD = ROOT / "data" / "raw_texts" / "pd"

GUTENBERG = [
    (2388, PD / "indian" / "bhagavad_gita_arnold_gutenberg_2388.txt"),
    (1658, PD / "greek" / "phaedo_jowett_gutenberg_1658.txt"),
    (216, PD / "chinese" / "tao_te_ching_legge_gutenberg_216.txt"),
    (59709, PD / "chinese" / "zhuangzi_giles_gutenberg_59709_fresh.txt"),
    (45109, PD / "greek" / "epictetus_enchiridion_gutenberg_45109.txt"),
    (10662, PD / "greek" / "epictetus_long_discourses_gutenberg_10662.txt"),
]

# Each COPIES entry MUST record its PD basis (publication year, Gutenberg ID, or archive URL)
# in a trailing comment so downstream scripts can verify copyright status before use.
COPIES = [
    # PD: Patrick (1889) — pre-1928 US publication
    (ROOT / "data" / "raw_texts" / "patrick_heraclitus_1889.txt", PD / "greek" / "heraclitus_patrick_1889.txt"),
    # PD: Giles (1889) Zhuangzi — Gutenberg #59709
    (ROOT / "data" / "raw_texts" / "ChaungTzuRaw", PD / "chinese" / "zhuangzi_giles_gutenberg_59709.txt"),
    # PD: Mackenna (1917–1930) Plotinus Enneads — pre-1928 US publication
    (ROOT / "data" / "raw_texts" / "plotinus_enneads_full.txt", PD / "greek" / "plotinus_mackenna_enneads.txt"),
    # PD: GRETIL IAST Yoga Sutras — open academic text, no translation copyright claim
    (ROOT / "data" / "raw_texts" / "yoga_sutras_gretil_iast.txt", PD / "indian" / "yoga_sutras_gretil_iast_sanskrit.txt"),
]


def _fetch(gutenberg_id: int, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = f"https://www.gutenberg.org/cache/epub/{gutenberg_id}/pg{gutenberg_id}.txt"
    subprocess.run(["curl", "-fsSL", url, "-o", str(dest)], check=True)
    print(f"  fetched #{gutenberg_id} -> {dest.relative_to(ROOT)}")


def main() -> int:
    print("Copying local PD files...")
    for src, dest in COPIES:
        if not src.exists():
            print(f"  skip missing {src.relative_to(ROOT)}")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(src.read_bytes())
        print(f"  copied -> {dest.relative_to(ROOT)}")

    print("Fetching Gutenberg texts...")
    for gid, dest in GUTENBERG:
        try:
            _fetch(gid, dest)
        except subprocess.CalledProcessError as e:
            print(f"  FAIL #{gid}: {e}", file=sys.stderr)

    print(f"Done. See {PD / 'manifest.yml'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
