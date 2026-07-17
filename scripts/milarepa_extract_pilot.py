#!/usr/bin/env python3
"""Extract pilot Milarepa song passages from Evans-Wentz (1928) PD text.

Priority songs from Chapter X (Meditation in Solitude). Note: the 1928 edition
summarizes but does not fully include the Snow Song, Six Bardos, or Lingwa
demoness chapters — those appear only as references in Chapter XI.

Usage:
  python scripts/milarepa_extract_pilot.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "raw_texts" / "pd" / "tibetan" / "milarepa_evans_wentz_1928.txt"
OUT_DIR = ROOT / "data" / "raw_texts" / "milarepa_pilot"

# Each entry: start/end plain-text anchors within the Evans-Wentz OCR text.
PILOT_SONGS: list[dict[str, str]] = [
    {
        "sutra_id": "MIL_SORROW_001",
        "slug": "sorrow_001",
        "title": "The Sorrowful Song to the Aunt",
        "chapter": "X",
        "start": "At the Feet of my Kind Father Marpa I bow down!",
        "end": "cool down Thy suppliant's wrath!",
    },
    {
        "sutra_id": "MIL_ZEAL_002",
        "slug": "zeal_002",
        "title": "Song on Yogic Zeal (The Plough of the Mind)",
        "chapter": "X",
        "start": "Grant that this mendicant may cling successfully to solitude.",
        "end": "Untroubled be by obstacles and interruptions on the Path",
        "context_before": "sang this song to impress the true interpretation",
    },
    {
        "sutra_id": "MIL_WISDOM_003",
        "slug": "wisdom_003",
        "title": "Song of Yogic Wisdom (By Compassion I Subdue the Demons)",
        "chapter": "X",
        "start": "Q Lord, my Guru, by Thy Grace do I the life ascetic live",
        "end": "pass my life in solitude successfully",
        "context_before": "sang to her the following song",
    },
    {
        "sutra_id": "MIL_REPROOF_004",
        "slug": "reproof_004",
        "title": "Song of Self-Reproof",
        "chapter": "X",
        "start": "Q Dorje-Chang Thyself, in Marpa's form!",
        "end": "the Poisons Five, of Ignorance, will subdue thee",
        "context_before": "song of self-reproof",
    },
    {
        "sutra_id": "MIL_COMFORTS_005",
        "slug": "comforts_005",
        "title": "Song of the Five Comforts",
        "chapter": "X",
        "start": "Tord! Gracious Marpa! I bow down at Thy Feet !",
        "end": "Therefore shall I into the State Quiescent of Samadhi",
        "context_before": "song about my Five Comforts",
    },
    {
        "sutra_id": "MIL_SISTER_006",
        "slug": "sister_006",
        "title": "Song to Peta (The Bodhi Mind in the Skeleton)",
        "chapter": "X",
        "start": "Obeisance to my Lords, the Gurus!",
        "end": "But also give thyself to penances, for religion's sake",
        "context_before": "this song to my sister",
    },
    {
        "sutra_id": "MIL_RACE_007",
        "slug": "race_007",
        "title": "Song of a Yogi's Race (The Horse of Mind)",
        "chapter": "X",
        "start": "T bow down at the Feet of my Gracious Father Marpa!",
        "end": "Worldly Happiness I covet not",
        "context_before": "hymn of a Yogi's Race",
    },
    {
        "sutra_id": "MIL_DEMON_008",
        "slug": "demon_008",
        "title": "Song Recalling Persecution (The Demoness in the Body of an Aunt)",
        "chapter": "X",
        "start": "Q Kind and Gracious Father, compassionate to all,",
        "end": "Tis better to go early, while there is still the time",
        "context_before": "song recalling the cruelties",
    },
]


def _clean_ocr(body: str) -> str:
    body = body.replace("\r\n", "\n").replace("\r", "\n")
    body = re.sub(r"\n{3,}", "\n\n", body)
    # Drop inline page headers like "CHAP. x] SONG OF ..."
    body = re.sub(r"(?m)^CHAP\.[^\n]+\n", "", body)
    body = re.sub(r"(?m)^\d+\s+MEDITATION IN SOLITUDE[^\n]*\n", "", body)
    body = re.sub(r"(?m)^\d+\s+THE [^\n]+\n", "", body)
    # Normalize OCR quote clutter at line starts
    body = re.sub(r"(?m)^['\u2018\u2019\"`\u00b4]+\*?", "'", body)
    body = re.sub(r"(?m)^\*\*", "'", body)
    return body.strip() + "\n"


def _norm(s: str) -> str:
    return (
        s.replace("\u2019", "'")
        .replace("\u2018", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\u00b4", "'")
    )


def _find_start(text: str, start: str, context_before: str = "") -> int:
    ntext = _norm(text)
    nstart = _norm(start)
    if context_before:
        ctx = _norm(context_before).lower()
        pos = 0
        while True:
            idx = ntext.lower().find(ctx, pos)
            if idx < 0:
                break
            sub = ntext[idx:]
            rel = sub.find(nstart)
            if rel >= 0:
                return idx + rel
            pos = idx + len(ctx)
    idx = ntext.find(nstart)
    if idx < 0:
        raise ValueError(f"start marker not found: {start[:60]}...")
    return idx


def _extract(text: str, start: str, end: str, context_before: str = "") -> str:
    start_idx = _find_start(text, start, context_before)
    chunk = text[start_idx:]
    nchunk = re.sub(r"\s+", " ", _norm(chunk))
    nend = re.sub(r"\s+", " ", _norm(end))
    end_idx = nchunk.find(nend)
    if end_idx < 0:
        raise ValueError(f"end marker not found after start: {end[:60]}...")
    # Map normalized offset back to original chunk by scanning.
    norm_pos = 0
    orig_end = len(chunk)
    target = end_idx + len(nend)
    buf = ""
    for i, ch in enumerate(chunk):
        buf = re.sub(r"\s+", " ", _norm(buf + ch))
        if len(buf) >= target:
            orig_end = i + 1
            break
    return _clean_ocr(chunk[:orig_end])


def build_manifest() -> list[dict]:
    if not SOURCE.exists():
        raise FileNotFoundError(
            f"Missing PD source: {SOURCE}\n"
            "Download from Internet Archive dli.ministry.06735 (DjVuTXT)."
        )

    text = SOURCE.read_text(encoding="utf-8", errors="replace")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest: list[dict] = []

    for entry in PILOT_SONGS:
        body = _extract(
            text,
            entry["start"],
            entry["end"],
            entry.get("context_before", ""),
        )
        fname = f"mil_{entry['slug']}.txt"
        fpath = OUT_DIR / fname
        fpath.write_text(body, encoding="utf-8")
        manifest.append(
            {
                "sutra_id": entry["sutra_id"],
                "slug": entry["slug"],
                "title": entry["title"],
                "chapter": entry["chapter"],
                "file": str(fpath.relative_to(ROOT)),
                "anchor_source": "W.Y. Evans-Wentz (ed.), Tibet's Great Yogi Milarepa (1928); Kazi Dawa-Samdup translation",
            }
        )
        print(f"  {entry['sutra_id']} -> {fpath.relative_to(ROOT)} ({len(body)} chars)")

    (OUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    print(f"Extracting from {SOURCE.relative_to(ROOT)}")
    manifest = build_manifest()
    print(f"Wrote {len(manifest)} passages -> {OUT_DIR.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
