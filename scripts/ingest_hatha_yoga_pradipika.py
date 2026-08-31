#!/usr/bin/env python3
"""Ingest the Haṭha Yoga Pradīpikā (Svātmārāma), Pañcham Sinh's English
translation (Panini Office, Allahabad; Sacred Books of the Hindus vol. 15,
1914/1915 — public domain).

Source text: a clean, proofread English-only transcription from Wikisource
(the Pañcham Sinh translation), saved verbatim to data/raw_texts/pd/hyp/
hyp_ch{1..4}.wikitext. Four chapters: āsanas, prāṇāyāma, mudrās, samādhi.

Marked for the "yoga" category (Haṭha/practice yoga), distinct from the
Kashmir-Śaiva tantra tomes.
"""
import os, re
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data/raw_texts/pd/hyp")
OUT = os.path.join(ROOT, "data/canonical/hatha_yoga_pradipika")
COLL = "Haṭha Yoga Pradīpikā"
CATEGORY = "yoga"

CHAPTERS = [
    (1, "On Āsanas", "āsana"),
    (2, "On Prāṇāyāma", "prāṇāyāma"),
    (3, "On Mudrās", "mudrā"),
    (4, "On Samādhi", "samādhi"),
]

PROV = ("English follows Pañcham Sinh, *The Haṭha Yoga Pradīpikā* (Panini Office, Allahabad; "
        "Sacred Books of the Hindus vol. 15, 1914/1915 — public domain). Verbatim from a proofread "
        "public-domain transcription; Sanskrit verse numbering preserved. Study rendering.")
NOTE = ("The Haṭha Yoga Pradīpikā, compiled by Svātmārāma (15th c.), is a foundational manual of "
        "haṭha yoga — āsana, prāṇāyāma, mudrā, and samādhi — presented as a ladder to rāja yoga. "
        "The practices (especially prāṇāyāma, kriyā, and bandha) are traditionally learned under a "
        "qualified teacher; offered here as a study reading, not an instruction manual.")


def wiki_clean(s: str) -> str:
    s = re.sub(r"<ref[^>]*>.*?</ref>", "", s, flags=re.S)      # footnotes
    s = re.sub(r"<ref[^>]*/>", "", s)
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"\{\{[^{}]*\}\}", "", s)                        # templates
    s = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", s)          # [[a|b]] -> b
    s = re.sub(r"\[\[([^\]]*)\]\]", r"\1", s)                   # [[a]] -> a
    s = re.sub(r"'''''(.+?)'''''", r"\1", s)
    s = re.sub(r"'''?(.+?)'''?", r"\1", s)                      # bold/italic
    s = re.sub(r"</?[a-z][^>]*>", "", s)                        # stray html
    s = s.replace("&nbsp;", " ").replace("&mdash;", "—").replace("&amp;", "&")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def title_from(text, maxlen=52):
    first = re.split(r"(?<=[.!?;:])\s", text.strip())[0]
    first = re.sub(r"^[\"'(]", "", first).strip()
    if len(first) > maxlen:
        return first[:maxlen].rsplit(" ", 1)[0].rstrip(",;:—- ") + "…"
    return first.rstrip(".")


def write_unit(n, ch_label, ch_tag, vnum, title, body):
    slug = "hatha_yoga_pradipika"
    uid = f"{slug}.{slug}_{n:03d}"
    themes = ["yoga", "haṭha yoga", ch_tag]
    unit = {
        "source_id": f"{slug}_{n:03d}".upper(), "category": "root_text", "work_id": slug,
        "work_title": COLL, "unit_id": uid,
        "unit_label": f"{ch_label} — {vnum}", "title": title, "unit_type": "verse",
        "commentary": "", "themes": themes, "tags": [slug, CATEGORY] + themes,
        "quality_score": 0, "editorial_score": 0, "editorial_maturity": "strong_draft",
        "translation_provenance": PROV,
        "pratibha_layers": [{"kind": "translation", "label": "Translation", "body": body}],
        "provenance": {"collection": COLL, "category": CATEGORY, "chapter": ch_label,
                       "verse": vnum, "cultural_context": NOTE},
        "translation": body,
    }
    with open(os.path.join(OUT, f"{uid.replace('.', '_')}.yml"), "w", encoding="utf-8") as fh:
        yaml.safe_dump(unit, fh, allow_unicode=True, sort_keys=False, width=100)


def build():
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for ch, ch_label, ch_tag in CHAPTERS:
        wt = open(os.path.join(RAW, f"hyp_ch{ch}.wikitext"), encoding="utf-8").read()
        verses = re.findall(r"^#\s+(.+)$", wt, re.M)
        for i, raw in enumerate(verses, 1):
            body = wiki_clean(raw)
            if len(body) < 20:
                continue
            n += 1
            write_unit(n, ch_label, ch_tag, f"{ch}.{i}", title_from(body), body)
    return n


if __name__ == "__main__":
    print("hatha_yoga_pradipika:", build(), "units")
