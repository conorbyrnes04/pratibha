#!/usr/bin/env python3
"""
Promote intermediate Vajrayāna pilot YAML (data/yaml/<slug>/) into canonical
corpus files (data/canonical/<work_id>/), reusing the exact normalization from
scripts/canonicalize_texts.py so the schema matches the rest of the corpus
(category, pratibha_layers, appendixes, provenance, thesis/source_excerpt).

Also writes a per-collection index.jsonl and merges the new units into the
global data/canonical/index.jsonl (idempotent: replaces any prior lines for the
same work_ids, dedupes by unit_id).

Usage:
  python scripts/vajrayana_promote_canonical.py \
      data/yaml/heart_sutra data/yaml/nagarjuna_mulamadhyamakakarika \
      data/yaml/shantideva_bodhicaryavatara data/yaml/tilopa_mahamudra
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.canonicalize_texts import _sanitize, normalize, txt  # noqa: E402

CANONICAL_ROOT = ROOT / "data" / "canonical"
GLOBAL_INDEX = CANONICAL_ROOT / "index.jsonl"


def _load_yaml_files(yaml_dir: Path) -> list[tuple[Path, dict]]:
    out: list[tuple[Path, dict]] = []
    for fp in sorted(yaml_dir.glob("*.yml")):
        raw = yaml.safe_load(fp.read_text(encoding="utf-8")) or {}
        if isinstance(raw, dict):
            out.append((fp, raw))
    return out


def promote_dir(yaml_dir: Path) -> tuple[str, list[dict]]:
    units: list[dict] = []
    for fp, raw in _load_yaml_files(yaml_dir):
        unit = normalize(fp, raw)
        units.append(unit)

    # dedupe by unit_id, preserve order
    seen: set[str] = set()
    kept: list[dict] = []
    for u in units:
        uid = txt(u.get("unit_id"))
        if not uid or uid in seen:
            continue
        seen.add(uid)
        kept.append(u)

    if not kept:
        return "", []

    work_id = txt(kept[0].get("work_id")) or yaml_dir.name
    out_dir = CANONICAL_ROOT / work_id
    out_dir.mkdir(parents=True, exist_ok=True)

    for u in kept:
        fname = f"{txt(u.get('unit_id')).replace('.', '_')}.yml"
        clean = _sanitize(u)
        (out_dir / fname).write_text(
            yaml.safe_dump(clean, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120),
            encoding="utf-8",
        )

    # per-collection index.jsonl
    with open(out_dir / "index.jsonl", "w", encoding="utf-8") as f:
        for u in kept:
            f.write(json.dumps(_sanitize(u), ensure_ascii=False) + "\n")

    root_n = sum(1 for u in kept if u.get("category") == "root_text")
    comm_n = sum(1 for u in kept if u.get("category") == "commentary_text")
    print(f"  {work_id}: {len(kept)} units (root_text={root_n}, commentary_text={comm_n}) -> {out_dir.relative_to(ROOT)}")
    return work_id, kept


def update_global_index(new_by_work: dict[str, list[dict]]) -> None:
    """Merge new units into the global index, replacing any prior lines for the
    same work_ids and deduping by unit_id."""
    existing: list[dict] = []
    if GLOBAL_INDEX.exists():
        for line in GLOBAL_INDEX.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                existing.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    target_work_ids = set(new_by_work.keys())
    merged: list[dict] = [
        rec for rec in existing if txt(rec.get("work_id")) not in target_work_ids
    ]
    seen_ids = {txt(rec.get("unit_id")) for rec in merged}
    added = 0
    for units in new_by_work.values():
        for u in units:
            uid = txt(u.get("unit_id"))
            if not uid or uid in seen_ids:
                continue
            seen_ids.add(uid)
            merged.append(_sanitize(u))
            added += 1

    with open(GLOBAL_INDEX, "w", encoding="utf-8") as f:
        for rec in merged:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"Global index: {len(merged)} total lines ({added} new for {sorted(target_work_ids)})")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("yaml_dirs", nargs="+", type=Path)
    args = ap.parse_args()

    new_by_work: dict[str, list[dict]] = {}
    for d in args.yaml_dirs:
        d = d if d.is_absolute() else ROOT / d
        if not d.is_dir():
            print(f"skip (not a dir): {d}")
            continue
        work_id, kept = promote_dir(d)
        if work_id:
            new_by_work[work_id] = kept

    if new_by_work:
        update_global_index(new_by_work)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
