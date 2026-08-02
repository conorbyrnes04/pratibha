#!/usr/bin/env python3
"""Modernize period-register PD translations (Marcus Aurelius, Pseudo-Dionysius)
into faithful, dignified modern English — preserving the meaning of the existing
translation, grounded in the Greek original, no thee/thou/-eth. Surgically
updates ONLY the translation (flat field + the explicit pratibha_layers entry),
leaving commentary / practice / original untouched. Resumable."""
import argparse, asyncio, glob, os, re, sys
import yaml
sys.path.insert(0, "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha")
from app.llm import smart_chat          # noqa
from app.data_loader import _as_text     # noqa

CANON = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha/data/canonical"

SYS = """You modernize the English register of a public-domain translation of {work}, WITHOUT changing its meaning.

You are given the Greek original and an archaic English translation (thee/thou/-eth/unto…). Re-render it in clear, dignified CONTEMPORARY English — the philosophical register of a good modern translation. Preserve the sense, argument, and imagery exactly; only the register changes. Do not add, cut, or reinterpret. Keep any pivotal Greek term glossed in brackets where it aids the reader. No archaic pronouns or verb endings.

Return ONLY the modernized English translation text, no preamble, no quotes."""


async def one(path, work, sem, force):
    d = yaml.safe_load(open(path))
    if not force and d.get("register") == "modern":
        return path, None, True
    greek = _as_text(d.get("sanskrit_devanagari"))
    arch = _as_text(d.get("translation") or d.get("translation_literal"))
    if not arch:
        return path, None, False
    async with sem:
        try:
            txt = await smart_chat([{"role": "system", "content": SYS.format(work=work)},
                                    {"role": "user", "content": f"Greek: {greek[:600]}\n\nArchaic translation:\n{arch[:1400]}"}],
                                   temperature=0.3, max_tokens=900)
        except Exception as e:
            return path, {"_error": str(e)[:60]}, False
    return path, re.sub(r'^```.*|```$', '', txt.strip()).strip().strip('"'), False


async def run(coll, work, write, limit):
    files = sorted(glob.glob(os.path.join(CANON, coll, "*.yml")))
    if limit:
        files = files[:limit]
    sem = asyncio.Semaphore(5)
    res = await asyncio.gather(*(one(f, work, sem, write) for f in files))
    ok = fail = 0
    for path, new, skipped in res:
        if skipped:
            continue
        if not new or isinstance(new, dict):
            fail += 1; print("  FAIL", os.path.basename(path)); continue
        d = yaml.safe_load(open(path))
        old = _as_text(d.get("translation") or d.get("translation_literal"))
        d["translation_literal"] = new
        d["translation"] = None
        d["register"] = "modern"
        for L in (d.get("pratibha_layers") or []):
            if isinstance(L, dict) and L.get("kind") == "translation":
                L["body"] = new
        ok += 1
        if limit and not write:
            print(f"=== {os.path.basename(path)} ===")
            print("OLD:", old[:110]); print("NEW:", new[:110]); print()
        if write:
            with open(path, "w") as fh:
                yaml.safe_dump(d, fh, allow_unicode=True, sort_keys=False, width=120)
    print(f"{coll}: {'wrote' if write else 'previewed'} {ok} | fail {fail}")


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    await run("marcus_aurelius_meditations", "Marcus Aurelius' Meditations", args.write, args.limit)
    await run("pseudo_dionysius", "Pseudo-Dionysius (Mystical Theology / Divine Names)", args.write, args.limit)


if __name__ == "__main__":
    asyncio.run(main())
