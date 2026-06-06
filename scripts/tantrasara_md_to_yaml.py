#!/usr/bin/env python3
"""Parse Tantrasāra Pratibha MD into canonical YAML units.

Usage:
  python scripts/tantrasara_md_to_yaml.py data/pratibha_md/tantrasara.md data/canonical/tantrasara
"""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path
from typing import Any

import yaml

UNIT_RE = re.compile(r"^##\s+(?!#)(.+?)\s*$", re.MULTILINE)
LAYER_RE = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)
SOURCE_RE = re.compile(r"^\*\*Source:\*\*\s*(.+?)\s*$", re.MULTILINE)
NOTE_RE = re.compile(r"^\*\(.*?\)\*\s*$", re.MULTILINE)


def _clean(s: str) -> str:
    s = (s or "").replace("\r", "\n")
    s = NOTE_RE.sub("", s)
    lines = [re.sub(r"[ \t]+", " ", ln).rstrip() for ln in s.split("\n")]
    out: list[str] = []
    blank = False
    for ln in lines:
        if ln.strip() == "---":
            continue
        if not ln.strip():
            if not blank and out:
                out.append("")
            blank = True
            continue
        out.append(ln.strip())
        blank = False
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()


def _layer_key(name: str) -> str:
    n = name.strip().lower()
    if "devanagari" in n or "original" in n:
        return "devanagari"
    if "iast" in n:
        return "iast"
    if "translation" in n:
        return "translation"
    if "commentary" in n:
        return "commentary"
    if "key term" in n:
        return "key_terms"
    if "resonance" in n:
        return "resonances"
    if "practice" in n or "abhyasa" in n:
        return "practice"
    return re.sub(r"[^a-z0-9]+", "_", n).strip("_")


def _split_units(text: str) -> list[tuple[str, str]]:
    units: list[tuple[str, str]] = []
    matches = list(UNIT_RE.finditer(text))
    skip_titles = ("glossary seeds",)
    for i, m in enumerate(matches):
        title = m.group(1).strip()
        if title.lower().startswith(skip_titles):
            continue
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        units.append((title, text[start:end].strip()))
    return units


def _parse_layers(block: str) -> tuple[str, dict[str, str]]:
    layers: dict[str, str] = {}
    heads = list(LAYER_RE.finditer(block))
    body_end = heads[0].start() if heads else len(block)
    body = block[:body_end]
    body = SOURCE_RE.sub("", body)
    body = _clean(body)
    for i, h in enumerate(heads):
        key = _layer_key(h.group(1))
        start = h.end()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(block)
        layers[key] = _clean(block[start:end])
    return body, layers


def _ahnika_ref(source: str) -> str:
    m = re.search(r"Āhnika\s+(\d+)\s*\(([^)]+)\)", source)
    if m:
        return f"{m.group(1)} ({m.group(2)})"
    m = re.search(r"Āhnika\s+(\d+)", source)
    return m.group(1) if m else ""


def _upaya_for_ahnika(source: str) -> str:
    m = re.search(r"Āhnika\s+(\d+)", source)
    if not m:
        return ""
    chapter = int(m.group(1))
    return {
        1: "",
        2: "anupāya",
        3: "śāmbhava",
        4: "śākta",
        5: "āṇava",
    }.get(chapter, "")


def _unit_type(source: str) -> str:
    if "Verse" in source:
        return "verse"
    if "Prose" in source or "Section" in source or "Upodghāta" in source:
        return "prose"
    return "unit"


def _infer_themes(*parts: str) -> list[str]:
    blob = " ".join(parts).lower()
    pairs = [
        ("consciousness", ("consciousness", "prakāśa", "prakasa", "samvit", "cit", "awareness")),
        ("sakti", ("śakti", "sakti", "energy", "power", "śaktipāta")),
        ("nonduality", ("non-dual", "nondual", "recognition", "svatantra", "freedom")),
        ("upaya", ("upāya", "upaya", "anupāya", "śāmbhava", "śākta", "āṇava")),
        ("mantra", ("mantra", "uccāra", "varṇa", "praṇava", "om")),
        ("meditation", ("dhyāna", "dhyana", "samādhi", "samadhi", "contemplat")),
        ("ignorance", ("avidyā", "avidya", "māyā", "maya", "ignorance", "bondage")),
        ("liberation", ("kaivalya", "mokṣa", "moksa", "jīvanmukti", "liberation")),
        ("practice", ("practice", "abhyasa", "bhāvanā", "bhavana")),
        ("heart", ("hṛdaya", "hrdaya", "heart", "kula")),
    ]
    out: list[str] = []
    for t, ws in pairs:
        if any(w in blob for w in ws):
            out.append(t)
    return out[:8]


def _insight(commentary: str) -> str:
    c = _clean(commentary)
    if not c:
        return ""
    first = re.split(r"(?<=[.!?])\s+", c)[0].strip()
    return first[:200]


def build_records(md_text: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    units = _split_units(md_text)
    for seq, (title, block) in enumerate(units, start=1):
        sm = SOURCE_RE.search(block)
        source = sm.group(1).strip() if sm else ""
        body, layers = _parse_layers(block)

        commentary_parts: list[str] = []
        if layers.get("commentary"):
            commentary_parts.append(layers["commentary"])
        if layers.get("key_terms"):
            commentary_parts.append("Key Terms\n\n" + layers["key_terms"])
        if layers.get("resonances"):
            commentary_parts.append("Cross-Tradition Resonances\n\n" + layers["resonances"])
        commentary = "\n\n".join(commentary_parts).strip()

        translation = layers.get("translation", "")
        practice = layers.get("practice", "")
        sid = f"TS_{seq:03d}"

        appendixes: list[dict[str, str]] = []
        if body:
            appendixes.append({"commentator": "Received translation (Śastra vault)", "text": body})

        themes = _infer_themes(title, translation, commentary, practice, source)
        upaya = _upaya_for_ahnika(source)

        rec = {
            "source_file": f"data/canonical/tantrasara/{sid.lower()}.yml",
            "source_id": sid,
            "category": "root_text",
            "work_id": "tantrasara",
            "work_title": "Tantrasāra",
            "unit_id": f"tantrasara.{sid.lower()}",
            "unit_label": title,
            "title": title,
            "unit_type": _unit_type(source),
            "sequence": seq,
            "reference": _ahnika_ref(source),
            "source_reference": source,
            "sanskrit_devanagari": layers.get("devanagari", ""),
            "sanskrit_iast": layers.get("iast", ""),
            "translation_literal": translation,
            "commentary": commentary,
            "insight": _insight(layers.get("commentary", "")),
            "practice": practice,
            "upaya": upaya,
            "themes": themes,
            "tags": sorted(set(themes + ["tantrasara", "root_text", "kashmir_shaivism", "abhinavagupta", "tantra"])),
            "editorial_maturity": "publishable",
            "quality_score": 0,
            "appendixes": appendixes,
            "provenance": {
                "collection": "Tantrasāra",
                "section": _unit_type(source),
                "original_id": sid,
                "edition": "Abhinavagupta; Śastra vault Pratibha MD (Wallis-informed)",
            },
        }
        records.append(rec)
    return records


def main() -> int:
    ap = argparse.ArgumentParser(description="Parse Tantrasāra Pratibha MD into canonical YAML.")
    ap.add_argument("input_path", type=Path)
    ap.add_argument("output_dir", type=Path)
    ap.add_argument("--clean", action="store_true", help="Remove output dir before writing.")
    args = ap.parse_args()

    md_text = args.input_path.read_text(encoding="utf-8", errors="replace")
    records = build_records(md_text)

    if args.clean and args.output_dir.exists():
        shutil.rmtree(args.output_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for r in records:
        out = args.output_dir / f"{r['source_id'].lower()}.yml"
        out.write_text(
            yaml.safe_dump(r, allow_unicode=True, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )
    print(f"Wrote {len(records)} YAML units to {args.output_dir}")
    for r in records:
        print(f"  {r['source_id']}  {r['reference']:<20}  {r['title']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
