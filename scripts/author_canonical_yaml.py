"""Turn a raw spiritual-text file into canonical YAML units ready for ingestion.

The pipeline (`app.data_loader.normalize_unit` -> `scripts/ingest_pgvector.py`)
expects each unit as one YAML file with specific fields, and it *parses the
`commentary` field* for "Key Terms:" / "Cross-Tradition Resonances:" headings to
build the key_terms / resonances layers. It also DROPS template-filler
commentary and generic practices. So this tool:

  1. Splits the raw text into units (blank-line, regex, or LLM segmentation).
  2. Asks an LLM for STRUCTURED JSON per unit (easy to validate).
  3. Deterministically renders canonical YAML, assembling the commentary in the
     exact format the parser needs.
  4. Runs the unit through `normalize_unit` and rejects anything that would be
     dropped as a stub -- so every file is guaranteed "perfect input".

Usage:
  python scripts/author_canonical_yaml.py \
      --input data/raw_texts/tao_te_ching.txt \
      --collection "Tao Te Ching" \
      --id-prefix ttc \
      --split blank
  # then:  python scripts/ingest_pgvector.py --dir data/canonical/tao_te_ching
"""

import argparse
import asyncio
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.collection_aliases import canonical_slug  # noqa: E402
from app.data_loader import (  # noqa: E402
    GENERIC_PRACTICE_MARKERS,
    TEMPLATE_COMMENTARY_MARKERS,
    _commentary_is_authored,
    normalize_unit,
)
from app.llm import smart_chat  # noqa: E402

MATURITY_SCORE = {
    "publishable": 90,
    "strong_draft": 70,
    "needs_rewrite": 40,
    "structural_draft": 20,
}

SYSTEM_PROMPT = """You are a meticulous editor of contemplative and philosophical literature \
(Sanskrit, Daoist, Greek, Sufi, and related traditions). You convert ONE raw passage into a \
single structured study unit.

Return ONLY a JSON object (no markdown fences, no prose) with EXACTLY these keys:

{
  "title": "short evocative English title (3-8 words)",
  "section": "human label for where this sits, e.g. 'Chapter 12', 'Verse 4', 'Fragment 23', 'Yukti 1'",
  "original": "the source-language text if present in the input (Devanagari/Greek/Chinese/Arabic); else empty string",
  "transliteration": "scholarly romanization (IAST for Sanskrit) if applicable; else empty string",
  "translation": "a clean, faithful, readable English translation of the passage",
  "commentary": "ORIGINAL, substantive commentary of AT LEAST 3 sentences (>=220 characters). Explain \
the meaning, context, and what is at stake. Do NOT use generic openers; write real insight specific to THIS passage.",
  "key_terms": [{"term": "word", "definition": "one-clause meaning"}],
  "resonances": [{"citation": "Tradition/Text, ref", "resonance": "how it echoes this passage", "divergence": "how it differs (optional)"}],
  "practice": "ONE concrete, specific contemplative practice grounded in THIS passage (not a generic 'read slowly three times').",
  "themes": ["3-8 lowercase keywords"],
  "editorial_maturity": "one of: publishable | strong_draft | needs_rewrite | structural_draft"
}

Rules:
- Commentary must be genuine analysis of the given passage; never boilerplate.
- key_terms and resonances may be empty arrays if not applicable, but prefer 2-4 of each when meaningful.
- Keep the translation honest to the source; do not invent content not implied by the passage.
- Output valid JSON only."""


def _segment(text: str, mode: str) -> list[str]:
    text = text.replace("\r\n", "\n").strip()
    if mode == "blank":
        units = re.split(r"\n\s*\n", text)
    elif mode.startswith("regex:"):
        pattern = mode.split("regex:", 1)[1]
        # Split *before* each match so the delimiter (e.g. a verse number) stays
        # attached to its unit.
        units = re.split(rf"(?=(?:{pattern}))", text)
    else:  # "lines"
        units = text.split("\n")
    return [u.strip() for u in units if u.strip()]


def _extract_json(raw: str) -> dict:
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.MULTILINE).strip()
    start, end = raw.find("{"), raw.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("no JSON object in model output")
    return json.loads(raw[start : end + 1])


def _render_commentary(data: dict) -> str:
    parts = [str(data.get("commentary") or "").strip()]

    key_terms = [t for t in (data.get("key_terms") or []) if isinstance(t, dict) and t.get("term")]
    if key_terms:
        parts.append("Key Terms:\n\n" + "\n".join(
            f"**{str(t.get('term')).strip()}** — {str(t.get('definition') or '').strip()}"
            for t in key_terms
        ))

    resonances = [r for r in (data.get("resonances") or []) if isinstance(r, dict) and r.get("citation")]
    if resonances:
        lines = []
        for r in resonances:
            line = f"**{str(r.get('citation')).strip()}:** {str(r.get('resonance') or '').strip()}"
            divergence = str(r.get("divergence") or "").strip()
            if divergence:
                line += f" Divergence: {divergence}"
            lines.append(line)
        parts.append("Cross-Tradition Resonances:\n\n" + "\n".join(lines))

    return "\n\n".join(p for p in parts if p)


def _validate(data: dict) -> str | None:
    """Return a reason string if the unit is unusable, else None."""
    translation = str(data.get("translation") or "").strip()
    commentary = str(data.get("commentary") or "").strip()
    practice = str(data.get("practice") or "").strip()
    if not translation:
        return "translation is empty"
    lowered = commentary.lower()
    if any(lowered.startswith(m) for m in TEMPLATE_COMMENTARY_MARKERS):
        return "commentary uses a banned template opener"
    if practice and any(m in practice.lower() for m in GENERIC_PRACTICE_MARKERS):
        return "practice is generic boilerplate"
    # Mirror the pipeline's authored-commentary gate (avoid producing a stub).
    if not _commentary_is_authored(_render_commentary(data)):
        return "commentary is too thin (needs >=220 chars of real analysis or key terms/resonances)"
    return None


async def author_unit(raw_unit: str, collection: str, model: str) -> dict:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Tradition / collection: {collection}\n\nRaw passage:\n\"\"\"\n{raw_unit}\n\"\"\""},
    ]
    last_reason = ""
    for attempt in range(2):
        if attempt == 1 and last_reason:
            messages.append({
                "role": "user",
                "content": f"Your previous output was rejected: {last_reason}. Return corrected JSON only.",
            })
        text = await smart_chat(messages, primary_model=model, temperature=0.3)
        try:
            data = _extract_json(text)
        except Exception as e:
            last_reason = f"invalid JSON ({e})"
            continue
        reason = _validate(data)
        if reason is None:
            return data
        last_reason = reason
    raise ValueError(f"unit failed validation after retries: {last_reason}")


def to_canonical_yaml(data: dict, collection: str, sutra_id: str, source_path: str) -> dict:
    maturity = str(data.get("editorial_maturity") or "strong_draft").strip()
    if maturity not in MATURITY_SCORE:
        maturity = "strong_draft"
    return {
        "_id": f"{canonical_slug(collection)}.{sutra_id.lower()}",
        "collection": collection,
        "section": str(data.get("section") or "").strip(),
        "sutra_id": sutra_id,
        "title": str(data.get("title") or "").strip(),
        "sanskrit": str(data.get("original") or "").strip(),
        "transliteration": str(data.get("transliteration") or "").strip(),
        "translation": str(data.get("translation") or "").strip(),
        "commentary": _render_commentary(data),
        "abhyasa": str(data.get("practice") or "").strip(),
        "themes": [str(t).strip().lower() for t in (data.get("themes") or []) if str(t).strip()],
        "editorial_maturity": maturity,
        "editorial_score": MATURITY_SCORE[maturity],
        "source": Path(source_path).name,
    }


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="raw text file")
    ap.add_argument("--collection", required=True, help="collection name, e.g. 'Tao Te Ching'")
    ap.add_argument("--out", default="", help="output dir (default: data/canonical/<slug>)")
    ap.add_argument("--id-prefix", default="", help="sutra_id prefix (default: slug abbreviation)")
    ap.add_argument("--split", default="blank", help="blank | lines | regex:<pattern>")
    ap.add_argument("--model", default="", help="LLM model (default: app DEFAULT_MODEL)")
    ap.add_argument("--max-units", type=int, default=0, help="limit number of units (0 = all)")
    ap.add_argument("--start-index", type=int, default=1)
    ap.add_argument("--dry-run", action="store_true", help="author + validate but do not write files")
    args = ap.parse_args()

    from app.config import settings

    raw = Path(args.input).read_text(encoding="utf-8", errors="replace")
    units = _segment(raw, args.split)
    if args.max_units:
        units = units[: args.max_units]
    if not units:
        print("No units found after segmentation.")
        return

    slug = canonical_slug(args.collection)
    out_dir = Path(args.out) if args.out else (ROOT / "data" / "canonical" / slug)
    prefix = args.id_prefix or slug[:3]
    model = args.model or settings.DEFAULT_MODEL
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"{len(units)} units -> collection '{args.collection}' (slug={slug}) using model {model}")
    written, failed = 0, 0
    for offset, unit in enumerate(units):
        idx = args.start_index + offset
        sutra_id = f"{prefix.upper()}_{idx:03d}"
        try:
            data = await author_unit(unit, args.collection, model)
            record = to_canonical_yaml(data, args.collection, sutra_id, args.input)
            # Final proof: it must survive the pipeline's own normalization.
            norm = normalize_unit(dict(record), f"{out_dir}/{sutra_id}.yml")
            layers = [layer.get("kind") for layer in norm.get("pratibha_layers", [])]
            if not args.dry_run:
                path = out_dir / f"{slug}_{sutra_id.lower()}.yml"
                path.write_text(
                    yaml.safe_dump(record, allow_unicode=True, sort_keys=False, width=100),
                    encoding="utf-8",
                )
            written += 1
            print(f"  [{sutra_id}] OK  maturity={norm.get('editorial_maturity')} layers={layers}")
        except Exception as e:
            failed += 1
            print(f"  [{sutra_id}] FAILED: {e}")

    print(f"\nDone. {written} units authored, {failed} failed. Output: {out_dir}")
    if not args.dry_run and written:
        print(f"Next: python scripts/ingest_pgvector.py --dir {out_dir.relative_to(ROOT)}")


if __name__ == "__main__":
    asyncio.run(main())
