#!/usr/bin/env python3
"""
Parse Plato's Phaedo EPUB into dialogue-aware YAML units.

Outputs two unit types:
- dialogue_section (short multi-turn exchanges)
- wisdom_pearl (concise high-signal statements)

Usage:
  python scripts/phaedo_epub_to_yaml.py <input.epub> <output_dir>
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

import yaml
from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, epub


SPEAKERS = ("ECHECRATES", "PHAEDO", "SOCRATES", "SIMMIAS", "CEBES", "CRITO")
SPEAKER_RE = re.compile(r"\b(" + "|".join(SPEAKERS) + r")\s*:\s*", re.IGNORECASE)

PEARL_KEYWORDS = (
    "soul",
    "death",
    "wisdom",
    "truth",
    "philosopher",
    "virtue",
    "body",
    "justice",
    "knowledge",
    "recollection",
    "immortality",
    "good",
)

DIALOGUE_KEYWORDS = (
    "soul",
    "death",
    "dying",
    "wisdom",
    "truth",
    "philosopher",
    "virtue",
    "body",
    "justice",
    "knowledge",
    "recollection",
    "immortality",
    "good",
    "being",
    "reason",
)

PHIL_CLAIM_TERMS = (
    " is ",
    " are ",
    " be ",
    " know",
    " true",
    " good",
    " just",
    " soul",
    " death",
    " wisdom",
    " knowledge",
    " being",
    " causes",
    " because",
    " therefore",
)


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
        out.append(ln)
        blank = False
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()


def _main_dialogue_text(epub_path: Path) -> str:
    book = epub.read_epub(str(epub_path))
    # Most editions keep Phaedo body in split_003.
    for item in book.get_items_of_type(ITEM_DOCUMENT):
        if "split_003" in item.get_name().lower():
            soup = BeautifulSoup(item.get_content(), "lxml")
            return clean_text(soup.get_text("\n"))

    # Fallback: pick the longest document chunk.
    best = ""
    for item in book.get_items_of_type(ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), "lxml")
        text = clean_text(soup.get_text("\n"))
        if len(text) > len(best):
            best = text
    return best


def parse_turns(text: str) -> list[dict[str, str]]:
    start = text.find("ECHECRATES:")
    if start > -1:
        text = text[start:]

    ms = list(SPEAKER_RE.finditer(text))
    turns: list[dict[str, str]] = []
    if not ms:
        return turns

    for i, m in enumerate(ms):
        speaker = m.group(1).upper()
        begin = m.end()
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        body = text[begin:end].strip()
        body = re.sub(r"\n{3,}", "\n\n", body)
        if not body:
            continue
        turns.append({"speaker": speaker, "text": body})
    return turns


def first_sentence(s: str, limit: int = 110) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    if not s:
        return ""
    t = re.split(r"(?<=[.!?])\s+", s)[0].strip()
    return t if len(t) <= limit else t[: limit - 3].rstrip() + "..."


def suggest_abhyasa(blob: str) -> str:
    b = blob.lower()
    if "in our power" in b or "control" in b:
        return "Write two short lists: what is in your control and what is not. Practice acting only on the first list today."
    if "soul" in b or "body" in b or "death" in b:
        return "Sit quietly for 3 minutes and observe changing sensations and thoughts. Ask what in experience is aware of these changes."
    if "virtue" in b or "justice" in b or "good" in b:
        return "Choose one small action today that reflects your highest value, and complete it without delay."
    return "Read this slowly three times. Pause for one minute and write one sentence of practical insight."


def _keyword_hits(s: str, keywords: tuple[str, ...]) -> int:
    l = s.lower()
    return sum(1 for k in keywords if k in l)


def _word_count(s: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", s or ""))


def _has_philosophical_claim(s: str) -> bool:
    compact = re.sub(r"\s+", " ", s.lower()).strip()
    blob = f" {compact} "
    return any(term in blob for term in PHIL_CLAIM_TERMS)


def _is_thin_unit_text(s: str) -> bool:
    return _word_count(s) < 40 and not _has_philosophical_claim(s)


def _is_substantive_window(window: list[dict[str, str]]) -> bool:
    block = " ".join(t["text"] for t in window)
    if len(block) < 360:
        return False
    # Keep philosophically dense windows; drop logistical narration.
    if _keyword_hits(block, DIALOGUE_KEYWORDS) >= 3:
        return True
    if "SOCRATES" in [t["speaker"] for t in window] and _keyword_hits(block, DIALOGUE_KEYWORDS) >= 2:
        return True
    return False


def _topic_label(block: str) -> str:
    b = block.lower()
    if "recollection" in b or "remember" in b or "knowledge" in b:
        return "On Recollection and Knowledge"
    if "soul" in b and ("death" in b or "dying" in b):
        return "On Soul and Death"
    if "body" in b and "soul" in b:
        return "On Body and Soul"
    if "virtue" in b or "justice" in b or "good" in b:
        return "On Virtue and the Good"
    if "philosopher" in b or "philosophy" in b:
        return "On the Philosophic Life"
    return "Dialogical Inquiry"


def _strip_lead_sentence(text: str, lead: str) -> str:
    text_n = re.sub(r"\s+", " ", text).strip()
    lead_n = re.sub(r"\s+", " ", lead).strip()
    if text_n.lower().startswith(lead_n.lower()):
        rest = text_n[len(lead_n) :].lstrip(" -,:;")
        return rest if rest else text_n
    return text_n


def build_dialogue_sections(turns: list[dict[str, str]], rejected: list[dict[str, str]] | None = None) -> list[dict]:
    out: list[dict] = []
    idx = 1
    # Use overlapping windows of 3 turns for context-rich RAG chunks.
    for i in range(0, max(0, len(turns) - 2), 2):
        window = turns[i : i + 3]
        if not _is_substantive_window(window):
            if rejected is not None:
                snippet = re.sub(r"\s+", " ", " ".join(f"{t['speaker']}: {t['text']}" for t in window))[:220]
                rejected.append({"kind": "dialogue_section", "reason": "non_substantive_window", "snippet": snippet})
            continue
        block = "\n\n".join(f"{t['speaker']}: {t['text']}" for t in window)
        if _is_thin_unit_text(block):
            if rejected is not None:
                snippet = re.sub(r"\s+", " ", block)[:220]
                rejected.append(
                    {
                        "kind": "dialogue_section",
                        "reason": "thin_unit_under_40_without_claim",
                        "snippet": snippet,
                    }
                )
            continue
        if len(block) > 2400:
            block = block[:2397].rstrip() + "..."
        # Anchor on the most philosophically dense turn in window.
        anchor = max(window, key=lambda t: (_keyword_hits(t["text"], DIALOGUE_KEYWORDS), len(t["text"])))
        lead = first_sentence(anchor["text"], limit=150)
        title = f"{_topic_label(block)}"
        commentary_turns: list[str] = []
        for t in window:
            t_text = t["text"]
            if t is anchor:
                t_text = _strip_lead_sentence(t_text, lead)
            commentary_turns.append(f"{t['speaker']}: {t_text}")

        out.append(
            {
                "sutra_id": f"PHA_D{idx:03d}",
                "collection": "Phaedo (Plato)",
                "section": "dialogue_section",
                "title": title,
                "sanskrit": "",
                "transliteration": "",
                "translation": f"{anchor['speaker']}: {lead}",
                "commentary": "\n\n".join(commentary_turns),
                "voice_of_siva": "",
                "abhyasa": suggest_abhyasa(block),
                "modes": {
                    "bhasya": "",
                    "doctrinal": "",
                    "comparative": "",
                    "sadhana": suggest_abhyasa(block),
                },
                "glossary": [],
            }
        )
        idx += 1
    return out


def build_wisdom_pearls(turns: list[dict[str, str]], limit: int = 72) -> list[dict]:
    # Collect sentence-level candidates from Socratic-heavy turns.
    cands: list[str] = []
    for t in turns:
        speaker = t["speaker"]
        if speaker not in {"SOCRATES", "SIMMIAS", "CEBES", "PHAEDO"}:
            continue
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", t["text"])) if s.strip()]
        for s in sentences:
            sl = s.lower()
            if len(s) < 170 or len(s) > 520:
                continue
            if sum(1 for k in PEARL_KEYWORDS if k in sl) < 2:
                continue
            cands.append(s)

    pearls: list[str] = []
    seen: set[str] = set()
    for c in cands:
        key = re.sub(r"\W+", " ", c.lower())[:140]
        if key in seen:
            continue
        seen.add(key)
        pearls.append(c)
        if len(pearls) >= limit:
            break

    out: list[dict] = []
    for i, p in enumerate(pearls, start=1):
        out.append(
            {
                "sutra_id": f"PHA_P{i:03d}",
                "collection": "Phaedo (Plato)",
                "section": "wisdom_pearl",
                "title": first_sentence(p, limit=84),
                "sanskrit": "",
                "transliteration": "",
                "translation": p,
                "commentary": "",
                "voice_of_siva": "",
                "abhyasa": suggest_abhyasa(p),
                "modes": {
                    "bhasya": "",
                    "doctrinal": "",
                    "comparative": "",
                    "sadhana": suggest_abhyasa(p),
                },
                "glossary": [],
            }
        )
    return out


def parse_epub(epub_path: Path) -> tuple[list[dict], list[dict[str, str]]]:
    text = _main_dialogue_text(epub_path)
    turns = parse_turns(text)
    rejected: list[dict[str, str]] = []
    dialogue_units = build_dialogue_sections(turns, rejected=rejected)
    pearl_units = build_wisdom_pearls(turns, limit=72)
    return [*dialogue_units, *pearl_units], rejected


def main() -> int:
    ap = argparse.ArgumentParser(description="Convert Phaedo EPUB to dialogue and wisdom-pearl YAML files.")
    ap.add_argument("epub_path", type=Path)
    ap.add_argument("output_dir", type=Path)
    args = ap.parse_args()

    records, rejected = parse_epub(args.epub_path)
    if args.output_dir.exists():
        shutil.rmtree(args.output_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for rec in records:
        sid = rec["sutra_id"].lower()
        out = args.output_dir / f"{sid}.yml"
        out.write_text(
            yaml.safe_dump(rec, allow_unicode=True, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )
    log_path = args.output_dir / "_thin_units.log"
    if rejected:
        lines = [
            f"{r.get('kind','unknown')}\t{r.get('reason','unknown')}\t{r.get('snippet','')}"
            for r in rejected
        ]
        log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    elif log_path.exists():
        log_path.unlink()
    print(f"Wrote {len(records)} YAML files to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

