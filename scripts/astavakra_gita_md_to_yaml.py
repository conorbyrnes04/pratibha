#!/usr/bin/env python3
"""
Parse Aṣṭāvakra Gītā markdown-like source into structured YAML verse files.

Usage:
  python scripts/astavakra_gita_md_to_yaml.py <input_path> <output_dir>
"""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path
from typing import Any

import yaml


VERSE_RE = re.compile(r"^###\s+(\d+\.\d+)\s*$", re.MULTILINE)
BOLD_HEADING_RE = re.compile(r"^\*\*([^*]+)\*\*\s*$", re.MULTILINE)
H3_RE = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)
RANGE_RE = re.compile(r"\b(\d+)\.(\d+)\s*[—-]\s*(\d+)\.(\d+)\b")
INLINE_VERSE_RE = re.compile(r"^\*\*(\d+\.\d+)\*\*(?:\s*[—-].*)?$", re.MULTILINE)


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


def _norm_heading(name: str) -> str:
    n = _clean(name).lower()
    n = n.replace("ā", "a").replace("ṣ", "s").replace("ṭ", "t").replace("ṛ", "r").replace("ś", "s")
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
    if "practice" in n or "abhyasa" in n:
        return "abhyasa"
    return re.sub(r"[^a-z0-9]+", "_", n).strip("_")


def _split_verse_blocks(text: str) -> list[tuple[str, str]]:
    ms = list(VERSE_RE.finditer(text))
    blocks: list[tuple[str, str]] = []
    for i, m in enumerate(ms):
        verse_id = m.group(1)
        start = m.end()
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        block = text[start:end].strip()
        blocks.append((verse_id, block))
    return blocks


def _split_h3_blocks(text: str) -> list[tuple[str, str]]:
    ms = list(H3_RE.finditer(text))
    blocks: list[tuple[str, str]] = []
    for i, m in enumerate(ms):
        heading = m.group(1).strip()
        start = m.end()
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        blocks.append((heading, text[start:end].strip()))
    return blocks


def _split_inline_verse_blocks(text: str) -> list[tuple[str, str]]:
    ms = list(INLINE_VERSE_RE.finditer(text))
    out: list[tuple[str, str]] = []
    for i, m in enumerate(ms):
        verse_id = m.group(1)
        start = m.end()
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        out.append((verse_id, text[start:end].strip()))
    return out


def _parse_sections(block: str) -> dict[str, str]:
    out: dict[str, str] = {}
    hs = list(BOLD_HEADING_RE.finditer(block))
    if not hs:
        return out
    for i, h in enumerate(hs):
        key = _norm_heading(h.group(1))
        start = h.end()
        end = hs[i + 1].start() if i + 1 < len(hs) else len(block)
        body = _clean(block[start:end])
        if body:
            out[key] = body
    return out


def _strip_md(s: str) -> str:
    s = re.sub(r"^##\s+.*$", "", s, flags=re.MULTILINE)
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"\*([^*]+)\*", r"\1", s)
    s = re.sub(r"^[-•]\s+", "", s, flags=re.MULTILINE)
    return _clean(s)


def _short_translation(text: str, limit: int = 190) -> str:
    t = _strip_md(text)
    if not t:
        return ""
    first = re.split(r"(?<=[.!?])\s+", t)[0].strip()
    if len(first) <= limit:
        return first
    return first[: limit - 3].rstrip() + "..."


def _parse_glossary(text: str) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for ln in text.splitlines():
        m = re.match(r"^-+\s+\*\*([^*]+)\*\*\s+—\s+(.+)$", ln.strip())
        if m:
            out.append({"term": m.group(1).strip(), "definition": m.group(2).strip()})
    return out


def _infer_themes(*parts: str) -> list[str]:
    blob = " ".join(parts).lower()
    pairs = [
        ("nonduality", ("non-dual", "nonduality", "advaita", "oneness", "duality")),
        ("witness", ("witness", "sakshin", "seer", "draṣṭā", "drasta")),
        ("liberation", ("mukti", "moksha", "liberation", "free", "bondage")),
        ("detachment", ("vairagya", "detachment", "desireless", "asaṅga", "asanga")),
        ("practice", ("practice", "abhyasa", "samadhi", "meditation")),
    ]
    out: list[str] = []
    for theme, ws in pairs:
        if any(w in blob for w in ws):
            out.append(theme)
    return out[:6]


def _make_record(verse_id: str, sections: dict[str, str]) -> dict[str, Any] | None:
    full_translation = sections.get("translation", "")
    translation = _short_translation(full_translation)
    # Skip summary-only pseudo headings without translation content.
    if not translation:
        return None

    commentary_parts: list[str] = []
    if full_translation and _clean(full_translation) != translation:
        commentary_parts.append("Extended Translation:\n" + _clean(full_translation))
    if sections.get("commentary"):
        commentary_parts.append(sections["commentary"])
    if sections.get("cross_tradition"):
        commentary_parts.append("Cross-Tradition Resonance:\n" + sections["cross_tradition"])
    commentary = "\n\n".join(commentary_parts).strip()
    abhyasa = sections.get("abhyasa", "")
    sid = "ASG_" + verse_id.replace(".", "_")

    return {
        "sutra_id": sid,
        "collection": "Astavakra Gita",
        "section": "verse",
        "title": f"Verse {verse_id}",
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
        "themes": _infer_themes(translation, commentary, abhyasa),
    }


def _first_quote_line(s: str) -> str:
    for ln in s.splitlines():
        t = ln.strip()
        if not t:
            continue
        if t.startswith('"') and t.endswith('"') and len(t) > 4:
            return t.strip('"').strip()
    return ""


def _make_inline_record(verse_id: str, block: str) -> dict[str, Any] | None:
    sections = _parse_sections(block)
    # Prefer explicit translated section; fallback to first quoted line.
    full_translation = sections.get("translation", "") or _first_quote_line(block)
    translation = _short_translation(full_translation)
    if not translation:
        return None

    commentary_parts: list[str] = []
    clean_block = _strip_md(block)
    if full_translation and _clean(full_translation) != translation:
        commentary_parts.append("Extended Translation:\n" + _clean(full_translation))
    if sections.get("commentary"):
        commentary_parts.append(sections["commentary"])
    elif clean_block:
        commentary_parts.append(clean_block)
    if sections.get("cross_tradition"):
        commentary_parts.append("Cross-Tradition Resonance:\n" + sections["cross_tradition"])
    commentary = "\n\n".join([p for p in commentary_parts if p]).strip()
    abhyasa = sections.get("abhyasa", "")

    return {
        "sutra_id": "ASG_" + verse_id.replace(".", "_"),
        "collection": "Astavakra Gita",
        "section": "verse",
        "title": f"Verse {verse_id}",
        "sanskrit": sections.get("devanagari", ""),
        "transliteration": sections.get("iast", ""),
        "translation": translation,
        "commentary": commentary,
        "voice_of_siva": "",
        "abhyasa": abhyasa,
        "modes": {"bhasya": "", "doctrinal": "", "comparative": "", "sadhana": abhyasa},
        "glossary": _parse_glossary(sections.get("key_terms", "")),
        "themes": _infer_themes(translation, commentary, abhyasa),
    }


def _is_summary_heading(heading: str) -> bool:
    h = heading.lower()
    return bool(
        RANGE_RE.search(heading)
        or "key verses" in h
        or "selected" in h
        or ("chapters" in h and re.search(r"\d+", h))
    )


def _strip_overview_heading(text: str) -> str:
    """Remove leading 'Overview' heading from chapter-summary blocks."""
    t = _strip_md(text)
    if not t:
        return t
    lines = t.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and lines[0].strip().lower() == "overview":
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines.pop(0)
        t = "\n".join(lines).strip()
    return t or _strip_md(text)


def _summary_unit_id(heading: str) -> str:
    m = RANGE_RE.search(heading)
    if m:
        a, b, c, d = m.groups()
        return f"ASG_SUM_{int(a):02d}_{int(b):02d}_{int(c):02d}_{int(d):02d}"
    key = re.sub(r"[^a-z0-9]+", "_", heading.lower()).strip("_")
    return f"ASG_SUM_{key[:40] or 'section'}"


def _make_summary_record(heading: str, block: str) -> dict[str, Any] | None:
    body = _strip_overview_heading(block)
    if len(body) < 140:
        return None
    translation = _short_translation(body)
    if not translation:
        return None
    title = _strip_md(heading)
    abhyasa = ""
    if "practice" in block.lower():
        # Extract first practice paragraph if present (skip generic stubs on summaries).
        m = re.search(r"Practice.*?\n(.+?)(?:\n\n|$)", block, flags=re.IGNORECASE | re.DOTALL)
        if m:
            candidate = _clean(m.group(1))
            if candidate and "read this passage slowly three times" not in candidate.lower():
                abhyasa = candidate
    return {
        "sutra_id": _summary_unit_id(heading),
        "collection": "Astavakra Gita",
        "section": "chapter_summary",
        "title": title,
        "sanskrit": "",
        "transliteration": "",
        "translation": translation,
        "commentary": body,
        "voice_of_siva": "",
        "abhyasa": abhyasa,
        "modes": {
            "bhasya": "",
            "doctrinal": "",
            "comparative": "",
            "sadhana": abhyasa,
        },
        "glossary": [],
        "themes": _infer_themes(translation, body, abhyasa),
    }


def parse_file(input_path: Path) -> list[dict[str, Any]]:
    text = input_path.read_text(encoding="utf-8", errors="replace")
    out: list[dict[str, Any]] = []
    for verse_id, block in _split_verse_blocks(text):
        sections = _parse_sections(block)
        rec = _make_record(verse_id, sections)
        if rec is not None:
            out.append(rec)
    # Parse inline verse markers used in "selected verse" sections.
    for verse_id, block in _split_inline_verse_blocks(text):
        rec = _make_inline_record(verse_id, block)
        if rec is not None:
            out.append(rec)
    # Add summary clusters to improve coverage of condensed chapter ranges.
    for heading, block in _split_h3_blocks(text):
        if re.fullmatch(r"\d+\.\d+", heading.strip()):
            continue
        if not _is_summary_heading(heading):
            continue
        rec = _make_summary_record(heading, block)
        if rec is not None:
            out.append(rec)
    # Dedupe by sutra_id and keep deterministic ordering.
    dedup: dict[str, dict[str, Any]] = {}
    for r in out:
        dedup[str(r["sutra_id"])] = r
    out = [dedup[k] for k in sorted(dedup.keys())]
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Parse Aṣṭāvakra Gītā markdown-like text into YAML verse files.")
    ap.add_argument("input_path", type=Path)
    ap.add_argument("output_dir", type=Path)
    args = ap.parse_args()

    records = parse_file(args.input_path)
    if args.output_dir.exists():
        shutil.rmtree(args.output_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for r in records:
        out = args.output_dir / f"{str(r['sutra_id']).lower()}.yml"
        out.write_text(
            yaml.safe_dump(r, allow_unicode=True, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )
    print(f"Wrote {len(records)} YAML files to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
