#!/usr/bin/env python3
"""
Parse the Tao Te Ching EPUB into chapter YAML files with appendix commentaries.

Output schema adds:
  appendixes:
    - commentator: "The River Master"
      text: "..."
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml
from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, epub


COMMENTATOR_MAP = {
    "THE RIVER MASTER": "The River Master",
    "MAGISTER LIU": "Magister Liu",
}


def clean_text(html: bytes) -> str:
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text("\n")
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def clean_line(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def looks_like_chapter_doc(name: str, lines: list[str]) -> bool:
    # Typical file names: xhtml/09_1_Gateway_to_All_Marv.xhtml
    if re.search(r"/\d+_\d+_", name):
        return True
    return bool(lines and re.fullmatch(r"\d{1,3}", lines[0]))


def detect_commentator_heading(line: str) -> str | None:
    raw = clean_line(line)
    key = raw.rstrip(":").upper()
    if key in COMMENTATOR_MAP:
        return COMMENTATOR_MAP[key]

    # Generic heading form: "Waley:" / "Duyvendak:" / "JM:"
    if raw.endswith(":"):
        label = raw[:-1].strip()
        if 1 <= len(label.split()) <= 6 and len(label) <= 40:
            # Avoid grabbing normal sentence lines.
            if re.fullmatch(r"[\w .'\-–]+", label) and label[:1].isalnum():
                return label
    return None


def parse_chapter(lines: list[str], fallback_n: int) -> dict[str, Any] | None:
    if len(lines) < 4:
        return None

    # first line should be chapter number
    if re.fullmatch(r"\d{1,3}", lines[0]):
        chapter_n = int(lines[0])
        start = 1
    else:
        chapter_n = fallback_n
        start = 0

    title = clean_line(lines[start]) if start < len(lines) else f"Chapter {chapter_n}"
    body = [l for l in lines[start + 1 :] if l.strip()]

    current_commentator: str | None = None
    verse_lines: list[str] = []
    comments: dict[str, list[str]] = {}

    for raw in body:
        line = clean_line(raw)
        if not line:
            continue
        canonical = detect_commentator_heading(line)
        if canonical:
            current_commentator = canonical
            comments.setdefault(canonical, [])
            continue
        if current_commentator is None:
            verse_lines.append(line)
        else:
            comments[current_commentator].append(line)

    translation = "\n".join(verse_lines).strip()
    appendixes = []
    for who, pieces in comments.items():
        t = "\n".join(pieces).strip()
        if t:
            appendixes.append({"commentator": who, "text": t})

    commentary = ""
    if appendixes:
        commentary = "\n\n".join(f"{a['commentator']}:\n{a['text']}" for a in appendixes)

    chapter_id = f"{chapter_n:03d}"
    return {
        "sutra_id": f"ttc_{chapter_id}",
        "sutra": f"Tao Te Ching {chapter_n}",
        "collection": "Tao Te Ching",
        "section": "verse chapter",
        "chapter_number": chapter_n,
        "title": title,
        "sanskrit": "",
        "transliteration": "",
        "translation": translation,
        "commentary": commentary,
        "appendixes": appendixes,
        "modes": {"bhasya": "", "doctrinal": "", "comparative": "", "sadhana": ""},
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("epub_path")
    ap.add_argument("output_dir")
    args = ap.parse_args()

    epub_path = Path(args.epub_path)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # clear existing chapter files for deterministic reruns
    for p in out_dir.glob("*.yml"):
        p.unlink()

    book = epub.read_epub(str(epub_path))
    chapters: list[dict[str, Any]] = []
    fallback_n = 1
    for item in book.get_items_of_type(ITEM_DOCUMENT):
        raw_text = clean_text(item.get_content())
        lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
        if not looks_like_chapter_doc(item.get_name(), lines):
            continue
        chapter = parse_chapter(lines, fallback_n=fallback_n)
        if chapter is None:
            continue
        chapters.append(chapter)
        fallback_n += 1

    chapters.sort(key=lambda c: int(c.get("chapter_number") or 0))
    for ch in chapters:
        n = int(ch["chapter_number"])
        fp = out_dir / f"ch_{n:03d}.yml"
        with open(fp, "w", encoding="utf-8") as f:
            yaml.safe_dump(ch, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120)

    print(f"Wrote {len(chapters)} chapter YAML files to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

