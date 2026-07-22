#!/usr/bin/env python3
"""Migrate resonance sections buried in canonical commentary into a layer.

This script edits data/canonical directly and keeps index.jsonl synchronized.
It never reads from or regenerates data/yaml.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import tempfile
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
CANONICAL = ROOT / "data" / "canonical"
INDEX = CANONICAL / "index.jsonl"

# Kept identical to scripts/audit/formatting.py.
RES_HEADER_RE = re.compile(r"cross[\s\-]*tradition\s+resonances?\s*[:\-]", re.I)
RES_LOOSE_RE = re.compile(r"^\s*(?:\*\*)?resonances?\s*[:\-]", re.I | re.M)
DIVERGENCE_RE = re.compile(r"^\s*[-*]?\s*\*?divergence\*?\s*[:\-]", re.I | re.M)

HEADER_LINE_RE = re.compile(
    r"(?im)^[ \t]*(?:#{1,6}[ \t]*)?cross[\s\-]*tradition\s+resonances?\s*[:\-][ \t]*$"
)
NEXT_SECTION_RE = re.compile(r"(?m)^[ \t]*#{1,6}[ \t]+\S")
BULLET_RE = re.compile(r"^\s*[-*]\s+(.*)$")
BOLD_ENTRY_RE = re.compile(r"^\s*\*\*(.+?):\*\*\s*(.*)$")
BULLET_BOLD_ENTRY_RE = re.compile(r"^\s*\*\s+\*\*(.+?):\*\*\s*(.*)$")
INLINE_BOLD_ENTRY_RE = re.compile(r"^\s*\*\*(.+?)\*\*\s+(.+)$")
EXPLICIT_DIVERGENCE_RE = re.compile(
    r"^\s*(?:[-*]\s+)?\*{0,2}divergence\*{0,2}\s*"
    r"[:\-]\*{0,2}\s*(.*)$",
    re.I,
)
INLINE_DIVERGENCE_RE = re.compile(
    r"\s+\*{0,2}divergence\*{0,2}\s*[:\-]\*{0,2}\s*", re.I
)
DIVERGENCE_CLAUSE_RE = re.compile(
    r"(?i)(?:(?<=^)|(?<=[,;:.!?])|(?<=\s[—–-]))\s*"
    r"(\b(?:but|however|whereas)\b.*|\bdiverges?\b.*)$"
)


def buried_in(text: str) -> bool:
    if not text:
        return False
    return bool(
        RES_HEADER_RE.search(text)
        or (RES_LOOSE_RE.search(text) and DIVERGENCE_RE.search(text))
    )


def normalized(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.lower().replace("&", " and ")
    return " ".join(re.findall(r"[a-z0-9]+", value))


def numeric_locus(value: str) -> tuple[int, ...]:
    return tuple(int(x) for x in re.findall(r"\d+", value))


class PassageResolver:
    """Conservatively resolve only unique, corpus-backed citation matches."""

    def __init__(self, units: list[dict[str, Any]]) -> None:
        self.units = units
        self.by_work: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self.work_aliases: dict[str, set[str]] = defaultdict(set)
        self.direct_aliases: dict[str, set[str]] = defaultdict(set)

        for unit in units:
            work_id = str(unit.get("work_id") or "")
            self.by_work[work_id].append(unit)
            for value in (work_id, str(unit.get("work_title") or "")):
                alias = normalized(value)
                if alias:
                    self.work_aliases[work_id].add(alias)

            for value in (
                str(unit.get("unit_id") or ""),
                str(unit.get("source_id") or ""),
            ):
                alias = self._zero_fold(normalized(value))
                if alias:
                    self.direct_aliases[alias].add(str(unit["unit_id"]))

    @staticmethod
    def _zero_fold(value: str) -> str:
        return " ".join(str(int(part)) if part.isdigit() else part for part in value.split())

    def resolve(self, citation: str) -> str:
        folded = self._zero_fold(normalized(citation))
        padded = f" {folded} "

        direct: set[str] = set()
        for alias, unit_ids in self.direct_aliases.items():
            if len(alias) >= 5 and f" {alias} " in padded:
                direct.update(unit_ids)
        if len(direct) == 1:
            return next(iter(direct))

        matching_works = [
            work_id
            for work_id, aliases in self.work_aliases.items()
            if any(
                len(alias) >= 5
                and f" {alias} " in padded
                for alias in aliases
            )
        ]
        if len(matching_works) != 1:
            return ""

        locus = numeric_locus(citation)
        if not locus:
            return ""
        candidates = []
        for unit in self.by_work[matching_works[0]]:
            source_locus = numeric_locus(str(unit.get("source_id") or ""))
            if source_locus == locus:
                candidates.append(str(unit["unit_id"]))
        return candidates[0] if len(candidates) == 1 else ""


def split_citation_and_body(text: str) -> tuple[str, str]:
    text = text.strip()
    bold = BOLD_ENTRY_RE.match(text)
    if bold:
        return bold.group(1).strip(), bold.group(2).strip()
    if ":" in text:
        citation, body = text.split(":", 1)
        return citation.strip(" *"), body.strip()
    for separator in (" — ", " – ", " - "):
        if separator in text:
            citation, body = text.split(separator, 1)
            return citation.strip(" *"), body.strip()
    raise ValueError(f"cannot split citation from resonance: {text!r}")


def split_divergence(body: str) -> tuple[str, str]:
    body = body.strip()
    match = DIVERGENCE_CLAUSE_RE.search(body)
    if not match:
        return body, ""
    resonance = body[: match.start()].rstrip(" ,;:—–-")
    divergence = match.group(1).strip()
    return resonance, divergence


def parse_entries(block: str, resolver: PassageResolver) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    current: dict[str, list[str] | str] | None = None

    def finish() -> None:
        nonlocal current
        if current is None:
            return
        citation = str(current["citation"]).strip()
        resonance_text = " ".join(str(x).strip() for x in current["body"] if str(x).strip())
        divergence_text = " ".join(
            str(x).strip() for x in current["divergence"] if str(x).strip()
        )
        inline_parts = INLINE_DIVERGENCE_RE.split(resonance_text, maxsplit=1)
        if len(inline_parts) == 2:
            resonance_text = inline_parts[0].strip()
            divergence_text = divergence_text or inline_parts[1].strip()
        resonance, inline_divergence = split_divergence(resonance_text)
        divergence = divergence_text or inline_divergence
        if not citation or not resonance:
            raise ValueError(
                f"incomplete resonance entry: citation={citation!r}, body={resonance_text!r}"
            )
        records.append(
            {
                "citation": citation,
                "resonance": resonance,
                "divergence": divergence,
                "passage_id": resolver.resolve(citation),
            }
        )
        current = None

    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        explicit_divergence = EXPLICIT_DIVERGENCE_RE.match(line)
        if explicit_divergence:
            if current is None:
                raise ValueError(f"divergence appears before a resonance: {line!r}")
            current["divergence"].append(explicit_divergence.group(1))
            continue

        bullet_bold = BULLET_BOLD_ENTRY_RE.match(raw_line)
        bold = BOLD_ENTRY_RE.match(raw_line)
        inline_bold = INLINE_BOLD_ENTRY_RE.match(raw_line)
        bullet = BULLET_RE.match(raw_line)
        if bullet_bold:
            finish()
            current = {
                "citation": bullet_bold.group(1).strip(),
                "body": [bullet_bold.group(2)],
                "divergence": [],
            }
        elif bold:
            finish()
            current = {
                "citation": bold.group(1).strip(),
                "body": [bold.group(2)],
                "divergence": [],
            }
        elif inline_bold:
            finish()
            current = {
                "citation": inline_bold.group(1).strip(),
                "body": [inline_bold.group(2)],
                "divergence": [],
            }
        elif bullet:
            finish()
            citation, body = split_citation_and_body(bullet.group(1))
            current = {"citation": citation, "body": [body], "divergence": []}
        elif current is not None:
            target = "divergence" if current["divergence"] else "body"
            current[target].append(line)
        else:
            raise ValueError(f"unrecognized text in resonance block: {line!r}")

    finish()
    if not records:
        raise ValueError("resonance block contained no entries")
    return records


def extract_block(commentary: str) -> tuple[str, str]:
    match = HEADER_LINE_RE.search(commentary)
    if not match:
        raise ValueError("detector matched commentary but no standalone resonance header was found")
    next_section = NEXT_SECTION_RE.search(commentary, match.end())
    end = next_section.start() if next_section else len(commentary)
    block = commentary[match.end() : end]
    prefix = commentary[: match.start()].rstrip()
    suffix = commentary[end:].lstrip()
    cleaned = (prefix + (f"\n\n{suffix}" if suffix else "")).strip()
    return cleaned, block


def has_structured_resonances(unit: dict[str, Any]) -> bool:
    return any(
        layer.get("kind") == "resonances"
        and (layer.get("items") or str(layer.get("body") or "").strip())
        for layer in unit.get("pratibha_layers") or []
        if isinstance(layer, dict)
    )


def migrate_unit(
    unit: dict[str, Any], resolver: PassageResolver
) -> tuple[bool, bool, list[dict[str, str]]]:
    commentary = str(unit.get("commentary") or "")
    if not buried_in(commentary):
        return False, False, []

    cleaned, block = extract_block(commentary)
    already_structured = has_structured_resonances(unit)
    items = [] if already_structured else parse_entries(block, resolver)
    unit["commentary"] = cleaned

    layers = unit.get("pratibha_layers")
    if not isinstance(layers, list):
        raise ValueError(f"{unit.get('unit_id')}: pratibha_layers is not a list")
    commentary_layers = [
        layer for layer in layers if isinstance(layer, dict) and layer.get("kind") == "commentary"
    ]
    if len(commentary_layers) != 1:
        raise ValueError(
            f"{unit.get('unit_id')}: expected one commentary layer, found {len(commentary_layers)}"
        )
    commentary_layers[0]["body"] = cleaned

    if not already_structured:
        new_layer = {
            "kind": "resonances",
            "label": "Cross-Tradition Resonances",
            "items": items,
            "layer_provenance": "migrated_from_commentary",
        }
        insertion = next(
            (
                index
                for index, layer in enumerate(layers)
                if isinstance(layer, dict)
                and layer.get("kind") in {"practice", "appendix"}
            ),
            len(layers),
        )
        layers.insert(insertion, new_layer)

    return True, already_structured, items


def load_index() -> tuple[list[str], list[dict[str, Any]]]:
    lines = INDEX.read_text(encoding="utf-8").splitlines(keepends=True)
    units = [json.loads(line) for line in lines if line.strip()]
    if len(lines) != len(units):
        raise ValueError("index.jsonl contains blank lines; refusing to rewrite ambiguously")
    for line, unit in zip(lines, units):
        regenerated = json.dumps(unit, ensure_ascii=False) + "\n"
        if regenerated.encode("utf-8") != line.encode("utf-8"):
            raise ValueError(
                f"index serialization mismatch before edits at {unit.get('unit_id')}"
            )
    return lines, units


def yaml_by_unit() -> dict[str, tuple[Path, dict[str, Any], str]]:
    result: dict[str, tuple[Path, dict[str, Any], str]] = {}
    for path in sorted(CANONICAL.glob("*/*.yml")):
        original = path.read_text(encoding="utf-8")
        unit = yaml.safe_load(original)
        if not isinstance(unit, dict) or not unit.get("unit_id"):
            raise ValueError(f"invalid canonical unit YAML: {path}")
        unit_id = str(unit["unit_id"])
        if unit_id in result:
            raise ValueError(f"duplicate unit_id in YAML files: {unit_id}")
        result[unit_id] = (path, unit, original)
    return result


def atomic_write(path: Path, content: str) -> None:
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        handle.write(content)
        temp_path = Path(handle.name)
    temp_path.replace(path)


def full_example(
    unit_id: str,
    before_commentary: str,
    after_commentary: str,
    items: list[dict[str, str]],
    redundant: bool,
) -> str:
    return (
        f"\n===== {unit_id} =====\n"
        f"BEFORE COMMENTARY:\n{before_commentary}\n\n"
        f"AFTER COMMENTARY:\n{after_commentary}\n\n"
        + (
            "STRUCTURED LAYER KEPT; REDUNDANT PROSE REMOVED\n"
            if redundant
            else "NEW RESONANCE ITEMS:\n"
            + json.dumps(items, ensure_ascii=False, indent=2)
            + "\n"
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run", action="store_true", help="show changes without writing files"
    )
    args = parser.parse_args()

    original_lines, index_units = load_index()
    yaml_units = yaml_by_unit()
    if set(yaml_units) != {str(unit["unit_id"]) for unit in index_units}:
        raise ValueError("YAML unit_ids and index.jsonl unit_ids do not match exactly")

    resolver = PassageResolver(index_units)
    changed: list[tuple[str, bool, list[dict[str, str]], str, str]] = []
    skipped: list[tuple[str, str]] = []
    changed_yaml: dict[Path, dict[str, Any]] = {}
    changed_index_lines: dict[int, str] = {}

    for line_number, index_unit in enumerate(index_units):
        unit_id = str(index_unit["unit_id"])
        path, yaml_unit, original_yaml = yaml_units[unit_id]
        if yaml_unit != index_unit:
            raise ValueError(f"{unit_id}: YAML content differs from index content before edits")

        before_commentary = str(index_unit.get("commentary") or "")
        next_index = copy.deepcopy(index_unit)
        next_yaml = copy.deepcopy(yaml_unit)
        try:
            index_result = migrate_unit(next_index, resolver)
            yaml_result = migrate_unit(next_yaml, resolver)
        except ValueError as error:
            skipped.append((unit_id, str(error)))
            continue
        if index_result != yaml_result or next_index != next_yaml:
            raise ValueError(f"{unit_id}: YAML/index migration results diverged")
        did_change, redundant, items = index_result
        if not did_change:
            continue
        roundtrip = yaml.safe_dump(
            yaml_unit,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
            width=120,
        )
        if roundtrip.encode("utf-8") != original_yaml.encode("utf-8"):
            raise ValueError(
                f"{unit_id}: YAML serializer would churn untouched formatting"
            )

        changed.append(
            (
                unit_id,
                redundant,
                items,
                before_commentary,
                str(next_index.get("commentary") or ""),
            )
        )
        changed_yaml[path] = next_yaml
        changed_index_lines[line_number] = json.dumps(next_index, ensure_ascii=False) + "\n"

    migrated = sum(not row[1] for row in changed)
    stripped_only = sum(row[1] for row in changed)
    resolved = sum(bool(item["passage_id"]) for row in changed for item in row[2])
    item_count = sum(len(row[2]) for row in changed)
    print(
        f"would change {len(changed)} units: migrate {migrated}, "
        f"strip redundant prose from {stripped_only}"
        if args.dry_run
        else f"changing {len(changed)} units: migrate {migrated}, "
        f"strip redundant prose from {stripped_only}"
    )
    print(f"new resonance items: {item_count}; confidently resolved passage_ids: {resolved}")
    print(f"skipped ambiguous units: {len(skipped)}")
    for unit_id, reason in skipped:
        print(f"SKIP {unit_id}: {reason}")
    for row in changed[:3]:
        print(full_example(row[0], row[3], row[4], row[2], row[1]))

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
    new_lines = [
        changed_index_lines.get(index, original)
        for index, original in enumerate(original_lines)
    ]
    atomic_write(INDEX, "".join(new_lines))
    print(f"wrote {len(changed_yaml)} YAML files and synchronized index.jsonl")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
