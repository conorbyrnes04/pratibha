"""Convert a section-delimited Plotinus tractate text file into canonical YAML.

Input format: a plain-text file whose passages are delimited by lines like
"## Section 1", "## Section 2", ... (as scraped from sacred-texts.com).
Each section becomes one translation-only canonical YAML unit, ready for
`scripts/ingest_pgvector.py`.

Usage:
  python scripts/plotinus_to_yaml.py \
      --input data/raw_texts/plotinus_enn_I_1.txt \
      --ennead I --tractate 1 \
      --tractate-title "The Animate and the Man"
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.collection_aliases import canonical_slug  # noqa: E402

COLLECTION = "Plotinus Enneads"


def parse_sections(text: str) -> list[tuple[str, str]]:
    text = text.replace("\r\n", "\n").strip()
    parts = re.split(r"(?m)^##\s*Section\s+(\d+)\s*$", text)
    # re.split keeps captured group: [pre, num, body, num, body, ...]
    out: list[tuple[str, str]] = []
    for i in range(1, len(parts), 2):
        num = parts[i].strip()
        body = parts[i + 1].strip()
        if body:
            out.append((num, body))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--ennead", required=True, help="e.g. I, II, ... or 1")
    ap.add_argument("--tractate", required=True, help="tractate number, e.g. 1")
    ap.add_argument("--tractate-title", default="")
    ap.add_argument("--collection", default=COLLECTION)
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    slug = canonical_slug(args.collection)
    out_dir = Path(args.out) if args.out else (ROOT / "data" / "canonical" / slug)
    out_dir.mkdir(parents=True, exist_ok=True)

    sections = parse_sections(Path(args.input).read_text(encoding="utf-8", errors="replace"))
    if not sections:
        print("No sections found (expected '## Section N' delimiters).")
        return

    title_suffix = f": {args.tractate_title}" if args.tractate_title else ""
    written = 0
    for num, body in sections:
        sutra_id = f"ENN_{args.ennead}_{args.tractate}_{int(num):02d}"
        record = {
            "_id": f"{slug}.{sutra_id.lower()}",
            "collection": args.collection,
            "section": f"Ennead {args.ennead}, Tractate {args.tractate}, Section {num}",
            "sutra_id": sutra_id,
            "title": f"Ennead {args.ennead}.{args.tractate}{title_suffix} (\u00a7{num})",
            "translation": body,
            "themes": [],
            "editorial_maturity": "structural_draft",
            "editorial_score": 20,
            "source": f"sacred-texts.com Enneads (MacKenna & Page) {Path(args.input).name}",
        }
        path = out_dir / f"{slug}_{sutra_id.lower()}.yml"
        path.write_text(
            yaml.safe_dump(record, allow_unicode=True, sort_keys=False, width=100),
            encoding="utf-8",
        )
        written += 1

    print(f"Wrote {written} YAML units to {out_dir}")
    print(f"Next: python scripts/ingest_pgvector.py --dir {out_dir.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
