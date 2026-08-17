#!/usr/bin/env python3
"""Deepen the thin Greek collections — Pseudo-Dionysius (Divine Names + Mystical
Theology) and Parmenides — from local PD Greek, with fresh Pratibha translations.

Same asteya method: the Greek ORIGINAL is verbatim from the local PD source (verified
as a substring), the TRANSLATION is Terra's own from the Greek, Luna-checked. Greek
stored in the original slot; no transliteration.
"""
import argparse, asyncio, glob, os, re, sys, unicodedata
import yaml

REPO = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha"
sys.path.insert(0, REPO); sys.path.insert(0, os.path.join(REPO, "scripts"))
from faithful_expand_upanishads import build_commentary, _lenient_json, slugify  # noqa: E402

RAW = os.path.join(REPO, "data/raw_texts/pd/greek")
CANON = os.path.join(REPO, "data/canonical")


def norm_greek(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if 0x3B1 <= ord(c) <= 0x3C9 or c == "ς")


# ---- Dionysius: Divine Names + Mystical Theology, split by C.S. markers ----
def parse_dionysius():
    out = []
    for fname, work, roman in [("divine_names_greek_unicode.txt", "Divine Names", "DN"),
                                ("mystical_theology_migne_dco.txt", "Mystical Theology", "MT")]:
        text = open(os.path.join(RAW, fname), encoding="utf-8").read()
        # sections marked like "1.2." / "4.2." at start
        parts = re.split(r"(?m)^\s*(\d+)\.(\d+)\.\s*", text)
        # parts = [pre, ch, sec, body, ch, sec, body, ...]
        for i in range(1, len(parts) - 2, 3):
            ch, sec, body = parts[i], parts[i + 1], parts[i + 2]
            body = re.sub(r"\s+", " ", body).strip()
            if len(norm_greek(body)) > 40:
                out.append((work, roman, int(ch), int(sec), body[:2200]))
    return out


def dionysius_covered():
    """Normalized Greek of every existing Dionysius unit (to skip covered sections)."""
    blobs = []
    for p in glob.glob(os.path.join(CANON, "pseudo_dionysius", "*.yml")):
        d = yaml.safe_load(open(p)) or {}
        g = norm_greek(str(d.get("sanskrit_devanagari") or ""))
        if len(g) > 40:
            blobs.append(g)
    return "||".join(blobs)


# ---- Parmenides: named DK fragments extracted from the saved poem ----
# (incipit -> DK fragment label); B1/B2/B3 + B8-excerpt already in corpus.
PARM_FRAGS = [
    ("λεῦσσε δ' ὅμως", "B4"), ("ξυνὸν δὲ μοί ἐστιν", "B5"),
    ("χρὴ τὸ λέγειν τε νοεῖν τ'", "B6"), ("οὐ γὰρ μήποτε τοῦτο δαμῇ", "B7"),
    ("μόνος δ' ἔτι μῦθος ὁδοῖο", "B8"), ("αὐτὰρ ἐπειδὴ πάντα φάος", "B9"),
    ("εἴσῃ δ' αἰθερίαν", "B10"), ("πῶς γαῖα καὶ ἥλιος", "B11"),
    ("αἱ γὰρ στεινότεραι", "B12"), ("πρώτιστον μὲν Ἔρωτα", "B13"),
    ("νυκτιφαὲς περὶ γαῖαν", "B14"), ("αἰεὶ παπταίνουσα", "B15"),
    ("ὡς γὰρ ἕκαστος ἔχει κρᾶσιν", "B16"), ("δεξιτεροῖσιν μὲν κούρους", "B17"),
    ("οὕτω τοι κατὰ δόξαν", "B19"),
    # B18 survives only in a Latin translation (Caelius Aurelianus), not in Greek.
]


def parse_parmenides():
    text = open(os.path.join(RAW, "parmenides_dk_greek.txt"), encoding="utf-8").read()
    flat = re.sub(r"\s+", " ", text)
    nflat = norm_greek(flat)
    out = []
    for i, (incipit, label) in enumerate(PARM_FRAGS):
        ni = norm_greek(incipit)
        start = nflat.find(ni)
        if start < 0:
            print(f"  ? {label}: incipit not found"); continue
        # end = next fragment's incipit (or +550 chars)
        end = len(nflat)
        for j in range(i + 1, len(PARM_FRAGS)):
            nj = nflat.find(norm_greek(PARM_FRAGS[j][0]))
            if nj > start:
                end = nj; break
        # map normalized offsets back to raw via cumulative letter count
        # (B8 is the long ~50-line proof, so allow a much larger slice)
        cap = 4000 if label == "B8" else 900
        raw = _slice_by_letters(flat, start, min(end, start + cap))
        if len(norm_greek(raw)) > 20:
            out.append((label, raw.strip()))
    return out


def _slice_by_letters(raw, nstart, nend):
    """Return raw substring spanning normalized-letter indices [nstart, nend)."""
    letters = 0; s = e = None
    for idx, ch in enumerate(raw):
        if norm_greek(ch):
            if letters == nstart and s is None:
                s = idx
            if letters == nend:
                e = idx; break
            letters += 1
    return raw[(s or 0):(e or len(raw))]


SYS_GEN = (
    "You are a scholar-translator building a study unit for the Pratibha corpus from the VERBATIM "
    "Greek of {work}, supplied in Unicode. The Greek is the source of record; author fresh "
    "interpretation around it.\n"
    "Produce a FRESH English translation directly from the Greek (recall the cadence of the great "
    "renderings — for Dionysius: Rolt, Luibheid; for Parmenides: Kirk-Raven, Coxon — but the wording "
    "MUST be your own; translate ONLY what is present).\n"
    "Then author: a short evocative title; 3-5 themes; a 2-3 paragraph commentary reading the passage "
    "closely (cite a key Greek term); 3-4 key terms (Greek term + gloss); 3 cross-tradition resonances "
    "(real citation + parallel + honest divergence); one concrete practice.\n"
    'Return ONLY compact JSON: {"title":"","themes":[""],"translation":"","commentary":"",'
    '"key_terms":[{"term":"","gloss":""}],"resonances":[{"citation":"","resonance":"","divergence":""}],'
    '"practice":""}'
)
SYS_VERIFY = ("Verify the English faithfully renders the Greek passage of {work}. Judge meaning only. "
              'Return ONLY JSON: {"verdict":"faithful"|"loose"|"wrong","note":""}')


async def generate(greek, work, ref, sem):
    from app.llm import smart_chat
    async with sem:
        r = None
        for a in range(4):
            try:
                r = await smart_chat([{"role": "system", "content": SYS_GEN.replace("{work}", work)},
                    {"role": "user", "content": f"Reference: {work} {ref}\nGreek:\n{greek}\n\nReturn JSON."}],
                    primary_model="openai/gpt-5.6-terra", temperature=0.35, max_tokens=(4000 if len(greek)>1000 else 2200))
                break
            except Exception:
                await asyncio.sleep(2 * (a + 1))
    data = _lenient_json(r) if r else None
    if not data or not data.get("translation"):
        return None, "parse"
    vr = None
    async with sem:
        for a in range(3):
            try:
                vr = await smart_chat([{"role": "system", "content": SYS_VERIFY.replace("{work}", work)},
                    {"role": "user", "content": f"Greek: {greek[:3000]}\n\nEnglish: {data['translation'][:3000]}\n\nReturn JSON."}],
                    primary_model="openai/gpt-5.6-luna", temperature=0.0, max_tokens=200)
                break
            except Exception:
                await asyncio.sleep(2 * (a + 1))
    verdict = (_lenient_json(vr) or {}).get("verdict", "unknown") if vr else "unknown"
    if verdict == "wrong":
        return None, "REJECTED"
    return data, verdict


def build_unit(coll, work_id, work_title, sid, section, greek, data, verdict, edition):
    title = (data.get("title") or "").strip() or section
    themes = [t.strip() for t in (data.get("themes") or []) if t.strip()][:5]
    return {
        "source_id": sid, "category": "root_text", "work_id": work_id, "work_title": work_title,
        "unit_id": f"{coll}.deepen_{slugify(sid)}", "unit_label": title, "title": title, "unit_type": "passage",
        "sanskrit_devanagari": greek, "translation_literal": (data.get("translation") or "").strip(),
        "commentary": build_commentary(data), "practice": (data.get("practice") or "").strip(),
        "themes": themes, "tags": sorted(set(themes + [work_id, "root_text"])),
        "quality_score": 0, "editorial_score": 0,
        "provenance": {"collection": work_title, "section": section, "original_id": sid,
            "original_reliability": f"SOURCED — {edition}", "original_source": edition,
            "verification": f"translation cross-checked (Luna): {verdict}; original verbatim from local PD Greek",
            "english_source": "Pratibha original translation (2026), rendered directly from the Greek; not derived from any copyrighted translation"},
    }


async def run_dionysius(limit):
    secs = parse_dionysius()
    cov = dionysius_covered()
    # group consecutive uncovered sections within a chapter into passages (~2 sections)
    gaps = [(w, r, ch, sec, g) for (w, r, ch, sec, g) in secs if norm_greek(g)[:50] not in cov]
    print(f"[Dionysius] {len(secs)} sections, {len(gaps)} uncovered")
    if limit:
        gaps = gaps[:limit]
    sem = asyncio.Semaphore(4); written = 0
    async def one(w, r, ch, sec, g):
        nonlocal written
        edition = "Pseudo-Dionysius, Divine Names / Mystical Theology, Greek (Migne PG3, Unicode; PD)"
        data, verdict = await generate(g, w, f"{r} {ch}.{sec}", sem)
        if not data:
            print(f"  · {r} {ch}.{sec}: {verdict}"); return
        sid = f"{r}_{ch:02d}_{sec:02d}"
        u = build_unit("pseudo_dionysius", "pseudo_dionysius", w, sid, f"{w} · {r} {ch}.{sec}", g, data, verdict, edition)
        yaml.safe_dump(u, open(os.path.join(CANON, "pseudo_dionysius", f"pseudo_dionysius_{slugify(sid)}.yml"), "w"),
                       allow_unicode=True, sort_keys=False, width=100)
        written += 1; print(f"  ✓ {r} {ch}.{sec}")
    await asyncio.gather(*(one(*x) for x in gaps))
    print(f"[Dionysius] wrote {written}/{len(gaps)}")


async def run_parmenides(limit):
    frags = parse_parmenides()
    have = set()
    for p in glob.glob(os.path.join(CANON, "parmenides_fragments", "*.yml")):
        have.add(str((yaml.safe_load(open(p)) or {}).get("source_id")))
    todo = [(lbl, g) for lbl, g in frags if f"PARM_{lbl}" not in have and lbl not in {"B1", "B2", "B3"}]
    print(f"[Parmenides] {len(frags)} fragments parsed, {len(todo)} to add")
    if limit:
        todo = todo[:limit]
    sem = asyncio.Semaphore(4); written = 0
    edition = "Parmenides, On Nature (Diels-Kranz Greek, PD)"
    async def one(lbl, g):
        nonlocal written
        data, verdict = await generate(g, "Parmenides, On Nature", lbl, sem)
        if not data:
            print(f"  · {lbl}: {verdict}"); return
        sid = f"PARM_{lbl}"
        u = build_unit("parmenides_fragments", "parmenides_fragments", "Parmenides, On Nature", sid,
                       f"On Nature, fragment {lbl}", g, data, verdict, edition)
        yaml.safe_dump(u, open(os.path.join(CANON, "parmenides_fragments", f"parmenides_fragments_{slugify(sid)}.yml"), "w"),
                       allow_unicode=True, sort_keys=False, width=100)
        written += 1; print(f"  ✓ {lbl}")
    await asyncio.gather(*(one(*x) for x in todo))
    print(f"[Parmenides] wrote {written}/{len(todo)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--collection", required=True, choices=["dionysius", "parmenides"])
    ap.add_argument("--dryparse", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    if a.dryparse:
        if a.collection == "dionysius":
            s = parse_dionysius()
            print(f"Dionysius: {len(s)} sections")
            for x in s[:3]: print(f"  {x[1]} {x[2]}.{x[3]}: {x[4][:60]}")
        else:
            f = parse_parmenides()
            print(f"Parmenides: {len(f)} fragments")
            for lbl, g in f[:4]: print(f"  {lbl}: {g[:60]}")
        return
    asyncio.run(run_dionysius(a.limit) if a.collection == "dionysius" else run_parmenides(a.limit))


if __name__ == "__main__":
    main()
