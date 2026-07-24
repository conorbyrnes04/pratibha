#!/usr/bin/env python3
"""Author real study commentary for units the audit flagged as template/thin/empty.

Reads data/practice_audit.json for units where commentary.decision != "keep"
(template filler, too-thin, or empty). For each, writes substantial study
commentary grounded in that unit's own verse — keeping the translation intact
(important for Śiva Sūtra, which is the author's own translation).

    python scripts/reauthor_commentary.py --limit 3          # preview
    python scripts/reauthor_commentary.py --write
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
from scripts.render_from_sanskrit import COLLECTIONS, _DEFAULT_CTX  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIT = os.path.join(ROOT, "data", "practice_audit.json")


def system_for(collection: str) -> str:
    work, focus = COLLECTIONS.get(collection, _DEFAULT_CTX)
    return f"""You write publishable study commentary for a unit of {work}, grounded in its SPECIFIC passage.
Write commentary that unpacks THIS passage: {focus}. State its central move or claim, situate it in the tradition's framework, and draw out the insight in clear, rigorous, unhurried prose — the register of a scholar who also practices. No throat-clearing ("This passage invites us to…"), no generic filler. Roughly 700-1400 characters. Keep genuine source-language terms with a brief gloss.
Then give 1-3 key terms (source-language term + one-line gloss), or [].
Return ONLY JSON: {{"commentary":"...", "key_terms":[{{"term":"...","definition":"..."}}]}}"""


def _kt_tail(kts):
    if not isinstance(kts, list) or not kts:
        return ""
    lines = ["", "Key Terms", ""]
    for k in kts[:3]:
        if isinstance(k, dict) and k.get("term"):
            lines.append(f"**{k['term']}** — {k.get('definition', '')}")
    return "\n".join(lines) if len(lines) > 3 else ""


async def author(collection: str, verse: str, title: str, old: str) -> dict | None:
    user = (f"Passage title: {title}\nTranslation: {verse[:900]}\n"
            + (f"(Current commentary is filler/thin, replace it: {old[:200]})\n" if old.strip() else "")
            + "\nWrite the commentary + key_terms as JSON.")
    txt = await smart_chat([{"role": "system", "content": system_for(collection)},
                            {"role": "user", "content": user}], temperature=0.5, max_tokens=1200)
    txt = re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M).strip()
    try:
        return json.loads(txt)
    except Exception:
        m = re.search(r"\{.*\}", txt, re.S)
        return json.loads(m.group(0)) if m else None


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--collection")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    if not settings.OPENROUTER_API_KEY:
        sys.exit("set OPENROUTER_API_KEY")

    audit = json.load(open(AUDIT, encoding="utf-8"))
    todo = [(uid, u) for uid, u in audit["units"].items()
            if u["commentary"]["decision"] != "keep"
            and (not args.collection or u["collection"] == args.collection)]
    if args.limit:
        todo = todo[: args.limit]
    print(f"commentary to author: {len(todo)}, model={settings.effective_default_model()}\n")

    done = 0
    for i, (uid, u) in enumerate(todo, 1):
        path = os.path.join(ROOT, u["file"])
        d = yaml.safe_load(open(path, encoding="utf-8"))
        if args.write and "authored study commentary" in str(d.get("commentary_provenance") or ""):
            continue
        verse = str(d.get("translation") or d.get("translation_literal") or d.get("title") or "")
        old = str(d.get("commentary") or "")
        r = await author(u["collection"], verse, str(d.get("title") or ""), old)
        if not r:
            print(f"[{i}] {uid}: no commentary"); continue
        commentary = str(r.get("commentary") or "").strip()
        tail = _kt_tail(r.get("key_terms"))
        full = (commentary + ("\n" + tail if tail else "")).strip()
        print(f"[{i}] {u['collection']}/{d.get('title','')[:24]:24s} → {commentary[:90]}")
        if args.write and len(commentary) >= 200:
            d["commentary"] = full
            d["commentary_provenance"] = "Study commentary authored from the passage."
            d.pop("pratibha_layers", None)
            yaml.safe_dump(d, open(path, "w", encoding="utf-8"), allow_unicode=True, sort_keys=False, width=100)
            done += 1
    print(f"\nauthored {done} commentaries" if args.write else "(preview)")


if __name__ == "__main__":
    asyncio.run(main())
