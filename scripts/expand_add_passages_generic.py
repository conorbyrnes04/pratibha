#!/usr/bin/env python3
"""Config-driven expansion: add canonical passages to an under-sampled text.
Luna selects (research), Terra authors (writing), grounded in GRETIL PD Sanskrit.
New units use flat fields only. Stages to data/staging/<work>_new. Resumable."""
import argparse, asyncio, json, os, re, sys
import yaml
sys.path.insert(0, "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iast_to_deva import iast_to_deva
from app.llm import smart_chat
from app.data_loader import normalize_unit

SP = os.path.dirname(os.path.abspath(__file__))
DIG = str.maketrans("0123456789", "०१२३४५६७८९")

CFG = {
    "bca": dict(work_id="shantideva_bodhicaryavatara", work_title="Shantideva Bodhicaryavatara",
                coll="Shantideva Bodhicaryavatara", verses="bca_verses.json", have=[],
                idfmt="bca", context="Śāntideva's Bodhicaryāvatāra (the bodhisattva path: bodhicitta, the six perfections, patience, wisdom/emptiness)",
                n=17),
    "chandogya": dict(work_id="chāndogya_upaniṣad", work_title="Chāndogya Upaniṣad",
                coll="Chāndogya Upaniṣad", verses="chandogya_verses.json", have=[],
                idfmt="chu", context="the Chāndogya Upaniṣad (tat tvam asi, the Self, Brahman, the udgītha)", n=13),
    "katha": dict(work_id="katha_upanishad", work_title="Katha Upanishad",
                  coll="Katha Upanishad", verses="katha_verses.json", have=[],
                  idfmt="ku", context="the Kaṭha Upaniṣad (Naciketas and Death, the two paths, the Self as rider of the chariot)", n=11),
}

SEL_SYS = ("You are a scholar selecting canonical passages from {ctx} for a world-wisdom corpus. "
           "Given verses ALREADY included and the available verse refs, pick the ~{n} MOST essential "
           "additional passages any serious reader expects, spread across the text, avoiding redundancy. "
           'Return ONLY JSON: {{"add":["1.1",...],"rationale":{{"1.1":"why"}}}}')

AUTH_SYS = """You author a full study unit for a single passage of {ctx}, grounded in the Sanskrit (IAST) given.
Produce, faithful to THIS passage:
- title: short evocative English title (no numbers).
- translation: faithful, spare English; pivotal Sanskrit terms glossed in parentheses. Work from THIS text.
- commentary: 700-1200 chars, rigorous, no filler.
- key_terms: 2-4 (term + one-line gloss) present in the passage.
- resonances: 2-3 cross-tradition parallels (recognizable text/figure + real parallel + one honest divergence). No invented citations.
- practice: one concrete contemplative instruction (2-3 sentences).
Return ONLY JSON with those keys."""


def clean_verse(iast):
    iast = re.sub(r"(?i)pariccheda\s+\d+\s*", "", iast)
    iast = re.sub(r"(?i)^\s*(?:aum|oṃ)\s+namo[^|/]*[|/]\s*", "", iast)
    iast = re.sub(r"=[0-9A-F]{2}", "'", iast)
    return re.sub(r"\s+", " ", iast).strip(" /|")


def build_commentary(d):
    out = d["commentary"].strip()
    kts = [k for k in d.get("key_terms", []) if isinstance(k, dict) and k.get("term")]
    if kts:
        out += "\n\nKey Terms\n\n" + "\n".join(
            f"**{k['term']}** — {(k.get('definition') or k.get('gloss') or '').strip()}" for k in kts[:4])
    res = [r for r in d.get("resonances", []) if isinstance(r, dict) and (r.get("citation") or r.get("parallel"))]
    if res:
        lines = []
        for r in res[:3]:
            cite = (r.get("citation") or r.get("parallel") or "").strip()
            body = (r.get("resonance") or r.get("connection") or "").strip()
            if r.get("divergence", "").strip():
                body += f" Divergence: {r['divergence'].strip()}"
            lines.append(f"**{cite}:** {body}")
        out += "\n\nCross-Tradition Resonances\n\n" + "\n".join(lines)
    return out


async def author(cfg, ref, iast, sem):
    async with sem:
        try:
            txt = await smart_chat([{"role": "system", "content": AUTH_SYS.format(ctx=cfg["context"])},
                                    {"role": "user", "content": f"Passage {ref}, IAST:\n{iast}\n\nReturn the JSON."}],
                                   primary_model="openai/gpt-5.6-terra", temperature=0.4, max_tokens=1500)
        except Exception as e:
            return ref, None, str(e)[:60]
    m = re.search(r"\{.*\}", re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M), re.S)
    try:
        return ref, json.loads(m.group(0)), None
    except Exception:
        return ref, None, "parse"


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True, choices=list(CFG))
    ap.add_argument("--select", action="store_true")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    cfg = CFG[args.work]
    verses = {k: clean_verse(v) for k, v in json.load(open(os.path.join(SP, cfg["verses"]))).items()}
    verses = {k: v for k, v in verses.items() if 12 < len(v) < 320}
    add_path = os.path.join(SP, f"{args.work}_add.json")

    if args.select:
        avail = [k for k in verses if k not in cfg["have"]]
        r = await smart_chat([{"role": "system", "content": SEL_SYS.format(ctx=cfg["context"], n=cfg["n"])},
                              {"role": "user", "content": f"Included: {cfg['have']}\nAvailable: {avail}\nSelect ~{cfg['n']}."}],
                             primary_model="openai/gpt-5.6-luna", temperature=0.2, max_tokens=1500)
        d = json.loads(re.search(r"\{.*\}", re.sub(r"^```(?:json)?|```$", "", r.strip(), flags=re.M), re.S).group(0))
        picks = [k for k in d["add"] if k in verses]
        json.dump(picks, open(add_path, "w"))
        print(f"{args.work}: Luna selected {len(picks)} (valid):")
        for k in picks:
            print(f"  {k}: {d.get('rationale', {}).get(k, '')[:55]}")
        return

    add = [k for k in json.load(open(add_path)) if k in verses]
    stage = f"/Users/conorbyrnes04/Documents/Projects/VAK/pratibha/data/staging/{args.work}_new"
    if args.write:
        os.makedirs(stage, exist_ok=True)
    sem = asyncio.Semaphore(5)
    res = await asyncio.gather(*(author(cfg, r, verses[r], sem) for r in add))
    ok = rich = 0
    for ref, data, err in res:
        if not data:
            print(f"  FAIL {ref} {err}"); continue
        parts = [p.strip() for p in re.split(r"[/|]", verses[ref]) if p.strip()]
        secs = ref.replace(".", "_")
        mk = f"{cfg['idfmt']}_" + "_".join(f"{int(x):02d}" for x in ref.split("."))
        unit = {
            "source_id": mk.upper(), "category": "root_text", "work_id": cfg["work_id"], "work_title": cfg["work_title"],
            "unit_id": f"{cfg['work_id']}.{mk}", "unit_label": data["title"], "title": data["title"], "unit_type": "verse",
            "sanskrit_devanagari": " ।\n".join(iast_to_deva(p) for p in parts) + f" ॥ {ref.translate(DIG)} ॥",
            "sanskrit_iast": " |\n".join(parts) + f" || {ref} ||",
            "translation_literal": data["translation"], "commentary": build_commentary(data),
            "practice": data["practice"], "themes": [], "tags": [],
            "provenance": {"collection": cfg["coll"], "sanskrit_source": f"GRETIL {cfg['work_title']} {ref} (PD); Devanagari from IAST.",
                           "english_source": "Pratibha own rendering from the Sanskrit (2026)."},
        }
        nm = normalize_unit(unit, "")
        is_rich = nm["editorial_maturity"] in ("rich", "polished"); rich += is_rich; ok += 1
        print(f"  {args.work} {ref} [{nm['editorial_maturity']}] '{data['title']}'")
        if args.write:
            with open(os.path.join(stage, f"{cfg['work_id']}_{mk}.yml"), "w") as fh:
                yaml.safe_dump(unit, fh, allow_unicode=True, sort_keys=False, width=120)
    print(f"\n{args.work}: {'wrote' if args.write else 'previewed'} {ok} | rich {rich}")


if __name__ == "__main__":
    asyncio.run(main())
