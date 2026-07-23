#!/usr/bin/env python3
"""Re-author generic / formulaic practices with FORM DIVERSITY.

Reads data/practice_audit.json for units marked `reauthor` (true boilerplate) or
`reauthor-form` (grounded but monotonous). For each, generates ONE fresh practice
grounded in the specific passage, VARYING the form to match what the text
prescribes, and avoiding the "Sit quietly…"/"Pick one…" openers that caused the
corpus-wide sameness. A per-collection diversity guard feeds each call the forms
already used so practices don't reconverge; a fresh practice that is still
formulaic (or duplicates a used opener) is retried once with a harder nudge.

Keeps translation and commentary untouched — only the practice field changes.

    python scripts/reauthor_practices.py --collection <slug> --limit 5        # preview
    python scripts/reauthor_practices.py --collection <slug> --write
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import settings          # noqa: E402
from app.llm import smart_chat           # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIT = os.path.join(ROOT, "data", "practice_audit.json")

FORMULAIC_OPENER = re.compile(
    r"^\s*(take one|pick one|choose one|bring to mind|sit quietly|sit comfortably|sit for|sit in|"
    r"spend (a|one|ten|five)|today,?\s|tonight|for the next|for one (day|week|minute)|set aside|"
    r"today notice|today practice|today pick|today choose|each (morning|night|day)|daily practice)\b",
    re.I,
)

FORMS = ("breath-work", "gaze / vision", "recitation of a phrase from the text", "a posture or gesture",
         "an act in daily life or with another person", "contemplative self-inquiry",
         "a letting-go / negation exercise", "noticing in the midst of activity", "a listening practice",
         "a walking practice", "a one-line vow repeated through the day")

SYSTEM = """You write ONE fresh contemplative practice for a study unit, grounded in its specific passage.

HARD RULES:
- Draw the practice from THIS passage's own instruction, image, or claim — never a generic exercise that could be pasted onto any text.
- VARY THE FORM to fit this passage. Options include: {forms}. Do NOT default to sitting-and-journaling.
- Do NOT begin with any of: "Sit quietly", "Sit comfortably", "Pick one", "Choose one", "Take one", "Today notice", "Bring to mind", "Spend", "For one day/week". Begin with the concrete action itself (e.g. "Walk until…", "On your next out-breath…", "The next time someone…", "Whisper the line…", "Hold your gaze on…").
- 1-3 sentences, embodied and doable today.

Return ONLY JSON: {{"practice": "..."}}"""


def _extract(txt: str) -> dict | None:
    txt = re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M).strip()
    try:
        return json.loads(txt)
    except Exception:
        m = re.search(r"\{.*\}", txt, re.S)
        return json.loads(m.group(0)) if m else None


def _opener(p: str) -> str:
    return " ".join(re.findall(r"[A-Za-z']+", p or "")[:3]).lower()


async def reauthor(verse: str, commentary: str, old: str, avoid_openers: list[str], hard: bool = False) -> str | None:
    avoid = ""
    if avoid_openers:
        avoid = ("\n\nOther practices in this same text already begin: "
                 + "; ".join(f'"{o}…"' for o in avoid_openers[-8:])
                 + ". Yours MUST open differently and use a different kind of practice.")
    if hard:
        avoid += "\n\nYour previous attempt was too generic/formulaic. Pick a clearly different, embodied form drawn straight from the passage's own words."
    user = (f"PASSAGE:\n{verse[:900]}\n\nCOMMENTARY (context):\n{commentary[:900]}\n\n"
            f"(The current practice to replace, do not imitate its shape: {old[:200]})"
            f"{avoid}\n\nWrite the new practice as JSON.")
    txt = await smart_chat([{"role": "system", "content": SYSTEM.format(forms=", ".join(FORMS))},
                            {"role": "user", "content": user}], temperature=0.7, max_tokens=350)
    d = _extract(txt)
    return str(d.get("practice") or "").strip() if d else None


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--collection", required=True)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    if not settings.OPENROUTER_API_KEY:
        sys.exit("set OPENROUTER_API_KEY")

    audit = json.load(open(AUDIT, encoding="utf-8"))
    todo = [(uid, u) for uid, u in audit["units"].items()
            if u["collection"] == args.collection and u["practice"]["decision"] in ("reauthor", "reauthor-form")]
    if args.limit:
        todo = todo[: args.limit]
    print(f"{args.collection}: {len(todo)} practices to re-author, model={settings.effective_default_model()}\n")

    used: list[str] = []
    still_formulaic = 0
    for i, (uid, u) in enumerate(todo, 1):
        path = os.path.join(ROOT, u["file"])
        d = yaml.safe_load(open(path, encoding="utf-8"))
        # Idempotent: skip units already re-authored so a re-run finishes the rest.
        if args.write and "form diversity" in str(d.get("practice_provenance") or ""):
            used.append(_opener(str(d.get("practice") or "")))  # keep its opener in the guard
            continue
        verse = str(d.get("translation") or d.get("translation_literal") or d.get("title") or "")
        old = str(d.get("abhyasa") or d.get("practice") or "")
        new = await reauthor(verse, str(d.get("commentary") or ""), old, used)
        # retry once if still formulaic or duplicates an opener already used
        if new and (FORMULAIC_OPENER.match(new) or _opener(new) in used):
            new = await reauthor(verse, str(d.get("commentary") or ""), old, used, hard=True) or new
        if not new:
            print(f"[{i}] {uid}: no practice"); continue
        if FORMULAIC_OPENER.match(new):
            still_formulaic += 1
        used.append(_opener(new))
        print(f"[{i}] {d.get('title','')[:26]:26s} → {new[:100]}")
        if args.write:
            d["practice"] = new
            d["abhyasa"] = new
            d["practice_provenance"] = "Practice re-authored for form diversity, grounded in the passage."
            yaml.safe_dump(d, open(path, "w", encoding="utf-8"), allow_unicode=True, sort_keys=False, width=100)

    uniq = len(set(used))
    print(f"\ndiversity: {uniq}/{len(used)} distinct openers | still-formulaic: {still_formulaic}"
          + ("  (WRITE)" if args.write else "  (preview)"))


if __name__ == "__main__":
    asyncio.run(main())
