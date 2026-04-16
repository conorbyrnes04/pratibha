#!/usr/bin/env python3
"""
Parse "All the Works of Epictetus ... .epub" into wisdom-pearl YAML files.

Usage:
  python scripts/epictetus_works_epub_to_yaml.py <input.epub> <output_dir>
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

import yaml
from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, epub


def clean_text(raw: str) -> str:
    raw = raw.replace("\r", "\n").replace("\f", "\n")
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in raw.split("\n")]
    out: list[str] = []
    blank = False
    for ln in lines:
        if not ln:
            if not blank:
                out.append("")
            blank = True
            continue
        out.append(ln)
        blank = False
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()


def first_paragraph(text: str, limit: int = 700) -> str:
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not parts:
        return ""
    p = parts[0]
    return p if len(p) <= limit else p[: limit - 3].rstrip() + "..."


def _is_heading_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    if re.match(r"^CHAPTER\s+[IVXLCDM0-9]+\b\.?$", s, flags=re.IGNORECASE):
        return True
    if re.match(r"^[IVXLCDM]+\.\s*$", s, flags=re.IGNORECASE):
        return True
    return False


def _is_subtitle_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    # Short all-caps-ish line used as chapter subtitle.
    if len(s) <= 150 and s == s.upper() and re.search(r"[A-Z]{3,}", s):
        return True
    return False


def _split_title_and_body(text: str, idx: int) -> tuple[str, str]:
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    if not lines:
        return f"Section {idx}", ""
    title = lines[0]
    body_start = 1
    if _is_heading_line(lines[0]) and len(lines) > 1 and _is_subtitle_line(lines[1]):
        title = f"{lines[0]} {lines[1]}"
        body_start = 2
    body = "\n".join(lines[body_start:]).strip()
    if not body:
        body = "\n".join(lines[1:]).strip()
    return title[:160], body


def compact_commentary(text: str, max_paragraphs: int = 3, max_chars: int = 1800) -> str:
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    if len(parts) <= 1:
        return ""
    out = "\n\n".join(parts[1 : 1 + max_paragraphs])
    out = re.sub(r"\s+", " ", out).strip()
    return out if len(out) <= max_chars else out[: max_chars - 3].rstrip() + "..."


def infer_section(idx: int, heading: str) -> str:
    if heading.startswith("CHAPTER "):
        return "Discourses"
    if idx >= 140:
        return "Fragments"
    return "Enchiridion"


def suggest_abhyasa(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ("power", "control", "in our power", "not in our power")):
        return "For one minute, separate what is in your control from what is not. Act only on the first, release the second."
    if any(k in t for k in ("anger", "grief", "disturb", "calamities")):
        return "When agitation appears today, pause for three breaths and name the judgment beneath the emotion before reacting."
    if any(k in t for k in ("god", "providence", "nature", "fate")):
        return "End the day by noting one event you resisted and one event you accepted. Reflect on how acceptance changed your mind."
    return "Read this passage slowly three times. Keep one sentence with you and return to it whenever you feel scattered."


def _split_index(name: str) -> int | None:
    m = re.search(r"_split_(\d+)\.html?$", name.lower())
    return int(m.group(1)) if m else None


def parse_epub(epub_path: Path) -> list[dict]:
    book = epub.read_epub(str(epub_path))
    records: list[dict] = []

    for item in book.get_items_of_type(ITEM_DOCUMENT):
        idx = _split_index(item.get_name())
        if idx is None:
            continue
        # Core content starts after frontmatter; skip final generated TOC.
        if idx < 5 or idx >= 146:
            continue

        soup = BeautifulSoup(item.get_content(), "lxml")
        text = clean_text(soup.get_text("\n"))
        if not text:
            continue

        first_line = next((ln.strip() for ln in text.split("\n") if ln.strip()), "")
        upper = first_line.upper()

        # Skip structural headers and transition note pages.
        if upper.startswith("BOOK "):
            continue
        if "THE FOLLOWING FRAGMENTS ARE OMITTED" in upper:
            continue
        if upper.startswith("TABLE OF CONTENTS"):
            continue

        if not (
            upper.startswith("CHAPTER ")
            or re.match(r"^[IVXLCDM]+\.\s+", first_line)
            or upper.startswith("ARRIAN TO ")
        ):
            continue

        title, body_text = _split_title_and_body(text, idx)
        if not body_text:
            continue

        section = infer_section(idx, upper)
        translation = first_paragraph(body_text, limit=700)
        if not translation or _is_heading_line(translation):
            continue
        commentary = compact_commentary(body_text, max_paragraphs=3, max_chars=1800)
        records.append(
            {
                "idx": idx,
                "section": section,
                "title": title,
                "translation": translation,
                "commentary": commentary,
                "abhyasa": suggest_abhyasa(translation + "\n" + commentary),
            }
        )
    return sorted(records, key=lambda r: r["idx"])


def to_yaml_records(records: list[dict]) -> list[dict]:
    out: list[dict] = []
    for i, r in enumerate(records, start=1):
        sid = f"EPI_P{i:03d}"
        out.append(
            {
                "sutra_id": sid,
                "collection": "Epictetus Works",
                "section": r["section"].lower().replace(" ", "_"),
                "title": r["title"],
                "sanskrit": "",
                "transliteration": "",
                "translation": r["translation"],
                "commentary": r["commentary"],
                "voice_of_siva": "",
                "abhyasa": r["abhyasa"],
                "modes": {
                    "bhasya": "",
                    "doctrinal": "",
                    "comparative": "",
                    "sadhana": r["abhyasa"],
                },
                "glossary": [],
            }
        )
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Convert Epictetus Works EPUB into wisdom-pearl YAML files.")
    ap.add_argument("epub_path", type=Path)
    ap.add_argument("output_dir", type=Path)
    args = ap.parse_args()

    records = parse_epub(args.epub_path)
    yaml_records = to_yaml_records(records)

    if args.output_dir.exists():
        shutil.rmtree(args.output_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for rec in yaml_records:
        idx = rec["sutra_id"].split("P")[-1]
        out = args.output_dir / f"epictetus_p{idx}.yml"
        out.write_text(
            yaml.safe_dump(rec, allow_unicode=True, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )

    print(f"Wrote {len(yaml_records)} YAML files to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

