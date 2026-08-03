#!/usr/bin/env python3
"""Reference-location audit of self-sourced Sanskrit: Luna checks whether each
verse actually SITS at its claimed reference (not just whether the wording is
valid Sanskrit) — catching mislabels like na-tatra-cakṣur (Kena) filed under BU.
Flags mismatches needs_source_review; does not auto-edit text."""
import asyncio, glob, json, os, re, sys
import yaml
sys.path.insert(0, "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha")
from app.llm import smart_chat
from app.data_loader import _as_text

COLLS = {"katha_upanishad": "Kaṭha Upaniṣad", "brihadaranyaka_upanishad": "Bṛhadāraṇyaka Upaniṣad",
         "mundaka_upanishad": "Muṇḍaka Upaniṣad", "isavasya_upanishad": "Īśāvāsya Upaniṣad",
         "svetasvatara_upanishad": "Śvetāśvatara Upaniṣad", "astavakra_gita": "Aṣṭāvakra Gītā",
         "mandukya_upanishad_and_gaudapada_karika": "Māṇḍūkya Upaniṣad / Gauḍapāda Kārikā"}
SYS = ("You are a Sanskrit textual scholar. Given a work, a claimed reference, and an IAST verse, judge whether "
       "this verse actually occurs AT that reference in that work. If the verse is genuinely from a DIFFERENT "
       "location or a different text, say so.\n"
       'Return ONLY JSON: {"located_here":true|false,"actual_location":"<where it really is if not here, else empty>","confidence":"high|medium|low"}')


async def audit(path, name, sem):
    d = yaml.safe_load(open(path))
    prov = d.get("provenance") or {}
    if "2026" not in str(prov.get("english_source", "")):
        return path, "skip"
    iast = _as_text(d.get("sanskrit_iast"))
    if not iast:
        return path, "no-iast"
    ref = _as_text(d.get("source_verse")) or _as_text(d.get("source_id"))
    body = re.sub(r"\s*\|\|.*", "", iast).replace("\n", " ").strip()
    async with sem:
        for a in range(3):
            try:
                r = await smart_chat([{"role": "system", "content": SYS},
                                      {"role": "user", "content": f"Work: {name}\nClaimed reference: {ref}\nVerse: {body}\n\nReturn JSON."}],
                                     primary_model="openai/gpt-5.6-luna", temperature=0.0, max_tokens=300)
                break
            except Exception:
                await asyncio.sleep(2 * (a + 1)); r = None
        if r is None:
            return path, "ERR"
    m = re.search(r"\{.*\}", re.sub(r"^```(?:json)?|```$", "", r.strip(), flags=re.M), re.S)
    try:
        v = json.loads(m.group(0))
    except Exception:
        return path, "parse"
    if v.get("located_here") is False and v.get("confidence") in ("high", "medium"):
        prov["original_reliability"] = f"MISLABELED — verse likely belongs at: {v.get('actual_location','elsewhere')}, not {ref}. Needs correction."
        d["provenance"] = prov; d["needs_source_review"] = True
        yaml.safe_dump(d, open(path, "w"), allow_unicode=True, sort_keys=False, width=120)
        return path, "MISLABELED:" + str(v.get("actual_location", ""))[:30]
    return path, "ok"


async def main():
    sem = asyncio.Semaphore(3)
    tasks = []
    for coll, name in COLLS.items():
        for path in glob.glob(f"/Users/conorbyrnes04/Documents/Projects/VAK/pratibha/data/canonical/{coll}/*.yml"):
            tasks.append(audit(path, name, sem))
    res = await asyncio.gather(*tasks)
    import collections
    print("audit:", dict(collections.Counter(s.split(':')[0] for _, s in res)))
    for p, s in res:
        if s.startswith("MISLABELED"):
            print("  ", p.split("/")[-1], "->", s)
asyncio.run(main())
