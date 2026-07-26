#!/usr/bin/env python3
"""Fill the romanization layer for non-Latin-script collections.

Generalizes the Persian transliterator to Chinese (pinyin), Ancient Greek,
classical Japanese (Hepburn), Sanskrit (IAST), and Persian. Reads the
source-language original (``sanskrit_devanagari``) and writes a clean
romanization to ``sanskrit_iast`` — transliteration only, so it introduces no
dependence on any copyrighted translation.

It overwrites placeholders and garbled part-romanizations ("See Original.",
"N/A…", pinyin-notes, key-terms mixed into the field, or any leftover source
script), and skips units that already hold a clean romanization.

    python scripts/transliterate.py --collection tao_te_ching            # preview
    python scripts/transliterate.py --collection tao_te_ching --write
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

COLLECTION_LANG = {
    "tao_te_ching": "chinese",
    "the_book_of_chuang_tzu": "chinese",
    "confucius_analects": "chinese",
    "zhongyong": "chinese",
    "plotinus_enneads": "greek",
    "heraclitus_fragments": "greek",
    "parmenides_fragments": "greek",
    "dogen_shobogenzo": "japanese",
    "rumi_mathnawi": "persian",
    "siva_sutra": "sanskrit",
    "chāndogya_upaniṣad": "sanskrit",
    "pratyabhijnahrdayam": "sanskrit",
}

LANG_PROMPT = {
    "chinese": """You are a Classical Chinese → Hànyǔ Pīnyīn transliterator.
Produce Hanyu Pinyin WITH tone marks for the given classical Chinese text.
- Transliterate ONLY. Do not translate, gloss, or comment.
- Preserve every line break exactly as given.
- Group syllables into words per standard pinyin orthography where natural; one syllable per character otherwise.
- Return ONLY the pinyin, no punctuation notes, no source characters.""",
    "greek": """You are an Ancient Greek transliterator.
Romanize the given Greek into standard scholarly transliteration.
- Transliterate ONLY. Do not translate, gloss, or list key terms.
- Use: ē (eta), ō (omega), y (upsilon), ph/th/ch/ps, rough breathing = initial h, ng for γγ/γκ. Keep accents if easy, else omit.
- Preserve every line break. Return ONLY the romanization — no Greek script, no notes.""",
    "japanese": """You are a Classical Japanese → Hepburn rōmaji transliterator.
Produce modified Hepburn romaji for the given classical Japanese (with kanji/kana).
- Transliterate ONLY. Do not translate or comment.
- Use macrons for long vowels (ō, ū); render particles は/へ/を as wa/e/o.
- Preserve every line break. Return ONLY the romaji — no kana/kanji, no notes.""",
    "persian": """You are a Persian (Farsi) transliterator.
Romanize the given classical Persian into clear scholarly transliteration (ā, ī, ū, kh, gh, ch, sh, zh, ʿ, ʾ; classical/Dari values).
- Transliterate ONLY. Preserve the " /// " hemistich separator and every line break.
- Return ONLY the romanization — no Perso-Arabic script, no notes.""",
    "sanskrit": """You are a Devanāgarī → IAST transliterator.
Produce IAST (International Alphabet of Sanskrit Transliteration) for the given Sanskrit.
- Transliterate ONLY. Do not translate or comment.
- Preserve every line break. Return ONLY the IAST — no Devanāgarī, no notes.""",
}

PLACEHOLDER_MARKERS = ("see original", "n/a", "chinese text", "no sanskrit", "pinyin romanization",
                       "key term", "not directly", "not provided", "with key terms")


def _is_latin(s: str) -> bool:
    for ch in s:
        o = ord(ch)
        if o < 0x300 or 0x1e00 <= o < 0x2100 or ch in "–—…‘’“”•/ \t\n":
            continue
        return False
    return True


def needs_translit(iast: str) -> bool:
    t = (iast or "").strip()
    if not t:
        return True
    low = t.lower()
    if any(m in low for m in PLACEHOLDER_MARKERS):
        return True
    if not _is_latin(t):          # leftover source script (Greek/Chinese/…)
        return True
    return False


def _clean(txt: str) -> str:
    txt = (txt or "").strip()
    txt = re.sub(r"^```.*?$", "", txt, flags=re.M).strip()
    txt = re.sub(r"^(transliteration|romanization|pinyin|rōmaji|romaji|iast)\s*:?\s*", "", txt, flags=re.I).strip()
    return txt


async def transliterate(text: str, lang: str) -> str | None:
    out = await smart_chat(
        [{"role": "system", "content": LANG_PROMPT[lang]},
         {"role": "user", "content": text}],
        temperature=0.2, max_tokens=1500,
    )
    out = _clean(out)
    return out or None


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--collection", required=True)
    ap.add_argument("--language", help="override; else inferred from collection")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    if not settings.OPENROUTER_API_KEY:
        sys.exit("set OPENROUTER_API_KEY")
    lang = args.language or COLLECTION_LANG.get(args.collection)
    if lang not in LANG_PROMPT:
        sys.exit(f"unknown language for {args.collection}; pass --language {list(LANG_PROMPT)}")

    files = sorted(glob.glob(os.path.join(ROOT, "data", "canonical", args.collection, "*.yml")))
    if args.limit:
        files = files[: args.limit]
    print(f"transliterate [{args.collection}, {lang}] — {len(files)} unit(s), "
          f"{'WRITE' if args.write else 'PREVIEW'}, model={settings.effective_default_model()}\n")

    done = skipped = failed = 0
    for i, path in enumerate(files, 1):
        d = yaml.safe_load(open(path, encoding="utf-8"))
        if not isinstance(d, dict):
            continue
        name = os.path.basename(path)
        original = str(d.get("sanskrit_devanagari") or d.get("original") or "").strip()
        if not original or _is_latin(original):
            skipped += 1; continue
        if not needs_translit(str(d.get("sanskrit_iast") or "")):
            skipped += 1; continue
        romanized = await transliterate(original, lang)
        if not romanized or not _is_latin(romanized):
            print(f"[{i}] {name}: transliteration failed/echoed script"); failed += 1; continue
        print(f"[{i}] {name}: {romanized.splitlines()[0][:78]}")
        if args.write:
            d["sanskrit_iast"] = romanized
            yaml.safe_dump(d, open(path, "w", encoding="utf-8"),
                           allow_unicode=True, sort_keys=False, width=100)
            done += 1
    print(f"\n{'wrote' if args.write else 'previewed'} {done}, skipped {skipped}, failed {failed}")


if __name__ == "__main__":
    asyncio.run(main())
