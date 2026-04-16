#!/usr/bin/env python3
"""
Parse "Know Yourself" (Ibn Arabi / Balyani) EPUB into wisdom-pearl YAML files.

Usage:
  python scripts/ibn_arabi_know_yourself_epub_to_yaml.py <input.epub> <output_dir>
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

import yaml
from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, epub


CORE_TITLE = "On the meaning of the saying of the Prophet Muhammad"


def clean_text(raw: str) -> str:
    raw = raw.replace("\r", "\n").replace("\f", "\n")
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in raw.split("\n")]
    lines = [ln for ln in lines if ln]
    text = "\n".join(lines).strip()
    return re.sub(r"\n{3,}", "\n\n", text)


def first_paragraph(text: str, limit: int = 420) -> str:
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not parts:
        return ""
    return parts[0][:limit].strip()


def detect_title(text: str) -> str:
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    if not lines:
        return ""

    first = lines[0]
    known = [
        "Acknowledgements",
        "Introduction",
        "Know Yourself",
        "On the meaning of the saying of the Prophet Muhammad",
        "Translator’s notes on the text",
        "History of the translations",
        "Quotations from the Quran",
        "Bibliography",
    ]
    for k in known:
        if first.lower().startswith(k.lower()):
            return k

    if len(first) <= 90:
        return first

    return "Section"


def parse_epub(epub_path: Path) -> list[dict]:
    book = epub.read_epub(str(epub_path))
    records: list[dict] = []

    for item in book.get_items_of_type(ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), "lxml")
        text = clean_text(soup.get_text("\n"))
        title = detect_title(text)
        records.append(
            {
                "title": title,
                "text": text,
            }
        )

    # Deduplicate near-identical sections by normalized prefix.
    deduped: list[dict] = []
    seen: set[str] = set()
    for r in records:
        key = re.sub(r"\W+", " ", (r["title"] + " " + r["text"][:180]).lower()).strip()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(r)
    return deduped


def _clean_pearl_text(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    # Remove footnote markers and common scholarly noise.
    s = re.sub(r"\b\d{1,3}\b", "", s)
    s = re.sub(r"\s{2,}", " ", s).strip()
    return s


def extract_wisdom_pearls(records: list[dict]) -> list[str]:
    """
    Produce concise contemplative pearls from the core chapter only.
    """
    core = next((r for r in records if r["title"].lower().startswith(CORE_TITLE.lower())), None)
    if not core:
        return []

    text = core["text"]
    # Strip chapter heading boilerplate before pearl extraction.
    text = re.sub(
        r"^On the meaning of the saying of the Prophet Muhammad.*?In the name of God,\s*the compassionate,\s*the merciful\s*",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    # Remove obvious scholarly apparatus and line noise before sentence splitting.
    text = re.sub(r"\bQ\.\d+:\d+\b", " ", text)
    text = re.sub(r"\b\d{1,2}\b", " ", text)
    text = re.sub(r"\s{2,}", " ", text).strip()

    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    pearls: list[str] = []

    # Build 2-4 sentence windows to capture complete wisdom statements.
    for i in range(len(sentences)):
        for span in (2, 3, 4):
            if i + span > len(sentences):
                continue
            c = _clean_pearl_text(" ".join(sentences[i : i + span]))
            cl = c.lower()
            if len(c) < 180 or len(c) > 820:
                continue
            if "if someone asks" in cl or "the answer is" in cl or "the reply is" in cl:
                continue
            if "bibliography" in cl or "history of the translations" in cl:
                continue
            # Keep highly contemplative/ontological windows.
            if sum(
                1
                for k in ("god", "self", "lord", "being", "oneness", "know", "union", "existence")
                if k in cl
            ) < 2:
                continue
            pearls.append(c)

    # Deduplicate near-equal pearls.
    out: list[str] = []
    seen: set[str] = set()
    for p in pearls:
        key = re.sub(r"\W+", " ", p.lower())[:140]
        if key in seen:
            continue
        seen.add(key)
        out.append(p)
        if len(out) >= 36:
            break
    return out


def to_yaml_records(records: list[dict]) -> list[dict]:
    pearls = extract_wisdom_pearls(records)
    out: list[dict] = []
    for i, pearl in enumerate(pearls, start=1):
        sid = f"KYS_P{i:03d}"
        out.append(
            {
                "sutra_id": sid,
                "collection": "Know Yourself (Ibn Arabi / Balyani)",
                "section": "wisdom_pearl",
                "title": f"Pearl #{i}",
                "sanskrit": "",
                "transliteration": "",
                "translation": first_paragraph(pearl, limit=520),
                "commentary": pearl,
                "modes": {
                    "bhasya": "",
                    "doctrinal": "",
                    "comparative": "",
                    "sadhana": "Contemplate this pearl slowly in silence for 3-5 minutes, then journal one direct insight.",
                },
            }
        )
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Convert Know Yourself EPUB to chapter YAML files.")
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
        out = args.output_dir / f"kys_p{idx}.yml"
        out.write_text(
            yaml.safe_dump(rec, allow_unicode=True, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )

    print(f"Wrote {len(yaml_records)} YAML files to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

