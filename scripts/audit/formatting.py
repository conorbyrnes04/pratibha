#!/usr/bin/env python3
"""
Pratibha corpus audit — FORMATTING & STRUCTURAL CONSISTENCY (READ-ONLY).

Audits data/canonical/index.jsonl against the Pratibha MD spec
(.cursor/skills/pratibha-md/SKILL.md). Detects:
  1. Layer completeness (missing keyterms / resonances / commentary / practice / translation)
  2. Buried / malformed resonances (resonances pasted into commentary text)
  3. Filler / templated boilerplate content
  4. Field consistency (commentary==insight, translation dup, layer order, appendix mismatch)
  5. Corpus hygiene (duplicate / near-duplicate work dirs, orphan dirs)

Writes findings to scripts/audit/formatting.md. Does NOT modify any data.

Run:
  cd /Users/conorbyrnes04/Documents/Projects/VAK/pratibha && python3 scripts/audit/formatting.py
"""

import json
import os
import re
import unicodedata
from collections import Counter, defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INDEX = os.path.join(ROOT, "data", "canonical", "index.jsonl")
CANON_DIR = os.path.join(ROOT, "data", "canonical")
OUT_MD = os.path.join(os.path.dirname(__file__), "formatting.md")

EXPECTED_ORDER = ["original", "iast", "translation", "commentary",
                  "keyterms", "resonances", "practice"]
CORE_KINDS = ["original", "iast", "translation", "commentary",
              "keyterms", "resonances", "practice"]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def norm_text(s):
    """Normalize a body of text for exact-duplicate grouping."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def norm_name(name):
    """Fold a work/dir name to compare near-duplicates.
    Strips diacritics, lowercases, drops non-alnum, collapses common variants."""
    n = unicodedata.normalize("NFKD", name)
    n = "".join(c for c in n if not unicodedata.combining(c))
    n = n.lower()
    n = re.sub(r"[^a-z0-9]", "", n)
    return n


def phon_fold(name):
    """Aggressive phonetic fold to cluster transliteration variants
    (shiva/siva/śiva, vijnana/vijñāna, upanishad/upaniṣad)."""
    n = norm_name(name)
    n = n.replace("sh", "s")          # sh -> s
    n = re.sub(r"(.)\1+", r"\1", n)    # collapse doubled letters
    return n


def layer_body(layer):
    return layer.get("body") or ""


def load_units():
    units = []
    with open(INDEX, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                units.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"WARN: line {i} unparseable: {e}")
    return units


# ---------------------------------------------------------------------------
# detectors
# ---------------------------------------------------------------------------

# Regexes for resonances buried in prose commentary.
RES_HEADER_RE = re.compile(r"cross[\s\-]*tradition\s+resonances?\s*[:\-]", re.I)
RES_LOOSE_RE = re.compile(r"^\s*(?:\*\*)?resonances?\s*[:\-]", re.I | re.M)
DIVERGENCE_RE = re.compile(r"^\s*[-*]?\s*\*?divergence\*?\s*[:\-]", re.I | re.M)


def resonance_buried_in(text):
    if not text:
        return False
    if RES_HEADER_RE.search(text):
        return True
    if RES_LOOSE_RE.search(text) and DIVERGENCE_RE.search(text):
        return True
    return False


def main():
    units = load_units()
    n = len(units)

    # ---- group by work ----
    by_work = defaultdict(list)
    for u in units:
        by_work[u.get("work_id") or "(none)"].append(u)

    # ---- 1. layer completeness ----
    # per-work counts of missing each core kind
    work_missing = defaultdict(lambda: defaultdict(int))
    work_total = defaultdict(int)
    global_missing = defaultdict(int)
    units_with_no_layers = []

    for u in units:
        w = u.get("work_id") or "(none)"
        work_total[w] += 1
        layers = u.get("pratibha_layers") or []
        kinds = set()
        for L in layers:
            k = L.get("kind")
            # a layer counts as "present" only if it has content
            has_content = bool((L.get("body") or "").strip()) or bool(L.get("items"))
            if has_content:
                kinds.add(k)
        if not layers:
            units_with_no_layers.append(u["unit_id"])
        for k in CORE_KINDS:
            if k not in kinds:
                work_missing[w][k] += 1
                global_missing[k] += 1

    # ---- 2. buried / malformed resonances ----
    buried = []          # buried in commentary AND no structured resonances layer
    buried_but_has_layer = []  # buried text present but layer also exists
    for u in units:
        layers = u.get("pratibha_layers") or []
        has_res_layer = any(
            L.get("kind") == "resonances" and (L.get("items") or (L.get("body") or "").strip())
            for L in layers
        )
        commentary = u.get("commentary") or ""
        # also scan commentary layer body
        for L in layers:
            if L.get("kind") == "commentary":
                commentary = commentary or layer_body(L)
        if resonance_buried_in(commentary):
            if has_res_layer:
                buried_but_has_layer.append(u["unit_id"])
            else:
                buried.append(u["unit_id"])

    # ---- 3. filler / templated content ----
    KNOWN_FILLER = {
        "practice": [
            "Read this passage slowly three times. Pause for one minute and "
            "write one sentence about how to apply it today.",
        ],
        "commentary": [
            "Read this line as a contemplative pointer: pause interpretation "
            "for a moment and let the insight disclose itself directly.",
        ],
    }
    known_filler_norm = {
        field: {norm_text(s) for s in lst} for field, lst in KNOWN_FILLER.items()
    }

    filler_hits = defaultdict(list)  # (field, normtext) -> [unit_ids]
    commentary_counter = Counter()
    practice_counter = Counter()
    insight_counter = Counter()
    commentary_examples = {}
    practice_examples = {}
    insight_examples = {}

    for u in units:
        c = norm_text(u.get("commentary"))
        p = norm_text(u.get("practice"))
        ins = norm_text(u.get("insight"))
        if c:
            commentary_counter[c] += 1
            commentary_examples.setdefault(c, (u["unit_id"], (u.get("commentary") or "")[:160]))
        if p:
            practice_counter[p] += 1
            practice_examples.setdefault(p, (u["unit_id"], (u.get("practice") or "")[:160]))
        if ins:
            insight_counter[ins] += 1
            insight_examples.setdefault(ins, (u["unit_id"], (u.get("insight") or "")[:160]))
        if c and c in known_filler_norm["commentary"]:
            filler_hits[("commentary", c)].append(u["unit_id"])
        if p and p in known_filler_norm["practice"]:
            filler_hits[("practice", p)].append(u["unit_id"])

    # ---- 4. field consistency ----
    commentary_eq_insight = []
    translation_dup = []       # translation_literal == translation layer body
    order_deviation = []       # core kinds not in expected relative order
    appendix_mismatch = []     # appendixes[] vs appendix layer presence disagree

    for u in units:
        c = norm_text(u.get("commentary"))
        ins = norm_text(u.get("insight"))
        if c and ins and c == ins:
            commentary_eq_insight.append(u["unit_id"])

        layers = u.get("pratibha_layers") or []
        tl = norm_text(u.get("translation_literal"))
        for L in layers:
            if L.get("kind") == "translation":
                if tl and norm_text(layer_body(L)) == tl:
                    translation_dup.append(u["unit_id"])
                break

        # order deviation: sequence of core kinds should be a subsequence of EXPECTED_ORDER
        seq = [L.get("kind") for L in layers if L.get("kind") in EXPECTED_ORDER]
        rank = {k: i for i, k in enumerate(EXPECTED_ORDER)}
        ranks = [rank[k] for k in seq if k in rank]
        if ranks != sorted(ranks):
            order_deviation.append((u["unit_id"], seq))

        # appendix consistency
        has_appendix_layer = any(L.get("kind") == "appendix" for L in layers)
        has_appendix_field = bool(u.get("appendixes"))
        if has_appendix_layer != has_appendix_field:
            appendix_mismatch.append((u["unit_id"], has_appendix_field, has_appendix_layer))

    # ---- 5. corpus hygiene ----
    dirs = [d for d in os.listdir(CANON_DIR)
            if os.path.isdir(os.path.join(CANON_DIR, d))]
    dir_ymls = {}
    for d in dirs:
        p = os.path.join(CANON_DIR, d)
        ymls = [f for f in os.listdir(p) if f.endswith((".yml", ".yaml"))]
        dir_ymls[d] = len(ymls)

    works_in_index = set(by_work.keys())
    orphan_dirs = sorted(d for d in dirs if d not in works_in_index)
    empty_dirs = sorted(d for d, c in dir_ymls.items() if c == 0)
    works_no_dir = sorted(w for w in works_in_index if w not in dirs and w != "(none)")

    # --- cluster dirs by phonetic fold, then merge clusters that are
    #     prefix-supersets of one another (e.g. base vs base_the_sacred_texts). ---
    fold_groups = defaultdict(list)
    for d in dirs:
        fold_groups[phon_fold(d)].append(d)

    keys = list(fold_groups.keys())
    parent = {k: k for k in keys}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        parent[find(a)] = find(b)

    for i in range(len(keys)):
        for j in range(len(keys)):
            if i == j:
                continue
            a, b = keys[i], keys[j]
            if a and b and a != b and b.startswith(a) and len(a) >= 6:
                union(a, b)

    merged = defaultdict(list)
    for k in keys:
        merged[find(k)].extend(fold_groups[k])

    dup_dir_clusters = {}
    for root_key, group in merged.items():
        group = sorted(set(group))
        if len(group) > 1:
            dup_dir_clusters[root_key] = group

    # map each empty/orphan dir to the populated canonical dir in its cluster
    orphan_to_home = {}
    for group in dup_dir_clusters.values():
        populated = [d for d in group if dir_ymls.get(d, 0) > 0]
        canonical = max(populated, key=lambda d: dir_ymls.get(d, 0)) if populated else None
        for d in group:
            if dir_ymls.get(d, 0) == 0 and canonical:
                orphan_to_home[d] = canonical

    # =====================================================================
    # write markdown
    # =====================================================================
    lines = []
    W = lines.append

    W("# Pratibha Corpus Audit — Formatting & Structural Consistency\n")
    W(f"_Read-only audit over `data/canonical/index.jsonl` ({n} units, "
      f"{len(work_total)} works). Spec: `.cursor/skills/pratibha-md/SKILL.md`._\n")

    # --- 1. layer completeness ---
    W("## 1. Layer Completeness (per work)\n")
    W("Expected layers per unit, in order: "
      "Original → IAST → Translation → Commentary → Key Terms → Resonances → Practice.\n")
    W("Counts below = units in that work **missing** each layer (empty layers count as missing).\n")
    header = "| work | units | miss orig | miss iast | miss transl | miss comm | miss keyterms | miss reson | miss practice |"
    W(header)
    W("|" + "---|" * 9)
    for w in sorted(work_total, key=lambda x: (-work_missing[x]["keyterms"], x)):
        m = work_missing[w]
        W(f"| {w} | {work_total[w]} | {m['original']} | {m['iast']} | "
          f"{m['translation']} | {m['commentary']} | {m['keyterms']} | "
          f"{m['resonances']} | {m['practice']} |")
    W("")
    W("**Corpus totals (units missing layer):**\n")
    for k in CORE_KINDS:
        W(f"- `{k}`: {global_missing[k]} / {n} "
          f"({100*global_missing[k]/n:.1f}%)")
    W("")
    if units_with_no_layers:
        W(f"- Units with **zero** pratibha_layers: {len(units_with_no_layers)} "
          f"(e.g. {', '.join(units_with_no_layers[:5])})")
    W("")

    # --- 2. buried resonances ---
    W("## 2. Buried / Malformed Resonances\n")
    W(f"- **{len(buried)}** units have cross-tradition resonances pasted into "
      f"the commentary text with **no** structured `resonances` layer.")
    if buried:
        W(f"  - Examples: {', '.join(buried[:20])}"
          + (" …" if len(buried) > 20 else ""))
    W(f"- **{len(buried_but_has_layer)}** units have resonance text in commentary "
      f"*and* a structured layer (redundant / needs cleanup).")
    if buried_but_has_layer:
        W(f"  - Examples: {', '.join(buried_but_has_layer[:15])}"
          + (" …" if len(buried_but_has_layer) > 15 else ""))
    W("")

    # --- 3. filler / templated ---
    W("## 3. Filler / Templated Content\n")
    W("### Known boilerplate strings\n")
    if filler_hits:
        for (field, _txt), ids in sorted(filler_hits.items(), key=lambda x: -len(x[1])):
            example = KNOWN_FILLER[field][0]
            W(f"- **{field}** filler — **{len(ids)}** units: "
              f"\"{example[:80]}…\"")
            W(f"  - e.g. {', '.join(ids[:12])}" + (" …" if len(ids) > 12 else ""))
    else:
        W("- No exact known-boilerplate matches found.")
    W("")

    def dump_top(counter, examples, label, top=8):
        W(f"### Top duplicated `{label}` bodies\n")
        W(f"| count | unit_id (example) | text (truncated) |")
        W("|---|---|---|")
        for txt, cnt in counter.most_common(top):
            if cnt < 2:
                continue
            uid, snippet = examples[txt]
            snippet = snippet.replace("\n", " ").replace("|", "\\|")
            W(f"| {cnt} | {uid} | {snippet[:90]} |")
        W("")

    dump_top(commentary_counter, commentary_examples, "commentary")
    dump_top(practice_counter, practice_examples, "practice")
    dump_top(insight_counter, insight_examples, "insight")

    # --- 4. field consistency ---
    W("## 4. Field Consistency\n")
    W(f"- **commentary == insight** (verbatim): {len(commentary_eq_insight)} units."
      + (f" e.g. {', '.join(commentary_eq_insight[:10])}" if commentary_eq_insight else ""))
    W(f"- **translation_literal == translation layer body** (only content): "
      f"{len(translation_dup)} units."
      + (f" e.g. {', '.join(translation_dup[:10])}" if translation_dup else ""))
    W(f"  - _Note: near-universal ({100*len(translation_dup)/n:.0f}%) — the "
      f"`Pratibha Translation` layer merely mirrors `translation_literal`, i.e. "
      f"no distinct interpretive translation exists separate from the literal one._")
    W(f"- **Layer order deviations** (core layers out of spec order): "
      f"{len(order_deviation)} units.")
    if order_deviation:
        oc = Counter(tuple(seq) for _uid, seq in order_deviation)
        for seq, cnt in oc.most_common(6):
            ex = next(uid for uid, s in order_deviation if tuple(s) == seq)
            W(f"  - {cnt}×  `{' → '.join(seq)}`  (e.g. {ex})")
    W(f"- **Appendix field/layer mismatch**: {len(appendix_mismatch)} units.")
    if appendix_mismatch:
        for uid, fld, lyr in appendix_mismatch[:8]:
            W(f"  - {uid}: appendixes_field={fld}, appendix_layer={lyr}")
    W("")

    # --- 5. corpus hygiene ---
    W("## 5. Corpus Hygiene — Duplicate / Orphan Works\n")
    W(f"- Directories under `data/canonical/`: {len(dirs)}; "
      f"work_ids in index: {len(works_in_index)}.\n")
    W("### Near-duplicate / variant-spelling directory clusters\n")
    W("Each cluster groups transliteration variants (diacritics, sh/s, doubled "
      "letters, long-name variants). `(N yml)` = files present; canonical = the "
      "populated one.\n")
    if dup_dir_clusters:
        for _fold, group in sorted(dup_dir_clusters.items(),
                                   key=lambda kv: -max(dir_ymls.get(d, 0) for d in kv[1])):
            canonical = max(group, key=lambda d: dir_ymls.get(d, 0))
            parts = []
            for d in sorted(group, key=lambda d: -dir_ymls.get(d, 0)):
                mark = " ← canonical" if d == canonical and dir_ymls.get(d, 0) else ""
                parts.append(f"`{d}` ({dir_ymls.get(d,0)} yml){mark}")
            W(f"- " + "; ".join(parts))
    else:
        W("- None found by name-folding.")
    W("")
    W("### Orphan / empty directories\n")
    W(f"- Empty dirs (0 yml files) — **{len(empty_dirs)}**: "
      + ", ".join(f"`{d}`" for d in empty_dirs))
    W(f"- Dirs not present as work_id in index — **{len(orphan_dirs)}**: "
      + ", ".join(f"`{d}`" for d in orphan_dirs))
    W(f"- work_ids in index with no matching dir: {works_no_dir or 'none'}")
    W("")
    if orphan_to_home:
        W("**Suggested consolidation (empty orphan → canonical home, name-matched):**\n")
        for d in sorted(orphan_to_home):
            W(f"- `{d}` (0 yml) → merge/delete in favor of "
              f"`{orphan_to_home[d]}` ({dir_ymls.get(orphan_to_home[d],0)} yml)")
        W("")

    # semantic (content-level) duplicates that name-folding cannot catch
    SEMANTIC_HINTS = {
        "vbt_translation_wallis_2": "vijnana_bhairava (VBT = Vijñāna Bhairava Tantra, Wallis translation)",
        "know_yourself_an_explanation_of_the_oneness_of_being": "know_yourself_ibn_arabi_balyani (same Balyāni treatise)",
        "the_manual_for_self_realization_112_meditations_of_the": "vijnana_bhairava / self_realization_manual (112 dhāraṇās = VBT)",
        "self_realization_manual": "vijnana_bhairava / the_manual_for_self_realization_112... (same 112 meditations)",
        "utpaladeva_philosopher_of_recognition": "pratyabhijnahrdayam (Utpaladeva / Pratyabhijñā recognition school)",
        "the_ubiquitous_siva_somananda_s_sivadrsti_and_his_tantric": "siva_sutra / pratyabhijnahrdayam (Somānanda Śivadṛṣṭi — Pratyabhijñā lineage)",
        "tantra_illuminated_the_philosophy_history_and_practice": "tantrasara (Tantra Illuminated — secondary/overview work)",
    }
    remaining = [d for d in empty_dirs if d not in orphan_to_home]
    hinted = [d for d in remaining if d in SEMANTIC_HINTS]
    if hinted:
        W("**Empty orphans with no name match — likely content-level duplicates / "
          "legacy dirs (editorial judgement needed):**\n")
        for d in sorted(hinted):
            W(f"- `{d}` (0 yml) → likely related to {SEMANTIC_HINTS[d]}")
        W("")

    # --- prioritized fixes ---
    W("## Prioritized Fixes\n")
    fixes = []
    if global_missing["keyterms"] > n * 0.5:
        fixes.append(
            f"**Key Terms layer is absent corpus-wide** "
            f"({global_missing['keyterms']}/{n} units). Either the extractor never "
            f"emits `kind=='keyterms'` or the field is unpopulated — fix the pipeline "
            f"so Key Terms are generated and structured.")
    if global_missing["resonances"]:
        fixes.append(
            f"**Backfill structured resonances** for the "
            f"{global_missing['resonances']} units missing a `resonances` layer, "
            f"starting with the {len(buried)} where resonances are already written "
            f"but trapped inside commentary prose — migrate those out first.")
    top_filler = max((len(v) for v in filler_hits.values()), default=0)
    if top_filler:
        fixes.append(
            f"**Replace templated filler** — the single most common boilerplate "
            f"string covers {top_filler} units; regenerate real, passage-specific "
            f"practice/commentary for these.")
    if commentary_eq_insight:
        fixes.append(
            f"**De-duplicate commentary/insight** — {len(commentary_eq_insight)} "
            f"units copy commentary verbatim into `insight`; derive a distinct "
            f"one-line insight or drop the field.")
    if dup_dir_clusters or empty_dirs:
        fixes.append(
            f"**Consolidate {len(orphan_to_home)} empty variant/orphan directories** "
            f"(diacritic & sh/s spellings, long-name duplicates) into their canonical "
            f"work_id to stop split provenance and confusion.")
    if order_deviation:
        fixes.append(
            f"**Normalize layer order** in {len(order_deviation)} units to the spec "
            f"sequence (practice currently precedes resonances in many units).")
    for i, fx in enumerate(fixes[:6], 1):
        W(f"{i}. {fx}")
    W("")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # ---- console summary ----
    print(f"Audited {n} units across {len(work_total)} works.")
    print("Missing layers (corpus):",
          {k: global_missing[k] for k in CORE_KINDS})
    print(f"Buried resonances (no layer): {len(buried)}; "
          f"buried+layer: {len(buried_but_has_layer)}")
    print("Known filler hits:",
          {f"{fld}": len(ids) for (fld, _t), ids in filler_hits.items()})
    print(f"commentary==insight: {len(commentary_eq_insight)}; "
          f"translation dup: {len(translation_dup)}; "
          f"order deviations: {len(order_deviation)}; "
          f"appendix mismatch: {len(appendix_mismatch)}")
    print(f"Dup dir clusters: {sum(len(v) for v in dup_dir_clusters.values())} dirs "
          f"in {len(dup_dir_clusters)} clusters; empty dirs: {len(empty_dirs)}; "
          f"orphan dirs: {len(orphan_dirs)}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
