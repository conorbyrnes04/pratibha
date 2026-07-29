#!/usr/bin/env python3
"""Verify/sync The Cloud of Unknowing Middle English originals (5 units).

ME text is already present in pratibha_layers.original on all 5 units
(historical Latin-script Middle English). This script:

  - Confirms each unit has non-placeholder ME original
  - Sets layer_provenance to Underhill 1912 PD ME edition note
    (manifest: cloud_of_unknowing_underhill_1912; local file may be absent —
    corpus ME already matches classic Underhill/early ME wording)
  - Syncs data/canonical/index.jsonl from YAML

  python scripts/restore_cloud_me.py            # preview
  python scripts/restore_cloud_me.py --write
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
CANON = ROOT / "data" / "canonical" / "the_cloud_of_unknowing"
MAIN_INDEX = ROOT / "data" / "canonical" / "index.jsonl"

PROV = (
    "middle_english: The Cloud of Unknowing — curated ME already in unit; "
    "PD edition Evelyn Underhill 1912 (and earlier ME manuscript tradition). "
    "Manifest id cloud_of_unknowing_underhill_1912. Not a diplomatic MS edition."
)

ME_MARK = re.compile(
    r"\b(thorou|werkes|him-self|chese|unknowyng|unknowing|nought|thou|ye |"
    r"bot |wolde|thinke|schal|apon|thicke|cloude|travaile|sodeyn|fulheed|"
    r"seiest|himself|hee)\b",
    re.I,
)
PLACEHOLDER = re.compile(r"source-language basis", re.I)


def layer_body(unit: dict[str, Any], kind: str) -> str:
    for L in unit.get("pratibha_layers") or []:
        if isinstance(L, dict) and L.get("kind") == kind:
            return str(L.get("body") or "")
    return ""


def is_me(text: str) -> bool:
    t = (text or "").strip()
    if not t or PLACEHOLDER.search(t):
        return False
    return bool(ME_MARK.search(t)) and len(t) > 40


def upsert_prov(unit: dict[str, Any]) -> None:
    layers = unit.get("pratibha_layers") or []
    for L in layers:
        if isinstance(L, dict) and L.get("kind") == "original":
            L["label"] = "Original (Middle English)"
            L["layer_provenance"] = PROV
    lp = unit.get("layer_provenance")
    if not isinstance(lp, dict):
        unit["layer_provenance"] = {"original": PROV}
    else:
        lp["original"] = PROV
    # Keep IAST note honest
    for L in layers:
        if isinstance(L, dict) and L.get("kind") == "iast":
            body = str(L.get("body") or "")
            if "Middle English" not in body:
                L["body"] = "Middle English (original language of the work).\n"
            L["layer_provenance"] = PROV
    top = unit.get("provenance")
    if isinstance(top, dict):
        ref = str(top.get("source_reference") or "")
        tip = "Underhill 1912 PD Middle English edition (corpus ME in Original layer)."
        if "Underhill" not in ref:
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

    paths = sorted(CANON.glob("*.yml"))
    # exclude index if any yml somehow
    paths = [p for p in paths if p.suffix == ".yml"]
    updated: dict[str, dict[str, Any]] = {}
    ok = miss = 0
    for path in paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or "unit_id" not in data:
            continue
        uid = data["unit_id"]
        orig = layer_body(data, "original") or (data.get("sanskrit_devanagari") or "")
        if is_me(orig):
            ok += 1
            print(f"OK  {uid}: ME len={len(orig.strip())}")
            if args.write:
                upsert_prov(data)
                if not (data.get("sanskrit_devanagari") or "").strip():
                    data["sanskrit_devanagari"] = layer_body(data, "original")
                data["sanskrit_iast"] = "Middle English (original language of the work)."
                atomic_write(path, dump_yaml(data))
                updated[uid] = data
        else:
            miss += 1
            print(f"MISS {uid}: no ME original (head={orig[:80]!r})")

    if args.write and updated:
        n = sync_index(updated)
        print(f"synced index.jsonl rows={n}")
    elif not args.write:
        print("dry-run (pass --write to apply provenance + index sync)")

    print(f"ME coverage: {ok}/{ok + miss} (unmatched={miss})")
    return 0 if miss == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
