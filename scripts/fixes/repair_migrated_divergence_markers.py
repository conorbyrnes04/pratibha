#!/usr/bin/env python3
"""Remove a parsed Markdown closing marker from migrated divergences."""
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


def repair(unit: dict[str, Any]) -> int:
    repaired = 0
    for layer in unit.get("pratibha_layers") or []:
        if (
            not isinstance(layer, dict)
            or layer.get("kind") != "resonances"
            or layer.get("layer_provenance") != "migrated_from_commentary"
        ):
            continue
        for item in layer.get("items") or []:
            divergence = str(item.get("divergence") or "")
            if divergence.startswith("* "):
                item["divergence"] = divergence[2:]
                repaired += 1
    return repaired


def atomic_write(path: Path, content: str) -> None:
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        handle.write(content)
        temporary = Path(handle.name)
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    lines = INDEX.read_text(encoding="utf-8").splitlines(keepends=True)
    units = [json.loads(line) for line in lines]
    yaml_units = {}
    for path in CANONICAL.glob("*/*.yml"):
        text = path.read_text(encoding="utf-8")
        unit = yaml.safe_load(text)
        yaml_units[str(unit["unit_id"])] = (path, unit, text)

    changed_lines = {}
    changed_yaml = {}
    item_count = 0
    for line_number, index_unit in enumerate(units):
        unit_id = str(index_unit["unit_id"])
        path, yaml_unit, original = yaml_units[unit_id]
        if yaml_unit != index_unit:
            raise ValueError(f"{unit_id}: YAML/index mismatch")
        next_index = copy.deepcopy(index_unit)
        next_yaml = copy.deepcopy(yaml_unit)
        index_count = repair(next_index)
        yaml_count = repair(next_yaml)
        if index_count != yaml_count or next_index != next_yaml:
            raise ValueError(f"{unit_id}: YAML/index repair mismatch")
        if not index_count:
            continue
        roundtrip = yaml.safe_dump(
            yaml_unit,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
            width=120,
        )
        if roundtrip != original:
            raise ValueError(f"{unit_id}: YAML serializer would cause formatting churn")
        item_count += index_count
        changed_lines[line_number] = json.dumps(next_index, ensure_ascii=False) + "\n"
        changed_yaml[path] = next_yaml

    print(
        f"{'would repair' if args.dry_run else 'repairing'} {item_count} "
        f"divergence markers across {len(changed_yaml)} units"
    )
    if args.dry_run:
        return 0

    for path, unit in changed_yaml.items():
        atomic_write(
            path,
            yaml.safe_dump(
                unit,
                allow_unicode=True,
                sort_keys=False,
                default_flow_style=False,
                width=120,
            ),
        )
    atomic_write(
        INDEX,
        "".join(
            changed_lines.get(line_number, line)
            for line_number, line in enumerate(lines)
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
