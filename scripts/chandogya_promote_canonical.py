#!/usr/bin/env python3
"""Promote Chāndogya pilot YAML to canonical corpus files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.data_loader import normalize_unit  # noqa: E402

WORK_ID = "chandogya_upanishad"
WORK_TITLE = "Chāndogya Upaniṣad"


def promote(yaml_dir: Path, canonical_dir: Path) -> int:
    yaml_dir = yaml_dir if yaml_dir.is_absolute() else ROOT / yaml_dir
    canonical_dir = canonical_dir if canonical_dir.is_absolute() else ROOT / canonical_dir
    canonical_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(yaml_dir.glob("*.yml"))
    if not files:
        print(f"No YAML files in {yaml_dir}", file=sys.stderr)
        return 1

    ok = 0
    for fp in files:
        raw = yaml.safe_load(fp.read_text(encoding="utf-8")) or {}
        if not isinstance(raw, dict):
            continue
        sid = str(raw.get("sutra_id") or fp.stem).upper()
        slug = sid.lower()
        unit_id = f"{WORK_ID}.{slug}"

        record = {
            "source_file": str(fp.relative_to(ROOT)).replace("\\", "/"),
            "source_id": sid,
            "category": "root_text",
            "work_id": WORK_ID,
            "work_title": WORK_TITLE,
            "unit_id": unit_id,
            "unit_label": raw.get("title") or sid,
            "title": raw.get("title") or sid,
            "unit_type": "sutra",
            "sanskrit_devanagari": raw.get("sanskrit") or raw.get("sanskrit_devanagari") or "",
            "sanskrit_iast": raw.get("transliteration") or raw.get("sanskrit_iast") or "",
            "translation_literal": raw.get("translation") or raw.get("translation_literal") or "",
            "commentary": raw.get("commentary") or "",
            "practice": raw.get("abhyasa") or raw.get("practice") or "",
            "themes": raw.get("themes") or [],
            "editorial_maturity": raw.get("editorial_maturity") or "strong_draft",
            "editorial_score": raw.get("editorial_score") or 70,
            "provenance": {
                "collection": WORK_TITLE,
                "section": raw.get("section") or "",
                "original_id": sid,
                "source_reference": raw.get("source") or "",
            },
        }

        norm = normalize_unit(record, str(canonical_dir / f"{WORK_ID}_{slug}.yml"))
        if not norm.get("commentary") and record.get("commentary"):
            # preserve commentary even if parser strips (shouldn't for authored content)
            record["commentary"] = raw.get("commentary")

        out = canonical_dir / f"{WORK_ID}_{slug}.yml"
        out.write_text(
            yaml.safe_dump(record, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120),
            encoding="utf-8",
        )
        ok += 1
        print(f"  {sid} -> {out.relative_to(ROOT)}")

    print(f"Promoted {ok} units to {canonical_dir.relative_to(ROOT)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--yaml-dir",
        type=Path,
        default=ROOT / "data" / "yaml" / "chandogya_upanishad",
    )
    ap.add_argument(
        "--canonical-dir",
        type=Path,
        default=ROOT / "data" / "canonical" / "chandogya_upanishad",
    )
    args = ap.parse_args()
    return promote(args.yaml_dir, args.canonical_dir)


if __name__ == "__main__":
    raise SystemExit(main())
