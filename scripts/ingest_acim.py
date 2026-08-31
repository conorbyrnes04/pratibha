#!/usr/bin/env python3
"""Ingest A Course in Miracles (Original Edition) — a CURATED selection of its
most powerful passages: the Introduction, the Miracle Principles, and the
strongest theme passages (love, peace, abundance, healing, the real world).

PROVENANCE: ACIM's copyright was ruled null and void in Penguin Books v. New
Christian Church of Full Endeavor (S.D.N.Y. 2003, Judge Sweet) — the text was
distributed before publication without notice, placing the Original Edition (the
1972 unabridged Schucman/Thetford text) in the US public domain. Court-based PD
status (contested by the Foundation for Inner Peace), original edition only.
"""
import os, re
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data/raw_texts/pd/acim/acim_original_edition_hlc.txt")
OUT = os.path.join(ROOT, "data/canonical/a_course_in_miracles")
COLL = "A Course in Miracles (Original Edition)"

PROV = ("A Course in Miracles, Original Edition (the 1972 unabridged Schucman/Thetford text). "
        "Public domain in the US: its copyright was ruled null and void in Penguin Books v. New "
        "Christian Church of Full Endeavor (S.D.N.Y. 2003) for pre-publication distribution. "
        "Verbatim from the public-domain text; Original Edition only. Study rendering.")
NOTE = ("A Course in Miracles is a modern revelatory text (scribed 1965–1972 by Helen Schucman with "
        "William Thetford). This Original Edition is in the US public domain by a 2003 federal ruling "
        "that voided its copyright (a status contested by the Foundation for Inner Peace). Passages are "
        "verbatim from the public-domain text.")

# Powerful theme passages — an anchor phrase; the paragraph containing it is taken whole.
THEME_ANCHORS = [
    ("Teach only love, for that is what you are", "Teach Only Love", ["love", "teaching"]),
    ("The only way to have peace is to teach peace", "To Have Peace, Teach Peace", ["peace", "teaching"]),
    ("Miracles are affirmations of Sonship, which is a state of completion and abundance",
     "Completion and Abundance", ["abundance", "sonship"]),
    ("abandoned the belief in deprivation in favor of the abundance", "Abundance Belongs to You",
     ["abundance", "the miracle"]),
    ("Atonement is the principle, and healing is the result", "Healing Is the Result", ["healing", "atonement"]),
    ("God is not a stranger to His Sons", "God Is Not a Stranger", ["god", "knowledge"]),
    ("beyond the gate of Heaven", "The Gate of Heaven", ["heaven", "purity"]),
    ("The abundance of Christ is the natural result", "The Abundance of Christ", ["abundance", "christ"]),
]


def clean(s):
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"^\d+\s+", "", s)                         # leading page number
    s = re.sub(r"\s+\d+\s+", " ", s)                     # stray page numbers
    s = re.sub(r"([.!?\"])([A-Z])", r"\1 \2", s)          # missing space after sentence
    return s.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'").strip()


def title_from(text, maxlen=52):
    first = re.split(r"(?<=[.!?;:])\s", text.strip())[0]
    first = re.sub(r'^["\']', "", first).strip()
    if len(first) > maxlen:
        return first[:maxlen].rsplit(" ", 1)[0].rstrip(",;:—- ") + "…"
    return first.rstrip(".")


def write_unit(slug, n, title, body, themes):
    uid = f"{slug}.{slug}_{n:03d}"
    unit = {
        "source_id": f"{slug}_{n:03d}".upper(),
        "category": "root_text",
        "work_id": slug,
        "work_title": COLL,
        "unit_id": uid,
        "unit_label": title,
        "title": title,
        "unit_type": "principle",
        "commentary": "",
        "themes": themes,
        "tags": [slug] + themes,
        "quality_score": 0,
        "editorial_score": 0,
        "editorial_maturity": "strong_draft",
        "translation_provenance": PROV,
        "pratibha_layers": [{"kind": "original", "label": "Original", "body": body}],
        "provenance": {"collection": COLL, "cultural_context": NOTE},
        "original": body,
    }
    with open(os.path.join(OUT, f"{uid.replace('.', '_')}.yml"), "w", encoding="utf-8") as fh:
        yaml.safe_dump(unit, fh, allow_unicode=True, sort_keys=False, width=100)


def build():
    txt = open(SRC, encoding="utf-8").read()
    os.makedirs(OUT, exist_ok=True)
    slug = "a_course_in_miracles"
    n = 0

    # 1. The Introduction — the crown.
    n += 1
    write_unit(slug, n, "Nothing Real Can Be Threatened",
               "Nothing real can be threatened. Nothing unreal exists. Herein lies the peace of God.",
               ["the real", "peace", "the miracle"])

    # 2. The Miracle Principles.
    seg = txt[txt.index("Nothing real can be threatened"):]
    seg = seg[:60000]
    principles = re.findall(r"\n(\d{1,2})\.\s+\d+\s+(.+?)(?=\n\d{1,2}\.\s+\d+\s|\Z)", seg, re.S)
    used = set()
    for num, raw in principles:
        pn = int(num)
        if not (1 <= pn <= 50) or pn in used:
            continue
        body = clean(raw)
        if not (60 < len(body) < 620) or not body.endswith((".", '"', "!", "?")):
            continue
        used.add(pn)
        n += 1
        write_unit(slug, n, f"Miracle Principle {pn}", body, ["the miracle", "love"])

    # 3. Powerful theme passages.
    paras = [clean(p) for p in re.split(r"\n\s*\n", txt)]
    for anchor, title, themes in THEME_ANCHORS:
        hit = next((p for p in paras if anchor in p and 60 < len(p) < 620), None)
        if hit:
            n += 1
            write_unit(slug, n, title, hit, themes)
    return n


if __name__ == "__main__":
    print("acim:", build(), "units")
