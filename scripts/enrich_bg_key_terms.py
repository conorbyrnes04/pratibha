#!/usr/bin/env python3
"""Promote buried Bhagavad Gītā Key Terms into structured pratibha_layers.

The verse-scale BG rebuild authored Key Terms inside each unit's commentary
(etymology → passage sense → translation trap). This script:

  1. Parses that Key Terms block
  2. Writes a ``key_terms`` layer with ``term`` / ``definition`` items
  3. Strips the Key Terms (+ trailing Cross-Tradition Resonances) block from
     stored commentary so the study view does not duplicate
  4. Syncs ``data/canonical/bhagavad_gita/*.yml`` + ``data/canonical/index.jsonl``

Definitions are preserved as authored (unlike the VBT enricher, which rewrites
them). Soft ``lemma_id`` attachment happens later via
``lexicon_link_occurrences.py``.

Dry-run by default. Pass ``--write`` to apply.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "canonical"
INDEX = CANONICAL / "index.jsonl"
WORK_ID = "bhagavad_gita"
AFTER_KEYTERMS = {"resonances", "practice", "appendix"}

# Capture from "Key Terms" through end of commentary (resonances often follow).
KT_BLOCK_RE = re.compile(
    r"(?ms)^[ \t]*Key Terms:?[ \t]*\n(.*)$",
)
KT_ITEM_RE = re.compile(
    r"\*\*([^*]+)\*\*\s*[—–\-]\s*(.+?)(?=\n\s*\*\*|\n\s*Cross-Tradition|\n\s*Practice|\Z)",
    re.S | re.I,
)
# Strip Key Terms and anything after that was meant as separate layers.
STRIP_FROM_KT_RE = re.compile(
    r"(?ms)\n*[ \t]*Key Terms:?[ \t]*\n.*\Z",
)


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", delete=False, dir=str(path.parent)
    ) as tmp:
        tmp.write(text)
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)


def dump_yaml(data: dict[str, Any]) -> str:
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=100)


def extract_commentary_key_terms(commentary: str) -> list[dict[str, str]]:
    m = KT_BLOCK_RE.search(commentary or "")
    if not m:
        return []
    items: list[dict[str, str]] = []
    for match in KT_ITEM_RE.finditer(m.group(1)):
        term = " ".join(match.group(1).split()).strip()
        definition = " ".join(match.group(2).split()).strip().rstrip(".")
        if term and definition:
            items.append({"term": term, "definition": definition})
    return items


def strip_buried_layers(commentary: str) -> str:
    """Remove Key Terms (+ Resonances that follow) from commentary body."""
    text = STRIP_FROM_KT_RE.sub("", commentary or "").rstrip()
    # Also drop a trailing Cross-Tradition block if it somehow precedes KT.
    text = re.sub(
        r"(?ms)\n*[ \t]*Cross-Tradition Resonances:?[ \t]*\n.*\Z",
        "",
        text,
    ).rstrip()
    return text


def extract_resonances(commentary: str) -> list[dict[str, str]]:
    """Best-effort parse of buried Cross-Tradition Resonances for promotion."""
    m = re.search(
        r"(?ms)^[ \t]*Cross-Tradition Resonances:?[ \t]*\n(.*?)(?=\n[ \t]*Practice|\Z)",
        commentary or "",
    )
    if not m:
        return []
    block = m.group(1)
    items: list[dict[str, str]] = []
    # **Citation:** resonance text\n*Divergence:* ...
    pattern = re.compile(
        r"\*\*([^*]+)\*\*:\s*(.+?)(?=\n\s*\*\*|\Z)",
        re.S,
    )
    for match in pattern.finditer(block):
        citation = " ".join(match.group(1).split()).strip()
        body = match.group(2).strip()
        resonance = body
        divergence = ""
        div_m = re.search(r"\*?Divergence:\*?\s*(.+)\Z", body, re.S | re.I)
        if div_m:
            divergence = " ".join(div_m.group(1).split()).strip()
            resonance = " ".join(body[: div_m.start()].split()).strip()
        if citation and resonance:
            row: dict[str, str] = {
                "citation": citation,
                "resonance": resonance,
                "passage_id": "",
            }
            if divergence:
                row["divergence"] = divergence
            items.append(row)
    return items


def set_layer(unit: dict[str, Any], layer: dict[str, Any]) -> None:
    kind = str(layer.get("kind") or "")
    layers = unit.get("pratibha_layers")
    if not isinstance(layers, list):
        unit["pratibha_layers"] = [copy.deepcopy(layer)]
        return
    for i, row in enumerate(layers):
        if isinstance(row, dict) and row.get("kind") == kind:
            layers[i] = copy.deepcopy(layer)
            return
    if kind == "key_terms":
        insertion = next(
            (
                i
                for i, row in enumerate(layers)
                if isinstance(row, dict) and row.get("kind") in AFTER_KEYTERMS
            ),
            len(layers),
        )
        layers.insert(insertion, copy.deepcopy(layer))
        return
    if kind == "resonances":
        insertion = next(
            (
                i
                for i, row in enumerate(layers)
                if isinstance(row, dict) and row.get("kind") in {"practice", "appendix"}
            ),
            len(layers),
        )
        layers.insert(insertion, copy.deepcopy(layer))
        return
    layers.append(copy.deepcopy(layer))


def set_commentary_bodies(unit: dict[str, Any], clean: str) -> None:
    unit["commentary"] = clean
    layers = unit.get("pratibha_layers")
    if not isinstance(layers, list):
        return
    for row in layers:
        if isinstance(row, dict) and row.get("kind") == "commentary":
            row["body"] = clean


def yaml_paths_for_work(work_id: str) -> dict[str, Path]:
    out: dict[str, Path] = {}
    work_dir = CANONICAL / work_id
    if not work_dir.is_dir():
        return out
    for path in work_dir.glob("*.yml"):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(data, dict) and data.get("unit_id"):
            out[str(data["unit_id"])] = path
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--max-units", type=int, default=0)
    parser.add_argument("--unit-id", action="append", default=[])
    parser.add_argument(
        "--promote-resonances",
        action="store_true",
        help="Also promote Cross-Tradition Resonances buried in commentary",
    )
    args = parser.parse_args()

    yaml_by_uid = yaml_paths_for_work(WORK_ID)
    lines = INDEX.read_text(encoding="utf-8").splitlines(keepends=True)
    units = [json.loads(line) for line in lines if line.strip()]
    if len(lines) != len(units):
        raise SystemExit("index.jsonl has blank lines; refusing to rewrite")

    want_uids = set(args.unit_id)
    changed = 0
    empty = 0
    items_total = 0
    resonance_units = 0
    examples: list[tuple[str, list[dict[str, str]]]] = []
    changed_idxs: list[int] = []
    yaml_cache: dict[str, dict[str, Any]] = {}

    for idx, unit in enumerate(units):
        if str(unit.get("work_id") or "") != WORK_ID:
            continue
        uid = str(unit.get("unit_id") or "")
        if want_uids and uid not in want_uids:
            continue

        path = yaml_by_uid.get(uid)
        commentary = ""
        ydata: dict[str, Any] | None = None
        if path is not None:
            try:
                ydata = yaml.safe_load(path.read_text(encoding="utf-8"))
            except Exception:
                ydata = None
            if isinstance(ydata, dict):
                yaml_cache[uid] = ydata
                commentary = str(ydata.get("commentary") or "")
                if not commentary:
                    for row in ydata.get("pratibha_layers") or []:
                        if isinstance(row, dict) and row.get("kind") == "commentary":
                            commentary = str(row.get("body") or "")
                            break
        if not commentary:
            commentary = str(unit.get("commentary") or "")
            for row in unit.get("pratibha_layers") or []:
                if isinstance(row, dict) and row.get("kind") == "commentary":
                    commentary = str(row.get("body") or commentary)
                    break

        # Prefer already-structured layer if present and non-empty.
        existing_items: list[dict[str, str]] = []
        for row in unit.get("pratibha_layers") or []:
            if isinstance(row, dict) and row.get("kind") == "key_terms":
                for it in row.get("items") or []:
                    if isinstance(it, dict) and it.get("term") and it.get("definition"):
                        existing_items.append(
                            {
                                "term": str(it["term"]),
                                "definition": str(it["definition"]),
                                **(
                                    {"lemma_id": str(it["lemma_id"])}
                                    if it.get("lemma_id")
                                    else {}
                                ),
                                **(
                                    {"sense_id": str(it["sense_id"])}
                                    if it.get("sense_id")
                                    else {}
                                ),
                            }
                        )
                break

        commentary_items = extract_commentary_key_terms(commentary)
        items = existing_items or commentary_items
        if not items:
            empty += 1
            print(f"WARN no Key Terms: {uid}")
            continue

        next_unit = copy.deepcopy(unit)
        set_layer(
            next_unit,
            {
                "kind": "key_terms",
                "label": "Key Terms",
                "items": items,
                "layer_provenance": "promoted-from-commentary",
            },
        )

        if args.promote_resonances:
            # Prefer structured; else parse buried block before strip.
            has_res = any(
                isinstance(r, dict) and r.get("kind") == "resonances" and r.get("items")
                for r in (next_unit.get("pratibha_layers") or [])
            )
            if not has_res:
                res_items = extract_resonances(commentary)
                if res_items:
                    set_layer(
                        next_unit,
                        {
                            "kind": "resonances",
                            "label": "Cross-Tradition Resonances",
                            "items": res_items,
                            "layer_provenance": "promoted-from-commentary",
                        },
                    )
                    resonance_units += 1

        clean = strip_buried_layers(commentary)
        set_commentary_bodies(next_unit, clean)

        units[idx] = next_unit
        changed_idxs.append(idx)
        changed += 1
        items_total += len(items)
        if len(examples) < 3:
            examples.append((uid, items))

        if args.max_units and changed >= args.max_units:
            break

    print(
        f"units_enriched={changed} items={items_total} "
        f"missing_kt={empty} resonances_promoted={resonance_units}"
    )
    for uid, items in examples:
        print(f"\nexample {uid}:")
        for it in items[:4]:
            print(f"  - {it['term']}")
            print(f"    {it['definition'][:140]}")

    if not args.write:
        print("\ndry-run only; re-run with --write to apply")
        return

    atomic_write(INDEX, "".join(json.dumps(u, ensure_ascii=False) + "\n" for u in units))

    yaml_written = 0
    for idx in changed_idxs:
        unit = units[idx]
        uid = str(unit.get("unit_id") or "")
        path = yaml_by_uid.get(uid)
        if path is None:
            print(f"WARN no YAML path for {uid}")
            continue
        data = yaml_cache.get(uid) or yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            continue
        for kind in ("key_terms", "resonances", "commentary"):
            layer = next(
                (
                    L
                    for L in unit.get("pratibha_layers") or []
                    if isinstance(L, dict) and L.get("kind") == kind
                ),
                None,
            )
            if layer:
                set_layer(data, layer)
        if "commentary" in unit:
            data["commentary"] = unit["commentary"]
        atomic_write(path, dump_yaml(data))
        yaml_written += 1

    print(f"wrote index.jsonl and {yaml_written} YAML files")


if __name__ == "__main__":
    main()
