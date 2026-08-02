#!/usr/bin/env python3
"""Create new full-scaffold MMK units for the Luna-selected canonical verses.
Sanskrit from GRETIL (PD IAST) + Devanagari (transliterated). Terra authors a
faithful translation + commentary + key terms + cross-tradition resonances +
practice, grounded in the verse. New units use flat fields only (no explicit
pratibha_layers), so everything derives cleanly. Writes to staging."""
import argparse, asyncio, json, os, re, sys
import yaml
sys.path.insert(0, "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iast_to_deva import iast_to_deva
from app.llm import smart_chat
from app.data_loader import normalize_unit

SP = os.path.dirname(os.path.abspath(__file__))
STAGE = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha/data/staging/mmk_new"
verses = json.load(open(f"{SP}/mmk_verses.json"))
add = json.load(open(f"{SP}/mmk_add.json"))
DIG = str.maketrans("0123456789", "०१२३४५६७८९")

SYS = """You author a full study unit for a single verse of Nāgārjuna's Mūlamadhyamakakārikā (MMK), grounded in the Sanskrit (IAST) given.

Produce, all faithful to THIS verse and Madhyamaka thought (emptiness/śūnyatā, dependent origination/pratītyasamutpāda, svabhāva critique, two truths, the tetralemma):
- title: a short evocative English title (no verse number).
- translation: faithful, spare, aphoristic English of the verse; pivotal Sanskrit terms glossed in parentheses. Work from THIS text, do not paraphrase a famous rendering.
- commentary: 700-1200 chars unpacking the verse's dialectical move and why it matters. Rigorous, unhurried, no filler.
- key_terms: 2-4 (Sanskrit term + one-line gloss) present in the verse.
- resonances: 2-3 cross-tradition parallels, each a RECOGNIZABLE text/figure with a real parallel + one honest divergence. No invented citations.
- practice: one concrete contemplative instruction (2-3 sentences) distilled from the verse.

Return ONLY JSON with those keys."""


def dev_of(iast):
    parts = [p.strip() for p in iast.split("/") if p.strip()]
    return " ।\n".join(iast_to_deva(p) for p in parts)


async def one(ref, sem):
    iast = re.sub(r"\s+", " ", verses[ref]).strip(" /")
    async with sem:
        try:
            txt = await smart_chat([{"role": "system", "content": SYS},
                                    {"role": "user", "content": f"MMK {ref}, IAST:\n{iast}\n\nReturn the JSON."}],
                                   primary_model="openai/gpt-5.6-terra", temperature=0.4, max_tokens=1500)
        except Exception as e:
            return ref, None, str(e)[:70]
    m = re.search(r"\{.*\}", re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M), re.S)
    try:
        return ref, json.loads(m.group(0)), None
    except Exception:
        return ref, None, "parse"


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


async def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--write", action="store_true"); ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    refs = add[: args.limit] if args.limit else add
    if args.write:
        os.makedirs(STAGE, exist_ok=True)
    sem = asyncio.Semaphore(5)
    results = await asyncio.gather(*(one(r, sem) for r in refs))
    ok = rich = 0
    for ref, data, err in results:
        if not data:
            print(f"  FAIL {ref} {err}"); continue
        ch, v = ref.split(".")
        iast = re.sub(r"\s+", " ", verses[ref]).strip(" /")
        parts = [p.strip() for p in iast.split("/") if p.strip()]
        unit = {
            "source_id": f"MMK_{int(ch):02d}_{int(v):02d}", "category": "root_text",
            "work_id": "nagarjuna_mulamadhyamakakarika", "work_title": "Nagarjuna Mulamadhyamakakarika",
            "unit_id": f"nagarjuna_mulamadhyamakakarika.mmk_{int(ch):02d}_{int(v):02d}",
            "unit_label": data["title"], "title": data["title"], "unit_type": "verse",
            "sanskrit_devanagari": dev_of(iast) + f" ॥ {str(ch).translate(DIG)}.{str(v).translate(DIG)} ॥",
            "sanskrit_iast": " |\n".join(parts) + f" || {ch}.{v} ||",
            "translation_literal": data["translation"], "commentary": build_commentary(data),
            "practice": data["practice"], "themes": [], "tags": [],
            "provenance": {"collection": "Nagarjuna Mulamadhyamakakarika",
                           "sanskrit_source": f"GRETIL MMK {ref} (PD); Devanagari from IAST.",
                           "english_source": "Pratibha own rendering from the Sanskrit (2026)."},
        }
        nm = normalize_unit(unit, "")
        is_rich = nm["editorial_maturity"] in ("rich", "polished")
        rich += is_rich; ok += 1
        print(f"  MMK {ref} [{nm['editorial_maturity']}] '{data['title']}'")
        if args.limit and not args.write:
            print("     ", data["translation"][:90])
        if args.write:
            with open(os.path.join(STAGE, f"nagarjuna_mulamadhyamakakarika_mmk_{int(ch):02d}_{int(v):02d}.yml"), "w") as fh:
                yaml.safe_dump(unit, fh, allow_unicode=True, sort_keys=False, width=120)
    print(f"\n{'wrote' if args.write else 'previewed'} {ok} | rich {rich}")


if __name__ == "__main__":
    asyncio.run(main())
