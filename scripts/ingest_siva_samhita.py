#!/usr/bin/env python3
"""Ingest the Śiva Saṃhitā, Rai Bahadur Srisa Chandra Vasu's English translation
(1914, published by Apurva Krishna Bose / the Panini Office — public domain).

Source: a proofread public-domain transcription of the Vasu 1914 edition,
data/raw_texts/pd/siva_samhita/siva_samhita_vasu_djvu.txt (verse text verbatim;
double-spaced OCR is collapsed, running heads and the translator's page markers
removed). Five chapters.

Marked for the "yoga" category, alongside the Haṭha Yoga Pradīpikā.
"""
import os, re
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data/raw_texts/pd/siva_samhita/siva_samhita_vasu_djvu.txt")
OUT = os.path.join(ROOT, "data/canonical/siva_samhita")
COLL = "Śiva Saṃhitā"
CATEGORY = "yoga"

CH_NAMES = {
    1: "On the One Reality (Jñāna)",
    2: "On the Microcosm (the Nāḍīs and the Inner Fire)",
    3: "On the Practice of Yoga (Prāṇāyāma and Āsana)",
    4: "On the Mudrās",
    5: "On the Fruits of Yoga",
}

PROV = ("English follows Rai Bahadur Srisa Chandra Vasu, *The Śiva Saṃhitā* (1914, Apurva Krishna "
        "Bose / Panini Office — public domain). Verbatim from a proofread public-domain "
        "transcription; verse numbering preserved, double-spaced OCR collapsed. Study rendering.")
NOTE = ("The Śiva Saṃhitā is a classical Sanskrit yoga treatise (spoken by Śiva to Pārvatī) on "
        "non-dual metaphysics, the subtle body (nāḍīs, cakras, kuṇḍalinī), prāṇāyāma, mudrā, and "
        "the fruits of practice — notably affirming that even a householder may attain liberation. "
        "The practices are traditionally learned from a qualified teacher; offered here as a study "
        "reading, not an instruction manual.")


def clean(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([;,.:!?)])", r"\1", s)
    s = re.sub(r"\(\s+", "(", s)
    s = s.replace("’", "'").replace("“", '"').replace("”", '"')
    return s.strip(" ;,")


def title_from(text, maxlen=52):
    first = re.split(r"(?<=[.!?;:])\s", text.strip())[0]
    first = re.sub(r"^[\"'(]", "", first).strip()
    if len(first) > maxlen:
        return first[:maxlen].rsplit(" ", 1)[0].rstrip(",;:—- ") + "…"
    return first.rstrip(".")


def write_unit(n, ch, vnum, title, body):
    slug = "siva_samhita"
    uid = f"{slug}.{slug}_{n:03d}"
    ch_label = CH_NAMES.get(ch, f"Chapter {ch}")
    themes = ["yoga", "subtle body" if ch in (2, 3, 4) else "non-duality", "śiva"]
    unit = {
        "source_id": f"{slug}_{n:03d}".upper(), "category": "root_text", "work_id": slug,
        "work_title": COLL, "unit_id": uid,
        "unit_label": f"Chapter {ch} — {vnum}", "title": title, "unit_type": "verse",
        "commentary": "", "themes": themes, "tags": [slug, CATEGORY] + themes,
        "quality_score": 0, "editorial_score": 0, "editorial_maturity": "strong_draft",
        "translation_provenance": PROV,
        "pratibha_layers": [{"kind": "translation", "label": "Translation", "body": body}],
        "provenance": {"collection": COLL, "category": CATEGORY, "chapter": ch_label,
                       "verse": f"{ch}.{vnum}", "cultural_context": NOTE},
        "translation": body,
    }
    with open(os.path.join(OUT, f"{uid.replace('.', '_')}.yml"), "w", encoding="utf-8") as fh:
        yaml.safe_dump(unit, fh, allow_unicode=True, sort_keys=False, width=100)


def build():
    os.makedirs(OUT, exist_ok=True)
    raw = open(SRC, encoding="utf-8", errors="ignore").read()
    # split into the five chapters on the "CHAPTER I..V" headers
    marks = list(re.finditer(r"\bCHAPTER\s+(I|II|III|IV|V)\b\.?", raw))
    ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5}
    # keep the LAST occurrence group per chapter start (TOC also mentions them, but the body
    # headers come after line ~55); take marks whose chapter increments monotonically.
    bounds = []
    seen = 0
    for m in marks:
        c = ROMAN[m.group(1)]
        if c == seen + 1:
            bounds.append((c, m.start()))
            seen = c
    bounds.append((99, len(raw)))
    n = 0
    for idx in range(len(bounds) - 1):
        ch, s = bounds[idx]
        seg = raw[s:bounds[idx + 1][1]]
        # strip running heads / page + key-entry markers
        seg = re.sub(r"The\s+Siva\s+Samhita\s*-\s*Chapter\s+[IVX]+", " ", seg, flags=re.I)
        seg = re.sub(r"Key\s+entry.*", " ", seg, flags=re.I | re.S)
        seg = re.sub(r"CHAPTER\s+[IVX]+\.?", " ", seg)
        seg = re.sub(r"\s+", " ", seg)
        # verses: a number (or range) followed by a period, then text up to the next such marker
        parts = re.split(r"(?:^|\s)(\d{1,3}(?:[-–]\d{1,3})?)\.\s+", " " + seg)
        # verse 1 opens the chapter as roman "I." and sits in the pre-marker chunk (parts[0]);
        # recover it verbatim from the first "I." to the chunk's end.
        m1 = re.search(r"\bI\.\s+([A-Z].*\.)\s*$", parts[0])
        if m1:
            body = clean(m1.group(1))
            if len(body) >= 15:
                n += 1
                write_unit(n, ch, "1", title_from(body), body)
        for i in range(1, len(parts) - 1, 2):
            vnum = parts[i].replace("–", "-")
            body = clean(parts[i + 1])
            # trim a trailing fragment that is actually the next section heading (all-caps run)
            body = re.sub(r"\s+[A-Z][A-Z .]{6,}$", "", body).strip()
            if len(body) < 15:
                continue
            n += 1
            write_unit(n, ch, vnum, title_from(body), body)
    return n


if __name__ == "__main__":
    print("siva_samhita:", build(), "units")
