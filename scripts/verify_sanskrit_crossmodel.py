#!/usr/bin/env python3
"""Cross-model verification of model-supplied Sanskrit. For each self-sourced unit,
Luna (a different model from the Terra author) independently checks the stored
IAST against the received text. On confident correction, apply it (regenerate
Devanagari) and note it; on agreement, upgrade provenance to cross-model-verified;
on uncertainty, keep the PD-pending flag and record a review note. Resumable."""
import argparse, asyncio, glob, json, os, re, sys
import yaml
sys.path.insert(0, "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iast_to_deva import iast_to_deva
from app.llm import smart_chat
from app.data_loader import _as_text

DIG = str.maketrans("0123456789", "०१२३४५६७८९")
# self-sourced Sanskrit collections + a readable name for the prompt
COLLS = {
    "katha_upanishad": "Kaṭha Upaniṣad", "brihadaranyaka_upanishad": "Bṛhadāraṇyaka Upaniṣad",
    "mundaka_upanishad": "Muṇḍaka Upaniṣad", "isavasya_upanishad": "Īśāvāsya Upaniṣad",
    "svetasvatara_upanishad": "Śvetāśvatara Upaniṣad", "astavakra_gita": "Aṣṭāvakra Gītā",
    "mandukya_upanishad_and_gaudapada_karika": "Māṇḍūkya Upaniṣad / Gauḍapāda Kārikā",
}

SYS = ("You are a Sanskrit textual scholar verifying a single verse against the RECEIVED (critical/traditional) text. "
       "You are given a work, a reference, and an IAST verse. Judge ONLY whether the Sanskrit wording is accurate to "
       "the received text of that specific verse.\n"
       'Return ONLY JSON: {"verdict":"correct"|"corrected"|"uncertain","corrected_iast":"<full corrected IAST if verdict=corrected, else empty>","note":"<short reason>"}\n'
       "Use verdict=correct only if the wording matches the received text (minor sandhi/spacing aside). "
       "Use verdict=corrected only if you are confident of the exact correct wording. "
       "Use verdict=uncertain if you cannot verify the exact wording.")


async def verify(path, coll_name, sem, force):
    d = yaml.safe_load(open(path))
    prov = d.get("provenance") if isinstance(d.get("provenance"), dict) else {}
    if not force and prov.get("verification"):
        return path, "skip"
    iast = _as_text(d.get("sanskrit_iast"))
    if not iast:
        return path, "no-iast"
    ref = _as_text(d.get("source_verse")) or _as_text(d.get("source_id"))
    body = re.sub(r"\s*\|\|.*", "", iast).replace("\n", " ").strip()
    async with sem:
        r = None
        for attempt in range(3):
            try:
                r = await smart_chat([{"role": "system", "content": SYS},
                                      {"role": "user", "content": f"Work: {coll_name}\nReference: {ref}\nIAST to verify:\n{body}\n\nReturn JSON."}],
                                     primary_model="openai/gpt-5.6-luna", temperature=0.0, max_tokens=500)
                break
            except Exception:
                await asyncio.sleep(2 * (attempt + 1))
        if r is None:
            return path, "ERR"
    m = re.search(r"\{.*\}", re.sub(r"^```(?:json)?|```$", "", r.strip(), flags=re.M), re.S)
    try:
        v = json.loads(m.group(0))
    except Exception:
        return path, "parse"
    verdict = v.get("verdict", "uncertain")
    prov["verification"] = f"cross-model (Luna): {verdict}"
    if v.get("note"):
        prov["verification_note"] = v["note"][:200]
    if verdict == "corrected" and v.get("corrected_iast", "").strip():
        seg = re.search(r"\|\|\s*([\d.]+)\s*\|\|", iast)
        segn = seg.group(1) if seg else ""
        parts = [p.strip() for p in re.split(r"[/|]", v["corrected_iast"]) if p.strip()]
        d["sanskrit_iast"] = " |\n".join(parts) + (f" || {segn} ||" if segn else "")
        d["sanskrit_devanagari"] = " ।\n".join(iast_to_deva(p) for p in parts) + (f" ॥ {segn.translate(DIG)} ॥" if segn else "")
        prov["sanskrit_source"] = re.sub(r"model-supplied[^;]*", "cross-model corrected (Luna)", _as_text(prov.get("sanskrit_source", "")))
    d["provenance"] = prov
    yaml.safe_dump(d, open(path, "w"), allow_unicode=True, sort_keys=False, width=120)
    return path, verdict


async def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--write", action="store_true")
    ap.parse_args()
    sem = asyncio.Semaphore(3)
    tasks = []
    for coll, name in COLLS.items():
        for path in glob.glob(f"/Users/conorbyrnes04/Documents/Projects/VAK/pratibha/data/canonical/{coll}/*.yml"):
            d = yaml.safe_load(open(path))
            prov = d.get("provenance") or {}
            # only the model-supplied units (skip pre-existing / already-PD)
            if "model-supplied" in str(prov.get("sanskrit_source", "")) or "2026" in str(prov.get("english_source", "")):
                tasks.append(verify(path, name, sem, True))
    res = await asyncio.gather(*tasks)
    import collections
    print("verification outcomes:", dict(collections.Counter(v for _, v in res)))


if __name__ == "__main__":
    asyncio.run(main())
