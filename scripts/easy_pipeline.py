#!/usr/bin/env python3
"""
Run the simple end-to-end text pipeline.

Steps:
1) raw_texts_to_yaml
2) canonicalize_texts
3) validate_canonical
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def run(cmd: list[str], env: dict[str, str] | None = None) -> None:
    print(">", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=ROOT, env=env)


def main() -> int:
    ap = argparse.ArgumentParser(description="Run raw->yaml->canonical pipeline.")
    ap.add_argument("--skip-raw", action="store_true", help="Skip raw_texts_to_yaml step.")
    ap.add_argument("--ingest", action="store_true", help="Ingest canonical outputs into pgvector.")
    args = ap.parse_args()

    py = sys.executable

    if not args.skip_raw:
        run([py, "scripts/raw_texts_to_yaml.py"])

    run([py, "scripts/canonicalize_texts.py"])
    run([py, "scripts/validate_canonical.py"])

    if args.ingest:
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            print("Skipping ingest: OPENAI_API_KEY is not set.")
            return 0
        canonical_root = ROOT / "data" / "canonical"
        for work_dir in sorted([d for d in canonical_root.iterdir() if d.is_dir()]):
            run([py, "scripts/ingest_pgvector.py", "--dir", str(work_dir)])

    print("Pipeline complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

