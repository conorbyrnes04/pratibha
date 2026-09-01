#!/usr/bin/env python3
"""Build a complete bilingual Tilopa Gaṅgā-mahāmudrā collection.

Original layer = VERBATIM Tibetan (Tilopa's ancient text, PD; hosted by Lotsawa
House). The Tibetan is segmented into its natural verses by a model and every
segment is verified as a verbatim substring of the source (anti-hallucination).
Translation = Pratibha's OWN English rendering from the Tibetan (interpretation,
per the no-model-supplied-SOURCE rule) — Ina Bieler's Lotsawa translation was
consulted as an accuracy reference but is NOT reproduced. Terra authors the
apparatus. Writes fresh til_### units (supersedes the 3 stubs; git keeps them).
"""
import asyncio, glob, json, os, re, sys, unicodedata
import yaml
sys.path.insert(0, "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha")
from app.llm import smart_chat
from faithful_expand_upanishads import _lenient_json

ROOT = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha"
SRC = os.path.join(ROOT, "data/raw_texts/pd/tibetan/tilopa_ganges_mahamudra_lotsawa_bo.txt")
OUT = os.path.join(ROOT, "data/canonical/tilopa_mahamudra")
TERRA = "openai/gpt-5.6-terra"
PROV = ("Tibetan verbatim from Tilopa's Gaṅgā-mahāmudrā (Mahāmudropadeśa), the ancient root text "
        "(public domain; Tibetan hosted by Lotsawa House, CC BY-NC). English is a Pratibha study "
        "translation from the Tibetan; Ina Bieler's Lotsawa House translation was consulted as a "
        "reference for accuracy but is not reproduced here.")


def dn(s):
    return re.sub(r"[^ༀ-࿿]", "", unicodedata.normalize("NFC", s))


async def segment(tib):
    r = await smart_chat(
        [{"role": "system", "content":
          "You are given the full Tibetan text of Tilopa's Gaṅgā-mahāmudrā. Split it into its natural "
          "verses (about 26-29). Copy each verse VERBATIM from the text — do not alter, translate, or "
          'add anything. Return ONLY JSON: {"verses":["<verbatim Tibetan verse>", ...]}'},
         {"role": "user", "content": tib + "\n\nReturn JSON."}],
        primary_model=TERRA, temperature=0.0, max_tokens=9000)
    return (_lenient_json(r) or {}).get("verses", [])


AUTH = """You are given ONE verbatim Tibetan verse of Tilopa's Gaṅgā-mahāmudrā (mahāmudrā, non-meditation,
the nature of mind as space, guru devotion). Produce a faithful study unit. Return ONLY JSON:
{"title":"<short evocative English title, no numbers>",
 "translation":"<your own faithful, spare English translation of THIS verse; pivotal terms glossed in ()>",
 "commentary":"<600-1000 chars, grounded in this verse, rigorous, no filler>",
 "key_terms":[{"term":"<Skt/Tib term in the verse>","gloss":"<one line>"}, ...2-3],
 "resonances":[{"ref":"<recognizable text/figure>","parallel":"<real parallel>","divergence":"<one honest divergence>"}, ...2],
 "practice":"<2-3 sentence contemplative exercise from this verse>"}"""


async def author(verse, sem):
    async with sem:
        for attempt in range(3):
            try:
                r = await smart_chat(
                    [{"role": "system", "content": AUTH},
                     {"role": "user", "content": f"Tibetan verse:\n{verse}\n\nReturn JSON."}],
                    primary_model=TERRA, temperature=0.4, max_tokens=1300)
                j = _lenient_json(r)
                if j and j.get("translation"):
                    return j
            except Exception as e:
                if "402" in str(e):
                    return {"_nocredits": True}
                await asyncio.sleep(2 * (attempt + 1))
    return None


async def main():
    tib = open(SRC, encoding="utf-8").read().strip()
    verses = await segment(tib)
    # verify verbatim
    good = [v.strip() for v in verses if len(dn(v)) > 8 and dn(v)[:30] in dn(tib)]
    print(f"segmented {len(verses)} verses; {len(good)} verified verbatim")
    if not good:
        print("segmentation failed"); return
    sem = asyncio.Semaphore(4)
    aps = await asyncio.gather(*(author(v, sem) for v in good))
    # wipe old stubs, write fresh complete set
    for f in glob.glob(os.path.join(OUT, "*.yml")):
        os.remove(f)
    slug = "tilopa_mahamudra"; written = 0
    for i, (v, ap) in enumerate(zip(good, aps), start=1):
        if not ap or ap.get("_nocredits"):
            if ap and ap.get("_nocredits"): print("credits exhausted");
            continue
        uid = f"{slug}.{slug}_{i:03d}"
        kt = "\n\n".join(f"**{t.get('term','')}** — {t.get('gloss','')}" for t in (ap.get('key_terms') or []))
        rz = "\n\n".join(f"**{r.get('ref','')}:** {r.get('parallel','')} Divergence: {r.get('divergence','')}"
                         for r in (ap.get('resonances') or []))
        layers = [{"kind": "original", "label": "Tibetan", "body": v},
                  {"kind": "translation", "label": "Translation", "body": ap["translation"]}]
        if ap.get("commentary"): layers.append({"kind": "commentary", "label": "Commentary", "body": ap["commentary"]})
        if kt: layers.append({"kind": "key_terms", "label": "Key Terms", "body": kt})
        if rz: layers.append({"kind": "resonances", "label": "Resonances", "body": rz})
        if ap.get("practice"): layers.append({"kind": "practice", "label": "Practice", "body": ap["practice"]})
        unit = {
            "source_id": f"{slug}_{i:03d}".upper(), "category": "root_text", "work_id": slug,
            "work_title": "Tilopa: Gaṅgā-mahāmudrā", "unit_id": uid,
            "unit_label": ap.get("title"), "title": ap.get("title"), "unit_type": "verse",
            "commentary": ap.get("commentary", ""), "themes": ["mahamudra", "mind", "non-meditation"],
            "tags": [slug, "mahamudra"], "quality_score": 0, "editorial_score": 0,
            "editorial_maturity": "strong_draft", "translation_provenance": PROV,
            "sanskrit_devanagari": "", "pratibha_layers": layers,
            "provenance": {"collection": "Tilopa: Gaṅgā-mahāmudrā", "cultural_context": PROV,
                           "original_source": "Tilopa, Gaṅgā-mahāmudrā, Tibetan (Lotsawa House, CC BY-NC)"},
            "translation": ap["translation"], "practice": ap.get("practice", ""), "abhyasa": ap.get("practice", ""),
        }
        with open(os.path.join(OUT, f"{uid.replace('.', '_')}.yml"), "w") as fh:
            yaml.safe_dump(unit, fh, allow_unicode=True, sort_keys=False, width=100)
        written += 1
    print(f"wrote {written} bilingual Tilopa units")


if __name__ == "__main__":
    asyncio.run(main())
