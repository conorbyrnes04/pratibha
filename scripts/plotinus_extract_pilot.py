#!/usr/bin/env python3
"""Extract pilot Plotinus tractates from MacKenna PD sources.

Pilot tractates (resonance-log priority):
  - I.6  On Beauty          (MIT/PD text)
  - V.1  Three Hypostases   (MIT/PD text)
  - VI.9 On the Good        (Delphi epub — MIT archive is truncated at V.3)

Writes section-delimited text files under data/raw_texts/plotinus_pilot/
and a manifest JSON for the authoring pipeline.

Usage:
  python scripts/plotinus_extract_pilot.py
  python scripts/plotinus_extract_pilot.py --include I.1
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.enneads_mit_to_yaml import parse as parse_mit  # noqa: E402

MIT_SOURCE = ROOT / "data" / "raw_texts" / "pd" / "greek" / "plotinus_mackenna_enneads.txt"
EPUB_SOURCE = ROOT / "data" / "raw_texts" / "Complete Works of Plotinus_ Complete Enneads.epub"
OUT_DIR = ROOT / "data" / "raw_texts" / "plotinus_pilot"

PILOT_TRACTATES = [
    ("I", 6, "Beauty"),
    ("V", 1, "The Three Initial Hypostases"),
    ("VI", 9, "On the Good, or the One"),
]

OPTIONAL = [("I", 1, "The Animate and the Man")]


def _slug(ennead: str, tractate: int) -> str:
    return f"enn_{ennead.lower()}_{tractate}"


def _section_file(ennead: str, tractate: int, section: int) -> str:
    return f"{_slug(ennead, tractate)}_s{section:02d}.txt"


def _write_section(path: Path, body: str) -> None:
    path.write_text(body.strip() + "\n", encoding="utf-8")


def _extract_mit(ennead: str, tractate: int, units: list[dict]) -> list[dict]:
    rows = [
        u
        for u in units
        if u["ennead"] == ennead and u["tractate"] == tractate
    ]
    rows.sort(key=lambda u: u["section"])
    return rows


def _html_to_text(data: str) -> str:
    data = re.sub(r"<script[^>]*>.*?</script>", "", data, flags=re.S | re.I)
    data = re.sub(r"<style[^>]*>.*?</style>", "", data, flags=re.S | re.I)
    data = re.sub(r"<br\s*/?>", "\n", data, flags=re.I)
    data = re.sub(r"</p>", "\n\n", data, flags=re.I)
    data = re.sub(r"<[^>]+>", "", data)
    data = html.unescape(data)
    return re.sub(r"\n{3,}", "\n\n", data).strip()


def _extract_vi9_from_epub(epub_path: Path) -> list[dict]:
    """Parse Ennead VI.9 from the Delphi epub (Ops/195.html)."""
    with zipfile.ZipFile(epub_path) as z:
        raw = z.read("Ops/195.html").decode("utf-8", errors="replace")
    text = _html_to_text(raw)

    # Drop Greek scholia header; English sections follow numbered markers.
    marker = re.search(r"(?m)^1\.\s+It is in virtue of unity", text)
    if marker:
        text = text[marker.start() :]

    parts = re.split(r"(?m)^(\d+)\.\s+", text)
    rows: list[dict] = []
    for i in range(1, len(parts), 2):
        num = int(parts[i])
        body = parts[i + 1].strip()
        # Stop if we hit bibliography / index noise.
        if re.match(r"(?i)^(contents|index|bibliography)\b", body):
            break
        if len(body) < 80:
            continue
        rows.append(
            {
                "ennead": "VI",
                "tractate": 9,
                "title": "On the Good, or the One",
                "section": num,
                "body": body,
            }
        )
    return rows


def build_manifest(include_i1: bool = False) -> list[dict]:
    if not MIT_SOURCE.exists():
        raise FileNotFoundError(f"MIT source missing: {MIT_SOURCE}")

    mit_units = parse_mit(MIT_SOURCE.read_text(encoding="utf-8", errors="replace"))
    manifest: list[dict] = []

    targets = list(PILOT_TRACTATES)
    if include_i1:
        targets = [OPTIONAL[0], *targets]

    for ennead, tractate, title in targets:
        if ennead == "VI":
            if not EPUB_SOURCE.exists():
                print(f"  WARN: epub missing, skipping {ennead}.{tractate}")
                continue
            rows = _extract_vi9_from_epub(EPUB_SOURCE)
        else:
            rows = _extract_mit(ennead, tractate, mit_units)
            if rows and not rows[0].get("title"):
                rows[0]["title"] = title

        if not rows:
            print(f"  WARN: no sections for Ennead {ennead}.{tractate}")
            continue

        tractate_title = rows[0].get("title") or title
        for row in rows:
            sec = int(row["section"])
            fname = _section_file(ennead, tractate, sec)
            fpath = OUT_DIR / fname
            _write_section(fpath, row["body"])
            manifest.append(
                {
                    "ennead": ennead,
                    "tractate": tractate,
                    "tractate_title": tractate_title,
                    "section": sec,
                    "sutra_id": f"ENN_{ennead}_{tractate}_{sec:02d}",
                    "file": str(fpath.relative_to(ROOT)),
                    "anchor_source": (
                        "Delphi epub (MacKenna & Page)"
                        if ennead == "VI"
                        else "MIT Classics (MacKenna & Page)"
                    ),
                }
            )
        print(f"  Ennead {ennead}.{tractate}  {tractate_title!r}  ({len(rows)} sections)")

    return manifest


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--include", nargs="*", default=[], help='Optional extra tractates, e.g. "I.1"')
    ap.add_argument("--out", default=str(OUT_DIR))
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    include_i1 = "I.1" in args.include
    print(f"Extracting pilot tractates -> {out_dir.relative_to(ROOT)}")
    manifest = build_manifest(include_i1=include_i1)

    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nWrote {len(manifest)} section files; manifest -> {manifest_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
