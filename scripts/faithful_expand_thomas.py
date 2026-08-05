#!/usr/bin/env python3
"""Faithfully expand a new collection: the Gospel of Thomas from the Coptic.

Same asteya method: the Coptic ORIGINAL is the source of record — the Coptic
Scriptorium TEI of Nag Hammadi Codex II,2 (CC-BY 4.0; the manuscript text itself
is ancient/public-domain, digital edition attributed). The TRANSLATION is
Pratibha's own, rendered by Terra directly from the Coptic, recalling the cadence
of the great renderings (Lambdin, Layton) without reproducing them; Luna checks
fidelity. One unit per logion (the prologue + 114 sayings). Coptic stored in the
`sanskrit_devanagari` slot by corpus convention (its own script — no translit).
"""
import argparse, asyncio, glob, os, re, sys
import yaml

REPO = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha"
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, "scripts"))
from faithful_expand_upanishads import build_commentary, _lenient_json, slugify  # noqa: E402

RAW = os.path.join(REPO, "data/raw_texts/pd/coptic/thomas_gospel_copticscriptorium_TEI.xml")
CANON = os.path.join(REPO, "data/canonical/gospel_of_thomas")
NAME = "Gospel of Thomas"
EDITION = "Coptic Scriptorium TEI of the Gospel of Thomas (Nag Hammadi Codex II,2; CC-BY 4.0)"


def parse_thomas():
    """Return ordered [(logion, coptic_text)]; logion 0 = prologue/incipit.
    Coptic word forms are recovered by joining <w> within each <phr>."""
    raw = open(RAW, encoding="utf-8").read()
    out = []
    for dm in re.finditer(r'<div1[^>]*\bn="(\d+)"[^>]*>(.*?)(?=<div1|</body)', raw, re.S):
        n = int(dm.group(1))
        phrs = re.findall(r"<phr>(.*?)</phr>", dm.group(2), re.S)
        words = ["".join(re.findall(r"<w[^>]*>\s*([^<]+?)\s*</w>", p)) for p in phrs]
        text = " ".join(w for w in words if w).strip()
        # fallback: any <w> not wrapped in <phr>
        if not text:
            text = " ".join(re.findall(r"<w[^>]*>\s*([^<]+?)\s*</w>", dm.group(2))).strip()
        if text:
            out.append((n, text))
    return out


def covered():
    cov = set()
    for path in glob.glob(os.path.join(CANON, "*.yml")):
        d = yaml.safe_load(open(path)) or {}
        sid = str(d.get("source_id") or "")
        m = re.search(r"(?:THOM|LOGION)[_ ]?(\d+)", sid) or \
            re.search(r"(?:Logion|Saying|Prologue)\s*(\d*)", str(d.get("section") or ""))
        if m:
            cov.add(int(m.group(1)) if m.group(1) else 0)
    return cov


def plan(logia, cov):
    return [[n] for (n, _) in logia if n not in cov]


SYS_GEN = (
    "You are a scholar-translator building a study unit for the Pratibha corpus from the VERBATIM "
    "Coptic (Sahidic) of the Gospel of Thomas, supplied in Coptic script. The Coptic is the source "
    "of record; your job is fresh interpretive authorship around it.\n"
    "Produce a FRESH English translation directly from the Coptic. You may recall the cadence of the "
    "great renderings (Lambdin, Layton), but the wording MUST be your own — never reproduce any "
    "existing translation. Translate ONLY what is present in this logion; be faithful, clear, spare.\n"
    "Then author: a short evocative title; 3-5 themes; a 2-3 paragraph commentary reading the saying "
    "closely (note a key Coptic/Greek-loan term if apt — e.g. ⲙⲟⲛⲁⲭⲟⲥ, ⲡⲗⲏⲣⲱⲙⲁ); 3-4 key terms "
    "(term + one-line gloss); 3 cross-tradition resonances, each a REAL recognizable citation + "
    "one-sentence parallel + one honest divergence; one concrete embodied practice.\n"
    'Return ONLY compact JSON: {"title":"","themes":[""],"translation":"","commentary":"",'
    '"key_terms":[{"term":"","gloss":""}],"resonances":[{"citation":"","resonance":"","divergence":""}],'
    '"practice":""}'
)
SYS_VERIFY = (
    "You verify that an English translation faithfully renders a given Coptic (Sahidic) logion of the "
    "Gospel of Thomas. Judge only fidelity of meaning (not style). "
    'Return ONLY JSON: {"verdict":"faithful"|"loose"|"wrong","note":"<short reason>"}'
)


async def generate(chunk, logia_map, sem):
    from app.llm import smart_chat
    n = chunk[0]
    coptic = logia_map[n]
    label = "Prologue" if n == 0 else f"Logion {n}"
    async with sem:
        r = None
        for attempt in range(4):
            try:
                r = await smart_chat(
                    [{"role": "system", "content": SYS_GEN},
                     {"role": "user", "content": f"Reference: Gospel of Thomas — {label}\nCoptic:\n{coptic}\n\nReturn JSON."}],
                    primary_model="openai/gpt-5.6-terra", temperature=0.35, max_tokens=2000)
                break
            except Exception:
                await asyncio.sleep(2 * (attempt + 1))
    if r is None:
        return label, "ERR", None
    data = _lenient_json(r)
    if not data or not data.get("translation"):
        return label, "parse", None
    vr = None
    async with sem:
        for attempt in range(3):
            try:
                vr = await smart_chat(
                    [{"role": "system", "content": SYS_VERIFY},
                     {"role": "user", "content": f"Coptic: {coptic[:2600]}\n\nEnglish: {data['translation'][:2600]}\n\nReturn JSON."}],
                    primary_model="openai/gpt-5.6-luna", temperature=0.0, max_tokens=300)
                break
            except Exception:
                await asyncio.sleep(2 * (attempt + 1))
    vj = _lenient_json(vr) if vr else None
    verdict = (vj or {}).get("verdict", "unknown")
    if verdict == "wrong":
        return label, f"REJECTED(wrong): {(vj or {}).get('note','')[:70]}", None
    return label, "ok", build_unit(n, coptic, data, verdict)


def build_unit(n, coptic, data, verdict):
    sid = "THOM_PROLOGUE" if n == 0 else f"THOM_{n:03d}"
    label = "Prologue" if n == 0 else f"Logion {n}"
    title = (data.get("title") or "").strip() or f"Gospel of Thomas — {label}"
    themes = [t.strip() for t in (data.get("themes") or []) if t.strip()][:5]
    return {
        "source_id": sid, "category": "root_text", "work_id": "gospel_of_thomas",
        "work_title": NAME, "unit_id": f"gospel_of_thomas.faithful_{slugify(sid)}",
        "unit_label": title, "title": title, "unit_type": "logion",
        "sanskrit_devanagari": coptic,   # Coptic in the original slot by corpus convention
        "translation_literal": (data.get("translation") or "").strip(),
        "commentary": build_commentary(data), "practice": (data.get("practice") or "").strip(),
        "themes": themes, "tags": sorted(set(themes + ["gospel_of_thomas", "root_text"])),
        "quality_score": 0, "editorial_score": 0,
        "provenance": {
            "collection": NAME, "section": f"Gospel of Thomas {label}", "original_id": sid,
            "original_reliability": f"SOURCED — {EDITION}",
            "verification": f"translation cross-checked (Luna): {verdict}; original from Coptic Scriptorium",
            "english_source": "Pratibha original translation (2026), rendered directly from the Coptic; voice-informed by public-domain scholarship, not derived from any copyrighted translation",
            "original_source": EDITION,
        },
    }


async def run_write(logia_map, chunks):
    print(f"[Thomas] generating {len(chunks)} units ...")
    sem = asyncio.Semaphore(4)
    res = await asyncio.gather(*(generate(ch, logia_map, sem) for ch in chunks))
    written = 0
    for label, status, unit in res:
        if status == "ok" and unit:
            p = os.path.join(CANON, f"gospel_of_thomas_{slugify(unit['source_id'])}.yml")
            yaml.safe_dump(unit, open(p, "w"), allow_unicode=True, sort_keys=False, width=100)
            written += 1; print(f"  ✓ {label}")
        else:
            print(f"  · {label}: {status}")
    print(f"[Thomas] wrote {written}/{len(chunks)} units")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dryparse", action="store_true")
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    logia = parse_thomas()
    lm = dict(logia)
    print(f"parsed {len(logia)} logia (n={logia[0][0]}..{logia[-1][0]})")
    if a.dryparse:
        for n, t in logia[:3]:
            print(f"  {n}: {t[:70]}")
        return
    cov = covered()
    print(f"covered: {len(cov)}")
    chunks = plan(logia, cov)
    print(f"gap chunks: {len(chunks)}")
    if a.write:
        asyncio.run(run_write(lm, chunks[:a.limit] if a.limit else chunks))


if __name__ == "__main__":
    main()
