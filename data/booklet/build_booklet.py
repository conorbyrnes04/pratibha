#!/usr/bin/env python3
"""Build the Himalayan Retreat Booklet (55 verses) from the Pratibha canonical corpus.

Reads data/canonical/index.jsonl (source of truth; no invented text) and emits:
  - himalaya_retreat_booklet.md      (primary manuscript)
  - docx_ready.html                  (Word / Google Docs import)
  - booklet_indesign.html            (semantic h1/h2 + verse classes for InDesign)

Run from repo root:  python3 data/booklet/build_booklet.py
"""
import json, re, html, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INDEX = os.path.join(ROOT, "data/canonical/index.jsonl")
OUTDIR = os.path.join(ROOT, "data/booklet")

# ---------------------------------------------------------------------------
# Source-display names per collection (Author, Work)
# ---------------------------------------------------------------------------
SOURCE = {
    "isavasya_upanishad": "Īśāvāsya Upaniṣad",
    "chāndogya_upaniṣad": "Chāndogya Upaniṣad",
    "siva_sutra": "Vasugupta, Śiva Sūtra",
    "pratyabhijnahrdayam": "Kṣemarāja, Pratyabhijñāhṛdayam",
    "tao_te_ching": "Laozi, Dào Dé Jīng",
    "astavakra_gita": "Aṣṭāvakra Gītā",
    "tantrasara": "Abhinavagupta, Tantrasāra",
    "milarepa_songs": "Milarepa, The Hundred Thousand Songs",
    "yoga_spandakarika": "Vasugupta / Kallaṭa, Spandakārikā",
    "svetasvatara_upanishad": "Śvetāśvatara Upaniṣad",
    "the_book_of_chuang_tzu": "Zhuāngzǐ",
    "shantideva_bodhicaryavatara": "Śāntideva, Bodhicaryāvatāra",
    "patañjali_yoga_sūtras": "Patañjali, Yoga Sūtras",
    "heart_sutra": "Prajñāpāramitā-hṛdaya (Heart Sūtra)",
    "nagarjuna_mulamadhyamakakarika": "Nāgārjuna, Mūlamadhyamakakārikā",
    "mandukya_upanishad_and_gaudapada_karika": "Māṇḍūkya Upaniṣad & Gauḍapāda Kārikā",
    "tilopa_mahamudra": "Tilopa, Mahāmudrā Upadeśa (Gaṅgā-mā)",
}

TRADITION = {
    "isavasya_upanishad": "Upaniṣads", "chāndogya_upaniṣad": "Upaniṣads",
    "svetasvatara_upanishad": "Upaniṣads", "mandukya_upanishad_and_gaudapada_karika": "Upaniṣads",
    "siva_sutra": "Kashmiri Śaivism", "pratyabhijnahrdayam": "Kashmiri Śaivism",
    "tantrasara": "Kashmiri Śaivism", "yoga_spandakarika": "Kashmiri Śaivism",
    "tao_te_ching": "Daoism", "the_book_of_chuang_tzu": "Daoism",
    "astavakra_gita": "Direct Path / Yoga", "patañjali_yoga_sūtras": "Direct Path / Yoga",
    "milarepa_songs": "Vajrayāna / Buddhist", "heart_sutra": "Vajrayāna / Buddhist",
    "nagarjuna_mulamadhyamakakarika": "Vajrayāna / Buddhist",
    "shantideva_bodhicaryavatara": "Vajrayāna / Buddhist", "tilopa_mahamudra": "Vajrayāna / Buddhist",
}

# Thematic titles for units whose stored title is just "Verse X" / "Sutra N"
TITLE_OVERRIDE = {
    "pratyabhijnahrdayam.phr_001": "Sovereign Consciousness Is the Ground of All",
    "pratyabhijnahrdayam.phr_005": "Mind Is Consciousness Contracted",
    "pratyabhijnahrdayam.phr_012": "Recognition Loosens the Knot",
    "astavakra_gita.asg_1_1": "The Three Questions We Carry Up the Mountain",
    "astavakra_gita.asg_1_2": "Turn From the Objects as From Poison",
    "astavakra_gita.asg_2_7": "Bondage Is Grasping; Freedom Is Its Absence",
    "astavakra_gita.asg_11_6": "Liberated While Living",
    "astavakra_gita.asg_15_11": "The Wave of the Universe Rises and Sets in You",
}

# unit_id -> True where the "original" layer is a source-language *basis note*
# rather than reproduced script, OR where no script exists in the corpus edition.
# These are surfaced honestly; no script is fabricated.
BASIS_NOTE = {
    # empty original layer in corpus -> we state the Sanskrit basis + reference
    "tantrasara.ts_001": "Sanskrit — Abhinavagupta, Tantrasāra, Āhnika 1 (verse 1). Source Devanāgarī not reproduced in this corpus edition.",
    "tantrasara.ts_008": "Sanskrit — Abhinavagupta, Tantrasāra, Āhnika 2 (Anupāya, prose). Source Devanāgarī not reproduced in this corpus edition.",
    "yoga_spandakarika.sp_01": "Sanskrit — Spandakārikā 1 (Niṣpanda / First Flow). Source Devanāgarī not reproduced in this corpus edition.",
    "yoga_spandakarika.sp_02": "Sanskrit — Spandakārikā 2. Source Devanāgarī not reproduced in this corpus edition.",
}

# ---------------------------------------------------------------------------
# The arc: 7 sections, each with a title, a prose transition, and ordered ids.
# ---------------------------------------------------------------------------
SECTIONS = [
 dict(no="I", title="Arrival — The Ground of Awareness",
   intro=("We climbed to thin air to remember something the valley kept crowding out: "
          "that awareness is not produced by the retreat but is the ground the whole "
          "world already rests in. These first passages set that ground. They move from "
          "fullness that cannot be diminished, through the syllable in which everything "
          "sounds, to the bare recognition that consciousness is not something we have "
          "but something we are — and they close with a warning that eloquence is not the point."),
   ids=["isavasya_upanishad.isa_001","chāndogya_upaniṣad.chu_i_01","siva_sutra.ss_i_1",
        "pratyabhijnahrdayam.phr_001","tao_te_ching.ttc_md_001","astavakra_gita.asg_1_1",
        "tantrasara.ts_001","milarepa_songs.mil_zeal_002"]),
 dict(no="II", title="Nature, the Elements, and the Tremor",
   intro=("Having found the ground, we turn to the landscape that teaches it. Water finds "
          "the low places; the unnameable holds mountain and sky; and beneath the visible "
          "elements a subtle pulsation — spanda, the sacred tremor — opens and closes the "
          "world. Here the peaks, the torrents, and the emptiness above the tree-line become "
          "instruction, and even the trees are named as our gentlest companions."),
   ids=["tao_te_ching.ttc_md_006","tao_te_ching.ttc_md_025","yoga_spandakarika.sp_01",
        "yoga_spandakarika.sp_02","svetasvatara_upanishad.svu_005","svetasvatara_upanishad.svu_003",
        "the_book_of_chuang_tzu.zhuangzi_md_001","shantideva_bodhicaryavatara.bca_08_trees"]),
 dict(no="III", title="Breath, Solitude, and Discipline",
   intro=("The landscape asks a discipline of us. Yoga is named plainly as the stilling of "
          "the mind's turnings; solitude is defended not as escape but as the condition in "
          "which insight can ripen. The hermit voice of Milarepa reproves its own restlessness "
          "and reframes every discomfort, while the sages insist that effort itself is the "
          "practitioner and that skill matures into non-forcing."),
   ids=["patañjali_yoga_sūtras.ys_1_02","patañjali_yoga_sūtras.ys_1_03","siva_sutra.ss_iii_11",
        "siva_sutra.ss_ii_2","milarepa_songs.mil_reproof_004","milarepa_songs.mil_comforts_005",
        "astavakra_gita.asg_1_2","the_book_of_chuang_tzu.zhuangzi_md_006"]),
 dict(no="IV", title="Emptiness and the Two Truths",
   intro=("Discipline clears a space, and into that space the Buddhist analysis enters like "
          "cold mountain light. Form is emptiness and emptiness is form; whatever arises "
          "dependently is empty, and that very emptiness is the middle way. This is not "
          "nihilism but the loosening of every grip — and the Daoist reminds us that the Way "
          "proceeds by subtraction, not accumulation."),
   ids=["heart_sutra.hs_001","heart_sutra.hs_002","heart_sutra.hs_003",
        "nagarjuna_mulamadhyamakakarika.mmk_24_18","nagarjuna_mulamadhyamakakarika.mmk_24_08",
        "nagarjuna_mulamadhyamakakarika.mmk_25_19","tilopa_mahamudra.til_001","tao_te_ching.ttc_md_011"]),
 dict(no="V", title="Self-Inquiry and Recognition",
   intro=("If all things are empty of independent existence, who is it that knows this? The "
          "arc now turns inward to the oldest question. Uddālaka points to the one Being "
          "without a second and says: you are that. The Māṇḍūkya names the Fourth, the silence "
          "behind waking, dream, and sleep. Recognition (pratyabhijñā) is simply the seer "
          "ceasing to mistake itself for what it sees — and knowing this, one is liberated while living."),
   ids=["chāndogya_upaniṣad.chu_vi_02","chāndogya_upaniṣad.chu_vi_10","chāndogya_upaniṣad.chu_vi_08",
        "mandukya_upanishad_and_gaudapada_karika.muk_009","mandukya_upanishad_and_gaudapada_karika.muk_015",
        "pratyabhijnahrdayam.phr_005","siva_sutra.ss_i_2","pratyabhijnahrdayam.phr_012",
        "astavakra_gita.asg_11_6"]),
 dict(no="VI", title="Compassion and the Heart",
   intro=("Recognition that stops at one's own peace is incomplete. Because self and other are "
          "equally empty and equally real, another's pain has the same claim on us as our own. "
          "Śāntideva teaches the exchange of self and other; Milarepa answers cruelty with grace "
          "and contemplates the body's impermanence with tenderness; and the Daoist names "
          "compassion as the first of the three treasures."),
   ids=["shantideva_bodhicaryavatara.bca_08_exchange","shantideva_bodhicaryavatara.bca_08_equal",
        "shantideva_bodhicaryavatara.bca_09_compassion","milarepa_songs.mil_sorrow_001",
        "milarepa_songs.mil_sister_006","tao_te_ching.ttc_md_067","chāndogya_upaniṣad.chu_viii_12"]),
 dict(no="VII", title="Non-Grasping, Mahāmudrā, and the Return",
   intro=("At the last we let even the practice fall open. The mind is shown to be like the open "
          "sky, in which thought passes as cloud; bondage is revealed as nothing but grasping "
          "and its release. Tilopa says look at the looker; Abhinavagupta names the pathless "
          "path where no means is needed; and the wave of the universe rises and sets in an "
          "ocean that neither gains nor loses. We ride the mind-horse home, and return to "
          "stillness as the quiet sovereign of all that moves."),
   ids=["tilopa_mahamudra.til_002","tilopa_mahamudra.til_003","milarepa_songs.mil_race_007",
        "astavakra_gita.asg_2_7","astavakra_gita.asg_15_11","tantrasara.ts_008","tao_te_ching.ttc_md_016"]),
]

# Optional one-line practice cue kept for a few meditation-forward verses.
KEEP_PRACTICE = {
    "vijnana_bhairava", "heart_sutra", "tilopa_mahamudra",
}

# ---------------------------------------------------------------------------
def load_index():
    by_id = {}
    with open(INDEX, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            o = json.loads(line)
            by_id[o.get("unit_id")] = o
    return by_id


def layers_of(o):
    d = {}
    for l in (o.get("pratibha_layers") or []):
        d[l.get("kind")] = (l.get("body") or "").strip()
    return d


CUT_MARKERS = [
    "Cross-Tradition Resonance", "Cross-Tradition", "Key Terms:", "Key terms:",
    "\nResonance", "Divergence:", "## Appendix", "### ", "Structural Notes",
]


def clean_commentary(text):
    """Trim a commentary layer to ~3-5 leading sentences of real argument."""
    if not text:
        return ""
    t = text.strip()
    # Drop a leading "Extended Translation:" block up to the first blank line.
    if t.lower().startswith("extended translation"):
        parts = t.split("\n\n", 1)
        t = parts[1].strip() if len(parts) > 1 else ""
    # Cut at scaffolding markers.
    lo = t
    idxs = [lo.find(m) for m in CUT_MARKERS if lo.find(m) != -1]
    if idxs:
        t = t[: min(idxs)].strip()
    # Collapse newlines to spaces within paragraphs, keep it as flowing prose.
    t = re.sub(r"\s*\n\s*", " ", t).strip()
    # Take first 3-5 sentences.
    sents = re.split(r"(?<=[.!?…])\s+", t)
    out, count = [], 0
    for s in sents:
        s = s.strip()
        if not s:
            continue
        out.append(s)
        count += 1
        if count >= 5:
            break
    result = " ".join(out).strip()
    # Ensure at least 3 sentences if available.
    return result


_STOP = {"the", "a", "an", "of", "to", "is", "from", "it", "and", "or", "in", "this", "that"}


def _clip(g, n=46):
    g = (g or "").strip()
    g = re.sub(r"^\s*etymolog(?:y|ical)\s*:?\s*", "", g, flags=re.I)
    for sep in ("->", "→", ";"):
        if sep in g:
            g = g.split(sep)[0]
    g = g.replace("*", "").replace("_", "").replace("`", "").strip().rstrip(".,;:—-– ")
    g = re.sub(r"\s+", " ", g)
    if g.lower() in _STOP:
        return ""
    if len(g) > n:
        g = g[:n].rsplit(" ", 1)[0] + "…"
    return g.strip()


def _has_diacritic_or_cjk(s):
    return bool(re.search(r"[\u00C0-\u024F\u1E00-\u1EFF\u4E00-\u9FFF\u0F00-\u0FFF]", s))


def build_key_terms(o, layers):
    """Compact key terms drawn strictly from the unit's own glosses (no fabrication)."""
    terms, order = {}, []

    def add(term, gloss):
        term = re.sub(r"[\*_`]", "", term).strip()
        term = re.sub(r"\s+", " ", term)
        gloss = _clip(gloss) if gloss else ""
        if len(term) < 2 or term.lower() in ("the", "and", "just", "here", "this", "that", "no", "nor"):
            return
        if term not in terms:
            terms[term] = gloss
            order.append(term)

    iast = layers.get("iast", "")
    comm = layers.get("commentary", "") or o.get("commentary", "")
    trans = layers.get("translation", "")

    # A) Explicit "Key terms" line (Milarepa/Tilopa/Śāntideva): *term* (gloss) or term (gloss).
    if re.match(r"\s*key\s*terms", iast, re.I):
        for m in re.finditer(r"\*([^*]{2,32})\*\s*\(([^)]{2,60})\)", iast):
            add(m.group(1), m.group(2))
        for m in re.finditer(r"(?<![*\w])([A-Za-z’'][\w’' .\-]{1,28}?)\s*\(([^)]{2,60})\)", iast):
            add(m.group(1), m.group(2))
    else:
        # B) Word-by-word gloss in iast (Heart Sūtra / MMK): term (gloss).
        for m in re.finditer(r"([\w’'\-]{2,32})\s*\(([^)]{2,60})\)", iast):
            if _has_diacritic_or_cjk(m.group(1)) or m.group(1).islower():
                add(m.group(1), m.group(2))

    # C) Bracketed technical terms in the translation: gloss [term] or [term].
    for m in re.finditer(r"([A-Za-z][A-Za-z\-]+)\s*\[([^\]]{2,40})\]", trans):
        add(m.group(2), m.group(1))

    # D) Italicised terms with an adjacent gloss in the commentary.
    for m in re.finditer(r"\*([A-Za-zĀ-ſ\u1E00-\u1EFF’'][\w’'\-]{1,24})\*\s*[—\-–]\s*([^.;*]{3,48})", comm):
        add(m.group(1), m.group(2))
    for m in re.finditer(r"\*([A-Za-zĀ-ſ\u1E00-\u1EFF’'][\w’'\-]{1,24})\*\s*\(([^)]{3,48})\)", comm):
        add(m.group(1), m.group(2))
    # E) Bold "**term (script)** - gloss" (isa style).
    for m in re.finditer(r"\*\*([^*]{2,40})\*\*\s*[—\-–]\s*([^.;\n]{3,48})", comm):
        add(re.sub(r"\s*\([^)]*\)", "", m.group(1)), m.group(2))

    items = [(t, terms[t]) for t in order]
    # Keep glossed entries first; bare terms only if they are technical (non-ASCII script).
    glossed = [(t, g) for t, g in items if g]
    bare = [(t, "") for t, g in items if not g and _has_diacritic_or_cjk(t)]
    picked = (glossed + bare)[:5]
    if picked:
        return picked

    # Fallback: bare technical (transliterated) terms from the iast line only.
    fallback = []
    for w in re.findall(r"[A-Za-z\u00C0-\u024F\u1E00-\u1EFF’']{3,}", iast):
        if _has_diacritic_or_cjk(w) and w not in [f[0] for f in fallback]:
            fallback.append((w, ""))
    return fallback[:4]


def unit_title(uid, o):
    t = TITLE_OVERRIDE.get(uid) or o.get("title") or o.get("unit_label") or uid
    return t.strip().rstrip(".")


ROMAN = {"i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5, "vi": 6, "vii": 7,
         "viii": 8, "ix": 9, "x": 10, "xi": 11, "xii": 12}
LOC_WORD = {
    "tao_te_ching": "ch.", "siva_sutra": "sūtra", "pratyabhijnahrdayam": "sūtra",
    "patañjali_yoga_sūtras": "sūtra", "astavakra_gita": "verse",
    "chāndogya_upaniṣad": "", "nagarjuna_mulamadhyamakakarika": "",
    "heart_sutra": "§", "tilopa_mahamudra": "§", "shantideva_bodhicaryavatara": "ch.",
    "yoga_spandakarika": "verse",
}
# Collections whose id-number is a curation index, not a real locator.
NO_LOC = {"milarepa_songs", "the_book_of_chuang_tzu", "svetasvatara_upanishad",
          "isavasya_upanishad"}


def _parse_nums(suf):
    nums = []
    for t in re.split(r"[_.]", suf):
        if not t or t in ("md", "sum", "p"):
            continue
        if t.isdigit():
            nums.append(str(int(t)))
        elif t.lower() in ROMAN:
            nums.append(str(ROMAN[t.lower()]))
    return ".".join(nums)


def source_line(uid, o):
    coll, suf = uid.split(".", 1)
    author = SOURCE.get(coll, o.get("work_title") or coll)
    prov = o.get("provenance") or {}
    sr = (prov.get("source_reference") or "").strip()
    if sr:
        # Strip inner markdown emphasis and the trailing provenance parenthetical.
        sr = sr.replace("*", "").replace("_", "")
        sr = re.sub(r"\s*\([^)]*(?:anchor|GRETIL|Pratibha|BCA_|MMK_|TIL_|HS_|rendering)[^)]*\)",
                    "", sr, flags=re.I).strip().rstrip(",;")
        return sr
    if coll == "mandukya_upanishad_and_gaudapada_karika":
        lab = (o.get("unit_label") or "").split("·")[0].split("—")[0].strip()
        return f"{author}, {lab}" if lab else author
    if coll in NO_LOC:
        return author
    loc = _parse_nums(suf)
    if not loc:
        return author
    word = LOC_WORD.get(coll, "verse")
    return f"{author}, {word} {loc}".replace(",  ", ", ") if word else f"{author} {loc}"


def original_block(uid, layers):
    """Return (label, text) for the original-language layer, honestly handling basis notes."""
    if uid in BASIS_NOTE:
        return ("Original Language", "*Source-language basis:* " + BASIS_NOTE[uid])
    orig = layers.get("original", "")
    if not orig:
        return ("Original Language", "*Source-language basis: not reproduced in this corpus edition.*")
    return ("Original", orig)


def display_iast(layers):
    """Only show the IAST layer when it is genuine transliteration, not a key-terms line."""
    t = layers.get("iast", "")
    if not t:
        return ""
    if re.match(r"\s*key\s*terms", t, re.I):
        return ""
    return t


def first_sentence(text):
    if not text:
        return ""
    t = re.sub(r"\s*\n\s*", " ", text.strip())
    m = re.split(r"(?<=[.!?…])\s+", t)
    return m[0].strip() if m else t


def collect_units(by_id):
    data = []
    for sec in SECTIONS:
        srecs = []
        for uid in sec["ids"]:
            o = by_id[uid]
            layers = layers_of(o)
            srecs.append(dict(
                uid=uid,
                coll=uid.split(".")[0],
                tradition=TRADITION[uid.split(".")[0]],
                title=unit_title(uid, o),
                source=source_line(uid, o),
                orig=original_block(uid, layers),
                iast=display_iast(layers),
                translation=layers.get("translation", "") or (o.get("translation_literal") or ""),
                commentary=clean_commentary(layers.get("commentary", "") or o.get("commentary", "")),
                key_terms=build_key_terms(o, layers),
                practice=first_sentence(layers.get("practice", "")) if uid.split(".")[0] in KEEP_PRACTICE else "",
                maturity=o.get("editorial_maturity", ""),
            ))
        data.append((sec, srecs))
    return data


# ===========================================================================
# Renderers
# ===========================================================================
TITLE = "Light on the Mountain"
SUBTITLE = "A Contemplative Arc in Fifty-Five Verses"
BLURB = ("Fifty-five passages from the world's non-dual and contemplative traditions, "
         "drawn from the Pratibhā corpus and arranged as a single luminous arc for a "
         "Himalayan retreat. Kashmiri Śaivism, Vajrayāna Buddhism, the Upaniṣads, Daoism, "
         "and the direct path of self-inquiry interleave — not by tradition, but by the "
         "turn of understanding each verse serves.")


def md_key_terms(items):
    parts = []
    for t, g in items:
        parts.append(f"**{t}** — {g}" if g else f"**{t}**")
    return " · ".join(parts)


def render_markdown(data):
    L = []
    # YAML metadata block (used by pandoc for .docx / .icml titling; harmless when read raw).
    L.append("---")
    L.append(f'title: "{TITLE}"')
    L.append(f'subtitle: "{SUBTITLE}"')
    L.append('author: "Compiled from the Pratibhā corpus"')
    L.append('date: "Himalayan Retreat Edition"')
    L.append("lang: en")
    L.append("---")
    L.append("")
    L.append(f"# {TITLE}")
    L.append(f"### {SUBTITLE}")
    L.append("")
    L.append(f"*{BLURB}*")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## The Arc")
    L.append("")
    n = 0
    for sec, recs in data:
        span = f"{n+1}–{n+len(recs)}"
        L.append(f"**{sec['no']}. {sec['title']}**  \n*Verses {span}*")
        L.append("")
        n += len(recs)
    L.append("")
    L.append("---")
    L.append("")
    seq = 0
    for sec, recs in data:
        L.append(f"# {sec['no']}. {sec['title']}")
        L.append("")
        L.append(f"> {sec['intro']}")
        L.append("")
        for r in recs:
            seq += 1
            L.append(f"## {seq}. {r['title']}")
            L.append("")
            L.append(f"*{r['source']}*  \n<sub>`{r['uid']}` · {r['tradition']}</sub>")
            L.append("")
            olabel, otext = r["orig"]
            L.append(f"**{olabel}**")
            L.append("")
            L.append(otext)
            L.append("")
            if r["iast"]:
                L.append("**IAST / Transliteration**")
                L.append("")
                L.append(r["iast"])
                L.append("")
            L.append("**Pratibhā Translation**")
            L.append("")
            L.append(r["translation"])
            L.append("")
            if r["commentary"]:
                L.append("**Commentary**")
                L.append("")
                L.append(r["commentary"])
                L.append("")
            if r["key_terms"]:
                L.append("**Key Terms**  ")
                L.append(md_key_terms(r["key_terms"]))
                L.append("")
            if r["practice"]:
                L.append(f"*Practice cue.* {r['practice']}")
                L.append("")
            L.append("---")
            L.append("")
    L.append("## Sources & Editorial Notes")
    L.append("")
    L.append("All text is drawn verbatim from the Pratibhā canonical corpus "
             "(`data/canonical/`); no source text has been invented. Commentary has been "
             "trimmed from each unit's own commentary layer. Section introductions are "
             "editorial connective prose.")
    L.append("")
    L.append("Where a unit's source script is not reproduced in the corpus edition "
             "(marked *Source-language basis*), the original language and reference are "
             "stated and no script has been fabricated. Heart Sūtra and Mūlamadhyamakakārikā "
             "originals are given in source-verified IAST (GRETIL) rather than Devanāgarī.")
    L.append("")
    return "\n".join(L)


def esc(s):
    return html.escape(s or "", quote=False)


def html_inline(s):
    """Minimal markdown-ish inline -> HTML: *em* and **strong**, `code`."""
    s = esc(s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def html_key_terms(items):
    parts = []
    for t, g in items:
        parts.append(f"<strong>{esc(t)}</strong> — {esc(g)}" if g else f"<strong>{esc(t)}</strong>")
    return " &middot; ".join(parts)


def para_breaks(text):
    return "<br/>".join(esc(line) for line in text.split("\n"))


CSS_DOCX = """
body{font-family:'Georgia','Times New Roman',serif;max-width:44rem;margin:2rem auto;
line-height:1.5;color:#1a1a1a;padding:0 1.25rem;}
h1{font-size:1.7rem;margin:2.4rem 0 .4rem;border-bottom:1px solid #ccc;padding-bottom:.3rem;}
h2{font-size:1.25rem;margin:1.8rem 0 .3rem;color:#222;}
h3{font-size:1.05rem;color:#555;font-weight:normal;font-style:italic;margin:.2rem 0 1rem;}
.blurb{font-style:italic;color:#444;}
.arc-item{margin:.2rem 0;}
.intro{font-style:italic;color:#444;border-left:3px solid #b8860b;padding-left:1rem;margin:1rem 0 1.6rem;}
.source{font-style:italic;color:#444;margin:.1rem 0;}
.trace{font-size:.78rem;color:#888;font-family:monospace;}
.label{font-variant:small-caps;letter-spacing:.05em;font-weight:bold;color:#8a6d3b;
font-size:.82rem;margin:1rem 0 .1rem;}
.original{font-size:1.12rem;line-height:1.7;}
.translation{font-size:1.05rem;}
.keyterms{font-size:.9rem;color:#333;}
.practice{font-style:italic;color:#555;font-size:.92rem;}
hr{border:none;border-top:1px solid #e2e2e2;margin:2rem 0;}
.verse{margin-bottom:1.2rem;}
"""


def render_docx_html(data):
    H = ['<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>',
         f"<title>{esc(TITLE)}</title><style>{CSS_DOCX}</style></head><body>"]
    H.append(f"<h1 style='border:none;text-align:center'>{esc(TITLE)}</h1>")
    H.append(f"<h3 style='text-align:center'>{esc(SUBTITLE)}</h3>")
    H.append(f"<p class='blurb'>{esc(BLURB)}</p>")
    H.append("<h1>The Arc</h1>")
    n = 0
    for sec, recs in data:
        H.append(f"<p class='arc-item'><strong>{sec['no']}. {esc(sec['title'])}</strong> "
                 f"&mdash; <em>verses {n+1}&ndash;{n+len(recs)}</em></p>")
        n += len(recs)
    seq = 0
    for sec, recs in data:
        H.append(f"<h1>{sec['no']}. {esc(sec['title'])}</h1>")
        H.append(f"<p class='intro'>{esc(sec['intro'])}</p>")
        for r in recs:
            seq += 1
            H.append("<div class='verse'>")
            H.append(f"<h2>{seq}. {esc(r['title'])}</h2>")
            H.append(f"<p class='source'>{esc(r['source'])}</p>")
            H.append(f"<p class='trace'>{esc(r['uid'])} &middot; {esc(r['tradition'])}</p>")
            olabel, otext = r["orig"]
            H.append(f"<p class='label'>{esc(olabel)}</p>")
            H.append(f"<p class='original'>{html_inline(otext)}</p>")
            if r["iast"]:
                H.append("<p class='label'>IAST / Transliteration</p>")
                H.append(f"<p class='iast'>{para_breaks(r['iast'])}</p>")
            H.append("<p class='label'>Pratibhā Translation</p>")
            H.append(f"<p class='translation'>{para_breaks(r['translation'])}</p>")
            if r["commentary"]:
                H.append("<p class='label'>Commentary</p>")
                H.append(f"<p class='commentary'>{html_inline(r['commentary'])}</p>")
            if r["key_terms"]:
                H.append("<p class='label'>Key Terms</p>")
                H.append(f"<p class='keyterms'>{html_key_terms(r['key_terms'])}</p>")
            if r["practice"]:
                H.append(f"<p class='practice'>Practice cue. {esc(r['practice'])}</p>")
            H.append("</div><hr/>")
    H.append("<h1>Sources &amp; Editorial Notes</h1>")
    H.append("<p>All text is drawn verbatim from the Pratibhā canonical corpus; no source "
             "text has been invented. Commentary is trimmed from each unit's own commentary "
             "layer; section introductions are editorial connective prose. Where source script "
             "is not reproduced (marked <em>Source-language basis</em>), the original language "
             "and reference are stated and no script has been fabricated.</p>")
    H.append("</body></html>")
    return "\n".join(H)


def render_indesign_html(data):
    """Semantic, lightly-styled HTML for InDesign placement (map classes to paragraph styles)."""
    H = ['<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>',
         f"<title>{esc(TITLE)}</title>",
         "<style>",
         "h1.book-title{}", "h2.subtitle{}", "h1.section-title{}", "p.section-intro{}",
         "h2.verse-title{}", "p.verse-source{}", "p.verse-id{}", "p.layer-label{}",
         "p.original{}", "p.iast{}", "p.translation{}", "p.commentary{}",
         "p.key-terms{}", "p.practice{}",
         "</style></head><body>"]
    H.append(f'<h1 class="book-title">{esc(TITLE)}</h1>')
    H.append(f'<h2 class="subtitle">{esc(SUBTITLE)}</h2>')
    H.append(f'<p class="blurb">{esc(BLURB)}</p>')
    seq = 0
    for sec, recs in data:
        H.append(f'<h1 class="section-title">{sec["no"]}. {esc(sec["title"])}</h1>')
        H.append(f'<p class="section-intro">{esc(sec["intro"])}</p>')
        for r in recs:
            seq += 1
            H.append(f'<article class="verse" data-unit="{esc(r["uid"])}" data-tradition="{esc(r["tradition"])}">')
            H.append(f'<h2 class="verse-title">{seq}. {esc(r["title"])}</h2>')
            H.append(f'<p class="verse-source">{esc(r["source"])}</p>')
            H.append(f'<p class="verse-id">{esc(r["uid"])}</p>')
            olabel, otext = r["orig"]
            H.append(f'<p class="layer-label">{esc(olabel)}</p>')
            H.append(f'<p class="original">{html_inline(otext)}</p>')
            if r["iast"]:
                H.append('<p class="layer-label">IAST / Transliteration</p>')
                H.append(f'<p class="iast">{para_breaks(r["iast"])}</p>')
            H.append('<p class="layer-label">Pratibha Translation</p>')
            H.append(f'<p class="translation">{para_breaks(r["translation"])}</p>')
            if r["commentary"]:
                H.append('<p class="layer-label">Commentary</p>')
                H.append(f'<p class="commentary">{html_inline(r["commentary"])}</p>')
            if r["key_terms"]:
                H.append('<p class="layer-label">Key Terms</p>')
                H.append(f'<p class="key-terms">{html_key_terms(r["key_terms"])}</p>')
            if r["practice"]:
                H.append(f'<p class="practice">Practice cue. {esc(r["practice"])}</p>')
            H.append("</article>")
    H.append("</body></html>")
    return "\n".join(H)


def main():
    by_id = load_index()
    missing = [u for sec in SECTIONS for u in sec["ids"] if u not in by_id]
    if missing:
        print("MISSING UNITS:", missing, file=sys.stderr)
        sys.exit(1)
    data = collect_units(by_id)
    total = sum(len(r) for _, r in data)
    os.makedirs(OUTDIR, exist_ok=True)
    with open(os.path.join(OUTDIR, "himalaya_retreat_booklet.md"), "w", encoding="utf-8") as f:
        f.write(render_markdown(data))
    with open(os.path.join(OUTDIR, "docx_ready.html"), "w", encoding="utf-8") as f:
        f.write(render_docx_html(data))
    with open(os.path.join(OUTDIR, "booklet_indesign.html"), "w", encoding="utf-8") as f:
        f.write(render_indesign_html(data))
    # tradition balance
    from collections import Counter
    bal = Counter(r["tradition"] for _, recs in data for r in recs)
    print(f"Built booklet: {total} verses across {len(data)} sections.")
    for k, v in bal.most_common():
        print(f"  {v:2d}  {k}")


if __name__ == "__main__":
    main()
