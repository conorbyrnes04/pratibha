#!/usr/bin/env python3
"""Faithfully expand the Dhammapada from the Fausböll romanized-Pali source.

Same asteya method: the Pali ORIGINAL is the source of record (Fausböll 1900,
romanized — a legitimate PD edition; shown as romanized Pali, not a fabricated
script); the TRANSLATION is Pratibha's own, rendered by Terra directly from the
Pali, recalling the cadence of the great renderings (Müller, Radhakrishnan) without
copying; Luna checks fidelity. Verses grouped thematically within a vagga so short
aphorisms don't read as fragments. Pali stored in the `sanskrit_devanagari` slot
by collection convention (no Devanagari transliteration for Pali)."""
import argparse, asyncio, glob, os, re, sys
import yaml

REPO = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha"
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, "scripts"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from faithful_expand_upanishads import build_commentary, _lenient_json, slugify  # noqa: E402

RAW = os.path.join(REPO, "data/raw_texts/pd/pali/dhammapada_fausboll_1900_pali.txt")
CANON = os.path.join(REPO, "data/canonical/dhammapada")
NAME = "Dhammapada"
EDITION = "Fausböll romanized-Pali edition of the Dhammapada (1900)"


def parse_dhp():
    """Return ordered [(global_verse, vagga_no, vagga_name, pali_text)]."""
    out = []
    vno, vname = 0, ""
    cur_n, cur_lines = None, []

    def flush():
        if cur_n is not None and cur_lines:
            txt = re.sub(r"\s+", " ", " ".join(cur_lines)).strip()
            out.append((cur_n, vno, vname, txt))

    for raw in open(RAW, encoding="utf-8"):
        line = raw.rstrip()
        s = line.strip()
        mch = re.match(r"^(\d+)\.\s+([A-Za-zāīūṅñṇṭḍṃḷ]+vagga)\s*$", s)
        if mch:
            flush(); cur_n, cur_lines = None, []
            vno, vname = int(mch.group(1)), mch.group(2)
            continue
        mv = re.match(r"^(\d+)\s+(.*)$", s)
        if mv and vno:                       # start of a new verse
            flush()
            cur_n, cur_lines = int(mv.group(1)), [mv.group(2)]
        elif cur_n is not None and s:
            cur_lines.append(s)
    flush()
    return out


def covered():
    """Global verse numbers already covered, from (N) markers in existing units."""
    cov = set()
    for path in glob.glob(os.path.join(CANON, "*.yml")):
        d = yaml.safe_load(open(path)) or {}
        g = str(d.get("sanskrit_devanagari") or "")
        for m in re.findall(r"\((\d+)\)", g):
            cov.add(int(m))
    return cov


def plan(verses, cov, target=4):
    uncov = [v for v in verses if v[0] not in cov]
    chunks, cur = [], []
    for v in uncov:
        if cur and (v[1] != cur[-1][1] or v[0] != cur[-1][0] + 1 or len(cur) >= target):
            chunks.append(cur); cur = []
        cur.append(v)
    if cur:
        chunks.append(cur)
    return chunks


SYS_GEN = (
    "You are a scholar-translator building a study unit for the Pratibha corpus from the VERBATIM "
    "Pali of the Dhammapada, supplied in romanized Pali. The Pali is the source of record; your job "
    "is fresh interpretive authorship around it.\n"
    "Produce a FRESH English translation directly from the Pali. You may recall the cadence of the "
    "great public-domain renderings (Müller, Radhakrishnan), but the wording MUST be your own — "
    "never reproduce any existing translation. Faithful, clear, unhurried.\n"
    "Then author: a short evocative title; 3-5 themes; a 2-3 paragraph commentary reading the passage "
    "closely (cite a key Pali term or two); 3-4 key terms drawn from words ACTUALLY in the verses "
    "(Pali term + one-line gloss); 3 cross-tradition resonances, each a REAL recognizable citation + "
    "one-sentence parallel + one honest divergence; one concrete embodied practice.\n"
    'Return ONLY compact JSON: {"title":"","themes":[""],"translation":"","commentary":"",'
    '"key_terms":[{"term":"","gloss":""}],"resonances":[{"citation":"","resonance":"","divergence":""}],'
    '"practice":""}'
)
SYS_VERIFY = (
    "You verify that an English translation faithfully renders a given romanized-Pali passage of the "
    "Dhammapada. Judge only fidelity of meaning (not style). "
    'Return ONLY JSON: {"verdict":"faithful"|"loose"|"wrong","note":"<short reason>"}'
)


async def generate(chunk, sem):
    from app.llm import smart_chat
    v0, v1 = chunk[0][0], chunk[-1][0]
    vno, vname = chunk[0][1], chunk[0][2]
    ref = f"{v0}" if v0 == v1 else f"{v0}–{v1}"
    pali_block = "\n".join(f"({v[0]}) {v[3]}" for v in chunk)
    plain = " ".join(v[3] for v in chunk)
    async with sem:
        r = None
        for attempt in range(4):
            try:
                r = await smart_chat(
                    [{"role": "system", "content": SYS_GEN},
                     {"role": "user", "content": f"Reference: Dhammapada {ref} ({vname})\nPali:\n{pali_block}\n\nReturn JSON."}],
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
                     {"role": "user", "content": f"Pali: {plain[:800]}\n\nEnglish: {data['translation'][:900]}\n\nReturn JSON."}],
                    primary_model="openai/gpt-5.6-luna", temperature=0.0, max_tokens=300)
                break
            except Exception:
                await asyncio.sleep(2 * (attempt + 1))
    vj = _lenient_json(vr) if vr else None
    verdict = (vj or {}).get("verdict", "unknown")
    if verdict == "wrong":
        return ref, f"REJECTED(wrong): {(vj or {}).get('note','')[:70]}", None
    return ref, "ok", build_unit(chunk, ref, data, pali_block, vno, vname, verdict)


def build_unit(chunk, ref, data, pali_block, vno, vname, verdict):
    v0, v1 = chunk[0][0], chunk[-1][0]
    sid = f"DHP_{v0:03d}" if v0 == v1 else f"DHP_{v0:03d}_{v1:03d}"
    title = (data.get("title") or "").strip() or f"{NAME} {ref}"
    themes = [t.strip() for t in (data.get("themes") or []) if t.strip()][:5]
    secref = f"{NAME} {ref} ({vname})"
    return {
        "source_id": sid, "category": "root_text", "work_id": "dhammapada",
        "work_title": NAME, "unit_id": f"dhammapada.faithful_{slugify(sid)}",
        "unit_label": title, "title": title, "unit_type": "verse",
        "sanskrit_devanagari": pali_block,   # romanized Pali lives in this slot by convention
        "translation_literal": (data.get("translation") or "").strip(),
        "commentary": build_commentary(data), "practice": (data.get("practice") or "").strip(),
        "themes": themes, "tags": sorted(set(themes + ["dhammapada", "root_text"])),
        "quality_score": 0, "editorial_score": 0,
        "provenance": {
            "collection": NAME, "section": secref, "original_id": sid,
            "original_reliability": f"SOURCED — {EDITION}",
            "verification": f"translation cross-checked (Luna): {verdict}; original from Fausböll Pali",
            "english_source": "Pratibha original translation (2026), rendered directly from the Pali; voice-informed by public-domain renderings, not derived from any copyrighted translation",
            "original_source": EDITION,
        },
    }


async def run_write(chunks):
    print(f"[Dhammapada] generating {len(chunks)} units ...")
    sem = asyncio.Semaphore(4)
    res = await asyncio.gather(*(generate(ch, sem) for ch in chunks))
    written = 0
    for ref, status, unit in res:
        if status == "ok" and unit:
            p = os.path.join(CANON, f"dhammapada_{slugify(unit['source_id'])}.yml")
            yaml.safe_dump(unit, open(p, "w"), allow_unicode=True, sort_keys=False, width=100)
            written += 1; print(f"  ✓ {ref}")
        else:
            print(f"  · {ref}: {status}")
    print(f"[Dhammapada] wrote {written}/{len(chunks)} units")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dryparse", action="store_true")
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--target", type=int, default=4)
    a = ap.parse_args()
    verses = parse_dhp()
    print(f"parsed {len(verses)} verses; vaggas {max(v[1] for v in verses)}")
    if a.dryparse:
        for v in verses[:3] + verses[-2:]:
            print(f"  {v[0]} ({v[2]}): {v[3][:70]}")
        return
    cov = covered()
    print(f"covered: {len(cov)} verses")
    chunks = plan(verses, cov, a.target)
    print(f"gap chunks: {len(chunks)} covering {sum(len(c) for c in chunks)} verses")
    if a.write:
        asyncio.run(run_write(chunks[:a.limit] if a.limit else chunks))


if __name__ == "__main__":
    main()
