#!/usr/bin/env python3
"""Faithful re-translation of the 43 Patañjali clusters FROM the Sanskrit (IAST).
Replaces the lifeless auto-generated literal glosses with renderings that keep
the sūtra's aphoristic force, terms glossed, dignified-but-modern register
(cross-checked against Woods 1914, PD — never copied). Per-sūtra, preserving the
**N.M** numbering. Writes translation_literal on the flat field (PYS clusters
have no explicit pratibha_layers, so it serves directly). Resumable."""
import argparse, asyncio, glob, json, os, re, sys
import yaml
sys.path.insert(0, "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha")
from app.llm import smart_chat          # noqa
from app.data_loader import _as_text     # noqa

CANON = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha/data/canonical/patañjali_yoga_sūtras"

SYSTEM = """You are a scholar-translator of the Yoga Sūtras of Patañjali, rendering a thematic cluster of sūtras from the Sanskrit (IAST).

The existing translations are flat, mechanical parse-glosses ("In that state, effort is practice"). Replace them with FAITHFUL, LIVING English that carries the sūtra's aphoristic compression and precision — the register of a translator who knows both the grammar and the practice. Dignified and clear, never archaic, never padded.

Rules:
- Translate ONLY what the Sanskrit says — this is a terse aphoristic text; do not inflate it into a paraphrase or sermon. Faithful and spare, but alive.
- Render EACH sūtra separately, prefixed exactly "**C.N** " (e.g. "**1.13** ").
- Keep pivotal Sanskrit terms in parentheses after the English on first use (e.g. "practice (abhyāsa)", "dispassion (vairāgya)", "the seer (draṣṭṛ)").
- Work from THIS text. You may cross-check your accuracy against the standard scholarly reading (Woods 1914) but never copy its Victorian wording.
- If a compound is genuinely ambiguous, choose the reading the tradition favors; note nothing in the output.

Return ONLY JSON: {"sutras": {"1.12": "english...", "1.13": "english...", ...}, "confidence": "high|medium|low"}"""


def parse_iast(text):
    out = {}
    parts = re.split(r"\|\|\s*([\d.]+)\s*\|\|", text)
    buf = parts[0]; i = 1
    while i < len(parts):
        out[parts[i].strip()] = re.sub(r"\s+", " ", buf).strip(); buf = parts[i+1] if i+1 < len(parts) else ''; i += 2
    return out


async def translate_cluster(path, sem, force):
    d = yaml.safe_load(open(path))
    if not force and d.get("translation_confidence"):
        return path, {"_skip": True}
    sutras = parse_iast(_as_text(d.get("sanskrit_iast")))
    if not sutras:
        return path, None
    listing = "\n".join(f"{k}: {v}" for k, v in sutras.items())
    async with sem:
        try:
            txt = await smart_chat([{"role": "system", "content": SYSTEM},
                                    {"role": "user", "content": f"Cluster {d.get('sutra_range')}:\n{listing}\n\nReturn the JSON."}],
                                   temperature=0.4, max_tokens=1200)
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
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    files = sorted(glob.glob(os.path.join(CANON, "*.yml")))
    if args.limit:
        files = files[: args.limit]
    sem = asyncio.Semaphore(5)
    results = await asyncio.gather(*(translate_cluster(f, sem, args.write) for f in files))

    ok = fail = 0
    conf = {}
    for path, data in results:
        if data and data.get("_skip"):
            continue
        if not data or not data.get("sutras") or data.get("_error"):
            fail += 1; print("  FAIL", os.path.basename(path), (data or {}).get("_error", "")); continue
        d = yaml.safe_load(open(path))
        # rebuild translation_literal preserving order from the IAST
        order = list(parse_iast(_as_text(d.get("sanskrit_iast"))).keys())
        lines = [f"**{k}** {data['sutras'][k].strip()}" for k in order if k in data["sutras"]]
        d["translation_literal"] = "\n".join(lines)
        d["translation_confidence"] = data.get("confidence", "medium")
        conf[data.get("confidence", "medium")] = conf.get(data.get("confidence", "medium"), 0) + 1
        ok += 1
        if args.limit and not args.write:
            print(f"=== {d.get('sutra_range')} [{data.get('confidence')}] ===")
            print(d["translation_literal"][:500])
        if args.write:
            with open(path, "w") as fh:
                yaml.safe_dump(d, fh, allow_unicode=True, sort_keys=False, width=120)
    print(f"\n{'wrote' if args.write else 'previewed'} {ok} | fail {fail} | confidence {conf}")


if __name__ == "__main__":
    asyncio.run(main())
