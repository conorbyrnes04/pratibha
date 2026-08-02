#!/usr/bin/env python3
"""Author a unified commentary (+ key terms + cross-tradition resonances) for each
staged Patañjali cluster, grounded in that cluster's own sūtras and the authored
per-sūtra commentary already on file. Operates in-place on the STAGING dir.

    python reauthor_clusters.py --limit 2     # preview, no write
    python reauthor_clusters.py --write       # author all, write staging
"""
import argparse, asyncio, glob, json, os, re, sys
import yaml
sys.path.insert(0, "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha")
from app.llm import smart_chat            # noqa: E402
from app.data_loader import normalize_unit, _as_text  # noqa: E402

STAGE = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha/data/staging/patanjali_clusters"

SYSTEM = """You write publishable study commentary for the Yoga Sūtras of Patañjali, grounded in a SPECIFIC cluster of consecutive sūtras that form one theme.

You are given the numbered translation of the cluster and the existing per-sūtra commentary as raw material. Synthesize ONE unified commentary for the whole cluster — do not repeat per-sūtra; trace the single argument the sūtras build together. State the central move, situate it in the Yoga/Sāṃkhya framework (citta, vṛtti, puruṣa/prakṛti, guṇas, kaivalya as relevant), and draw out the insight in clear, rigorous, unhurried prose — a scholar who also practices. No throat-clearing ("This passage invites us…"), no filler. 900–1600 characters. Keep genuine Sanskrit terms with a brief gloss.

Then give 2–4 key terms (Sanskrit term + one-line gloss) actually present in the cluster.
Then give 2–3 cross-tradition resonances: each a RECOGNIZABLE text/figure with a real parallel idea, and one honest divergence. Use only well-known references you are confident exist (e.g. "Bhagavad Gītā 6.35", "Dhammapada", "Epictetus, Enchiridion", "Meister Eckhart", "Plotinus"). Do not invent citations.

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


async def author_one(path: str, sem: asyncio.Semaphore) -> tuple[str, dict | None]:
    d = yaml.safe_load(open(path))
    user = (f"Cluster: Yoga Sūtras {d.get('sutra_range')} — \"{d.get('title')}\"\n\n"
            f"Translation:\n{_as_text(d.get('translation_literal'))[:1400]}\n\n"
            f"Existing per-sūtra commentary (raw material to synthesize):\n"
            f"{_as_text(d.get('commentary'))[:4000]}\n\nWrite the JSON.")
    async with sem:
        txt = await smart_chat(
            [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
            temperature=0.5, max_tokens=1600)
    txt = re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M).strip()
    try:
        data = json.loads(txt)
    except Exception:
        m = re.search(r"\{.*\}", txt, re.S)
        if not m:
            return path, None
        try:
            data = json.loads(m.group(0))
        except Exception:
            return path, None
    return path, data


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    files = sorted(glob.glob(os.path.join(STAGE, "*.yml")))
    if args.limit:
        files = files[: args.limit]
    sem = asyncio.Semaphore(5)
    results = await asyncio.gather(*(author_one(f, sem) for f in files))

    ok = 0
    for path, data in results:
        d = yaml.safe_load(open(path))
        if not data or not data.get("commentary"):
            print(f"  FAIL  {os.path.basename(path)} (no usable output)")
            continue
        new_comm = build_commentary(data)
        d["commentary"] = new_comm
        d.pop("needs_commentary_reauthor", None)
        norm = normalize_unit(d, "")
        kinds = [L["kind"] for L in norm.get("pratibha_layers", [])]
        nres = sum(len(L.get("items") or []) for L in norm["pratibha_layers"] if L["kind"] == "resonances")
        tier = norm.get("editorial_maturity")
        rich = {"original", "translation", "commentary", "key_terms", "resonances", "practice"} <= set(kinds)
        flag = "RICH" if rich and nres >= 2 else "draft"
        print(f"  {'WROTE' if args.write else 'PREVIEW'} {d['sutra_range']:9} [{tier:8}] {flag} res={nres} kt={'key_terms' in kinds} comm={len(data['commentary'])}c")
        if args.limit and not args.write:
            print("    ---- commentary ----")
            print("   ", data["commentary"][:500].replace("\n", "\n    "), "…")
            print("    key_terms:", [k.get("term") for k in data.get("key_terms", [])])
            print("    resonances:", [r.get("citation") for r in data.get("resonances", [])])
        if args.write:
            with open(path, "w") as fh:
                yaml.safe_dump(d, fh, allow_unicode=True, sort_keys=False, width=120)
        ok += 1
    print(f"\n{'wrote' if args.write else 'previewed'} {ok}/{len(files)} clusters")


if __name__ == "__main__":
    asyncio.run(main())
