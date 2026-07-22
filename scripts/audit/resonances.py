#!/usr/bin/env python3
"""
Pratibha corpus quality audit — DIMENSION: CROSS-TRADITION RESONANCES.

READ-ONLY. Reads data/canonical/index.jsonl and writes a findings report to
scripts/audit/resonances.md. Does not modify any corpus data.

Measures, per the pratibha-md spec ("Cross-Tradition Resonances": 2-4 entries
per unit; each entry needs (a) structural homology, (b) a SPECIFIC cited
passage, (c) a divergence clause):

  1. COVERAGE      — distribution of structured resonance counts per unit
  2. TITLE-ONLY    — resonances that cite a work/author but no specific passage
  3. DIVERGENCE    — items missing / trivial / boilerplate divergence clauses
  4. DEPTH         — items asserting only shared THEME, not structural homology
  5. INTEGRITY     — passage_id values that dangle (no matching unit_id)
  6. DUPLICATION   — identical resonance text templated across many units
"""

import json
import re
import os
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INDEX = os.path.join(ROOT, "data", "canonical", "index.jsonl")
OUT = os.path.join(ROOT, "scripts", "audit", "resonances.md")


def load_units(path):
    units = []
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                units.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"WARN: bad JSON on line {i}: {e}")
    return units


def get_resonance_items(unit):
    """Return the list of resonance item dicts for a unit (may be empty)."""
    for layer in unit.get("pratibha_layers", []):
        if layer.get("kind") == "resonances":
            items = layer.get("items")
            if isinstance(items, list):
                return items
            return []
    return []


# ---- Heuristics -----------------------------------------------------------

# passage_id well-formed = "work.unit_something" (a dot, non-empty both sides)
PID_RE = re.compile(r"^[^.\s]+\..+$")

# A citation is "specific" if it references a number, section marker, verse ref,
# chapter, fragment, saying, etc. Otherwise it's likely a bare work/author name.
SPECIFIC_CITATION_RE = re.compile(
    r"(\d+|[§¶]|\bverse\b|\bch(?:apter)?\.?\b|\bsec(?:tion)?\.?\b|"
    r"\bfr(?:agment|\.)\b|\bsutra\b|\bsūtra\b|\bsaying\b|\bstanza\b|"
    r"\bstromata\b|\bbook\b|\bline\b|\bfol(?:io)?\.?\b|\bpart\b|"
    r"\bpsalm\b|\bkarika\b|\bkārikā\b|\bchapter\b|—|:)",
    re.IGNORECASE,
)

# Generic / thematic phrasing that signals a shared-theme claim rather than a
# structural homology claim.
GENERIC_PHRASES = [
    "both texts discuss",
    "both discuss",
    "similar theme",
    "same theme",
    "both emphasize",
    "both mention",
    "both talk about",
    "both are about",
    "both speak of",
    "shares the theme",
    "shared theme",
    "both explore",
    "both address",
    "both deal with",
    "similar idea",
    "similar concept",
    "like this passage",
    "also discusses",
    "also talks about",
]

# Vocabulary indicating a genuine STRUCTURAL claim (mirrors the SKILL rubric).
STRUCTURAL_MARKERS = [
    "structur", "move", "mechanism", "reduc", "collapse", "invert", "mirror",
    "parallel", "homolog", "logic", "operation", "gesture", "arc", "sequence",
    "reversal", "negat", "dialectic", "paradox", "identif", "locate",
    "grounds", "performs", "stages", "same form", "isomorph", "map",
]

DIVERGENCE_MIN_LEN = 25          # chars; below this a divergence is trivial
RESONANCE_SHORT_LEN = 140        # chars; below this the body is suspiciously thin


def is_specific_citation(citation):
    if not citation or not citation.strip():
        return False
    return bool(SPECIFIC_CITATION_RE.search(citation))


def points_to_specific_passage(item):
    """True if the item references a concrete passage via pid OR citation."""
    pid = (item.get("passage_id") or "").strip()
    if pid and PID_RE.match(pid):
        return True
    return is_specific_citation(item.get("citation") or "")


def divergence_missing_or_trivial(item):
    d = (item.get("divergence") or "").strip()
    if not d:
        return "missing"
    if len(d) < DIVERGENCE_MIN_LEN:
        return "trivial"
    return None


def asserts_theme_only(item):
    """Heuristic: body uses generic thematic phrasing and lacks structural markers."""
    body = (item.get("resonance") or "").strip()
    low = body.lower()
    has_generic = any(p in low for p in GENERIC_PHRASES)
    has_structural = any(m in low for m in STRUCTURAL_MARKERS)
    short = len(body) < RESONANCE_SHORT_LEN
    # flagged if: explicit generic phrasing w/o structural language, OR very short w/o structure
    if has_generic and not has_structural:
        return True
    if short and not has_structural:
        return True
    return False


def norm(text):
    return re.sub(r"\s+", " ", (text or "").strip().lower())


# ---- Main -----------------------------------------------------------------

def main():
    units = load_units(INDEX)
    total = len(units)

    valid_unit_ids = {u.get("unit_id") for u in units if u.get("unit_id")}

    # coverage buckets
    cov_overall = Counter()          # bucket -> count
    cov_by_work = defaultdict(Counter)
    work_title = {}

    # item-level tallies
    total_items = 0
    title_only = []          # (unit_id, citation, passage_id)
    div_missing = []         # (unit_id, citation)
    div_trivial = []         # (unit_id, citation, divergence)
    theme_only = []          # (unit_id, citation, resonance)
    dangling = []            # (unit_id, passage_id)
    pid_present = 0
    pid_wellformed = 0

    resonance_text_map = defaultdict(list)   # normalized resonance -> [unit_ids]

    for u in units:
        wid = u.get("work_id") or "(none)"
        work_title[wid] = u.get("work_title") or wid
        items = get_resonance_items(u)
        n = len(items)

        if n == 0:
            bucket = "0"
        elif n == 1:
            bucket = "1"
        elif n <= 4:
            bucket = "2-4"
        else:
            bucket = ">4"
        cov_overall[bucket] += 1
        cov_by_work[wid][bucket] += 1

        uid = u.get("unit_id")
        for it in items:
            total_items += 1
            pid = (it.get("passage_id") or "").strip()
            citation = it.get("citation") or ""

            if pid:
                pid_present += 1
                if PID_RE.match(pid):
                    pid_wellformed += 1
                if pid not in valid_unit_ids:
                    dangling.append((uid, pid, citation))

            if not points_to_specific_passage(it):
                title_only.append((uid, citation.strip(), pid))

            dv = divergence_missing_or_trivial(it)
            if dv == "missing":
                div_missing.append((uid, citation.strip()))
            elif dv == "trivial":
                div_trivial.append((uid, citation.strip(), (it.get("divergence") or "").strip()))

            if asserts_theme_only(it):
                theme_only.append((uid, citation.strip(), (it.get("resonance") or "").strip()))

            r = norm(it.get("resonance"))
            if r:
                resonance_text_map[r].append(uid)

    # duplication: resonance texts reused across >1 unit
    dups = [(text, uids) for text, uids in resonance_text_map.items() if len(set(uids)) > 1]
    dups.sort(key=lambda x: -len(set(x[1])))

    report = build_report(
        total, cov_overall, cov_by_work, work_title,
        total_items, title_only, div_missing, div_trivial, theme_only,
        dangling, pid_present, pid_wellformed, dups,
        units_with_res=cov_overall["1"] + cov_overall["2-4"] + cov_overall[">4"],
    )

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(report)

    # console summary
    print(report)
    print(f"\n[written] {OUT}")


def pct(n, d):
    return f"{(100.0 * n / d):.1f}%" if d else "0.0%"


def build_report(total, cov_overall, cov_by_work, work_title,
                 total_items, title_only, div_missing, div_trivial, theme_only,
                 dangling, pid_present, pid_wellformed, dups, units_with_res):
    L = []
    W = L.append
    W("# Pratibha Corpus Audit — Cross-Tradition Resonances Quality\n")
    W(f"_Source: `data/canonical/index.jsonl` — {total} canonical units. "
      f"Read-only audit; no data modified._\n")

    # ---- 1. Coverage ----
    W("\n## 1. Coverage distribution\n")
    W(f"- **Units with a structured `resonances` layer:** {units_with_res} / {total} "
      f"({pct(units_with_res, total)})\n")
    W(f"- **Total resonance items across corpus:** {total_items}\n")
    W("\n| Resonance count | Units | Share |\n|---|---|---|\n")
    for b in ["0", "1", "2-4", ">4"]:
        W(f"| {b} | {cov_overall[b]} | {pct(cov_overall[b], total)} |\n")
    below = cov_overall["0"] + cov_overall["1"]
    W(f"\n**{below} / {total} units ({pct(below, total)}) fall below the 2-entry "
      f"minimum** (0 or 1 resonance). Only {cov_overall['2-4']} "
      f"({pct(cov_overall['2-4'], total)}) sit in the 2-4 target band.\n")

    W("\n### Per-work coverage\n")
    W("| Work | Units | 0 | 1 | 2-4 | >4 | % below min |\n|---|---|---|---|---|---|---|\n")
    for wid in sorted(cov_by_work, key=lambda w: work_title.get(w, w).lower()):
        c = cov_by_work[wid]
        wtot = c["0"] + c["1"] + c["2-4"] + c[">4"]
        bel = c["0"] + c["1"]
        W(f"| {work_title.get(wid, wid)} | {wtot} | {c['0']} | {c['1']} | "
          f"{c['2-4']} | {c['>4']} | {pct(bel, wtot)} |\n")

    # ---- 2. Title-only ----
    W("\n## 2. \"Cites titles, not verses\" — title-only resonances\n")
    W(f"- **Resonance items pointing to NO specific passage** "
      f"(no well-formed `passage_id` AND citation lacks any verse/section/number marker): "
      f"**{len(title_only)} / {total_items}** ({pct(len(title_only), total_items)}).\n")
    W(f"- `passage_id` present on {pid_present}/{total_items} items "
      f"({pct(pid_present, total_items)}); well-formed (`work.unit`) on "
      f"{pid_wellformed}/{total_items} ({pct(pid_wellformed, total_items)}).\n")
    if title_only:
        W("\nExamples (unit_id — citation — passage_id):\n")
        for uid, cit, pid in title_only[:12]:
            W(f"- `{uid}` — \"{cit or '(empty citation)'}\" — passage_id: `{pid or '(none)'}`\n")

    # ---- 3. Divergence ----
    W("\n## 3. Divergence clause quality\n")
    W(f"- **Missing (empty) divergence:** {len(div_missing)} items.\n")
    W(f"- **Trivial divergence** (< {DIVERGENCE_MIN_LEN} chars): {len(div_trivial)} items.\n")
    if div_missing:
        W("\nExamples missing divergence (unit_id — citation):\n")
        for uid, cit in div_missing[:10]:
            W(f"- `{uid}` — \"{cit}\"\n")
    if div_trivial:
        W("\nExamples trivial divergence (unit_id — divergence):\n")
        for uid, cit, dv in div_trivial[:8]:
            W(f"- `{uid}` — \"{dv}\"\n")

    # ---- 4. Depth ----
    W("\n## 4. Depth — theme-only (non-structural) resonances\n")
    W(f"- **Items flagged as asserting shared THEME rather than structural homology:** "
      f"**{len(theme_only)} / {total_items}** ({pct(len(theme_only), total_items)}).\n")
    W("  (Heuristic: generic phrasing like \"both discuss / both emphasize\" without "
      "structural-claim vocabulary, or very short bodies lacking a structural claim.)\n")
    if theme_only:
        W("\nExamples (unit_id — resonance excerpt):\n")
        for uid, cit, body in theme_only[:8]:
            excerpt = body[:160].replace("\n", " ")
            W(f"- `{uid}` — \"{excerpt}{'…' if len(body) > 160 else ''}\"\n")

    # ---- 5. Integrity ----
    W("\n## 5. Integrity — dangling passage_id references\n")
    W(f"- **`passage_id` values that do NOT resolve to any unit_id in the corpus:** "
      f"**{len(dangling)}** (of {pid_present} passage_ids present).\n")
    if dangling:
        W("\nExamples (unit_id — dangling passage_id — citation):\n")
        for uid, pid, cit in dangling[:15]:
            W(f"- `{uid}` → `{pid}`  (\"{cit}\")\n")

    # ---- 6. Duplication ----
    W("\n## 6. Duplication — templated resonance text\n")
    W(f"- **Distinct resonance bodies reused across >1 unit:** {len(dups)} "
      f"template strings.\n")
    if dups:
        total_dup_units = sum(len(set(u)) for _, u in dups)
        W(f"- Together these span **{total_dup_units} unit-occurrences**.\n")
        W("\nMost-reused resonance texts (reuse count — excerpt — example units):\n")
        for text, uids in dups[:10]:
            uu = sorted(set(uids))
            excerpt = text[:120]
            W(f"- **×{len(uu)}** — \"{excerpt}…\" — e.g. {', '.join('`'+x+'`' for x in uu[:4])}\n")

    # ---- Recommendations ----
    W("\n## 7. Prioritized recommendations\n")
    below = cov_overall["0"] + cov_overall["1"]
    recs = []
    recs.append(
        f"**Close the coverage gap first.** {below}/{total} units ({pct(below, total)}) "
        f"are below the 2-entry minimum — {cov_overall['0']} have zero. Generating "
        f"resonances for zero-coverage units is the single highest-leverage fix, since it "
        f"unlocks the whole layer rather than polishing existing entries."
    )
    if dangling:
        recs.append(
            f"**Repair {len(dangling)} dangling `passage_id` links.** These break the "
            f"cross-reference graph; either remap to a real unit_id or drop the field. "
            f"Add a CI check that validates every `passage_id` against the index."
        )
    recs.append(
        f"**Enforce specific-passage citation.** {len(title_only)} items ({pct(len(title_only), total_items)}) "
        f"cite only a work/author with no verse/section anchor. Require a well-formed "
        f"`passage_id` (currently only {pct(pid_wellformed, total_items)} of items) or a "
        f"citation containing an explicit locus before a resonance is accepted."
    )
    recs.append(
        f"**Raise depth from theme to structure.** {len(theme_only)} items read as "
        f"shared-theme assertions rather than structural homology. Flag generic phrasing "
        f"in review and require a named structural move (reduction, inversion, mechanism, etc.)."
    )
    if div_missing or div_trivial:
        recs.append(
            f"**Backfill divergence clauses.** {len(div_missing)} missing + {len(div_trivial)} "
            f"trivial. The divergence clause is mandatory per spec; treat its absence as a "
            f"hard validation failure."
        )
    if dups:
        recs.append(
            f"**De-template duplicated resonances.** {len(dups)} resonance bodies are copied "
            f"verbatim across multiple units; rewrite them to the specific passage at hand."
        )
    for i, r in enumerate(recs, 1):
        W(f"{i}. {r}\n")

    return "".join(L)


if __name__ == "__main__":
    main()
