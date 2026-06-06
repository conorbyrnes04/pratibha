"""Enrich chunk metadata in place (no re-embedding required).

Backfills metadata that older ingests never wrote:
  - layer_kind        (derived from the existing `section`)
  - editorial_maturity / editorial_score / themes  (from source YAML via
    the app's own `normalize_unit`, when the source file still exists)
  - canonical collection slug (unifies "Tao Te Ching" / "tao_te_ching")

It only UPDATEs the `metadata` jsonb column; embeddings and chunk bodies are
left untouched, so it is safe to run without an embedding API key. Idempotent.

Usage:
  python scripts/enrich_metadata.py            # dry-run, prints a plan
  python scripts/enrich_metadata.py --apply     # write changes
"""

import argparse
import asyncio
import json
import re
import sys
from collections import Counter
from pathlib import Path

import asyncpg
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.config import settings  # noqa: E402
from app.collection_aliases import COLLECTION_ALIASES, slugify  # noqa: E402
from app.data_loader import normalize_unit  # noqa: E402


# section label -> canonical layer kind. Covers both the legacy key-based
# section names (e.g. "translation_literal") and current pratibha_layers kinds.
_LAYER_KIND_MAP = {
    "sanskrit": "original",
    "sanskrit_devanagari": "original",
    "original": "original",
    "transliteration": "iast",
    "sanskrit_iast": "iast",
    "iast": "iast",
    "translation": "translation",
    "translation_literal": "translation",
    "commentary": "commentary",
    "key_terms": "key_terms",
    "resonances": "resonances",
    "practice": "practice",
    "abhyasa": "practice",
}


def section_to_layer_kind(section: str) -> str:
    s = (section or "").strip().lower()
    if not s:
        return "commentary"
    if s.startswith("appendix:") or s == "appendix":
        return "appendix"
    if s.startswith("mode:"):
        return "mode"
    return _LAYER_KIND_MAP.get(s, s)


# Precompute slug -> canonical-slug lookup from the alias registry.
_ALIAS_TO_CANONICAL: dict[str, str] = {}
for _canonical, _aliases in COLLECTION_ALIASES.items():
    for _name in {_canonical, *_aliases}:
        _ALIAS_TO_CANONICAL[slugify(_name)] = _canonical


def canonical_collection(value: str, source_file: str) -> str:
    s = slugify(value)
    if s in _ALIAS_TO_CANONICAL:
        return _ALIAS_TO_CANONICAL[s]
    # Fall back to the directory name in the source path.
    m = re.search(r"data/(?:yaml|canonical)/([^/]+)/", (source_file or "").lower())
    if m:
        s2 = slugify(m.group(1))
        return _ALIAS_TO_CANONICAL.get(s2, s2)
    return s


_yaml_cache: dict[str, dict | None] = {}


def load_source_norm(source_file: str) -> dict | None:
    if source_file in _yaml_cache:
        return _yaml_cache[source_file]
    path = source_file if Path(source_file).is_absolute() else str(ROOT / source_file)
    result: dict | None = None
    try:
        p = Path(path)
        if p.is_file():
            raw = yaml.safe_load(p.read_text(encoding="utf-8", errors="replace")) or {}
            if isinstance(raw, dict):
                result = normalize_unit(raw, p.as_posix())
    except Exception:
        result = None
    _yaml_cache[source_file] = result
    return result


def _meta(value) -> dict:
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, dict) else {}
        except Exception:
            return {}
    return {}


def enrich_one(meta: dict) -> dict:
    out = dict(meta)
    source_file = str(meta.get("source_file") or "")

    out["layer_kind"] = section_to_layer_kind(str(meta.get("section") or ""))
    out["collection"] = canonical_collection(str(meta.get("collection") or ""), source_file)

    norm = load_source_norm(source_file)
    if norm is not None:
        out["editorial_maturity"] = norm.get("editorial_maturity") or out.get("editorial_maturity") or "needs_rewrite"
        out["editorial_score"] = norm.get("editorial_score") or out.get("editorial_score") or 0
        if isinstance(norm.get("themes"), list) and norm["themes"]:
            out["themes"] = norm["themes"]
        for key in ("_id", "title", "sutra_id", "type"):
            if not out.get(key) and norm.get(key):
                out[key] = norm.get(key)
    else:
        # No source file on disk: keep what we have, but ensure the fields exist
        # so downstream filters/ordering have something to read.
        out.setdefault("editorial_maturity", out.get("editorial_maturity") or "needs_rewrite")
        out.setdefault("editorial_score", out.get("editorial_score") or 0)
        out.setdefault("themes", out.get("themes") if isinstance(out.get("themes"), list) else [])

    if not isinstance(out.get("quality_score"), (int, float)):
        out["quality_score"] = out.get("editorial_score") or 0
    return out


async def main(apply: bool) -> None:
    conn = await asyncpg.connect(
        user=settings.PG_USER,
        password=settings.PG_PASSWORD,
        database=settings.PG_DB,
        host=settings.PG_HOST,
        port=settings.PG_PORT,
    )
    rows = await conn.fetch("SELECT id, metadata FROM chunks ORDER BY id")
    print(f"Loaded {len(rows)} chunks.")

    updates: list[tuple[int, str]] = []
    layer_kinds: Counter = Counter()
    collections: Counter = Counter()
    maturities: Counter = Counter()
    changed = 0
    missing_files: set[str] = set()

    for row in rows:
        meta = _meta(row["metadata"])
        new_meta = enrich_one(meta)
        layer_kinds[new_meta.get("layer_kind")] += 1
        collections[new_meta.get("collection")] += 1
        maturities[new_meta.get("editorial_maturity")] += 1
        if load_source_norm(str(meta.get("source_file") or "")) is None and meta.get("source_file"):
            missing_files.add(str(meta.get("source_file")))
        if new_meta != meta:
            changed += 1
            updates.append((row["id"], json.dumps(new_meta, ensure_ascii=False)))

    print(f"\nPlanned changes: {changed} / {len(rows)} rows will be updated.")
    print(f"Source files missing on disk (partial enrich): {len(missing_files)}")

    def _summary(title: str, counter: Counter, top: int = 12) -> None:
        print(f"\n{title}:")
        for key, count in counter.most_common(top):
            print(f"  {count:6d}  {key}")

    _summary("layer_kind distribution (after)", layer_kinds)
    _summary("editorial_maturity distribution (after)", maturities)
    _summary("collection distribution (after)", collections, top=40)

    if not apply:
        print("\nDry-run only. Re-run with --apply to write these changes.")
        await conn.close()
        return

    async with conn.transaction():
        for chunk_id, payload in updates:
            await conn.execute(
                "UPDATE chunks SET metadata = $1::jsonb WHERE id = $2",
                payload,
                chunk_id,
            )
    print(f"\nApplied {len(updates)} metadata updates.")
    await conn.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write changes (default is dry-run)")
    args = ap.parse_args()
    asyncio.run(main(apply=args.apply))
