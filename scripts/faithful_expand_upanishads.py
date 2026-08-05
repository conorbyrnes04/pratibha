#!/usr/bin/env python3
"""Faithfully expand Upanishad collections from REAL GRETIL IAST originals.

Principle (asteya): the ORIGINAL is the source of record, taken verbatim from a
verified public-domain edition (GRETIL). The TRANSLATION is Pratibha's own fresh
rendering — Terra translates FROM the real IAST, recalling the cadence of the
great renderings without copying any of them. Commentary / key terms / resonances
/ practice are authored interpretation. Devanagari is transliterated from the IAST
(deterministic, round-trip verified). No model ever supplies the original.

Usage:
  python faithful_expand.py --collection katha --dryparse      # parse only
  python faithful_expand.py --collection katha --plan          # show gap chunks
  python faithful_expand.py --collection katha --write         # generate + write
"""
import argparse, asyncio, glob, json, os, re, sys
import yaml

REPO = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha"
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, "scripts"))
from lib_iast_to_deva import iast_to_deva  # noqa: E402

RAW = os.path.join(REPO, "data/raw_texts/pd/indian")
CANON = os.path.join(REPO, "data/canonical")

# collection config. `marker` captures (chapter, verse) or, when `single`, just
# (verse) with chapter fixed to 1. Only clean mūla e-texts are listed — the
# Māṇḍūkya/Gauḍapāda GRETIL file is mūla+Śaṅkara-bhāṣya interleaved and is NOT
# usable for verse extraction, so it is deliberately excluded.
COLLS = {
    "katha": dict(
        canon="katha_upanishad", raw="katha_upanishad_gretil_iast.txt",
        marker=r"//\s*KaU[_ ]?(\d+)[.,](\d+)\s*//", single=False, cover_id=None,
        name="Kaṭha Upaniṣad", work_id="katha_upanishad",
        edition="GRETIL Kaṭhopaniṣad e-text (after Olivelle, The Early Upaniṣads, 1998)"),
    "svetasvatara": dict(
        canon="svetasvatara_upanishad", raw="svetasvatara_upanishad_gretil_iast.txt",
        marker=r"(?<![\w.])SvetUp[_ ]?(\d+)[.,](\d+)(?![\w])", single=False,
        cover_id=r"SU[_ ]?(\d+)[_ ](\d+)",
        name="Śvetāśvatara Upaniṣad", work_id="svetasvatara_upanishad",
        edition="GRETIL Śvetāśvataropaniṣad e-text (Limaye–Vadekar, Eighteen Principal Upaniṣads, 1958)"),
    "isavasya": dict(
        canon="isavasya_upanishad", raw="isavasya_upanishad_gretil_iast.txt",
        marker=r"\|\|\s*IsUp[_ ]?(\d+)\s*\|\|", single=True, cover_id=r"ISA[_ ]?0*(\d+)",
        name="Īśāvāsya Upaniṣad", work_id="isavasya_upanishad",
        edition="GRETIL Īśāvāsyopaniṣad e-text"),
    "mmk": dict(
        canon="nagarjuna_mulamadhyamakakarika", raw="nagarjuna_mmk_gretil_iast.txt",
        marker=r"//\s*MMK[_ ]?(\d+)[.,](\d+)\s*//", single=False,
        cover_id=r"MMK[_ ]?(\d+)[_ ](\d+)", sid_prefix="MMK",
        name="Mūlamadhyamakakārikā", work_id="nagarjuna_mulamadhyamakakarika",
        edition="GRETIL Mūlamadhyamakakārikā e-text (Nāgārjuna; de Jong / Ye critical readings)"),
    # Diamond Sūtra — prose, one unit per traditional section (|| N ||, 1..32)
    "vajracchedika": dict(
        canon="vajracchedika_diamond_sutra", raw="vajracchedika_gretil_iast.txt",
        marker=r"\|\|\s*(\d+)\s*\|\|", single=True, cover_id=None, sid_prefix="VAJ",
        prose=True,
        name="Vajracchedikā Prajñāpāramitā", work_id="vajracchedika_diamond_sutra",
        edition="GRETIL Vajracchedikā Prajñāpāramitā e-text (Conze/Vaidya ed.)"),
}

# a line of the source that is genuine IAST verse text (not header/English)
IAST_LINE = re.compile(r"^[\sa-zāīūṛṝḷḹṅñṭḍṇśṣṃḥ'/|.,;()\d-]+$")
DIACRITIC = re.compile(r"[āīūṛṝḷḹṅñṭḍṇśṣṃḥ]")
# single word that is a title/colophon token, e.g. "kaṭhopaniṣat"
COLOPHON = re.compile(r"^[a-zāīūṛṝḷṅñṭḍṇśṣṃḥ]*opaniṣa[dt]$")
# GRETIL diacritics-legend / grammar-guide words (carry diacritics but are English)
LEGEND = re.compile(r"(?i)\b(long|short|vocalic|velar|palatal|retroflex|dental|labial|"
                    r"nasal|anusvara|anusvāra|visarga|visarj|guttural|sibilant|aspirate|semivowel)\b")


def _iast_only(span: str) -> str:
    """Keep only genuine IAST verse lines from a span. English header prose passes
    the ASCII IAST charset test, so additionally require a Sanskrit diacritic or a
    pada-slash on the line — header sentences have neither."""
    out = []
    for ln in span.splitlines():
        s = ln.strip()
        if not s or not IAST_LINE.match(s):
            continue
        if not (DIACRITIC.search(s) or "/" in s):
            continue
        if COLOPHON.match(s) or LEGEND.search(s):  # drop title/colophon + legend
            continue
        # drop vallī / adhyāya section colophons (e.g. "iti pañcamī vallī")
        s = re.sub(r"//?\s*iti\s+[a-zāīūṛṝḷṅñṭḍṇśṣṃḥ\x27 ]*?(?:vall[īi]|adhyāyaḥ?|khaṇḍaḥ?)\s*//?", " ", s).strip()
        s = re.sub(r"[a-zāīūṛṝḷṅñṭḍṇśṣṃḥ]+o \x27?adhyāyaḥ", " ", s).strip()
        if not s or not (DIACRITIC.search(s) or "/" in s):
            continue
        out.append(s)
    return " ".join(out).strip()


def parse_gretil(cfg) -> list[tuple[int, int, str]]:
    """Return [(chapter, verse, iast_text)] in order."""
    if cfg.get("prose"):
        return _parse_prose_sections(cfg)
    text = open(os.path.join(RAW, cfg["raw"]), encoding="utf-8").read()
    marker = re.compile(cfg["marker"])
    out = []
    last = 0
    for m in marker.finditer(text):
        span = text[last:m.start()]
        iast = _iast_only(span)
        iast = re.sub(r"\s*\|\|?\s*$", "", iast).strip()
        if iast:
            if cfg["single"]:
                ch, vs = 1, int(m.group(1))
            else:
                ch, vs = int(m.group(1)), int(m.group(2))
            out.append((ch, vs, iast))
        last = m.end()
    return out


def _parse_prose_sections(cfg) -> list[tuple[int, int, str]]:
    """Prose sūtra split into traditional sections marked `|| N ||`. Handles the
    Vajracchedikā quirk where section 26's gāthā is sub-numbered (…25, 1, 2, 27…):
    a number that is not the expected next section starts a merge-run that is
    folded into one section. Strips the header/title before 'evaṃ mayā śrutam'."""
    text = open(os.path.join(RAW, cfg["raw"]), encoding="utf-8").read()
    marker = re.compile(cfg["marker"])

    def clean_prose(span):
        # keep IAST prose (which has ? - ' digits); drop only header/English lines
        keep = []
        for ln in span.splitlines():
            s = ln.strip()
            if not s or LEGEND.search(s):
                continue
            if not DIACRITIC.search(s):        # header/URL/English lines lack diacritics
                continue
            keep.append(s)
        s = re.sub(r"\s+", " ", " ".join(keep)).strip()
        return re.sub(r"\s*\|\|?\s*$", "", s).strip()

    raw_segs, last = [], 0
    for m in marker.finditer(text):
        raw_segs.append((int(m.group(1)), clean_prose(text[last:m.start()])))
        last = m.end()
    # drop title/URL/invocation before the sūtra proper
    if raw_segs:
        k0, s0 = raw_segs[0]
        cut = s0.find("evaṃ mayā")
        raw_segs[0] = (k0, s0[cut:].strip() if cut >= 0 else s0)
    out, sec, i = [], 0, 0
    while i < len(raw_segs):
        k, seg = raw_segs[i]
        sec += 1
        if k == sec:
            if seg:
                out.append((1, sec, seg))
            i += 1
        else:                                   # reset-run (gāthā): merge until k jumps past sec
            buf = []
            while i < len(raw_segs) and raw_segs[i][0] <= sec:
                if raw_segs[i][1]:
                    buf.append(raw_segs[i][1])
                i += 1
            if buf:
                out.append((1, sec, " | ".join(buf)))
    return out


# ---- coverage ----
def covered_verses(cfg) -> set[tuple[int, int]]:
    """Verse (chapter, verse) pairs already covered by existing units, read from
    each unit's provenance.section range like 'Kaṭha Upaniṣad 2.1–2.6'."""
    covered = set()
    rng = re.compile(r"(\d+)\.(\d+)\s*[–\-—]\s*(\d+)\.(\d+)")
    single = re.compile(r"(\d+)\.(\d+)\s*$")
    # source_id like SU_03_08, ISA_001, MMK_01_02 or a RANGE MMK_01_02_06
    cover_id = re.compile((cfg["cover_id"] or "") + r"(?:[_ ](\d+))?") if cfg.get("cover_id") else None
    for path in glob.glob(os.path.join(CANON, cfg["canon"], "*.yml")):
        d = yaml.safe_load(open(path)) or {}
        prov = d.get("provenance") if isinstance(d.get("provenance"), dict) else {}
        # (a) per-verse (or verse-range) source_id
        matched = False
        if cover_id:
            sid = str(d.get("source_id") or (prov or {}).get("original_id") or "")
            m = cover_id.search(sid)
            if m:
                g = [x for x in m.groups()]
                if cfg["single"]:                      # ISA_001 -> (1, v[, vend])
                    ch, v1 = 1, int(g[0]); vend = int(g[1]) if len(g) > 1 and g[1] else v1
                else:                                  # MMK_01_02[_06] -> (ch, v1[, vend])
                    ch, v1 = int(g[0]), int(g[1]); vend = int(g[2]) if len(g) > 2 and g[2] else v1
                covered.update((ch, v) for v in range(v1, vend + 1))
                matched = True
        if matched:
            continue
        # (b) thematic section range like 'Kaṭha Upaniṣad 2.1–2.6'
        sec = str((prov or {}).get("section") or "") or str(d.get("section") or "")
        m = rng.search(sec)
        if m:
            c1, v1, c2, v2 = map(int, m.groups())
            if c1 == c2:
                covered.update((c1, v) for v in range(v1, v2 + 1))
            else:
                covered.add((c1, v1)); covered.add((c2, v2))
            continue
        m = single.search(sec)
        if m:
            covered.add((int(m.group(1)), int(m.group(2))))
            continue
        # (c) single-number section for single=True collections, e.g. 'Vajracchedikā … 7'
        if cfg.get("single"):
            m = re.search(r"(\d+)\s*$", sec)
            if m:
                covered.add((1, int(m.group(1))))
    return covered


def plan_chunks(cfg, verses, covered, target=5):
    """Group uncovered verses into contiguous thematic passages of ~`target`
    verses, never crossing a chapter boundary."""
    uncovered = [(c, v, t) for (c, v, t) in verses if (c, v) not in covered]
    chunks, cur = [], []
    for item in uncovered:
        if cur and (item[0] != cur[-1][0] or item[1] != cur[-1][1] + 1 or len(cur) >= target):
            chunks.append(cur); cur = []
        cur.append(item)
    if cur:
        chunks.append(cur)
    return chunks


# ---- Devanagari assembly ----
def iast_to_deva_verse(iast: str) -> str:
    """Transliterate one verse/passage's IAST to Devanagari, mapping the pada or
    sentence break (/ or single |) to a daṇḍa. Deterministic transliterator."""
    padas = [p.strip() for p in re.split(r"[/|]", iast) if p.strip()]
    return " ।\n".join(iast_to_deva(p) for p in padas)


def assemble_original(chunk):
    """Join the chunk's verses into IAST and Devanagari blocks, each verse closed
    with its verse number (॥ n ॥)."""
    DIG = str.maketrans("0123456789", "०१२३४५६७८९")
    iast_lines, deva_lines = [], []
    for c, v, t in chunk:
        body = re.sub(r"\s+", " ", t).strip().rstrip("/").strip()
        iast_lines.append(f"{body} || {v} ||")
        deva_lines.append(f"{iast_to_deva_verse(body)} ॥ {str(v).translate(DIG)} ॥")
    return "\n".join(iast_lines), "\n".join(deva_lines)


# ---- generation (Terra) + verification (Luna) ----
SYS_GEN = (
    "You are a scholar-translator building a study unit for the Pratibha corpus from the "
    "VERBATIM Sanskrit original of {name}, supplied in IAST. The original is the source of "
    "record; your job is fresh interpretive authorship around it.\n"
    "Produce a FRESH English translation directly from the Sanskrit. You may recall the "
    "dignified cadence of the great public-domain renderings (Müller, Radhakrishnan, "
    "Olivelle), but the wording MUST be your own — never reproduce any existing translation. "
    "Be faithful to the Sanskrit, clear, and unhurried. CRITICAL: translate ONLY the Sanskrit "
    "given — render exactly what is present and nothing more. Do NOT add, expand, complete, or "
    "import passages from elsewhere in the work, even if you recognize the text and it seems "
    "elliptical, abbreviated, or repetitive. If the passage is short or terse, keep it so. "
    "Buddhist ellipsis markers (pe, peyālam, yāvat, la, …) mark elided repetition — render "
    "them tersely as written; do NOT expand them into the full formula.\n"
    "Then author: a short evocative title; 3-5 themes; a 2-3 paragraph commentary that reads "
    "the passage closely (name what the Sanskrit actually says and does); 3-4 key terms drawn "
    "from words ACTUALLY in the verse, each with a one-line gloss; 3 cross-tradition resonances, "
    "each a REAL recognizable citation (text/figure) + a one-sentence parallel + one honest "
    "divergence; and one concrete embodied practice.\n"
    'Return ONLY compact JSON: {"title":"","themes":[""],"translation":"","commentary":"",'
    '"key_terms":[{"term":"","gloss":""}],"resonances":[{"citation":"","resonance":"","divergence":""}],'
    '"practice":""}'
)

SYS_VERIFY = (
    "You verify that an English translation faithfully renders a given Sanskrit (IAST) passage "
    "of {name}. Judge only fidelity of meaning (not style). "
    'Return ONLY JSON: {"verdict":"faithful"|"loose"|"wrong","note":"<short reason>"}'
)


def _lenient_json(r):
    s = re.sub(r"^```(?:json)?|```$", "", r.strip(), flags=re.M).strip()
    m = re.search(r"\{.*\}", s, re.S)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            pass
    return None


def build_commentary(data):
    body = data.get("commentary", "").strip()
    kts = [k for k in data.get("key_terms", []) if k.get("term") and (k.get("gloss") or k.get("definition"))]
    if kts:
        body += "\n\nKey Terms\n\n" + "\n".join(
            f"**{k['term'].strip()}** — {(k.get('gloss') or k.get('definition')).strip()}" for k in kts[:4])
    res = [r for r in data.get("resonances", []) if r.get("citation") and r.get("resonance")]
    if res:
        lines = []
        for r in res[:3]:
            b = r["resonance"].strip()
            if r.get("divergence", "").strip():
                b += f" Divergence: {r['divergence'].strip()}"
            lines.append(f"**{r['citation'].strip()}:** {b}")
        body += "\n\nCross-Tradition Resonances\n\n" + "\n".join(lines)
    return body


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:40]


async def generate(chunk, cfg, sem, verify=True):
    from app.llm import smart_chat
    c0, v0 = chunk[0][0], chunk[0][1]
    c1, v1 = chunk[-1][0], chunk[-1][1]
    ref = f"{c0}.{v0}" if len(chunk) == 1 else f"{c0}.{v0}–{c1}.{v1}"
    iast_block, deva_block = assemble_original(chunk)
    plain_iast = " ".join(re.sub(r"\|\|.*?\|\|", "", t) for _, _, t in chunk).strip()
    async with sem:
        r = None
        for attempt in range(4):
            try:
                r = await smart_chat(
                    [{"role": "system", "content": SYS_GEN.replace("{name}", cfg["name"])},
                     {"role": "user", "content": f"Reference: {cfg['name']} {ref}\nSanskrit (IAST):\n{iast_block}\n\nReturn JSON."}],
                    primary_model="openai/gpt-5.6-terra", temperature=0.4,
                    max_tokens=5200 if len(iast_block) > 2500 else (3600 if len(iast_block) > 700 else 1800))
                break
            except Exception:
                await asyncio.sleep(2 * (attempt + 1))
    if r is None:
        return ref, "ERR", None
    data = _lenient_json(r)
    if not data or not data.get("translation"):
        return ref, "parse", None
    verification = "authored from verified GRETIL original; translation Pratibha's own"
    if verify:
        vr = None
        async with sem:
            for attempt in range(3):
                try:
                    vr = await smart_chat(
                        [{"role": "system", "content": SYS_VERIFY.replace("{name}", cfg["name"])},
                         {"role": "user", "content": f"Sanskrit (IAST): {plain_iast[:6500]}\n\nEnglish: {data['translation'][:6500]}\n\nReturn JSON."}],
                        primary_model="openai/gpt-5.6-luna", temperature=0.0, max_tokens=300)
                    break
                except Exception:
                    await asyncio.sleep(2 * (attempt + 1))
        vj = _lenient_json(vr) if vr else None
        verdict = (vj or {}).get("verdict", "unknown")
        if verdict == "wrong":
            return ref, f"REJECTED(wrong): {(vj or {}).get('note','')[:80]}", None
        verification = f"translation cross-checked (Luna): {verdict}; original from GRETIL"
    unit = build_unit(chunk, cfg, ref, data, deva_block, iast_block, verification)
    return ref, "ok", unit


def build_unit(chunk, cfg, ref, data, deva_block, iast_block, verification):
    c0, v0 = chunk[0][0], chunk[0][1]
    c1, v1 = chunk[-1][0], chunk[-1][1]
    pfx = cfg.get("sid_prefix") or cfg["work_id"][:3].upper()
    if cfg["single"]:
        sid = f"{pfx}_{v0:03d}" if len(chunk) == 1 else f"{pfx}_{v0:03d}_{v1:03d}"
        secref = f"{cfg['name']} {v0}" if len(chunk) == 1 else f"{cfg['name']} {v0}–{v1}"
    else:
        tag = f"{c0:02d}_{v0:02d}" if len(chunk) == 1 else f"{c0:02d}_{v0:02d}_{v1:02d}"
        sid = f"{pfx}_{tag}"
        secref = f"{cfg['name']} {ref}"
    title = data.get("title", "").strip() or secref
    uid = f"{cfg['work_id']}.faithful_{slugify(sid)}"
    themes = [t.strip() for t in (data.get("themes") or []) if t.strip()][:5]
    return {
        "source_id": sid, "category": "root_text", "work_id": cfg["work_id"],
        "work_title": cfg["name"], "unit_id": uid, "unit_label": title, "title": title,
        "unit_type": "verse",
        "sanskrit_devanagari": deva_block, "sanskrit_iast": iast_block,
        "translation_literal": data["translation"].strip(),
        "commentary": build_commentary(data),
        "practice": data.get("practice", "").strip(),
        "themes": themes, "tags": sorted(set(themes + [cfg["work_id"], "root_text"])),
        "quality_score": 0, "editorial_score": 0,
        "provenance": {
            "collection": cfg["name"], "section": secref, "original_id": sid,
            "original_reliability": f"SOURCED — {cfg['edition']}; Devanagari transliterated from IAST (round-trip verified)",
            "verification": verification,
            "english_source": "Pratibha original translation (2026), rendered directly from the Sanskrit; voice-informed by public-domain renderings, not derived from any copyrighted translation",
            "original_source": cfg["edition"],
        },
    }


async def run_write(cfg, name, limit, target, no_verify):
    verses = parse_gretil(cfg)
    covered = covered_verses(cfg)
    chunks = plan_chunks(cfg, verses, covered, target)
    if limit:
        chunks = chunks[:limit]
    print(f"[{name}] generating {len(chunks)} units (verify={not no_verify}) ...")
    sem = asyncio.Semaphore(4)
    results = await asyncio.gather(*(generate(ch, cfg, sem, verify=not no_verify) for ch in chunks))
    outdir = os.path.join(CANON, cfg["canon"])
    written = 0
    for ref, status, unit in results:
        if status == "ok" and unit:
            path = os.path.join(outdir, f"{cfg['canon']}_{slugify(unit['source_id'])}.yml")
            yaml.safe_dump(unit, open(path, "w"), allow_unicode=True, sort_keys=False, width=100)
            written += 1
            print(f"  ✓ {ref} -> {os.path.basename(path)}")
        else:
            print(f"  · {ref}: {status}")
    print(f"[{name}] wrote {written}/{len(chunks)} units")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--collection", required=True, choices=list(COLLS))
    ap.add_argument("--dryparse", action="store_true")
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--no-verify", action="store_true")
    ap.add_argument("--target", type=int, default=5)
    args = ap.parse_args()
    cfg = COLLS[args.collection]
    if args.write:
        asyncio.run(run_write(cfg, args.collection, args.limit, args.target, args.no_verify))
        return
    verses = parse_gretil(cfg)
    print(f"[{args.collection}] parsed {len(verses)} verses; "
          f"chapters {sorted(set(c for c,_,_ in verses))}")
    if args.dryparse:
        for c, v, t in verses[:4]:
            print(f"  {c}.{v}: {t[:90]}")
        return
    covered = covered_verses(cfg)
    print(f"  covered: {len(covered)} verses")
    chunks = plan_chunks(cfg, verses, covered, args.target)
    tot = sum(len(c) for c in chunks)
    print(f"  gap chunks: {len(chunks)} covering {tot} uncovered verses")
    if args.plan:
        for ch in chunks:
            print(f"    {ch[0][0]}.{ch[0][1]}–{ch[-1][0]}.{ch[-1][1]}  ({len(ch)} vv)")


if __name__ == "__main__":
    main()
