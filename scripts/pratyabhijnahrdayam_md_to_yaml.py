#!/usr/bin/env python3
"""
Parse Pratyabhijnahrdayam markdown-like source into structured YAML sutra files.

Usage:
  python scripts/pratyabhijnahrdayam_md_to_yaml.py <input_path> <output_dir>
"""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path
from typing import Any

import yaml


SUTRA_RE = re.compile(r"^##\s*S[ūu]tra\s+(\d+)\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)


def _clean(s: str) -> str:
    s = s.replace("\r", "\n")
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in s.split("\n")]
    out: list[str] = []
    blank = False
    for ln in lines:
        if ln.startswith("---"):
            continue
        if not ln:
            if not blank:
                out.append("")
            blank = True
            continue
        out.append(ln)
        blank = False
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()


def _normalize_heading(name: str) -> str:
    n = name.strip().lower()
    n = n.replace("ā", "a").replace("ṛ", "r").replace("ś", "s").replace("ṇ", "n")
    if "devan" in n:
        return "devanagari"
    if "iast" in n:
        return "iast"
    if "translation" in n:
        return "translation"
    if "commentary" in n:
        return "commentary"
    if "key terms" in n:
        return "key_terms"
    if "cross-tradition" in n or "cross tradition" in n:
        return "cross_tradition"
    if "abhyasa" in n or "practice" in n:
        return "abhyasa"
    return re.sub(r"[^a-z0-9]+", "_", n).strip("_")


def _split_sutra_blocks(text: str) -> list[tuple[int, str]]:
    ms = list(SUTRA_RE.finditer(text))
    blocks: list[tuple[int, str]] = []
    if not ms:
        return blocks
    for i, m in enumerate(ms):
        n = int(m.group(1))
        start = m.end()
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        block = text[start:end].strip()
        # Stop before appendix/context section if present.
        appendix_start = re.search(r"^##\s+Appendix\b", block, flags=re.MULTILINE)
        if appendix_start:
            block = block[: appendix_start.start()].strip()
        blocks.append((n, block))
    return blocks


def _parse_sections(block: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    hs = list(HEADING_RE.finditer(block))
    for i, h in enumerate(hs):
        raw_name = h.group(1)
        key = _normalize_heading(raw_name)
        start = h.end()
        end = hs[i + 1].start() if i + 1 < len(hs) else len(block)
        body = _clean(block[start:end])
        if body:
            sections[key] = body
    return sections


def _parse_glossary(text: str) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for ln in text.splitlines():
        m = re.match(r"^-+\s+\*\*([^*]+)\*\*\s+—\s+(.+)$", ln.strip())
        if not m:
            continue
        term = m.group(1).strip()
        definition = m.group(2).strip()
        if term and definition:
            out.append({"term": term, "definition": definition})
    return out


def _infer_themes(*parts: str) -> list[str]:
    blob = " ".join(parts).lower()
    pairs = [
        ("recognition", ("recognition", "pratyabhijna", "pratyabhijna")),
        ("consciousness", ("consciousness", "citi", "awareness")),
        ("nonduality", ("non-dual", "nonduality", "one", "unity")),
        ("practice", ("practice", "abhyasa", "upaya", "samadhi")),
        ("self", ("self", "aham", "i-consciousness", "atman")),
    ]
    out: list[str] = []
    for t, ws in pairs:
        if any(w in blob for w in ws):
            out.append(t)
    return out[:6]


def _short_translation(text: str, limit: int = 170) -> str:
    t = _clean(text)
    if not t:
        return ""
    first = re.split(r"(?<=[.!?])\s+", t)[0].strip()
    if len(first) <= limit:
        return first
    return first[: limit - 3].rstrip() + "..."


def _make_record(sutra_n: int, sections: dict[str, str]) -> dict[str, Any]:
    full_translation = sections.get("translation", "")
    translation = _short_translation(full_translation)
    commentary_parts = []
    if full_translation and _clean(full_translation) != translation:
        commentary_parts.append("Extended Translation:\n" + _clean(full_translation))
    if sections.get("commentary"):
        commentary_parts.append(sections["commentary"])
    if sections.get("cross_tradition"):
        commentary_parts.append("Cross-Tradition Resonance:\n" + sections["cross_tradition"])
    commentary = "\n\n".join(commentary_parts).strip()
    abhyasa = sections.get("abhyasa", "")
    title = f"Sutra {sutra_n}"
    themes = _infer_themes(translation, commentary, abhyasa)
    return {
        "sutra_id": f"PHR_{sutra_n:03d}",
        "collection": "Pratyabhijnahrdayam",
        "section": "sutra",
        "title": title,
        "sanskrit": sections.get("devanagari", ""),
        "transliteration": sections.get("iast", ""),
        "translation": translation,
        "commentary": commentary,
        "voice_of_siva": "",
        "abhyasa": abhyasa,
        "modes": {
            "bhasya": "",
            "doctrinal": "",
            "comparative": "",
            "sadhana": abhyasa,
        },
        "glossary": _parse_glossary(sections.get("key_terms", "")),
        "themes": themes,
    }


def parse_text(input_path: Path) -> list[dict[str, Any]]:
    raw = input_path.read_text(encoding="utf-8", errors="replace")
    blocks = _split_sutra_blocks(raw)
    records: list[dict[str, Any]] = []
    for n, block in blocks:
        sections = _parse_sections(block)
        record = _make_record(n, sections)
        if record["translation"].strip():
            records.append(record)
    # Preserve appendix as a context unit for compare/retrieval.
    m = re.search(r"^##\s+Appendix:.*$", raw, flags=re.MULTILINE)
    if m:
        appendix = _clean(raw[m.end() :])
        if appendix:
            summary = appendix
            first = re.split(r"(?<=[.!?])\s+", appendix)
            if first:
                summary = first[0][:180]
            records.append(
                {
                    "sutra_id": "PHR_SUM_APPENDIX",
                    "collection": "Pratyabhijnahrdayam",
                    "section": "chapter_summary",
                    "title": "Appendix: Philosophical Context",
                    "sanskrit": "",
                    "transliteration": "",
                    "translation": summary,
                    "commentary": appendix,
                    "voice_of_siva": "",
                    "abhyasa": "",
                    "modes": {"bhasya": "", "doctrinal": "", "comparative": "", "sadhana": ""},
                    "glossary": [],
                    "themes": _infer_themes(summary, appendix),
                }
            )
    return records


def main() -> int:
    ap = argparse.ArgumentParser(description="Parse Pratyabhijnahrdayam source into YAML sutra files.")
    ap.add_argument("input_path", type=Path)
    ap.add_argument("output_dir", type=Path)
    args = ap.parse_args()

    records = parse_text(args.input_path)
    if args.output_dir.exists():
        shutil.rmtree(args.output_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for r in records:
        out = args.output_dir / f"{r['sutra_id'].lower()}.yml"
        out.write_text(
            yaml.safe_dump(r, allow_unicode=True, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )
    print(f"Wrote {len(records)} YAML files to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
