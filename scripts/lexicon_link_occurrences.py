#!/usr/bin/env python3
"""Attach lemma_id / sense_id pointers on canonical key_terms occurrences.

Matches occurrence `term` strings against lemma aliases and scripts in
data/lexicon/lemmas/. High-confidence exact matches only.

Dry-run is the default. Pass --write to patch canonical YAML + index.jsonl.
Never overwrites a non-empty definition; only adds ids when missing.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import tempfile
import unicodedata
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "canonical"
INDEX = CANONICAL / "index.jsonl"
LEMMAS_DIR = ROOT / "data" / "lexicon" / "lemmas"

PAREN_RE = re.compile(r"\(([^)]+)\)")
NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")


def fold_key(value: str) -> str:
    text = unicodedata.normalize("NFKD", value or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().strip()
    text = NON_ALNUM_RE.sub("_", text).strip("_")
    return text


def strip_script_parens(term: str) -> str:
    return " ".join(PAREN_RE.sub(" ", term or "").split())


def term_match_keys(term: str) -> set[str]:
    """Normalized keys that may identify this occurrence term."""
    keys: set[str] = set()
    raw = (term or "").strip()
    if not raw:
        return keys
    for candidate in (
        raw,
        strip_script_parens(raw),
        *[m.group(1).strip() for m in PAREN_RE.finditer(raw)],
    ):
        if not candidate:
            continue
        folded = fold_key(candidate)
        if folded:
            keys.add(folded)
        # Also keep exact lowercase (for CJK / Greek where fold may be empty-ish)
        lowered = candidate.lower().strip()
        if lowered:
            keys.add(f"lit:{lowered}")
    return keys


def load_lemma_index(lemmas_dir: Path) -> dict[str, list[dict[str, Any]]]:
    """match_key -> list of {lemma_id, sense_ids}."""
    index: dict[str, list[dict[str, Any]]] = {}
    if not lemmas_dir.is_dir():
        return index

    for path in sorted(lemmas_dir.glob("*.yml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        lemma_id = str(data.get("id") or path.stem).strip()
        if not lemma_id:
            continue
        senses = data.get("senses") if isinstance(data.get("senses"), list) else []
        sense_ids = [
            str(sense.get("id")).strip()
            for sense in senses
            if isinstance(sense, dict) and sense.get("id")
        ]
        entry = {"lemma_id": lemma_id, "sense_ids": sense_ids, "path": str(path)}

        surface_forms: list[str] = [lemma_id]
        aliases = data.get("aliases") or []
        if isinstance(aliases, list):
            surface_forms.extend(str(a) for a in aliases if a)
        scripts = data.get("scripts") or {}
        if isinstance(scripts, dict):
            surface_forms.extend(str(v) for v in scripts.values() if v)

        for form in surface_forms:
            for key in term_match_keys(form):
                index.setdefault(key, []).append(entry)
            # also index bare id fold
            fk = fold_key(form)
            if fk:
                index.setdefault(fk, []).append(entry)

    # Deduplicate lemma entries per key
    for key, entries in index.items():
        seen: set[str] = set()
        unique: list[dict[str, Any]] = []
        for entry in entries:
            lid = entry["lemma_id"]
            if lid in seen:
                continue
            seen.add(lid)
            unique.append(entry)
        index[key] = unique
    return index


def resolve_match(
    term: str, lemma_index: dict[str, list[dict[str, Any]]]
) -> tuple[str | None, str | None, str]:
    """Return (lemma_id, sense_id, reason). High-confidence only."""
    keys = term_match_keys(term)
    if not keys:
        return None, None, "empty_term"

    hits: dict[str, dict[str, Any]] = {}
    for key in keys:
        for entry in lemma_index.get(key, []):
            hits[entry["lemma_id"]] = entry

    if not hits:
        return None, None, "no_match"
    if len(hits) > 1:
        return None, None, f"ambiguous:{','.join(sorted(hits))}"

    entry = next(iter(hits.values()))
    lemma_id = entry["lemma_id"]
    sense_ids = entry["sense_ids"]
    sense_id = sense_ids[0] if len(sense_ids) == 1 else None
    reason = "exact_unique"
    if sense_id:
        reason += "+single_sense"
    return lemma_id, sense_id, reason


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


def link_items(
    items: list[Any], lemma_index: dict[str, list[dict[str, Any]]]
) -> tuple[list[Any], list[dict[str, str]], int]:
    """Return (new_items, link_events, changed_count)."""
    events: list[dict[str, str]] = []
    changed = 0
    new_items: list[Any] = []
    for item in items:
        if not isinstance(item, dict):
            new_items.append(item)
            continue
        next_item = copy.deepcopy(item)
        term = str(next_item.get("term") or "").strip()
        lemma_id, sense_id, reason = resolve_match(term, lemma_index)

        if not lemma_id:
            events.append({"term": term, "status": reason})
            new_items.append(next_item)
            continue

        item_changed = False
        if not next_item.get("lemma_id"):
            next_item["lemma_id"] = lemma_id
            item_changed = True
        elif str(next_item.get("lemma_id")) != lemma_id:
            # Never overwrite an existing different pointer.
            events.append(
                {
                    "term": term,
                    "status": "kept_existing_lemma",
                    "lemma_id": str(next_item.get("lemma_id")),
                    "candidate": lemma_id,
                }
            )
            new_items.append(next_item)
            continue

        if sense_id and not next_item.get("sense_id"):
            next_item["sense_id"] = sense_id
            item_changed = True

        # Explicitly do not touch definition.
        if item_changed:
            changed += 1
            events.append(
                {
                    "term": term,
                    "status": "linked",
                    "lemma_id": lemma_id,
                    "sense_id": sense_id or "",
                    "reason": reason,
                }
            )
        else:
            events.append(
                {
                    "term": term,
                    "status": "already_linked",
                    "lemma_id": str(next_item.get("lemma_id") or ""),
                }
            )
        new_items.append(next_item)
    return new_items, events, changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="Apply changes (default is dry-run).",
    )
    parser.add_argument(
        "--lemmas-dir",
        type=Path,
        default=LEMMAS_DIR,
        help=f"Lemma YAML directory (default: {LEMMAS_DIR})",
    )
    parser.add_argument(
        "--examples",
        type=int,
        default=12,
        help="How many link events to print.",
    )
    args = parser.parse_args()
    dry_run = not args.write

    lemma_index = load_lemma_index(args.lemmas_dir)
    lemma_files = list(args.lemmas_dir.glob("*.yml")) if args.lemmas_dir.is_dir() else []
    print(f"lemmas_dir={args.lemmas_dir}")
    print(f"lemma_files={len(lemma_files)}")
    print(f"match_keys={len(lemma_index)}")

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

    changed_index_lines: dict[int, str] = {}
    changed_yaml: dict[Path, dict[str, Any]] = {}
    stats = {
        "units_scanned": 0,
        "items_scanned": 0,
        "items_linked": 0,
        "units_changed": 0,
        "no_match": 0,
        "ambiguous": 0,
        "already_linked": 0,
        "kept_existing": 0,
    }
    sample_events: list[dict[str, str]] = []

    def kt_layer_indexes(unit: dict[str, Any]) -> list[int]:
        layers = unit.get("pratibha_layers") or []
        return [
            i
            for i, layer in enumerate(layers)
            if isinstance(layer, dict) and layer.get("kind") == "key_terms" and layer.get("items")
        ]

    for line_number, index_unit in enumerate(index_units):
        uid = str(index_unit["unit_id"])
        path, yaml_unit, _original_yaml = yaml_units[uid]

        index_kt = kt_layer_indexes(index_unit)
        yaml_kt = kt_layer_indexes(yaml_unit)
        if not index_kt and not yaml_kt:
            continue

        stats["units_scanned"] += 1
        next_index = copy.deepcopy(index_unit)
        next_yaml = copy.deepcopy(yaml_unit)
        index_changed = False
        yaml_changed = False

        for layer_i in index_kt:
            items = next_index["pratibha_layers"][layer_i].get("items") or []
            stats["items_scanned"] += len(items)
            new_items, events, changed = link_items(items, lemma_index)
            for event in events:
                status = event.get("status", "")
                if status == "no_match":
                    stats["no_match"] += 1
                elif status.startswith("ambiguous"):
                    stats["ambiguous"] += 1
                elif status == "already_linked":
                    stats["already_linked"] += 1
                elif status == "kept_existing_lemma":
                    stats["kept_existing"] += 1
                if status == "linked" and len(sample_events) < args.examples:
                    sample_events.append({"unit_id": uid, **event})
            if changed:
                next_index["pratibha_layers"][layer_i]["items"] = new_items
                stats["items_linked"] += changed
                index_changed = True

        for layer_i in yaml_kt:
            items = next_yaml["pratibha_layers"][layer_i].get("items") or []
            new_items, _events, changed = link_items(items, lemma_index)
            if changed:
                next_yaml["pratibha_layers"][layer_i]["items"] = new_items
                yaml_changed = True

        # If index gained ids and YAML still has a key_terms layer, mirror items.
        if index_changed and yaml_kt:
            for index_i, yaml_i in zip(index_kt, yaml_kt):
                next_yaml["pratibha_layers"][yaml_i]["items"] = copy.deepcopy(
                    next_index["pratibha_layers"][index_i]["items"]
                )
            yaml_changed = True

        if index_changed:
            changed_index_lines[line_number] = json.dumps(next_index, ensure_ascii=False) + "\n"
        if yaml_changed:
            changed_yaml[path] = next_yaml
        if index_changed or yaml_changed:
            stats["units_changed"] += 1

    print(f"units_with_key_terms_scanned={stats['units_scanned']}")
    print(f"items_scanned={stats['items_scanned']}")
    print(f"{'would link' if dry_run else 'linked'} items={stats['items_linked']}")
    print(f"units_changed={stats['units_changed']}")
    print(
        f"no_match={stats['no_match']} ambiguous={stats['ambiguous']} "
        f"already_linked={stats['already_linked']} kept_existing={stats['kept_existing']}"
    )
    if sample_events:
        print("\nexamples:")
        for event in sample_events:
            print(json.dumps(event, ensure_ascii=False))
    elif not lemma_files:
        print("\nNo lemma YAML files found yet; linker is ready for when Agent A seeds lemmas.")

    if dry_run:
        print("\ndry-run only; re-run with --write to apply")
        return 0

    for path, unit in changed_yaml.items():
        atomic_write(path, dump_yaml(unit))
    if changed_index_lines:
        new_lines = [
            changed_index_lines.get(i, original) for i, original in enumerate(original_lines)
        ]
        atomic_write(INDEX, "".join(new_lines))
    print(
        f"\nwrote {len(changed_yaml)} YAML files"
        + (
            f" and synchronized index.jsonl ({len(changed_index_lines)} lines)"
            if changed_index_lines
            else ""
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
