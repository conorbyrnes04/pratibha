#!/usr/bin/env python3
"""
Parse Pratibha markdown for Chāndogya Upaniṣad into YAML units.

Usage:
  python scripts/chandogya_pratibha_md_to_yaml.py <input_md> <output_dir>
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
CHU_REF_RE = re.compile(r"CHU_[A-Z0-9_]+", re.I)
SECTION_RE = re.compile(r"Ch[aā]ndogya[^,]*,\s*([IVXLC\d\.]+)", re.I)


def _clean(s: str) -> str:
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    lines: list[str] = []
    for raw in s.split("\n"):
        line = re.sub(r"[ \t]+", " ", raw).rstrip()
        if re.match(r"^\s*---+\s*$", line):
            continue
        if "Pratibha corpus entry" in line or "Pratibha — Ch" in line:
            continue
        lines.append(line)
    s = "\n".join(lines)
    return re.sub(r"\n{3,}", "\n\n", s).strip()


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


def _parse_refs(source: str, unit_num: int) -> tuple[str, str, str]:
    source = re.sub(r"\*+", "", source)
    sid = ""
    m = CHU_REF_RE.search(source)
    if m:
        sid = m.group(0).upper()
    if not sid:
        sid = f"CHU_PILOT_{unit_num:03d}"
    section_label = ""
    sec = SECTION_RE.search(source)
    if sec:
        section_label = f"Chāndogya Upaniṣad {sec.group(1).strip()}"
    return sid, section_label, source


def _themes(*parts: str) -> list[str]:
    blob = _slug_ascii(" ".join(parts))
    seeds = [
        "atman",
        "brahman",
        "self",
        "identity",
        "consciousness",
        "meditation",
        "knowledge",
        "sacrifice",
        "death",
        "sleep",
        "creation",
        "teacher",
        "student",
        "desire",
        "truth",
        "soul",
    ]
    return [t for t in seeds if re.search(rf"\b{re.escape(t)}\b", blob)][:8]


def parse_markdown(path: Path) -> list[dict]:
    text = _clean(path.read_text(encoding="utf-8"))
    units: list[dict] = []

    heads = list(HEADING_RE.finditer(text))
    for i, m in enumerate(heads):
        title = _clean(m.group(1))
        if title.startswith("Pratibha") or title.startswith("Corpus entry"):
            continue
        start = m.end()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        block = _clean(text[start:end])
        if not block:
            continue

        source_match = re.search(r"(?m)^\*\*Source:\*\*\s*(.+?)\s*$", block)
        source = source_match.group(1).strip() if source_match else ""

        sub_start = SUBHEADING_RE.search(block)
        body = _clean(block[: sub_start.start()] if sub_start else "")
        body = re.sub(r"^\*\*Source:\*\*.*$", "", body, flags=re.M).strip()

        fields = _extract_subsections(block)
        original = fields.get("devanagari", "") or fields.get("original", "")
        iast = fields.get("iast", "")
        translation = fields.get("pratibha_translation", "") or fields.get("translation", "")
        commentary = fields.get("pratibha_commentary", "") or fields.get("commentary", "")
        key_terms = fields.get("key_terms", "")
        resonances = fields.get("cross_tradition_resonances", "")
        practice = fields.get("practice_abhyasa", "") or fields.get("practice", "")

        if not translation and not body:
            continue
        if not translation:
            translation = body

        long_parts: list[str] = []
        if commentary:
            long_parts.append(commentary)
        if key_terms:
            long_parts.append(f"Key Terms:\n\n{key_terms}")
        if resonances:
            long_parts.append(f"Cross-Tradition Resonances:\n\n{resonances}")

        unit_num = len(units) + 1
        sutra_id, section_label, _ = _parse_refs(source, unit_num)

        units.append(
            {
                "sutra_id": sutra_id,
                "collection": "Chāndogya Upaniṣad",
                "section": section_label or "teaching_passage",
                "title": title,
                "anchor_translation": body,
                "sanskrit": original,
                "transliteration": iast,
                "translation": _clean(translation),
                "commentary": "\n\n".join(p.strip() for p in long_parts if p.strip()),
                "abhyasa": practice,
                "themes": _themes(title, translation, commentary, key_terms),
                "source": source or "Chāndogya Upaniṣad (Müller SBE 1, 1879)",
                "editorial_maturity": "strong_draft",
                "editorial_score": 70,
            }
        )
    return units


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input_md", type=Path)
    ap.add_argument("output_dir", type=Path)
    args = ap.parse_args()

    records = parse_markdown(args.input_md)
    if args.output_dir.exists():
        shutil.rmtree(args.output_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for rec in records:
        sid = rec["sutra_id"].lower()
        out = args.output_dir / f"chandogya_upanishad_{sid}.yml"
        out.write_text(
            yaml.safe_dump(rec, allow_unicode=True, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )

    print(f"Wrote {len(records)} units -> {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
