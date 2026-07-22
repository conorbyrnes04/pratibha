#!/usr/bin/env python3
"""Generate controlled-vocabulary themes for low-theme units (<=1 theme).

Themes drive cross-tradition resonance pooling (theme overlap), browse filters
and RAG tags. Many units carry 0-1 themes because the pipeline's keyword match
missed them. This picks 4-8 themes per unit from the SAME controlled vocabulary
(THEME_TERMS) the canonicalizer uses, grounded in the unit's own text, via a
cheap LLM classification. Output is a JSONL patch for apply_canonical_patch.py.

Never invents themes outside the allowed vocabulary; merges with existing themes.
"""
from __future__ import annotations

import argparse
import asyncio
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.data_loader import load_all  # noqa: E402


def _load_theme_terms() -> list[str]:
    path = ROOT / "scripts" / "canonicalize_texts.py"
    spec = importlib.util.spec_from_file_location("canonicalize_texts", path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    seen: list[str] = []
    for t in module.THEME_TERMS:
        if t not in seen:
            seen.append(t)
    return seen


ALLOWED = _load_theme_terms()
ALLOWED_SET = {t.lower() for t in ALLOWED}

SYSTEM = (
    "You are a comparative-philosophy editor tagging a contemplative passage with themes.\n"
    "Choose ONLY from the provided controlled vocabulary. Pick the 4-8 themes that a scholar\n"
    "would use to find cross-tradition parallels to this passage. Prefer broad, shared\n"
    "concepts (e.g. awareness, self, breath, emptiness, stillness, death) over narrow ones.\n"
    "Rules:\n"
    "- Use only exact strings from the vocabulary. Never invent terms.\n"
    "- Base choices on what the passage is actually about, not decoration.\n"
    '- Return ONLY valid JSON: {"themes": ["...", "..."]}'
)


def _first(text: str, limit: int) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[#*_`>]", "", text or "")).strip()[:limit]


def _layer(unit: dict[str, Any], kind: str) -> str:
    for l in unit.get("pratibha_layers") or []:
        if l.get("kind") == kind:
            return str(l.get("body") or "")
    return ""


def build_prompt(unit: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"Tradition: {unit.get('collection')}",
            f"Title: {unit.get('title')}",
            f"Translation: {_first(_layer(unit, 'translation'), 500) or '(none)'}",
            f"Commentary: {_first(_layer(unit, 'commentary'), 500) or '(none)'}",
            "",
            "CONTROLLED VOCABULARY (choose 4-8 exact strings):",
            ", ".join(ALLOWED),
            "",
            'Return JSON: {"themes": ["...", "..."]}',
        ]
    )


async def _llm_themes(unit: dict[str, Any]) -> list[str]:
    from app.llm import smart_chat

    text = (
        await smart_chat(
            [{"role": "system", "content": SYSTEM}, {"role": "user", "content": build_prompt(unit)}],
            temperature=0.2,
        )
    ).strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        data = json.loads(text)
    except Exception:
        return []
    picked = data.get("themes") if isinstance(data, dict) else None
    if not isinstance(picked, list):
        return []
    out: list[str] = []
    for t in picked:
        s = str(t).strip()
        if s.lower() in ALLOWED_SET and s not in out:
            out.append(s)
    return out


def _theme_count(unit: dict[str, Any]) -> int:
    return len(unit.get("themes") or [])


async def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-existing", type=int, default=1, help="target units with <= this many themes")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--concurrency", type=int, default=6)
    ap.add_argument("--out", default=str(ROOT / "scratch" / "themes_proposals.jsonl"))
    args = ap.parse_args()

    units = load_all()
    targets = [u for u in units if _theme_count(u) <= args.max_existing]
    if args.limit:
        targets = targets[: args.limit]
    print(f"target units (<= {args.max_existing} themes): {len(targets)}")

    sem = asyncio.Semaphore(args.concurrency)
    records: list[dict[str, Any]] = []
    skipped = 0

    async def work(u: dict[str, Any]) -> None:
        nonlocal skipped
        async with sem:
            new = await _llm_themes(u)
        existing = [t for t in (u.get("themes") or [])]
        merged: list[str] = []
        for t in existing + new:
            if t not in merged:
                merged.append(t)
        if len(merged) < 2 or merged == existing:
            skipped += 1
            print(f"  [skip] {u['_id']} ({len(new)} new)")
            return
        records.append(
            {"unit_id": u["_id"], "set_fields": {"themes": merged}, "retag_from_themes": True}
        )
        print(f"  [ok]   {u['_id']}: {existing} + {new}")

    await asyncio.gather(*(work(u) for u in targets))

    out_path = Path(args.out)
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n", encoding="utf-8")
    print(f"\nwrote {len(records)} theme patches ({skipped} skipped) -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
