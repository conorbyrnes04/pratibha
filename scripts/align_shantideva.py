#!/usr/bin/env python3
"""Align each Śāntideva Bodhicaryāvatāra unit to its actual PD Sanskrit verses
(GRETIL) and render fresh English FROM the Sanskrit.

Our 8 units are thematic selections from BCA ch. 8 (Dhyāna) and ch. 9 (Prajñā).
For each unit we give the model that chapter's verses and its current (possibly
copyright-influenced) English only as a POINTER to locate the matching verses;
the model returns the matching verse tags + a fresh rendering from the Sanskrit.
The located Sanskrit is stored on the unit; provenance is stamped PD-Sanskrit.

    python scripts/align_shantideva.py            # preview
    python scripts/align_shantideva.py --write
"""
from __future__ import annotations
import argparse, asyncio, glob, json, os, re, sys
import yaml
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import settings          # noqa: E402
from app.llm import smart_chat           # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data/raw_texts/pd/indian/bodhicaryavatara_gretil_iast_sanskrit.txt")
UNITS = os.path.join(ROOT, "data/canonical/shantideva_bodhicaryavatara")


def load_verses() -> dict[str, str]:
    """Map 'Bca_8.90' -> Sanskrit verse text (2 lines joined)."""
    raw = open(SRC, encoding="utf-8").read()
    verses: dict[str, str] = {}
    # Each verse ends with '// Bca_C.V'; text precedes the tag, may span 2 lines.
    for m in re.finditer(r"(.*?)//\s*Bca_(\d+)\.(\d+)", raw, re.S):
        body = " ".join(m.group(1).split())
        # keep only the tail after the previous tag
        body = body.split("//")[-1].strip()
        verses[f"{m.group(2)}.{m.group(3)}"] = body
    return verses


def chapter_block(verses: dict[str, str], chap: int) -> str:
    rows = [(int(k.split(".")[1]), k, v) for k, v in verses.items() if k.startswith(f"{chap}.")]
    rows.sort()
    return "\n".join(f"[{k}] {v}" for _, k, v in rows)


SYSTEM = """You align a study unit to the Sanskrit verses it is based on, then translate FROM the Sanskrit.
You are given the Sanskrit verses of one chapter of Śāntideva's Bodhicaryāvatāra (each tagged [8.NN]) and a study unit's theme + its current English (which may derive from a copyrighted translation — use it ONLY to locate the matching verses, never as your translation source).
Return ONLY JSON:
{"verse_tags": ["8.90","8.91",...], "translation": "...", "commentary": "...", "practice": "...", "key_terms": [{"term":"...","definition":"..."}]}
- verse_tags: the 3–8 verses this unit is actually based on.
- translation: fresh English rendered from THOSE Sanskrit verses — your own words from the Sanskrit, not a paraphrase of the given English or any published translation.
- commentary: publishable study commentary on what these verses teach; practice: one concrete practice. Keep genuine Sanskrit terms (bodhicitta, śūnyatā, saṃvṛti) with a gloss."""


async def align_unit(item: dict, verses: dict[str, str], chap: int) -> dict | None:
    title = item.get("title") or ""
    cur = str(item.get("translation_literal") or "")[:600]
    user = (f"Bodhicaryāvatāra chapter {chap} verses:\n{chapter_block(verses, chap)}\n\n"
            f"UNIT THEME: {title}\nUNIT CURRENT ENGLISH (pointer only): {cur}\n\n"
            "Return the JSON.")
    txt = await smart_chat([{"role":"system","content":SYSTEM},{"role":"user","content":user}],
                           temperature=0.4, max_tokens=1800)
    txt = re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M).strip()
    try:
        return json.loads(txt)
    except Exception:
        m = re.search(r"\{.*\}", txt, re.S)
        return json.loads(m.group(0)) if m else None


def _kt_tail(kts):
    if not isinstance(kts, list) or not kts: return ""
    out=["","Key Terms",""]
    for k in kts[:3]:
        if isinstance(k,dict) and k.get("term"): out.append(f"**{k['term']}** — {k.get('definition','')}")
    return "\n".join(out) if len(out)>3 else ""


async def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--write",action="store_true"); ap.add_argument("--limit",type=int,default=0)
    a = ap.parse_args()
    if not settings.OPENROUTER_API_KEY: sys.exit("set OPENROUTER_API_KEY")
    verses = load_verses()
    print(f"parsed {len(verses)} BCA verses; ch8={sum(k.startswith('8.') for k in verses)}, ch9={sum(k.startswith('9.') for k in verses)}")
    files = sorted(glob.glob(os.path.join(UNITS,"**","*.yml"),recursive=True))
    if a.limit: files=files[:a.limit]
    for i,f in enumerate(files,1):
        d = yaml.safe_load(open(f,encoding="utf-8")); name=os.path.basename(f)
        # Idempotent: skip units already aligned so a resume only does the rest.
        if a.write and "public-domain Sanskrit (GRETIL" in str(d.get("translation_provenance") or ""):
            continue
        chap = 9 if "_09_" in name else 8
        try: r = await align_unit(d, verses, chap)
        except Exception as e: print(f"[{i}] {name}: ERR {e!r}"); continue
        if not r: print(f"[{i}] {name}: no json"); continue
        tags = r.get("verse_tags") or []
        skt = "\n".join(f"{t}: {verses.get(t,'')}" for t in tags if t in verses)
        print(f"[{i}] {name}: verses {tags} | {str(r.get('translation'))[:70]}")
        if a.write and skt:
            d["sanskrit_iast"] = skt
            d["translation"] = d["translation_literal"] = str(r.get("translation") or "").strip()
            tail=_kt_tail(r.get("key_terms"))
            d["commentary"] = (str(r.get("commentary") or "").strip()+("\n"+tail if tail else "")).strip()
            d["practice"] = d["abhyasa"] = str(r.get("practice") or "").strip()
            d["editorial_maturity"]="strong_draft"
            d["translation_provenance"]=f"Rendered from the public-domain Sanskrit (GRETIL, BCA {','.join(tags)}). Study rendering."
            d.pop("pratibha_layers",None)
            yaml.safe_dump(d, open(f,"w",encoding="utf-8"), allow_unicode=True, sort_keys=False, width=100)
    print("done" + (" (WRITE)" if a.write else " (preview)"))

if __name__=="__main__":
    asyncio.run(main())
