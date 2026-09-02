#!/usr/bin/env python3
"""Bake slim /verses JSON so a cold API can serve the Library before YAML loads."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.catalog import write_baked_catalog  # noqa: E402


def main() -> None:
    for maturity in (None, "strong_draft"):
        path = write_baked_catalog(maturity)
        size = path.stat().st_size
        print(f"wrote {path} ({size:,} bytes)")


if __name__ == "__main__":
    main()
