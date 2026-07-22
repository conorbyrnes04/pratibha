#!/usr/bin/env python3
"""
READ-ONLY quality audit: TITLES + THEMATIC SHALLOWNESS
Dimension owner: titles that are bare references (not thematic claims),
titles copied verbatim from the passage, thin/mis-tagged themes, and
filler / sub-spec commentary.

Reads:  data/canonical/index.jsonl  (1 JSON object per line)
Writes: scripts/audit/titles_themes.md
Does NOT modify any data file.
"""
import json
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "data" / "canonical" / "index.jsonl"
OUT = ROOT / "scripts" / "audit" / "titles_themes.md"

COMMENTARY_MIN_WORDS = 150  # per SKILL.md spec

# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------
rows = []
with INDEX.open(encoding="utf-8") as fh:
    for line in fh:
        line = line.strip()
        if line:
            rows.append(json.loads(line))

TOTAL = len(rows)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def norm(s):
    """Normalize text for comparison: collapse whitespace, strip, casefold."""
    if not s:
        return ""
    return re.sub(r"\s+", " ", str(s)).strip()

def norm_cmp(s):
    return norm(s).casefold().rstrip(".;: ")

def word_count(s):
    if not s:
        return 0
    # strip markdown emphasis markers so *word* counts as one word
    txt = re.sub(r"[*_`>#]", " ", str(s))
    return len(re.findall(r"\S+", txt))

def translation_body(r):
    """Best-effort primary passage / translation text for a unit."""
    for layer in r.get("pratibha_layers", []):
        if layer.get("kind") == "translation":
            return layer.get("body", "") or ""
    return r.get("translation_literal") or r.get("translation") or r.get("pratibha_translation") or ""

# ---------------------------------------------------------------------------
# Bare-reference title detection
# ---------------------------------------------------------------------------
# Whole-title patterns that indicate a pointer rather than a thematic claim.
REF_KEYWORD = (
    r"(?:verse|verses|yukti|sutra|sūtra|sloka|śloka|karika|kārikā|fragment|"
    r"pearl|chapter|section|aphorism|enchiridion|book|canto|stanza|hymn|"
    r"mantra|khanda|khaṇḍa|adhyaya|adhyāya|pada|pāda|part|no|number)"
)
BARE_PATTERNS = [
    re.compile(r"^\s*" + REF_KEYWORD + r"[\s#.:§-]*[0-9ivxlcdm]+([.\-–][0-9ivxlcdm]+)*\s*[.:]?\s*$", re.I),
    re.compile(r"^\s*§\s*[0-9]+.*$", re.I),                       # §1
    re.compile(r"^\s*#\s*[0-9]+\s*$"),                            # #12
    re.compile(r"^\s*[0-9]+([.\-–][0-9]+)*\s*[.:]?\s*$"),         # 1.27 / 11.5
    re.compile(r"^\s*[ivxlcdm]+([.\-–][0-9]+)*\s*[.:]?\s*$", re.I),  # roman numeral refs (III, IV.2)
    re.compile(r"^\s*" + REF_KEYWORD + r"\s*[#§]\s*[0-9]+\s*$", re.I),  # Yukti #28
]

def is_bare_title(title, unit_label):
    t = norm(title)
    if not t:
        return True  # missing title = no thematic claim authored
    for pat in BARE_PATTERNS:
        if pat.match(t):
            return True
    return False

# ---------------------------------------------------------------------------
# Verbatim-passage title detection (title == the passage sentence)
# ---------------------------------------------------------------------------
def is_verbatim_title(r):
    t = norm_cmp(r.get("title"))
    if not t:
        return False
    candidates = [
        r.get("translation_literal"),
        r.get("source_excerpt"),
        translation_body(r),
        r.get("insight"),
    ]
    for c in candidates:
        c = norm_cmp(c)
        if not c:
            continue
        if t == c:
            return True
        # title is a full-sentence prefix of the passage body (copied opening sentence)
        if len(t) >= 40 and c.startswith(t):
            return True
    # generic heuristic: long title that reads like a full sentence
    if word_count(t) >= 12 and re.search(r"[.!?]$", norm(r.get("title"))):
        return True
    return False

# ---------------------------------------------------------------------------
# Boilerplate commentary detection
# ---------------------------------------------------------------------------
BOILERPLATE_PREFIXES = [
    "read this line as a contemplative pointer",
    "the emphasis turns inward",
    "this line points to a deeper order",
    "the teaching frames change as lawful",
    "read this passage slowly",
]

def is_boilerplate(body):
    b = norm_cmp(body)
    return any(b.startswith(p) for p in BOILERPLATE_PREFIXES)

# ---------------------------------------------------------------------------
# Aggregate
# ---------------------------------------------------------------------------
by_work = defaultdict(list)
for r in rows:
    by_work[r["work_id"]].append(r)

work_stats = {}
all_themes = Counter()
theme_count_dist = Counter()
commentary_bodies = Counter()
boilerplate_examples = defaultdict(list)  # body -> [unit_ids]

overall = {
    "bare": 0,
    "verbatim": 0,
    "sub150": 0,
    "cmt_eq_insight": 0,
    "boilerplate": 0,
    "themes_le1": 0,
    "themes_0": 0,
}

for wid, units in by_work.items():
    s = {
        "n": len(units),
        "work_title": units[0].get("work_title", wid),
        "bare": 0,
        "verbatim": 0,
        "sub150": 0,
        "cmt_eq_insight": 0,
        "boilerplate": 0,
        "themes_le1": 0,
        "theme_counts": [],
        "cmt_words": [],
        "bare_ids": [],
        "verbatim_ids": [],
        "sub150_ids": [],
        "thin_theme_ids": [],
    }
    for r in units:
        # titles
        if is_bare_title(r.get("title"), r.get("unit_label")):
            s["bare"] += 1
            s["bare_ids"].append(r["unit_id"])
            overall["bare"] += 1
        elif is_verbatim_title(r):  # elif: don't double-count a bare ref as verbatim
            s["verbatim"] += 1
            s["verbatim_ids"].append(r["unit_id"])
            overall["verbatim"] += 1

        # themes
        themes = r.get("themes") or []
        tc = len(themes)
        s["theme_counts"].append(tc)
        theme_count_dist[tc] += 1
        for th in themes:
            all_themes[th] += 1
        if tc <= 1:
            s["themes_le1"] += 1
            overall["themes_le1"] += 1
            s["thin_theme_ids"].append(r["unit_id"])
        if tc == 0:
            overall["themes_0"] += 1

        # commentary
        cmt = r.get("commentary") or ""
        wc = word_count(cmt)
        s["cmt_words"].append(wc)
        if wc < COMMENTARY_MIN_WORDS:
            s["sub150"] += 1
            s["sub150_ids"].append(r["unit_id"])
            overall["sub150"] += 1
        if norm_cmp(cmt) and norm_cmp(cmt) == norm_cmp(r.get("insight")):
            s["cmt_eq_insight"] += 1
            overall["cmt_eq_insight"] += 1
        commentary_bodies[norm(cmt)] += 1
        if is_boilerplate(cmt):
            s["boilerplate"] += 1
            overall["boilerplate"] += 1
            boilerplate_examples[norm(cmt)[:200]].append(r["unit_id"])

    work_stats[wid] = s

# theme vocabulary health
distinct_themes = len(all_themes)
singleton_themes = [t for t, n in all_themes.items() if n == 1]

# repeated commentary bodies (boilerplate/templated)
repeated_commentaries = [(b, n) for b, n in commentary_bodies.most_common() if n > 1]

# ---------------------------------------------------------------------------
# Console summary
# ---------------------------------------------------------------------------
def pct(a, b):
    return (100.0 * a / b) if b else 0.0

print(f"Units: {TOTAL} across {len(by_work)} works\n")

print("== TITLES ==")
print(f"Bare-reference titles: {overall['bare']} ({pct(overall['bare'], TOTAL):.1f}%)")
print(f"Verbatim-passage titles: {overall['verbatim']} ({pct(overall['verbatim'], TOTAL):.1f}%)")
worst_bare = sorted(work_stats.items(), key=lambda kv: pct(kv[1]["bare"], kv[1]["n"]), reverse=True)
print("\nWorst works by bare-title %:")
for wid, s in worst_bare:
    if s["bare"]:
        print(f"  {wid:42s} {s['bare']:3d}/{s['n']:<3d} ({pct(s['bare'], s['n']):5.1f}%)  eg {s['bare_ids'][:2]}")

print("\n== THEMATIC SHALLOWNESS ==")
print(f"Units with <=1 theme: {overall['themes_le1']} ({pct(overall['themes_le1'], TOTAL):.1f}%); with 0 themes: {overall['themes_0']}")
print(f"Sub-150-word commentaries: {overall['sub150']} ({pct(overall['sub150'], TOTAL):.1f}%)")
print(f"commentary == insight (no development): {overall['cmt_eq_insight']}")
print(f"Boilerplate commentaries: {overall['boilerplate']}")
worst_cmt = sorted(work_stats.items(), key=lambda kv: pct(kv[1]["sub150"], kv[1]["n"]), reverse=True)
print("\nWorst works by sub-150-word commentary %:")
for wid, s in worst_cmt:
    if s["sub150"]:
        print(f"  {wid:42s} {s['sub150']:3d}/{s['n']:<3d} ({pct(s['sub150'], s['n']):5.1f}%)")

print("\n== THEME VOCABULARY ==")
print(f"Distinct themes: {distinct_themes}; singletons (used once): {len(singleton_themes)}")
print("Theme-count distribution (themes -> units):")
for k in sorted(theme_count_dist):
    print(f"  {k}: {theme_count_dist[k]}")

# ---------------------------------------------------------------------------
# Markdown report
# ---------------------------------------------------------------------------
lines = []
A = lines.append
A("# Pratibha Corpus Audit — Titles & Thematic Shallowness")
A("")
A(f"Read-only audit of `data/canonical/index.jsonl` — **{TOTAL} units across {len(by_work)} works**.")
A(f"Spec reference: `.cursor/skills/pratibha-md/SKILL.md` (Title = thematic claim; Commentary >= {COMMENTARY_MIN_WORDS} words, claim-led).")
A("")
A("## Executive Summary")
A("")
A(f"- **Bare-reference titles** (verse/section pointers, not thematic claims): **{overall['bare']} / {TOTAL} ({pct(overall['bare'], TOTAL):.1f}%)**")
A(f"- **Verbatim-passage titles** (title is the passage sentence, not a distilled claim): **{overall['verbatim']} ({pct(overall['verbatim'], TOTAL):.1f}%)**")
A(f"- **Sub-{COMMENTARY_MIN_WORDS}-word commentaries** (below spec minimum): **{overall['sub150']} ({pct(overall['sub150'], TOTAL):.1f}%)**")
A(f"- **Commentary == insight** (no development beyond the one-line insight): **{overall['cmt_eq_insight']}**")
A(f"- **Boilerplate/templated commentaries**: **{overall['boilerplate']}**")
A(f"- **Units with <=1 theme**: **{overall['themes_le1']} ({pct(overall['themes_le1'], TOTAL):.1f}%)** (0 themes: {overall['themes_0']})")
A(f"- **Theme vocabulary**: {distinct_themes} distinct themes, {len(singleton_themes)} used only once")
A("")

A("## 1. Titles — Bare-Reference & Verbatim (per work)")
A("")
A("| Work | Units | Bare titles | Bare % | Verbatim titles | Verbatim % |")
A("|------|------:|------------:|-------:|----------------:|-----------:|")
for wid, s in sorted(work_stats.items(), key=lambda kv: (pct(kv[1]["bare"], kv[1]["n"]) + pct(kv[1]["verbatim"], kv[1]["n"])), reverse=True):
    A(f"| {wid} | {s['n']} | {s['bare']} | {pct(s['bare'], s['n']):.0f}% | {s['verbatim']} | {pct(s['verbatim'], s['n']):.0f}% |")
A("")
A("### Worst works for bare titles — examples")
A("")
for wid, s in worst_bare:
    if s["bare"]:
        ex = ", ".join(f"`{u}`" for u in s["bare_ids"][:4])
        A(f"- **{wid}** — {s['bare']}/{s['n']} ({pct(s['bare'], s['n']):.0f}%): {ex}")
A("")
A("### Verbatim-passage titles — examples")
A("")
verb_examples = []
for wid, s in sorted(work_stats.items(), key=lambda kv: kv[1]["verbatim"], reverse=True):
    if s["verbatim"]:
        ex = ", ".join(f"`{u}`" for u in s["verbatim_ids"][:4])
        A(f"- **{wid}** — {s['verbatim']}/{s['n']}: {ex}")
A("")
# concrete cited example (spec-named)
her = next((r for r in rows if r["unit_id"] == "heraclitus_fragments.hfr_p125"), None)
if her:
    A(f"Cited example — `heraclitus_fragments.hfr_p125` title: \"{norm(her['title'])}\" (the whole passage sentence).")
    A("")

A("## 2. Thematic Shallowness — Commentary Depth (per work)")
A("")
A("| Work | Units | Sub-150w | Sub-150w % | Median cmt words | cmt==insight | boilerplate | Units <=1 theme |")
A("|------|------:|---------:|-----------:|-----------------:|-------------:|------------:|----------------:|")
for wid, s in sorted(work_stats.items(), key=lambda kv: pct(kv[1]["sub150"], kv[1]["n"]), reverse=True):
    med = int(statistics.median(s["cmt_words"])) if s["cmt_words"] else 0
    A(f"| {wid} | {s['n']} | {s['sub150']} | {pct(s['sub150'], s['n']):.0f}% | {med} | {s['cmt_eq_insight']} | {s['boilerplate']} | {s['themes_le1']} |")
A("")
A("### Thinnest-commentary works — example unit_ids")
A("")
for wid, s in worst_cmt[:8]:
    if s["sub150"]:
        ex = ", ".join(f"`{u}`" for u in s["sub150_ids"][:4])
        A(f"- **{wid}** — {s['sub150']}/{s['n']} ({pct(s['sub150'], s['n']):.0f}%): {ex}")
A("")

A("## 3. Theme-Count Distribution")
A("")
A("| # themes | # units | % of corpus |")
A("|---------:|--------:|------------:|")
for k in sorted(theme_count_dist):
    A(f"| {k} | {theme_count_dist[k]} | {pct(theme_count_dist[k], TOTAL):.1f}% |")
A("")
A("Units with <=1 theme by work (thin tagging):")
A("")
for wid, s in sorted(work_stats.items(), key=lambda kv: pct(kv[1]["themes_le1"], kv[1]["n"]), reverse=True):
    if s["themes_le1"]:
        ex = ", ".join(f"`{u}`" for u in s["thin_theme_ids"][:3])
        A(f"- **{wid}** — {s['themes_le1']}/{s['n']} ({pct(s['themes_le1'], s['n']):.0f}%): {ex}")
A("")

A("## 4. Boilerplate / Templated Commentary")
A("")
A(f"Repeated commentary bodies (identical text reused across units) — {len(repeated_commentaries)} distinct bodies reused, covering {sum(n for _, n in repeated_commentaries)} units:")
A("")
A("| Count | Commentary body (truncated) |")
A("|------:|------------------------------|")
for body, n in repeated_commentaries[:12]:
    snippet = body[:140].replace("|", "\\|").replace("\n", " ")
    A(f"| {n} | {snippet}… |")
A("")
A("Representative unit_ids for the top boilerplate strings:")
A("")
for body, ids in sorted(boilerplate_examples.items(), key=lambda kv: len(kv[1]), reverse=True)[:6]:
    snippet = body[:80].replace("\n", " ")
    A(f"- \"{snippet}…\" — {len(ids)} units, e.g. {', '.join(f'`{u}`' for u in ids[:4])}")
A("")

A("## 5. Theme Vocabulary Health")
A("")
A(f"- Distinct themes: **{distinct_themes}**")
A(f"- Singleton themes (used exactly once): **{len(singleton_themes)}**")
A("")
A("Most-used themes:")
A("")
A("| Theme | Uses |")
A("|-------|-----:|")
for th, n in all_themes.most_common(20):
    A(f"| {th} | {n} |")
A("")
A("Sample singleton themes (possible inconsistent/one-off tagging): " + ", ".join(f"`{t}`" for t in sorted(singleton_themes)[:40]))
A("")
# rough near-duplicate label detection (same stem / plural-singular / case)
def theme_key(t):
    return re.sub(r"[^a-z]", "", t.lower()).rstrip("s")
label_groups = defaultdict(set)
for t in all_themes:
    label_groups[theme_key(t)].add(t)
inconsistent = {k: v for k, v in label_groups.items() if len(v) > 1}
if inconsistent:
    A("Possible inconsistent labels (same concept, different strings):")
    A("")
    for k, v in sorted(inconsistent.items()):
        A(f"- {', '.join(sorted(repr(x) for x in v))}")
    A("")

A("## Prioritized Recommendations")
A("")
recs = []
# 1. worst bare-title works
top_bare = [w for w, s in worst_bare if s["bare"]][:5]
if top_bare:
    detail = "; ".join(f"{w} ({work_stats[w]['bare']}/{work_stats[w]['n']})" for w in top_bare)
    recs.append(f"**Author thematic titles first for the pointer-titled works**: {detail}. These have titles that are pure verse/section references (e.g. `Yukti #1`, `Sutra 1`, `Verse 11.5`, `Pearl #1`) and violate the spec's Title rule outright.")
# 2. verbatim
top_verb = [w for w, s in sorted(work_stats.items(), key=lambda kv: kv[1]['verbatim'], reverse=True) if s['verbatim']][:4]
if top_verb:
    detail = "; ".join(f"{w} ({work_stats[w]['verbatim']})" for w in top_verb)
    recs.append(f"**Distill verbatim-sentence titles into claims** for: {detail}. Titles currently copy the passage sentence (e.g. `heraclitus_fragments`, `siva_sutra`, `yoga_spandakarika`) instead of naming the move.")
# 3. thin commentary
top_thin = [w for w, s in worst_cmt if s["sub150"]][:5]
if top_thin:
    detail = "; ".join(f"{w} ({pct(work_stats[w]['sub150'], work_stats[w]['n']):.0f}%)" for w in top_thin)
    recs.append(f"**Deepen thinnest commentary first**: {detail}. These have the highest share of sub-{COMMENTARY_MIN_WORDS}-word commentaries.")
# 4. boilerplate
if overall["boilerplate"]:
    recs.append(f"**Replace {overall['boilerplate']} boilerplate commentaries** (templated strings like \"Read this line as a contemplative pointer…\" and \"The emphasis turns inward…\") with claim-led argument; {overall['cmt_eq_insight']} units also have commentary identical to the one-line insight.")
# 5. themes
recs.append(f"**Enrich thin theme tagging**: {overall['themes_le1']} units carry <=1 theme; consolidate the {len(singleton_themes)} singleton themes and reconcile inconsistent labels to a controlled vocabulary.")
for i, r in enumerate(recs, 1):
    A(f"{i}. {r}")
A("")

OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"\nReport written to {OUT.relative_to(ROOT)}")
