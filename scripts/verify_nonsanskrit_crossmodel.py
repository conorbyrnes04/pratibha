#!/usr/bin/env python3
"""Cross-model verification of model-supplied NON-Sanskrit originals (Persian,
Greek, Chinese, Arabic). Luna checks the stored original against the received
text; applies a confident correction directly to the original field; upgrades
provenance. No transliteration involved."""
import asyncio, glob, json, os, re, sys
import yaml
sys.path.insert(0, "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha")
from app.llm import smart_chat
from app.data_loader import _as_text

COLLS = {
    "rumi_mathnawi": "Rūmī's Mathnawī (Persian)", "plotinus_enneads": "Plotinus's Enneads (Greek)",
    "confucius_analects": "the Analects of Confucius (Classical Chinese)",
    "the_book_of_chuang_tzu": "the Zhuangzi (Classical Chinese)",
    "know_yourself_ibn_arabi_balyani": "the Treatise on Unity (Arabic)",
    "dōgen_shōbōgenzō": "Dōgen's Shōbōgenzō (Japanese/Sino-Japanese)",
    "marcus_aurelius_meditations": "Marcus Aurelius's Meditations (Greek)",
    "meister_eckhart": "Meister Eckhart's sermons (Middle High German/Latin)",
    "zhongyong": "the Zhōngyōng (Classical Chinese)", "epictetus_works": "Epictetus (Greek)",
    "milarepa_songs": "Milarepa's songs (Tibetan)", "phaedo_plato": "Plato's Phaedo (Greek)",
    "pseudo_dionysius": "Pseudo-Dionysius (Greek)",
}

SYS = ("You verify a passage's ORIGINAL-language text against the received text of the named work. "
       "Judge only whether the quoted original is accurate (allowing minor orthographic variation). If the passage "
       "is loosely attributed or you cannot verify the exact original, say uncertain rather than guessing.\n"
       'Return ONLY JSON: {"verdict":"correct"|"corrected"|"uncertain","corrected_original":"<full corrected original if confident, else empty>","note":"<short reason>"}')


async def verify(path, name, sem):
    d = yaml.safe_load(open(path))
    prov = d.get("provenance") if isinstance(d.get("provenance"), dict) else {}
    orig = _as_text(d.get("sanskrit_devanagari"))
    if not orig or "model-supplied" not in str(prov.get("original_source", "")) + str(prov.get("sanskrit_source", "")):
        return path, "skip"
    ref = _as_text(d.get("section")) or _as_text(d.get("title"))
    async with sem:
        r = None
        for attempt in range(3):
            try:
                r = await smart_chat([{"role": "system", "content": SYS},
                                      {"role": "user", "content": f"Work: {name}\nContext: {ref}\nOriginal to verify:\n{orig[:300]}\n\nReturn JSON."}],
                                     primary_model="openai/gpt-5.6-luna", temperature=0.0, max_tokens=500)
                break
            except Exception:
                await asyncio.sleep(2 * (attempt + 1))
        if r is None:
            return path, "ERR"
    m = re.search(r"\{.*\}", re.sub(r"^```(?:json)?|```$", "", r.strip(), flags=re.M), re.S)
    try:
        v = json.loads(m.group(0))
    except Exception:
        return path, "parse"
    verdict = v.get("verdict", "uncertain")
    prov["verification"] = f"cross-model (Luna): {verdict}"
    if v.get("note"):
        prov["verification_note"] = v["note"][:200]
    if verdict == "corrected" and v.get("corrected_original", "").strip():
        d["sanskrit_devanagari"] = v["corrected_original"].strip()
    d["provenance"] = prov
    yaml.safe_dump(d, open(path, "w"), allow_unicode=True, sort_keys=False, width=120)
    return path, verdict


async def main():
    sem = asyncio.Semaphore(3)
    tasks = []
    for coll, name in COLLS.items():
        for path in glob.glob(f"/Users/conorbyrnes04/Documents/Projects/VAK/pratibha/data/canonical/{coll}/*.yml"):
            d = yaml.safe_load(open(path))
            prov = d.get("provenance") or {}
            if "2026" in str(prov.get("english_source", "")):
                tasks.append(verify(path, name, sem))
    res = await asyncio.gather(*tasks)
    import collections
    print("non-Sanskrit verification:", dict(collections.Counter(v for _, v in res)))


if __name__ == "__main__":
    asyncio.run(main())
