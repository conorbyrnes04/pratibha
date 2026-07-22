#!/usr/bin/env python3
"""Apply a JSONL patch to canonical units WITHOUT a full re-canonicalize.

Generalizes inject_key_terms.py / inject_resonances.py. Reads a proposals file
(one JSON object per line) and applies field/layer edits to the matching
data/canonical/<work>/*.yml unit AND the data/canonical/index.jsonl line,
keeping the two byte-synchronized, with the same safety guards used by the
Wave-1 injectors:

  * index.jsonl must round-trip its own serialization before any edit
  * each canonical unit must equal its index line before any edit
  * re-dumping an *untouched* canonical unit must reproduce it byte-for-byte
    (so we never churn formatting of files we do not change)

Patch record (per line):
  {
    "unit_id": "vijnana_bhairava.yukti_002",
    "set_fields": {"title": "...", "themes": ["a","b"]},   # top-level replace
    "retag_from_themes": true,          # rebuild `tags` = non-theme tags + themes
    "set_layers": [                     # upsert layers (by kind), spec-ordered
      {"kind": "original", "body": "...", "layer_provenance": "transliterated_from_iast"}
    ]
  }

Only keys present in a record are touched; everything else is left intact.
It never edits data/yaml and never runs canonicalize's writer.
"""
from __future__ import annotations

import argparse
import copy
import json
import tempfile
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
CANONICAL = ROOT / "data" / "canonical"
INDEX = CANONICAL / "index.jsonl"

LAYER_ORDER = ["original", "iast", "translation", "commentary", "key_terms", "resonances", "practice", "appendix"]


def load_index() -> tuple[list[str], list[dict[str, Any]]]:
    lines = INDEX.read_text(encoding="utf-8").splitlines(keepends=True)
    units = [json.loads(line) for line in lines if line.strip()]
    if len(lines) != len(units):
        raise ValueError("index.jsonl contains blank lines; refusing to rewrite ambiguously")
    for line, unit in zip(lines, units):
        if (json.dumps(unit, ensure_ascii=False) + "\n").encode("utf-8") != line.encode("utf-8"):
            raise ValueError(f"index serialization mismatch before edits at {unit.get('unit_id')}")
    return lines, units


def yaml_by_unit() -> dict[str, tuple[Path, dict[str, Any], str]]:
    result: dict[str, tuple[Path, dict[str, Any], str]] = {}
    for path in sorted(CANONICAL.glob("*/*.yml")):
        if path.name == "_work.yml":
            continue
        original = path.read_text(encoding="utf-8")
        unit = yaml.safe_load(original)
        if not isinstance(unit, dict) or not unit.get("unit_id"):
            raise ValueError(f"invalid canonical unit YAML: {path}")
        result[str(unit["unit_id"])] = (path, unit, original)
    return result


def atomic_write(path: Path, content: str) -> None:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(content)
        temp_path = Path(handle.name)
    temp_path.replace(path)


def dump_yaml(unit: dict[str, Any]) -> str:
    return yaml.safe_dump(
        unit, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120
    )


def upsert_layer(unit: dict[str, Any], spec: dict[str, Any]) -> None:
    kind = spec["kind"]
    layers = unit.get("pratibha_layers")
    if not isinstance(layers, list):
        layers = []
        unit["pratibha_layers"] = layers
    existing = next((l for l in layers if isinstance(l, dict) and l.get("kind") == kind), None)
    if existing is not None:
        for k in ("body", "items", "layer_provenance", "label"):
            if k in spec:
                existing[k] = spec[k]
        return
    new_layer: dict[str, Any] = {"kind": kind}
    if "label" in spec:
        new_layer["label"] = spec["label"]
    for k in ("body", "items", "layer_provenance"):
        if k in spec:
            new_layer[k] = spec[k]
    # Insert at spec-ordered position.
    my_rank = LAYER_ORDER.index(kind) if kind in LAYER_ORDER else len(LAYER_ORDER)
    insertion = next(
        (
            i
            for i, l in enumerate(layers)
            if isinstance(l, dict)
            and (LAYER_ORDER.index(l["kind"]) if l.get("kind") in LAYER_ORDER else len(LAYER_ORDER)) > my_rank
        ),
        len(layers),
    )
    layers.insert(insertion, new_layer)


def apply_patch(unit: dict[str, Any], patch: dict[str, Any]) -> None:
    old_themes = list(unit.get("themes") or [])
    set_fields = patch.get("set_fields") or {}
    for key, value in set_fields.items():
        unit[key] = value
    if patch.get("retag_from_themes"):
        new_themes = list(unit.get("themes") or [])
        base_tags = [t for t in (unit.get("tags") or []) if t not in old_themes]
        unit["tags"] = sorted(set(base_tags) | set(new_themes))
    for spec in patch.get("set_layers") or []:
        upsert_layer(unit, spec)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("patch", help="path to a JSONL proposals file")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--show", type=int, default=3, help="how many example diffs to print")
    args = parser.parse_args()

    patches: dict[str, dict[str, Any]] = {}
    for line in Path(args.patch).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        uid = str(rec["unit_id"])
        if uid in patches:
            raise ValueError(f"duplicate unit_id in patch file: {uid}")
        patches[uid] = rec

    original_lines, index_units = load_index()
    yaml_units = yaml_by_unit()
    if set(yaml_units) != {str(u["unit_id"]) for u in index_units}:
        raise ValueError("YAML unit_ids and index.jsonl unit_ids do not match exactly")

    missing = [u for u in patches if u not in yaml_units]
    if missing:
        raise ValueError(f"patch references unknown unit_ids: {missing[:5]} ({len(missing)} total)")

    changed_index_lines: dict[int, str] = {}
    changed_yaml: dict[Path, dict[str, Any]] = {}
    examples: list[tuple[str, dict[str, Any], dict[str, Any]]] = []

    for line_number, index_unit in enumerate(index_units):
        uid = str(index_unit["unit_id"])
        patch = patches.get(uid)
        if not patch:
            continue
        path, yaml_unit, original_yaml = yaml_units[uid]
        if yaml_unit != index_unit:
            raise ValueError(f"{uid}: YAML content differs from index content before edits")

        # Churn guard: serializer must reproduce the untouched unit exactly.
        if dump_yaml(yaml_unit).encode("utf-8") != original_yaml.encode("utf-8"):
            raise ValueError(f"{uid}: YAML serializer would churn untouched formatting; skipping is unsafe")

        next_index = copy.deepcopy(index_unit)
        next_yaml = copy.deepcopy(yaml_unit)
        apply_patch(next_index, patch)
        apply_patch(next_yaml, patch)
        if next_index != next_yaml:
            raise ValueError(f"{uid}: YAML/index diverged after patch")

        changed_yaml[path] = next_yaml
        changed_index_lines[line_number] = json.dumps(next_index, ensure_ascii=False) + "\n"
        if len(examples) < args.show:
            examples.append((uid, index_unit, next_index))

    print(f"patch records: {len(patches)}")
    print(f"{'would change' if args.dry_run else 'changing'} {len(changed_yaml)} units")
    for uid, before, after in examples:
        print(f"\n===== {uid} =====")
        if before.get("title") != after.get("title"):
            print(f"  title: {before.get('title')!r} -> {after.get('title')!r}")
        if before.get("themes") != after.get("themes"):
            print(f"  themes: {before.get('themes')} -> {after.get('themes')}")
        bk = [l.get("kind") for l in before.get("pratibha_layers", [])]
        ak = [l.get("kind") for l in after.get("pratibha_layers", [])]
        if bk != ak:
            print(f"  layers: {bk} -> {ak}")
        for l in after.get("pratibha_layers", []):
            if l.get("kind") == "original" and l.get("body"):
                print(f"  original: {l['body'][:80]!r}")

    if args.dry_run:
        return 0

    for path, unit in changed_yaml.items():
        atomic_write(path, dump_yaml(unit))
    new_lines = [changed_index_lines.get(i, original) for i, original in enumerate(original_lines)]
    atomic_write(INDEX, "".join(new_lines))
    print(f"\nwrote {len(changed_yaml)} YAML files and synchronized index.jsonl")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
