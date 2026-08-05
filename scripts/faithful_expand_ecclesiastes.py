#!/usr/bin/env python3
"""Faithfully expand a new collection: Ecclesiastes (Qoheleth) from the Hebrew.

Same asteya method as the Greek/Epictetus pipelines: the Hebrew ORIGINAL is the
source of record — the public-domain Westminster Leningrad Codex (OpenScriptures
WLC, Masoretic text), NOT a copyrighted or NC-licensed edition. The TRANSLATION is
Pratibha's own, rendered by Terra directly from the Hebrew, recalling the cadence
of the great public-domain renderings (KJV, JPS 1917) without reproducing them;
Luna cross-checks fidelity. Verses grouped into thematic passages within a chapter.
Hebrew stored in the `sanskrit_devanagari` slot by corpus convention (its own
script — no transliteration).
"""
import argparse, asyncio, glob, html, os, re, sys
import yaml

REPO = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha"
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, "scripts"))
from faithful_expand_upanishads import build_commentary, _lenient_json, slugify  # noqa: E402

RAW = os.path.join(REPO, "data/raw_texts/pd/hebrew/ecclesiastes_wlc_openscriptures.xml")
CANON = os.path.join(REPO, "data/canonical/ecclesiastes_qoheleth")
NAME = "Ecclesiastes (Qoheleth)"
EDITION = "Westminster Leningrad Codex (OpenScriptures WLC, public domain Masoretic Hebrew)"


def parse_wlc():
    """Return ordered [(chapter, verse, hebrew_text)] from the OSIS WLC."""
    raw = open(RAW, encoding="utf-8").read()
    out = []
    for vm in re.finditer(r'<verse[^>]*osisID="Eccl\.(\d+)\.(\d+)"[^>]*>(.*?)</verse>', raw, re.S):
        ch, vs = int(vm.group(1)), int(vm.group(2))
        body = vm.group(3)
        # keep word tokens; drop notes/segs markup, then all tags
        body = re.sub(r"<note.*?</note>", " ", body, flags=re.S)
        body = re.sub(r"<[^>]+>", " ", body)
        body = html.unescape(body)
        body = body.replace("/", "")            # WLC morpheme-divider, not part of the text
        body = re.sub(r"[\s]+", " ", body).strip()
        # normalize maqqef and sof-pasuq spacing
        body = body.replace(" ־ ", "־").replace(" ׃", "׃").replace("־ ", "־").strip()
        if body:
            out.append((ch, vs, body))
    return out


def covered():
    cov = set()
    for path in glob.glob(os.path.join(CANON, "*.yml")):
        d = yaml.safe_load(open(path)) or {}
        sec = str((d.get("provenance") or {}).get("section") or d.get("section") or "")
        m = re.search(r"(\d+):(\d+)\s*[–\-—]\s*(?:\d+:)?(\d+)", sec)
        if m:
            c, a, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
            cov.update((c, v) for v in range(a, b + 1)); continue
        m = re.search(r"(\d+):(\d+)\s*$", sec)
        if m:
            cov.add((int(m.group(1)), int(m.group(2))))
    return cov


def plan(verses, cov, target=5):
    uncov = [v for v in verses if (v[0], v[1]) not in cov]
    chunks, cur = [], []
    for v in uncov:
        if cur and (v[0] != cur[-1][0] or v[1] != cur[-1][1] + 1 or len(cur) >= target):
            chunks.append(cur); cur = []
        cur.append(v)
    if cur:
        chunks.append(cur)
    return chunks


SYS_GEN = (
    "You are a scholar-translator building a study unit for the Pratibha corpus from the VERBATIM "
    "Hebrew of Ecclesiastes (Qoheleth), supplied in the Masoretic text with vowel points. The "
    "Hebrew is the source of record; your job is fresh interpretive authorship around it.\n"
    "Produce a FRESH English translation directly from the Hebrew. You may recall the dignified "
    "cadence of the great public-domain renderings (KJV, JPS 1917), but the wording MUST be your "
    "own — never reproduce any existing translation. Translate ONLY what is present; be faithful, "
    "clear, unhurried.\n"
    "Then author: a short evocative title; 3-5 themes; a 2-3 paragraph commentary reading the "
    "passage closely (cite a key Hebrew term or two — e.g. הֶבֶל hevel, עָמָל ʿamal); 3-4 key terms "
    "drawn from words ACTUALLY in the passage (Hebrew term + transliteration + one-line gloss); 3 "
    "cross-tradition resonances, each a REAL recognizable citation + one-sentence parallel + one "
    "honest divergence; one concrete embodied practice.\n"
    'Return ONLY compact JSON: {"title":"","themes":[""],"translation":"","commentary":"",'
    '"key_terms":[{"term":"","gloss":""}],"resonances":[{"citation":"","resonance":"","divergence":""}],'
    '"practice":""}'
)
SYS_VERIFY = (
    "You verify that an English translation faithfully renders a given Hebrew passage of Ecclesiastes "
    "(Masoretic text). Judge only fidelity of meaning (not style). "
    'Return ONLY JSON: {"verdict":"faithful"|"loose"|"wrong","note":"<short reason>"}'
)


async def generate(chunk, sem):
    from app.llm import smart_chat
    c0, v0, c1, v1 = chunk[0][0], chunk[0][1], chunk[-1][0], chunk[-1][1]
    ref = f"{c0}:{v0}" if (c0, v0) == (c1, v1) else f"{c0}:{v0}–{c1}:{v1}"
    heb_block = "\n".join(f"({v[0]}:{v[1]}) {v[2]}" for v in chunk)
    plain = " ".join(v[2] for v in chunk)
    async with sem:
        r = None
        for attempt in range(4):
            try:
                r = await smart_chat(
                    [{"role": "system", "content": SYS_GEN},
                     {"role": "user", "content": f"Reference: Ecclesiastes {ref}\nHebrew:\n{heb_block}\n\nReturn JSON."}],
                    primary_model="openai/gpt-5.6-terra", temperature=0.35,
                    max_tokens=3600 if len(plain) > 700 else 1800)
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
                     {"role": "user", "content": f"Hebrew: {plain[:2600]}\n\nEnglish: {data['translation'][:2600]}\n\nReturn JSON."}],
                    primary_model="openai/gpt-5.6-luna", temperature=0.0, max_tokens=300)
                break
            except Exception:
                await asyncio.sleep(2 * (attempt + 1))
    vj = _lenient_json(vr) if vr else None
    verdict = (vj or {}).get("verdict", "unknown")
    if verdict == "wrong":
        return ref, f"REJECTED(wrong): {(vj or {}).get('note','')[:70]}", None
    return ref, "ok", build_unit(chunk, ref, data, heb_block, verdict)


def build_unit(chunk, ref, data, heb_block, verdict):
    c0, v0, c1, v1 = chunk[0][0], chunk[0][1], chunk[-1][0], chunk[-1][1]
    tag = f"{c0:02d}_{v0:02d}" if (c0, v0) == (c1, v1) else f"{c0:02d}_{v0:02d}_{v1:02d}"
    sid = f"QOH_{tag}"
    title = (data.get("title") or "").strip() or f"{NAME} {ref}"
    themes = [t.strip() for t in (data.get("themes") or []) if t.strip()][:5]
    return {
        "source_id": sid, "category": "root_text", "work_id": "ecclesiastes_qoheleth",
        "work_title": NAME, "unit_id": f"ecclesiastes_qoheleth.faithful_{slugify(sid)}",
        "unit_label": title, "title": title, "unit_type": "passage",
        "sanskrit_devanagari": heb_block,   # Hebrew in the original slot by corpus convention
        "translation_literal": (data.get("translation") or "").strip(),
        "commentary": build_commentary(data), "practice": (data.get("practice") or "").strip(),
        "themes": themes, "tags": sorted(set(themes + ["ecclesiastes_qoheleth", "root_text"])),
        "quality_score": 0, "editorial_score": 0,
        "provenance": {
            "collection": NAME, "section": f"Ecclesiastes {ref}", "original_id": sid,
            "original_reliability": f"SOURCED — {EDITION}",
            "verification": f"translation cross-checked (Luna): {verdict}; original from WLC Hebrew",
            "english_source": "Pratibha original translation (2026), rendered directly from the Hebrew; voice-informed by public-domain renderings (KJV, JPS 1917), not derived from any copyrighted translation",
            "original_source": EDITION,
        },
    }


async def run_write(chunks):
    print(f"[Ecclesiastes] generating {len(chunks)} units ...")
    sem = asyncio.Semaphore(4)
    res = await asyncio.gather(*(generate(ch, sem) for ch in chunks))
    written = 0
    for ref, status, unit in res:
        if status == "ok" and unit:
            p = os.path.join(CANON, f"ecclesiastes_qoheleth_{slugify(unit['source_id'])}.yml")
            yaml.safe_dump(unit, open(p, "w"), allow_unicode=True, sort_keys=False, width=100)
            written += 1; print(f"  ✓ {ref}")
        else:
            print(f"  · {ref}: {status}")
    print(f"[Ecclesiastes] wrote {written}/{len(chunks)} units")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dryparse", action="store_true")
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--target", type=int, default=5)
    a = ap.parse_args()
    verses = parse_wlc()
    print(f"parsed {len(verses)} verses; chapters {sorted(set(c for c,_,_ in verses))}")
    if a.dryparse:
        for v in verses[:3]:
            print(f"  {v[0]}:{v[1]}  {v[2][:60]}")
        return
    cov = covered()
    print(f"covered: {len(cov)} verses")
    chunks = plan(verses, cov, a.target)
    print(f"gap chunks: {len(chunks)} covering {sum(len(c) for c in chunks)} verses")
    if a.write:
        asyncio.run(run_write(chunks[:a.limit] if a.limit else chunks))


if __name__ == "__main__":
    main()
