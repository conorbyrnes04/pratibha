#!/usr/bin/env python3
"""Grounded cross-tradition resonance enrichment.

Rather than free-associating, this pipeline shows the LLM a menu of *real*
corpus passages (ranked by theme overlap, drawn from other traditions) and asks
it to pick 2-3 that share a genuine structural homology with the target, and to
name the divergence for each. Because every resonance cites a passage that
actually exists in the corpus, each one carries an exact `passage_id` and is
guaranteed navigable in the reader.

Usage:
  python scripts/enrich_resonances.py --collection heraclitus_fragments --limit 3 --dry-run
  python scripts/enrich_resonances.py --only-empty            # all empty units
  python scripts/enrich_resonances.py --collection vijnana_bhairava --min 2
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.data_loader import load_all  # noqa: E402

CANONICAL = ROOT / "data" / "canonical"

SYSTEM = """You are a careful comparative-philosophy editor for Pratibha, a \
contemplative corpus spanning Indian, Chinese, Greek, Buddhist, and Sufi \
traditions. You write cross-tradition resonances: precise notes on how a passage \
from one tradition structurally echoes a passage from another.

You will be given a TARGET passage and a numbered MENU of candidate passages from \
OTHER traditions. Choose the 2-3 candidates with the strongest genuine \
structural homology (a shared move of thought, not a vague vibe). For each choice \
return:
  - "index": the candidate's number
  - "resonance": 1-2 sentences naming the specific structural homology (what \
move both texts make). Reference the concrete idea, not generic themes.
  - "divergence": 1 sentence naming how the two traditions differ on this point \
(emphasis, metaphysics, method). This is required.

Rules:
- Only choose from the provided candidates. Never invent a passage.
- Prefer variety of traditions; do not pick two candidates that say the same thing.
- If fewer than 2 candidates have a real homology, return only the ones that do.
- Be specific and restrained; no purple prose, no filler.
- Return ONLY valid JSON: {"resonances": [{"index": int, "resonance": str, "divergence": str}, ...]}"""


def _first_sentence(text: str, limit: int = 240) -> str:
    text = re.sub(r"\s+", " ", re.sub(r"[#*_`>]", "", text or "")).strip()
    if not text:
        return ""
    m = re.search(r"^(.+?[.!?])(\s|$)", text)
    out = m.group(1) if m else text
    return out[:limit].strip()


def _layer_body(unit: dict[str, Any], kind: str) -> str:
    for layer in unit.get("pratibha_layers") or []:
        if layer.get("kind") == kind:
            return str(layer.get("body") or "")
    return ""


def _resonance_count(unit: dict[str, Any]) -> int:
    for layer in unit.get("pratibha_layers") or []:
        if layer.get("kind") == "resonances":
            return len(layer.get("items") or [])
    return 0


def _gist(unit: dict[str, Any]) -> str:
    for kind in ("translation", "commentary"):
        s = _first_sentence(_layer_body(unit, kind))
        if s:
            return s
    return _first_sentence(str(unit.get("thesis") or unit.get("source_excerpt") or ""))


def _citation_label(unit: dict[str, Any]) -> str:
    coll = str(unit.get("collection") or "").strip()
    ref = str(unit.get("reference") or "").strip()
    if ref:
        return f"{coll} {ref}"
    prov = unit.get("provenance") or {}
    section = str(prov.get("section") or unit.get("section") or "").strip()
    # Prefer a real section reference (e.g. "Ennead I, Tractate 6") over a slug.
    if section and not re.fullmatch(r"[a-z_]+", section) and len(section) < 60:
        return f"{coll} — {section}"
    title = str(unit.get("title") or "").strip()
    if title and len(title) < 70:
        return f"{coll} — {title}"
    return coll


def _themes(unit: dict[str, Any]) -> set[str]:
    return {str(t).strip().lower() for t in (unit.get("themes") or []) if str(t).strip()}


def build_candidate_pool(target: dict[str, Any], units: list[dict[str, Any]], k: int = 16) -> list[dict[str, Any]]:
    """Cross-tradition passages ranked by theme overlap, capped per collection."""
    t_themes = _themes(target)
    t_coll = target.get("collection")
    scored: list[tuple[float, dict[str, Any]]] = []
    for u in units:
        if u["_id"] == target["_id"] or u.get("collection") == t_coll:
            continue
        if not _gist(u):
            continue
        u_themes = _themes(u)
        overlap = len(t_themes & u_themes)
        if overlap == 0:
            continue
        union = len(t_themes | u_themes) or 1
        jaccard = overlap / union
        maturity = {"publishable": 0.15, "strong_draft": 0.08}.get(str(u.get("editorial_maturity")), 0.0)
        scored.append((overlap + jaccard + maturity, u))
    scored.sort(key=lambda x: x[0], reverse=True)

    pool: list[dict[str, Any]] = []
    per_coll: dict[str, int] = {}
    for _, u in scored:
        c = str(u.get("collection"))
        if per_coll.get(c, 0) >= 2:  # diversity: max 2 per tradition
            continue
        per_coll[c] = per_coll.get(c, 0) + 1
        pool.append(u)
        if len(pool) >= k:
            break
    return pool


def build_prompt(target: dict[str, Any], pool: list[dict[str, Any]]) -> str:
    lines = [
        "TARGET PASSAGE",
        f"Tradition: {target.get('collection')}",
        f"Title: {target.get('title')}",
        f"Themes: {', '.join(sorted(_themes(target))) or '(none)'}",
        f"Translation: {_first_sentence(_layer_body(target, 'translation'), 400) or '(none)'}",
        f"Commentary: {_first_sentence(_layer_body(target, 'commentary'), 400) or '(none)'}",
        "",
        "CANDIDATE MENU (choose 2-3 by index):",
    ]
    for i, u in enumerate(pool):
        lines.append(f"[{i}] {_citation_label(u)} ({u.get('collection')})")
        lines.append(f"    {_gist(u)}")
    lines.append("")
    lines.append('Return JSON: {"resonances": [{"index": int, "resonance": str, "divergence": str}]}')
    return "\n".join(lines)


async def _llm_json(system: str, user: str) -> dict[str, Any]:
    from app.llm import smart_chat

    text = (await smart_chat([{"role": "system", "content": system}, {"role": "user", "content": user}], temperature=0.3)).strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def _valid(resonance: str, divergence: str) -> bool:
    return len(re.sub(r"\s+", " ", resonance).strip()) >= 40 and len(re.sub(r"\s+", " ", divergence).strip()) >= 25


async def enrich_unit(target: dict[str, Any], units: list[dict[str, Any]], min_keep: int) -> list[dict[str, str]] | None:
    pool = build_candidate_pool(target, units)
    if len(pool) < 2:
        return None
    try:
        out = await _llm_json(SYSTEM, build_prompt(target, pool))
    except Exception as e:  # noqa: BLE001
        print(f"    LLM/JSON error: {str(e)[:120]}")
        return None

    chosen = out.get("resonances") if isinstance(out, dict) else None
    if not isinstance(chosen, list):
        return None

    results: list[dict[str, str]] = []
    used_colls: set[str] = set()
    used_idx: set[int] = set()
    for c in chosen:
        if not isinstance(c, dict):
            continue
        idx = c.get("index")
        if not isinstance(idx, int) or idx < 0 or idx >= len(pool) or idx in used_idx:
            continue
        resonance = str(c.get("resonance") or "").strip()
        divergence = str(c.get("divergence") or "").strip()
        if not _valid(resonance, divergence):
            continue
        cand = pool[idx]
        coll = str(cand.get("collection"))
        if coll in used_colls:  # keep traditions distinct
            continue
        used_colls.add(coll)
        used_idx.add(idx)
        results.append(
            {
                "citation": _citation_label(cand),
                "resonance": resonance,
                "divergence": divergence,
                "passage_id": cand["_id"],
            }
        )
        if len(results) >= 3:
            break
    if len(results) < min_keep:
        return None
    return results


def source_file_map() -> dict[str, Path]:
    """canonical unit_id -> source data/yaml path."""
    out: dict[str, Path] = {}
    for p in CANONICAL.rglob("*.yml"):
        if p.name == "_work.yml":
            continue
        try:
            d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except Exception:  # noqa: BLE001
            continue
        uid = d.get("unit_id")
        src = d.get("source_file")
        if uid and src:
            out[str(uid)] = ROOT / str(src)
    return out


def write_resonances(path: Path, resonances: list[dict[str, str]]) -> bool:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        return False
    data["resonances"] = resonances
    prov = data.get("layer_provenance")
    if not isinstance(prov, dict):
        prov = {}
    prov["resonances"] = "generated_grounded"
    data["layer_provenance"] = prov
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8")
    return True


async def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--collection", help="restrict to a collection (data/yaml dir name or display substring)")
    ap.add_argument("--limit", type=int, default=0, help="max units to process (0 = all)")
    ap.add_argument("--min", type=int, default=2, help="minimum resonances to keep a unit (default 2)")
    ap.add_argument("--only-empty", action="store_true", default=True, help="only units with no resonances (default)")
    ap.add_argument("--include-thin", dest="only_empty", action="store_false", help="also top up units with <2 resonances")
    ap.add_argument("--dry-run", action="store_true", help="print, do not write")
    ap.add_argument("--concurrency", type=int, default=4)
    args = ap.parse_args()

    print("Loading corpus...")
    units = load_all()
    print(f"  {len(units)} units")

    def match_coll(u: dict[str, Any]) -> bool:
        if not args.collection:
            return True
        c = args.collection.lower()
        return c in str(u.get("collection", "")).lower() or c in str(u.get("_id", "")).lower()

    threshold = 1 if args.only_empty else 2
    targets = [u for u in units if match_coll(u) and _resonance_count(u) < threshold]
    if args.limit:
        targets = targets[: args.limit]
    print(f"  {len(targets)} target units (threshold <{threshold} resonances)")

    src_map = source_file_map()
    sem = asyncio.Semaphore(args.concurrency)
    written = skipped = 0

    async def work(t: dict[str, Any]):
        nonlocal written, skipped
        async with sem:
            res = await enrich_unit(t, units, args.min)
        label = f"{t['_id']}"
        if not res:
            skipped += 1
            print(f"  [skip] {label}")
            return
        print(f"  [ok]   {label}: {len(res)} resonances")
        for r in res:
            print(f"           - {r['citation']}  (-> {r['passage_id']})")
            print(f"             {r['resonance'][:140]}")
        if args.dry_run:
            return
        path = src_map.get(t["_id"])
        if not path or not path.exists():
            print(f"           ! no source file for {t['_id']}")
            skipped += 1
            return
        if write_resonances(path, res):
            written += 1

    await asyncio.gather(*(work(t) for t in targets))
    print(f"\nDone. written={written} skipped={skipped} dry_run={args.dry_run}")
    if written and not args.dry_run:
        print("Next: run scripts/canonicalize_texts.py to rebuild canonical files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
