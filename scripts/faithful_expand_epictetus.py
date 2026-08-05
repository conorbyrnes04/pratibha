#!/usr/bin/env python3
"""Faithfully expand Epictetus's Enchiridion from the Perseus GREEK source.

Same asteya method as the Marcus pipeline: the Greek ORIGINAL is the source of
record (Perseus grc2, Unicode — fetched verbatim, not model-supplied); the
TRANSLATION is Pratibha's own, rendered by Terra directly from the Greek,
recalling the cadence of the great public-domain renderings (Long, Higginson,
Carter) without reproducing them; Luna cross-checks fidelity. One unit per
Enchiridion chapter (aggregating its sections). Greek stored in the
`sanskrit_devanagari` slot by collection convention.
"""
import argparse, asyncio, glob, html, os, re, sys, unicodedata
import yaml

REPO = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha"
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, "scripts"))
from faithful_expand_upanishads import build_commentary, _lenient_json, slugify  # noqa: E402

RAW = os.path.join(REPO, "data/raw_texts/pd/greek/epictetus_enchiridion_perseus_grc2.xml")
CANON = os.path.join(REPO, "data/canonical/epictetus_works")
NAME = "Enchiridion"
EDITION = "Perseus grc2 e-text of Epictetus, Encheiridion (Schenkl), Unicode Greek"


def parse_enchiridion():
    """Return {chapter: greek_text} aggregating all sections of the chapter."""
    raw = open(RAW, encoding="utf-8").read()
    out = {}
    for cm in re.finditer(r'<div[^>]*subtype="chapter"[^>]*\bn="(\d+)"[^>]*>(.*?)(?=<div[^>]*subtype="chapter"|</body|</text)', raw, re.S):
        ch = int(cm.group(1))
        body = re.sub(r"<[^>]+>", " ", cm.group(2))
        body = html.unescape(body)
        body = re.sub(r"\s+", " ", body).strip()
        if body:
            out[ch] = body
    return out


def norm_greek(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^α-ω]", "", s)


def covered(ench):
    """Chapters already covered. ENCH_NN via 'Enchiridion N' section; opaque
    EPI_ENC_NNN via Greek content-match."""
    cov = set()
    joined, offs, pos = "", [], 0
    for c, t in ench.items():
        n = norm_greek(t); joined += n; offs.append((pos, pos + len(n), c)); pos += len(n)

    def at(off):
        for a, e, c in offs:
            if a <= off < e:
                return c
        return None
    for path in glob.glob(os.path.join(CANON, "*.yml")):
        d = yaml.safe_load(open(path)) or {}
        sid = str(d.get("source_id") or "")
        sec = str(d.get("section") or (d.get("provenance") or {}).get("section") or "")
        m = re.search(r"Enchiridion\s+(\d+)|Ench(?:iridion)?[_ ](\d+)", sec) or re.search(r"ENCH[_ ](\d+)", sid)
        if m:
            cov.add(int([g for g in m.groups() if g][0])); continue
        g = norm_greek(str(d.get("sanskrit_devanagari") or ""))
        if len(g) < 20:
            continue
        start = -1
        for hl in (30, 20, 14):
            start = joined.find(g[:hl])
            if start >= 0:
                break
        if start >= 0 and at(start):
            cov.add(at(start))
        else:
            print(f"  ? {sid}: no chapter match")
    return cov


def plan(ench, cov):
    return [[c] for c in sorted(ench) if c not in cov]


SYS_GEN = (
    "You are a scholar-translator building a study unit for the Pratibha corpus from the VERBATIM "
    "Greek of Epictetus's Enchiridion, supplied in Unicode. The Greek is the source of record; your "
    "job is fresh interpretive authorship around it.\n"
    "Produce a FRESH English translation directly from the Greek. You may recall the cadence of the "
    "great public-domain renderings (Long, Carter, Higginson), but the wording MUST be your own — "
    "never reproduce any existing translation. Faithful, clear, unhurried.\n"
    "Then author: a short evocative title; 3-5 themes; a 2-3 paragraph commentary reading the passage "
    "closely (cite a key Greek term or two — e.g. προαίρεσις, τὰ ἐφʼ ἡμῖν); 3-4 key terms drawn from "
    "words ACTUALLY in the passage (Greek term + one-line gloss); 3 cross-tradition resonances, each a "
    "REAL recognizable citation + one-sentence parallel + one honest divergence; one concrete practice.\n"
    'Return ONLY compact JSON: {"title":"","themes":[""],"translation":"","commentary":"",'
    '"key_terms":[{"term":"","gloss":""}],"resonances":[{"citation":"","resonance":"","divergence":""}],'
    '"practice":""}'
)
SYS_VERIFY = (
    "You verify that an English translation faithfully renders a given Greek passage of Epictetus's "
    "Enchiridion. Judge only fidelity of meaning (not style). "
    'Return ONLY JSON: {"verdict":"faithful"|"loose"|"wrong","note":"<short reason>"}'
)


async def generate(chunk, ench, sem):
    from app.llm import smart_chat
    ch = chunk[0]
    greek = ench[ch]
    async with sem:
        r = None
        for attempt in range(4):
            try:
                r = await smart_chat(
                    [{"role": "system", "content": SYS_GEN},
                     {"role": "user", "content": f"Reference: Enchiridion {ch}\nGreek:\n{greek}\n\nReturn JSON."}],
                    primary_model="openai/gpt-5.6-terra", temperature=0.4,
                    max_tokens=4000 if len(greek) > 700 else 1800)
                break
            except Exception:
                await asyncio.sleep(2 * (attempt + 1))
    if r is None:
        return ch, "ERR", None
    data = _lenient_json(r)
    if not data or not data.get("translation"):
        return ch, "parse", None
    vr = None
    async with sem:
        for attempt in range(3):
            try:
                vr = await smart_chat(
                    [{"role": "system", "content": SYS_VERIFY},
                     {"role": "user", "content": f"Greek: {greek[:2600]}\n\nEnglish: {data['translation'][:2600]}\n\nReturn JSON."}],
                    primary_model="openai/gpt-5.6-luna", temperature=0.0, max_tokens=300)
                break
            except Exception:
                await asyncio.sleep(2 * (attempt + 1))
    vj = _lenient_json(vr) if vr else None
    verdict = (vj or {}).get("verdict", "unknown")
    if verdict == "wrong":
        return ch, f"REJECTED(wrong): {(vj or {}).get('note','')[:70]}", None
    return ch, "ok", build_unit(ch, greek, data, verdict)


def build_unit(ch, greek, data, verdict):
    sid = f"ENCH_{ch:02d}"
    title = (data.get("title") or "").strip() or f"{NAME} {ch}"
    themes = [t.strip() for t in (data.get("themes") or []) if t.strip()][:5]
    return {
        "source_id": sid, "category": "root_text", "work_id": "epictetus_works",
        "work_title": "Epictetus, Enchiridion", "unit_id": f"epictetus_works.faithful_{slugify(sid)}",
        "unit_label": title, "title": title, "unit_type": "chapter",
        "sanskrit_devanagari": greek,   # Greek in the original slot by collection convention
        "translation_literal": (data.get("translation") or "").strip(),
        "commentary": build_commentary(data), "practice": (data.get("practice") or "").strip(),
        "themes": themes, "tags": sorted(set(themes + ["epictetus_works", "root_text"])),
        "quality_score": 0, "editorial_score": 0,
        "provenance": {
            "collection": "Epictetus, Enchiridion", "section": f"{NAME} {ch}", "original_id": sid,
            "original_reliability": f"SOURCED — {EDITION}",
            "verification": f"translation cross-checked (Luna): {verdict}; original from Perseus Greek",
            "english_source": "Pratibha original translation (2026), rendered directly from the Greek; voice-informed by public-domain renderings, not derived from any copyrighted translation",
            "original_source": EDITION,
        },
    }


async def run_write(ench, chunks):
    print(f"[Enchiridion] generating {len(chunks)} units ...")
    sem = asyncio.Semaphore(4)
    res = await asyncio.gather(*(generate(ch, ench, sem) for ch in chunks))
    written = 0
    for ch, status, unit in res:
        if status == "ok" and unit:
            p = os.path.join(CANON, f"epictetus_works_{slugify(unit['source_id'])}.yml")
            yaml.safe_dump(unit, open(p, "w"), allow_unicode=True, sort_keys=False, width=100)
            written += 1; print(f"  ✓ {ch}")
        else:
            print(f"  · {ch}: {status}")
    print(f"[Enchiridion] wrote {written}/{len(chunks)} units")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dryparse", action="store_true")
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    ench = parse_enchiridion()
    print(f"parsed {len(ench)} chapters (1..{max(ench)})")
    if a.dryparse:
        for c in list(ench)[:3]:
            print(f"  {c}: {ench[c][:80]}")
        return
    cov = covered(ench)
    print(f"covered: {len(cov)} chapters")
    chunks = plan(ench, cov)
    print(f"gap chunks: {len(chunks)}")
    if a.write:
        asyncio.run(run_write(ench, chunks[:a.limit] if a.limit else chunks))


if __name__ == "__main__":
    main()
