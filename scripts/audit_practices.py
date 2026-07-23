#!/usr/bin/env python3
"""Audit practice (abhyasa) AND commentary quality across the canonical corpus.

Two stages:
  1. PATTERN pass (free, default): classify each unit's practice + commentary by
     known boilerplate/template markers and length. Fast, whole corpus.
  2. GROUNDING pass (--ground, costs credits): for fields that PASS the pattern
     check, an INDEPENDENT model judges whether the text is actually grounded in
     THIS unit's verse — catching hallucination (plausible but not derivable from
     the source) that a regex can't see.

Output: data/practice_audit.json — per-unit verdicts + a keep/reauthor/remove map
+ a summary. Nothing is modified in the corpus; this is read-only reporting.

    python scripts/audit_practices.py                      # pattern pass, whole corpus
    python scripts/audit_practices.py --collection siva_sutra
    python scripts/audit_practices.py --ground --limit 40  # add model grounding check
"""
from __future__ import annotations

import argparse
import asyncio
import glob
import json
import os
import re
import sys
from collections import Counter

import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.data_loader import (  # noqa: E402
    GENERIC_PRACTICE_MARKERS,
    TEMPLATE_COMMENTARY_MARKERS,
    _commentary_is_authored,
    _practice_is_generic,
    _strip_layer_tail,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(ROOT, "data", "canonical")
OUT = os.path.join(ROOT, "data", "practice_audit.json")

# Extra generic markers — ONLY unambiguous boilerplate that data_loader's markers
# miss. Deliberately NARROW: openers like "sit quietly and…" or "notice how…" are
# how many GROUNDED practices legitimately begin, so they are NOT flagged here.
# Subtle generic/hallucinated cases are caught by the --ground model pass instead.
_PRACTICE_GENERIC_EXTRA = (
    "read this passage", "read this fragment", "read this line", "read the fragment",
    "read the line slowly", "read the excerpt slowly", "read once slowly",
    "write one sentence about how to apply",
)

# ---- pattern classification --------------------------------------------------

# Formulaic openers: the templated forms the render pipeline over-used. A single
# such practice is fine (many grounded practices legitimately begin "Sit quietly…");
# the DEFECT is collection-wide convergence — most practices sharing one form. So we
# tag `formulaic` per unit, then flag for form-reauthoring only where a collection's
# convergence is high.
FORMULAIC_OPENER = re.compile(
    r"^\s*(take one|pick one|choose one|bring to mind|sit quietly|sit comfortably|sit for|sit in|"
    r"spend (a|one|ten|five)|today,?\s|tonight|for the next|for one (day|week|minute)|set aside|"
    r"today notice|today practice|today pick|today choose|each (morning|night|day)|daily practice)\b",
    re.I,
)


def is_formulaic(text: str) -> bool:
    return bool(FORMULAIC_OPENER.match((text or "").strip()))


def classify_practice(text: str) -> str:
    p = (text or "").strip()
    if not p or p.lower() == "none":
        return "empty"
    low = p.lower()
    if _practice_is_generic(p) or any(m in low for m in _PRACTICE_GENERIC_EXTRA):
        return "generic"
    if len(p) < 40:
        return "thin"
    return "substantive"


def classify_commentary(text: str) -> str:
    c = _strip_layer_tail(str(text or ""))
    if not c.strip():
        return "empty"
    low = c.strip().lower()
    if any(low.startswith(m) for m in TEMPLATE_COMMENTARY_MARKERS):
        return "template"
    if not _commentary_is_authored(c):
        return "thin"
    return "substantive"


def decision(cls: str) -> str:
    return {"empty": "reauthor", "generic": "reauthor", "template": "reauthor",
            "thin": "review", "substantive": "keep"}[cls]


# ---- grounding pass (optional, model) ---------------------------------------

GROUND_SYSTEM = """You judge whether a study unit's PRACTICE and COMMENTARY are genuinely grounded in the given source passage, or are generic (could be pasted onto any text) or HALLUCINATED (assert images, claims, or instructions not present in or derivable from the passage).
Return ONLY JSON: {"practice_grounded":true/false,"practice_note":"...","commentary_grounded":true/false,"commentary_note":"..."}
Grounded = it uses this passage's specific language/instruction/imagery. Not grounded = generic OR invents content the passage doesn't support. Be strict."""


async def ground_unit(verse: str, practice: str, commentary: str):
    from app.llm import smart_chat
    user = (f"PASSAGE:\n{verse[:900]}\n\nPRACTICE:\n{practice[:600]}\n\n"
            f"COMMENTARY:\n{commentary[:1200]}\n\nJudge grounding as JSON.")
    txt = await smart_chat([{"role": "system", "content": GROUND_SYSTEM},
                            {"role": "user", "content": user}], temperature=0.2, max_tokens=400)
    txt = re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M).strip()
    try:
        return json.loads(txt)
    except Exception:
        m = re.search(r"\{.*\}", txt, re.S)
        return json.loads(m.group(0)) if m else None


def _verse_text(d: dict) -> str:
    for k in ("translation", "translation_literal"):
        v = str(d.get(k) or "").strip()
        if v and v.lower() != "none":
            return v
    return str(d.get("title") or "")


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--collection", help="limit to one collection dir")
    ap.add_argument("--ground", action="store_true", help="add independent model grounding check")
    ap.add_argument("--limit", type=int, default=0, help="cap units in the grounding pass")
    args = ap.parse_args()

    pattern = os.path.join(CANON, args.collection or "*", "**", "*.yml")
    files = [f for f in sorted(glob.glob(pattern, recursive=True)) if os.path.basename(f) != "_work.yml"]

    units: dict[str, dict] = {}
    prac_cls, comm_cls = Counter(), Counter()
    by_coll: dict[str, Counter] = {}

    coll_prac_total, coll_formulaic = Counter(), Counter()
    for f in files:
        d = yaml.safe_load(open(f, encoding="utf-8"))
        if not isinstance(d, dict):
            continue
        uid = str(d.get("unit_id") or d.get("_id") or os.path.basename(f))
        coll = os.path.basename(os.path.dirname(f))
        prac_text = str(d.get("abhyasa") or d.get("practice") or "")
        pr = classify_practice(prac_text)
        cm = classify_commentary(str(d.get("commentary") or ""))
        formulaic = pr == "substantive" and is_formulaic(prac_text)
        prac_cls[pr] += 1
        comm_cls[cm] += 1
        by_coll.setdefault(coll, Counter())[f"prac_{pr}"] += 1
        by_coll[coll][f"comm_{cm}"] += 1
        if prac_text.strip():
            coll_prac_total[coll] += 1
        if formulaic:
            coll_formulaic[coll] += 1
        units[uid] = {
            "file": os.path.relpath(f, ROOT), "collection": coll,
            "practice": {"class": pr, "decision": decision(pr), "formulaic": formulaic},
            "commentary": {"class": cm, "decision": decision(cm)},
            "grounded": None,
        }

    # Form-convergence pass: in collections where >=55% of practices share a
    # formulaic opener, the formulaic ones need form-reauthoring (grounded but
    # monotonous). A lone "Sit quietly…" in a varied collection is left alone.
    CONVERGE = 0.55
    converged = {c: round(coll_formulaic[c] / max(1, coll_prac_total[c]), 2)
                 for c in coll_prac_total if coll_formulaic[c] / max(1, coll_prac_total[c]) >= CONVERGE}
    for u in units.values():
        if u["practice"].get("formulaic") and u["collection"] in converged and u["practice"]["decision"] == "keep":
            u["practice"]["decision"] = "reauthor-form"

    # optional grounding pass: only on units that PASSED the pattern check (substantive),
    # since those are where hidden hallucination lives.
    if args.ground:
        candidates = [(uid, u) for uid, u in units.items()
                      if u["practice"]["class"] == "substantive" or u["commentary"]["class"] == "substantive"]
        if args.limit:
            candidates = candidates[: args.limit]
        print(f"grounding pass on {len(candidates)} substantive units...")
        for i, (uid, u) in enumerate(candidates, 1):
            d = yaml.safe_load(open(os.path.join(ROOT, u["file"]), encoding="utf-8"))
            try:
                g = await ground_unit(_verse_text(d), str(d.get("abhyasa") or d.get("practice") or ""),
                                      str(d.get("commentary") or ""))
            except Exception as e:
                print(f"[{i}] {uid}: ERR {e!r}"); continue
            if not g:
                continue
            u["grounded"] = g
            if g.get("practice_grounded") is False and u["practice"]["class"] == "substantive":
                u["practice"]["decision"] = "reauthor"  # hallucinated despite passing pattern
            if g.get("commentary_grounded") is False and u["commentary"]["class"] == "substantive":
                u["commentary"]["decision"] = "reauthor"

    prac_decisions = Counter(u["practice"]["decision"] for u in units.values())
    summary = {
        "total_units": len(units),
        "practice": dict(prac_cls),
        "commentary": dict(comm_cls),
        "practice_decisions": dict(prac_decisions),
        "practice_generic_or_empty": sum(1 for u in units.values() if u["practice"]["class"] in ("generic", "empty")),
        "practice_reauthor_form": sum(1 for u in units.values() if u["practice"]["decision"] == "reauthor-form"),
        "commentary_to_fix": sum(1 for u in units.values() if u["commentary"]["decision"] != "keep"),
        "converged_collections": converged,
    }
    json.dump({"summary": summary, "by_collection": {k: dict(v) for k, v in by_coll.items()}, "units": units},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("=== PRACTICE class ===", dict(prac_cls))
    print("=== PRACTICE decisions ===", dict(prac_decisions))
    print("=== COMMENTARY ===", dict(comm_cls))
    print(f"\nTRUE-generic/empty practices: {summary['practice_generic_or_empty']}")
    print(f"Grounded-but-FORMULAIC (form-reauthor): {summary['practice_reauthor_form']}")
    print(f"Commentary to fix: {summary['commentary_to_fix']}")
    print(f"\nform-converged collections (>=55% formulaic openers):")
    for c, pct in sorted(converged.items(), key=lambda kv: -kv[1]):
        print(f"  {c:42s} {int(pct*100)}%")
    print("\ntop collections needing work (practice generic/empty + commentary template/empty):")
    scored = sorted(by_coll.items(),
                    key=lambda kv: -(kv[1].get("prac_generic", 0) + kv[1].get("prac_empty", 0)
                                     + kv[1].get("comm_template", 0) + kv[1].get("comm_empty", 0)))
    for c, v in scored[:14]:
        pbad = v.get("prac_generic", 0) + v.get("prac_empty", 0) + v.get("prac_thin", 0)
        cbad = v.get("comm_template", 0) + v.get("comm_empty", 0) + v.get("comm_thin", 0)
        if pbad or cbad:
            print(f"  {c:42s} practice_bad={pbad:3d}  commentary_bad={cbad:3d}")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
