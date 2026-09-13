"""Remove chunk rows whose source YAML file no longer exists.

These accumulate when a collection is renamed. The ingest keys rows by
`metadata->>'source_file'`, so a rename leaves the old rows behind under unit ids
that are no longer in the corpus. `get_verse_by_id()` returns None for them, so
they are already invisible to readers — but they waste space and can surface as
dead neighbours in precomputed resonances.

Known cases at time of writing (11 files / 118 rows), all renames:
    rumi_mathnawi/..._mth_NNN.yml      -> rūmī_mathnawī_yi_maʿnawī/..._rum_NNN.yml
    tilopa_mahamudra/..._til_NNN.yml   -> tilopa_mahamudra/..._tilopa_mahamudra_NNN.yml
    pseudo_dionysius/..._pd_mt_01.yml  -> removed from the corpus

SAFETY
------
  * recomputes the orphan set at run time — never trusts a stale list;
  * refuses if any affected unit id also exists under a live source file;
  * writes every row it will delete (body, metadata AND embedding) to
    data/_orphan_chunks_backup.json first, so the delete is fully reversible;
  * deletes inside a transaction and rolls back unless the deleted row count
    matches the backup exactly;
  * dry run by default.

USAGE
    uv run python scripts/prune_orphan_chunks.py            # dry run, prints the plan
    uv run python scripts/prune_orphan_chunks.py --apply    # perform the delete

RESTORE
    The backup holds full rows including embeddings; re-INSERT them to undo.
"""

from __future__ import annotations

import argparse
import asyncio
import glob
import json
import os
import sys
from pathlib import Path

import asyncpg

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.config import settings  # noqa: E402

BACKUP = "data/_orphan_chunks_backup.json"


def disk_files() -> set[str]:
    return set(glob.glob("data/canonical/**/*.yml", recursive=True)) | set(
        glob.glob("data/canonical/**/*.yaml", recursive=True)
    )


async def main(apply: bool) -> None:
    conn = await asyncpg.connect(command_timeout=300, **settings.asyncpg_kwargs())
    try:
        await conn.execute("SET statement_timeout = 0")

        on_disk = disk_files()
        in_db = {
            r["sf"]
            for r in await conn.fetch("SELECT DISTINCT metadata->>'source_file' sf FROM chunks")
            if r["sf"]
        }
        orphans = sorted(in_db - on_disk)
        if not orphans:
            print("No orphaned source files. Nothing to do.")
            return

        print(f"source files: {len(in_db):,} in DB, {len(on_disk):,} on disk")
        print(f"ORPHANED: {len(orphans)}\n")

        # Guard: an orphan's unit id must not also live under a real source file,
        # otherwise we would be deleting one copy of a still-present unit.
        total = 0
        for sf in orphans:
            uid = await conn.fetchval(
                "SELECT metadata->>'_id' FROM chunks WHERE metadata->>'source_file'=$1 LIMIT 1", sf
            )
            shared = await conn.fetchval(
                "SELECT count(*) FROM chunks WHERE metadata->>'_id'=$1 AND metadata->>'source_file'<>$2",
                uid,
                sf,
            )
            if shared:
                raise SystemExit(f"REFUSING: unit {uid} also exists under another source_file")
            n = await conn.fetchval("SELECT count(*) FROM chunks WHERE metadata->>'source_file'=$1", sf)
            total += n
            print(f"  {sf}\n      unit={uid}  chunks={n}")
        print(f"\nrows to delete: {total}")

        rows = await conn.fetch(
            "SELECT body, embedding::text emb, metadata::text meta "
            "FROM chunks WHERE metadata->>'source_file' = ANY($1::text[])",
            orphans,
        )
        expected = len(rows)
        if expected != total:
            raise SystemExit(f"REFUSING: row count mismatch ({expected} vs {total})")

        if not apply:
            print(f"\nDRY RUN — would delete {expected} rows across {len(orphans)} files.")
            print("Re-run with --apply to execute (a full backup is written first).")
            return

        payload = [
            {"body": r["body"], "embedding": r["emb"], "metadata": json.loads(r["meta"])} for r in rows
        ]
        os.makedirs("data", exist_ok=True)
        with open(BACKUP, "w", encoding="utf-8") as fh:
            json.dump({"source_files": orphans, "rows": payload}, fh, ensure_ascii=False)
        print(f"\nbackup written: {BACKUP} ({os.path.getsize(BACKUP)/1048576:.1f} MB, {expected} rows)")

        async with conn.transaction():
            tag = await conn.execute(
                "DELETE FROM chunks WHERE metadata->>'source_file' = ANY($1::text[])", orphans
            )
            deleted = int(tag.split()[-1])
            if deleted != expected:
                raise SystemExit(f"ROLLING BACK: deleted {deleted} != expected {expected}")
            print(f"deleted {deleted} rows (matches backup exactly)")

        remaining = await conn.fetchval("SELECT count(*) FROM chunks")
        left = {
            r["sf"]
            for r in await conn.fetch("SELECT DISTINCT metadata->>'source_file' sf FROM chunks")
            if r["sf"]
        } - disk_files()
        print(f"\ncommitted. rows now {remaining:,}; orphans remaining: {len(left)}")
    finally:
        await conn.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="perform the delete (default: dry run)")
    asyncio.run(main(ap.parse_args().apply))
