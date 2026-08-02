#!/usr/bin/env python3
"""Fix the layer-override regression in VBT / Spanda: units carried explicit
pratibha_layers holding the OLD copyrighted translation/commentary/resonances,
which overrode the fresh flat fields the pipeline wrote. This generates a real
practice (the old one was generic boilerplate) and DELETES the stale explicit
pratibha_layers so every layer derives from the fresh flat fields.
Resumable; --write to persist."""
import argparse, asyncio, glob, os, re, sys
import yaml
sys.path.insert(0, "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha")
from app.llm import smart_chat  # noqa
from app.data_loader import normalize_unit, _as_text, _practice_is_generic  # noqa

DIRS = {
    "vbt": ("/Users/conorbyrnes04/Documents/Projects/VAK/pratibha/data/canonical/vijnana_bhairava",
            "a dhāraṇā (centering technique) from the Vijñāna Bhairava"),
    "spanda": ("/Users/conorbyrnes04/Documents/Projects/VAK/pratibha/data/staging/spanda_sanskrit",
               "a kārikā of Vasugupta's Spandakārikā on spanda, the pulse of consciousness"),
}
SYS = ("Write ONE concrete first-person-neutral practice instruction (2–3 sentences) that a "
       "practitioner can actually do today, distilled from this passage of {ctx}. Embodied and "
       "specific — not 'reflect on' or 'read slowly'. Return ONLY the practice text, no preamble.")


async def practice_for(iast, trans, ctx, sem):
    async with sem:
        try:
            t = await smart_chat([{"role": "system", "content": SYS.format(ctx=ctx)},
                                  {"role": "user", "content": f"IAST: {iast}\nTranslation: {trans}"}],
                                 temperature=0.5, max_tokens=200)
            return re.sub(r"^```.*|```$", "", t.strip()).strip().strip('"')
        except Exception as e:
            return None


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--which", choices=list(DIRS), required=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    d_dir, ctx = DIRS[args.which]
    files = sorted(glob.glob(os.path.join(d_dir, "*.yml")))
    if args.limit:
        files = files[: args.limit]
    sem = asyncio.Semaphore(5)

    async def one(f):
        d = yaml.safe_load(open(f))
        cur = _as_text(d.get("practice") or d.get("abhyasa"))
        need = _practice_is_generic(cur) or not cur
        pr = await practice_for(_as_text(d.get("sanskrit_iast")), _as_text(d.get("translation_literal")), ctx, sem) if need else cur
        return f, d, pr

    results = await asyncio.gather(*(one(f) for f in files))
    rich = fail = 0
    for f, d, pr in results:
        if not pr:
            fail += 1; print("  practice FAIL", os.path.basename(f)); continue
        d["practice"] = pr
        d["abhyasa"] = pr
        d.pop("pratibha_layers", None)          # drop stale explicit layers
        nm = normalize_unit(d, f)
        served = [L["kind"] for L in nm["pratibha_layers"]]
        is_rich = nm["editorial_maturity"] in ("rich", "polished")
        rich += is_rich
        if args.write:
            with open(f, "w") as fh:
                yaml.safe_dump(d, fh, allow_unicode=True, sort_keys=False, width=120)
        if args.limit and not args.write:
            print(f"  {os.path.basename(f)} [{nm['editorial_maturity']}] {served}")
            print(f"     practice: {pr[:80]}")
    print(f"\n{'wrote' if args.write else 'previewed'} {len(results)-fail} | rich {rich} | fail {fail}")


if __name__ == "__main__":
    asyncio.run(main())
