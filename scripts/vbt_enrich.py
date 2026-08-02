#!/usr/bin/env python3
"""Enrich each VBT yukti to `rich`: unified commentary + key terms + cross-tradition
resonances, grounded in the fresh translation + attached Sanskrit. Resumable;
operates on the staged VBT files. Writes commentary with the section tail the
loader parses into key_terms / resonances layers."""
import argparse, asyncio, glob, json, os, re, sys
import yaml
sys.path.insert(0, "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha")
from app.llm import smart_chat          # noqa
from app.data_loader import normalize_unit, _as_text  # noqa

STAGE = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha/data/staging/vbt_sanskrit"

SYSTEM = """You write publishable study commentary for a single dhāraṇā (centering technique) of the Vijñāna Bhairava — the Kashmir Śaiva text of 112 methods for entering Bhairava-consciousness.

You are given the verse's IAST, a faithful English translation, and its yukti number. Write commentary that unpacks THIS technique: what the practitioner actually does, the mechanism by which it dissolves the contracted self and opens the expansive state (bhairava-samāveśa), and where it sits in the Trika view (prāṇa/śakti, madhya/the Center, vikalpa vs nirvikalpa, the Void). Clear, rigorous, unhurried — a scholar who also practices. No throat-clearing, no filler. 700–1300 characters. Keep genuine Sanskrit terms with a brief gloss.

Then 2–4 key terms (Sanskrit term + one-line gloss) actually in the verse.
Then 2–3 cross-tradition resonances: each a RECOGNIZABLE text/figure with a real parallel in contemplative practice, plus one honest divergence. Use only references you are confident exist (e.g. "Dhyāna in the Yoga Sūtras 3.2", "Dzogchen rushen", "Plotinus, Enneads VI.9", "The Cloud of Unknowing", "Zhuangzi, 'fasting of the heart'"). Do not invent citations.

Return ONLY JSON:
{"commentary":"...", "key_terms":[{"term":"...","definition":"..."}], "resonances":[{"citation":"...","resonance":"...","divergence":"..."}]}"""


def build_commentary(data: dict) -> str:
    parts = [data.get("commentary", "").strip()]
    kts = [k for k in data.get("key_terms", []) if isinstance(k, dict) and k.get("term")]
    if kts:
        parts.append("\n\nKey Terms\n\n" + "\n".join(
            f"**{k['term']}** — {k.get('definition','').strip()}" for k in kts[:4]))
    res = [r for r in data.get("resonances", []) if isinstance(r, dict) and r.get("citation")]
    if res:
        lines = []
        for r in res[:3]:
            body = r.get("resonance", "").strip()
            if r.get("divergence", "").strip():
                body += f" Divergence: {r['divergence'].strip()}"
            lines.append(f"**{r['citation'].strip()}:** {body}")
        parts.append("\n\nCross-Tradition Resonances\n\n" + "\n".join(lines))
    return "".join(parts)


async def enrich_one(path: str, sem: asyncio.Semaphore, force: bool) -> tuple[str, dict | None]:
    d = yaml.safe_load(open(path))
    if not force and d.get("enriched"):
        return path, {"_skip": True}
    n = re.search(r"yukti_(\d+)", path).group(1)
    user = (f"Yukti #{int(n)} (verse {d.get('source_verse')}).\n"
            f"IAST: {_as_text(d.get('sanskrit_iast'))}\n"
            f"Translation: {_as_text(d.get('translation_literal'))}\n\nWrite the JSON.")
    async with sem:
        try:
            txt = await smart_chat(
                [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
                temperature=0.5, max_tokens=1400)
        except Exception as e:
            return path, {"_error": str(e)[:80]}
    txt = re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M).strip()
    m = re.search(r"\{.*\}", txt, re.S)
    if not m:
        return path, None
    try:
        return path, json.loads(m.group(0))
    except Exception:
        return path, None


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    files = sorted(glob.glob(os.path.join(STAGE, "*.yml")))
    if args.limit:
        files = files[: args.limit]
    sem = asyncio.Semaphore(5)
    results = await asyncio.gather(*(enrich_one(f, sem, args.force) for f in files))

    ok = rich = skip = fail = 0
    for path, data in results:
        if data and data.get("_skip"):
            skip += 1; continue
        n = re.search(r"yukti_(\d+)", path).group(1)
        if not data or not data.get("commentary") or data.get("_error"):
            fail += 1; print(f"  FAIL yukti {n} {data.get('_error','') if data else ''}"); continue
        d = yaml.safe_load(open(path))
        d["commentary"] = build_commentary(data)
        d["enriched"] = True
        norm = normalize_unit(d, path)
        kinds = {L["kind"] for L in norm["pratibha_layers"]}
        nres = sum(len(L.get("items") or []) for L in norm["pratibha_layers"] if L["kind"] == "resonances")
        is_rich = {"original", "translation", "commentary", "key_terms", "resonances", "practice"} <= kinds and nres >= 2
        rich += is_rich
        print(f"  {'WROTE' if args.write else 'PREVIEW'} yukti {n} [{norm['editorial_maturity']}] {'RICH' if is_rich else '...'} res={nres}")
        if args.limit and not args.write:
            print("    ", data["commentary"][:300].replace("\n", " "), "…")
            print("    KT:", [k.get("term") for k in data.get("key_terms", [])], "| RES:", [r.get("citation") for r in data.get("resonances", [])])
        if args.write:
            with open(path, "w") as fh:
                yaml.safe_dump(d, fh, allow_unicode=True, sort_keys=False, width=120)
        ok += 1
    print(f"\n{'wrote' if args.write else 'previewed'} {ok} | rich {rich} | skipped {skip} | failed {fail}")


if __name__ == "__main__":
    asyncio.run(main())
