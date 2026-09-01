#!/usr/bin/env python3
"""Ingest ʿAṭṭār's Conference of the Birds + Hujwīrī's Kashf al-Maḥjūb,
and enrich the Balyānī / Ibn ʿArabī Know Yourself units.

English is pd_adapted from named PD cribs (Masani 1924, Nicholson 1911,
Weir 1901). Persian originals for Attar come from Ganjoor (PD mūla).
Arabic originals for Know Yourself are kept verbatim. Hujwīrī Original is
ALA-LC romanization of the Persian/Arabic technical core already in Nicholson
(not invented Persian script).

  .venv/bin/python scripts/ingest_sufi_wave.py --dry
  .venv/bin/python scripts/ingest_sufi_wave.py --work attar --write
  .venv/bin/python scripts/ingest_sufi_wave.py --all --write
"""
from __future__ import annotations

import argparse, asyncio, glob, json, os, re, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from app.llm import smart_chat  # noqa: E402

TERRA = "openai/gpt-5.6-terra"
CANON = os.path.join(ROOT, "data/canonical")
PD = os.path.join(ROOT, "data/raw_texts/pd")
MASANI = os.path.join(PD, "persian/attar_conference_masani_1924.txt")
HUJWIRI = os.path.join(PD, "persian/hujwiri_kashf_al_mahjub_nicholson_1911.txt")
WEIR = os.path.join(PD, "arabic/ibn_arabi_balyani_weir_jras_1901.txt")

# Ten heroes each (mandala + Listen bake).
ATTAR_HEROES = {1, 2, 3, 8, 14, 17, 20, 22, 27, 28}
HUJWIRI_HEROES = {1, 4, 6, 7, 11, 13, 18, 19, 21, 25}
KY_HEROES = {
    "ky_001", "ky_002", "ky_004", "ky_005", "ky_008",
    "kys_p001", "kys_p007", "kys_p013", "kys_p026", "kys_p034",
}


def _lenient_json(r: str):
    s = re.sub(r"^```(?:json)?|```$", "", (r or "").strip(), flags=re.M).strip()
    m = re.search(r"\{.*\}", s, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None


def squash(s: str) -> str:
    s = (s or "").replace("¬", "").replace("\u00ad", "")
    s = re.sub(r"(\w)-\s+(\w)", r"\1\2", s)
    s = re.sub(r"\b\d+\s+CONFERENCE OF BIRDS\b", " ", s, flags=re.I)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def slice_at(text: str, start: str, stop: str | None, maxlen: int = 880, after: str = "") -> str:
    start, stop = squash(start), (squash(stop) if stop else None)
    base = text.find(squash(after)) if after else 0
    if base < 0:
        base = 0
    i = text.find(start, base)
    if i < 0:
        key = start[:48]
        i = text.find(key, base)
    if i < 0:
        return ""
    j = text.find(stop, i + max(8, len(start) // 2)) if stop else -1
    chunk = text[i : (j if j > i else i + maxlen + 80)]
    if len(chunk) > maxlen:
        chunk = chunk[:maxlen]
        k = max(chunk.rfind(". "), chunk.rfind(".”"), chunk.rfind(".'"))
        if k > maxlen // 2:
            chunk = chunk[: k + 1]
    return squash(chunk)


# Ganjoor PD mūla (https://ganjoor.net/attar/manteghotteyr/). Couple openings only.
PERSIAN = {
    15: """چون فرو آیی به وادی طلب
پیشت آید هر زمانی صدتعب
صد بلا در هر نفس اینجا بود
طوطی گردون، مگس اینجا بود
جد و جهد اینجات باید سال‌ها
زآن که اینجا قلب گردد حال‌ها
ملک اینجا بایدت انداختن
ملک اینجا بایدت در باختن
چون نماند هیچ معلومت به دست
دل بباید پاک کرد از هرچه هست""",
    17: """بعد ازین وادی عشق آید پدید
غرق آتش شد کسی کانجا رسید
کس درین وادی به جز آتش مباد
وانک آتش نیست عیشش خوش مباد
عاشق آن باشد که چون آتش بود
گرم رو سوزنده و سرکش بود
عاقبت اندیش نبود یک زمان
در کشد خوش خوش بر آتش صد جهان
نیک و بد در راه او یکسان بود
خود چو عشق آمد نه این نه آن بود""",
    18: """بعد از آن بنمایدت پیش نظر
معرفت را وادیی بی پا و سر""",
    19: """بعد ازین وادی استغنا بود
نه درو دعوی و نه معنی بود
می‌جهد از بی‌نیازی صرصری
می‌زند بر هم به یک دم کشوری
هفت دریا یک شمر اینجا بود
هفت اخگر یک شرر اینجا بود""",
    21: """بعد ازین وادی حیرت آیدت
کار دایم درد و حسرت آیدت
هر نفس اینجا چو تیغی باشدت
هر دمی اینجا دریغی باشدت
مرد حیران چون رسد این جایگاه
در تحیر مانده و گم کرده راه
عاشقم اما ندانم بر کیم
نه مسلمانم نه کافر، پس چیم""",
    22: """بعد ازین وادی فقرست و فنا
کی بود اینجا سخن گفتن روا
عین وادی فراموشی بود
لنگی و کری و بیهوشی بود
صد هزاران سایهٔ جاوید تو
گم شده بینی ز یک خورشید تو
گم شدن اول قدم، زین پس چه بود
لاجرم دیگر قدم را کس نبود""",
    23: """یک شبی پروانگان جمع آمدند
در طلب آن شمع را می‌جستند""",
    26: """زین سخن مرغان وادی سر به سر
سرنگون گشتند در خون جگر
عالمی پر مرغ می‌بردند راه
بیش نرسیدند سی آن جایگاه
سی تن بی‌بال و پر، رنجور و سست
دل شکسته، جان شده، تن نادرست""",
    27: """زین سخن مرغان وادی سر به سر
سرنگون گشتند در خون جگر
عالمی پر مرغ می‌بردند راه
بیش نرسیدند سی آن جایگاه
سی تن بی‌بال و پر، رنجور و سست
دل شکسته، جان شده، تن نادرست""",
    28: """چون نگه کردند آن سی مرغ زود
بی‌شک این سی مرغ آن سیمرغ بود
بود خود سیمرغ سی مرغ مدام
سیمرغ در آینه پیدا شد تمام""",
}

ATTAR = [
    dict(n=1, section="Hoopoe summons the birds", start="We have a king, my friends", stop="On hearing this account of the Simurg"),
    dict(n=2, section="The feather in China", start="During the early days of Creation He passed", stop="On hearing this account of the Simurg"),
    dict(n=3, section="The Nightingale and the Rose", start="The first to retrace its steps was the Nightingale", stop="After the Nightingale had been thus admonished"),
    dict(n=4, section="The Parrot's excuse", start="Parrot came forward", stop="The Peacock urged"),
    dict(n=5, section="The Peacock and the Duck", start="The Peacock urged that he was", stop="Falcon could not brook"),
    dict(n=6, section="Falcon, heron, owl", start="Falcon could not brook", stop="The Hoopoe brushed aside"),
    dict(n=7, section="You are the Simurgh's shadow", start="removed the veil from His face", stop="If you, my friends"),
    dict(n=8, section="Love above faith and heresy", start="He who has become a lover should never think of his life", stop="Shaykh San"),
    dict(n=9, section="Shaykh Sanʿān", start="Shaykh San'an was a saint", stop="When the birds heard this love-story"),
    dict(n=10, section="The Hoopoe crowned", start="the honour fell to the lot of the worthiest", stop="The march now commenced"),
    dict(n=11, section="A glance from Solomon", start="I had a glance from Solomon", stop="Know thou"),
    dict(n=12, section="The aperture of death", start="Izracl, the Ang", stop="A love-sick bird then came forward"),
    dict(n=13, section="Consume whatsoever thou hast", start="The only provisions for the journey in the Path of Truth", stop='Indeed", continued the Hoopoe'),
    dict(n=14, section="The seven valleys named", start="These are the seven valleys:", stop="THROUGH THE SEVEN VALLEYS"),
    dict(n=15, section="Valley of the Quest", start="THE VALLEY OF THE QUEST", stop="MAJNUN"),
    dict(n=16, section="Majnūn sifts the dust", start="One day Majnun was sifting earth", stop="THE VALLEY OF LOVE"),
    dict(n=17, section="Valley of Love", start="THE VALLEY OF LOVE", stop="THE VALLEY OF KNOWLEDGE"),
    dict(n=18, section="Valley of Knowledge", start="THE VALLEY OF KNOWLEDGE", stop="THE VALLEY OF DETACHMENT"),
    dict(n=19, section="Valley of Detachment", start="THE VALLEY OF DETACHMENT", stop="THE VALLEY OF UNITY"),
    dict(n=20, section="Valley of Unity", start="THE VALLEY OF UNITY", stop="THE VALLEY OF BEWILDERMENT"),
    dict(n=21, section="Valley of Bewilderment", start="THE VALLEY OF BEWILDERMENT", stop="THE VALLEY OF POVERTY"),
    dict(n=22, section="Valley of Poverty and Annihilation", start="THE VALLEY OF POVERTY AND ANNIHILATION", stop="RECEPTION AT THE ROYAL COURT"),
    dict(n=23, section="The fly in the honey", start="THE FLY AND THE BEE-HIVE", stop="THE VALLEY OF UNITY"),
    dict(n=24, section="Ask nothing of the Simurgh", start="What shall we ask of the Simurg when we meet", stop="What shall we proffer"),
    dict(n=25, section="Treasure already in the seat", start="You have become totally drowned in egotism", stop="Be cheerful"),
    dict(n=26, section="Millions set out", start="the burden of their mission was too heavy", stop="the reflection of their faces"),
    dict(n=27, section="Thirty birds remain", start="Thirty birds—only thirty out of millions", stop="the reflection of their faces"),
    dict(n=28, section="Thirty birds, one Simurgh", start="The Sun of my Majesty is a mirror", stop="If you have succeeded in crossing"),
]

# n=2 start is inside n=1; extract n=2 from a later unique phrase if first fails.
ATTAR[1]["start"] = "A feather from His wing fell on Chinese soil"

HUJWIRI_LOCS = [
    dict(n=1, section="I. Divine and human knowledge", start="Knowledge is of two kinds: Divine and Human", stop="The Knowledge of the Truth"),
    dict(n=2, section="I. Three pillars of Truth", start="The Knowledge of the Truth (_Ḥaqíqat_) has three pillars", stop="The Knowledge of the Law (_Sharí`at_) also has three pillars"),
    dict(n=3, section="I. Life of the heart", start="Knowledge is the life of the heart, which delivers it from the death of", stop=None),
    dict(n=4, section="II. Form and essence of poverty", start="Now, Poverty has a form (_rasm_) and an essence (_ḥaqíqat_)", stop=None),
    dict(n=5, section="II. Poverty is glorious", start='The Prophet said: "Poverty is glorious to those who are worthy of it."', stop=None),
    dict(n=6, section="III. The science of Sufiism is obsolete", start="Know that in this our time the science of Ṣúfiism is obsolete", stop=None),
    dict(n=7, section="III. The true Sufi", start="The true Ṣúfí is he that leaves", stop=None),
    dict(n=8, section="III. Language that is his state", start="The Ṣúfí is he whose language, when he speaks, is the reality of his", stop=None),
    dict(n=9, section="III. Nothing in his possession", start="The Ṣúfí is he that has nothing in his possession nor is", stop=None),
    dict(n=10, section="III. Sees nothing except God", start="Ṣúfí is he that sees nothing except God in the two worlds", stop=None),
    dict(n=11, section="XV. Gnosis of God", start="Gnosis (_`ilm-i ma`rifat_), whereby He is known to all His prophets", stop=None),
    dict(n=12, section="XV. Gnosis as gift", start="Gnosis consists in knowing that the motion and rest of mankind depend", stop=None),
    dict(n=13, section="XVI. Three kinds of unification", start="Unification is of three kinds: (1) God's unification of God", stop=None),
    dict(n=14, section="XVI. Junayd on unification", start='Junayd said: "Unification is this, that one should be a figure', stop=None),
    dict(n=15, section="XVII. Faith", start="Etymologically, faith (_ímán_) means verification", stop=None),
    dict(n=16, section="IV. The patched frock", start="Know that the wearing of a _muraqqa`a_ (patched frock) is the badge of", stop=None),
    dict(n=17, section="VI. Blame", start="Now blame (_malámat_) is of three kinds", stop=None),
    dict(n=18, section="XXIV. Stations and states", start='escaped from the captivity of "stations" (_maqámát_)', stop=None),
    dict(n=19, section="XXIV. Fanā and baqā", start="annihilation (_faná_)", stop=None, after="CHAPTER XXIV"),
    dict(n=20, section="XXV. Audition", start="THE UNCOVERING OF THE ELEVENTH VEIL: CONCERNING AUDITION", stop=None),
    dict(n=21, section="Love of God", start="love of God", stop=None, after="CHAPTER XIV"),
    dict(n=22, section="Trust", start="tawakkul", stop=None, after="CHAPTER II"),
    dict(n=23, section="Repentance", start="Repentance is", stop=None, after="CHAPTER XVIII"),
    dict(n=24, section="Introduction: unveiling", start="unveiling (_kashf_) is destruction of the veiled object", stop=None),
    dict(n=25, section="Two veils", start="There are two veils: one is the", stop=None),
    dict(n=26, section="XVIII. Purification", start="THE UNCOVERING OF THE FOURTH VEIL", stop=None),
    dict(n=27, section="Eight qualities of Sufiism", start="Ṣúfiism is founded on eight qualities exemplified in eight Apostles", stop=None),
    dict(n=28, section="Sufiism as imitation of God", start="Ṣúfiism is an imitation of", stop=None),
]


AUTH = """You author the study apparatus for ONE passage of {ctx}.
You are given a VERBATIM public-domain English crib (OCR may be dirty).
Modernize lightly: fix hyphenation/OCR, lift archaisms (thou/ye/verily), keep sense.
Do NOT invent lines that are not in the crib. Do NOT follow Davis/Darbandi, Twinch, or any living translator.
Return ONLY JSON:
{{"title":"<thematic English title, no numbers, no 'Chapter'>",
  "translation":"<modernized PD English, 1-3 short paragraphs, readable aloud>",
  "romanization":"<ALA-LC romanization of the source-language core: key Persian/Arabic terms and the gist of the first 2-4 sentences. Do not fake a full poem.>",
  "commentary":"<900-1400 chars. Open with a philosophical claim. Name the contested move. Situate in the Sufi source. No 'In this passage...'>",
  "key_terms":[{{"term":"<Persian or Arabic term in script if you know it, else transliteration>","definition":"<etymology -> this-passage meaning -> what the default gloss misses>"}}],
  "resonances":[{{"citation":"<Author, Text, passage>","resonance":"<structural homology>","divergence":"<where it breaks and why that matters>"}}],
  "practice":"<second person, one executable act today, derived from THIS passage, not 'read three times'>"}}
Need 2-4 key_terms and 2-3 resonances."""


KY_AUTH = """You enrich ONE unit of Balyānī's Risālat al-aḥadiyya (long ascribed to Ibn ʿArabī), "Know Yourself".
English must be a light modernization of T. H. Weir's 1901 JRAS public-domain translation of the MATCHING passage.
Never follow Cecilia Twinch or any copyrighted English. Keep the Arabic original EXACTLY as given (do not rewrite or vocalize it).
If Arabic is empty, leave original_arabic as "".
Return ONLY JSON:
{{"title":"<thematic claim, not Pearl #N>",
  "translation":"<Weir modernized, present tense where the claim is general>",
  "commentary":"<900-1400 chars, claim-led, waḥdat al-wujūd / self-knowledge as knowledge of the Lord, the contested move>",
  "key_terms":[{{"term":"...","definition":"etymology -> this passage -> missed by the default gloss"}}],
  "resonances":[{{"citation":"...","resonance":"...","divergence":"..."}}],
  "practice":"<second person, one act today>"}}
Need 2-4 key_terms and 2-3 resonances. Practice must not be 'read three times'."""


def layers(original, translation, ap):
    kt = ap.get("key_terms") or []
    rz = ap.get("resonances") or []
    out = []
    if original:
        out.append({"kind": "original", "label": "Original", "body": original})
    out.append({"kind": "translation", "label": "Pratibha Translation", "body": translation})
    if ap.get("commentary"):
        out.append({"kind": "commentary", "label": "Pratibha Commentary", "body": ap["commentary"].strip()})
    if kt:
        items = []
        for t in kt[:4]:
            if isinstance(t, dict) and t.get("term"):
                items.append({"term": str(t["term"]).strip(), "definition": str(t.get("definition") or t.get("gloss") or "").strip()})
        if items:
            out.append({"kind": "key_terms", "label": "Key Terms", "items": items})
    if rz:
        items = []
        for r in rz[:3]:
            if not isinstance(r, dict):
                continue
            cit = r.get("citation") or r.get("ref") or ""
            if cit:
                items.append({
                    "citation": str(cit).strip(),
                    "resonance": str(r.get("resonance") or r.get("parallel") or "").strip(),
                    "divergence": str(r.get("divergence") or "").strip(),
                })
        if items:
            out.append({"kind": "resonances", "label": "Cross-Tradition Resonances", "items": items})
    if ap.get("practice"):
        out.append({"kind": "practice", "label": "Practice (Abhyasa)", "body": str(ap["practice"]).strip()})
    return out


def dump_unit(path, unit):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(unit, fh, allow_unicode=True, sort_keys=False, width=100)


async def author(system, user, sem):
    async with sem:
        for attempt in range(4):
            try:
                r = await smart_chat(
                    [{"role": "system", "content": system}, {"role": "user", "content": user}],
                    primary_model=TERRA, temperature=0.35, max_tokens=2200,
                )
                j = _lenient_json(r)
                if j and (j.get("commentary") or j.get("translation")):
                    return j
            except Exception as e:
                if "402" in str(e):
                    return {"_nocredits": True}
                await asyncio.sleep(2 * (attempt + 1))
    return None


def harvest_attar():
    raw = open(MASANI, encoding="utf-8", errors="replace").read()
    text = squash(raw)
    out = []
    for spec in ATTAR:
        body = slice_at(text, spec["start"], spec.get("stop"), 900)
        out.append({**spec, "crib": body, "persian": PERSIAN.get(spec["n"], "").strip()})
    return out


def harvest_hujwiri():
    raw = open(HUJWIRI, encoding="utf-8", errors="replace").read()
    text = squash(raw)
    out = []
    for spec in HUJWIRI_LOCS:
        body = slice_at(text, spec["start"], spec.get("stop"), 820, spec.get("after") or "")
        out.append({**spec, "crib": body})
    return out


def write_attar_unit(spec, ap):
    n = spec["n"]
    slug = "conference_of_the_birds"
    uid = f"{slug}.cot_{n:02d}"
    tr = (ap.get("translation") or spec["crib"]).strip()
    orig = spec.get("persian") or ""
    rom = (ap.get("romanization") or "").strip()
    if not orig:
        orig = rom
    layers_ = layers(orig, tr, ap)
    unit = {
        "source_id": f"COT_{n:02d}",
        "category": "root_text",
        "work_id": slug,
        "work_title": "Conference of the Birds",
        "unit_id": uid,
        "unit_label": spec["section"],
        "title": (ap.get("title") or spec["section"]).strip(),
        "unit_type": "teaching_passage",
        "commentary": (ap.get("commentary") or "").strip(),
        "themes": ["quest", "love", "annihilation", "simurgh"],
        "tags": [slug, "sufi", "attar", "persian"],
        "quality_score": 0,
        "editorial_score": 0,
        "editorial_maturity": "strong_draft",
        "translation_provenance": (
            "English is a Pratibha adaptation (2026) of R. P. Masani, *The Conference of the Birds* "
            "(Oxford / Humphrey Milford, 1924 — public domain abridgment of ʿAṭṭār's Manṭiq al-ṭayr). "
            "Persian mūla from Ganjoor where cited. Does not follow Davis & Darbandi, Nott, or Avery."
        ),
        "pratibha_layers": layers_,
        "provenance": {
            "collection": "Conference of the Birds",
            "section": spec["section"],
            "cultural_context": (
                "Farīd al-Dīn ʿAṭṭār (d. c. 1221), Manṭiq al-ṭayr: the birds' quest for the Simurgh "
                "through seven valleys. Masani 1924 is an English prose abridgment."
            ),
            "original_source": "Persian, ʿAṭṭār, Manṭiq al-ṭayr (Ganjoor e-text of the PD poem)",
            "english_source": "R. P. Masani 1924, pd_adapted",
        },
        "translation": tr,
        "practice": (ap.get("practice") or "").strip(),
        "abhyasa": (ap.get("practice") or "").strip(),
        "original": orig,
        "sanskrit_devanagari": orig,
        "sanskrit_iast": rom or "Persian (ALA-LC in Key Terms).",
    }
    if n in ATTAR_HEROES:
        unit["tts_key"] = True
    dump_unit(os.path.join(CANON, slug, uid.replace(".", "_") + ".yml"), unit)
    return uid


def write_hujwiri_unit(spec, ap):
    n = spec["n"]
    slug = "kashf_al_mahjub"
    uid = f"{slug}.kam_{n:02d}"
    tr = (ap.get("translation") or spec["crib"]).strip()
    orig = (ap.get("romanization") or "").strip()
    layers_ = layers(orig, tr, ap)
    unit = {
        "source_id": f"KAM_{n:02d}",
        "category": "root_text",
        "work_id": slug,
        "work_title": "Kashf al-Maḥjūb",
        "unit_id": uid,
        "unit_label": spec["section"],
        "title": (ap.get("title") or spec["section"]).strip(),
        "unit_type": "teaching_passage",
        "commentary": (ap.get("commentary") or "").strip(),
        "themes": ["unveiling", "gnosis", "poverty", "tawhid"],
        "tags": [slug, "sufi", "hujwiri", "persian"],
        "quality_score": 0,
        "editorial_score": 0,
        "editorial_maturity": "strong_draft",
        "translation_provenance": (
            "English is a Pratibha adaptation (2026) of Reynold A. Nicholson, *The Kashf al-Maḥjúb: "
            "The Oldest Persian Treatise on Sufiism* (Gibb Memorial XVII, 1911 — public domain). "
            "Gutenberg #64786. Original is romanized from Nicholson's Persian/Arabic technical core."
        ),
        "pratibha_layers": layers_,
        "provenance": {
            "collection": "Kashf al-Maḥjūb",
            "section": spec["section"],
            "cultural_context": (
                "ʿAlī b. ʿUthmān al-Jullābī al-Hujwīrī (d. c. 1072–77), Kashf al-Maḥjūb, "
                "the earliest surviving Persian Sufi handbook: unveiling, stations, gnosis."
            ),
            "original_source": "Persian (with Arabic citations), Kashf al-Maḥjūb",
            "english_source": "Nicholson 1911, pd_adapted",
        },
        "translation": tr,
        "practice": (ap.get("practice") or "").strip(),
        "abhyasa": (ap.get("practice") or "").strip(),
        "original": orig,
        "sanskrit_devanagari": orig,
        "sanskrit_iast": orig or "Persian/Arabic romanized (ALA-LC).",
    }
    if n in HUJWIRI_HEROES:
        unit["tts_key"] = True
    dump_unit(os.path.join(CANON, slug, uid.replace(".", "_") + ".yml"), unit)
    return uid


async def run_attar(write: bool, sem):
    rows = harvest_attar()
    missing = [r["n"] for r in rows if len(r["crib"]) < 120]
    print(f"[attar] {len(rows)} locators; short/missing: {missing or 'none'}")
    for r in rows:
        print(f"  cot_{r['n']:02d} {len(r['crib']):4d}c  {r['section']}")
    if not write:
        return
    slug = "conference_of_the_birds"
    pending = []
    for r in rows:
        path = os.path.join(CANON, slug, f"{slug}_cot_{r['n']:02d}.yml")
        if os.path.exists(path):
            print(f"  skip cot_{r['n']:02d} (exists)")
        else:
            pending.append(r)
    rows = pending
    if not rows:
        print("[attar] nothing to author")
        return
    ctx = "Farīd al-Dīn ʿAṭṭār, Manṭiq al-ṭayr (Conference of the Birds): hoopoe, excuses, seven valleys, Simurgh"
    tasks = [
        author(AUTH.format(ctx=ctx), f"MASANI 1924 CRIB (verbatim, public domain):\n{r['crib']}\n\nPERSIAN MŪLA (if any):\n{r['persian']}\n\nReturn JSON.", sem)
        for r in rows
    ]
    apparats = await asyncio.gather(*tasks)
    n = 0
    for r, ap in zip(rows, apparats):
        if not ap or ap.get("_nocredits"):
            print(f"  FAIL cot_{r['n']:02d} {('credits' if ap else 'no json')}")
            if ap and ap.get("_nocredits"):
                break
            continue
        uid = write_attar_unit(r, ap)
        n += 1
        print(f"  wrote {uid}  {ap.get('title','')[:50]}")
    print(f"[attar] wrote {n}")


async def run_hujwiri(write: bool, sem):
    rows = harvest_hujwiri()
    missing = [r["n"] for r in rows if len(r["crib"]) < 80]
    print(f"[hujwiri] {len(rows)} locators; short/missing: {missing or 'none'}")
    for r in rows:
        print(f"  kam_{r['n']:02d} {len(r['crib']):4d}c  {r['section']}")
    if not write:
        return
    slug = "kashf_al_mahjub"
    pending = []
    for r in rows:
        path = os.path.join(CANON, slug, f"{slug}_kam_{r['n']:02d}.yml")
        if os.path.exists(path):
            print(f"  skip kam_{r['n']:02d} (exists)")
        else:
            pending.append(r)
    rows = pending
    if not rows:
        print("[hujwiri] nothing to author")
        return
    ctx = "Hujwīrī, Kashf al-Maḥjūb (Unveiling of the Veiled), earliest Persian Sufi handbook"
    tasks = [
        author(AUTH.format(ctx=ctx), f"NICHOLSON 1911 CRIB (verbatim, public domain):\n{r['crib']}\n\nReturn JSON.", sem)
        for r in rows
    ]
    apparats = await asyncio.gather(*tasks)
    n = 0
    for r, ap in zip(rows, apparats):
        if not ap or ap.get("_nocredits"):
            print(f"  FAIL kam_{r['n']:02d}")
            if ap and ap.get("_nocredits"):
                break
            continue
        uid = write_hujwiri_unit(r, ap)
        n += 1
        print(f"  wrote {uid}  {ap.get('title','')[:50]}")
    print(f"[hujwiri] wrote {n}")


def ky_files():
    return sorted(glob.glob(os.path.join(CANON, "know_yourself_ibn_arabi_balyani", "*.yml")))


async def run_ky(write: bool, sem, limit: int = 0):
    weir = open(WEIR, encoding="utf-8", errors="replace").read()
    files = ky_files()
    if limit:
        files = files[:limit]
    print(f"[ky] {len(files)} units; Weir {len(weir.split())} words")
    if not write:
        for f in files:
            d = yaml.safe_load(open(f, encoding="utf-8")) or {}
            print(f"  {d.get('unit_id')}  title={d.get('title')!r}  comm={len(str(d.get('commentary') or ''))}")
        return
    weir_slice = weir[:14000]

    async def one(path):
        d = yaml.safe_load(open(path, encoding="utf-8")) or {}
        ar = str(d.get("sanskrit_devanagari") or d.get("original") or "").strip()
        loc = str(d.get("translation") or d.get("translation_literal") or d.get("source_excerpt") or "")[:700]
        user = (
            f"WEIR 1901 (public domain, use this as the English source):\n{weir_slice}\n\n"
            f"ARABIC ORIGINAL (keep verbatim; do not rewrite):\n{ar or '[none in file]'}\n\n"
            f"CURRENT TITLE: {d.get('title')}\n"
            f"CURRENT ENGLISH (locator only; may be Twinch-tainted — do not copy):\n{loc}\n\n"
            "Return JSON for the matching Weir passage."
        )
        ap = await author(KY_AUTH, user, sem)
        return path, d, ap

    results = await asyncio.gather(*(one(f) for f in files))
    n = 0
    for path, d, ap in results:
        if not ap or ap.get("_nocredits"):
            print(f"  FAIL {os.path.basename(path)}")
            if ap and ap.get("_nocredits"):
                break
            continue
        tr = (ap.get("translation") or d.get("translation") or "").strip()
        ar = str(d.get("sanskrit_devanagari") or "").strip()
        title = (ap.get("title") or d.get("title") or "").strip()
        prac = (ap.get("practice") or "").strip()
        comm = (ap.get("commentary") or "").strip()
        d["title"] = title
        d["unit_label"] = title
        d["translation"] = d["translation_literal"] = tr
        d["commentary"] = comm
        d["practice"] = d["abhyasa"] = prac
        d["editorial_maturity"] = "strong_draft"
        d["translation_provenance"] = (
            "Based on the public-domain English translation by T. H. Weir (JRAS, 1901), "
            "lightly modernized. Study rendering. Does not follow Twinch."
        )
        d["pratibha_layers"] = layers(ar, tr, ap)
        if ar:
            d["original"] = ar
            d["sanskrit_devanagari"] = ar
        short = (d.get("unit_id") or "").split(".")[-1]
        if short in KY_HEROES:
            d["tts_key"] = True
        dump_unit(path, d)
        n += 1
        print(f"  wrote {d.get('unit_id')}  {title[:50]}")
    print(f"[ky] wrote {n}")


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", choices=["attar", "hujwiri", "ky", "all"], default="all")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--concurrency", type=int, default=4)
    args = ap.parse_args()
    write = args.write and not args.dry
    sem = asyncio.Semaphore(args.concurrency)
    works = ["attar", "hujwiri", "ky"] if args.work == "all" else [args.work]
    if "attar" in works:
        await run_attar(write, sem)
    if "hujwiri" in works:
        await run_hujwiri(write, sem)
    if "ky" in works:
        await run_ky(write, sem, args.limit)


if __name__ == "__main__":
    asyncio.run(main())
