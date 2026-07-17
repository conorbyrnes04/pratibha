#!/usr/bin/env python3
"""Author Pratibha MD units for the Heraclitus fragments pilot.

Reads data/raw_texts/heraclitus_pilot/manifest.json, calls the configured LLM
for each Patrick (1889) anchor passage, and writes:
  - data/pratibha_md/heraclitus_fragments_pilot.md
  - data/yaml/fragments/fragment_XXX.yml  (via heraclitus_pratibha_md_to_yaml)

Usage:
  python scripts/heraclitus_pilot_extract.py
  python scripts/heraclitus_pilot_author.py
  python scripts/heraclitus_pilot_author.py --max-units 2 --dry-run
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.llm import smart_chat  # noqa: E402

MANIFEST = ROOT / "data" / "raw_texts" / "heraclitus_pilot" / "manifest.json"
MD_OUT = ROOT / "data" / "pratibha_md" / "heraclitus_fragments_pilot.md"
YAML_OUT = ROOT / "data" / "yaml" / "fragments"

SYSTEM_PROMPT = """You are authoring one Pratibha corpus unit for a Heraclitus fragment.

Return ONLY a markdown fragment (no outer document title) with EXACTLY this structure:

## [Thematic title — a philosophical claim, not "Fragment 12"]
**Source:** Heraclitus, *Fragments* (HFR_P###; DK B##; Patrick 1889 / Bywater Greek)

[Complete Patrick anchor passage — never truncated]

---

### Original
[Greek script for the key line when standard forms are known, e.g. πάντα ῥεῖ; else label source-language basis and give transliterated Greek terms]

### IAST
[Transliterated Greek with diacritics/macrons where standard; key terms in Greek letters with transliteration]

### Pratibha Translation
[Readable present-tense philosophical English; preserve Logos, physis, harmoniē, psychē on first use with Greek in brackets]

### Pratibha Commentary
[MINIMUM 180 words. Open with explicit philosophical claim. Name counterintuitive move. No "In this passage..." openers. Situate in pre-Socratic / Ephesian context. Point to existential application. Never paraphrase the translation.]

### Key Terms
[2-4 entries: **term (Greek)** — etymology -> Heraclitean meaning in this fragment -> what default translation misses]

### Cross-Tradition Resonances
[2-4 entries with format:
**[Tradition/Author, Text, Passage]:** structural homology.
*Divergence:* where parallel breaks.]

### Practice (Abhyasa)
[One executable second-person instruction derived from THIS fragment only]

Rules:
- Commentary must be original analysis, not paraphrase of translation.
- Resonances must cite specific passages; rotate beyond overused BGV 2.47 / Enchiridion 1.
- Prefer resonances from: Dōgen Shōbōgenzō, Plotinus Enneads, Tao Te Ching, Zhuangzi, Chandogya Upanishad, Epictetus.
- Do NOT copy Patrick verbatim in Pratibha Translation — modernize while anchoring to the input text.
- Patrick uses "Reason" for Logos — use Logos in Pratibha layers."""


def _clean_model_md(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:markdown|md)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    if not text.startswith("## "):
        m = re.search(r"(?m)^##\s+", text)
        if m:
            text = text[m.start() :]
    return text.strip()


async def author_unit(entry: dict, model: str) -> str:
    body = Path(ROOT / entry["file"]).read_text(encoding="utf-8").strip()
    dk = entry.get("dk_ref", "")
    sid = entry["sutra_id"]

    user = f"""{entry['title']}
Sutra ID: {sid}
DK reference: {dk}
Anchor: {entry['anchor_source']}

Patrick (1889) passage:
\"\"\"
{body}
\"\"\"
"""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user},
    ]
    raw = await smart_chat(messages, primary_model=model, temperature=0.35)
    return _clean_model_md(raw)


async def main_async(args: argparse.Namespace) -> int:
    from app.config import settings

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest = [e for e in manifest if not e.get("skip_author")]
    if args.max_units:
        manifest = manifest[: args.max_units]

    model = args.model or settings.DEFAULT_MODEL
    print(f"Authoring {len(manifest)} units with model {model}")

    parts = [
        "# Pratibha — Heraclitus Fragments (Pilot)",
        "**Corpus entry:** Greek Pre-Socratic / Ephesus / c. 500 BCE",
        "**Anchor:** George T.W. Patrick, *The Fragments of Heraclitus* (1889, Bywater Greek; Internet Archive, public domain)",
        "**Pilot:** Logos, fire, river, war, harmony, soul — curated Pratibha layers",
        "",
        "---",
        "",
    ]

    for i, entry in enumerate(manifest, 1):
        sid = entry["sutra_id"]
        print(f"  [{i}/{len(manifest)}] {sid} ...", flush=True)
        try:
            unit_md = await author_unit(entry, model)
            parts.append(unit_md)
            parts.append("\n---\n")
        except Exception as e:
            print(f"    FAILED {sid}: {e}", file=sys.stderr)

    md_text = "\n".join(parts).strip() + "\n"
    if args.dry_run:
        print(f"\nDry-run: would write {len(manifest)} units to {MD_OUT.relative_to(ROOT)}")
        return 0

    MD_OUT.parent.mkdir(parents=True, exist_ok=True)
    MD_OUT.write_text(md_text, encoding="utf-8")
    print(f"\nWrote MD -> {MD_OUT.relative_to(ROOT)}")

    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "heraclitus_pratibha_md_to_yaml.py"),
            str(MD_OUT),
            str(YAML_OUT),
        ],
        check=True,
    )
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="")
    ap.add_argument("--max-units", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    raise SystemExit(main())
