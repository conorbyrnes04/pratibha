#!/usr/bin/env python3
"""Apply deterministic canonical directory and Sanskrit-script hygiene fixes."""
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
TARGET_WORKS = {"nagarjuna_mulamadhyamakakarika", "heart_sutra"}
TARGET_HEART_UNITS = {"heart_sutra.hs_001", "heart_sutra.hs_002"}


def has_devanagari(text: str) -> bool:
    return any("\u0900" <= character <= "\u097f" for character in text)


def is_target(unit: dict[str, Any]) -> bool:
    work_id = unit.get("work_id")
    if work_id == "nagarjuna_mulamadhyamakakarika":
        return True
    return unit.get("unit_id") in TARGET_HEART_UNITS


def fix_unit(unit: dict[str, Any]) -> bool:
    if not is_target(unit):
        return False
    misplaced = str(unit.get("sanskrit_devanagari") or "")
    if not misplaced:
        raise ValueError(f"{unit.get('unit_id')}: expected a non-empty misplaced field")
    if has_devanagari(misplaced):
        raise ValueError(
            f"{unit.get('unit_id')}: field contains Devanagari; refusing to move it"
        )

    layers = unit.get("pratibha_layers")
    if not isinstance(layers, list):
        raise ValueError(f"{unit.get('unit_id')}: pratibha_layers is not a list")
    original_layers = [
        layer for layer in layers if isinstance(layer, dict) and layer.get("kind") == "original"
    ]
    iast_layers = [
        layer for layer in layers if isinstance(layer, dict) and layer.get("kind") == "iast"
    ]
    if len(original_layers) != 1 or len(iast_layers) != 1:
        raise ValueError(
            f"{unit.get('unit_id')}: expected one original and one iast layer"
        )
    if str(original_layers[0].get("body") or "") != misplaced:
        raise ValueError(
            f"{unit.get('unit_id')}: original layer does not mirror sanskrit_devanagari"
        )

    unit["sanskrit_devanagari"] = ""
    unit["sanskrit_iast"] = misplaced
    original_layers[0]["body"] = ""
    iast_layers[0]["body"] = misplaced
    return True


def atomic_write(path: Path, content: str) -> None:
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        handle.write(content)
        temp_path = Path(handle.name)
    temp_path.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    index_lines = INDEX.read_text(encoding="utf-8").splitlines(keepends=True)
    index_units = [json.loads(line) for line in index_lines if line.strip()]
    if len(index_lines) != len(index_units):
        raise ValueError("index.jsonl contains blank lines")
    for line, unit in zip(index_lines, index_units):
        if json.dumps(unit, ensure_ascii=False) + "\n" != line:
            raise ValueError(f"index serialization mismatch at {unit.get('unit_id')}")

    yaml_units: dict[str, tuple[Path, dict[str, Any], str]] = {}
    for path in sorted(CANONICAL.glob("*/*.yml")):
        original = path.read_text(encoding="utf-8")
        unit = yaml.safe_load(original)
        if not isinstance(unit, dict) or not unit.get("unit_id"):
            raise ValueError(f"invalid canonical YAML: {path}")
        yaml_units[str(unit["unit_id"])] = (path, unit, original)

    empty_dirs = []
    for directory in sorted(path for path in CANONICAL.iterdir() if path.is_dir()):
        yaml_files = list(directory.rglob("*.yml")) + list(directory.rglob("*.yaml"))
        if yaml_files:
            continue
        entries = list(directory.iterdir())
        if entries:
            raise ValueError(
                f"{directory}: has no YAML but is not truly empty: "
                + ", ".join(entry.name for entry in entries)
            )
        empty_dirs.append(directory)

    changed_yaml: dict[Path, dict[str, Any]] = {}
    changed_lines: dict[int, str] = {}
    changed_ids = []
    for line_number, index_unit in enumerate(index_units):
        unit_id = str(index_unit["unit_id"])
        path, yaml_unit, original_yaml = yaml_units[unit_id]
        if yaml_unit != index_unit:
            raise ValueError(f"{unit_id}: YAML differs from index before edits")
        next_index = copy.deepcopy(index_unit)
        next_yaml = copy.deepcopy(yaml_unit)
        changed_index = fix_unit(next_index)
        changed_file = fix_unit(next_yaml)
        if changed_index != changed_file or next_index != next_yaml:
            raise ValueError(f"{unit_id}: YAML/index fixes diverged")
        if not changed_index:
            continue
        roundtrip = yaml.safe_dump(
            yaml_unit,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
            width=120,
        )
        if roundtrip != original_yaml:
            raise ValueError(f"{unit_id}: YAML serializer would cause formatting churn")
        changed_ids.append(unit_id)
        changed_yaml[path] = next_yaml
        changed_lines[line_number] = json.dumps(next_index, ensure_ascii=False) + "\n"

    expected_ids = {
        unit["unit_id"]
        for unit in index_units
        if unit.get("work_id") == "nagarjuna_mulamadhyamakakarika"
    } | TARGET_HEART_UNITS
    if set(changed_ids) != expected_ids or len(changed_ids) != 11:
        raise ValueError(
            f"expected exactly 11 target units, got {len(changed_ids)}: {changed_ids}"
        )

    verb = "would fix" if args.dry_run else "fixing"
    print(f"{verb} {len(changed_ids)} Sanskrit field/layer pairs")
    for unit_id in changed_ids:
        print(f"FIELD {unit_id}")
    print(f"{'would remove' if args.dry_run else 'removing'} {len(empty_dirs)} empty dirs")
    for directory in empty_dirs:
        print(f"DIR {directory.name}")

    if args.dry_run:
        return 0

    for path, unit in changed_yaml.items():
        content = yaml.safe_dump(
            unit,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
            width=120,
        )
        atomic_write(path, content)
    atomic_write(
        INDEX,
        "".join(
            changed_lines.get(line_number, line)
            for line_number, line in enumerate(index_lines)
        ),
    )
    for directory in empty_dirs:
        directory.rmdir()
    print("canonical YAML and index.jsonl synchronized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
