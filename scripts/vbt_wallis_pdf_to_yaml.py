#!/usr/bin/env python3
"""
Parse Christopher Wallis VBT PDF into 112 Yukti YAML files.

Usage:
  python scripts/vbt_wallis_pdf_to_yaml.py \
    "data/raw_texts/VBT+translation+WALLIS-2.pdf" \
    "data/yaml/vbt_translation_wallis_2"
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml
from pdfminer.high_level import extract_text


MIN_YUKTI = 1
MAX_YUKTI = 112
FIRST_VERSE = 24


SKIP_PREFIXES = (
    "this verse",
    "the practice here",
    "copyright",
    "apocryphal",
    "the blessed goddess said",
    "thus, o goddess",
    "village, kingdom, city",
    "o goddess, what is the point",
    "having spoken thus",
    "for the kashmir shaiva",
)


def _clean_ws(s: str) -> str:
    s = s.replace("\r", "\n").replace("\f", "\n")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def _clean_block(s: str) -> str:
    s = _clean_ws(s)
    # Drop lone footnote/page numbers.
    s = re.sub(r"(?m)^\s*\d{1,3}\s*$", "", s)
    s = re.sub(r"\n{2,}", "\n\n", s).strip()
    return s


def _valid_candidate(s: str) -> bool:
    if not s:
        return False
    ss = s.strip().lower()
    if len(ss) < 40:
        return False
    if any(ss.startswith(p) for p in SKIP_PREFIXES):
        return False
    return True


def _extract_labeled_yuktis(text: str) -> dict[int, str]:
    out: dict[int, str] = {}
    pattern = re.compile(
        r"YUKTI\s*#\s*(\d{1,3})(?:[a-z])?\s*(.*?)(?=(?:YUKTI\s*#\s*\d{1,3}(?:[a-z])?)|$)",
        flags=re.IGNORECASE | re.DOTALL,
    )
    for m in pattern.finditer(text):
        idx = int(m.group(1))
        if idx < MIN_YUKTI or idx > MAX_YUKTI:
            continue
        block = _clean_block(m.group(2))
        verse_m = re.search(r"(.*?\|\|\s*\d{1,3}(?:-\d{1,3})?(?:[a-z])?)", block, flags=re.DOTALL)
        core = _clean_block(verse_m.group(1) if verse_m else block)
        if "||" not in core:
            continue
        # Ignore commentary references like "Yukti #1, because..."
        if core[:1] in {",", ".", ";", ":"}:
            continue
        if _valid_candidate(core):
            out.setdefault(idx, core)
    return out


def _extract_verse_candidates(text: str) -> dict[int, str]:
    """
    Build verse->candidate map for verses 24..135 (112 entries).
    Heuristic: pull the final paragraph before each verse marker "|| n".
    """
    out: dict[int, str] = {}
    for m in re.finditer(r"(?s)(.{30,900}?)\|\|\s*(\d{1,3})(?:[a-z])?", text):
        verse = int(m.group(2))
        if verse < FIRST_VERSE or verse > 200:
            continue
        blob = _clean_block(m.group(1))
        parts = [p.strip() for p in re.split(r"\n\s*\n", blob) if p.strip()]
        if not parts:
            continue
        cand = _clean_block(parts[-1])
        if not _valid_candidate(cand):
            continue
        if not cand.endswith(f"|| {verse}"):
            cand = f"{cand} || {verse}"
        # Keep the first plausible candidate for each verse.
        out.setdefault(verse, cand)
    return out


def _to_yaml_obj(i: int, content: str) -> dict:
    sid = f"yukti_{i:03d}"
    title = f"Yukti #{i}"
    return {
        "sutra_id": sid,
        "collection": "Vijnana Bhairava",
        "section": "meditation_technique",
        "title": title,
        "sanskrit": "",
        "transliteration": "",
        "translation": content,
        "commentary": "",
        "modes": {
            "bhasya": "",
            "doctrinal": "",
            "comparative": "",
            "sadhana": content,
        },
    }


def build_112_yuktis(text: str) -> tuple[dict[int, str], list[int]]:
    labeled = _extract_labeled_yuktis(text)
    by_verse = _extract_verse_candidates(text)

    out: dict[int, str] = {}
    missing: list[int] = []
    used_verses: set[int] = set()

    # Prefer explicit Yukti headings for the first available numbered entries.
    for i in range(MIN_YUKTI, MAX_YUKTI + 1):
        if i not in labeled:
            continue
        content = labeled[i]
        if not content.lower().startswith("yukti #"):
            content = f"YUKTI #{i}\n{content}"
        out[i] = content
        vm = re.search(r"\|\|\s*(\d{1,3})", content)
        if vm:
            used_verses.add(int(vm.group(1)))

    # Fill remaining yuktis from ascending verse candidates after the explicit range.
    explicit_max_verse = max(used_verses) if used_verses else (FIRST_VERSE - 1)
    tail_verses = [
        v for v in sorted(by_verse.keys())
        if v > explicit_max_verse and v not in used_verses
    ]
    tail_iter = iter(tail_verses)

    for i in range(MIN_YUKTI, MAX_YUKTI + 1):
        if i in out:
            continue
        v = next(tail_iter, None)
        if v is None:
            missing.append(i)
            out[i] = f"YUKTI #{i}\n[Missing extraction; please review source PDF manually.]"
            continue
        out[i] = f"YUKTI #{i}\n{by_verse[v]}"
    return out, missing


def main() -> int:
    ap = argparse.ArgumentParser(description="Convert VBT Wallis PDF to 112 Yukti YAML files.")
    ap.add_argument("pdf_path", type=Path)
    ap.add_argument("output_dir", type=Path)
    args = ap.parse_args()

    text = _clean_ws(extract_text(str(args.pdf_path)))
    yuktis, missing = build_112_yuktis(text)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for i in range(MIN_YUKTI, MAX_YUKTI + 1):
        data = _to_yaml_obj(i, yuktis[i])
        out = args.output_dir / f"yukti_{i:03d}.yaml"
        out.write_text(
            yaml.safe_dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )

    print(f"Wrote {MAX_YUKTI} YAML files to {args.output_dir}")
    if missing:
        print(f"Missing auto-extraction for {len(missing)} yuktis: {missing[:12]}{'...' if len(missing) > 12 else ''}")
    else:
        print("All 112 yuktis auto-extracted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

