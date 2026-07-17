#!/usr/bin/env python3
"""
Parse a Pratibha 7-layer markdown pilot into intermediate YAML units.

Generic version used for the Vajrayāna gap-fill collections (Heart Sūtra,
Nāgārjuna MMK, Śāntideva Bodhicaryāvatāra, Tilopa Mahāmudrā). Mirrors the
existing per-collection md_to_yaml scripts (milarepa/heraclitus/chandogya) but
takes the collection name, output slug, and sutra_id prefix as arguments so one
script handles all four texts.

Output: data/yaml/<slug>/<slug>_<sutra_id>.yml  (intermediate form consumed by
scripts/canonicalize_texts.py / the promote script).

Usage:
  python scripts/vajrayana_pratibha_md_to_yaml.py <input_md> <output_dir> \
      --collection "Heart Sutra" --slug heart_sutra --prefix HS
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
        if line.startswith("Pratibha corpus entry") or line.startswith("# Pratibha —"):
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


def _section_from_source(source: str, collection: str) -> str:
    src = re.sub(r"\*+", "", source)
    m = re.search(r"Ch(?:apter)?\.?\s+([IVXLC\d]+)", src)
    if m:
        return f"Chapter {m.group(1).upper()}"
    m = re.search(r"([IVXLC]+)\.(\d+)", src)  # e.g. MMK 24.8
    if m:
        return f"{m.group(1)}.{m.group(2)}"
    return "teaching_passage"


def parse_markdown(path: Path, collection: str, prefix: str) -> list[dict]:
    ref_re = re.compile(rf"{re.escape(prefix)}_[A-Z0-9_]+")
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

        rm = ref_re.search(re.sub(r"\*+", "", source))
        sutra_id = rm.group(0).upper() if rm else f"{prefix.upper()}_PILOT_{len(units) + 1:03d}"

        units.append(
            {
                "sutra_id": sutra_id,
                "collection": collection,
                "section": _section_from_source(source, collection),
                "title": title,
                "anchor_translation": body,
                "sanskrit": original,
                "transliteration": iast,
                "translation": _clean(translation),
                "commentary": "\n\n".join(p.strip() for p in long_parts if p.strip()),
                "abhyasa": practice,
                "source": source,
                "source_reference": source,
                "editorial_maturity": "strong_draft",
                "editorial_score": 78,
            }
        )
    return units


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input_md", type=Path)
    ap.add_argument("output_dir", type=Path)
    ap.add_argument("--collection", required=True)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--prefix", required=True)
    ap.add_argument(
        "--drop-anchor",
        action="store_true",
        help="Drop the plain-English body gloss (anchor_translation). Use for "
        "original-rendering collections (orange license) so no misleading "
        "'Public-domain anchor' appendix is generated.",
    )
    args = ap.parse_args()

    records = parse_markdown(args.input_md, args.collection, args.prefix)
    if args.drop_anchor:
        for rec in records:
            rec["anchor_translation"] = ""
    if args.output_dir.exists():
        shutil.rmtree(args.output_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for rec in records:
        sid = rec["sutra_id"].lower()
        out = args.output_dir / f"{args.slug}_{sid}.yml"
        out.write_text(
            yaml.safe_dump(rec, allow_unicode=True, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )

    print(f"Wrote {len(records)} YAML files to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
