#!/usr/bin/env python3
"""Dedup grounding: assign each Tantrasāra essay a DISTINCT Sanskrit segment
within its āhnika (joint one-to-one matching, no reuse). Terra returns the
assignment + a faithful translation per essay. Writes to the staging dir."""
import asyncio, glob, json, os, re, sys
import yaml
sys.path.insert(0, "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iast_to_deva import iast_to_deva
from app.llm import smart_chat
from app.data_loader import _as_text, normalize_unit

SP = os.path.dirname(os.path.abspath(__file__))
CANON = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha/data/canonical/tantrasara"
STAGE = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha/data/staging/tantrasara_grounded"
verses = json.load(open(f"{SP}/tantrasara_verses.json"))
DIG = str.maketrans("0123456789", "०१२३४५६७८९")

# essay ids grouped by āhnika
GROUPS = {
    1: ["ts_001", "ts_002", "ts_003", "ts_004", "ts_005", "ts_006", "ts_007"],
    2: ["ts_008", "ts_009"],
    3: ["ts_010", "ts_011", "ts_012"],
    4: ["ts_013", "ts_014"],
    5: ["ts_015", "ts_016", "ts_017", "ts_018", "ts_019"],
}

SYS = ("You ground several Pratibha essays about one āhnika of Abhinavagupta's Tantrasāra in its Sanskrit. "
       "Assign each essay a DISTINCT segment (one-to-one, NEVER reuse a segment for two essays) — the segment "
       "whose content that essay most directly reflects. If more essays than good matches, give the weakest essay "
       "the least-bad distinct segment. For each, give a faithful modern English translation, terms glossed. "
       'Return ONLY JSON: {"ts_001":{"segment":"1.1","translation":"...","confidence":"high|medium|low"}, ...}')


async def do_ahnika(ah, ids, sem):
    essays = {}
    for ts in ids:
        d = yaml.safe_load(open(os.path.join(CANON, f"tantrasara_{ts}.yml")))
        essays[ts] = (_as_text(d.get("title")), _as_text(d.get("commentary"))[:450])
    cand = {k: v for k, v in verses.items() if k.split(".")[0] == str(ah)}
    seg_list = "\n".join(f"{k}: {v[:130]}" for k, v in list(cand.items())[:40])
    essay_list = "\n\n".join(f"[{ts}] {t}:\n{c}" for ts, (t, c) in essays.items())
    async with sem:
        r = await smart_chat([{"role": "system", "content": SYS},
                              {"role": "user", "content": f"ĀHNIKA {ah} SEGMENTS:\n{seg_list}\n\nESSAYS ({len(ids)}, assign distinct):\n{essay_list}\n\nReturn JSON."}],
                             primary_model="openai/gpt-5.6-terra", temperature=0.2, max_tokens=1800)
    m = re.search(r"\{.*\}", re.sub(r"^```(?:json)?|```$", "", r.strip(), flags=re.M), re.S)
    return ah, json.loads(m.group(0))


async def main():
    sem = asyncio.Semaphore(3)
    results = await asyncio.gather(*(do_ahnika(ah, ids, sem) for ah, ids in GROUPS.items()))
    assign = {}
    for ah, mp in results:
        for ts, info in mp.items():
            assign[ts] = info
    # verify distinctness within āhnika
    for ah, ids in GROUPS.items():
        segs = [assign.get(t, {}).get("segment") for t in ids if assign.get(t, {}).get("segment")]
        dup = [s for s in set(segs) if segs.count(s) > 1]
        if dup:
            print(f"  WARN āhnika {ah} still has duplicate segments: {dup}")
    # write
    os.makedirs(STAGE, exist_ok=True)
    rich = 0
    for ts, info in sorted(assign.items()):
        seg = info.get("segment")
        if not seg or seg not in verses:
            print(f"  {ts}: no segment"); continue
        iast = re.sub(r"\s+", " ", verses[seg]).strip(" /")
        parts = [p.strip() for p in re.split(r"[/|]", iast) if p.strip()]
        d = yaml.safe_load(open(os.path.join(CANON, f"tantrasara_{ts}.yml")))
        d["sanskrit_iast"] = " |\n".join(parts) + f" || {seg} ||"
        d["sanskrit_devanagari"] = " ।\n".join(iast_to_deva(p) for p in parts) + f" ॥ {seg.translate(DIG)} ॥"
        d["translation_literal"] = info["translation"]
        d["source_verse"] = f"Tantrasāra {seg}"
        d["source_confidence"] = info.get("confidence")
        prov = d.get("provenance") if isinstance(d.get("provenance"), dict) else {}
        prov["sanskrit_source"] = f"GRETIL Abhinavagupta Tantrasāra {seg} (PD); Devanagari from IAST."
        d["provenance"] = prov
        nm = normalize_unit(d, "x")
        rich += nm["editorial_maturity"] in ("rich", "polished")
        print(f"  {ts} -> {seg} [{info.get('confidence')}] {nm['editorial_maturity']}")
        with open(os.path.join(STAGE, f"tantrasara_{ts}.yml"), "w") as fh:
            yaml.safe_dump(d, fh, allow_unicode=True, sort_keys=False, width=120)
    print(f"\ngrounded {len(assign)} | rich/polished {rich}")


if __name__ == "__main__":
    asyncio.run(main())
