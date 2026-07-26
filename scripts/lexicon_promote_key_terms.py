#!/usr/bin/env python3
"""Promote orphan source glossaries into canonical key_terms layers.

Finds source units whose glossary/key_terms would emit a key_terms layer, then:

  1. Injects that layer into index.jsonl units that lack key_terms
  2. Syncs key_terms into per-unit canonical YAML when the index has them
     but the YAML file does not (common when flat YAML drifted from index)

Uses the same insert position / atomic write patterns as
scripts/fixes/inject_key_terms.py. Never runs a full canonicalize.

Dry-run is the default. Pass --write to apply.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
YAML_ROOT = ROOT / "data" / "yaml"
CANONICAL = ROOT / "data" / "canonical"
INDEX = CANONICAL / "index.jsonl"

AFTER_KEYTERMS = {"resonances", "practice", "appendix"}


def load_canonicalizer() -> Any:
    path = ROOT / "scripts" / "canonicalize_texts.py"
    spec = importlib.util.spec_from_file_location("canonicalize_texts", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_key_terms_layers(
    canon: Any, collections: set[str] | None = None
) -> dict[str, dict[str, Any]]:
    """unit_id -> key_terms layer the pipeline emits from source."""
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
        work_id = str(unit.get("work_id") or "")
        folder = path.parent.name
        if collections and work_id not in collections and folder not in collections:
            coll = str(record.get("collection") or "")
            if coll not in collections:
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


def get_key_terms_layer(unit: dict[str, Any]) -> dict[str, Any] | None:
    for layer in unit.get("pratibha_layers") or []:
        if isinstance(layer, dict) and layer.get("kind") == "key_terms" and layer.get("items"):
            return layer
    return None


def insert_key_terms(unit: dict[str, Any], layer: dict[str, Any]) -> None:
    layers = unit.get("pratibha_layers")
    if not isinstance(layers, list):
        unit["pratibha_layers"] = [copy.deepcopy(layer)]
        return
    insertion = next(
        (
            i
            for i, layer_row in enumerate(layers)
            if isinstance(layer_row, dict) and layer_row.get("kind") in AFTER_KEYTERMS
        ),
        len(layers),
    )
    layers.insert(insertion, copy.deepcopy(layer))


def coverage(units: list[dict[str, Any]]) -> tuple[int, int, Counter[str]]:
    total = len(units)
    with_kt = 0
    by_work: Counter[str] = Counter()
    for unit in units:
        if has_key_terms(unit):
            with_kt += 1
            by_work[str(unit.get("work_id") or "unknown")] += 1
    return total, with_kt, by_work


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


def print_coverage(label: str, total: int, with_kt: int, by_work: Counter[str]) -> None:
    pct = (100.0 * with_kt / total) if total else 0.0
    print(f"{label}: {with_kt}/{total} units with key_terms ({pct:.1f}%)")
    for work_id, count in sorted(by_work.items()):
        print(f"  {work_id}: {count}")


def in_scope(work_id: str, uid: str, collections: set[str] | None, kt: dict[str, Any]) -> bool:
    if not collections:
        return True
    if work_id in collections:
        return True
    return uid in kt


def sync_yaml_key_terms(
    yaml_unit: dict[str, Any], layer: dict[str, Any], index_unit: dict[str, Any]
) -> dict[str, Any]:
    """Return yaml unit with key_terms present, preserving other YAML-only fields."""
    next_yaml = copy.deepcopy(yaml_unit)
    if has_key_terms(next_yaml):
        return next_yaml

    layers = next_yaml.get("pratibha_layers")
    if isinstance(layers, list) and layers:
        insert_key_terms(next_yaml, layer)
        return next_yaml

    # Flat / drifted YAML: attach the index layers (includes key_terms) without
    # removing YAML-only top-level fields.
    index_layers = index_unit.get("pratibha_layers")
    if isinstance(index_layers, list) and index_layers:
        next_yaml["pratibha_layers"] = copy.deepcopy(index_layers)
        if not has_key_terms(next_yaml):
            insert_key_terms(next_yaml, layer)
        return next_yaml

    insert_key_terms(next_yaml, layer)
    return next_yaml


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="Apply changes (default is dry-run).",
    )
    parser.add_argument(
        "--collection",
        action="append",
        default=[],
        help="Limit to work_id / collection / folder (repeatable). "
        "Examples: astavakra_gita, pratyabhijnahrdayam, the_book_of_chuang_tzu",
    )
    parser.add_argument(
        "--examples",
        type=int,
        default=3,
        help="How many example layers to print (default 3).",
    )
    args = parser.parse_args()
    dry_run = not args.write
    collections = set(args.collection) if args.collection else None

    canon = load_canonicalizer()
    kt = source_key_terms_layers(canon, collections)

    original_lines, index_units = load_index()
    yaml_units = yaml_by_unit()
    index_ids = {str(u["unit_id"]) for u in index_units}
    yaml_only = sorted(set(yaml_units) - index_ids)
    index_only = sorted(index_ids - set(yaml_units))
    if index_only:
        raise ValueError(
            f"index.jsonl units missing canonical YAML ({len(index_only)}): "
            f"{index_only[:5]}"
        )
    if yaml_only:
        print(
            f"WARNING: {len(yaml_only)} canonical YAML files not in index.jsonl "
            f"(ignored; index is authoritative). sample={yaml_only[:5]}"
        )

    before_total, before_kt, before_by_work = coverage(index_units)
    print_coverage("BEFORE index", before_total, before_kt, before_by_work)
    yaml_list = [yaml_units[uid][1] for uid in sorted(yaml_units) if uid in index_ids]
    y_total, y_kt, y_by_work = coverage(yaml_list)
    print_coverage("BEFORE yaml", y_total, y_kt, y_by_work)

    changed_index_lines: dict[int, str] = {}
    changed_yaml: dict[Path, dict[str, Any]] = {}
    added_index: list[str] = []
    synced_yaml: list[str] = []
    already_index: list[str] = []
    added_by_work: Counter[str] = Counter()
    synced_by_work: Counter[str] = Counter()
    example_layers: list[tuple[str, dict[str, Any]]] = []

    for line_number, index_unit in enumerate(index_units):
        uid = str(index_unit["unit_id"])
        work_id = str(index_unit.get("work_id") or "")
        if not in_scope(work_id, uid, collections, kt):
            continue

        path, yaml_unit, _original_yaml = yaml_units[uid]
        source_layer = kt.get(uid)
        index_layer = get_key_terms_layer(index_unit)

        next_index = index_unit
        index_changed = False

        if source_layer and not index_layer:
            next_index = copy.deepcopy(index_unit)
            insert_key_terms(next_index, source_layer)
            changed_index_lines[line_number] = json.dumps(next_index, ensure_ascii=False) + "\n"
            added_index.append(uid)
            added_by_work[work_id] += 1
            index_changed = True
            index_layer = get_key_terms_layer(next_index)
            if len(example_layers) < args.examples and index_layer:
                example_layers.append((uid, index_layer))
        elif index_layer:
            already_index.append(uid)

        # Prefer index layer (authoritative working copy); fall back to source.
        layer_for_yaml = index_layer or source_layer
        if not layer_for_yaml:
            continue

        if has_key_terms(yaml_unit):
            continue

        # When index was just updated in-memory, sync from that; else from current index.
        index_for_sync = next_index if index_changed else index_unit
        next_yaml = sync_yaml_key_terms(yaml_unit, layer_for_yaml, index_for_sync)
        if not has_key_terms(next_yaml):
            raise ValueError(f"{uid}: failed to sync key_terms into YAML")
        changed_yaml[path] = next_yaml
        synced_yaml.append(uid)
        synced_by_work[work_id] += 1
        if len(example_layers) < args.examples:
            example_layers.append((uid, get_key_terms_layer(next_yaml) or layer_for_yaml))

    print()
    print(f"source units with key_terms content (in scope): {len(kt)}")
    print(f"index already had key_terms: {len(already_index)}")
    print(f"{'would add' if dry_run else 'adding'} key_terms to index: {len(added_index)}")
    if added_by_work:
        for work_id, count in sorted(added_by_work.items()):
            print(f"  index {work_id}: {count}")
    print(f"{'would sync' if dry_run else 'syncing'} key_terms into yaml: {len(synced_yaml)}")
    if synced_by_work:
        for work_id, count in sorted(synced_by_work.items()):
            print(f"  yaml {work_id}: {count}")

    for uid, layer in example_layers[: max(0, args.examples)]:
        print(f"\n===== {uid} =====\n{json.dumps(layer, ensure_ascii=False, indent=2)}")

    after_units = []
    for i, unit in enumerate(index_units):
        if i in changed_index_lines:
            after_units.append(json.loads(changed_index_lines[i]))
        else:
            after_units.append(unit)
    after_total, after_kt, after_by_work = coverage(after_units)
    print()
    print_coverage("AFTER index (projected)" if dry_run else "AFTER index", after_total, after_kt, after_by_work)
    print(f"index delta: +{after_kt - before_kt} units with key_terms")

    after_yaml_map = {uid: yaml_units[uid][1] for uid in index_ids}
    for path, unit in changed_yaml.items():
        after_yaml_map[str(unit["unit_id"])] = unit
    ay_total, ay_kt, ay_by = coverage([after_yaml_map[uid] for uid in sorted(after_yaml_map)])
    print_coverage("AFTER yaml (projected)" if dry_run else "AFTER yaml", ay_total, ay_kt, ay_by)
    print(f"yaml delta: +{ay_kt - y_kt} units with key_terms")

    if dry_run:
        print("\ndry-run only; re-run with --write to apply")
        return 0

    for path, unit in changed_yaml.items():
        atomic_write(path, dump_yaml(unit))
    if changed_index_lines:
        new_lines = [changed_index_lines.get(i, original) for i, original in enumerate(original_lines)]
        atomic_write(INDEX, "".join(new_lines))
    print(
        f"\nwrote {len(changed_yaml)} YAML files"
        + (f" and synchronized index.jsonl ({len(changed_index_lines)} lines)" if changed_index_lines else "")
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
