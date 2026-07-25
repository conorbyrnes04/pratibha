#!/usr/bin/env python3
"""Upgrade structural_draft PD ingest units to strong_draft.

Rewrites boilerplate commentary + practice so each unit is passage-specific,
then sets editorial_maturity: strong_draft. Does not promote to canonical.

    python scripts/upgrade_structural_maturity.py --limit 2          # preview
    python scripts/upgrade_structural_maturity.py --write
    python scripts/upgrade_structural_maturity.py --write --dir dhammapada
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import settings  # noqa: E402
from app.llm import smart_chat  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
YAML_ROOT = ROOT / "data" / "yaml"

DIRS = [
    "brihadaranyaka_upanishad",
    "cloud_of_unknowing",
    "dhammapada",
    "katha_upanishad",
    "marcus_aurelius_meditations",
    "mundaka_upanishad",
    "parmenides",
    "fragments",
]

CTX: dict[str, tuple[str, str]] = {
    "brihadaranyaka_upanishad": (
        "the Bṛhadāraṇyaka Upaniṣad (Yājñavalkya dialogues on the Self)",
        "the specific Vedāntic cut this unit makes — neti-neti, madhu, fear from a second, Self as light — not a generic Upaniṣad summary",
    ),
    "cloud_of_unknowing": (
        "The Cloud of Unknowing (Middle English contemplative treatise)",
        "the apophatic discipline this chapter names — naked intent, cloud of forgetting, piercing love — without recycling the same Cloud summary",
    ),
    "dhammapada": (
        "the Dhammapada (Pali Buddhist verse anthology)",
        "the governing claim of THIS chapter/verses — mind, earnestness, anger, the path, etc. — as a concrete discipline of attention",
    ),
    "katha_upanishad": (
        "the Kaṭha Upaniṣad (Naciketas and Yama)",
        "the precise move in this stretch of the Naciketas–Yama dialogue — boons, chariot, two paths, the thumb-sized Self",
    ),
    "marcus_aurelius_meditations": (
        "Marcus Aurelius' Meditations (Stoic spiritual exercises)",
        "the specific Stoic discipline of the ruling faculty this entry trains — morning readiness, death, assent, cosmopolitan duty",
    ),
    "mundaka_upanishad": (
        "the Muṇḍaka Upaniṣad",
        "the structural image THIS unit uses — two knowledges, two birds, the bow of Om, the knot of the heart",
    ),
    "parmenides": (
        "Parmenides' poem On Nature (fragments)",
        "the hard epistemic fork this fragment draws — being, the two ways, the impossibility of not-being — without generic Presocratic filler",
    ),
    "fragments": (
        "the fragments of Heraclitus (Presocratic Greek)",
        "THIS fragment's own paradox or image — logos, fire, flux, the bow/lyre, waking/sleeping, the shared vs the private — not a generic 'everything flows' gloss",
    ),
}

SYSTEM = """You upgrade a study unit for {work}.

Write TWO fields grounded ONLY in this specific passage:
1) commentary — unpack THIS passage's central move ({focus}). Rigorous, practiced, unhurried prose. No throat-clearing ("This passage invites…"), no museum filler, no identical collection boilerplate. Roughly 700–1400 characters. Keep genuine source-language terms with a brief gloss when natural.
2) practice — ONE embodied exercise drawn from THIS passage's own image/claim. 1–3 sentences. Do NOT begin with Sit quietly / Pick one / Choose one / Take one / Today notice / Bring to mind / Spend / For one day. Begin with the concrete action. Vary form (breath, gaze, phrase, daily act, self-inquiry, walking, listening, negation).

Return ONLY JSON:
{{"commentary":"...","practice":"...","themes":["…","…","…","…"]}}
Themes: 3–6 short lowercase English tags."""


def _extract(txt: str) -> dict | None:
    txt = re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M).strip()
    try:
        return json.loads(txt)
    except Exception:
        m = re.search(r"\{.*\}", txt, re.S)
        return json.loads(m.group(0)) if m else None


async def upgrade_unit(dir_slug: str, path: Path, used_openers: list[str]) -> dict | None:
    y = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    work, focus = CTX[dir_slug]
    title = str(y.get("title") or path.stem)
    section = str(y.get("section") or "")
    original = str(y.get("sanskrit") or "")
    verse = str(y.get("translation") or "")
    old_cm = str(y.get("commentary") or "")
    old_ab = str(y.get("abhyasa") or "")
    avoid = ""
    if used_openers:
        avoid = (
            "\nOther practices in this collection already open: "
            + "; ".join(f'"{o}…"' for o in used_openers[-6:])
            + ". Open differently."
        )
    user = (
        f"Title: {title}\nSection: {section}\n"
        f"Original (may be partial): {original[:500]}\n"
        f"Translation: {verse[:1100]}\n"
        f"(Old commentary to replace, do not imitate: {old_cm[:220]})\n"
        f"(Old practice to replace: {old_ab[:180]})"
        f"{avoid}\n\nWrite commentary + practice + themes as JSON."
    )
    txt = await smart_chat(
        [
            {"role": "system", "content": SYSTEM.format(work=work, focus=focus)},
            {"role": "user", "content": user},
        ],
        temperature=0.55,
        max_tokens=1400,
    )
    return _extract(txt)


def _opener(p: str) -> str:
    return " ".join(re.findall(r"[A-Za-z']+", p or "")[:3]).lower()


async def run_dir(
    dir_slug: str,
    write: bool,
    limit: int,
    sem: asyncio.Semaphore,
    only_structural: bool,
) -> tuple[int, int]:
    d = YAML_ROOT / dir_slug
    files = sorted(d.glob("*.yml"))
    used: list[str] = []
    ok = 0
    fail = 0
    skipped = 0

    # Seed opener diversity from already-strong units so new practices don't collide.
    for fp in files:
        y = yaml.safe_load(fp.read_text(encoding="utf-8")) or {}
        if y.get("editorial_maturity") == "strong_draft":
            used.append(_opener(str(y.get("abhyasa") or y.get("practice") or "")))

    todo: list[Path] = []
    for fp in files:
        y = yaml.safe_load(fp.read_text(encoding="utf-8")) or {}
        if only_structural and y.get("editorial_maturity") != "structural_draft":
            skipped += 1
            continue
        if write and "maturity upgrade" in str(y.get("commentary_provenance") or ""):
            skipped += 1
            continue
        todo.append(fp)
    if limit:
        todo = todo[:limit]
    print(f"  queue={len(todo)} skipped={skipped}")

    async def one(fp: Path) -> None:
        nonlocal ok, fail
        async with sem:
            y = yaml.safe_load(fp.read_text(encoding="utf-8")) or {}
            r = None
            last_err: Exception | None = None
            for attempt in range(2):
                try:
                    r = await upgrade_unit(dir_slug, fp, used)
                    if r and len(str(r.get("commentary") or "").strip()) >= 220:
                        break
                    r = None
                except Exception as e:
                    last_err = e
                    r = None
            if not r:
                fail += 1
                print(f"  FAIL {fp.name}: {last_err or 'thin/empty/unparseable response'}")
                return
            commentary = str(r["commentary"]).strip()
            practice = str(r.get("practice") or "").strip()
            themes = r.get("themes") if isinstance(r.get("themes"), list) else y.get("themes")
            print(f"  {fp.name}: {commentary[:88]}…")
            print(f"           practice: {practice[:88]}")
            if write:
                y["commentary"] = commentary
                if practice:
                    y["abhyasa"] = practice
                if themes:
                    y["themes"] = [str(t).strip().lower() for t in themes if str(t).strip()][:6]
                y["editorial_maturity"] = "strong_draft"
                y["commentary_provenance"] = "Study commentary from maturity upgrade (passage-specific)."
                y["practice_provenance"] = "Practice from maturity upgrade (form diversity)."
                fp.write_text(
                    yaml.safe_dump(y, allow_unicode=True, sort_keys=False, width=100),
                    encoding="utf-8",
                )
                used.append(_opener(practice))
            ok += 1

    # sequential within collection so opener diversity has real history
    for fp in todo:
        await one(fp)
    return ok, fail


async def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="Per-directory limit")
    ap.add_argument("--dir", action="append", dest="dirs", help="Only these yaml dir slugs")
    ap.add_argument("--concurrency", type=int, default=1)
    ap.add_argument(
        "--only-structural",
        action="store_true",
        default=True,
        help="Only rewrite structural_draft units (default: on)",
    )
    ap.add_argument("--all-maturity", action="store_true", help="Rewrite every unit, not only structural_draft")
    args = ap.parse_args()
    if not settings.OPENROUTER_API_KEY and not settings.OPENAI_API_KEY:
        print("Need OPENROUTER_API_KEY or OPENAI_API_KEY", file=sys.stderr)
        return 1

    dirs = args.dirs or DIRS
    only_structural = not args.all_maturity
    print(
        f"model={settings.effective_default_model()} write={args.write} "
        f"only_structural={only_structural} dirs={dirs}\n"
    )
    sem = asyncio.Semaphore(max(1, args.concurrency))
    total_ok = total_fail = 0
    for slug in dirs:
        if slug not in CTX:
            print(f"skip unknown dir {slug}")
            continue
        print(f"=== {slug} ===")
        ok, fail = await run_dir(slug, args.write, args.limit, sem, only_structural)
        total_ok += ok
        total_fail += fail
        print(f"  -> ok={ok} fail={fail}\n")
    print(f"DONE ok={total_ok} fail={total_fail}" + ("" if args.write else " (preview)"))
    return 0 if total_fail == 0 else 2


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
