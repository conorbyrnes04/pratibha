#!/usr/bin/env python3
"""
Parse Pratibha markdown source for Bhagavad Gita into YAML units.

Usage:
  python scripts/bhagavad_gita_pratibha_md_to_yaml.py <input_md> <output_dir>
"""

from __future__ import annotations

import argparse
import re
import shutil
import unicodedata
from pathlib import Path

import yaml


HEADING_RE = re.compile(r"(?m)^##\s+(.+?)\s*$")
SUBHEADING_RE = re.compile(r"(?m)^###\s+(.+?)\s*$")


def _clean(s: str) -> str:
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    lines: list[str] = []
    for raw in s.split("\n"):
        line = re.sub(r"[ \t]+", " ", raw).rstrip()
        if re.match(r"^\s*---+\s*$", line):
            continue
        if "Pratibha corpus entry" in line:
            continue
        lines.append(line)
    s = "\n".join(lines)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def _slug_ascii(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w\s-]", " ", s.lower())
    return re.sub(r"[\s_-]+", "_", s).strip("_")


def _extract_subsections(block: str) -> dict[str, str]:
    out: dict[str, str] = {}
    matches = list(SUBHEADING_RE.finditer(block))
    for i, m in enumerate(matches):
        key = _slug_ascii(m.group(1))
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(block)
        out[key] = _clean(block[start:end])
    return out


def _themes(*parts: str) -> list[str]:
    blob = _slug_ascii(" ".join(parts))
    seeds = [
        "dharma",
        "karma",
        "yoga",
        "jnana",
        "bhakti",
        "sannyasa",
        "equanimity",
        "detachment",
        "self_knowledge",
        "action",
        "practice",
        "liberation",
    ]
    return [t for t in seeds if re.search(rf"\b{re.escape(t)}\b", blob)][:8]


def parse_markdown(path: Path) -> list[dict]:
    text = _clean(path.read_text(encoding="utf-8"))
    units: list[dict] = []

    heads = list(HEADING_RE.finditer(text))
    for i, m in enumerate(heads):
        title = _clean(m.group(1))
        if "pratibha" in title.lower() and "bhagavad" in title.lower():
            continue

        start = m.end()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        block = _clean(text[start:end])
        if not block:
            continue

        source_match = re.search(r"(?m)^\*\*Source:\*\*\s*(.+?)\s*$", block)
        source = source_match.group(1).strip() if source_match else ""

        fields = _extract_subsections(block)
        # Skill uses ### Devanagari; older drafts used ### Original.
        original = (
            fields.get("devanagari", "")
            or fields.get("original", "")
            or fields.get("sanskrit", "")
        )
        iast = fields.get("iast", "")
        translation = fields.get("pratibha_translation", "") or fields.get("translation", "")
        commentary = fields.get("pratibha_commentary", "") or fields.get("commentary", "")
        key_terms = fields.get("key_terms", "")
        resonances = (
            fields.get("cross_tradition_resonances", "")
            or fields.get("resonances", "")
        )
        practice = fields.get("practice_abhyasa", "") or fields.get("practice", "")

        if not translation:
            continue

        long_parts: list[str] = [commentary] if commentary else []
        if key_terms:
            long_parts.append(f"Key Terms:\n\n{key_terms}")
        if resonances:
            long_parts.append(f"Cross-Tradition Resonances:\n\n{resonances}")
        long_commentary = "\n\n".join(p.strip() for p in long_parts if p.strip())

        # Verse-stable IDs (avoid colliding with retired thematic BG_MD_001..012 hubs).
        # Source examples: "Bhagavad Gītā 2.47" / "Bhagavad Gītā 1.2–1.4"
        ch, start_v, end_v = _verse_span(source)
        if ch and start_v:
            if end_v and end_v != start_v:
                sutra_id = f"BG_{ch:02d}_{start_v:02d}_{end_v:02d}"
            else:
                sutra_id = f"BG_{ch:02d}_{start_v:02d}"
        else:
            sutra_id = f"BG_MD_{len(units) + 1:03d}"

        units.append(
            {
                "sutra_id": sutra_id,
                "collection": "Bhagavad Gita",
                "section": f"chapter_{ch:02d}" if ch else "teaching_passage",
                "title": title,
                "sanskrit": original,
                "transliteration": iast,
                "translation": translation,
                "commentary": long_commentary,
                "voice_of_siva": "",
                "abhyasa": practice,
                "modes": {
                    "bhasya": "",
                    "doctrinal": "",
                    "comparative": "",
                    "sadhana": practice,
                },
                "glossary": [],
                "themes": _themes(title, source, translation, commentary, key_terms, resonances),
                "source": source,
            }
        )
    return units


def _verse_span(source: str) -> tuple[int, int, int]:
    """Return (chapter, start_verse, end_verse) from a Source line."""
    m = re.search(
        r"(\d+)\s*\.\s*(\d+)\s*[–—-]\s*(?:(\d+)\s*\.\s*)?(\d+)",
        source or "",
    )
    if m:
        ch = int(m.group(1))
        start = int(m.group(2))
        end = int(m.group(4))
        return ch, start, end
    m = re.search(r"(\d+)\s*\.\s*(\d+)", source or "")
    if m:
        ch = int(m.group(1))
        v = int(m.group(2))
        return ch, v, v
    return 0, 0, 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Convert Bhagavad Gita Pratibha markdown to YAML files.")
    ap.add_argument("input_md", type=Path)
    ap.add_argument("output_dir", type=Path)
    args = ap.parse_args()

    records = parse_markdown(args.input_md)
    if args.output_dir.exists():
        shutil.rmtree(args.output_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for rec in records:
        slug = rec["sutra_id"].lower()
        out = args.output_dir / f"{slug}.yml"
        out.write_text(
            yaml.safe_dump(rec, allow_unicode=True, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )

    print(f"Wrote {len(records)} YAML files to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
