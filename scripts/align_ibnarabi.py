#!/usr/bin/env python3
"""Reground the Ibn ʿArabī / Balyānī "Know Yourself" units on the PUBLIC-DOMAIN
T. H. Weir translation (JRAS 1901), replacing the copyrighted-lineage (Twinch)
English they were demoted for.

Weir's 1901 English is public domain, so we may legitimately modernize it. For
each unit we give the model Weir's full treatise + the unit's current English
(as a locator only) and ask for a clean modern rendering of the MATCHING Weir
passage + study commentary. Units are re-promoted to strong_draft with Weir
provenance.

    python scripts/align_ibnarabi.py            # preview
    python scripts/align_ibnarabi.py --write
"""
from __future__ import annotations
import argparse, asyncio, glob, json, os, re, sys
import yaml
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import settings          # noqa: E402
from app.llm import smart_chat           # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEIR = os.path.join(ROOT, "data/raw_texts/pd/arabic/ibn_arabi_balyani_weir_jras_1901.txt")
UNITS = os.path.join(ROOT, "data/canonical/know_yourself_ibn_arabi_balyani")

SYSTEM = """You reground a study unit on a PUBLIC-DOMAIN source translation.
You are given T. H. Weir's 1901 public-domain English translation of the Sufi treatise "Whoso Knoweth Himself Knoweth His Lord" (Balyānī, long ascribed to Ibn ʿArabī), and a study unit's theme + its current English (which derives from a COPYRIGHTED modern translation — use it ONLY to locate the matching passage; never reproduce it).
Return ONLY JSON:
{"translation":"...", "commentary":"...", "practice":"...", "key_terms":[{"term":"...","definition":"..."}]}
- translation: a clean, lightly-modernized rendering of the MATCHING passage of WEIR's public-domain text — smooth out Weir's archaic 1901 grammar and OCR artifacts, but stay faithful to Weir's wording and meaning. This is your source, and it is free to use.
- commentary: publishable study commentary on what the passage teaches (the oneness of being / waḥdat al-wujūd, self-knowledge as knowledge of God, the critique of 'ceasing to be'); practice: one concrete contemplative practice.
- key_terms: 1–3 relevant terms (e.g. tawḥīd, fanā, ma'rifa) with a gloss, or []."""


async def rende(item: dict, weir: str) -> dict | None:
    cur = str(item.get("translation_literal") or "")[:500]
    user = (f"WEIR 1901 (public-domain source):\n{weir}\n\n"
            f"UNIT THEME: {item.get('title')}\nUNIT CURRENT ENGLISH (locator only, copyrighted — do not reuse): {cur}\n\n"
            "Return the JSON for the matching Weir passage.")
    txt = await smart_chat([{"role":"system","content":SYSTEM},{"role":"user","content":user}],
                           temperature=0.4, max_tokens=1500)
    txt = re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M).strip()
    try: return json.loads(txt)
    except Exception:
        m = re.search(r"\{.*\}", txt, re.S); return json.loads(m.group(0)) if m else None


def _kt_tail(kts):
    if not isinstance(kts,list) or not kts: return ""
    out=["","Key Terms",""]
    for k in kts[:3]:
        if isinstance(k,dict) and k.get("term"): out.append(f"**{k['term']}** — {k.get('definition','')}")
    return "\n".join(out) if len(out)>3 else ""


async def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--write",action="store_true"); ap.add_argument("--limit",type=int,default=0)
    a=ap.parse_args()
    if not settings.OPENROUTER_API_KEY: sys.exit("set OPENROUTER_API_KEY")
    weir=open(WEIR,encoding="utf-8").read()
    files=sorted(glob.glob(os.path.join(UNITS,"**","*.yml"),recursive=True))
    if a.limit: files=files[:a.limit]
    print(f"Ibn ʿArabī: {len(files)} units, Weir source {len(weir.split())} words, model={settings.effective_default_model()}")
    for i,f in enumerate(files,1):
        d=yaml.safe_load(open(f,encoding="utf-8")); name=os.path.basename(f)
        if a.write and "Based on the public-domain English translation by T. H. Weir" in str(d.get("translation_provenance") or ""): continue
        try: r=await rende(d,weir)
        except Exception as e: print(f"[{i}] {name}: ERR {e!r}"); continue
        if not r: print(f"[{i}] {name}: no json"); continue
        print(f"[{i}] {name}: {str(r.get('translation'))[:75]}")
        if a.write:
            tail=_kt_tail(r.get("key_terms"))
            d["translation"]=d["translation_literal"]=str(r.get("translation") or "").strip()
            d["commentary"]=(str(r.get("commentary") or "").strip()+("\n"+tail if tail else "")).strip()
            d["practice"]=d["abhyasa"]=str(r.get("practice") or "").strip()
            d["editorial_maturity"]="strong_draft"   # un-demote
            d["translation_provenance"]="Based on the public-domain English translation by T. H. Weir (JRAS, 1901), lightly modernized. Study rendering."
            d.pop("pratibha_layers",None)
            yaml.safe_dump(d, open(f,"w",encoding="utf-8"), allow_unicode=True, sort_keys=False, width=100)
    print("done"+(" (WRITE)" if a.write else " (preview)"))

if __name__=="__main__":
    asyncio.run(main())
