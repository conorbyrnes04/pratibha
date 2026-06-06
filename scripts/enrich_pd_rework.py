#!/usr/bin/env python3
"""Clean PD anchor OCR and apply Pratibha reworks (anchor vs display translation split).

Usage:
  python scripts/enrich_pd_rework.py --collection heraclitus_fragments
  python scripts/enrich_pd_rework.py --collection the_book_of_chuang_tzu --prefix ch_
  python scripts/enrich_pd_rework.py --all
  python scripts/enrich_pd_rework.py --all --canonicalize
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
REWORK_FILE = ROOT / "data" / "rework" / "pd_anchors.yml"

COLLECTION_DIRS = {
    "heraclitus_fragments": ROOT / "data" / "yaml" / "fragments",
    "the_book_of_chuang_tzu": ROOT / "data" / "yaml" / "the_book_of_chuang_tzu",
}


def clean_ocr(text: str) -> str:
    """Fix common Archive.org hyphenation and whitespace without changing meaning."""
    text = re.sub(r"(\w)-\s+(\w)", r"\1\2", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = text.replace("''", '"').replace('""', '"')
    return text.strip()


def load_reworks() -> dict[str, dict[str, dict[str, str]]]:
    if not REWORK_FILE.exists():
        return {}
    raw = yaml.safe_load(REWORK_FILE.read_text(encoding="utf-8")) or {}
    return {str(k): v for k, v in raw.items() if isinstance(v, dict)}


def apply_rework(data: dict[str, Any], rework: dict[str, str]) -> bool:
    changed = False
    anchor = clean_ocr(str(data.get("anchor_translation") or data.get("translation") or ""))
    if anchor and data.get("anchor_translation") != anchor:
        data["anchor_translation"] = anchor
        changed = True
    elif anchor and not data.get("anchor_translation"):
        data["anchor_translation"] = anchor
        changed = True

    for field in ("pratibha_translation", "commentary"):
        if field in rework and rework[field].strip():
            if data.get(field) != rework[field].strip():
                data[field] = rework[field].strip()
                changed = True
    return changed


def enrich_file(path: Path, reworks: dict[str, dict[str, str]]) -> bool:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    sid = str(data.get("sutra_id") or path.stem)
    stem_key = path.stem  # e.g. ch_001

    rework = reworks.get(sid) or reworks.get(stem_key) or {}

    changed = False
    trans = str(data.get("translation") or "").strip()
    if trans:
        cleaned = clean_ocr(trans)
        if not data.get("anchor_translation"):
            data["anchor_translation"] = cleaned
            changed = True
        elif data.get("anchor_translation") != cleaned:
            data["anchor_translation"] = cleaned
            changed = True

    if rework:
        changed = apply_rework(data, rework) or changed

    # Display translation: Pratibha rework when present, else cleaned anchor.
    display = str(data.get("pratibha_translation") or data.get("anchor_translation") or trans).strip()
    if display and data.get("translation") != display:
        data["translation"] = display
        changed = True

    if changed:
        path.write_text(
            yaml.safe_dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False, width=110),
            encoding="utf-8",
        )
    return changed


def main() -> int:
    ap = argparse.ArgumentParser(description="Apply OCR cleanup and Pratibha reworks to PD anchor YAML.")
    ap.add_argument("--collection", choices=list(COLLECTION_DIRS.keys()))
    ap.add_argument("--prefix", default="", help="Only files matching this prefix (e.g. ch_)")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--canonicalize", action="store_true")
    args = ap.parse_args()

    if not args.all and not args.collection:
        ap.error("Specify --collection or --all")

    all_reworks = load_reworks()
    targets = list(COLLECTION_DIRS.keys()) if args.all else [args.collection]

    total = 0
    for coll in targets:
        yaml_dir = COLLECTION_DIRS[coll]
        reworks = all_reworks.get(coll, {})
        coll_count = 0
        for path in sorted(yaml_dir.glob("*.yml")):
            if args.prefix and not path.name.startswith(args.prefix):
                continue
            if enrich_file(path, reworks):
                coll_count += 1
        total += coll_count
        print(f"{coll}: updated {coll_count} files (reworks catalog: {len(reworks)} manual entries)")

    if args.canonicalize:
        py = sys.executable
        subprocess.run([py, str(ROOT / "scripts" / "canonicalize_texts.py")], check=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
