#!/usr/bin/env python3
"""
Parse The Book of Chuang Tzu EPUB into chapter-level YAML units.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml
from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, epub


def clean_text(html: bytes) -> str:
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text("\n")
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def clean_line(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def is_chapter_doc(name: str, lines: list[str]) -> bool:
    if re.search(r"/ch\d+\.html$", name, flags=re.IGNORECASE):
        return True
    return bool(lines and re.fullmatch(r"CHAPTER\s+\d+", lines[0], flags=re.IGNORECASE))


def parse_chapter(name: str, text: str) -> dict[str, Any] | None:
    lines = [clean_line(l) for l in text.splitlines() if clean_line(l)]
    if not is_chapter_doc(name, lines):
        return None

    m_name = re.search(r"ch(\d+)\.html$", name, flags=re.IGNORECASE)
    m_head = re.match(r"CHAPTER\s+(\d+)", lines[0], flags=re.IGNORECASE) if lines else None
    if m_name:
        chapter_n = int(m_name.group(1))
    elif m_head:
        chapter_n = int(m_head.group(1))
    else:
        return None

    # Typical form: CHAPTER N / title / body...
    title = f"Chapter {chapter_n}"
    body_start = 1
    if len(lines) > 1 and not re.match(r"^\d+$", lines[1]):
        title = lines[1]
        body_start = 2

    body = "\n\n".join(lines[body_start:]).strip()
    if not body:
        return None

    # Use opening excerpt as translation summary.
    excerpt = body[:1200].strip()

    return {
        "sutra_id": f"ctz_{chapter_n:03d}",
        "sutra": f"Chuang Tzu {chapter_n}",
        "collection": "The Book of Chuang Tzu",
        "section": f"chapter {chapter_n}",
        "chapter_number": chapter_n,
        "title": title,
        "sanskrit": "",
        "transliteration": "",
        "translation": excerpt,
        "commentary": body,
        "modes": {"bhasya": "", "doctrinal": "", "comparative": "", "sadhana": ""},
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("epub_path")
    ap.add_argument("output_dir")
    args = ap.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for p in out_dir.glob("*.yml"):
        p.unlink()

    book = epub.read_epub(args.epub_path)
    chapters: list[dict[str, Any]] = []
    for item in book.get_items_of_type(ITEM_DOCUMENT):
        text = clean_text(item.get_content())
        ch = parse_chapter(item.get_name(), text)
        if ch:
            chapters.append(ch)

    chapters.sort(key=lambda x: int(x["chapter_number"]))
    for c in chapters:
        fp = out_dir / f"ch_{int(c['chapter_number']):03d}.yml"
        with open(fp, "w", encoding="utf-8") as f:
            yaml.safe_dump(c, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120)

    print(f"Wrote {len(chapters)} chapter YAML files to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

