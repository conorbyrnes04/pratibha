#!/usr/bin/env python3
"""Add new Milarepa song units from the PUBLIC-DOMAIN Evans-Wentz / Kazi
Dawa-Samdup translation (1928), which contains the songs embedded in the life
story. We select well-spaced songs the corpus doesn't already have, modernize
the PD verses, and author a full study unit for each.

    python scripts/build_milarepa_songs.py --n 7            # preview
    python scripts/build_milarepa_songs.py --n 7 --write
"""
from __future__ import annotations
import argparse, asyncio, json, os, re, sys
import yaml
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import settings          # noqa: E402
from app.llm import smart_chat           # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data/raw_texts/pd/tibetan/milarepa_evans_wentz_1928.txt")
OUT = os.path.join(ROOT, "data/canonical/milarepa_songs")

MARKER = re.compile(r"sang (?:this|the following)(?: song| hymn| verses)?[^:]{0,40}:", re.I)


def candidate_songs(text: str, n: int) -> list[str]:
    """Grab the verse block after each 'sang the following song:' marker."""
    starts = [m.end() for m in MARKER.finditer(text)]
    blocks = []
    for s in starts:
        block = text[s:s+2200]                 # ~song-length window
        # cut at the first long prose paragraph after the verses (heuristic)
        block = re.split(r"\n\s*\n(?=[A-Z][a-z]+ [a-z]+ [a-z]+ [a-z]+ [a-z]+ [a-z]+ [a-z]+ [a-z]+)", block)[0]
        block = " ".join(block.split())
        if len(block.split()) >= 90:
            blocks.append(block)
    # evenly spaced selection across the book
    if len(blocks) <= n:
        return blocks
    step = len(blocks) / n
    return [blocks[int(i*step)] for i in range(n)]


SYSTEM = """You are authoring a study unit for one song of Milarepa, from the PUBLIC-DOMAIN Evans-Wentz / Kazi Dawa-Samdup translation (1928). You are given a raw song passage (archaic English + OCR noise).
Return ONLY JSON:
{"title":"...", "translation":"...", "commentary":"...", "practice":"...", "themes":["..."], "keep":true}
- title: a short evocative English title for the song.
- translation: the song's verses, lightly modernized from this public-domain text (fix archaic grammar and OCR errors; keep the imagery and meaning; verse lines separated by newlines). This PD text is free to use.
- commentary: publishable study commentary on what this song teaches (Milarepa's yogic realization, impermanence, mahāmudrā, guru-devotion, the hardships of practice).
- practice: one concrete contemplative practice drawn from the song.
- themes: 3-6 lowercase theme tags (e.g. impermanence, renunciation, mahamudra, mind, devotion, solitude).
- keep: false ONLY if the passage is not actually a coherent song worth including; else true."""


async def author(block: str) -> dict | None:
    txt = await smart_chat([{"role":"system","content":SYSTEM},
                            {"role":"user","content":f"Song passage (Evans-Wentz 1928, PD):\n{block}\n\nAuthor the unit as JSON."}],
                           temperature=0.5, max_tokens=1600)
    txt = re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M).strip()
    try: return json.loads(txt)
    except Exception:
        m = re.search(r"\{.*\}", txt, re.S); return json.loads(m.group(0)) if m else None


def write_unit(idx: int, r: dict):
    sid = f"mil_ew_{idx:03d}"
    unit = {
        "unit_id": f"milarepa_songs.{sid}", "source_id": sid,
        "unit_label": r.get("title"), "title": r.get("title"),
        "work_title": "Milarepa Songs", "work_id": "milarepa_songs",
        "unit_type": "sutra", "category": "root_text",
        "translation": r.get("translation"), "translation_literal": r.get("translation"),
        "commentary": str(r.get("commentary") or "").strip(),
        "practice": str(r.get("practice") or "").strip(), "abhyasa": str(r.get("practice") or "").strip(),
        "themes": r.get("themes") or [], "tags": r.get("themes") or [],
        "provenance": {"collection": "Milarepa Songs", "section": "Songs (Jetsün-Kahbum)",
                       "original_id": sid.upper(), "source_reference": "Evans-Wentz / Kazi Dawa-Samdup 1928 (public domain)"},
        "editorial_maturity": "strong_draft",
        "translation_provenance": "Modernized from the public-domain Evans-Wentz / Kazi Dawa-Samdup translation (1928). Study rendering.",
    }
    path = os.path.join(OUT, f"milarepa_songs_{sid}.yml")
    yaml.safe_dump(unit, open(path,"w",encoding="utf-8"), allow_unicode=True, sort_keys=False, width=100)
    return path


async def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--n",type=int,default=7); ap.add_argument("--write",action="store_true")
    a=ap.parse_args()
    if not settings.OPENROUTER_API_KEY: sys.exit("set OPENROUTER_API_KEY")
    blocks = candidate_songs(open(SRC,encoding="utf-8").read(), a.n)
    print(f"selected {len(blocks)} candidate songs, model={settings.effective_default_model()}")
    made=0
    for i, block in enumerate(blocks, start=15):   # continue numbering after the 14 existing
        try: r = await author(block)
        except Exception as e: print(f"[{i}] ERR {e!r}"); continue
        if not r or not r.get("keep", True): print(f"[{i}] skipped (not a song)"); continue
        print(f"[{i}] {r.get('title')} — themes {r.get('themes')}")
        if a.write: made+=1; print("    ->", os.path.basename(write_unit(i, r)))
    print(f"done: {made} new song units" if a.write else "done (preview)")

if __name__=="__main__":
    asyncio.run(main())
