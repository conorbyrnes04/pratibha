#!/usr/bin/env python3
"""Assemble chapter Pratibha MD files into YAML + canonicalize, replacing old mega-units.

Usage:
  python scripts/assemble_bhagavad_gita_full.py
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD_DIR = ROOT / "data" / "pratibha_md" / "bhagavad_gita"
YAML_DIR = ROOT / "data" / "yaml" / "bhagavad_gita"
CANON_DIR = ROOT / "data" / "canonical" / "bhagavad_gita"
CONVERTER = ROOT / "scripts" / "bhagavad_gita_pratibha_md_to_yaml.py"


def main() -> int:
    chapters = sorted(MD_DIR.glob("chapter_*.md"))
    if not chapters:
        print(f"No chapter_*.md in {MD_DIR}", file=sys.stderr)
        return 1
    # Concatenate into one MD for the existing converter, renumbering units
    combined = MD_DIR / "_full_combined.md"
    parts = ["# Pratibha — Bhagavad Gītā (full verse-scale corpus)\n"]
    for p in chapters:
        text = p.read_text(encoding="utf-8")
        # Keep only unit headings. Chapter H1 + **Corpus entry:** preambles must
        # not sit after the previous chapter's last Practice layer, or they are
        # ingested (and then spoken by Listen) as part of that unit.
        start = re.search(r"(?m)^##\s+", text)
        text = text[start.start():] if start else re.sub(
            r"(?m)^#\s+(?!#).*\n?", "", text, count=1
        )
        parts.append(text.strip())
        parts.append("")
    combined.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    if YAML_DIR.exists():
        shutil.rmtree(YAML_DIR)
    YAML_DIR.mkdir(parents=True)
    subprocess.run([sys.executable, str(CONVERTER), str(combined), str(YAML_DIR)], check=True, cwd=ROOT)
    subprocess.run([sys.executable, str(ROOT / "scripts" / "canonicalize_texts.py")], check=True, cwd=ROOT)
    n = len(list(CANON_DIR.glob("*.yml")))
    print(f"canonical units in {CANON_DIR}: {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
