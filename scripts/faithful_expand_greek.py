#!/usr/bin/env python3
"""Faithfully expand Marcus Aurelius's Meditations from the Perseus GREEK source.

Same asteya method as the Sanskrit pipeline: the Greek ORIGINAL is the source of
record (converted from the Perseus TLG Betacode to Unicode); the TRANSLATION is
Pratibha's own, rendered by Terra directly from the Greek, recalling the cadence
of the great public-domain renderings (Long, Farquharson) without reproducing
them; Luna cross-checks fidelity. No transliteration/Devanagari (Greek stands as
its own script). Greek is stored in the `sanskrit_devanagari` slot, matching the
collection's existing convention, so data_loader builds the Original layer from it.
"""
import argparse, asyncio, glob, html, os, re, sys
import yaml

REPO = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha"
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, "scripts"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_betacode_to_greek import betacode_to_greek  # noqa: E402
from faithful_expand_upanishads import build_commentary, _lenient_json, slugify  # noqa: E402

RAW = os.path.join(REPO, "data/raw_texts/pd/greek/marcus_aurelius_perseus_greek.xml")
CANON = os.path.join(REPO, "data/canonical/marcus_aurelius_meditations")
NAME = "Meditations"
EDITION = "Perseus TLG e-text of Marcus Aurelius, τὰ εἰς ἑαυτόν (Betacode → Unicode)"


def parse_meditations():
    """Return {(book, chapter): greek_text}."""
    raw = open(RAW, encoding="utf-8").read()
    out = {}
    for bm in re.finditer(r'<div1[^>]*type="book"[^>]*n="(\d+)"[^>]*>(.*?)(?=<div1|\Z)', raw, re.S):
        book = int(bm.group(1))
        for cm in re.finditer(r'<div2[^>]*type="chapter"[^>]*n="(\d+)"[^>]*>(.*?)(?=<div2|</div1)', bm.group(2), re.S):
            ch = int(cm.group(1))
            body = cm.group(2)
            body = re.sub(r"<[^>]+>", " ", body)          # strip milestones/markup
            body = html.unescape(body)
            body = re.sub(r"\s+", " ", body).strip()
            greek = betacode_to_greek(body)
            if greek:
                out[(book, ch)] = greek
    return out


def norm_greek(s: str) -> str:
    import unicodedata
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^α-ω]", "", s)  # base letters only, drop diacritics/space


ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}


def roman_to_int(s):
    s = s.upper(); total = 0
    for i, ch in enumerate(s):
        if ch not in ROMAN:
            return None
        v = ROMAN[ch]
        total += -v if (i + 1 < len(s) and ROMAN.get(s[i + 1], 0) > v) else v
    return total


def unit_bookchapter(d):
    """(book, chapter) for a unit. Handles: MA_BB_CC and new MED_BB_CC ids;
    'Meditations 2.2' arabic sections; and legacy MED_00N opaque units via their
    Roman 'II.11' section."""
    sid = str(d.get("source_id") or "")
    m = re.search(r"(?:MA|MED)[_ ]?(\d+)[_ ](\d+)", sid)   # MA_02_11 or MED_02_02
    if m:
        return int(m.group(1)), int(m.group(2))
    prov = d.get("provenance") if isinstance(d.get("provenance"), dict) else {}
    sec = str(d.get("section") or prov.get("section") or "")
    m = re.search(r"Meditations\s+(\d+)\.(\d+)", sec)       # 'Meditations 3.7'
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.match(r"\s*([IVXLC]+)[.\s]+(\d+)", sec)          # legacy Roman 'II.11'
    if m and roman_to_int(m.group(1)):
        return roman_to_int(m.group(1)), int(m.group(2))
    return None


def covered(meds):
    cov = set()
    for path in glob.glob(os.path.join(CANON, "*.yml")):
        d = yaml.safe_load(open(path)) or {}
        bc = unit_bookchapter(d)
        if bc:
            cov.add(bc)
    return cov


def reconcile_med(meds, apply):
    """For each MED unit: pin coverage via its Roman section and replace any
    model-supplied ('per received text') Greek with the verified Perseus Greek
    for that chapter — a genuine original-provenance upgrade."""
    fixed = 0
    for path in sorted(glob.glob(os.path.join(CANON, "*.yml"))):
        d = yaml.safe_load(open(path)) or {}
        sid = str(d.get("source_id") or "")
        if not sid.startswith("MED_"):
            continue
        bc = unit_bookchapter(d)
        prov = d.get("provenance") if isinstance(d.get("provenance"), dict) else {}
        if not bc or bc not in meds:
            print(f"  ? {sid}: section {d.get('section')} not resolvable"); continue
        cur = norm_greek(str(d.get("sanskrit_devanagari") or ""))
        real = meds[bc]
        matches = norm_greek(real)[:14] and cur[:14] in norm_greek(real)
        tag = "already-verified" if matches else "REPLACED model-supplied Greek"
        print(f"  ✓ {sid}: {bc[0]}.{bc[1]}  ({tag})")
        if apply and not matches:
            d["sanskrit_devanagari"] = real
            prov["section"] = f"{NAME} {bc[0]}.{bc[1]}"
            prov["original_reliability"] = (
                f"RESTORED — Perseus Greek for Meditations {bc[0]}.{bc[1]} "
                f"(replaces a model-supplied paraphrase); {EDITION}")
            prov["original_source"] = EDITION
            prov["verification"] = "original replaced with verified PD Greek; translation retained"
            d["provenance"] = prov
            yaml.safe_dump(d, open(path, "w"), allow_unicode=True, sort_keys=False, width=100)
            fixed += 1
    print(f"[Meditations] fixed {fixed} MED originals" if apply else "[dry run]")


SYS_GEN = (
    "You are a scholar-translator building a study unit for the Pratibha corpus from the "
    "VERBATIM Greek of Marcus Aurelius's Meditations (τὰ εἰς ἑαυτόν), supplied in Unicode. "
    "The Greek is the source of record; your job is fresh interpretive authorship around it.\n"
    "Produce a FRESH English translation directly from the Greek. You may recall the dignified "
    "cadence of the great public-domain renderings (Long, Farquharson), but the wording MUST be "
    "your own — never reproduce any existing translation. Be faithful, clear, and unhurried.\n"
    "Then author: a short evocative title; 3-5 themes; a 2-3 paragraph commentary reading the "
    "passage closely (name what the Greek actually says — cite a key Greek term or two); 3-4 key "
    "terms drawn from words ACTUALLY in the passage (Greek term + one-line gloss); 3 cross-tradition "
    "resonances, each a REAL recognizable citation + one-sentence parallel + one honest divergence; "
    "and one concrete embodied practice.\n"
    'Return ONLY compact JSON: {"title":"","themes":[""],"translation":"","commentary":"",'
    '"key_terms":[{"term":"","gloss":""}],"resonances":[{"citation":"","resonance":"","divergence":""}],'
    '"practice":""}'
)
SYS_VERIFY = (
    "You verify that an English translation faithfully renders a given Greek passage of Marcus "
    "Aurelius's Meditations. Judge only fidelity of meaning (not style). "
    'Return ONLY JSON: {"verdict":"faithful"|"loose"|"wrong","note":"<short reason>"}'
)


async def generate(chunk, meds, sem):
    from app.llm import smart_chat
    b0, c0 = chunk[0]; b1, c1 = chunk[-1]
    ref = f"{b0}.{c0}" if len(chunk) == 1 else f"{b0}.{c0}–{b1}.{c1}"
    greek = "\n".join(f"{meds[(b,c)]}  [{b}.{c}]" for (b, c) in chunk)
    plain = " ".join(meds[(b, c)] for (b, c) in chunk)
    async with sem:
        r = None
        for attempt in range(4):
            try:
                r = await smart_chat(
                    [{"role": "system", "content": SYS_GEN},
                     {"role": "user", "content": f"Reference: Meditations {ref}\nGreek:\n{greek}\n\nReturn JSON."}],
                    primary_model="openai/gpt-5.6-terra", temperature=0.4, max_tokens=1800)
                break
            except Exception:
                await asyncio.sleep(2 * (attempt + 1))
    if r is None:
        return ref, "ERR", None
    data = _lenient_json(r)
    if not data or not data.get("translation"):
        return ref, "parse", None
    vr = None
    async with sem:
        for attempt in range(3):
            try:
                vr = await smart_chat(
                    [{"role": "system", "content": SYS_VERIFY},
                     {"role": "user", "content": f"Greek: {plain[:800]}\n\nEnglish: {data['translation'][:900]}\n\nReturn JSON."}],
                    primary_model="openai/gpt-5.6-luna", temperature=0.0, max_tokens=300)
                break
            except Exception:
                await asyncio.sleep(2 * (attempt + 1))
    vj = _lenient_json(vr) if vr else None
    verdict = (vj or {}).get("verdict", "unknown")
    if verdict == "wrong":
        return ref, f"REJECTED(wrong): {(vj or {}).get('note','')[:70]}", None
    return ref, "ok", build_unit(chunk, ref, data, "\n".join(meds[(b, c)] for (b, c) in chunk), verdict)


def build_unit(chunk, ref, data, greek_block, verdict):
    b0, c0 = chunk[0]; b1, c1 = chunk[-1]
    tag = f"{b0:02d}_{c0:02d}" if len(chunk) == 1 else f"{b0:02d}_{c0:02d}_{c1:02d}"
    sid = f"MED_{tag}"
    title = (data.get("title") or "").strip() or f"{NAME} {ref}"
    themes = [t.strip() for t in (data.get("themes") or []) if t.strip()][:5]
    return {
        "source_id": sid, "category": "root_text", "work_id": "marcus_aurelius_meditations",
        "work_title": NAME, "unit_id": f"marcus_aurelius_meditations.faithful_{slugify(sid)}",
        "unit_label": title, "title": title, "unit_type": "chapter",
        "sanskrit_devanagari": greek_block,   # Greek lives in this slot by collection convention
        "translation_literal": (data.get("translation") or "").strip(),
        "commentary": build_commentary(data), "practice": (data.get("practice") or "").strip(),
        "themes": themes, "tags": sorted(set(themes + ["marcus_aurelius_meditations", "root_text"])),
        "quality_score": 0, "editorial_score": 0,
        "provenance": {
            "collection": NAME, "section": f"{NAME} {ref}", "original_id": sid,
            "original_reliability": f"SOURCED — {EDITION}",
            "verification": f"translation cross-checked (Luna): {verdict}; original from Perseus Greek",
            "english_source": "Pratibha original translation (2026), rendered directly from the Greek; voice-informed by public-domain renderings, not derived from any copyrighted translation",
            "original_source": EDITION,
        },
    }


async def run_write(meds, chunks):
    print(f"[Meditations] generating {len(chunks)} units ...")
    sem = asyncio.Semaphore(4)
    res = await asyncio.gather(*(generate(ch, meds, sem) for ch in chunks))
    written = 0
    for ref, status, unit in res:
        if status == "ok" and unit:
            p = os.path.join(CANON, f"marcus_aurelius_meditations_{slugify(unit['source_id'])}.yml")
            yaml.safe_dump(unit, open(p, "w"), allow_unicode=True, sort_keys=False, width=100)
            written += 1
            print(f"  ✓ {ref}")
        else:
            print(f"  · {ref}: {status}")
    print(f"[Meditations] wrote {written}/{len(chunks)} units")


def plan(meds, cov, target=1, minbook=1, maxbook=12):
    keys = sorted(meds)
    uncov = [k for k in keys if k not in cov and minbook <= k[0] <= maxbook]
    chunks, cur = [], []
    for k in uncov:
        if cur and (k[0] != cur[-1][0] or k[1] != cur[-1][1] + 1 or len(cur) >= target):
            chunks.append(cur); cur = []
        cur.append(k)
    if cur:
        chunks.append(cur)
    return chunks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dryparse", action="store_true")
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--reconcile", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--target", type=int, default=1)
    ap.add_argument("--minbook", type=int, default=1)
    ap.add_argument("--maxbook", type=int, default=12)
    a = ap.parse_args()
    meds = parse_meditations()
    print(f"parsed {len(meds)} chapters; books {sorted(set(b for b,_ in meds))}")
    if a.dryparse:
        for k in list(meds)[:3]:
            print(f"  {k[0]}.{k[1]}: {meds[k][:80]}")
        return
    if a.reconcile:
        reconcile_med(meds, a.apply)
        return
    cov = covered(meds)
    print(f"covered: {len(cov)} chapters")
    chunks = plan(meds, cov, a.target, a.minbook, a.maxbook)
    print(f"gap chunks: {len(chunks)} covering {sum(len(c) for c in chunks)} chapters")
    if a.plan:
        from collections import Counter
        print("  by book:", dict(sorted(Counter(c[0][0] for c in chunks).items())))
    if a.write:
        asyncio.run(run_write(meds, chunks[:a.limit] if a.limit else chunks))


if __name__ == "__main__":
    main()
