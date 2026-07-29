#!/usr/bin/env python3
"""Restore Tibetan Unicode originals for tilopa_mahamudra (3 units).

Source:
  data/raw_texts/pd/tibetan/tilopa_ganges_mahamudra_lotsawa_bo.txt
  (phyag chen gang gā ma / Ganges Mahāmudrā; Lotsawa House Tibetan text dump).
  Unit slices already stored on YAML as tibetan_uchen / tibetan_wylie were
  verified as contiguous exact matches against that file (TIL_001 = ll.1–9,
  TIL_002 = ll.10–38, TIL_003 = ll.39–67).

Promotes Tibetan into pratibha_layers.original (and Wylie into iast),
mirrors into sanskrit_devanagari / sanskrit_iast, and syncs index.jsonl.

Honest provenance: not a critical xylograph edition; editorial Tengyur-
tradition Tibetan as transmitted in the Lotsawa House dump. English remains
Pratibha editorial.

  python scripts/restore_tilopa_tibetan.py            # preview
  python scripts/restore_tilopa_tibetan.py --write
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
CANON = ROOT / "data" / "canonical" / "tilopa_mahamudra"
MAIN_INDEX = ROOT / "data" / "canonical" / "index.jsonl"
COLL_INDEX = CANON / "index.jsonl"
SRC = ROOT / "data" / "raw_texts" / "pd" / "tibetan" / "tilopa_ganges_mahamudra_lotsawa_bo.txt"

PROV = (
    "tibetan: phyag chen gang gā ma (Tilopa Ganges Mahāmudrā) from "
    "data/raw_texts/pd/tibetan/tilopa_ganges_mahamudra_lotsawa_bo.txt "
    "(Lotsawa House Tibetan dump; Tengyur-tradition transmission). "
    "Not a critical xylograph edition. Wylie = unit tibetan_wylie / "
    "sanskrit_iast. English = Pratibha editorial."
)

TIB_RE = re.compile(r"[\u0F00-\u0FFF]")
PLACEHOLDER = re.compile(r"source-language basis", re.I)

# Contiguous line ranges in SRC (0-based, end exclusive) verified exact.
SLICES = {
    "tilopa_mahamudra.til_001": (0, 9),
    "tilopa_mahamudra.til_002": (9, 38),
    "tilopa_mahamudra.til_003": (38, 67),
}


def tib_count(text: str) -> int:
    return len(TIB_RE.findall(text or ""))


def has_native(text: str, min_chars: int = 20) -> bool:
    if tib_count(text) < min_chars:
        return False
    if PLACEHOLDER.search(text or ""):
        return False
    return True


def src_lines() -> list[str]:
    raw = SRC.read_text(encoding="utf-8")
    return [ln.strip() for ln in raw.splitlines() if ln.strip()]


def normalize_block(lines: list[str]) -> str:
    return "\n".join(lines).strip() + "\n"


def upsert_layer(
    unit: dict[str, Any],
    kind: str,
    body: str,
    label: str,
    provenance: str,
) -> None:
    layers = unit.get("pratibha_layers")
    if not isinstance(layers, list):
        layers = []
        unit["pratibha_layers"] = layers
    existing = next(
        (L for L in layers if isinstance(L, dict) and L.get("kind") == kind), None
    )
    if existing is None:
        existing = {"kind": kind, "label": label}
        order = [
            "original",
            "iast",
            "translation",
            "commentary",
            "key_terms",
            "resonances",
            "practice",
            "appendix",
        ]
        idx = order.index(kind) if kind in order else len(layers)
        pos = 0
        for i, L in enumerate(layers):
            k = L.get("kind") if isinstance(L, dict) else None
            if k in order and order.index(k) <= idx:
                pos = i + 1
        layers.insert(pos, existing)
    existing["label"] = label
    existing["body"] = body if body.endswith("\n") else body + "\n"
    existing["layer_provenance"] = provenance


def apply_to_unit(data: dict[str, Any], tibetan: str, wylie: str) -> None:
    upsert_layer(data, "original", tibetan, "Original (Tibetan)", PROV)
    upsert_layer(data, "iast", wylie, "Wylie", PROV)
    data["sanskrit_devanagari"] = tibetan
    data["sanskrit_iast"] = wylie
    data["tibetan_uchen"] = tibetan
    data["tibetan_wylie"] = wylie
    data["source_edition"] = (
        "Tilopa, Ganges Mahāmudrā (phyag chen gang gā ma); "
        "Tibetan from Lotsawa House dump (PD traditional text)."
    )
    top = data.get("provenance")
    if isinstance(top, dict):
        top["source_reference"] = (
            "Tilopa, *Mahāmudropadeśa* (Ganges Mahāmudrā); Tibetan Unicode from "
            "Lotsawa House dump (data/raw_texts/pd/tibetan/tilopa_ganges_mahamudra_lotsawa_bo.txt)."
        )
    lp = data.get("layer_provenance")
    if not isinstance(lp, dict):
        data["layer_provenance"] = {"original": PROV}
    else:
        lp["original"] = PROV


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
    if not MAIN_INDEX.is_file():
        raise SystemExit(f"missing {MAIN_INDEX}")
    lines = MAIN_INDEX.read_text(encoding="utf-8").splitlines(keepends=True)
    if any(not ln.strip() for ln in lines):
        # allow trailing blank only
        if lines and not lines[-1].strip() and any(not ln.strip() for ln in lines[:-1]):
            raise SystemExit("index.jsonl has blank lines; refusing")
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
    if COLL_INDEX.is_file():
        coll_lines = []
        for uid in sorted(updated):
            coll_lines.append(json.dumps(updated[uid], ensure_ascii=False) + "\n")
        atomic_write(COLL_INDEX, "".join(coll_lines))
    return n


def layer_body(unit: dict[str, Any], kind: str) -> str:
    for L in unit.get("pratibha_layers") or []:
        if isinstance(L, dict) and L.get("kind") == kind:
            return str(L.get("body") or "")
    return ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    if not SRC.is_file():
        print(f"missing source: {SRC}", file=sys.stderr)
        return 1

    lines = src_lines()
    paths = sorted(CANON.glob("tilopa_mahamudra_til_*.yml"))
    if len(paths) != 3:
        print(f"expected 3 YAML units, found {len(paths)}", file=sys.stderr)
        return 1

    before = after = 0
    updated: dict[str, dict[str, Any]] = {}

    for path in paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        uid = data.get("unit_id")
        if uid not in SLICES:
            print(f"skip unknown {uid}")
            continue
        old = layer_body(data, "original")
        if has_native(old):
            before += 1

        start, end = SLICES[uid]
        want = normalize_block(lines[start:end])
        have = normalize_block(
            [
                ln.strip()
                for ln in (data.get("tibetan_uchen") or data.get("sanskrit_devanagari") or "").splitlines()
                if ln.strip()
            ]
        )
        if have.strip() and have != want:
            # Prefer on-disk uchen if it already matched; else require SRC slice.
            if not has_native(have) or [
                ln.strip() for ln in have.splitlines() if ln.strip()
            ] != lines[start:end]:
                print(f"WARN {uid}: unit Tibetan differs from SRC slice; using SRC")
            tibetan = want
        else:
            tibetan = want if not have.strip() else have

        # Re-verify exact match to SRC
        unit_lines = [ln.strip() for ln in tibetan.splitlines() if ln.strip()]
        if unit_lines != lines[start:end]:
            print(f"ERROR {uid}: failed exact match to SRC[{start}:{end}]", file=sys.stderr)
            return 1

        wylie = (data.get("tibetan_wylie") or data.get("sanskrit_iast") or "").strip()
        if not wylie or PLACEHOLDER.search(wylie):
            print(f"ERROR {uid}: missing Wylie on unit", file=sys.stderr)
            return 1
        if not wylie.endswith("\n"):
            wylie += "\n"

        print(f"{uid}: tib_chars={tib_count(tibetan)} lines={len(unit_lines)} src[{start}:{end}]")
        if args.write:
            apply_to_unit(data, tibetan if tibetan.endswith("\n") else tibetan + "\n", wylie)
            atomic_write(path, dump_yaml(data))
            updated[uid] = data
            if has_native(layer_body(data, "original")):
                after += 1
        else:
            if has_native(tibetan):
                after += 1

    if args.write:
        n = sync_index(updated)
        print(f"wrote {len(updated)} YAML; synced index rows={n}")
    else:
        print("dry-run (pass --write to apply)")

    print(f"native original coverage: before={before} after={after} / 3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
