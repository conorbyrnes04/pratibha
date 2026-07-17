#!/usr/bin/env python3
"""
Parse Pratibha markdown for Heraclitus pilot fragments into YAML units.

Updates data/yaml/fragments/fragment_XXX.yml by HFR_P### id (does not wipe the directory).

Usage:
  python scripts/heraclitus_pratibha_md_to_yaml.py <input_md> <output_dir>
"""

from __future__ import annotations

import argparse
import re
import unicodedata
from pathlib import Path

import yaml

HEADING_RE = re.compile(r"(?m)^##\s+(.+?)\s*$")
SUBHEADING_RE = re.compile(r"(?m)^###\s+(.+?)\s*$")
HFR_REF_RE = re.compile(r"HFR_P\d{3}", re.I)


def _clean(s: str) -> str:
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    lines: list[str] = []
    for raw in s.split("\n"):
        line = re.sub(r"[ \t]+", " ", raw).rstrip()
        if re.match(r"^\s*---+\s*$", line):
            continue
        if "Pratibha corpus entry" in line or "Pratibha — Heraclitus" in line:
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


def _parse_refs(source: str) -> str:
    source = re.sub(r"\*+", "", source)
    m = HFR_REF_RE.search(source)
    return m.group(0).upper() if m else ""


def _frag_num(sutra_id: str) -> int:
    m = re.search(r"HFR_P(\d+)", sutra_id, re.I)
    return int(m.group(1)) if m else 0


def _themes(*parts: str) -> list[str]:
    blob = _slug_ascii(" ".join(parts))
    seeds = [
        "logos",
        "fire",
        "river",
        "harmony",
        "soul",
        "war",
        "change",
        "nature",
        "knowledge",
        "opposition",
        "measure",
        "becoming",
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
        original = fields.get("original", "")
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

        sutra_id = _parse_refs(source) or f"HFR_PILOT_{len(units) + 1:03d}"
        frag_n = _frag_num(sutra_id)

        units.append(
            {
                "sutra_id": sutra_id,
                "collection": "Heraclitus Fragments",
                "section": f"Fragment {frag_n}" if frag_n else "teaching_passage",
                "title": title,
                "anchor_translation": body,
                "sanskrit": original,
                "transliteration": iast,
                "translation": _clean(translation),
                "commentary": "\n\n".join(p.strip() for p in long_parts if p.strip()),
                "abhyasa": practice,
                "themes": _themes(title, translation, commentary, key_terms),
                "source": source or f"Heraclitus, Patrick (1889), {sutra_id}",
                "editorial_maturity": "strong_draft",
                "editorial_score": 72,
                "source_reference": source,
            }
        )
    return units


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input_md", type=Path)
    ap.add_argument("output_dir", type=Path)
    args = ap.parse_args()

    records = parse_markdown(args.input_md)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for rec in records:
        frag_n = _frag_num(rec["sutra_id"])
        if not frag_n:
            continue
        out = args.output_dir / f"fragment_{frag_n:03d}.yml"
        out.write_text(
            yaml.safe_dump(rec, allow_unicode=True, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )

    print(f"Wrote {len(records)} YAML files to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
