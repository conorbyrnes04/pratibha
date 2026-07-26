#!/usr/bin/env python3
"""Enrich key_terms for Vijnana Bhairava + Yoga Spandakarika units.

Promotes passage-aware Key Terms already authored in each unit's top-level
commentary into pratibha_layers key_terms items, rewriting definitions to:

  etymology/root hint → meaning in THIS passage → what default English misses

Sets layer_provenance: editorial-enriched. Attaches lemma_id/sense_id when
known (lexicon lemmas or curated meta). Syncs per-unit YAML + index.jsonl.

Dry-run by default. Pass --write to apply.
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
LEMMAS_DIR = ROOT / "data" / "lexicon" / "lemmas"
TERM_META_PATH = ROOT / "scripts" / "data" / "shaiva_term_meta.json"

WORK_IDS = {"vijnana_bhairava", "yoga_spandakarika"}
AFTER_KEYTERMS = {"resonances", "practice", "appendix"}

KT_BLOCK_RE = re.compile(r"Key Terms\s*(.*)$", re.S | re.I)
KT_ITEM_RE = re.compile(
    r"\*\*([^*]+)\*\*\s*[—–\-]\s*(.+?)(?=\n\s*\*\*|\n\s*\n\s*\n|\Z)",
    re.S,
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


def load_term_meta() -> dict[str, dict[str, Any]]:
    return json.loads(TERM_META_PATH.read_text(encoding="utf-8"))


def load_lemmas() -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for path in sorted(LEMMAS_DIR.glob("*.yml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            continue
        lemma_id = str(data.get("id") or path.stem)
        senses = [s for s in (data.get("senses") or []) if isinstance(s, dict)]
        sense = next(
            (
                s
                for s in senses
                if "shaiva" in str(s.get("id") or "")
                or "kashmir_shaivism" in (s.get("traditions") or [])
            ),
            senses[0] if senses else None,
        )
        scripts = data.get("scripts") if isinstance(data.get("scripts"), dict) else {}
        out[lemma_id] = {
            "iast": str(scripts.get("iast") or lemma_id),
            "devanagari": str(scripts.get("devanagari") or ""),
            "etymology": str((sense or {}).get("etymology") or ""),
            "traps": [str(t) for t in ((sense or {}).get("traps") or [])],
            "sense_id": str((sense or {}).get("id") or ""),
        }
    return out


def extract_commentary_key_terms(commentary: str) -> list[dict[str, str]]:
    m = KT_BLOCK_RE.search(commentary or "")
    if not m:
        return []
    items: list[dict[str, str]] = []
    for match in KT_ITEM_RE.finditer(m.group(1)):
        term = " ".join(match.group(1).split()).strip()
        definition = " ".join(match.group(2).split()).strip()
        if term and definition:
            items.append({"term": term, "definition": definition})
    return items


def clean_passage_meaning(definition: str) -> str:
    text = " ".join((definition or "").split()).strip()
    # Drop leading "Literally …;" / "Literally … —" — etymology covers that work.
    text = re.sub(
        r"^[Ll]iterally\s+.+?(?:[;:—–\-]\s+|\.\s+)",
        "",
        text,
        count=1,
    )
    # Soften leading capitalization for mid-definition flow.
    if text and text[0].isupper() and not text[:2].isupper():
        first = text.split()[0]
        keep = {"Bhairava", "Śakti", "Śiva", "Śaṅkara", "OM", "OṂ"}
        if first not in keep and not first.isupper():
            text = text[0].lower() + text[1:]
    return text.rstrip(".")


def format_term_label(term: str, dewa: str | None) -> str:
    term = term.strip()
    if not dewa:
        return term
    # Already has Devanagari in parentheses.
    if re.search(r"\([\u0900-\u097F]", term):
        return term
    # Strip latin parenthetical notes (e.g. apāna) before attaching script.
    base = re.sub(r"\s*\((?![^\)]*[\u0900-\u097F])[^)]*\)", "", term).strip()
    base = re.sub(r"\s+", " ", base)
    return f"{base} ({dewa})"


def compose_definition(
    passage: str,
    meta: dict[str, Any] | None,
    lemma: dict[str, Any] | None,
) -> str:
    etym = ""
    misses = ""
    if meta:
        etym = str(meta.get("etymology") or "").strip()
        misses = str(meta.get("misses") or "").strip()
    if not etym and lemma:
        etym = str(lemma.get("etymology") or "").strip()
    if not misses and lemma and lemma.get("traps"):
        traps = lemma["traps"][:2]
        misses = "default English slides into " + " / ".join(traps)
    if not etym:
        etym = "technical Śaiva usage"
    if not misses:
        misses = "stock English glosses drop the operative force this verse gives the term"
    passage = clean_passage_meaning(passage)
    return f"{etym} → {passage} → {misses}"


def build_items(
    commentary_items: list[dict[str, str]],
    term_meta: dict[str, dict[str, Any]],
    lemmas: dict[str, dict[str, Any]],
) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for row in commentary_items[:5]:
        term = row["term"]
        meta = term_meta.get(term)
        lemma_id = (meta or {}).get("lemma_id")
        sense_id = (meta or {}).get("sense_id")
        lemma = lemmas.get(lemma_id) if lemma_id else None
        dewa = (meta or {}).get("devanagari") or (lemma or {}).get("devanagari") or ""
        # Prefer lexicon etymology when lemma linked and meta etym is thin? Keep meta first.
        definition = compose_definition(row["definition"], meta, lemma)
        item: dict[str, str] = {
            "term": format_term_label(term, dewa or None),
            "definition": definition,
        }
        if lemma_id:
            item["lemma_id"] = str(lemma_id)
        if sense_id:
            item["sense_id"] = str(sense_id)
        elif lemma and lemma.get("sense_id"):
            item["sense_id"] = str(lemma["sense_id"])
        items.append(item)
    return items


def set_key_terms_layer(unit: dict[str, Any], layer: dict[str, Any]) -> None:
    layers = unit.get("pratibha_layers")
    if not isinstance(layers, list):
        unit["pratibha_layers"] = [copy.deepcopy(layer)]
        return
    for i, row in enumerate(layers):
        if isinstance(row, dict) and row.get("kind") == "key_terms":
            layers[i] = copy.deepcopy(layer)
            return
    insertion = next(
        (
            i
            for i, row in enumerate(layers)
            if isinstance(row, dict) and row.get("kind") in AFTER_KEYTERMS
        ),
        len(layers),
    )
    layers.insert(insertion, copy.deepcopy(layer))


def yaml_paths_by_unit() -> dict[str, Path]:
    out: dict[str, Path] = {}
    for path in CANONICAL.glob("*/*.yml"):
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
    args = parser.parse_args()

    term_meta = load_term_meta()
    lemmas = load_lemmas()
    yaml_by_uid = yaml_paths_by_unit()

    lines = INDEX.read_text(encoding="utf-8").splitlines(keepends=True)
    units = [json.loads(line) for line in lines if line.strip()]
    if len(lines) != len(units):
        raise SystemExit("index.jsonl has blank lines; refusing to rewrite")

    # Index commentary is often a short insight stub; full Key Terms live in YAML.
    yaml_commentary: dict[str, str] = {}
    yaml_units: dict[str, dict[str, Any]] = {}
    for uid, path in yaml_by_uid.items():
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        if str(data.get("work_id") or "") not in WORK_IDS:
            continue
        yaml_units[uid] = data
        yaml_commentary[uid] = str(data.get("commentary") or "")

    want_uids = set(args.unit_id)
    changed = 0
    empty = 0
    lemma_linked = 0
    items_total = 0
    by_work: Counter[str] = Counter()
    provenance_before: Counter[str] = Counter()
    examples: list[tuple[str, list[dict[str, str]]]] = []
    changed_idxs: list[int] = []

    for idx, unit in enumerate(units):
        work = str(unit.get("work_id") or "")
        if work not in WORK_IDS:
            continue
        uid = str(unit.get("unit_id") or "")
        if want_uids and uid not in want_uids:
            continue

        # Provenance before
        old_prov = ""
        for row in unit.get("pratibha_layers") or []:
            if isinstance(row, dict) and row.get("kind") == "key_terms":
                old_prov = str(row.get("layer_provenance") or "")
                break
        provenance_before[old_prov or "(none)"] += 1

        commentary_src = yaml_commentary.get(uid) or str(unit.get("commentary") or "")
        commentary_items = extract_commentary_key_terms(commentary_src)
        if not commentary_items:
            empty += 1
            print(f"WARN no commentary Key Terms: {uid}")
            continue

        items = build_items(commentary_items, term_meta, lemmas)
        if not items:
            empty += 1
            continue

        layer = {
            "kind": "key_terms",
            "label": "Key Terms",
            "items": items,
            "layer_provenance": "editorial-enriched",
        }
        next_unit = copy.deepcopy(unit)
        set_key_terms_layer(next_unit, layer)
        units[idx] = next_unit
        changed_idxs.append(idx)
        changed += 1
        items_total += len(items)
        by_work[work] += 1
        lemma_linked += sum(1 for it in items if it.get("lemma_id"))
        if len(examples) < 2:
            examples.append((uid, items))

        if args.max_units and changed >= args.max_units:
            break

    print(
        f"units_enriched={changed} items={items_total} "
        f"lemma_links={lemma_linked} missing_commentary_kt={empty}"
    )
    print("by_work:", dict(by_work))
    print("provenance_before:", dict(provenance_before))
    for uid, items in examples:
        print(f"\nexample {uid}:")
        for it in items:
            print(f"  - {it['term']}")
            print(f"    {it['definition'][:160]}…")

    if not args.write:
        print("\ndry-run only; re-run with --write to apply")
        return

    new_lines = [json.dumps(u, ensure_ascii=False) + "\n" for u in units]
    atomic_write(INDEX, "".join(new_lines))

    yaml_written = 0
    for idx in changed_idxs:
        unit = units[idx]
        uid = str(unit.get("unit_id") or "")
        path = yaml_by_uid.get(uid)
        if path is None:
            print(f"WARN no YAML path for {uid}")
            continue
        data = yaml_units.get(uid) or yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            continue
        kt = next(
            (
                L
                for L in unit.get("pratibha_layers") or []
                if isinstance(L, dict) and L.get("kind") == "key_terms"
            ),
            None,
        )
        if not kt:
            continue
        set_key_terms_layer(data, kt)
        atomic_write(path, dump_yaml(data))
        yaml_written += 1

    print(f"wrote index.jsonl and {yaml_written} YAML files")


if __name__ == "__main__":
    main()
