#!/usr/bin/env python3
"""
Parse Pratibha markdown source for Mandukya Upanishad + Gaudapada Karika into YAML units.

Usage:
  python scripts/mandukya_md_to_yaml.py <input_md> <output_dir>
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
        lines.append(line)
    s = "\n".join(lines)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def _slug_ascii(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w\s-]", " ", s.lower())
    return re.sub(r"[\s_-]+", "_", s).strip("_")


def _strip_md(s: str) -> str:
    s = re.sub(r"\*\*(.*?)\*\*", r"\1", s)
    s = re.sub(r"\*(.*?)\*", r"\1", s)
    return s.strip()


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
        "consciousness",
        "nonduality",
        "self",
        "awareness",
        "silence",
        "meditation",
        "advaita",
        "ajativada",
        "om",
        "practice",
    ]
    return [t for t in seeds if re.search(rf"\b{re.escape(t)}\b", blob)][:8]


def _strip_source_line(s: str) -> str:
    return re.sub(r"(?m)^\*\*Source:\*\*.*$", "", s).strip()


def parse_markdown(path: Path) -> list[dict]:
    text = _clean(path.read_text(encoding="utf-8"))
    units: list[dict] = []

    heads = list(HEADING_RE.finditer(text))
    for i, m in enumerate(heads):
        title = _strip_md(_clean(m.group(1)))
        low = title.lower()
        if re.search(r"[\u0900-\u097F]", title):
            # Skip decorative Sanskrit heading duplicate at file top.
            continue
        if any(
            skip in low
            for skip in (
                "maṇḍūkya upaniṣad",
                "textual architecture",
                "translation note",
                "appendix: philosophical architecture",
            )
        ):
            continue

        start = m.end()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        block = _clean(text[start:end])
        if not block:
            continue

        source_match = re.search(r"(?m)^\*\*Source:\*\*\s*(.+?)\s*$", block)
        source = _strip_md(source_match.group(1)) if source_match else ""

        fields = _extract_subsections(block)
        sanskrit = fields.get("devanagari", "") or fields.get("devanagari_traditional_chinese", "")
        iast = fields.get("iast", "")
        translation = fields.get("pratibha_translation", "") or fields.get("translation", "")
        commentary = fields.get("pratibha_commentary", "") or fields.get("commentary", "")
        key_terms = fields.get("key_terms", "")
        resonances = fields.get("cross_tradition_resonance", "") or fields.get("cross_tradition_resonances", "")
        karika = fields.get("karika_resonances", "") or fields.get("karika_resonances_agama_prakarana_i_1_2", "")
        practice = fields.get("practice_abhyasa", "") or fields.get("practice_abhyasa_", "") or fields.get("practice", "")

        if not translation:
            fallback = _strip_source_line(block)
            paras = [p.strip() for p in fallback.split("\n\n") if p.strip()]
            if paras:
                translation = _strip_md(re.sub(r"(?m)^###\s+", "", paras[0]).strip())
                if len(paras) > 1 and not commentary:
                    commentary = _strip_md("\n\n".join(paras[1:3]))

        if not translation:
            continue

        long_parts: list[str] = []
        if commentary:
            long_parts.append(commentary)
        if key_terms:
            long_parts.append(f"Key Terms:\n\n{key_terms}")
        if karika:
            long_parts.append(f"Karika Resonances:\n\n{karika}")
        if resonances:
            long_parts.append(f"Cross-Tradition Resonances:\n\n{resonances}")
        long_commentary = "\n\n".join(p.strip() for p in long_parts if p.strip())

        unit_num = len(units) + 1
        units.append(
            {
                "sutra_id": f"MUK_{unit_num:03d}",
                "collection": "Mandukya Upanishad and Gaudapada Karika",
                "section": "teaching_passage",
                "title": title,
                "sanskrit": sanskrit,
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
                "themes": _themes(title, translation, commentary, key_terms, resonances, karika),
                "source": source,
            }
        )
    return units


def main() -> int:
    ap = argparse.ArgumentParser(description="Convert Mandukya markdown to YAML files.")
    ap.add_argument("input_md", type=Path)
    ap.add_argument("output_dir", type=Path)
    args = ap.parse_args()

    records = parse_markdown(args.input_md)
    if args.output_dir.exists():
        shutil.rmtree(args.output_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for rec in records:
        idx = rec["sutra_id"].split("_")[-1]
        out = args.output_dir / f"mandukya_{idx}.yml"
        out.write_text(
            yaml.safe_dump(rec, allow_unicode=True, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )

    print(f"Wrote {len(records)} YAML files to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
