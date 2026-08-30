#!/usr/bin/env python3
"""Authoring enrichment for the newly-ingested living-tradition collections
(Eastman, Zitkála-Šá, Yoruba proverbs). These units carry only sourced text, so
this pass AUTHORS commentary + practice and appends key_terms / resonances —
never touching the source layer.

Cultural posture: humble, interpretive study apparatus for LIVING traditions,
not an authoritative voice. No invented ethnographic claims, no invented
citations. Writes to data/staging/enrich/<collection>/; promote with --promote.
"""
import argparse, asyncio, glob, json, os, re, sys
import yaml

ROOT = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha"
sys.path.insert(0, ROOT)
from app.llm import smart_chat  # noqa
from app.data_loader import normalize_unit, _as_text  # noqa

CANON = os.path.join(ROOT, "data/canonical")
STAGE = os.path.join(ROOT, "data/staging/enrich")
TARGETS = ["eastman_soul_of_the_indian", "zitkala_sa_old_indian_legends", "yoruba_proverbs"]

SYSTEM = """You write short study apparatus for a passage from a LIVING wisdom tradition (Native American or Yoruba). Posture: humble and interpretive. This is offered to students as a study reading, NOT an authoritative account of the tradition. Respect that living communities hold this knowledge.

Rules:
- Ground everything in the GIVEN passage. Do not add ethnographic "facts", ritual details, or claims about the tradition that are not present in the text. When you interpret, interpret the passage's meaning, not the whole culture.
- Never invent a citation, book, or verse number. Use only well-known texts/figures you are confident exist.
- No exoticizing or romanticizing ("noble savage", "ancient mystical wisdom" clichés). Plain, respectful, precise.

Produce JSON only:
{
 "commentary": "2-4 sentences illuminating what THIS passage says and why it matters, interpretively.",
 "practice": "one short contemplative application a reader can do today.",
 "key_terms": [{"term":"...","definition":"..."}],   // 0-3; ONLY genuine terms actually in the passage (e.g. a Yoruba word, or 'the Great Mystery'). Empty list if none — do not fabricate.
 "resonances": [{"citation":"...","resonance":"...","divergence":"..."}]  // 2-3 parallels to RECOGNIZABLE texts (e.g. Tao Te Ching, Heraclitus, Dhammapada, Ecclesiastes, Meister Eckhart), each with one honest divergence.
}"""


def append_tail(commentary: str, kts, res) -> str:
    out = (commentary or "").rstrip()
    if kts:
        out += "\n\n\nKey Terms\n\n\n" + "\n".join(
            f"**{k['term']}** — {k['definition']}" for k in kts if k.get("term") and k.get("definition"))
    if res:
        out += "\n\n\nCross-Tradition Resonances\n\n\n" + "\n\n".join(
            f"**{r['citation']}:** {r.get('resonance','')} Divergence: {r.get('divergence','')}"
            for r in res if r.get("citation"))
    return out


async def enrich_one(path, sem):
    d = yaml.safe_load(open(path))
    norm = normalize_unit(d, path)
    coll = _as_text(norm.get("collection"))
    note = ((d.get("provenance") or {}).get("cultural_context") or "")
    # The sourced text is in either the original (English-authored) or translation layer.
    text = ""
    for L in norm.get("pratibha_layers", []):
        if L.get("kind") in ("original", "translation") and L.get("body"):
            text = L["body"]; break
    if not text:
        return path, {"_skip": "no-text"}
    user = (f"Tradition / collection: {coll}\nContext: {note}\n\nPassage:\n{text[:2600]}\n\nReturn the JSON.")
    async with sem:
        try:
            txt = await smart_chat([{"role": "system", "content": SYSTEM},
                                    {"role": "user", "content": user}], temperature=0.4, max_tokens=1100)
        except Exception as e:
            return path, {"_error": str(e)[:100]}
    m = re.search(r"\{.*\}", re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M), re.S)
    if not m:
        return path, {"_error": "no-json"}
    try:
        return path, json.loads(m.group(0))
    except Exception as e:
        return path, {"_error": f"bad-json {e}"[:60]}


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--collection", default="", help="substring filter")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    files = []
    for slug in TARGETS:
        if args.collection and args.collection not in slug:
            continue
        files += sorted(glob.glob(os.path.join(CANON, slug, "*.yml")))
    if args.limit:
        files = files[: args.limit]
    print(f"units in scope: {len(files)}")

    sem = asyncio.Semaphore(5)
    results = await asyncio.gather(*(enrich_one(p, sem) for p in files))

    ok = fail = 0
    for path, data in results:
        if not data or data.get("_error") or data.get("_skip"):
            fail += 1
            if data and data.get("_error"):
                print("  ERR", os.path.basename(path), data["_error"])
            continue
        commentary = (data.get("commentary") or "").strip()
        practice = (data.get("practice") or "").strip()
        kts = [k for k in data.get("key_terms", []) if isinstance(k, dict) and k.get("term")]
        res = [r for r in data.get("resonances", []) if isinstance(r, dict) and r.get("citation")]
        if not commentary or len(res) < 1:
            fail += 1; continue
        ok += 1
        if not args.limit or args.write:
            d = yaml.safe_load(open(path))
            d["commentary"] = append_tail(commentary, kts, res)
            if practice:
                d["abhyasa"] = practice
                d["practice"] = practice
            d["enriched"] = True
            if args.write:
                rel = os.path.relpath(path, CANON)
                dest = os.path.join(STAGE, rel)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest, "w") as fh:
                    yaml.safe_dump(d, fh, allow_unicode=True, sort_keys=False, width=120)
        if args.limit and not args.write:
            print(f"  {os.path.basename(path)}\n    COMM: {commentary[:110]}\n    RES: {[r['citation'] for r in res]}")
    print(f"\n{'wrote' if args.write else 'previewed'} {ok} | failed {fail}")


def promote():
    n = 0
    for src in glob.glob(os.path.join(STAGE, "*", "*.yml")):
        rel = os.path.relpath(src, STAGE)
        dst = os.path.join(CANON, rel)
        if any(t in rel for t in TARGETS):
            yaml.safe_dump(yaml.safe_load(open(src)), open(dst, "w"), allow_unicode=True, sort_keys=False, width=120)
            n += 1
    print(f"promoted {n} units to canonical")


if __name__ == "__main__":
    if "--promote" in sys.argv:
        promote()
    else:
        asyncio.run(main())
