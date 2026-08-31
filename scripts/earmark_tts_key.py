#!/usr/bin/env python3
"""Earmark which verses are TTS ("Listen") key verses.

Ships ALL verses in the corpus, but for *really large* collections only a curated
set of key verses is TTS-eligible (so Listen offers "the essentials", not 500
verses). Bhagavad Gītā is the explicit exception: every verse is a key verse.

- GATED collections: an LLM curates the N most essential / quotable / representative
  verses; those get `tts_key: true`.
- Bhagavad Gītā: every verse gets `tts_key: true`.
- All other (smaller) collections are left unmarked; the Listen gate treats any verse
  in a non-gated collection as eligible (see app/tts.py available_sections).
"""
import argparse, asyncio, glob, json, os, re, sys
import yaml

ROOT = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha"
sys.path.insert(0, ROOT)
from app.llm import smart_chat  # noqa

CANON = os.path.join(ROOT, "data/canonical")

# really-large collections → number of TTS key verses to curate
GATED = {
    "siva_samhita": 30,
    "marcus_aurelius_meditations": 30,
    "hatha_yoga_pradipika": 28,
}
ALL_KEY = {"bhagavad_gita"}   # every verse is a key verse

SELECT_SYSTEM = """You curate a short "listen to the essentials" set for a large classical wisdom text. From the numbered verses given, choose the {n} most essential to hear read aloud: the most quotable, spiritually central, and self-contained verses that best represent the whole text to a newcomer. Prefer verses that stand on their own as wisdom; avoid purely procedural or technical verses (exact breath counts, cleansing techniques, long anatomical or enumerative lists) unless a verse is genuinely iconic. Spread the choices across the whole text, not just the opening. Return ONLY a JSON array of the chosen verse numbers, e.g. [3, 17, 42]."""


def layer_text(u):
    """Best English verse text — TTS speaks English, so prefer a Latin-script
    translation over a non-Latin original (e.g. Marcus's Greek original layer)."""
    cands = []
    for L in u.get("pratibha_layers", []) or []:
        if L.get("kind") == "translation" and L.get("body"):
            cands.append(str(L["body"]))
    for k in ("translation", "translation_literal"):
        if u.get(k):
            cands.append(str(u[k]))
    for L in u.get("pratibha_layers", []) or []:
        if L.get("kind") == "original" and L.get("body"):
            cands.append(str(L["body"]))
    for k in ("original", "text"):
        if u.get(k):
            cands.append(str(u[k]))
    for c in cands:
        if sum(1 for ch in c if ch.isascii() and ch.isalpha()) >= 20:
            return c
    return cands[0] if cands else ""


def set_key(path, value: bool):
    u = yaml.safe_load(open(path))
    if value:
        u["tts_key"] = True
    else:
        u.pop("tts_key", None)
    with open(path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(u, fh, allow_unicode=True, sort_keys=False, width=100)


async def curate(slug, n):
    files = sorted(glob.glob(os.path.join(CANON, slug, "*.yml")))
    units = [(f, yaml.safe_load(open(f))) for f in files]
    listing = "\n".join(
        f"{i}. {re.sub(chr(92)+'s+', ' ', layer_text(u))[:150]}" for i, (f, u) in enumerate(units, 1)
    )
    msg = [
        {"role": "system", "content": SELECT_SYSTEM.format(n=n)},
        {"role": "user", "content": f"Text: {units[0][1].get('work_title', slug)}\n\n{listing}\n\nReturn the JSON array of {n} verse numbers."},
    ]
    txt = await smart_chat(msg, temperature=0.3, max_tokens=400)
    m = re.search(r"\[[\d,\s]+\]", txt)
    if not m:
        print(f"  {slug}: NO selection returned"); return
    picks = {int(x) for x in re.findall(r"\d+", m.group(0)) if 1 <= int(x) <= len(units)}
    for i, (f, u) in enumerate(units, 1):
        set_key(f, i in picks)
    print(f"  {slug}: {len(picks)} key verses of {len(units)}")


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    for slug in ALL_KEY:
        files = glob.glob(os.path.join(CANON, slug, "*.yml"))
        if args.only and args.only != slug:
            continue
        for f in files:
            set_key(f, True)
        print(f"  {slug}: ALL {len(files)} verses marked key")
    for slug, n in GATED.items():
        if args.only and args.only != slug:
            continue
        await curate(slug, n)


if __name__ == "__main__":
    asyncio.run(main())
