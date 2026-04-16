#!/usr/bin/env python3
"""
Parse Heraclitus "Fragments.epub" into wisdom-pearl YAML files.

Usage:
  python scripts/fragments_epub_to_yaml.py <input.epub> <output_dir>
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

import yaml
from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, epub


def clean_lines(raw: str) -> list[str]:
    raw = raw.replace("\r", "\n").replace("\f", "\n")
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in raw.split("\n")]
    return [ln for ln in lines if ln]


def title_from_text(text: str, n: int) -> str:
    t = re.sub(r"\s+", " ", text).strip()
    if not t:
        return f"Fragment {n}"
    if len(t) > 92:
        return t[:89].rstrip() + "..."
    return t


def _fragment_score(text: str) -> int:
    # Prefer richer English renderings when duplicate fragment numbers appear.
    score = len(text)
    if re.search(r"\b(the|and|of|to|is|in|for|with)\b", text.lower()):
        score += 40
    if "unus dies" in text.lower():
        score -= 80
    return score


def parse_core_fragments(epub_path: Path) -> dict[int, str]:
    book = epub.read_epub(str(epub_path))
    core_item = None
    for item in book.get_items_of_type(ITEM_DOCUMENT):
        name = item.get_name().lower()
        if "_c01_" in name:
            core_item = item
            break
    if core_item is None:
        return {}

    soup = BeautifulSoup(core_item.get_content(), "lxml")
    lines = clean_lines(soup.get_text("\n"))

    found: dict[int, str] = {}
    current_n: int | None = None
    buff: list[str] = []

    def flush() -> None:
        nonlocal current_n, buff
        if current_n is None:
            buff = []
            return
        text = "\n".join(buff).strip()
        text = re.sub(r"\n{3,}", "\n\n", text)
        if not text:
            buff = []
            return
        # Drop obvious placeholder/noise fragments.
        if text.lower() in {"see note.", "see note"}:
            buff = []
            return
        prev = found.get(current_n)
        if prev is None or _fragment_score(text) > _fragment_score(prev):
            found[current_n] = text
        buff = []

    for ln in lines:
        if re.fullmatch(r"\d{1,3}", ln):
            flush()
            current_n = int(ln)
            continue
        # Ignore title/header noise before first numbered fragment.
        if current_n is None:
            continue
        buff.append(ln)
    flush()
    return found


def to_yaml_records(fragments: dict[int, str]) -> list[dict]:
    out: list[dict] = []
    for n in sorted(fragments.keys()):
        text = fragments[n]
        sid = f"HFR_P{n:03d}"
        out.append(
            {
                "sutra_id": sid,
                "collection": "Heraclitus Fragments",
                "section": "wisdom_pearl",
                "title": title_from_text(text.split("\n")[0], n),
                "sanskrit": "",
                "transliteration": "",
                "translation": text,
                "commentary": micro_commentary(text),
                "voice_of_siva": "",
                "abhyasa": "Read this fragment three times slowly. Pause in silence for one minute and note one direct insight it reveals.",
                "modes": {
                    "bhasya": "",
                    "doctrinal": "",
                    "comparative": "",
                    "sadhana": "Hold this fragment in awareness through the day; return to it whenever reactivity appears.",
                },
                "glossary": [],
            }
        )
    return out


def micro_commentary(text: str) -> str:
    """
    Add a concise interpretive gloss while preserving aphoristic force.
    """
    s = re.sub(r"\s+", " ", text).lower()
    if any(k in s for k in ("word", "logos", "listen", "hearing", "wisdom")):
        return "The fragment points to a wisdom that is heard rather than invented: reality has an intelligible order, and our task is to align attention with it."
    if any(k in s for k in ("fire", "lightning", "cosmos", "measure")):
        return "Here change is not chaos but lawful transformation. The world is dynamic, yet governed by proportion and measure."
    if any(k in s for k in ("war", "strife", "conflict", "opposition", "contending")):
        return "Opposites are not enemies to erase but tensions that generate becoming. Harmony is discovered through, not apart from, contrast."
    if any(k in s for k in ("soul", "fate", "character", "death")):
        return "The line turns inquiry inward: character and attention shape destiny. Mortality sharpens the call to live deliberately."
    return "This fragment invites direct contemplation rather than argument: hold its paradox quietly and let understanding ripen through experience."


def main() -> int:
    ap = argparse.ArgumentParser(description="Convert Fragments EPUB to wisdom-pearl YAML files.")
    ap.add_argument("epub_path", type=Path)
    ap.add_argument("output_dir", type=Path)
    args = ap.parse_args()

    fragments = parse_core_fragments(args.epub_path)
    records = to_yaml_records(fragments)

    if args.output_dir.exists():
        shutil.rmtree(args.output_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for rec in records:
        n = int(rec["sutra_id"].split("P")[-1])
        out = args.output_dir / f"fragment_{n:03d}.yml"
        out.write_text(
            yaml.safe_dump(rec, allow_unicode=True, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )

    print(f"Wrote {len(records)} YAML files to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

