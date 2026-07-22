#!/usr/bin/env python3
"""Inject key_terms layers into canonical units WITHOUT a full re-canonicalize.

Re-running scripts/canonicalize_texts.py would clobber canonical-only
enrichments (directly-written resonances, migrated layers, field fixes).
Instead, this script:

  1. Runs the (patched) canonicalizer's own normalize() on each SOURCE yaml
     to obtain exactly the key_terms layer the pipeline would emit.
  2. Injects only that key_terms layer into the matching data/canonical unit,
     in the spec-correct position (after commentary, before resonances),
     leaving every other field/layer byte-for-byte untouched.
  3. Keeps data/canonical/<work>/*.yml and index.jsonl synchronized, using the
     same serialization + roundtrip guarantees as migrate_buried_resonances.py.

It never edits data/yaml and never runs canonicalize's writer.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import tempfile
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
YAML_ROOT = ROOT / "data" / "yaml"
CANONICAL = ROOT / "data" / "canonical"
INDEX = CANONICAL / "index.jsonl"

# Spec layer order: original, iast, translation, commentary, key_terms,
# resonances, practice, appendix. key_terms goes before any of these:
AFTER_KEYTERMS = {"resonances", "practice", "appendix"}


def load_canonicalizer() -> Any:
    path = ROOT / "scripts" / "canonicalize_texts.py"
    spec = importlib.util.spec_from_file_location("canonicalize_texts", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_key_terms_layers(canon: Any) -> dict[str, dict[str, Any]]:
    """unit_id -> the key_terms layer the patched pipeline emits from source."""
    out: dict[str, dict[str, Any]] = {}
    for path in canon.all_yaml_files(YAML_ROOT):
        try:
            raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(raw, dict):
            continue
        try:
            record = canon._coerce_wrapped_record(raw)
            unit = canon.normalize(path, record)
        except Exception:
            continue
        if not isinstance(unit, dict):
            continue
        uid = str(unit.get("unit_id") or "")
        if not uid:
            continue
        for layer in unit.get("pratibha_layers") or []:
            if isinstance(layer, dict) and layer.get("kind") == "key_terms" and layer.get("items"):
                out[uid] = layer
                break
    return out


def has_key_terms(unit: dict[str, Any]) -> bool:
    return any(
        isinstance(layer, dict) and layer.get("kind") == "key_terms" and layer.get("items")
        for layer in unit.get("pratibha_layers") or []
    )


def insert_key_terms(unit: dict[str, Any], layer: dict[str, Any]) -> None:
    layers = unit.get("pratibha_layers")
    if not isinstance(layers, list):
        raise ValueError(f"{unit.get('unit_id')}: pratibha_layers is not a list")
    insertion = next(
        (
            i
            for i, l in enumerate(layers)
            if isinstance(l, dict) and l.get("kind") in AFTER_KEYTERMS
        ),
        len(layers),
    )
    layers.insert(insertion, copy.deepcopy(layer))


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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    canon = load_canonicalizer()
    kt = source_key_terms_layers(canon)

    original_lines, index_units = load_index()
    yaml_units = yaml_by_unit()
    if set(yaml_units) != {str(u["unit_id"]) for u in index_units}:
        raise ValueError("YAML unit_ids and index.jsonl unit_ids do not match exactly")

    changed_index_lines: dict[int, str] = {}
    changed_yaml: dict[Path, dict[str, Any]] = {}
    added: list[str] = []
    already: list[str] = []

    for line_number, index_unit in enumerate(index_units):
        uid = str(index_unit["unit_id"])
        path, yaml_unit, original_yaml = yaml_units[uid]
        if yaml_unit != index_unit:
            raise ValueError(f"{uid}: YAML content differs from index content before edits")
        layer = kt.get(uid)
        if not layer:
            continue
        if has_key_terms(index_unit):
            already.append(uid)
            continue

        next_index = copy.deepcopy(index_unit)
        next_yaml = copy.deepcopy(yaml_unit)
        insert_key_terms(next_index, layer)
        insert_key_terms(next_yaml, layer)
        if next_index != next_yaml:
            raise ValueError(f"{uid}: YAML/index diverged after insert")

        # Guard: only the key_terms layer may differ from the original.
        roundtrip = dump_yaml(yaml_unit)
        if roundtrip.encode("utf-8") != original_yaml.encode("utf-8"):
            raise ValueError(f"{uid}: YAML serializer would churn untouched formatting")

        changed_yaml[path] = next_yaml
        changed_index_lines[line_number] = json.dumps(next_index, ensure_ascii=False) + "\n"
        added.append(uid)

    print(f"source units with key_terms content: {len(kt)}")
    print(f"already have a key_terms layer (skipped): {len(already)}")
    print(f"{'would add' if args.dry_run else 'adding'} key_terms layers to {len(added)} units")
    for uid in added[:3]:
        example = next(u for u in index_units if str(u["unit_id"]) == uid)
        merged = copy.deepcopy(example)
        insert_key_terms(merged, kt[uid])
        new_layer = next(l for l in merged["pratibha_layers"] if l.get("kind") == "key_terms")
        print(f"\n===== {uid} =====\n{json.dumps(new_layer, ensure_ascii=False, indent=2)}")

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
