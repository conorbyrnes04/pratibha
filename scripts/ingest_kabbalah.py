#!/usr/bin/env python3
"""Ingest a Jewish Kabbalah collection from public-domain sources:
  - Sefer Yetzirah (Book of Formation), W. Wynn Westcott's translation (1887) —
    the foundational Kabbalistic text: the ten Sefirot and thirty-two paths.
  - A few clean verses of the Zohar (Sifra di-Tzeniuta / Idra) from S.L. MacGregor
    Mathers, The Kabbalah Unveiled (1887).

Both translations are public domain (pre-1929). An esoteric Jewish tradition,
offered with humility as a study reading.
"""
import os, re
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SY = os.path.join(ROOT, "data/raw_texts/pd/kabbalah/sefer_yetzirah_westcott_1887.txt")
ZO = os.path.join(ROOT, "data/raw_texts/pd/kabbalah/mathers_kabbalah_unveiled_1887_djvu.txt")
OUT = os.path.join(ROOT, "data/canonical/kabbalah_zohar_yetzirah")
COLL = "Kabbalah — Sefer Yetzirah & the Zohar"

PROV_SY = ("English follows W. Wynn Westcott, Sepher Yetzirah — The Book of Formation (1887, public "
           "domain). Study rendering of a foundational Kabbalistic text.")
PROV_ZO = ("English follows S.L. MacGregor Mathers, The Kabbalah Unveiled (1887, public domain), "
           "translating the Zohar. Study rendering.")
NOTE = ("Kabbalah is the esoteric stream of Jewish mysticism; some hold it as study-restricted "
        "(traditionally approached with maturity and grounding). Offered here with humility as a study "
        "reading, from public-domain translations — Westcott's Sefer Yetzirah and Mathers' Zohar.")


def clean(s):
    s = re.sub(r"(\w)-\s+(\w)", r"\1\2", s)            # rejoin OCR line-break hyphens
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\([^)]*\)", "", s)                    # drop translator parentheticals
    s = re.sub(r"\s+([;,.:!?])", r"\1", s)             # tighten space before punctuation
    s = re.sub(r"\s+", " ", s).strip(" ;,.")
    return s + "." if s and not s.endswith((".", "!", "?")) else s


def title_from(text, maxlen=48):
    first = re.split(r"(?<=[.!?;:])\s", text.strip())[0]
    if len(first) > maxlen:
        return first[:maxlen].rsplit(" ", 1)[0].rstrip(",;:—- ") + "…"
    return first.rstrip(".")


def write_unit(n, title, body, prov, themes):
    slug = "kabbalah_zohar_yetzirah"
    uid = f"{slug}.{slug}_{n:03d}"
    unit = {
        "source_id": f"{slug}_{n:03d}".upper(), "category": "root_text", "work_id": slug,
        "work_title": COLL, "unit_id": uid, "unit_label": title, "title": title,
        "unit_type": "verse", "commentary": "", "themes": themes, "tags": [slug] + themes,
        "quality_score": 0, "editorial_score": 0, "editorial_maturity": "strong_draft",
        "translation_provenance": prov,
        "pratibha_layers": [{"kind": "translation", "label": "Translation", "body": body}],
        "provenance": {"collection": COLL, "cultural_context": NOTE},
        "translation": body,
    }
    with open(os.path.join(OUT, f"{uid.replace('.', '_')}.yml"), "w", encoding="utf-8") as fh:
        yaml.safe_dump(unit, fh, allow_unicode=True, sort_keys=False, width=100)


def build():
    os.makedirs(OUT, exist_ok=True)
    n = 0
    # --- Sefer Yetzirah ---
    html = open(SY, encoding="utf-8", errors="ignore").read()
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"&[a-z]+;", " ", text)
    i = text.find("two and thirty")
    seg = text[i - 60:] if i > 0 else text
    verses = re.findall(r"\b(\d{1,2})\.\s+([A-Z][^0-9]{40,420}?\.)\s", seg[:16000])
    seen = set()
    for num, v in verses:
        body = re.sub(r"\s+", " ", v).strip()
        body = re.sub(r"([;,])n([a-z])", r"\1 \2", body)   # mangled line-break "Fire;nthe"
        if len(body) < 45 or body.lower()[:40] in seen:
            continue
        seen.add(body.lower()[:40])
        n += 1
        write_unit(n, title_from(body), body, PROV_SY, ["kabbalah", "creation", "the sefirot"])
        if n >= 23:
            break
    # --- Zohar: a few clean verbatim verses from Mathers (verse text starts on the
    # given 1-indexed line; we join wrapped lines until the first blank / bracket /
    # asterisk footnote, then drop parenthetical commentary). Anchors verified by hand
    # against the source file so the text is verbatim, not model-supplied.
    zlines = open(ZO, encoding="utf-8", errors="ignore").read().splitlines()
    ZOHAR_ANCHORS = [
        (7906, ["the concealed", "the divine"]),   # The Ancient One is hidden and concealed
        (5545, ["equilibrium", "the divine"]),      # In His form existeth the equilibrium
        (9112, ["the vast countenance", "light"]),  # White are His garments
        (6736, ["light", "the divine"]),            # Two apples are beheld, to illuminate the lights
    ]
    zc = 0
    for start, themes in ZOHAR_ANCHORS:
        buf = []
        for ln in zlines[start - 1:start + 5]:
            s = ln.strip()
            if not s or s[0] in "[*" or (buf and s[0].isdigit() and "." in s[:3]):
                break
            buf.append(s)
        body = clean(re.sub(r"^\d{1,2}\.\s*", "", " ".join(buf)))
        body = re.sub(r"\s+([;,.])", r"\1", body)
        if len(body) < 40:
            continue
        zc += 1
        n += 1
        write_unit(n, title_from(body), body, PROV_ZO, ["kabbalah"] + themes)
        if zc >= 4:
            break
    return n


if __name__ == "__main__":
    print("kabbalah:", build(), "units")
