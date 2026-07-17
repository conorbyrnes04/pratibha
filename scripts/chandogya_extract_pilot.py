#!/usr/bin/env python3
"""Extract pilot Chāndogya Upaniṣad passages from Müller SBE vol. 1 (1879).

Priority passages per PD manifest:
  - tat tvam asi (VI.8–16)
  - Sāṇḍilya-vidyā (III.14)
  - Prajāpati's instruction to Indra (VIII.7–12)

Usage:
  python scripts/chandogya_extract_pilot.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "raw_texts" / "pd" / "indian" / "chandogya_upanishad_muller_sbe01.txt"
OUT_DIR = ROOT / "data" / "raw_texts" / "chandogya_pilot"

PILOT_PASSAGES: list[dict[str, str]] = [
    {
        "sutra_id": "CHU_I_01",
        "slug": "i_01",
        "title": "Meditation on Om as Udgitha",
        "section": "Chāndogya Upaniṣad I.1",
        "start": "Let  a  man  meditate  on  the  syllable",
        "end": "full account  of  the  syllable  Om",
    },
    {
        "sutra_id": "CHU_III_14",
        "slug": "iii_14",
        "title": "Sāṇḍilya-Vidyā — All This Is Brahman",
        "section": "Chāndogya Upaniṣad III.14",
        "start": "All  this  is  Brahman",
        "end": "thus  said  SincTilyB",
    },
    {
        "sutra_id": "CHU_VI_01",
        "slug": "vi_01",
        "title": "Instruction Beyond the Vedas",
        "section": "Chāndogya Upaniṣad VI.1",
        "start": "There  lived  once  .Svetaketu",
        "end": "Be  it  so,'\n said  the  father",
    },
    {
        "sutra_id": "CHU_VI_02",
        "slug": "vi_02",
        "title": "Sat Alone — One Without a Second",
        "section": "Chāndogya Upaniṣad VI.2",
        "start": "In  the  beginning,'  my  dear,  'there  was  that",
        "end": "from  water  alone  is  eatable",
    },
    {
        "sutra_id": "CHU_VI_08",
        "slug": "vi_08",
        "title": "Thou Art That — At Death the Self Remains",
        "section": "Chāndogya Upaniṣad VI.8",
        "start": "When  a  man  departs  from  hence,  his  speech",
        "end": "thou,  O  ^Svetaketu,  art  it'",
        "context_before": "Seventh  Khanda",
    },
    {
        "sutra_id": "CHU_VI_09",
        "slug": "vi_09",
        "title": "Bees and Honey — Creatures Merged in the True",
        "section": "Chāndogya Upaniṣad VI.9",
        "start": "make  honey  by  col",
        "end": "thou,  O  .Svetaketu,  art  it.'",
        "context_before": "Ninth  Kh",
    },
    {
        "sutra_id": "CHU_VI_10",
        "slug": "vi_10",
        "title": "Rivers Returning to the Sea",
        "section": "Chāndogya Upaniṣad VI.10",
        "start": "These  rivers,  my  son,  run",
        "end": "thou,  O  .Svetaketu,  art  it.'",
    },
    {
        "sutra_id": "CHU_VI_11",
        "slug": "vi_11",
        "title": "The Tree and the Living Self",
        "section": "Chāndogya Upaniṣad VI.11",
        "start": "Mf  some  one  were  to  strike  at  the  root  of  this",
        "end": "thou,  5vetaketu,  art  iC",
    },
    {
        "sutra_id": "CHU_VI_16",
        "slug": "vi_16",
        "title": "The Heated Hatchet — Knowledge That Does Not Return",
        "section": "Chāndogya Upaniṣad VI.16",
        "start": "they  bring  a  man  hither  whom  they  have  taken  by  the  hand",
        "end": "yea,  he  understood  it",
    },
    {
        "sutra_id": "CHU_VIII_07",
        "slug": "viii_07",
        "title": "Prajāpati's Search for the Self",
        "section": "Chāndogya Upaniṣad VIII.7",
        "start": "Praglpati  said :  *  The  Self  which  is  free  from  sin",
        "end": "He  himself  indeed  is  seen  in  all  these",
    },
    {
        "sutra_id": "CHU_VIII_11",
        "slug": "viii_11",
        "title": "Dreamless Sleep as the Self",
        "section": "Chāndogya Upaniṣad VIII.11",
        "start": "When  a  man  being  asleep,  reposing,  and  at  perfect  rest",
        "end": "I  see  no  good  in  this",
    },
    {
        "sutra_id": "CHU_VIII_12",
        "slug": "viii_12",
        "title": "The Mortal Body and the Immortal Self",
        "section": "Chāndogya Upaniṣad VIII.12",
        "start": "Maghavat,  this  body  is  mortal",
        "end": "thus  said  Pra^dpati",
    },
]


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("\u2019", "'").replace("\u2018", "'")).strip()


def _find(text: str, needle: str, *, after: int = 0, ctx: str = "") -> int:
    n = _norm(needle)
    if ctx:
        ctx_pos = text.lower().find(ctx.lower(), after)
        if ctx_pos != -1:
            after = ctx_pos
    chunk = text[after:]
    # Try exact first
    pos = chunk.find(needle)
    if pos != -1:
        return after + pos
    # Fuzzy: collapse whitespace in sliding windows
    target = re.sub(r"\s+", "", n.lower())
    collapsed = re.sub(r"\s+", "", chunk.lower())
    cpos = collapsed.find(target)
    if cpos == -1:
        return -1
    # Map back to approximate position in original
    idx = 0
    orig_idx = 0
    while idx < cpos and orig_idx < len(chunk):
        if not chunk[orig_idx].isspace():
            idx += 1
        orig_idx += 1
    return after + orig_idx


def _clean_ocr(body: str) -> str:
    body = body.replace("\r\n", "\n").replace("\r", "\n")
    body = re.sub(r"\n{3,}", "\n\n", body)
    # Drop page headers / footers common in Google scan
    body = re.sub(r"(?m)^\d+\s+[A-Z][A-Z\s\-]+\.\s*$", "", body)
    body = re.sub(r"(?m)^\d+\s+[a-zA-Z].{0,40}UPANISHAD\.?\s*$", "", body)
    return body.strip() + "\n"


def extract_one(text: str, entry: dict[str, str]) -> str:
    after = 0
    ctx = entry.get("context_before", "")
    start = _find(text, entry["start"], ctx=ctx)
    if start == -1:
        raise ValueError(f"start anchor not found: {entry['start']!r}")
    end = _find(text, entry["end"], after=start + len(entry["start"]))
    if end == -1:
        raise ValueError(f"end anchor not found: {entry['end']!r}")
    end += len(entry["end"])
    return _clean_ocr(text[start:end])


def main() -> int:
    if not SOURCE.is_file():
        print(f"Missing source: {SOURCE}", file=sys.stderr)
        return 1

    text = SOURCE.read_text(encoding="utf-8", errors="replace")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    manifest: list[dict] = []
    ok = 0
    for entry in PILOT_PASSAGES:
        sid = entry["sutra_id"]
        try:
            body = extract_one(text, entry)
            rel = f"data/raw_texts/chandogya_pilot/{entry['slug']}.txt"
            out_path = ROOT / rel
            out_path.write_text(body, encoding="utf-8")
            manifest.append(
                {
                    "sutra_id": sid,
                    "slug": entry["slug"],
                    "title": entry["title"],
                    "section": entry["section"],
                    "file": rel,
                    "anchor_source": "Max Müller, Chāndogya Upaniṣad (SBE vol. 1, 1879, public domain)",
                    "chars": len(body),
                }
            )
            ok += 1
            print(f"  OK  {sid}  ({len(body)} chars)")
        except Exception as e:
            print(f"  FAIL {sid}: {e}", file=sys.stderr)

    manifest_path = OUT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nExtracted {ok}/{len(PILOT_PASSAGES)} -> {OUT_DIR.relative_to(ROOT)}")
    return 0 if ok == len(PILOT_PASSAGES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
