#!/usr/bin/env python3
"""Author Pratibha MD units for the Chāndogya Upaniṣad pilot.

Reads data/raw_texts/chandogya_pilot/manifest.json, calls the configured LLM
for each Müller passage, and writes:
  - data/pratibha_md/chandogya_upanishad_pilot.md
  - data/yaml/chandogya_upanishad/*.yml  (via chandogya_pratibha_md_to_yaml)

Usage:
  python scripts/chandogya_pilot_author.py
  python scripts/chandogya_pilot_author.py --max-units 2 --dry-run
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

MANIFEST = ROOT / "data" / "raw_texts" / "chandogya_pilot" / "manifest.json"
MD_OUT = ROOT / "data" / "pratibha_md" / "chandogya_upanishad_pilot.md"
YAML_OUT = ROOT / "data" / "yaml" / "chandogya_upanishad"

SYSTEM_PROMPT = """You are authoring one Pratibha corpus unit for the Chāndogya Upaniṣad.

Return ONLY a markdown fragment (no outer document title) with EXACTLY this structure:

## [Thematic title — a philosophical claim, not just section number]
**Source:** Chāndogya Upaniṣad, [section ref] (CHU_XXX; Max Müller trans., SBE vol. 1, 1879)

[Complete Müller passage body — dewrapped paragraphs, never truncated]

---

### Devanagari
[Sanskrit in Devanagari for key mantras/lines when standard; else cite IAST with note that Devanagari follows received Chāndogya text]

### IAST
[Full diacritics for Sanskrit terms; key verses in IAST]

### Pratibha Translation
[Readable present-tense philosophical English; preserve technical terms in brackets on first use]

### Pratibha Commentary
[MINIMUM 180 words. Open with explicit philosophical claim. Name counterintuitive move. No "In this passage..." openers. Situate in Upaniṣadic/Vedānta context. Point to existential application. Never paraphrase the translation.]

### Key Terms
[3-4 entries: **term (script/IAST)** — etymology -> tradition-specific meaning -> what default translation misses]

### Cross-Tradition Resonances
[2-4 entries with format:
**[Tradition/Author, Text, Passage]:** structural homology.
*Divergence:* where parallel breaks.]

### Practice (Abhyasa)
[One executable second-person instruction derived from THIS passage only]

Rules:
- Commentary must be original analysis, not paraphrase of translation.
- Resonances must cite specific passages from corpus traditions where possible: Mandukya, Astavakra, Bhagavad Gita, Plotinus VI.9, Tao Te Ching, Milarepa, Epictetus, Dōgen, Pratyabhijñā.
- For *tat tvam asi* units: treat identity as pedagogical reversal, not slogan.
- Keep the anchor passage complete and faithful to the input Müller text (OCR quirks may be silently corrected for readability)."""


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
    section = entry["section"]
    title = entry["title"]
    body = Path(ROOT / entry["file"]).read_text(encoding="utf-8").strip()

    user = f"""{section}, {title}
Sutra ID: {entry['sutra_id']}
Anchor: {entry['anchor_source']}

Müller passage (correct obvious OCR spacing errors only):
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
    if args.max_units:
        manifest = manifest[: args.max_units]

    model = args.model or settings.DEFAULT_MODEL
    print(f"Authoring {len(manifest)} units with model {model}")

    parts = [
        "# Pratibha — Chāndogya Upaniṣad (Pilot)",
        "**Corpus entry:** Śukla Yajurveda Upaniṣad / Vedānta",
        "**Anchor:** F. Max Müller, *The Upanishads*, Part 1 (SBE vol. 1, 1879; public domain)",
        "**Pilot:** Om/udgitha, Sāṇḍilya-vidyā, Uddālaka–Śvetaketu (*tat tvam asi*), Prajāpati–Indra",
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
            str(ROOT / "scripts" / "chandogya_pratibha_md_to_yaml.py"),
            str(MD_OUT),
            str(YAML_OUT),
        ],
        check=True,
    )

    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "chandogya_promote_canonical.py")],
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
