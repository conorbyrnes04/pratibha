#!/usr/bin/env python3
"""Build Epictetus units from the REAL Carter Enchiridion (PD, classics.mit.edu) —
the source of record for the translation. Terra does ONLY interpretation
(commentary + key terms + resonances + practice), never source text. No fabricated
Greek. Honest provenance. Stages to data/staging/epictetus_real."""
import asyncio, json, os, re, sys
import yaml
sys.path.insert(0, "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha")
from app.llm import smart_chat
from app.data_loader import normalize_unit

SP = os.path.dirname(os.path.abspath(__file__))
STAGE = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha/data/staging/epictetus_real"
secs = {int(k): v for k, v in json.load(open(f"{SP}/enchiridion_secs.json")).items()}
# canonical sections to add (avoid pre-existing 1,5,17), spread across the work
PICK = [2, 3, 4, 8, 9, 11, 13, 15, 19, 20, 33, 43, 48]

SYS = ("You write a study unit for one section of Epictetus's Enchiridion. You are given Carter's public-domain "
       "English (the fixed source text — do NOT rewrite it as the translation). Produce interpretation only:\n"
       "- title: short evocative English title.\n"
       "- commentary: 700-1200 chars, rigorous Stoic reading, no filler.\n"
       "- key_terms: 2-4 Greek Stoic terms relevant to this section (term + one-line gloss), e.g. prohairesis, eph' hēmin, apatheia.\n"
       "- resonances: 3 cross-tradition parallels (recognizable text/figure + real parallel + honest divergence; no invented citations).\n"
       "- practice: one concrete contemplative instruction.\n"
       "Return ONLY JSON with those keys.")


async def one(n, sem):
    text = secs[n]
    async with sem:
        for a in range(3):
            try:
                r = await smart_chat([{"role": "system", "content": SYS},
                                      {"role": "user", "content": f"Enchiridion section {n} (Carter, PD):\n{text[:900]}\n\nReturn JSON."}],
                                     primary_model="openai/gpt-5.6-terra", temperature=0.4, max_tokens=1200)
                break
            except Exception:
                await asyncio.sleep(2 * (a + 1)); r = None
        if r is None:
            return n, None
    m = re.search(r"\{.*\}", re.sub(r"^```(?:json)?|```$", "", r.strip(), flags=re.M), re.S)
    try:
        return n, json.loads(m.group(0))
    except Exception:
        return n, None


def tail(d):
    out = ""
    kts = [k for k in d.get("key_terms", []) if isinstance(k, dict) and k.get("term")]
    if kts:
        out += "\n\nKey Terms\n\n" + "\n".join(f"**{k['term']}** — {(k.get('definition') or k.get('gloss') or '').strip()}" for k in kts[:4])
    res = [r for r in d.get("resonances", []) if isinstance(r, dict) and (r.get("citation") or r.get("parallel"))]
    if res:
        L = []
        for r in res[:3]:
            c = (r.get("citation") or r.get("parallel") or "").strip()
            b = (r.get("resonance") or r.get("connection") or "").strip()
            if r.get("divergence", "").strip():
                b += f" Divergence: {r['divergence'].strip()}"
            L.append(f"**{c}:** {b}")
        out += "\n\nCross-Tradition Resonances\n\n" + "\n".join(L)
    return out


async def main():
    os.makedirs(STAGE, exist_ok=True)
    sem = asyncio.Semaphore(4)
    res = await asyncio.gather(*(one(n, sem) for n in PICK if n in secs))
    ok = 0
    for n, data in res:
        if not data or not data.get("commentary"):
            print(f"  FAIL sec {n}"); continue
        unit = {
            "source_id": f"ENCH_{n:02d}", "category": "root_text", "work_id": "epictetus_works",
            "work_title": "Epictetus Works", "unit_id": f"epictetus_works.ench_{n:02d}",
            "unit_label": data["title"], "title": data["title"], "unit_type": "verse",
            "section": f"Enchiridion {n}",
            "translation_literal": secs[n],   # Carter's real PD text = translation of record
            "commentary": (data["commentary"].strip() + tail(data)),
            "practice": data.get("practice", ""), "themes": [], "tags": [],
            "provenance": {"collection": "Epictetus Works",
                           "english_source": "Elizabeth Carter, The Enchiridion of Epictetus (1758, public domain; classics.mit.edu). Source of record — not model-generated.",
                           "verification": "PD source (Carter 1758)"},
        }
        nm = normalize_unit(unit, "")
        print(f"  ench_{n:02d} [{nm['editorial_maturity']}] '{data['title'][:34]}'")
        with open(os.path.join(STAGE, f"epictetus_works_ench_{n:02d}.yml"), "w") as fh:
            yaml.safe_dump(unit, fh, allow_unicode=True, sort_keys=False, width=120)
        ok += 1
    print(f"wrote {ok}")

asyncio.run(main())
