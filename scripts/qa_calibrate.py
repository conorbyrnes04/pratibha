#!/usr/bin/env python3
"""Calibration: how much did the cheap triage (Gemini Flash) MISS?

Takes a stratified sample of units the tiered QA pass marked 'sound' (i.e. Flash
passed them, so they never reached the strong reviewer) and sends them STRAIGHT to
the strong reviewer (Claude Sonnet), read-only. If Sonnet flags many of these as
minor/error, the triage is under-sensitive and the corpus 'sound' verdicts are
optimistic. Writes nothing to the corpus — pure measurement.

  python qa_calibrate.py [--per-collection 5] [--reviewer anthropic/claude-sonnet-4.5]
"""
import argparse, asyncio, glob, os, random, sys
import yaml

REPO = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha"
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, "scripts"))
from qa_crosscheck import original_of, translation_of, SYS_REVIEW, _ask, CANON  # noqa: E402
from faithful_expand_upanishads import _lenient_json  # noqa: E402
from app.data_loader import _as_text  # noqa: E402

REPORT = os.path.join(REPO, "data/qa_crosscheck_report.tsv")


def sound_sample(per_collection, seed):
    """Stratified sample of 'sound'-verdict units, up to N per collection."""
    by_coll = {}
    for line in open(REPORT):
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 4 or parts[2] != "sound":
            continue
        by_coll.setdefault(parts[0], []).append(parts[1])
    rng = random.Random(seed)
    picks = []
    for coll, sids in sorted(by_coll.items()):
        rng.shuffle(sids)
        for sid in sids[:per_collection]:
            picks.append((coll, sid))
    return picks


def find_unit(coll, sid):
    for path in glob.glob(os.path.join(CANON, coll, "*.yml")):
        d = yaml.safe_load(open(path))
        if isinstance(d, dict) and _as_text(d.get("source_id")) == sid:
            return path, d
    return None, None


async def review(coll, sid, reviewer, sem, out):
    path, d = find_unit(coll, sid)
    if not d:
        return
    orig, lang = original_of(d)
    trans = translation_of(d)
    if not orig or len(trans) < 20:
        return
    work = _as_text((d.get("provenance") or {}).get("collection")) or coll
    ref = _as_text((d.get("provenance") or {}).get("section")) or sid
    r = await _ask(reviewer, SYS_REVIEW.replace("{work}", work),
                   f"Passage: {work} — {ref}\nORIGINAL ({lang}):\n{orig[:2600]}\n\nNEW TRANSLATION:\n{trans[:2600]}\n\nReturn JSON.",
                   sem)
    if r in (None, "__NO_CREDITS__"):
        out.append((coll, sid, "ERR" if r is None else "NO_CREDITS", ""))
        return
    v = _lenient_json(r) or {}
    verdict = v.get("verdict", "sound")
    issues = "; ".join(x for x in (v.get("issues") or []) if x)[:200]
    out.append((coll, sid, verdict, issues))


async def main_async(args):
    picks = sound_sample(args.per_collection, args.seed)
    print(f"[calibrate] re-reviewing {len(picks)} 'sound' units directly with {args.reviewer} (triage bypassed)")
    sem = asyncio.Semaphore(args.concurrency)
    out = []
    await asyncio.gather(*(review(c, s, args.reviewer, sem, out) for c, s in picks))
    import collections as C
    dist = C.Counter(v for _, _, v, _ in out)
    n = len(out)
    missed = sum(dist.get(k, 0) for k in ("minor", "error"))
    print(f"[calibrate] Sonnet verdicts on triage-'sound' units: {dict(dist)}")
    if n:
        print(f"[calibrate] triage MISS RATE (sound→flagged by strong model): "
              f"{missed}/{n} = {100*missed/n:.0f}%  (error alone: "
              f"{dist.get('error',0)}/{n} = {100*dist.get('error',0)/n:.0f}%)")
    print("\n  newly-flagged (triage said sound, Sonnet disagrees):")
    for coll, sid, v, issues in sorted(out):
        if v in ("minor", "error"):
            print(f"   [{v:5}] {coll}/{sid}: {issues[:110]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-collection", type=int, default=5)
    ap.add_argument("--reviewer", default="anthropic/claude-sonnet-4.5")
    ap.add_argument("--concurrency", type=int, default=6)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
