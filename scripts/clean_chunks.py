"""Clean chunk bodies so retrieved sources read as pure teaching text.

What it does (metadata is untouched; embeddings are left as-is):
  - Strips the machine header baked into bodies, e.g.
        "[tao_te_ching | TYING KNOTS | commentary]\\n\\n<text>"
    The web UI and LLM attribution already come from metadata, so this header
    is redundant slug-noise.
  - Normalizes whitespace (trailing spaces, runs of blank lines).
  - DELETES verbatim "slop" commentary -- the bulk auto-enrichment filler the
    app's own `_commentary_is_authored` rejects (e.g. "The emphasis turns
    inward...") -- because it is fake insight that pollutes retrieval.

Short translations and the structured "Key Terms / Cross-Tradition Resonances"
tails are preserved (they carry real semantic value).

NOTE: bodies were embedded with the header present. Since semantic search is
currently disabled (no embedding key), changing the body text has no retrieval
downside today; re-run ingestion to re-embed clean bodies once a key is set.

Usage:
  python scripts/clean_chunks.py            # dry-run, prints a plan
  python scripts/clean_chunks.py --apply     # write changes
"""

import argparse
import asyncio
import re
import sys
from collections import Counter
from pathlib import Path

import asyncpg

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.config import settings  # noqa: E402
from app.data_loader import (  # noqa: E402
    GENERIC_PRACTICE_MARKERS,
    TEMPLATE_COMMENTARY_MARKERS,
)

# Only strip a leading bracket line that looks like our header (contains a
# pipe), so a passage that legitimately starts with "[" is never touched.
_HEADER_RE = re.compile(r"^\[[^\n\]]*\|[^\n\]]*\]\s*\n+")


def strip_header(body: str) -> str:
    return _HEADER_RE.sub("", body or "", count=1)


def normalize_ws(text: str) -> str:
    text = (text or "").replace("\r\n", "\n").replace("\r", "\n")
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def is_slop(body: str) -> bool:
    """Verbatim template filler that should never be a retrievable source."""
    text = body.strip()
    if not text:
        return True
    lowered = text.lower()
    if any(lowered.startswith(marker) for marker in TEMPLATE_COMMENTARY_MARKERS):
        return True
    if any(marker in lowered for marker in GENERIC_PRACTICE_MARKERS):
        return True
    return False


async def main(apply: bool) -> None:
    conn = await asyncpg.connect(
        user=settings.PG_USER,
        password=settings.PG_PASSWORD,
        database=settings.PG_DB,
        host=settings.PG_HOST,
        port=settings.PG_PORT,
    )
    rows = await conn.fetch("SELECT id, body, metadata->>'layer_kind' AS kind FROM chunks ORDER BY id")
    print(f"Loaded {len(rows)} chunks.")

    to_delete: list[int] = []
    to_update: list[tuple[int, str]] = []
    delete_reasons: Counter = Counter()
    delete_samples: list[str] = []
    update_samples: list[tuple[str, str]] = []

    for row in rows:
        original = row["body"] or ""
        kind = (row["kind"] or "").strip()
        cleaned = normalize_ws(strip_header(original))

        if not cleaned:
            to_delete.append(row["id"])
            delete_reasons["empty_after_strip"] += 1
            continue
        # Only commentary/appendix are subject to slop deletion; never drop a
        # translation or original-text chunk.
        if kind in ("commentary", "appendix") and is_slop(cleaned):
            to_delete.append(row["id"])
            delete_reasons[f"slop_{kind}"] += 1
            if len(delete_samples) < 5:
                delete_samples.append(cleaned[:160])
            continue
        if cleaned != original:
            to_update.append((row["id"], cleaned))
            if len(update_samples) < 3:
                update_samples.append((original[:160], cleaned[:160]))

    print(f"\nPlanned: delete {len(to_delete)} chunks, rewrite {len(to_update)} bodies.")
    print("Delete reasons:")
    for reason, count in delete_reasons.most_common():
        print(f"  {count:6d}  {reason}")

    if delete_samples:
        print("\nSample chunks to DELETE:")
        for s in delete_samples:
            print(f"  - {s!r}")
    if update_samples:
        print("\nSample header strips (before -> after):")
        for before, after in update_samples:
            print(f"  - {before!r}\n    -> {after!r}")

    if not apply:
        print("\nDry-run only. Re-run with --apply to write these changes.")
        await conn.close()
        return

    async with conn.transaction():
        if to_delete:
            await conn.execute("DELETE FROM chunks WHERE id = ANY($1::int[])", to_delete)
        for chunk_id, body in to_update:
            await conn.execute("UPDATE chunks SET body = $1 WHERE id = $2", body, chunk_id)

    remaining = await conn.fetchval("SELECT count(*) FROM chunks")
    print(f"\nDeleted {len(to_delete)}, rewrote {len(to_update)}. Chunks remaining: {remaining}.")
    await conn.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write changes (default is dry-run)")
    args = ap.parse_args()
    asyncio.run(main(apply=args.apply))
