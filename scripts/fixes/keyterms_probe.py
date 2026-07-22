#!/usr/bin/env python3
"""Read-only audit of source and canonical key-term coverage."""
from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
YAML_ROOT_DEFAULT = ROOT / "data" / "yaml"
INDEX_DEFAULT = ROOT / "data" / "canonical" / "index.jsonl"
CANDIDATE_FIELDS = ("glossary", "key_terms", "terms", "keyterms", "vocabulary")


def _load_canonicalizer() -> Any:
    path = ROOT / "scripts" / "canonicalize_texts.py"
    spec = importlib.util.spec_from_file_location("canonicalize_texts", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _nonempty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, (list, dict, str)):
        return bool(value)
    return True


def _term_entries(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [
        row
        for row in value
        if isinstance(row, dict)
        and str(row.get("term") or "").strip()
        and str(row.get("definition") or row.get("meaning") or "").strip()
    ]


def _unwrap(raw: dict[str, Any], canonicalizer: Any) -> dict[str, Any]:
    return canonicalizer._coerce_wrapped_record(raw)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--yaml-root", type=Path, default=YAML_ROOT_DEFAULT)
    parser.add_argument("--index", type=Path, default=INDEX_DEFAULT)
    args = parser.parse_args()

    canonicalizer = _load_canonicalizer()
    files = canonicalizer.all_yaml_files(args.yaml_root)
    present = Counter()
    nonempty = Counter()
    emittable_files = Counter()
    emittable_entries = Counter()
    discovered_term_fields = Counter()
    work_glossary = Counter()
    work_key_terms = Counter()
    work_any_terms = Counter()
    canonical_by_work = Counter()
    parse_errors: list[str] = []
    source_with_any_terms = 0
    projected_units: dict[str, str] = {}

    for path in files:
        try:
            raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:
            parse_errors.append(f"{path}: {exc}")
            continue
        if not isinstance(raw, dict):
            continue
        record = _unwrap(raw, canonicalizer)
        work_id = canonicalizer.slug(
            str(record.get("collection") or path.parent.name)
        )

        has_any_terms = False
        for field in CANDIDATE_FIELDS:
            if field not in record:
                continue
            present[field] += 1
            value = record[field]
            if _nonempty(value):
                nonempty[field] += 1
            entries = _term_entries(value)
            if entries:
                emittable_files[field] += 1
                emittable_entries[field] += len(entries)
                has_any_terms = True
                if field == "glossary":
                    work_glossary[work_id] += 1
                elif field == "key_terms":
                    work_key_terms[work_id] += 1

        for field, value in record.items():
            if _term_entries(value):
                discovered_term_fields[str(field)] += 1

        if has_any_terms:
            source_with_any_terms += 1
            work_any_terms[work_id] += 1
        try:
            unit = canonicalizer.normalize(path, record)
            if any(
                isinstance(layer, dict) and layer.get("kind") == "key_terms"
                for layer in unit.get("pratibha_layers", [])
            ):
                projected_units[str(unit.get("unit_id") or "")] = str(
                    unit.get("work_id") or work_id
                )
        except Exception as exc:
            parse_errors.append(f"{path}: normalize failed: {exc}")

    canonical_units = 0
    canonical_with_key_terms = 0
    with args.index.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                unit = json.loads(line)
            except json.JSONDecodeError as exc:
                parse_errors.append(f"{args.index}:{line_number}: {exc}")
                continue
            canonical_units += 1
            if any(
                isinstance(layer, dict) and layer.get("kind") == "key_terms"
                for layer in unit.get("pratibha_layers", [])
            ):
                canonical_with_key_terms += 1
                canonical_by_work[str(unit.get("work_id") or "unknown")] += 1

    print(f"source_yaml_files={len(files)}")
    for field in CANDIDATE_FIELDS:
        print(
            f"{field}: present={present[field]} non_empty={nonempty[field]} "
            f"files_with_term_definitions={emittable_files[field]} "
            f"term_definition_entries={emittable_entries[field]}"
        )
    print(f"source_files_with_any_term_content={source_with_any_terms}")
    discovered = ", ".join(
        f"{field}={count}" for field, count in sorted(discovered_term_fields.items())
    )
    print(f"fields_holding_term_definition_data={discovered or 'none'}")
    print(f"canonical_index_units={canonical_units}")
    print(f"canonical_units_with_key_terms_layer={canonical_with_key_terms}")
    print(
        "projected_unique_units_with_key_terms_after_current_patch="
        f"{len(projected_units)}"
    )
    projected_by_work = Counter(projected_units.values())
    works = sorted(
        set(work_any_terms) | set(projected_by_work) | set(canonical_by_work)
    )
    print("per_work_term_coverage:")
    for work_id in works:
        print(
            f"  {work_id}: glossary_sources={work_glossary[work_id]} "
            f"key_terms_sources={work_key_terms[work_id]} "
            f"any_term_sources={work_any_terms[work_id]} "
            f"projected_units={projected_by_work[work_id]} "
            f"canonical_current={canonical_by_work[work_id]}"
        )
    print(f"parse_or_normalize_errors={len(parse_errors)}")
    for error in parse_errors:
        print(f"ERROR {error}")
    return 1 if parse_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
