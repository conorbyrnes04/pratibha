#!/usr/bin/env python3
"""Restore Devanagari originals for shantideva_bodhicaryavatara (8 units).

Source: GRETIL Bodhicaryāvatāra IAST (Minayeff/Vaidya lineage), local copy at
  data/raw_texts/pd/indian/bodhicaryavatara_gretil_iast_sanskrit.txt
  (from http://gretil.sub.uni-goettingen.de/ … sa_zAntideva-bodhicaryAvatAra.xml)

Verse tags are curated against each unit's English (Barnett 1909 PD anchors /
study translations). IAST is stored with verse tags; Devanagari is produced
deterministically via indic_transliteration (IAST → Devanagari).

Updates:
  - data/canonical/shantideva_bodhicaryavatara/*.yml
  - data/canonical/shantideva_bodhicaryavatara/index.jsonl
  - data/canonical/index.jsonl (shantideva rows only)

Does not commit. Does not rewrite English commentary/translation.

    python scripts/restore_shantideva_sanskrit.py            # preview
    python scripts/restore_shantideva_sanskrit.py --write
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
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "data" / "canonical" / "shantideva_bodhicaryavatara"
MAIN_INDEX = ROOT / "data" / "canonical" / "index.jsonl"
COLL_INDEX = CANON / "index.jsonl"
GRETIL = ROOT / "data" / "raw_texts" / "pd" / "indian" / "bodhicaryavatara_gretil_iast_sanskrit.txt"
REPORT = ROOT / "data" / "raw_texts" / "pd" / "indian" / "shantideva_sanskrit_restore_report.tsv"

PROV = (
    "sanskrit: GRETIL Bodhicaryāvatāra IAST (Minayeff/Vaidya PD lineage; "
    "data/raw_texts/pd/indian/bodhicaryavatara_gretil_iast_sanskrit.txt) → "
    "Devanagari via indic_transliteration; verse tags curated to unit English "
    "(Barnett 1909 PD locator)."
)

DEV_RE = re.compile(r"[\u0900-\u097F]")
PLACEHOLDER_RE = re.compile(
    r"source-language basis|key terms in iast|not source-verified|per-verse",
    re.I,
)

# Curated verse ranges matched to unit English (Barnett / study anchors).
UNIT_VERSES: dict[str, list[str]] = {
    "shantideva_bodhicaryavatara.bca_08_solitude": ["8.1", "8.2", "8.3", "8.4"],
    "shantideva_bodhicaryavatara.bca_08_trees": ["8.26", "8.27", "8.28", "8.29", "8.33"],
    "shantideva_bodhicaryavatara.bca_08_body": [
        "8.178",
        "8.179",
        "8.180",
        "8.181",
        "8.182",
        "8.184",
    ],
    "shantideva_bodhicaryavatara.bca_08_equal": ["8.90", "8.91", "8.92", "8.93", "8.94"],
    "shantideva_bodhicaryavatara.bca_08_exchange": [
        "8.111",
        "8.112",
        "8.113",
        "8.114",
        "8.115",
    ],
    "shantideva_bodhicaryavatara.bca_09_twotruths": ["9.1", "9.2"],
    "shantideva_bodhicaryavatara.bca_09_dream": ["9.151", "9.152", "9.153", "9.154"],
    "shantideva_bodhicaryavatara.bca_09_compassion": ["9.167", "9.168"],
}


def load_verses(path: Path) -> dict[str, str]:
    """Map '8.90' -> cleaned IAST verse body (no chapter colophons)."""
    raw = path.read_text(encoding="utf-8")
    verses: dict[str, str] = {}
    for m in re.finditer(r"(.*?)//\s*Bca_(\d+)\.(\d+)", raw, re.S):
        body = " ".join(m.group(1).split())
        body = body.split("//")[-1].strip()
        # Drop chapter colophons / pariccheda headers that precede verse 1 of a chapter.
        body = re.sub(
            r"^bodhicaryāvatāre\s+.*?paricchedaḥ\s*\|\|\s*",
            "",
            body,
            flags=re.I,
        )
        body = re.sub(r"^pariccheda\s+\d+\s*", "", body, flags=re.I)
        body = body.strip()
        if body:
            verses[f"{m.group(2)}.{m.group(3)}"] = body
    return verses


def iast_to_deva_line(iast: str) -> str:
    """Transliterate one IAST verse; normalize avagraha / daṇḍas lightly."""
    # Preserve Latin verse tag "8.90: " if present.
    m = re.match(r"^(\d+\.\d+:\s*)(.*)$", iast, re.S)
    prefix, text = (m.group(1), m.group(2)) if m else ("", iast)
    # Normalize ASCII avagraha before transliteration.
    text = text.replace("'", "'").replace("'", "'")
    dev = transliterate(text, sanscript.IAST, sanscript.DEVANAGARI)
    # Collapse space before avagraha (ऽ) that some converters insert.
    dev = re.sub(r"\s+ऽ", "ऽ", dev)
    return f"{prefix}{dev}".strip()


def format_iast(tags: list[str], verses: dict[str, str]) -> str:
    lines = []
    for t in tags:
        if t not in verses:
            raise KeyError(t)
        lines.append(f"{t}: {verses[t]}")
    return "\n".join(lines).strip() + "\n"


def format_deva(iast_block: str) -> str:
    out = []
    for line in iast_block.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        out.append(iast_to_deva_line(line))
    return "\n".join(out).strip() + "\n"


def has_native_deva(text: str, min_chars: int = 20) -> bool:
    if PLACEHOLDER_RE.search(text or ""):
        return False
    return len(DEV_RE.findall(text or "")) >= min_chars


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
    existing = next((L for L in layers if isinstance(L, dict) and L.get("kind") == kind), None)
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


def apply_to_unit(unit: dict[str, Any], iast: str, deva: str, tags: list[str]) -> None:
    upsert_layer(unit, "original", deva, "Original", PROV)
    upsert_layer(unit, "iast", iast, "IAST", PROV)
    unit["sanskrit_devanagari"] = deva
    unit["sanskrit_iast"] = iast
    prov = unit.get("layer_provenance")
    if not isinstance(prov, dict):
        prov = {}
    prov["original"] = PROV
    prov["iast"] = "gretil_bca_iast"
    unit["layer_provenance"] = prov
    top = unit.get("provenance")
    if isinstance(top, dict):
        top = dict(top)
        top["sanskrit_source"] = (
            f"GRETIL BCA IAST → Devanagari; verses {','.join(tags)}"
        )
        unit["provenance"] = top


def dump_yaml(unit: dict[str, Any]) -> str:
    return yaml.safe_dump(
        unit, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120
    )


def atomic_write(path: Path, content: str) -> None:
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        handle.write(content)
        tmp = Path(handle.name)
    tmp.replace(path)


def unit_has_deva(unit: dict[str, Any]) -> bool:
    layers = unit.get("pratibha_layers") or []
    for L in layers:
        if isinstance(L, dict) and L.get("kind") == "original":
            if has_native_deva(str(L.get("body") or "")):
                return True
    return has_native_deva(str(unit.get("sanskrit_devanagari") or ""))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    if not GRETIL.is_file():
        print(f"missing GRETIL source: {GRETIL}", file=sys.stderr)
        return 1

    verses = load_verses(GRETIL)
    paths = sorted(p for p in CANON.glob("*.yml") if p.name != "_work.yml")
    before = sum(1 for p in paths if unit_has_deva(yaml.safe_load(p.read_text(encoding="utf-8"))))

    plans: list[dict[str, Any]] = []
    unmatched: list[str] = []
    report: list[str] = ["unit_id\tverses\tok\tpreview"]

    print(f"gretil_verses={len(verses)} units={len(paths)} write={args.write}")
    print(f"before_native_deva={before}/{len(paths)}")

    for path in paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        uid = str(data.get("unit_id") or "")
        tags = UNIT_VERSES.get(uid)
        if not tags:
            unmatched.append(uid or path.name)
            report.append(f"{uid}\t\tFalse\tno verse map")
            print(f"  NO MAP {uid}")
            continue
        missing = [t for t in tags if t not in verses]
        if missing:
            unmatched.append(f"{uid} missing={missing}")
            report.append(f"{uid}\t{','.join(tags)}\tFalse\tmissing {missing}")
            print(f"  MISSING {uid}: {missing}")
            continue
        iast = format_iast(tags, verses)
        deva = format_deva(iast)
        if not has_native_deva(deva):
            unmatched.append(f"{uid} (no Devanagari produced)")
            report.append(f"{uid}\t{','.join(tags)}\tFalse\ttranslit failed")
            print(f"  TRANSLIT FAIL {uid}")
            continue
        preview = deva.splitlines()[0][:70]
        print(f"  {uid}: {','.join(tags)} | {preview}")
        report.append(f"{uid}\t{','.join(tags)}\tTrue\t{preview}")
        plans.append({"path": path, "uid": uid, "tags": tags, "iast": iast, "deva": deva, "data": data})

    print(f"planned={len(plans)} unmatched={len(unmatched)}")
    if unmatched:
        print("UNMATCHED:")
        for u in unmatched:
            print(" ", u)

    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"report={REPORT}")

    if not args.write:
        print("dry-run only; pass --write to apply")
        return 0

    index_lines = MAIN_INDEX.read_text(encoding="utf-8").splitlines(keepends=True)
    index_units = [json.loads(line) for line in index_lines if line.strip()]
    by_uid = {u["unit_id"]: i for i, u in enumerate(index_units)}

    coll_lines: list[str] | None = None
    coll_units: list[dict[str, Any]] | None = None
    coll_by_uid: dict[str, int] = {}
    if COLL_INDEX.is_file():
        coll_lines = COLL_INDEX.read_text(encoding="utf-8").splitlines(keepends=True)
        coll_units = [json.loads(line) for line in coll_lines if line.strip()]
        coll_by_uid = {u["unit_id"]: i for i, u in enumerate(coll_units)}

    updated = 0
    for plan in plans:
        data = plan["data"]
        apply_to_unit(data, plan["iast"], plan["deva"], plan["tags"])
        atomic_write(plan["path"], dump_yaml(data))

        uid = plan["uid"]
        if uid in by_uid:
            idx = by_uid[uid]
            apply_to_unit(index_units[idx], plan["iast"], plan["deva"], plan["tags"])
            index_lines[idx] = json.dumps(index_units[idx], ensure_ascii=False) + "\n"
        if coll_units is not None and coll_lines is not None and uid in coll_by_uid:
            cidx = coll_by_uid[uid]
            apply_to_unit(coll_units[cidx], plan["iast"], plan["deva"], plan["tags"])
            coll_lines[cidx] = json.dumps(coll_units[cidx], ensure_ascii=False) + "\n"
        updated += 1

    atomic_write(MAIN_INDEX, "".join(index_lines))
    if coll_lines is not None:
        atomic_write(COLL_INDEX, "".join(coll_lines))

    after = sum(1 for p in paths if unit_has_deva(yaml.safe_load(p.read_text(encoding="utf-8"))))
    idx_after = 0
    for line in MAIN_INDEX.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("work_id") != "shantideva_bodhicaryavatara":
            continue
        if unit_has_deva(row):
            idx_after += 1

    print(f"wrote {updated} YAML units")
    print(f"after_native_deva yaml={after}/{len(paths)} index={idx_after}/8")
    print("index synced: main + collection")
    return 0


if __name__ == "__main__":
    sys.exit(main())
