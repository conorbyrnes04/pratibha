#!/usr/bin/env python3
"""
Pratibha corpus audit — ORIGINAL-LANGUAGE TEXT dimension (READ-ONLY).

Loads data/canonical/index.jsonl and measures, per unit and aggregated per work:
  1. Presence/absence of original-language text (sanskrit_devanagari,
     sanskrit_iast, and a non-empty pratibha_layers entry of kind
     "original" or "iast").
  2. Language-appropriateness: Sanskrit works should carry Devanagari + IAST;
     Greek/Chinese/Arabic/Persian/Tibetan/Japanese/German works should carry
     their native source script (or an explicit, labelled source-language
     basis). Placeholder "originals" (e.g. "*(Greek original not in
     corpus...)*", "*Source-language basis:* ...") are flagged, not counted as
     real original text.
  3. Consistency: IAST present but Devanagari missing (or vice-versa);
     native-script field populated with romanized text (malformed).
  4. Per-work coverage table: % of units with complete original + IAST /
     native original-script.

Writes findings to scripts/audit/original_language.md.

This script only READS data files. It never writes to data/.
"""

from __future__ import annotations

import json
import os
import re
from collections import Counter, defaultdict
from typing import Optional

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INDEX = os.path.join(ROOT, "data", "canonical", "index.jsonl")
CANONICAL_DIR = os.path.join(ROOT, "data", "canonical")
REPORT = os.path.join(os.path.dirname(__file__), "original_language.md")

# --- Language classification (provenance fields are all null, so key on work_id) ---
# script codes: deva, greek, cjk (han + kana), arabic, tibetan, latin (no distinct script)
WORK_LANG = {
    # Sanskrit — require Devanagari + IAST
    "astavakra_gita": "sanskrit",
    "bhagavad_gita": "sanskrit",
    "chāndogya_upaniṣad": "sanskrit",
    "heart_sutra": "sanskrit",
    "isavasya_upanishad": "sanskrit",
    "mandukya_upanishad_and_gaudapada_karika": "sanskrit",
    "nagarjuna_mulamadhyamakakarika": "sanskrit",
    "patañjali_yoga_sūtras": "sanskrit",
    "pratyabhijnahrdayam": "sanskrit",
    "shantideva_bodhicaryavatara": "sanskrit",
    "siva_sutra": "sanskrit",
    "svetasvatara_upanishad": "sanskrit",
    "tantrasara": "sanskrit",
    "vijnana_bhairava": "sanskrit",
    "yoga_spandakarika": "sanskrit",
    "yoginihrdaya": "sanskrit",
    # Greek — require Greek script (IAST N/A)
    "epictetus_works": "greek",
    "heraclitus_fragments": "greek",
    "phaedo_plato": "greek",
    "plotinus_enneads": "greek",
    # Chinese — require Han characters (pinyin N/A for IAST)
    "tao_te_ching": "chinese",
    "the_book_of_chuang_tzu": "chinese",
    # Persian / Arabic — require Arabic script
    "rumi_mathnawi": "persian",
    "conference_of_the_birds": "persian",
    "kashf_al_mahjub": "persian",
    "know_yourself_ibn_arabi_balyani": "arabic",
    # Tibetan — native Tibetan script preferred; romanized Wylie = labelled basis
    "milarepa_songs": "tibetan",
    "tilopa_mahamudra": "tibetan",
    # Japanese — require kana/kanji
    "dogen_shobogenzo": "japanese",
    # Middle High German — Latin-script original text
    "meister_eckhart": "german",
}

LANG_SCRIPT = {
    "sanskrit": "deva",
    "greek": "greek",
    "chinese": "cjk",
    "persian": "arabic",
    "arabic": "arabic",
    "tibetan": "tibetan",
    "japanese": "cjk",
    "german": "latin",  # no distinct script; presence of a real body suffices
}

# Empty / duplicate work directories under data/canonical (corpus hygiene).
def find_empty_dirs() -> list[str]:
    empties = []
    if not os.path.isdir(CANONICAL_DIR):
        return empties
    for name in sorted(os.listdir(CANONICAL_DIR)):
        p = os.path.join(CANONICAL_DIR, name)
        if os.path.isdir(p) and not os.listdir(p):
            empties.append(name)
    return empties


# --- Script detection ---
def _has(text: str, lo: int, hi: int) -> bool:
    return any(lo <= ord(c) <= hi for c in text)


def detect_scripts(text: str) -> set[str]:
    s = set()
    if not text:
        return s
    if _has(text, 0x0900, 0x097F):
        s.add("deva")
    if _has(text, 0x0370, 0x03FF) or _has(text, 0x1F00, 0x1FFF):
        s.add("greek")
    if _has(text, 0x4E00, 0x9FFF):
        s.add("cjk")
    if _has(text, 0x3040, 0x30FF):  # kana
        s.add("cjk")
    if _has(text, 0x0600, 0x06FF) or _has(text, 0x0750, 0x077F):
        s.add("arabic")
    if _has(text, 0x0F00, 0x0FFF):
        s.add("tibetan")
    # latin with combining diacritics (IAST etc.)
    if _has(text, 0x0041, 0x007A) or _has(text, 0x00C0, 0x024F) or _has(text, 0x1E00, 0x1EFF):
        s.add("latin")
    return s


# Text that is a note ABOUT the source language rather than the source text itself.
PLACEHOLDER_PAT = re.compile(
    r"source-language basis|not applicable|^\s*n/a\b|see original|not in corpus|"
    r"not yet aligned|not directly provided|pending|no sanskrit original|"
    r"chinese text|chinese source|greek text|greek source|greek original|"
    r"tibetan \(|persian original|arabic original|romaniz",
    re.I,
)


def is_placeholder_note(text: str, native_script: str) -> bool:
    """True if `text` is a meta-note (no native script) rather than real original text."""
    if not text or not text.strip():
        return False
    scripts = detect_scripts(text)
    if native_script in scripts:
        return False  # contains real native script -> not a pure placeholder
    t = text.strip()
    if t.startswith("*(") or t.startswith("("):
        return True
    return bool(PLACEHOLDER_PAT.search(t[:120]))


def layer_body(unit: dict, kind: str) -> Optional[str]:
    """Return the body of the first pratibha_layer of `kind`, or None if absent.

    Layers that carry `items` instead of `body` are serialised so we can still
    test for non-emptiness / script content.
    """
    for layer in unit.get("pratibha_layers") or []:
        if layer.get("kind") == kind:
            body = layer.get("body")
            if (body is None or not str(body).strip()) and layer.get("items"):
                body = json.dumps(layer["items"], ensure_ascii=False)
            return body or ""
    return None


class UnitFinding:
    __slots__ = (
        "unit_id", "work_id", "lang", "native_script",
        "deva_field", "iast_field", "orig_layer", "iast_layer",
        "orig_text", "orig_scripts",
        "has_native_original", "has_iast",
        "problem",  # one of the problem-class tags, or None
    )

    def __init__(self, unit: dict):
        self.unit_id = unit.get("unit_id")
        self.work_id = unit.get("work_id")
        self.lang = WORK_LANG.get(self.work_id, "unknown")
        self.native_script = LANG_SCRIPT.get(self.lang, "latin")

        self.deva_field = (unit.get("sanskrit_devanagari") or "").strip()
        self.iast_field = (unit.get("sanskrit_iast") or "").strip()
        self.orig_layer = layer_body(unit, "original")
        self.iast_layer = layer_body(unit, "iast")

        # Best candidate for the "original" text: layer body, else deva field.
        ol = (self.orig_layer or "").strip()
        self.orig_text = ol if ol else self.deva_field
        self.orig_scripts = detect_scripts(self.orig_text)

        # Does real native-script original text exist anywhere?
        native = self.native_script
        if native == "latin":
            # German: any non-placeholder original body counts.
            self.has_native_original = bool(
                self.orig_text and not is_placeholder_note(self.orig_text, native)
            )
        else:
            self.has_native_original = (
                native in self.orig_scripts or native in detect_scripts(self.deva_field)
            )

        # IAST present? (real transliteration, not a "See Original" note)
        il = (self.iast_layer or "").strip()
        iast_candidates = [c for c in (il, self.iast_field) if c]
        self.has_iast = any(
            ("latin" in detect_scripts(c)) and not is_placeholder_note(c, "latin-note")
            and not re.match(r"^\s*(see original|n/a\b|not applicable)", c, re.I)
            for c in iast_candidates
        )

        self.problem = self._classify()

    def _classify(self) -> Optional[str]:
        native = self.native_script
        has_any_orig_text = bool(self.orig_text and self.orig_text.strip())

        # A. Missing entirely: no original text and (for sanskrit) no IAST either.
        if not has_any_orig_text and not self.iast_field and not (self.iast_layer or "").strip():
            return "missing_entirely"

        # B. Placeholder note in place of native script.
        if has_any_orig_text and is_placeholder_note(self.orig_text, native):
            return "placeholder_original"

        # For non-Sanskrit native scripts:
        if self.lang != "sanskrit":
            if native == "latin":
                return None if self.has_native_original else "missing_native_script"
            if not self.has_native_original:
                return "missing_native_script"
            return None

        # --- Sanskrit-specific consistency checks ---
        has_deva = self.native_script in detect_scripts(self.deva_field) or self.native_script in self.orig_scripts
        if not has_deva and self.has_iast:
            # IAST present but Devanagari missing; if the deva field is filled
            # with romanized text this is a malformed/mislabelled field.
            if self.deva_field and "latin" in detect_scripts(self.deva_field) and "deva" not in detect_scripts(self.deva_field):
                return "romanized_in_deva_field"
            return "iast_only_no_deva"
        if has_deva and not self.has_iast:
            return "deva_only_no_iast"
        if not has_deva and not self.has_iast:
            return "missing_entirely"
        return None  # complete: Devanagari + IAST


def is_complete(f: UnitFinding) -> bool:
    if f.lang == "sanskrit":
        has_deva = "deva" in detect_scripts(f.deva_field) or "deva" in f.orig_scripts
        return has_deva and f.has_iast
    if f.native_script == "latin":
        return f.has_native_original
    return f.has_native_original


def main() -> None:
    findings: list[UnitFinding] = []
    with open(INDEX, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            findings.append(UnitFinding(json.loads(line)))

    empty_dirs = find_empty_dirs()

    # Aggregate per work.
    per_work: dict[str, dict] = defaultdict(lambda: {
        "n": 0, "complete": 0, "problems": Counter(), "examples": defaultdict(list),
    })
    problem_examples: dict[str, list[str]] = defaultdict(list)

    for f in findings:
        w = per_work[f.work_id]
        w["n"] += 1
        if is_complete(f):
            w["complete"] += 1
        if f.problem:
            w["problems"][f.problem] += 1
            if len(w["examples"][f.problem]) < 4:
                w["examples"][f.problem].append(f.unit_id)
            if len(problem_examples[f.problem]) < 8:
                problem_examples[f.problem].append(f.unit_id)

    write_report(findings, per_work, problem_examples, empty_dirs)
    print(f"Audited {len(findings)} units across {len(per_work)} works.")
    print(f"Report written to {REPORT}")


PROBLEM_LABELS = {
    "missing_entirely": "No original text at all (no script, no IAST)",
    "placeholder_original": "Placeholder / source-language-basis note (no native script)",
    "missing_native_script": "Non-Sanskrit work missing its native source script",
    "romanized_in_deva_field": "Devanagari field holds romanized (IAST) text — malformed",
    "iast_only_no_deva": "IAST present but Devanagari missing",
    "deva_only_no_iast": "Devanagari present but IAST missing",
}


def pct(a: int, b: int) -> str:
    return f"{(100.0 * a / b):.0f}%" if b else "—"


def write_report(findings, per_work, problem_examples, empty_dirs) -> None:
    total = len(findings)
    total_complete = sum(w["complete"] for w in per_work.values())

    lines: list[str] = []
    lines.append("# Pratibha Corpus Audit — Original-Language Text\n")
    lines.append(
        "_Read-only audit of original-language coverage across "
        f"{total} canonical units in {len(per_work)} works "
        "(source: `data/canonical/index.jsonl`)._\n"
    )
    lines.append(
        f"**Headline:** {total_complete}/{total} units "
        f"({pct(total_complete, total)}) carry complete, language-appropriate "
        "original text (Devanagari+IAST for Sanskrit; native script for "
        "Greek/Chinese/Persian/Arabic/Tibetan/Japanese/German).\n"
    )

    # --- Coverage table ---
    lines.append("## Per-work coverage\n")
    lines.append(
        "| Work | Lang | Units | Complete | % | Top problem (count) |\n"
        "|------|------|------:|---------:|--:|---------------------|"
    )
    rows = sorted(
        per_work.items(),
        key=lambda kv: (kv[1]["complete"] / kv[1]["n"] if kv[1]["n"] else 1, -kv[1]["n"]),
    )
    for work, w in rows:
        lang = WORK_LANG.get(work, "unknown")
        top = w["problems"].most_common(1)
        top_str = f"{PROBLEM_LABELS.get(top[0][0], top[0][0])} ({top[0][1]})" if top else "—"
        lines.append(
            f"| `{work}` | {lang} | {w['n']} | {w['complete']} | "
            f"{pct(w['complete'], w['n'])} | {top_str} |"
        )

    # --- Worst offenders ---
    lines.append("\n## Worst offenders (by missing units)\n")
    offenders = sorted(
        per_work.items(),
        key=lambda kv: (kv[1]["n"] - kv[1]["complete"]),
        reverse=True,
    )
    lines.append("| Work | Lang | Units | Missing/incomplete | Dominant issue |")
    lines.append("|------|------|------:|-------------------:|----------------|")
    for work, w in offenders[:12]:
        miss = w["n"] - w["complete"]
        if miss == 0:
            continue
        top = w["problems"].most_common(1)
        top_str = f"{PROBLEM_LABELS.get(top[0][0], top[0][0])} ({top[0][1]})" if top else "—"
        lines.append(f"| `{work}` | {WORK_LANG.get(work,'?')} | {w['n']} | {miss} | {top_str} |")

    # --- Problem classes with representative unit_ids ---
    lines.append("\n## Problem classes & representative unit_ids\n")
    all_problems = Counter()
    for w in per_work.values():
        all_problems.update(w["problems"])
    for prob, count in all_problems.most_common():
        ex = ", ".join(f"`{u}`" for u in problem_examples.get(prob, [])[:6])
        lines.append(f"- **{PROBLEM_LABELS.get(prob, prob)}** — {count} units. e.g. {ex}")

    # --- Corpus hygiene ---
    lines.append("\n## Corpus hygiene — empty / duplicate work directories\n")
    lines.append(
        "These directories under `data/canonical/` contain zero unit files. "
        "Several are transliteration/name duplicates of populated works "
        "(e.g. `śiva_sūtra` vs `siva_sutra`, `vijñāna_bhairava` vs "
        "`vijnana_bhairava`, `chandogya_upanishad` vs `chāndogya_upaniṣad`).\n"
    )
    for d in empty_dirs:
        lines.append(f"- `{d}/`")

    # --- Recommendations ---
    lines.append("\n## Prioritized recommendations\n")
    lines.extend(RECOMMENDATIONS)

    with open(REPORT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


RECOMMENDATIONS = [
    "1. **Restore original text to the fully-empty Sanskrit works first — this is the "
    "largest, highest-value gap.** `vijnana_bhairava` (112 units), `yoga_spandakarika` "
    "(52), and `tantrasara` (19) have **no** Devanagari, IAST, or original layer on "
    "*any* unit — 183 Sanskrit units missing entirely. These are canonical Śaiva texts "
    "with readily available critical editions; ingest Devanagari + IAST in bulk.",
    "2. **Fix malformed Sanskrit `sanskrit_devanagari` fields that actually hold "
    "romanized IAST.** `nagarjuna_mulamadhyamakakarika` (9/9) and `heart_sutra` (2/3) "
    "store IAST in the Devanagari field, so they read as 'has original' but carry no "
    "Devanagari. Move the IAST to the IAST layer and supply real Devanagari.",
    "3. **Replace 'source-language basis' placeholders with real script.** "
    "`bhagavad_gita` (12), `shantideva_bodhicaryavatara` (8), `phaedo_plato` (12) and "
    "`tilopa_mahamudra` (3) ship notes like '*Source-language basis:* ...' instead of "
    "Devanagari/Greek/Tibetan. The Gītā and Phaedo are high-traffic anchor texts and "
    "should be prioritized.",
    "4. **Backfill Greek source script for Heraclitus.** `heraclitus_fragments` is the "
    "second-largest work (128 units) but only 11 carry Greek script; 117 have no "
    "original layer. Even Diels–Kranz fragment text for the attested fragments would "
    "close most of this gap. `know_yourself_ibn_arabi_balyani` (36 units) similarly has "
    "no Arabic original on any unit.",
    "5. **Resolve corpus-hygiene duplicate directories** (transliteration variants and "
    "empty stubs) so language-coverage tooling keys on one canonical work_id per text, "
    "and add a `provenance.source_language` field (currently null everywhere) so future "
    "audits need not infer language from work_id.",
]


if __name__ == "__main__":
    main()
