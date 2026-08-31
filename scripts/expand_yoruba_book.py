#!/usr/bin/env python3
"""Expand the Yoruba Proverbs (Òwe) collection into a proper book: re-parse Ellis
(1894), joining wrapped lines into complete proverbs and gating hard on OCR
cleanliness, so the book reads well. Same asteya framing as the first ingest —
verbatim PD text, colonial source flagged, Yoruba original not preserved, study
rendering pending review by tradition-bearers.
"""
import glob, os, re
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data/raw_texts/pd/yoruba/ellis_yoruba_speaking_peoples_1894_djvu.txt")
OUT = os.path.join(ROOT, "data/canonical/yoruba_proverbs")
CAP = 130

PROV = ("English follows A.B. Ellis, The Yoruba-Speaking Peoples of the Slave Coast of West Africa "
        "(1894, public domain). Colonial-era ethnography recorded by an outside observer; the Yoruba "
        "original (òwe) is not preserved in the source. Study rendering pending review by tradition-bearers.")
NOTE = ("Yoruba proverbs (òwe) — 'the horse of conversation.' Recorded in English by the British colonial "
        "official A.B. Ellis (1894); his framing is that of an outside observer of his era and may distort. "
        "The Yoruba original is not preserved here. Offered as a study reading pending review by Yoruba "
        "tradition-bearers.")


def clean(s):
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"PROVERBS?\.?\s*\d*", "", s).strip()
    return s


def garbled(s):
    # Reject OCR noise so the book reads cleanly.
    if re.search(r"\b[A-Z]\d|\bAV|\bMs\b|\bthd\b|\bhia\b|\bMm\b|\bwitli\b|\btlie\b", s):
        return True
    if re.search(r"[%£¥{}|\\<>@#*_=+~`]", s):
        return True
    if s.count("(") != s.count(")"):
        return True
    if re.search(r"[a-z][A-Z]{2}|[A-Z]{2}[a-z]", s):  # midword caps (AVheu, buffaLo)
        return True
    letters = sum(c.isalpha() or c.isspace() or c in ".,;:'\"?!-—" for c in s)
    if letters / max(1, len(s)) < 0.9:
        return True
    return False


def title_from(text, maxlen=48):
    first = re.split(r"(?<=[.!?;:])\s", text.strip())[0]
    first = re.sub(r"^[\"“'‘]", "", first).strip()
    if len(first) > maxlen:
        return first[:maxlen].rsplit(" ", 1)[0].rstrip(",;:—- ") + "…"
    return first.rstrip(".")


def build():
    txt = open(SRC, encoding="utf-8").read()
    start = txt.index("CHAPTER XIII.", txt.index("FOLK-LORE TALES"))
    seg = txt[start:start + 42000]
    items = re.findall(r"\n(\d{1,3})\.\s+(.+?)(?=\n\d{1,3}\.\s|\nCHAPTER|\Z)", seg, re.S)
    # wipe old files so numbering is clean
    for f in glob.glob(os.path.join(OUT, "*.yml")):
        os.remove(f)
    os.makedirs(OUT, exist_ok=True)
    n = 0
    seen = set()
    for num, raw in items:
        p = clean(raw)
        if p.startswith("(") or len(p) < 18 or len(p) > 220:
            continue
        if not p.endswith((".", "!", "?", '"', "”")):
            continue
        if garbled(p):
            continue
        key = p.lower()
        if key in seen:
            continue
        seen.add(key)
        n += 1
        if n > CAP:
            break
        slug = "yoruba_proverbs"
        uid = f"{slug}.{slug}_{n:03d}"
        unit = {
            "source_id": f"{slug}_{n:03d}".upper(),
            "category": "root_text",
            "work_id": slug,
            "work_title": "Yoruba Proverbs (Òwe)",
            "unit_id": uid,
            "unit_label": title_from(p),
            "title": title_from(p),
            "unit_type": "proverb",
            "commentary": "",
            "themes": ["wisdom", "proverb", "yoruba"],
            "tags": [slug, "wisdom", "proverb", "yoruba"],
            "quality_score": 0,
            "editorial_score": 0,
            "editorial_maturity": "strong_draft",
            "translation_provenance": PROV,
            "pratibha_layers": [{"kind": "translation", "label": "Translation", "body": p}],
            "provenance": {"collection": "Yoruba Proverbs (Òwe)", "cultural_context": NOTE},
            "translation": p,
        }
        with open(os.path.join(OUT, f"{uid.replace('.', '_')}.yml"), "w", encoding="utf-8") as fh:
            yaml.safe_dump(unit, fh, allow_unicode=True, sort_keys=False, width=100)
    return n


if __name__ == "__main__":
    print("yoruba book:", build(), "proverbs")
