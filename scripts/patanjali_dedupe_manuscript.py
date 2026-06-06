#!/usr/bin/env python3
"""Remove duplicate Yoga Sūtra units from Pratibha MD (keep last occurrence per ref)."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT = ROOT / "data/pratibha_md/patanjali_yoga_sutras.md"

HEADER_END = "---\n"
UNIT_RE = re.compile(r"(?m)^##\s+(?!#)(.+?)\s*$")
SOURCE_RE = re.compile(r"^\*\*Source:\*\*\s*Patañjali, Yoga Sūtras\s+(\d+)\.(\d+)", re.M)


def _sutra_key(pada: int, num: int) -> tuple[int, int]:
    return pada, num


def dedupe(text: str) -> tuple[str, list[str]]:
    header_end = text.find(HEADER_END)
    if header_end == -1:
        header, body = "", text
    else:
        header = text[: header_end + len(HEADER_END)]
        body = text[header_end + len(HEADER_END) :]

    matches = list(UNIT_RE.finditer(body))
    units: list[tuple[tuple[int, int], str, str]] = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        block = body[start:end].strip() + "\n\n"
        sm = SOURCE_RE.search(block)
        if not sm:
            continue
        key = _sutra_key(int(sm.group(1)), int(sm.group(2)))
        title = m.group(1).strip()
        units.append((key, title, block))

    by_key: dict[tuple[int, int], tuple[str, str]] = {}
    removed: list[str] = []
    for key, title, block in units:
        if key in by_key:
            old_title = by_key[key][0]
            removed.append(f"{key[0]}.{key[1]}: dropped earlier '{old_title}', kept '{title}'")
        by_key[key] = (title, block)

    ordered = [by_key[k][1] for k in sorted(by_key.keys())]
    return header + "".join(ordered), removed


def main() -> int:
    ap = argparse.ArgumentParser(description="Dedupe Patanjali Yoga Sūtras Pratibha MD.")
    ap.add_argument("--path", type=Path, default=DEFAULT)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    text = args.path.read_text(encoding="utf-8")
    new_text, removed = dedupe(text)
    print(f"Removed {len(removed)} duplicate units; {len(removed) + (new_text.count('**Source:**'))} unique refs remain")
    for line in removed[:20]:
        print(" ", line)
    if len(removed) > 20:
        print(f"  ... and {len(removed) - 20} more")

    if args.dry_run:
        return 0
    args.path.write_text(new_text, encoding="utf-8")
    print(f"Wrote deduped manuscript to {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
