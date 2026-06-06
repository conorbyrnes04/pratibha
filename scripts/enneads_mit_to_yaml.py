"""Parse the Internet Classics Archive plain-text Enneads into canonical YAML.

Source: https://classics.mit.edu/Plotinus/enneads.mb.txt  (MacKenna & Page).
Structure:
    THE FIRST ENNEAD
    First Tractate
    THE ANIMATE AND THE MAN.
    1. <section text, hard-wrapped, blank-line paragraphs>
    2. ...

Each numbered section becomes one translation-only canonical YAML unit ready
for `scripts/ingest_pgvector.py`. Hard line-wraps are de-wrapped into clean
paragraphs.

Usage:
  python scripts/enneads_mit_to_yaml.py --input data/raw_texts/plotinus_enneads_full.txt
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
ENNEAD_NUM = {"FIRST": "I", "SECOND": "II", "THIRD": "III", "FOURTH": "IV", "FIFTH": "V", "SIXTH": "VI"}
ORD_NUM = {
    "First": 1, "Second": 2, "Third": 3, "Fourth": 4, "Fifth": 5,
    "Sixth": 6, "Seventh": 7, "Eighth": 8, "Ninth": 9,
}

RE_ENNEAD = re.compile(r"^THE ([A-Z]+) ENNEAD\s*$")
RE_TRACTATE = re.compile(r"^(First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth) Tractate\s*$")
RE_SECTION = re.compile(r"^(\d+)\.\s+(.*)$")


def _dewrap(buf: list[str]) -> str:
    """Join hard-wrapped lines into paragraphs (blank line = paragraph break)."""
    text = "\n".join(buf)
    paras = re.split(r"\n\s*\n", text)
    cleaned = [" ".join(p.split()) for p in paras if p.strip()]
    return "\n\n".join(cleaned).strip()


def parse(text: str) -> list[dict]:
    units: list[dict] = []
    ennead = tractate = title = None
    expected = 1
    sec_num = None
    buf: list[str] = []
    expect_title = False

    def flush():
        nonlocal buf, sec_num
        if sec_num is not None and buf:
            body = _dewrap(buf)
            if body:
                units.append({"ennead": ennead, "tractate": tractate, "title": title, "section": sec_num, "body": body})
        buf = []
        sec_num = None

    for raw in text.split("\n"):
        line = raw.rstrip()
        stripped = line.strip()

        m = RE_ENNEAD.match(stripped)
        if m and m.group(1) in ENNEAD_NUM:
            flush()
            ennead = ENNEAD_NUM[m.group(1)]
            continue

        m = RE_TRACTATE.match(stripped)
        if m:
            flush()
            tractate = ORD_NUM[m.group(1)]
            title = None
            expected = 1
            expect_title = True
            continue

        if expect_title:
            if not stripped:
                continue
            title = re.sub(r"\s+", " ", stripped).strip().rstrip(".").title()
            expect_title = False
            continue

        m = RE_SECTION.match(stripped)
        # Accept a section marker only when it matches the expected next number,
        # so digit-led lines inside the prose don't trigger false splits.
        if m and int(m.group(1)) == expected and ennead and tractate:
            flush()
            sec_num = expected
            expected += 1
            buf = [m.group(2)]
            continue

        if sec_num is not None:
            buf.append(line)

    flush()
    return units


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--collection", default=COLLECTION)
    ap.add_argument("--out", default="")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    slug = canonical_slug(args.collection)
    out_dir = Path(args.out) if args.out else (ROOT / "data" / "canonical" / slug)
    units = parse(Path(args.input).read_text(encoding="utf-8", errors="replace"))
    if not units:
        print("No sections parsed.")
        return

    tractates = sorted({(u["ennead"], u["tractate"], u["title"]) for u in units}, key=lambda t: (list(ENNEAD_NUM.values()).index(t[0]), t[1]))
    print(f"Parsed {len(units)} sections across {len(tractates)} tractates.")
    for enn, tr, ttl in tractates:
        n = sum(1 for u in units if u["ennead"] == enn and u["tractate"] == tr)
        print(f"  Ennead {enn}.{tr}  {ttl!r}  ({n} sections)")

    if args.dry_run:
        print("\nDry-run: no files written.")
        return

    out_dir.mkdir(parents=True, exist_ok=True)
    for u in units:
        sutra_id = f"ENN_{u['ennead']}_{u['tractate']}_{u['section']:02d}"
        ttl = u["title"] or "Tractate"
        record = {
            "_id": f"{slug}.{sutra_id.lower()}",
            "collection": args.collection,
            "section": f"Ennead {u['ennead']}, Tractate {u['tractate']}, Section {u['section']}",
            "sutra_id": sutra_id,
            "title": f"Ennead {u['ennead']}.{u['tractate']}: {ttl} (\u00a7{u['section']})",
            "translation": u["body"],
            "themes": [],
            "editorial_maturity": "structural_draft",
            "editorial_score": 20,
            "source": "classics.mit.edu Enneads (MacKenna & Page)",
        }
        (out_dir / f"{slug}_{sutra_id.lower()}.yml").write_text(
            yaml.safe_dump(record, allow_unicode=True, sort_keys=False, width=100),
            encoding="utf-8",
        )
    print(f"\nWrote {len(units)} YAML units to {out_dir}")
    print(f"Next: python scripts/ingest_pgvector.py --dir {out_dir.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
