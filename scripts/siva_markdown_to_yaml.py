#!/usr/bin/env python3
"""
Convert a long-form Shiva Sutra markdown manuscript into per-sutra YAML files.

Expected section shape:
  ## Śiva Sūtra I.1
  ### Devanāgarī
  ...
  ### IAST
  ...
  ### Pratibhā Translation
  ...
  ### Pratibhā Commentary
  ...
  ### Key Words / Terms
  - ...
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml


CHAPTER_LABEL = {
    "I": "Śāmbhavopāya",
    "II": "Śāktopāya",
    "III": "Āṇavopāya",
}


def clean_block(text: str) -> str:
    # Normalize spacing and strip horizontal-rule separators.
    t = text.replace("\r\n", "\n")
    lines = [ln.strip() for ln in t.splitlines()]
    lines = [ln for ln in lines if ln != "---"]
    t = "\n".join(lines).strip()
    t = re.sub(r"\n{3,}", "\n\n", t).strip()
    return t


def extract_heading_block(section: str, heading: str) -> str:
    pattern = rf"^###\s+{re.escape(heading)}\s*$"
    m = re.search(pattern, section, flags=re.MULTILINE)
    if not m:
        return ""
    start = m.end()
    tail = section[start:]
    n = re.search(r"^###\s+", tail, flags=re.MULTILINE)
    block = tail[: n.start()] if n else tail
    return clean_block(block)


def normalize_translation(block: str) -> str:
    b = block.strip()
    b = b.replace("**", "").replace("__", "").strip()
    b = re.sub(r"\s*---\s*$", "", b).strip()
    return b


def normalize_iast(block: str) -> str:
    b = block.strip()
    b = b.replace("_", "").replace("`", "").replace("*", "").strip()
    b = re.sub(r"\s*---\s*$", "", b).strip()
    return b


def parse_keywords(block: str) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for line in block.splitlines():
        ln = line.strip()
        if not ln.startswith("-"):
            continue
        ln = ln[1:].strip()
        parts = re.split(r"\s+—\s+", ln, maxsplit=1)
        if len(parts) == 2:
            term, meaning = parts
        else:
            term, meaning = ln, ""
        out.append({"term": term.strip(" *"), "meaning": re.sub(r"\s*---\s*$", "", meaning.strip())})
    return out


def parse_sutra_sections(markdown: str) -> list[dict[str, Any]]:
    # Capture all "## Śiva Sūtra I.1" style headers.
    rx = re.compile(r"^##\s+Śiva Sūtra\s+([IVX]+)\.(\d+)\s*$", flags=re.MULTILINE)
    hits = list(rx.finditer(markdown))
    out: list[dict[str, Any]] = []
    for i, hit in enumerate(hits):
        chap = hit.group(1).strip()
        num = int(hit.group(2))
        start = hit.end()
        end = hits[i + 1].start() if i + 1 < len(hits) else len(markdown)
        section = markdown[start:end]

        devanagari = extract_heading_block(section, "Devanāgarī")
        iast = normalize_iast(extract_heading_block(section, "IAST"))
        translation = normalize_translation(extract_heading_block(section, "Pratibhā Translation"))
        commentary = extract_heading_block(section, "Pratibhā Commentary")
        keywords_raw = extract_heading_block(section, "Key Words / Terms")
        keywords = parse_keywords(keywords_raw)

        sutra_num = f"{chap}.{num}"
        sutra_id = f"SS_{sutra_num}"
        out.append(
            {
                "sutra_id": sutra_id,
                "sutra": sutra_num,
                "title": translation or sutra_num,
                "collection": "Siva Sutra",
                "section": CHAPTER_LABEL.get(chap, f"Chapter {chap}"),
                "sanskrit": devanagari,
                "transliteration": iast.strip("_ "),
                "translation": translation,
                "commentary": commentary,
                "voice_of_siva": "",
                "abhyasa": "",
                "modes": {
                    "bhasya": "",
                    "doctrinal": "",
                    "comparative": "",
                    "sadhana": "",
                },
                "glossary": keywords,
            }
        )
    return out


def dump_yaml_records(records: list[dict[str, Any]], out_dir: Path) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    # Clear previous generated files in this style.
    for p in out_dir.glob("SS_*.yaml"):
        p.unlink()

    for rec in records:
        sid = str(rec["sutra_id"]).replace("SS_", "")
        path = out_dir / f"SS_{sid}.yaml"
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(rec, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120)
    return len(records)


def main() -> int:
    ap = argparse.ArgumentParser(description="Split a Shiva Sutra markdown manuscript into per-sutra YAML files.")
    ap.add_argument("--source", required=True, help="Path to manuscript markdown file")
    ap.add_argument("--out-dir", default="data/yaml/siva_sutra", help="Output directory for SS_*.yaml")
    args = ap.parse_args()

    src = Path(args.source)
    if not src.exists():
        print(f"Source not found: {src}")
        return 1
    text = src.read_text(encoding="utf-8", errors="replace")
    records = parse_sutra_sections(text)
    if not records:
        print("No sutra sections found.")
        return 2
    n = dump_yaml_records(records, Path(args.out_dir))
    print(f"Wrote {n} sutra YAML files to {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

