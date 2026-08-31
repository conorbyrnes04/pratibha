#!/usr/bin/env python3
"""Promote Yoruba enrich drafts from staging into canonical layers.

Splits the unstructured enrich commentary into commentary / key_terms /
resonances / practice. Does not ingest pgvector — only writes YAML.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "data/staging/enrich/yoruba_proverbs"
CANONICAL = ROOT / "data/canonical/yoruba_proverbs"


def split_enrich(commentary: str) -> tuple[str, str, str]:
    text = (commentary or "").strip()
    parts = re.split(r"\n\s*Key Terms\s*\n", text, maxsplit=1, flags=re.I)
    body = parts[0].strip()
    rest = parts[1].strip() if len(parts) > 1 else ""
    key = ""
    res = ""
    if rest:
        res_parts = re.split(r"\n\s*Cross-Tradition Resonances\s*\n", rest, maxsplit=1, flags=re.I)
        key = res_parts[0].strip()
        res = res_parts[1].strip() if len(res_parts) > 1 else ""
    else:
        res_parts = re.split(r"\n\s*Cross-Tradition Resonances\s*\n", body, maxsplit=1, flags=re.I)
        if len(res_parts) > 1:
            body = res_parts[0].strip()
            res = res_parts[1].strip()
    return body, key, res


def promote_one(src: Path) -> bool:
    data = yaml.safe_load(src.read_text())
    if not isinstance(data, dict):
        return False
    dest = CANONICAL / src.name
    existing = yaml.safe_load(dest.read_text()) if dest.exists() else {}
    if not isinstance(existing, dict):
        existing = {}

    body, key_terms, resonances = split_enrich(str(data.get("commentary") or ""))
    practice = str(data.get("practice") or data.get("abhyasa") or "").strip()
    translation = ""
    for layer in existing.get("pratibha_layers") or []:
        if isinstance(layer, dict) and layer.get("kind") == "translation":
            translation = str(layer.get("body") or "")
            break
    if not translation:
        translation = str(existing.get("translation") or data.get("translation") or "")

    layers = []
    if translation:
        layers.append({"kind": "translation", "label": "Translation", "body": translation})
    if body:
        layers.append({"kind": "commentary", "label": "Pratibha Commentary", "body": body})
    if key_terms:
        layers.append({"kind": "key_terms", "label": "Key Terms", "body": key_terms})
    if resonances:
        layers.append({"kind": "resonances", "label": "Cross-Tradition Resonances", "body": resonances})
    if practice:
        layers.append({"kind": "practice", "label": "Practice", "body": practice})

    if not body:
        return False

    merged = dict(existing)
    merged.update(
        {
            "source_id": data.get("source_id") or existing.get("source_id"),
            "work_id": "yoruba_proverbs",
            "work_title": existing.get("work_title") or data.get("work_title"),
            "unit_id": data.get("unit_id") or existing.get("unit_id"),
            "title": existing.get("title") or data.get("title"),
            "unit_label": existing.get("unit_label") or data.get("unit_label"),
            "unit_type": "proverb",
            "commentary": body,
            "translation": translation,
            "practice": practice,
            "editorial_maturity": "strong_draft",
            "pratibha_layers": layers,
            "provenance": existing.get("provenance") or data.get("provenance"),
            "translation_provenance": existing.get("translation_provenance")
            or data.get("translation_provenance"),
        }
    )
    merged.pop("enriched", None)
    dest.write_text(yaml.safe_dump(merged, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return True


def main() -> int:
    promoted = 0
    skipped = 0
    for src in sorted(STAGING.glob("*.yml")):
        if promote_one(src):
            promoted += 1
        else:
            skipped += 1
            print(f"skip (failed audit): {src.name}")
    print(f"promoted {promoted}; skipped {skipped}")
    return 0 if promoted else 1


if __name__ == "__main__":
    raise SystemExit(main())
