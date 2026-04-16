#!/usr/bin/env python3
"""
Start backend and web dev servers in one command.
"""
from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    ap = argparse.ArgumentParser(description="Start FastAPI + Next.js dev servers.")
    ap.add_argument("--backend-port", type=int, default=8000)
    ap.add_argument("--web-port", type=int, default=3000)
    ap.add_argument("--canonical-only", default="true", choices=["true", "false"])
    args = ap.parse_args()

    env = os.environ.copy()
    env["CANONICAL_ONLY"] = args.canonical_only
    env["NEXT_PUBLIC_API_BASE"] = f"http://localhost:{args.backend_port}"
    env["PORT"] = str(args.web_port)

    py = sys.executable
    backend_cmd = [py, "-m", "uvicorn", "app.main:app", "--reload", "--port", str(args.backend_port)]
    web_cmd = ["npm", "run", "dev", "--", "-p", str(args.web_port)]

    print("Starting backend:", " ".join(backend_cmd))
    backend = subprocess.Popen(backend_cmd, cwd=ROOT, env=env)

    print("Starting web:", " ".join(web_cmd))
    web = subprocess.Popen(web_cmd, cwd=ROOT / "web", env=env)

    procs = [backend, web]

    def shutdown(*_: object) -> None:
        for p in procs:
            if p.poll() is None:
                p.terminate()
        for p in procs:
            try:
                p.wait(timeout=8)
            except Exception:
                if p.poll() is None:
                    p.kill()

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        while True:
            if backend.poll() is not None or web.poll() is not None:
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        shutdown()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

