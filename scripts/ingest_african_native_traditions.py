#!/usr/bin/env python3
"""Ingest three public-domain wisdom collections into the Pratibha canonical corpus:

  1. Charles A. Eastman (Ohíyeʼsa), The Soul of the Indian (1911) — Dakota author.
  2. Zitkála-Šá (Gertrude Bonnin), Old Indian Legends (1901) — Yankton Dakota author.
  3. Yoruba proverbs (òwe) as recorded by A.B. Ellis (1894).

ASTEYA: text is taken verbatim from the downloaded public-domain sources under
data/raw_texts/pd/ — never model-generated. Units are marked `strong_draft`
study renderings pending review by tradition-bearers, with explicit provenance,
prominent author attribution, and a cultural-context note. These are living,
often oral traditions; legal public domain is not cultural permission.
"""
import os, re, textwrap
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw_texts", "pd")
CANON = os.path.join(ROOT, "data", "canonical")


def write_unit(slug, unit):
    d = os.path.join(CANON, slug)
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, f"{unit['unit_id'].replace('.', '_')}.yml")
    with open(path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(unit, fh, allow_unicode=True, sort_keys=False, width=100)


def base_unit(slug, work_title, n, title, unit_type, text_layer_kind, text, provenance_str, note, themes):
    uid = f"{slug}.{slug}_{n:03d}"
    layers = [{"kind": text_layer_kind, "label": "Original" if text_layer_kind == "original" else "Translation", "body": text}]
    unit = {
        "source_id": f"{slug}_{n:03d}".upper(),
        "category": "root_text",
        "work_id": slug,
        "work_title": work_title,
        "unit_id": uid,
        "unit_label": title,
        "title": title,
        "unit_type": unit_type,
        "commentary": "",
        "themes": themes,
        "tags": [slug] + themes,
        "quality_score": 0,
        "editorial_score": 0,
        "editorial_maturity": "strong_draft",
        "translation_provenance": provenance_str,
        "pratibha_layers": layers,
        "provenance": {
            "collection": work_title,
            "cultural_context": note,
        },
    }
    # Exactly one text layer per unit — original (author's own words) OR a
    # recorded translation — so the reader never shows the same English twice.
    unit[text_layer_kind] = text
    return unit


# ---------------------------------------------------------------------------
def clean(s):
    s = re.sub(r"\s+", " ", s).strip()
    return s


def title_from(text, maxlen=54):
    """Derive a short title from the first sentence/clause of a passage."""
    first = re.split(r"(?<=[.!?;:])\s", text.strip())[0]
    first = re.sub(r"^[\"“'‘]", "", first).strip()
    if len(first) > maxlen:
        cut = first[:maxlen].rsplit(" ", 1)[0]
        return cut.rstrip(",;:—- ") + "…"
    return first.rstrip(".")


# ---- 1. Eastman -----------------------------------------------------------
def ingest_eastman():
    path = os.path.join(RAW, "native_american", "eastman_soul_of_the_indian_gutenberg_340.txt")
    txt = open(path, encoding="utf-8").read()
    # Body between the title line and the Gutenberg license.
    start = txt.index("I. THE GREAT MYSTERY")
    end = txt.index("THE FULL PROJECT GUTENBERG")
    body = txt[start:end]
    chapters = re.split(r"\n(?=[IVX]+\. [A-Z])", body)
    prov = ("Original text by Charles A. Eastman (Ohíyeʼsa), The Soul of the Indian "
            "(1911, public domain).")
    note = ("Charles Eastman (Ohíyeʼsa) was a Santee Dakota writer and physician; these are "
            "his own words, published to interpret Native spirituality across cultures. A living "
            "tradition — offered here as a study reading, with respect to Dakota descendants.")
    n = 0
    for chap in chapters:
        lines = chap.strip().split("\n", 1)
        chap_title = clean(lines[0]).title() if lines else ""
        rest = lines[1] if len(lines) > 1 else ""
        paras = [clean(p) for p in re.split(r"\n\s*\n", rest) if clean(p)]
        picked = 0
        for p in paras:
            if not (260 <= len(p) <= 1200):
                continue
            if p.isupper() or p.startswith("[") or "Gutenberg" in p:
                continue
            picked += 1
            if picked > 5:
                break
            n += 1
            themes = ["the great mystery", "silence", "reverence"]
            unit = base_unit("eastman_soul_of_the_indian", "The Soul of the Indian", n,
                             title_from(p), "reflection", "original", p, prov, note, themes)
            unit["provenance"]["section"] = chap_title
            write_unit("eastman_soul_of_the_indian", unit)
    return n


# ---- 2. Zitkála-Šá --------------------------------------------------------
def ingest_zitkala():
    path = os.path.join(RAW, "native_american", "zitkala_sa_old_indian_legends_gutenberg_338.txt")
    txt = open(path, encoding="utf-8").read()
    titles = ["IKTOMI AND THE DUCKS", "IKTOMI'S BLANKET", "IKTOMI AND THE MUSKRAT",
              "IKTOMI AND THE COYOTE", "IKTOMI AND THE FAWN", "THE BADGER AND THE BEAR",
              "THE TREE-BOUND", "SHOOTING OF THE RED EAGLE", "IKTOMI AND THE TURTLE",
              "DANCE IN A BUFFALO SKULL", "THE TOAD AND THE BOY", "THE WARLIKE SEVEN"]
    prov = ("Original text by Zitkála-Šá (Gertrude Simmons Bonnin), Old Indian Legends "
            "(1901, public domain).")
    note = ("Zitkála-Šá, a Yankton Dakota writer, transcribed these Sioux oral legends she was "
            "told as a child, to keep them for the next generation. Trickster tales (Iktomi) and "
            "teaching-stories — a living oral tradition, offered as a study reading with respect "
            "to Dakota descendants.")
    n = 0
    for i, t in enumerate(titles):
        try:
            s = txt.index("\n" + t + "\n")
        except ValueError:
            continue
        nxt = titles[i + 1] if i + 1 < len(titles) else "PLEASE READ THIS BEFORE"
        try:
            e = txt.index("\n" + nxt + "\n", s + 1)
        except ValueError:
            e = txt.index("PLEASE READ THIS BEFORE", s + 1)
        story = clean(txt[s + len(t) + 2:e])
        if len(story) < 120:
            continue
        n += 1
        title = t.title().replace("Iktomi", "Iktomi")
        unit = base_unit("zitkala_sa_old_indian_legends", "Old Indian Legends", n,
                         title, "legend", "original", story, prov, note,
                         ["trickster", "teaching story", "oral tradition"])
        write_unit("zitkala_sa_old_indian_legends", unit)
    return n


# ---- 3. Yoruba proverbs (Ellis) ------------------------------------------
def ingest_yoruba():
    path = os.path.join(RAW, "yoruba", "ellis_yoruba_speaking_peoples_1894_djvu.txt")
    txt = open(path, encoding="utf-8").read()
    start = txt.index("CHAPTER XIII.", txt.index("FOLK-LORE TALES"))  # the real chapter, not TOC
    seg = txt[start:start + 30000]
    # Numbered proverbs: "N. text ...". Join wrapped lines until the next number.
    items = re.findall(r"\n(\d{1,3})\.\s+(.+?)(?=\n\d{1,3}\.\s|\nCHAPTER)", seg, re.S)
    prov = ("English follows A.B. Ellis, The Yoruba-Speaking Peoples of the Slave Coast of West "
            "Africa (1894, public domain). Colonial-era ethnography recorded by an outside "
            "observer; the Yoruba original (òwe) is not preserved in the source. Study rendering "
            "pending review by tradition-bearers.")
    note = ("Yoruba proverbs (òwe) — 'the horse of conversation.' Recorded in English by the "
            "British colonial official A.B. Ellis (1894); his framing is that of an outside "
            "observer of his era and may distort. The Yoruba original is not preserved here. "
            "Offered as a study reading pending review by Yoruba tradition-bearers.")
    n = 0
    seen = set()
    for num, raw in items:
        p = clean(raw)
        # Drop OCR page headers and Ellis's editorial English-equivalent notes.
        p = re.sub(r"PROVERBS?\.?\s*\d*", "", p).strip()
        if p.startswith("(") or len(p) < 18 or len(p) > 240:
            continue
        if p.lower() in seen:
            continue
        seen.add(p.lower())
        n += 1
        if n > 45:
            break
        unit = base_unit("yoruba_proverbs", "Yoruba Proverbs (Òwe)", n,
                         title_from(p, 48), "proverb", "translation", p, prov, note,
                         ["wisdom", "proverb", "yoruba"])
        write_unit("yoruba_proverbs", unit)
    return n


if __name__ == "__main__":
    print("eastman :", ingest_eastman(), "units")
    print("zitkala :", ingest_zitkala(), "units")
    print("yoruba  :", ingest_yoruba(), "units")
