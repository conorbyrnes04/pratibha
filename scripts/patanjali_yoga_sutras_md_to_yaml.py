#!/usr/bin/env python3
"""Parse Patañjali Yoga Sūtras Pratibha MD into canonical YAML units.

Usage:
  python scripts/patanjali_yoga_sutras_md_to_yaml.py data/pratibha_md/patanjali_yoga_sutras.md data/yaml/patanjali_yoga_sutras
  python scripts/canonicalize_texts.py
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
    if "devanagari" in n:
        return "devanagari"
    if "iast" in n:
        return "iast"
    if "pratibha translation" in n:
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
    for i, m in enumerate(matches):
        title = m.group(1).strip()
        if title.startswith("#"):
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


def _sutra_ref(source: str) -> tuple[int, int]:
    m = re.search(r"Yoga\s+Sūtras\s+(\d+)\.(\d+)", source)
    if not m:
        return 0, 0
    return int(m.group(1)), int(m.group(2))


def _pada_name(pada: int) -> str:
    return {1: "Samādhi", 2: "Sādhana", 3: "Vibhūti", 4: "Kaivalya"}.get(pada, "")


def _infer_themes(*parts: str) -> list[str]:
    blob = " ".join(parts).lower()
    pairs = [
        ("samadhi", ("samādhi", "samadhi", "contemplation", "dhyana", "dharana")),
        ("practice", ("abhyasa", "sadhana", "practice", "discipline", "yama", "niyama")),
        ("mind", ("citta", "vṛtti", "vrtti", "mental", "thought")),
        ("liberation", ("kaivalya", "mokṣa", "moksa", "liberation", "freedom")),
        ("self", ("puruṣa", "purusa", "seer", "witness", "atman")),
        ("nature", ("prakṛti", "prakrti", "gunas", "nature")),
        ("knowledge", ("pramana", "pramāṇa", "knowledge", "inference")),
        ("ignorance", ("avidya", "avidyā", "ignorance", "misapprehension")),
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
    records_by_key: dict[tuple[int, int], dict[str, Any]] = {}
    units = _split_units(md_text)
    for title, block in units:
        sm = SOURCE_RE.search(block)
        source = sm.group(1).strip() if sm else ""
        pada, num = _sutra_ref(source)
        if not pada or not num:
            continue
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
        sid = f"YS_{pada}_{num:02d}"

        appendixes: list[dict[str, str]] = []
        if body:
            if pada == 1 or (pada == 2 and num <= 30):
                label = "Manilal Nabhubhai Dvivedi (1890, PD anchor)"
            else:
                label = "Swami Satchidananda (1978, attributed aphorism)"
            appendixes.append({"commentator": label, "text": body})

        themes = _infer_themes(title, translation, commentary, practice, source)

        rec = {
            "sutra_id": sid,
            "collection": "Patañjali Yoga Sūtras",
            "section": f"{_pada_name(pada)} Pāda",
            "title": title,
            "sanskrit": layers.get("devanagari", ""),
            "transliteration": layers.get("iast", ""),
            "translation": translation,
            "commentary": commentary,
            "voice_of_siva": _insight(layers.get("commentary", "")),
            "abhyasa": practice,
            "themes": themes,
            "source_reference": source,
            "reference": f"{pada}.{num} ({_pada_name(pada)} Pāda)",
            "appendixes": appendixes,
            "editorial_maturity": "strong_draft",
            "quality_score_unit": 0,
        }
        records_by_key[(pada, num)] = rec
    records = list(records_by_key.values())
    records.sort(key=lambda r: _sutra_ref(r.get("source_reference", "")))
    return records


def main() -> int:
    ap = argparse.ArgumentParser(description="Parse Patañjali Pratibha MD into canonical YAML.")
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
        out = args.output_dir / f"{r['sutra_id'].lower()}.yml"
        out.write_text(
            yaml.safe_dump(r, allow_unicode=True, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )
    print(f"Wrote {len(records)} YAML units to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
