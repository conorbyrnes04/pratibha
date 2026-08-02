#!/usr/bin/env python3
"""Safe enrichment wave: for draft units that already have source + a good
translation + AUTHORED commentary but lack key terms / cross-tradition
resonances, generate just those two and APPEND them (preserving the existing
commentary) so the unit reaches `rich`. Never rewrites authored prose.

Reads canonical, writes to data/staging/enrich/<collection>/ (promote = copy back).
Resumable, per-collection, low temperature. Grounded in the unit's own content.
"""
import argparse, asyncio, glob, json, os, re, sys
import yaml
sys.path.insert(0, "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha")
from app.llm import smart_chat          # noqa
from app.data_loader import (normalize_unit, _as_text, _daily_present_layers,   # noqa
                             _daily_resonance_count, _daily_translation_len)

ROOT = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha"
CANON = os.path.join(ROOT, "data/canonical")
STAGE = os.path.join(ROOT, "data/staging/enrich")

SYSTEM = """You add scholarly apparatus to an ALREADY-WRITTEN study passage. You are given a source tradition, a translation, and existing commentary. Do NOT rewrite them. Produce only:

- key_terms: 2–4 pivotal terms in the passage's OWN language (Sanskrit, Pāli, Greek, Chinese, Arabic…) with a one-line gloss. Use the correct source-language term with diacritics; if the passage is Chinese/Greek give the romanization + script where you are confident.
- resonances: 2–3 cross-tradition parallels. Each names a RECOGNIZABLE text/figure with a genuine parallel idea and one honest divergence. Use only references you are confident exist; never invent a citation or verse number you are unsure of.

Ground everything in the given passage — no generic filler. Return ONLY JSON:
{"key_terms":[{"term":"...","definition":"..."}], "resonances":[{"citation":"...","resonance":"...","divergence":"..."}]}"""


def needs(v):
    p = _daily_present_layers(v)
    return ("key_terms" not in p) or (_daily_resonance_count(v) < 2)


def eligible(v):
    p = _daily_present_layers(v)
    return ("original" in p and _daily_translation_len(v) >= 120
            and "commentary" in p and needs(v))


def append_tail(commentary: str, data: dict) -> str:
    out = commentary.rstrip()
    kts = [k for k in data.get("key_terms", []) if isinstance(k, dict) and k.get("term")]
    res = [r for r in data.get("resonances", []) if isinstance(r, dict) and r.get("citation")]
    if kts:
        out += "\n\nKey Terms\n\n" + "\n".join(
            f"**{k['term']}** — {k.get('definition','').strip()}" for k in kts[:4])
    if res:
        lines = []
        for r in res[:3]:
            body = r.get("resonance", "").strip()
            if r.get("divergence", "").strip():
                body += f" Divergence: {r['divergence'].strip()}"
            lines.append(f"**{r['citation'].strip()}:** {body}")
        out += "\n\nCross-Tradition Resonances\n\n" + "\n".join(lines)
    return out


async def enrich_one(path: str, sem, force):
    d = yaml.safe_load(open(path))
    norm = normalize_unit(d, path)
    if not eligible(norm):
        return path, {"_skip": "not-eligible"}
    coll = _as_text(norm.get("collection"))
    comm = _as_text(norm.get("commentary"))
    trans = _as_text(norm.get("translation"))
    user = (f"Tradition: {coll}\nTranslation: {trans[:700]}\n"
            f"Existing commentary (do not rewrite): {comm[:1500]}\n\nReturn the JSON.")
    async with sem:
        try:
            txt = await smart_chat([{"role": "system", "content": SYSTEM},
                                    {"role": "user", "content": user}], temperature=0.4, max_tokens=900)
        except Exception as e:
            return path, {"_error": str(e)[:80]}
    m = re.search(r"\{.*\}", re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M), re.S)
    if not m:
        return path, None
    try:
        return path, json.loads(m.group(0))
    except Exception:
        return path, None


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--collection", default="", help="substring filter on dir name")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    files = []
    for path in sorted(glob.glob(os.path.join(CANON, "*", "*.yml"))):
        if args.collection and args.collection.lower() not in path.lower():
            continue
        files.append(path)
    # pre-filter to eligible to avoid wasting calls
    todo = []
    for p in files:
        try:
            if eligible(normalize_unit(yaml.safe_load(open(p)), p)):
                todo.append(p)
        except Exception:
            pass
    if args.limit:
        todo = todo[: args.limit]
    print(f"eligible units in scope: {len(todo)}")
    sem = asyncio.Semaphore(5)
    results = await asyncio.gather(*(enrich_one(p, sem, args.write) for p in todo))

    ok = rich = fail = 0
    for path, data in results:
        if data and (data.get("_skip") or data.get("_error")):
            if data.get("_error"):
                fail += 1; print("  ERR", os.path.basename(path), data["_error"])
            continue
        if not data or not (data.get("key_terms") or data.get("resonances")):
            fail += 1; continue
        d = yaml.safe_load(open(path))
        d["commentary"] = append_tail(_as_text(normalize_unit(d, path).get("commentary")), data)
        d["enriched"] = True
        norm = normalize_unit(d, path)
        kinds = {L["kind"] for L in norm["pratibha_layers"]}
        nres = sum(len(L.get("items") or []) for L in norm["pratibha_layers"] if L["kind"] == "resonances")
        is_rich = {"original", "translation", "commentary", "key_terms", "resonances", "practice"} <= kinds and nres >= 2
        rich += is_rich; ok += 1
        if args.write:
            rel = os.path.relpath(path, CANON)
            dest = os.path.join(STAGE, rel)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "w") as fh:
                yaml.safe_dump(d, fh, allow_unicode=True, sort_keys=False, width=120)
        if args.limit and not args.write:
            print(f"  {os.path.basename(path)} [{norm['editorial_maturity']}] {'RICH' if is_rich else '..'}",
                  "KT", [k.get("term") for k in data.get("key_terms", [])],
                  "RES", [r.get("citation") for r in data.get("resonances", [])])
    print(f"\n{'wrote' if args.write else 'previewed'} {ok} | ->rich {rich} | failed {fail}")


if __name__ == "__main__":
    asyncio.run(main())
