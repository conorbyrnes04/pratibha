#!/usr/bin/env python3
"""Fill the romanized-transliteration layer for Persian units (Rūmī).

The Rūmī units carry correct Ganjoor Persian in the Original layer but the
transliteration slot (`sanskrit_iast`) is a "See Original." placeholder, which
shuts out any student who cannot read the Perso-Arabic script. This produces a
readable scholarly romanization from the Persian itself — no translation, so it
introduces no dependence on any copyrighted English rendering.

It also stamps an honest book/story source reference derived from the unit
grouping (verifiable from the well-known location of each story in the Mathnawī).

    python scripts/transliterate_persian.py --collection rumi_mathnawi          # preview
    python scripts/transliterate_persian.py --collection rumi_mathnawi --write
"""
from __future__ import annotations

import argparse
import asyncio
import glob
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import settings          # noqa: E402
from app.llm import smart_chat           # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SYSTEM = """You are a Persian (Farsi) transliterator. Romanize the given classical Persian couplets into a clear, readable scholarly transliteration.

RULES:
- Transliterate ONLY. Do NOT translate, gloss, or comment.
- Preserve the line structure exactly: keep the " /// " hemistich separator and every line break as given.
- Use a consistent readable romanization: ā (alef/madd), i/u for short vowels, ī/ū where long, kh (خ), gh/q (غ/ق), ch (چ), sh (ش), zh (ژ), ʿ (ayn), ʾ (hamza). Reflect classical/Dari values (e.g. "chun", "mikonad", "jodāyi").
- Return ONLY the transliteration text, no quotes, no notes, no JSON."""

# Source references derived from the unit grouping. These are book/story level
# (the location of each story in the Mathnawī is well established); no fabricated
# per-line numbers.
SOURCE_REF = {
    range(1, 9):  "Mathnawī-yi Maʿnawī, Book I — proem, the Song of the Reed (Ney-nāma), ll. 1–18 (Ganjoor)",
    range(9, 13): "Mathnawī-yi Maʿnawī, Book II — Moses and the shepherd (Ganjoor)",
    range(13, 16): "Mathnawī-yi Maʿnawī, Book III — The elephant in the dark house (Ganjoor)",
    range(16, 18): "Mathnawī-yi Maʿnawī, Book I — The contest of the Chinese and the Greek painters (Ganjoor)",
    range(18, 23): "Mathnawī-yi Maʿnawī, Book I — The merchant and his parrot (Ganjoor)",
}


def source_ref_for(unit_num: int) -> str | None:
    for rng, ref in SOURCE_REF.items():
        if unit_num in rng:
            return ref
    return None


def _clean(txt: str) -> str:
    txt = txt.strip()
    txt = re.sub(r"^```.*?$", "", txt, flags=re.M).strip()
    # Drop any accidental leading label like "Transliteration:".
    txt = re.sub(r"^(transliteration|romanization)\s*:?\s*", "", txt, flags=re.I).strip()
    return txt


async def transliterate(persian: str) -> str | None:
    out = await smart_chat(
        [{"role": "system", "content": SYSTEM},
         {"role": "user", "content": persian}],
        temperature=0.2, max_tokens=1200,
    )
    out = _clean(out or "")
    return out or None


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--collection", default="rumi_mathnawi")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    if not settings.OPENROUTER_API_KEY:
        sys.exit("set OPENROUTER_API_KEY")

    files = sorted(glob.glob(os.path.join(ROOT, "data", "canonical", args.collection, "*.yml")))
    if args.limit:
        files = files[: args.limit]
    print(f"transliterate [{args.collection}] — {len(files)} unit(s), "
          f"{'WRITE' if args.write else 'PREVIEW'}, model={settings.effective_default_model()}\n")

    done = 0
    for i, path in enumerate(files, 1):
        d = yaml.safe_load(open(path, encoding="utf-8"))
        if not isinstance(d, dict):
            continue
        name = os.path.basename(path)
        persian = str(d.get("sanskrit_devanagari") or "").strip()
        cur = str(d.get("sanskrit_iast") or "").strip()
        if not persian:
            print(f"[{i}] {name}: no Persian source — skip"); continue
        # Idempotent: skip units already transliterated.
        if args.write and cur and cur not in ("See Original.", "None", ""):
            done += 1; continue
        translit = await transliterate(persian)
        if not translit:
            print(f"[{i}] {name}: transliteration failed"); continue
        m = re.search(r"_(\d+)\.yml$", name)
        num = int(m.group(1)) if m else 0
        ref = source_ref_for(num)
        print(f"[{i}] {name}: {translit.splitlines()[0][:80]}")
        if args.write:
            d["sanskrit_iast"] = translit
            if ref:
                prov = d.get("provenance")
                if isinstance(prov, dict) and not prov.get("source_reference"):
                    prov["source_reference"] = ref
            yaml.safe_dump(d, open(path, "w", encoding="utf-8"),
                           allow_unicode=True, sort_keys=False, width=100)
            done += 1
    print(f"\n{'wrote' if args.write else 'previewed'} {done} unit(s)")


if __name__ == "__main__":
    asyncio.run(main())
