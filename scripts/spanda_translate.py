#!/usr/bin/env python3
"""Faithful re-translation of the 112 VBT yuktis FROM the attached Sanskrit.

Per the agreed method: render fresh, clear modern English from the IAST original
using the model's own Sanskrit competence — NOT a copy of any in-copyright
translation, NOT a swap to an archaic PD one. Keep genuine terms with a gloss.
Flag low-confidence renderings for human review. Operates on the STAGED VBT
Sanskrit files (data/staging/vbt_sanskrit); writes translation back there.
"""
import argparse, asyncio, glob, json, os, re, sys
import yaml
sys.path.insert(0, "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha")
from app.llm import smart_chat            # noqa
from app.data_loader import _as_text      # noqa

STAGE = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha/data/staging/spanda_sanskrit"

SYSTEM = """You are a scholar of Kashmir Śaiva Sanskrit translating a kārikā (or two) from Vasugupta's Spandakārikā — the foundational text on spanda, the subtle creative vibration/pulse of consciousness (Śiva-Śakti) underlying all appearance.

Translate the given IAST into clear, faithful, contemporary English — accurate to the grammar and the Spanda/Trika doctrine, dignified but not archaic. These are doctrinal verses about recognizing spanda, not step-by-step instructions.

Rules:
- Translate ONLY what the Sanskrit says. Do not import a famous rendering from memory; work from THIS text.
- Keep pivotal terms in parentheses after the English (e.g. "the vibration (spanda)", "the group of faculties (karaṇa-varga)", "the knowing subject (grāhaka)").
- Keep it to the length of the verse — usually 1–3 sentences.
- If a word/compound is ambiguous or you are unsure, set "confidence":"low" and name the uncertainty in "note".

Return ONLY JSON: {"translation":"...", "confidence":"high|medium|low", "note":"..."}"""


async def translate_one(path: str, sem: asyncio.Semaphore) -> tuple[str, dict | None]:
    d = yaml.safe_load(open(path))
    if d.get('translation_confidence'):
        return path, {'_skip': True}
    iast = _as_text(d.get("sanskrit_iast"))
    ref = _as_text(d.get("translation") or d.get("translation_literal"))
    ref = re.sub(r"^YUKTI #\d+\s*", "", ref)
    ref = re.sub(r"\s*\|\|.*$", "", ref).strip()
    user = (f"Verse ({d.get('source_verse')}), IAST:\n{iast}\n\n"
            f"(For cross-check only — an existing English rendering; do NOT copy its wording, "
            f"verify your own against it: {ref[:400]})\n\nReturn the JSON.")
    async with sem:
        try:
            txt = await smart_chat(
                [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
                temperature=0.3, max_tokens=600)
        except Exception as e:  # credits/network — don't crash the whole batch
            return path, {"_error": str(e)[:80]}
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
    results = await asyncio.gather(*(translate_one(f, sem) for f in files))

    low = []
    ok = 0
    for path, data in results:
        n = re.search(r"sp_(\d+)", path).group(1)
        if not data or not data.get("translation"):
            print(f"  FAIL yukti {n}")
            continue
        conf = data.get("confidence", "?")
        if conf == "low":
            low.append((n, data.get("note", "")))
        if args.limit and not args.write:
            print(f"\n--- yukti {n} [{conf}] ---")
            print("  ", data["translation"])
            if data.get("note"):
                print("   note:", data["note"])
        else:
            print(f"  yukti {n} [{conf}] {data['translation'][:70]}")
        if args.write:
            d = yaml.safe_load(open(path))
            d["translation_literal"] = data["translation"]
            d["translation_confidence"] = conf
            if data.get("note"):
                d["translation_note"] = data["note"]
            d.pop("insight", None)  # drop the old Wallis-derived filler insight
            with open(path, "w") as fh:
                yaml.safe_dump(d, fh, allow_unicode=True, sort_keys=False, width=120)
        ok += 1
    print(f"\n{'wrote' if args.write else 'previewed'} {ok}/{len(files)} | low-confidence: {len(low)}")
    for n, note in low[:20]:
        print(f"   REVIEW yukti {n}: {note}")


if __name__ == "__main__":
    asyncio.run(main())
