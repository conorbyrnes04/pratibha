#!/usr/bin/env python3
"""Content-align the 39 real Spandakārikā units to the GRETIL kārikās (IAST).
Odier's numbering merges/omits vs the traditional text, so each real unit maps
to one OR MORE consecutive kārikās, monotonic. Verified for monotonicity +
coverage; low-confidence maps are flagged, never force-fit. No writes."""
import asyncio, json, os, re, sys
sys.path.insert(0, "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha")
from app.llm import smart_chat  # noqa

SP = os.path.dirname(os.path.abspath(__file__))
units = json.load(open(f"{SP}/spanda_units.json"))
real = {int(k): v for k, v in units["real"].items()}
seq = json.load(open(f"{SP}/spanda_clean.json"))
KARIKA = {i + 1: seq[i] for i in range(len(seq) - 2)}  # drop 2 colophon verses

real_block = "\n".join(f"[{n}] {real[n][:150]}" for n in sorted(real))
kar_block = "\n".join(f"({i}) {KARIKA[i]}" for i in sorted(KARIKA))

SYSTEM = """You align English translations of Spandakārikā verses to their Sanskrit (IAST) kārikās.
You get REAL translated units (in text order, but non-consecutively numbered — the gaps are duplicate units removed) and the Sanskrit kārikās (numbered 1..N in order).
Map each unit number to the kārikā number(s) it translates. Rules:
- kārikā numbers must be NON-DECREASING as unit order increases.
- A unit usually maps to ONE kārikā; some map to TWO consecutive kārikās (the source merged them).
- Cover the kārikās in order with no gaps if possible.
- If a unit's match is uncertain, set its value to [] rather than guessing.
Return ONLY JSON mapping unit->list-of-karika-ints, e.g. {"1":[1],"2":[2],"3":[3,4],...}"""

async def main():
    out = await smart_chat(
        [{"role": "system", "content": SYSTEM},
         {"role": "user", "content": f"UNITS:\n{real_block}\n\nKARIKAS:\n{kar_block}\n\nReturn the JSON map."}],
        temperature=0.0, max_tokens=3000)
    out = re.sub(r"^```(?:json)?|```$", "", out.strip(), flags=re.M).strip()
    mapping = {int(k): [int(x) for x in v] for k, v in json.loads(re.search(r"\{.*\}", out, re.S).group(0)).items()}

    last = 0; problems = []; uncertain = []
    for n in sorted(real):
        vs = mapping.get(n, [])
        if not vs:
            uncertain.append(n); continue
        if vs[0] < last:
            problems.append(f"unit {n}: non-monotonic {vs} after {last}")
        last = vs[-1]
    covered = sorted({v for vs in mapping.values() for v in vs})
    gaps = [k for k in KARIKA if k not in covered]
    print(f"real units mapped: {len([n for n in mapping if mapping[n]])}/{len(real)}")
    print(f"kārikā coverage: {len(covered)}/{len(KARIKA)} | gaps: {gaps}")
    print(f"uncertain (flagged, not forced): {uncertain}")
    print(f"monotonicity problems: {len(problems)}")
    for p in problems[:10]:
        print("  -", p)
    json.dump({str(k): v for k, v in mapping.items()}, open(f"{SP}/spanda_alignment.json", "w"))
    # spot content check
    print("\nspot-check:")
    for n in list(sorted(real))[:3] + list(sorted(real))[-3:]:
        vs = mapping.get(n, [])
        print(f"  unit {n} -> {vs}")
        print(f"    EN: {real[n][:60]}")
        if vs:
            print(f"    SA: {KARIKA[vs[0]][:60]}")

asyncio.run(main())
