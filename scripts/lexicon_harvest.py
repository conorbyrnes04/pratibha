#!/usr/bin/env python3
"""Harvest key_terms occurrences into a clustered lexicon candidate file.

Scans canonical key_terms (and optionally source YAML glossary/key_terms),
normalizes terms for clustering, and writes data/lexicon/_harvest.json.

Does NOT create lemma YAML — editorial seeds belong to Agent A.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import unicodedata
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "canonical"
INDEX = CANONICAL / "index.jsonl"
YAML_ROOT = ROOT / "data" / "yaml"
OUT_DEFAULT = ROOT / "data" / "lexicon" / "_harvest.json"

PAREN_RE = re.compile(r"\(([^)]+)\)")
NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")


def fold_key(value: str) -> str:
    """Lowercase ASCII-fold grouping key (diacritics stripped)."""
    text = unicodedata.normalize("NFKD", value or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().strip()
    text = NON_ALNUM_RE.sub("_", text).strip("_")
    return text


def strip_script_parens(term: str) -> str:
    return " ".join(PAREN_RE.sub(" ", term or "").split())


def extract_variants(term: str) -> list[str]:
    """Primary form (parens stripped) plus parenthetical script forms."""
    raw = (term or "").strip()
    if not raw:
        return []
    variants: list[str] = []
    primary = strip_script_parens(raw)
    if primary:
        variants.append(primary)
    for match in PAREN_RE.finditer(raw):
        inner = " ".join(match.group(1).split())
        if inner and inner not in variants:
            variants.append(inner)
    if raw not in variants:
        variants.append(raw)
    return variants


def suggest_lemma_id(term: str) -> str:
    primary = strip_script_parens(term)
    slug = fold_key(primary)
    return slug or fold_key(term) or "unknown"


def load_canonicalizer() -> Any:
    path = ROOT / "scripts" / "canonicalize_texts.py"
    spec = importlib.util.spec_from_file_location("canonicalize_texts", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def iter_canonical_occurrences() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with INDEX.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            unit = json.loads(line)
            uid = str(unit.get("unit_id") or "")
            work_id = str(unit.get("work_id") or "unknown")
            collection = str(unit.get("collection") or work_id)
            for layer in unit.get("pratibha_layers") or []:
                if not isinstance(layer, dict) or layer.get("kind") != "key_terms":
                    continue
                for item in layer.get("items") or []:
                    if not isinstance(item, dict):
                        continue
                    term = str(item.get("term") or "").strip()
                    if not term:
                        continue
                    rows.append(
                        {
                            "term": term,
                            "definition": str(item.get("definition") or "").strip(),
                            "unit_id": uid,
                            "work_id": work_id,
                            "collection": collection,
                            "source": "canonical",
                            "lemma_id": item.get("lemma_id"),
                            "sense_id": item.get("sense_id"),
                        }
                    )
    return rows


def iter_source_occurrences(canon: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
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
        uid = str(unit.get("unit_id") or "")
        work_id = str(unit.get("work_id") or "unknown")
        collection = str(record.get("collection") or work_id)
        for layer in unit.get("pratibha_layers") or []:
            if not isinstance(layer, dict) or layer.get("kind") != "key_terms":
                continue
            for item in layer.get("items") or []:
                if not isinstance(item, dict):
                    continue
                term = str(item.get("term") or "").strip()
                if not term:
                    continue
                rows.append(
                    {
                        "term": term,
                        "definition": str(item.get("definition") or "").strip(),
                        "unit_id": uid,
                        "work_id": work_id,
                        "collection": collection,
                        "source": "source_yaml",
                    }
                )
    return rows


def cluster_occurrences(rows: list[dict[str, Any]], sample_limit: int = 8) -> list[dict[str, Any]]:
    clusters: dict[str, dict[str, Any]] = {}

    for row in rows:
        variants = extract_variants(row["term"])
        # Prefer the folded primary (parens stripped) as the cluster key.
        primary = variants[0] if variants else row["term"]
        key = fold_key(primary) or fold_key(row["term"])
        if not key:
            continue
        cluster = clusters.get(key)
        if cluster is None:
            cluster = {
                "cluster_key": key,
                "suggested_lemma_id": suggest_lemma_id(row["term"]),
                "variants": [],
                "variant_counts": defaultdict(int),
                "count": 0,
                "collections": set(),
                "work_ids": set(),
                "sample_passage_ids": [],
                "sample_definitions": [],
                "linked_lemma_ids": set(),
            }
            clusters[key] = cluster

        cluster["count"] += 1
        cluster["collections"].add(row["collection"])
        cluster["work_ids"].add(row["work_id"])
        for variant in variants:
            cluster["variant_counts"][variant] += 1
        if row["unit_id"] and row["unit_id"] not in cluster["sample_passage_ids"]:
            if len(cluster["sample_passage_ids"]) < sample_limit:
                cluster["sample_passage_ids"].append(row["unit_id"])
        definition = row.get("definition") or ""
        if definition and definition not in cluster["sample_definitions"]:
            if len(cluster["sample_definitions"]) < 3:
                cluster["sample_definitions"].append(definition)
        if row.get("lemma_id"):
            cluster["linked_lemma_ids"].add(str(row["lemma_id"]))

    out: list[dict[str, Any]] = []
    for key, cluster in clusters.items():
        variant_counts = cluster["variant_counts"]
        variants_sorted = sorted(variant_counts.keys(), key=lambda v: (-variant_counts[v], v))
        # Prefer a roman/ascii-friendly variant for suggested id when available.
        suggested = cluster["suggested_lemma_id"]
        for variant in variants_sorted:
            candidate = suggest_lemma_id(variant)
            if candidate and re.search(r"[a-z]", candidate):
                suggested = candidate
                break
        out.append(
            {
                "cluster_key": key,
                "suggested_lemma_id": suggested,
                "variants": variants_sorted,
                "variant_counts": {v: variant_counts[v] for v in variants_sorted},
                "count": cluster["count"],
                "collections": sorted(cluster["collections"]),
                "work_ids": sorted(cluster["work_ids"]),
                "sample_passage_ids": cluster["sample_passage_ids"],
                "sample_definitions": cluster["sample_definitions"],
                "linked_lemma_ids": sorted(cluster["linked_lemma_ids"]),
            }
        )
    out.sort(key=lambda row: (-row["count"], row["cluster_key"]))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--include-source",
        action="store_true",
        help="Also scan source YAML glossary/key_terms (via canonicalize normalize).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=OUT_DEFAULT,
        help=f"Output path (default: {OUT_DEFAULT})",
    )
    parser.add_argument("--sample-limit", type=int, default=8)
    args = parser.parse_args()

    rows = iter_canonical_occurrences()
    sources = {"canonical": len(rows)}
    if args.include_source:
        canon = load_canonicalizer()
        source_rows = iter_source_occurrences(canon)
        sources["source_yaml"] = len(source_rows)
        # Prefer canonical; append source for terms that add coverage signal.
        rows = rows + source_rows

    clusters = cluster_occurrences(rows, sample_limit=args.sample_limit)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": sources,
        "occurrence_rows": len(rows),
        "cluster_count": len(clusters),
        "clusters": clusters,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"occurrence_rows={len(rows)}")
    print(f"clusters={len(clusters)}")
    print(f"wrote {args.out}")
    print("top clusters:")
    for cluster in clusters[:15]:
        print(
            f"  {cluster['suggested_lemma_id']}: count={cluster['count']} "
            f"variants={cluster['variants'][:3]} collections={cluster['collections']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
