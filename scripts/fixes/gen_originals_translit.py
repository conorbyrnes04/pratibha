#!/usr/bin/env python3
"""Generate IAST->Devanagari transliteration patches for Sanskrit units that
carry verified IAST but no Devanagari script.

Deterministic, no LLM: transliterates existing (human/source-verified) IAST via
indic_transliteration. Only targets genuine Sanskrit works whose IAST is verse
text (not glossary notes or 'source-language basis' placeholders).

Emits a JSONL patch consumable by apply_canonical_patch.py.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

ROOT = Path(__file__).resolve().parents[2]
CANONICAL = ROOT / "data" / "canonical"

# Works with real, verse-level Sanskrit IAST (verified above); exclude
# shantideva (glossary-style notes) and bhagavad_gita (placeholder notes).
TARGET_WORKS = ["nagarjuna_mulamadhyamakakarika", "heart_sutra"]


def clean_iast(s: str) -> str:
    """Strip trailing provenance parentheticals like '*(Sanskrit, IAST, ...)*'."""
    s = re.split(r"\n\n\*\(", s, maxsplit=1)[0]
    s = re.sub(r"\*\([^)]*\)\*\s*$", "", s).strip()
    return s


def to_devanagari(iast: str) -> str:
    dev = transliterate(iast, sanscript.IAST, sanscript.DEVANAGARI)
    # Normalize dandas: double first so the single pass doesn't split them.
    dev = dev.replace(" // ", " ॥ ").replace("//", "॥")
    dev = dev.replace(" / ", " । ").replace("/", "।")
    return dev.strip()


def looks_like_verse_iast(s: str) -> bool:
    if not s:
        return False
    if re.search(r"source-language basis|key terms in iast|pending|not available", s, re.I):
        return False
    # Require diacritics typical of IAST verse text.
    return bool(re.search(r"[āīūṛṝḷṃḥṅñṭḍṇśṣ]", s))


def main() -> int:
    out_path = ROOT / "scratch" / "originals_translit.jsonl"
    out_path.parent.mkdir(exist_ok=True)
    records = []
    skipped = []
    for work in TARGET_WORKS:
        for path in sorted((CANONICAL / work).glob("*.yml")):
            if path.name == "_work.yml":
                continue
            d = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(d, dict):
                continue
            uid = str(d.get("unit_id"))
            raw_iast = str(d.get("sanskrit_iast") or d.get("transliteration") or "")
            existing_dev = str(d.get("sanskrit_devanagari") or d.get("sanskrit") or "")
            if re.search(r"[\u0900-\u097F]", existing_dev):
                skipped.append((uid, "already has devanagari"))
                continue
            iast = clean_iast(raw_iast)
            if not looks_like_verse_iast(iast):
                skipped.append((uid, "iast not verse-like"))
                continue
            dev = to_devanagari(iast)
            if not re.search(r"[\u0900-\u097F]", dev):
                skipped.append((uid, "transliteration produced no devanagari"))
                continue
            records.append(
                {
                    "unit_id": uid,
                    "set_fields": {
                        "sanskrit_devanagari": dev,
                        "sanskrit_iast": iast,  # drop trailing provenance note
                    },
                    "set_layers": [
                        {"kind": "original", "body": dev, "layer_provenance": "transliterated_from_iast"},
                        {"kind": "iast", "body": iast},
                    ],
                }
            )

    out_path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n", encoding="utf-8")
    print(f"wrote {len(records)} transliteration patches -> {out_path}")
    for uid, why in skipped:
        print(f"  skipped {uid}: {why}")
    for r in records[:3]:
        print(f"\n{r['unit_id']}:\n  {r['set_fields']['sanskrit_devanagari'][:90]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
