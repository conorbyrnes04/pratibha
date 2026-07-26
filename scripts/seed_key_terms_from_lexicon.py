#!/usr/bin/env python3
"""Seed key_terms layers on units that lack them, using lexicon lemma matches.

For each canonical unit without a non-empty key_terms layer, scan
original/iast/translation/commentary for lexicon aliases and scripts, then
inject up to N occurrence glosses with lemma_id/sense_id pointers.

Dry-run by default. Pass --write to patch data/canonical/**/*.yml + index.jsonl.

This is a coverage pass, not a finished editorial pass. Definitions use the
lemma sense short plus an optional local "Here:" clause when the commentary
mentions the term.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import tempfile
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "canonical"
INDEX = CANONICAL / "index.jsonl"
LEMMAS_DIR = ROOT / "data" / "lexicon" / "lemmas"

AFTER_KEYTERMS = {"resonances", "practice", "appendix"}
PAREN_RE = re.compile(r"\(([^)]+)\)")
NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")

# English gloss aliases that are too ambiguous to seed from alone.
WEAK_ALIASES = {
    "self",
    "fire",
    "time",
    "knowledge",
    "mind",
    "body",
    "world",
    "way",
    "the way",
    "power",
    "virtue",
    "soul",
    "spirit",
    "breath",
    "emptiness",
    "void",
    "yoga",
    "practice",
    "path",
    "truth",
    "one",
    "nature",
    "principle",
    "form",
    "dream",
    "bondage",
    "liberation",
    "awareness",
    "consciousness",
    "vibration",
    "throb",
    "wisdom",
    "knowing",
    "limitation",
    "portion",
    "transformation of things",
    "equalizing things",
    "cosmic fire",
}


def fold_key(value: str) -> str:
    text = unicodedata.normalize("NFKD", value or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().strip()
    text = NON_ALNUM_RE.sub("_", text).strip("_")
    return text


def has_key_terms(unit: dict[str, Any]) -> bool:
    return any(
        isinstance(layer, dict) and layer.get("kind") == "key_terms" and layer.get("items")
        for layer in unit.get("pratibha_layers") or []
    )


def insert_key_terms(unit: dict[str, Any], layer: dict[str, Any]) -> None:
    layers = unit.get("pratibha_layers")
    if not isinstance(layers, list):
        unit["pratibha_layers"] = [copy.deepcopy(layer)]
        return
    # Replace empty key_terms shell if present.
    for i, row in enumerate(layers):
        if isinstance(row, dict) and row.get("kind") == "key_terms":
            if not row.get("items"):
                layers[i] = copy.deepcopy(layer)
                return
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


def layer_body(unit: dict[str, Any], kind: str) -> str:
    for layer in unit.get("pratibha_layers") or []:
        if isinstance(layer, dict) and layer.get("kind") == kind:
            return str(layer.get("body") or "")
    # Flat fallbacks
    flat = {
        "original": unit.get("sanskrit_devanagari") or unit.get("sanskrit") or "",
        "iast": unit.get("sanskrit_iast") or unit.get("transliteration") or "",
        "translation": unit.get("translation") or unit.get("translation_literal") or "",
        "commentary": unit.get("commentary") or "",
    }
    return str(flat.get(kind) or "")


def haystack(unit: dict[str, Any]) -> str:
    parts = [
        layer_body(unit, "original"),
        layer_body(unit, "iast"),
        layer_body(unit, "translation"),
        layer_body(unit, "commentary"),
        str(unit.get("title") or ""),
    ]
    return "\n".join(parts)


def load_matchers() -> list[dict[str, Any]]:
    """Longest-first matchers: needle -> lemma metadata."""
    matchers: list[dict[str, Any]] = []
    for path in sorted(LEMMAS_DIR.glob("*.yml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            continue
        lemma_id = str(data.get("id") or path.stem).strip()
        senses = [s for s in (data.get("senses") or []) if isinstance(s, dict)]
        if not senses:
            continue
        # Prefer tradition-tagged first sense; keep all for later.
        primary = senses[0]
        sense_id = str(primary.get("id") or "")
        short = str(primary.get("short") or "").strip()
        scripts = data.get("scripts") if isinstance(data.get("scripts"), dict) else {}
        aliases = [str(a).strip() for a in (data.get("aliases") or []) if str(a).strip()]

        needles: list[tuple[str, str, int]] = []  # needle, kind, priority
        for key, val in scripts.items():
            val = str(val or "").strip()
            if not val:
                continue
            # Split dual forms like "kalā / kāla"
            for part in re.split(r"\s*/\s*", val):
                part = part.strip()
                if not part:
                    continue
                prio = 100 if key in {"devanagari", "chinese", "greek", "arabic"} else 80
                needles.append((part, "script", prio + len(part)))
        for alias in aliases:
            if alias.casefold() in WEAK_ALIASES:
                continue
            # Prefer non-ascii / diacritic-rich aliases
            prio = 50 + len(alias)
            if any(ord(ch) > 127 for ch in alias):
                prio += 20
            needles.append((alias, "alias", prio))

        # Always include lemma id and iast-like id forms
        needles.append((lemma_id.replace("_", " "), "id", 40))
        needles.append((lemma_id, "id", 40))

        # Dedup needles casefolding carefully for CJK
        seen: set[str] = set()
        for needle, kind, prio in needles:
            key = needle if any(ord(c) > 127 for c in needle) else needle.casefold()
            if key in seen or len(needle) < 2:
                continue
            seen.add(key)
            matchers.append(
                {
                    "needle": needle,
                    "kind": kind,
                    "prio": prio,
                    "lemma_id": lemma_id,
                    "sense_id": sense_id if len(senses) == 1 else "",
                    "short": short,
                    "display": str(scripts.get("iast") or scripts.get("pinyin") or scripts.get("greek") or lemma_id),
                    "script_native": str(
                        scripts.get("devanagari")
                        or scripts.get("chinese")
                        or scripts.get("greek")
                        or scripts.get("arabic")
                        or ""
                    ),
                }
            )

    matchers.sort(key=lambda m: (-m["prio"], -len(m["needle"])))
    return matchers


def find_here_clause(commentary: str, needle: str) -> str:
    if not commentary or not needle:
        return ""
    # Sentence containing needle (casefold for latin; exact for non-latin)
    non_latin = any(ord(c) > 127 for c in needle)
    chunks = re.split(r"(?<=[.!?。；;])\s+", commentary)
    for chunk in chunks:
        hit = (needle in chunk) if non_latin else (needle.casefold() in chunk.casefold())
        if hit:
            text = " ".join(chunk.split())
            if len(text) > 220:
                text = text[:217] + "…"
            return text
    return ""


def match_unit(unit: dict[str, Any], matchers: list[dict[str, Any]], limit: int) -> list[dict[str, str]]:
    text = haystack(unit)
    if not text.strip():
        return []
    commentary = layer_body(unit, "commentary")
    text_fold = text.casefold()
    used_lemmas: set[str] = set()
    items: list[dict[str, str]] = []

    for m in matchers:
        if len(items) >= limit:
            break
        lid = m["lemma_id"]
        if lid in used_lemmas:
            continue
        needle = m["needle"]
        non_latin = any(ord(c) > 127 for c in needle)
        if non_latin:
            if needle not in text:
                continue
        else:
            # wordish boundary for short latin needles
            if len(needle) <= 3:
                if not re.search(rf"(?<![a-z0-9]){re.escape(needle.casefold())}(?![a-z0-9])", text_fold):
                    continue
            elif needle.casefold() not in text_fold:
                continue

        used_lemmas.add(lid)
        display = m["display"]
        native = m["script_native"]
        if native and native not in display and "/" not in native:
            term = f"{display} ({native})" if display != native else native
        else:
            term = display

        definition = m["short"] or f"See lexicon entry `{lid}`."
        here = find_here_clause(commentary, needle)
        if not here:
            # try display / lemma id
            here = find_here_clause(commentary, display) or find_here_clause(commentary, lid)
        if here:
            definition = f"{definition} Here: {here}"

        item: dict[str, str] = {
            "term": term,
            "definition": definition,
            "lemma_id": lid,
        }
        if m["sense_id"]:
            item["sense_id"] = m["sense_id"]
        items.append(item)

    return items


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=str(path.parent)) as tmp:
        tmp.write(text)
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)


def dump_yaml(data: dict[str, Any]) -> str:
    return yaml.safe_dump(
        data,
        allow_unicode=True,
        sort_keys=False,
        width=100,
    )


def yaml_paths_by_unit() -> dict[str, Path]:
    out: dict[str, Path] = {}
    for path in CANONICAL.glob("*/*.yml"):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        uid = str(data.get("unit_id") or "")
        if not uid:
            # Infer from filename stem patterns used in corpus
            stem = path.stem
            # e.g. siva_sutra_ss_i_1 -> prefer unit_id from index later
            continue
        out[uid] = path
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--limit-per-unit", type=int, default=4)
    parser.add_argument("--collection", action="append", default=[], help="work_id filter; repeatable")
    parser.add_argument("--max-units", type=int, default=0, help="optional cap for testing")
    parser.add_argument("--overwrite", action="store_true", help="replace existing key_terms items")
    args = parser.parse_args()

    matchers = load_matchers()
    print(f"matchers={len(matchers)} lemmas_dir={LEMMAS_DIR}")

    lines = INDEX.read_text(encoding="utf-8").splitlines(keepends=True)
    units = [json.loads(line) for line in lines if line.strip()]
    yaml_by_uid = yaml_paths_by_unit()
    # Build stem->path fallback
    stem_paths = {p.stem: p for p in CANONICAL.glob("*/*.yml")}

    filters = set(args.collection)
    seeded = 0
    skipped_has = 0
    skipped_empty = 0
    items_total = 0
    by_work: Counter[str] = Counter()
    changed_index: list[int] = []

    for idx, unit in enumerate(units):
        work = str(unit.get("work_id") or "")
        if filters and work not in filters:
            continue
        if has_key_terms(unit) and not args.overwrite:
            skipped_has += 1
            continue
        items = match_unit(unit, matchers, args.limit_per_unit)
        if not items:
            skipped_empty += 1
            continue
        layer = {
            "kind": "key_terms",
            "label": "Key Terms",
            "items": items,
            "layer_provenance": "lexicon-seeded",
        }
        next_unit = copy.deepcopy(unit)
        if args.overwrite and has_key_terms(next_unit):
            next_unit["pratibha_layers"] = [
                layer if (isinstance(L, dict) and L.get("kind") == "key_terms") else L
                for L in (next_unit.get("pratibha_layers") or [])
            ]
            if not any(isinstance(L, dict) and L.get("kind") == "key_terms" for L in next_unit["pratibha_layers"]):
                insert_key_terms(next_unit, layer)
            else:
                # ensure items replaced
                for i, L in enumerate(next_unit["pratibha_layers"]):
                    if isinstance(L, dict) and L.get("kind") == "key_terms":
                        next_unit["pratibha_layers"][i] = copy.deepcopy(layer)
        else:
            insert_key_terms(next_unit, layer)

        seeded += 1
        items_total += len(items)
        by_work[work] += 1
        changed_index.append(idx)
        units[idx] = next_unit

        if args.max_units and seeded >= args.max_units:
            break

    print(f"would_seed_units={seeded} items={items_total} skipped_has={skipped_has} no_match={skipped_empty}")
    for work, n in by_work.most_common():
        print(f"  {work}: {n}")

    if not args.write:
        print("dry-run only; re-run with --write to apply")
        return

    # Write index
    new_lines = [json.dumps(u, ensure_ascii=False) + "\n" for u in units]
    atomic_write(INDEX, "".join(new_lines))

    # Write YAML companions when unit_id known
    yaml_written = 0
    for idx in changed_index:
        unit = units[idx]
        uid = str(unit.get("unit_id") or "")
        path = yaml_by_uid.get(uid)
        if path is None:
            # try filename conventions
            # work_id.unit_local -> work_id_unit_local with dots to underscores
            guess = uid.replace(".", "_")
            path = stem_paths.get(guess)
        if path is None:
            continue
        original = path.read_text(encoding="utf-8")
        data = yaml.safe_load(original)
        if not isinstance(data, dict):
            continue
        # Sync pratibha_layers key_terms from index unit
        kt = None
        for L in unit.get("pratibha_layers") or []:
            if isinstance(L, dict) and L.get("kind") == "key_terms":
                kt = L
                break
        if not kt:
            continue
        if "pratibha_layers" in data:
            insert_key_terms(data, kt)
            # if already had, insert_key_terms no-ops when items exist — force replace if overwrite
            if args.overwrite:
                for i, L in enumerate(data.get("pratibha_layers") or []):
                    if isinstance(L, dict) and L.get("kind") == "key_terms":
                        data["pratibha_layers"][i] = copy.deepcopy(kt)
        else:
            # attach layers from index for drifted files
            data["pratibha_layers"] = copy.deepcopy(unit.get("pratibha_layers") or [kt])
        atomic_write(path, dump_yaml(data))
        yaml_written += 1

    print(f"wrote index.jsonl ({seeded} units) and {yaml_written} YAML files")


if __name__ == "__main__":
    main()
