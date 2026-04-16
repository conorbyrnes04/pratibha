#!/usr/bin/env python3
"""
Parse Yoga Spandakarika EPUB into SS-style stanza YAML files.

Usage:
  python scripts/yoga_spandakarika_epub_to_yaml.py <input.epub> <output_dir>
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

import yaml
from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, epub


CORE_DOCS = {
    "9781620554418_c02.htm",  # stanzas 1-16
    "9781620554418_c03.htm",  # stanzas 17-27
    "9781620554418_c04.htm",  # stanzas 28-52
}


def clean_text(raw: str) -> str:
    raw = raw.replace("\r", "\n").replace("\f", "\n")
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in raw.split("\n")]
    out: list[str] = []
    blank = False
    for ln in lines:
        if not ln:
            if not blank:
                out.append("")
            blank = True
            continue
        # Drop isolated footnote/index markers.
        if re.fullmatch(r"\*?\d{1,3}", ln):
            continue
        out.append(ln)
        blank = False
    text = "\n".join(out).strip()
    return re.sub(r"\n{3,}", "\n\n", text)


def section_for_stanza(n: int) -> str:
    if 1 <= n <= 16:
        return "First Flow"
    if 17 <= n <= 27:
        return "Second Flow"
    return "Third Flow"


def title_from_translation(t: str, n: int) -> str:
    t = t.strip()
    if not t:
        return f"Stanza {n}"
    sentence = re.split(r"(?<=[.!?])\s+", t)[0].strip()
    sentence = sentence.replace("\n", " ")
    sentence = re.sub(r"\s+", " ", sentence)
    if len(sentence) > 90:
        sentence = sentence[:87].rstrip() + "..."
    return sentence or f"Stanza {n}"


def split_translation_commentary(block: str) -> tuple[str, str]:
    parts = [p.strip() for p in re.split(r"\n\s*\n", block) if p.strip()]
    if not parts:
        return "", ""
    translation = parts[0]
    commentary = "\n\n".join(parts[1:]).strip()
    return translation, commentary


def tighten_commentary(commentary: str, max_paragraphs: int = 3, max_chars: int = 1800) -> str:
    """
    Keep the first substantial paragraphs to match a concise SS-like read.
    """
    text = commentary.strip()
    if not text:
        return ""
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

    def is_insert_paragraph(p: str) -> bool:
        pl = p.lower().strip()
        if not pl:
            return True
        # Common anthology/quote prefaces.
        if "sings:" in pl or pl.startswith("mind, empty like space"):
            return True
        if re.match(r"^(in|from)\s+the\s+[^:]{1,90}:\s*$", pl):
            return True
        # Remove footnote-like/citation-heavy segments.
        if re.search(r"\[[^\]]{1,40}\]", p) and len(p) < 500:
            return True
        # Drop poem/chant inserts: many short lines and sparse prose punctuation.
        lines = [ln.strip() for ln in p.splitlines() if ln.strip()]
        if len(lines) >= 5:
            short_lines = sum(1 for ln in lines if len(ln.split()) <= 7)
            if short_lines / len(lines) >= 0.7:
                return True
        return False
    kept: list[str] = []
    for p in paras:
        # Skip tiny fragments and list-like remnants from EPUB layout noise.
        if len(p) < 30:
            continue
        if is_insert_paragraph(p):
            continue
        kept.append(p)
        if len(kept) >= max_paragraphs:
            break
    if not kept:
        kept = paras[:1]
    out = "\n\n".join(kept)
    out = re.sub(r"\s+", " ", out).strip()
    if len(out) > max_chars:
        out = out[: max_chars - 3].rstrip() + "..."
    return out


def suggest_abhyasa(translation: str, commentary: str) -> str:
    """
    Generate short practice prompts keyed to dominant motifs.
    """
    blob = f"{translation} {commentary}".lower()
    if any(k in blob for k in ("breath", "inhale", "exhale", "prana", "spanda")):
        return "Sit for 5 minutes and follow the breath naturally. At each inhale and exhale, notice the subtle vibration of awareness before naming it."
    if any(k in blob for k in ("action", "do", "actor", "fruit", "goal")):
        return "Choose one ordinary action today and perform it fully without seeking an outcome. Afterward, rest for one minute in the felt sense of simple presence."
    if any(re.search(p, blob) for p in (r"\bspeech\b", r"\bwords?\b", r"\blanguage\b", r"\binner talk\b", r"\bmantra\b")):
        return "For 3 minutes, watch inner speech without suppressing it. Each time words arise, return to the silent awareness that knows the words."
    if any(k in blob for k in ("dream", "sleep", "waking", "three states")):
        return "Before sleep and upon waking, pause for 30 seconds and ask: what is unchanged across waking, dream, and sleep? Rest in that recognition."
    if any(k in blob for k in ("self", "consciousness", "awareness", "shiva", "shakti")):
        return "Close the eyes for 2 minutes and release all labels. Repeatedly return to the immediate sense 'I am aware' without adding any story."
    return "Read the stanza slowly three times. Keep one line in attention through the day, and return to it whenever the mind contracts."


def parse_stanza_blocks(text: str) -> list[tuple[list[int], str]]:
    """
    Return list of (stanza_numbers, block_text).
    Handles markers like:
      STANZA 11
      STANZAS 12 AND 13
      STANZAS 14   (inferred as range up to next marker-1)
    """
    marker_re = re.compile(
        r"(?m)^\s*(STANZA|STANZAS)\s+([0-9]+(?:\s*,\s*[0-9]+)*(?:\s*,?\s*(?:AND|&)\s*[0-9]+)?)\b",
        re.IGNORECASE,
    )
    ms = list(marker_re.finditer(text))
    out: list[tuple[list[int], str]] = []
    if not ms:
        return out

    for i, m in enumerate(ms):
        word = m.group(1).upper()
        nums_raw = m.group(2).strip()
        start = m.end()
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        block = text[start:end].strip()

        nums = [int(x) for x in re.findall(r"\d+", nums_raw)]
        if len(nums) == 2:
            stanza_nums = list(range(min(nums), max(nums) + 1))
        elif len(nums) > 2:
            stanza_nums = sorted(set(nums))
        elif len(nums) == 1:
            n = nums[0]
            if word == "STANZAS":
                # Infer range for plural marker with one number.
                if i + 1 < len(ms):
                    next_first = int(re.findall(r"\d+", ms[i + 1].group(2))[0])
                    if next_first > n + 1:
                        stanza_nums = list(range(n, next_first))
                    else:
                        stanza_nums = [n]
                else:
                    stanza_nums = [n]
            else:
                stanza_nums = [n]
        else:
            stanza_nums = []

        if stanza_nums and block:
            out.append((stanza_nums, block))
    return out


def parse_epub(epub_path: Path) -> dict[int, dict]:
    book = epub.read_epub(str(epub_path))
    stanza_map: dict[int, dict] = {}

    docs: list[tuple[str, str]] = []
    for item in book.get_items_of_type(ITEM_DOCUMENT):
        name = item.get_name()
        if name not in CORE_DOCS:
            continue
        soup = BeautifulSoup(item.get_content(), "lxml")
        text = clean_text(soup.get_text("\n"))
        docs.append((name, text))

    for _, doc_text in sorted(docs, key=lambda x: x[0]):
        for stanza_nums, block in parse_stanza_blocks(doc_text):
            tr, comm = split_translation_commentary(block)
            cleaned_comm = tighten_commentary(comm)
            for n in stanza_nums:
                if not (1 <= n <= 52):
                    continue
                stanza_map[n] = {
                    "title": title_from_translation(tr, n),
                    "translation": tr,
                    "commentary": cleaned_comm,
                    "abhyasa": suggest_abhyasa(tr, cleaned_comm),
                }
    _collapse_duplicate_stanza_text(stanza_map)
    return stanza_map


def _collapse_duplicate_stanza_text(stanza_map: dict[int, dict]) -> None:
    """
    Some source blocks are explicitly grouped (e.g., stanzas 14-16), yielding duplicate
    text across multiple stanza ids. Keep full text on the first stanza and replace
    duplicates with compact cross-references.
    """
    clusters: dict[tuple[str, str], list[int]] = {}
    for n, rec in stanza_map.items():
        tr = (rec.get("translation") or "").strip()
        co = (rec.get("commentary") or "").strip()
        if not tr:
            continue
        clusters.setdefault((tr, co), []).append(n)

    for nums in clusters.values():
        if len(nums) <= 1:
            continue
        nums = sorted(nums)
        primary = nums[0]
        for n in nums[1:]:
            stanza_map[n]["title"] = f"Shared with Stanza {primary}"
            stanza_map[n]["translation"] = (
                f"Shared source passage with Stanza {primary}. "
                f"See Stanza {primary} for the full translation and commentary."
            )
            stanza_map[n]["commentary"] = ""


def main() -> int:
    ap = argparse.ArgumentParser(description="Convert Yoga Spandakarika EPUB into stanza YAML files.")
    ap.add_argument("epub_path", type=Path)
    ap.add_argument("output_dir", type=Path)
    args = ap.parse_args()

    stanza_map = parse_epub(args.epub_path)

    if args.output_dir.exists():
        shutil.rmtree(args.output_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    for n in range(1, 53):
        rec = stanza_map.get(n)
        if not rec:
            # Keep continuity with placeholders so IDs remain stable.
            rec = {
                "title": f"Stanza {n}",
                "translation": f"[Missing extraction for stanza {n}; please review source EPUB manually.]",
                "commentary": "",
            }

        sid = f"SP_{n:02d}"
        obj = {
            "sutra_id": sid,
            "sutra": f"{n}",
            "title": rec["title"],
            "collection": "Yoga Spandakarika",
            "section": section_for_stanza(n),
            "sanskrit": "",
            "transliteration": "",
            "translation": rec["translation"],
            "commentary": rec["commentary"],
            "voice_of_siva": "",
            "abhyasa": rec.get("abhyasa", ""),
            "modes": {"bhasya": "", "doctrinal": "", "comparative": "", "sadhana": ""},
            "glossary": [],
        }
        out = args.output_dir / f"SP_{n:02d}.yaml"
        out.write_text(
            yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )
        written += 1

    print(f"Wrote {written} YAML files to {args.output_dir}")
    missing = [n for n in range(1, 53) if "Missing extraction" in (stanza_map.get(n, {}).get("translation", ""))]
    if missing:
        print(f"Potentially missing stanzas: {missing}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

