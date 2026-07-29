#!/usr/bin/env python3
"""Verify/sync Meister Eckhart MHG originals (12 units).

MHG for *Von Abegescheidenheit* is already present in pratibha_layers.original
on all 12 units (Latin-script historical source). This script:

  - Confirms each unit has a non-placeholder MHG original body
  - Sets layer_provenance to the PD Pfeiffer 1857 registry note
    (local OCR: data/raw_texts/pd/german/pfeiffer_eckhart_1857_ocr.txt).
    Orthography of the curated text follows the common DW/Quint digital
    conventions already in the units; we do NOT re-OCR-replace from the
    messy Google OCR (honest gap vs wrong text).
  - Syncs data/canonical/index.jsonl from YAML

  python scripts/restore_eckhart_mhg.py            # preview
  python scripts/restore_eckhart_mhg.py --write
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "data" / "canonical" / "meister_eckhart"
MAIN_INDEX = ROOT / "data" / "canonical" / "index.jsonl"
PFEIFFER = ROOT / "data" / "raw_texts" / "pd" / "german" / "pfeiffer_eckhart_1857_ocr.txt"

PROV = (
    "mhg: Von Abegescheidenheit — curated Middle High German already in unit; "
    "PD registry Franz Pfeiffer, Deutsche Mystiker des vierzehnten Jahrhunderts "
    "Bd. 2 (1857), local OCR at data/raw_texts/pd/german/pfeiffer_eckhart_1857_ocr.txt. "
    "Orthography follows common Quint DW digital conventions; not a fresh OCR "
    "substitution from the noisy Google scan."
)

MHG_MARK = re.compile(
    r"abegescheiden|daz |diu |wan |sô |niht |ûf |ûz |Ich hân|Ich lobe|Nû |Die meister|Die lêrære|Wer nû|Ein meister",
    re.I,
)
PLACEHOLDER = re.compile(r"source-language basis", re.I)


def layer_body(unit: dict[str, Any], kind: str) -> str:
    for L in unit.get("pratibha_layers") or []:
        if isinstance(L, dict) and L.get("kind") == kind:
            return str(L.get("body") or "")
    return ""


def is_mhg(text: str) -> bool:
    t = (text or "").strip()
    if not t or PLACEHOLDER.search(t):
        return False
    return bool(MHG_MARK.search(t)) and len(t) > 40


def upsert_prov(unit: dict[str, Any]) -> None:
    layers = unit.get("pratibha_layers") or []
    for L in layers:
        if isinstance(L, dict) and L.get("kind") == "original":
            L["label"] = L.get("label") or "Original (Middle High German)"
            if "Middle High German" not in str(L.get("label")):
                L["label"] = "Original (Middle High German)"
            L["layer_provenance"] = PROV
    lp = unit.get("layer_provenance")
    if not isinstance(lp, dict):
        unit["layer_provenance"] = {"original": PROV}
    else:
        lp["original"] = PROV
    top = unit.get("provenance")
    if isinstance(top, dict):
        ref = str(top.get("source_reference") or "")
        tip = "Pfeiffer 1857 PD MHG registry; curated Von Abegescheidenheit MHG in Original layer."
        if "Pfeiffer" not in ref:
            top["source_reference"] = f"{ref}; {tip}".strip("; ") if ref else tip


def dump_yaml(unit: dict[str, Any]) -> str:
    return yaml.safe_dump(
        unit, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120
    )


def atomic_write(path: Path, content: str) -> None:
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        handle.write(content)
        temp = Path(handle.name)
    temp.replace(path)


def sync_index(updated: dict[str, dict[str, Any]]) -> int:
    lines = MAIN_INDEX.read_text(encoding="utf-8").splitlines(keepends=True)
    out: list[str] = []
    n = 0
    for line in lines:
        if not line.strip():
            out.append(line)
            continue
        obj = json.loads(line)
        uid = obj.get("unit_id")
        if uid in updated:
            out.append(json.dumps(updated[uid], ensure_ascii=False) + "\n")
            n += 1
        else:
            out.append(line)
    atomic_write(MAIN_INDEX, "".join(out))
    return n


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    if not PFEIFFER.is_file():
        print(f"WARN missing Pfeiffer OCR: {PFEIFFER}", file=sys.stderr)

    paths = sorted(CANON.glob("*.yml"))
    updated: dict[str, dict[str, Any]] = {}
    ok = miss = 0
    for path in paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        uid = data.get("unit_id") or path.stem
        orig = layer_body(data, "original") or (data.get("sanskrit_devanagari") or "")
        if is_mhg(orig):
            ok += 1
            print(f"OK  {uid}: MHG len={len(orig.strip())}")
            if args.write:
                # Ensure original layer carries the MHG (promote from top field if needed)
                layers = data.get("pratibha_layers") or []
                has_orig = any(
                    isinstance(L, dict) and L.get("kind") == "original" for L in layers
                )
                if not has_orig:
                    layers.insert(
                        0,
                        {
                            "kind": "original",
                            "label": "Original (Middle High German)",
                            "body": orig if orig.endswith("\n") else orig + "\n",
                        },
                    )
                    data["pratibha_layers"] = layers
                elif not is_mhg(layer_body(data, "original")) and is_mhg(
                    data.get("sanskrit_devanagari") or ""
                ):
                    for L in layers:
                        if L.get("kind") == "original":
                            L["body"] = data["sanskrit_devanagari"]
                upsert_prov(data)
                if not (data.get("sanskrit_devanagari") or "").strip():
                    data["sanskrit_devanagari"] = layer_body(data, "original")
                atomic_write(path, dump_yaml(data))
                updated[uid] = data
        else:
            miss += 1
            print(f"MISS {uid}: no MHG original (head={orig[:80]!r})")

    if args.write and updated:
        n = sync_index(updated)
        print(f"synced index.jsonl rows={n}")
    elif not args.write:
        print("dry-run (pass --write to apply provenance + index sync)")

    print(f"MHG coverage: {ok}/{ok + miss} (unmatched={miss})")
    return 0 if miss == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
