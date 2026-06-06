#!/usr/bin/env python3
"""Strip spurious footnote-reference markers from the Chuang Tzu canonical units.

The Palmer translation that seeded `data/canonical/the_book_of_chuang_tzu/` carried
inline footnote numbers (17, 18, 19, ...). During extraction each marker became its
own paragraph, splitting a single flowing sentence into three pieces:

    "Yen Hui" / "17" / "went to see Confucius..."

This cleaner removes every numeric-only paragraph and rejoins the surrounding text,
so the verse reads as continuous prose again. Only string fields are touched; all
other data is preserved. Run with --apply to write changes (default is a dry run).
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import sys

import yaml

COLLECTION_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "canonical",
    "the_book_of_chuang_tzu",
)

# Fields that hold reader-facing prose and may contain embedded markers.
TEXT_FIELDS = ("thesis", "source_excerpt", "translation_literal", "commentary", "insight")

_PARAGRAPH_SPLIT = re.compile(r"\n\s*\n")
_FOOTNOTE_MARKER = re.compile(r"^\d{1,3}$")


def clean_text(text: str) -> str:
    """Drop numeric-only paragraphs and merge the prose they interrupted."""
    if not isinstance(text, str) or not text.strip():
        return text
    paragraphs = [p.strip() for p in _PARAGRAPH_SPLIT.split(text)]
    result: list[str] = []
    join_next = False
    for para in paragraphs:
        if not para:
            continue
        if _FOOTNOTE_MARKER.match(para):
            # A footnote marker split one sentence in two; signal a merge.
            if result:
                join_next = True
            continue
        if join_next and result:
            result[-1] = f"{result[-1]} {para}"
            join_next = False
        else:
            result.append(para)
    return "\n\n".join(result)


def _str_representer(dumper: yaml.SafeDumper, data: str):
    """Render multi-line strings as literal blocks for readable diffs."""
    style = "|" if "\n" in data else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


class _Dumper(yaml.SafeDumper):
    pass


_Dumper.add_representer(str, _str_representer)


def process_file(path: str, apply: bool) -> int:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        return 0

    changes = 0
    for field in TEXT_FIELDS:
        if field not in data:
            continue
        original = data[field]
        cleaned = clean_text(original)
        if cleaned != original:
            data[field] = cleaned
            changes += 1

    # `source_excerpt` is often just a stranded fragment (e.g. "Yen Hui").
    # Replace it with the opening sentence(s) of the cleaned translation.
    translation = data.get("translation_literal") or ""
    excerpt = (data.get("source_excerpt") or "").strip()
    if isinstance(translation, str) and translation.strip() and 0 < len(excerpt) < 60:
        first_block = translation.strip().split("\n\n", 1)[0].strip()
        if first_block and first_block != excerpt:
            data["source_excerpt"] = first_block
            changes += 1

    if changes and apply:
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(
                data,
                f,
                Dumper=_Dumper,
                allow_unicode=True,
                sort_keys=False,
                width=4096,
                default_flow_style=False,
            )
    return changes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="write changes (default: dry run)")
    args = parser.parse_args()

    paths = sorted(glob.glob(os.path.join(COLLECTION_DIR, "*.yml")))
    if not paths:
        print(f"No YAML files found under {COLLECTION_DIR}", file=sys.stderr)
        return 1

    total_files = 0
    total_changes = 0
    for path in paths:
        changes = process_file(path, args.apply)
        if changes:
            total_files += 1
            total_changes += changes
            print(f"{'updated' if args.apply else 'would update'} {os.path.basename(path)} ({changes} fields)")

    verb = "Updated" if args.apply else "Would update"
    print(f"\n{verb} {total_files} files, {total_changes} fields total.")
    if not args.apply:
        print("Dry run only. Re-run with --apply to write changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
