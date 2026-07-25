#!/usr/bin/env python3
"""Build 22 new Rūmī (Mathnawī) study-unit stubs from public-domain Ganjoor Persian.

Sources the exact Persian couplets for eleven of the Mathnawī's best-attested
stories (two study units each) straight from the Ganjoor API — never from
memory — so the source text is faithful and every unit carries a real
daftar/section reference. It writes only the Persian + metadata; the English,
commentary, and practice are produced afterward by render_from_sanskrit.py
(independent rendering, echo-gate on) and the transliteration by
transliterate_persian.py — exactly the pipeline used for the first 22 units.

    python scripts/build_rumi_expansion.py            # preview
    python scripts/build_rumi_expansion.py --write
"""
from __future__ import annotations

import argparse
import json
import os
import urllib.request

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COLL_DIR = os.path.join(ROOT, "data", "canonical", "rumi_mathnawi")
CACHE = os.path.join(ROOT, ".cache", "ganjoor")

# (unit, title, daftar, section, couplet_start, couplet_count, book_roman, story_en)
MANIFEST = [
    ("rum_023", "The King Falls in Love with the Dying Handmaiden", 1, "sh2", 0, 5, "I", "The King and the Handmaiden"),
    ("rum_024", "When the Physicians Fail, the King Turns to God", 1, "sh3", 0, 5, "I", "The King and the Handmaiden"),
    ("rum_025", "In Praise of the Hare's Knowledge", 1, "sh56", 0, 5, "I", "The Lion and the Hare"),
    ("rum_026", "The Lion Sees His Own Reflection in the Well", 1, "sh72", 0, 4, "I", "The Lion and the Hare"),
    ("rum_027", "It Is I at the Beloved's Door", 1, "sh144", 0, 4, "I", "The Lover at the Door"),
    ("rum_028", "“No Room for the Raw” — Enter by Dying to Self", 1, "sh144", 4, 4, "I", "The Lover at the Door"),
    ("rum_029", "The Old Harper Who Played for God", 1, "sh97", 0, 5, "I", "The Old Harper"),
    ("rum_030", "The Harper's Repentance and the Rain of Mercy", 1, "sh103", 0, 4, "I", "The Old Harper"),
    ("rum_031", "The Grammarian and the Boatman", 1, "sh137", 0, 4, "I", "The Grammarian and the Boatman"),
    ("rum_032", "All Your Grammar Is Drowned — Learn Self-Effacement", 1, "sh137", 4, 4, "I", "The Grammarian and the Boatman"),
    ("rum_033", "The Thirsty Man Who Threw Clods from the Wall", 2, "sh25", 0, 5, "II", "The Thirsty Man and the Wall"),
    ("rum_034", "The Barrier Between You and the Water", 2, "sh25", 5, 4, "II", "The Thirsty Man and the Wall"),
    ("rum_035", "The Ducklings Reared by a Hen", 2, "sh114", 0, 5, "II", "The Ducklings and the Hen"),
    ("rum_036", "The Sea Is Your Nurse, Not the Dry Land", 2, "sh114", 5, 4, "II", "The Ducklings and the Hen"),
    ("rum_037", "The Snake-Catcher and the Frozen Dragon", 3, "sh37", 0, 5, "III", "The Snake-Catcher and the Frozen Dragon"),
    ("rum_038", "The Dragon Thaws: The Nafs Revived by Warmth", 3, "sh37", 5, 5, "III", "The Snake-Catcher and the Frozen Dragon"),
    ("rum_039", "I Died as Mineral and Became a Plant", 3, "sh187", 17, 3, "III", "The Ascent of the Soul"),
    ("rum_040", "Beyond the Angel: To Him We Return", 3, "sh187", 20, 3, "III", "The Ascent of the Soul"),
    ("rum_041", "The Chickpea Leaps from the Boiling Pot", 3, "sh198", 0, 5, "III", "The Chickpea and the Cook"),
    ("rum_042", "The Cook Answers the Chickpea", 3, "sh200", 0, 5, "III", "The Chickpea and the Cook"),
    ("rum_043", "The Three Fishes: Wise, Half-Wise, and Foolish", 4, "sh83", 0, 5, "IV", "The Three Fishes"),
    ("rum_044", "The Half-Wise Fish Feigns Death", 4, "sh87", 0, 5, "IV", "The Three Fishes"),
]


def fetch_section(daftar: int, section: str) -> dict:
    os.makedirs(CACHE, exist_ok=True)
    fn = os.path.join(CACHE, f"daftar{daftar}_{section}.json")
    if not os.path.exists(fn):
        url = f"https://api.ganjoor.net/api/ganjoor/poem?url=/moulavi/masnavi/daftar{daftar}/{section}"
        with urllib.request.urlopen(url, timeout=30) as r:
            data = r.read()
        with open(fn, "wb") as f:
            f.write(data)
    return json.load(open(fn, encoding="utf-8"))


def couplets(poem: dict) -> list[tuple[str, str]]:
    v = poem.get("verses") or []
    out = []
    i = 0
    while i + 1 < len(v):
        out.append((v[i].get("text", "").strip(), v[i + 1].get("text", "").strip()))
        i += 2
    return out


def persian_block(cs: list[tuple[str, str]]) -> str:
    # Match the existing units' shape: "misra1 /// misra2" per couplet, newline-separated.
    return "\n".join(f"{a} /// {b}" for a, b in cs if a or b)


def build(unit, title, daftar, section, start, count, book, story) -> tuple[dict, str]:
    poem = fetch_section(daftar, section)
    cs = couplets(poem)
    chosen = cs[start:start + count]
    persian = persian_block(chosen)
    ref = f"Mathnawī-yi Maʿnawī, Book {book}, §{section[2:]} — {story} (Ganjoor, public domain)"
    d = {
        "source_file": f"data/canonical/rumi_mathnawi/{unit}.yml",
        "source_id": unit.upper(),
        "category": "root_text",
        "work_id": "rumi_mathnawi",
        "work_title": "Mathnawi-yi Ma'nawi",
        "unit_id": f"rumi_mathnawi.{unit}",
        "unit_label": title,
        "title": title,
        "unit_type": "sutra",
        "sanskrit_devanagari": persian,
        "sanskrit_iast": "See Original.",
        "sanskrit": persian,
        "translation_literal": "",
        "commentary": "",
        "practice": "",
        "themes": [],
        "tags": ["root_text", "rumi_mathnawi"],
        "quality_score": 0,
        "editorial_maturity": "strong_draft",
        "provenance": {
            "collection": "Rumi — Mathnawi-yi Ma'nawi",
            "section": story,
            "source_reference": ref,
            "ganjoor_url": f"/moulavi/masnavi/daftar{daftar}/{section}",
        },
    }
    return d, persian


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    made = 0
    for row in MANIFEST:
        unit, title = row[0], row[1]
        d, persian = build(*row)
        n_couplets = len(persian.split("\n")) if persian else 0
        print(f"{unit}: {title[:44]:44s} couplets={n_couplets}  {persian.split(chr(10))[0][:46]}")
        if not persian:
            print(f"  !! {unit}: no Persian extracted — check couplet range"); continue
        if args.write:
            path = os.path.join(COLL_DIR, f"{unit}.yml")
            yaml.safe_dump(d, open(path, "w", encoding="utf-8"), allow_unicode=True, sort_keys=False, width=100)
            made += 1
    print(f"\n{'wrote' if args.write else 'previewed'} {made if args.write else len(MANIFEST)} unit stubs")


if __name__ == "__main__":
    main()
