"""Shared parsers for public-domain anchor texts (Heraclitus Patrick, Giles Zhuangzi)."""

from __future__ import annotations

import re
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PD_ROOT = ROOT / "data" / "raw_texts" / "pd"


def _pd_path(*parts: str, legacy: Path | None = None) -> Path:
    """Prefer data/raw_texts/pd/ layout; fall back to legacy raw_texts paths."""
    candidate = PD_ROOT.joinpath(*parts)
    if candidate.exists():
        return candidate
    if legacy and legacy.exists():
        return legacy
    return candidate

_ROMAN = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
]


def roman_to_int(s: str) -> int | None:
    s = re.sub(r"[^IVXLCDM]", "", s.upper())
    if not s:
        return None
    total = 0
    i = 0
    while i < len(s):
        matched = False
        for value, numeral in _ROMAN:
            if s[i : i + len(numeral)] == numeral:
                total += value
                i += len(numeral)
                matched = True
                break
        if not matched:
            return None
    return total or None


def _normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _is_citation_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    low = s.lower()
    if low.startswith(
        (
            "compare ",
            "sources.—",
            "sourcres.—",
            "context :",
            "context:",
            "hippolytus,",
            "aristotle,",
            "plutarch,",
            "clement of alex",
            "sextus empir",
            "theodoretus,",
            "plato,",
            "proclus ",
            "parmenides ",
            "lucianus,",
            "chalcidius ",
            "simplicius ",
            "eustathius ",
            "schol. ",
            "idem,",
        )
    ):
        return True
    if re.match(r"^[A-Z][a-z]+(?:ius|us|es|is|or),", s):
        return True
    if re.match(r"^[A-Z][a-z]+\s+[A-Z][a-z]+\.", s):  # e.g. Chalcidius in Tim.
        return True
    if re.match(r"^\d+\s+HERACLITUS\.", s):
        return True
    if re.match(r"^ON NATURE\.", s):
        return True
    if low.startswith("from gods and human"):
        return True
    if "p. " in low and re.search(r"\b\d{2,4}\b", low):
        return True
    return False


def _is_sources_break(line: str) -> bool:
    s = line.strip().lower()
    return s.startswith("sources.—") or s.startswith("sourcres.—")


def parse_patrick_heraclitus(text: str) -> dict[int, str]:
    """Parse Patrick (1889) translation keyed by fragment number (Roman numeral).

    Uses first occurrence of each Roman marker in the translation portion only,
    merging lines across OCR page breaks while skipping source citations.
    """
    start = text.find("HERACLITUS OF EPHESUS ON NATURE")
    if start < 0:
        start = text.find("HERACLITUS OF KPHESUS ON NATURE")
    if start < 0:
        raise ValueError("Could not locate Patrick translation section")

    end = text.find("\nCRITICAL NOTES.", start)
    if end < 0:
        end = len(text)
    lines = text[start:end].splitlines()

    marker = re.compile(r"^\s*([IVXLCDMivxlcdm]+)\s*\.?\s*—\s*(.*)$")
    seen: set[int] = set()
    parts: dict[int, list[str]] = {}
    current_num: int | None = None
    buff: list[str] = []
    in_sources = False

    def flush() -> None:
        nonlocal buff, in_sources
        if current_num is None:
            buff = []
            in_sources = False
            return
        chunk = _clean_patrick_chunk(" ".join(buff))
        if len(chunk) >= 12 and not _is_source_citation(chunk):
            parts.setdefault(current_num, []).append(chunk)
        buff = []
        in_sources = False

    for line in lines:
        if _is_sources_break(line):
            flush()
            in_sources = True
            continue
        m = marker.match(line)
        if m:
            num = roman_to_int(m.group(1))
            if num is None:
                continue
            if num in seen:
                in_sources = True
                continue
            flush()
            seen.add(num)
            current_num = num
            first = m.group(2).strip()
            buff = [first] if first and not _is_citation_line(first) else []
            in_sources = False
            continue
        if current_num is None or in_sources:
            continue
        if _is_citation_line(line):
            continue
        buff.append(line.strip())

    flush()

    out: dict[int, str] = {}
    for num, chunks in parts.items():
        # First chunk is the translation; later chunks are OCR continuations only.
        merged = _clean_patrick_chunk(chunks[0])
        if len(merged) >= 12 and not _is_source_citation(merged):
            out[num] = merged

    _repair_patrick_ocr_gaps(lines, out)
    return out


def _repair_patrick_ocr_gaps(lines: list[str], out: dict[int, str]) -> None:
    """Fix known Archive.org OCR page-break splits in Patrick."""
    joined = re.sub(r"-\s+", "", "\n".join(lines))

    if 2 in out:
        if out[2].rstrip().endswith("ignorant of what"):
            cut = out[2].find("it is ordered.")
            if cut > 0:
                out[2] = out[2][: cut + len("it is ordered.")]
        if "asleep" not in out[2].lower():
            m = re.search(
                r"they do when awake as they are forgetful of what they\s+do when asleep\.?",
                joined,
                re.IGNORECASE,
            )
            if m:
                out[2] = _clean_patrick_chunk(f"{out[2]} {m.group(0)}")

    m = re.search(
        r"(separates unites with itself\. It is a harmony of oppositions, as in the case of the bow and of the lyre\.?)",
        joined,
        re.IGNORECASE,
    )
    if m:
        lead = "They do not understand how that which "
        out[45] = _clean_patrick_chunk(f"{lead}{m.group(1)}")


def _clean_patrick_chunk(chunk: str) -> str:
    for stop in ("Context :—", "Context:—", "Hippolytus,", "Aristotle,", "Sextus Empir."):
        idx = chunk.find(stop)
        if idx > 40:
            chunk = chunk[:idx]
    chunk = chunk.replace("|", " ")
    chunk = re.sub(r"-\s+", "", chunk)
    chunk = re.sub(r"\s+", " ", chunk).strip()
    return chunk


def _is_source_citation(text: str) -> bool:
    head = text[:80].lower()
    markers = (
        "hippolytus",
        "clement of alex",
        "sextus empir",
        "aristotle",
        "plutarch",
        "context :",
        "context:",
        "compare ",
        "sources.—",
        "theodoretus",
    )
    return any(m in head for m in markers)


def match_patrick_fragment(haxton_text: str, patrick: dict[int, str]) -> tuple[int, str, float]:
    """Pick the best Patrick fragment for an existing Haxton/DK unit."""
    h = _normalize(haxton_text)
    if not h:
        return 0, "", 0.0
    best_n = 0
    best_text = ""
    best_score = 0.0
    for n, p in patrick.items():
        score = SequenceMatcher(None, h, _normalize(p)).ratio()
        if score > best_score:
            best_n = n
            best_text = p
            best_score = score
    return best_n, best_text, best_score


def patrick_for_corpus_number(corpus_n: int, patrick: dict[int, str], haxton_text: str) -> tuple[int, str, float]:
    """Prefer same-number Patrick fragment; fall back to fuzzy match."""
    # Haxton EPUB order swaps Patrick I and II relative to file numbers 1 and 2.
    direct_map = {1: 2, 2: 1}
    candidate = direct_map.get(corpus_n, corpus_n)
    if candidate in patrick:
        return candidate, patrick[candidate], 1.0
    return match_patrick_fragment(haxton_text, patrick)


def parse_giles_chuang_tzu(text: str) -> dict[int, dict[str, str]]:
    """Parse Giles (1889) chapters from Project Gutenberg plain text."""
    start = text.find("CHAPTER I.")
    if start < 0:
        raise ValueError("Could not locate Giles chapter I")
    body = text[start:]
    # Stop before appendices if present
    for marker in ("\nAPPENDIX", "\nIndex", "\nINDEX"):
        idx = body.find(marker)
        if idx > 0:
            body = body[:idx]

    pattern = re.compile(
        r"CHAPTER\s+([IVXLCDM]+)\.\s*\n([^\n]+)\n\n(Argument:—[^\n]+\n\n)?(.+?)(?=\nCHAPTER\s+[IVXLCDM]+\.\s*\n|\Z)",
        re.DOTALL,
    )
    chapters: dict[int, dict[str, str]] = {}
    for m in pattern.finditer(body):
        num = roman_to_int(m.group(1))
        if num is None:
            continue
        subtitle = m.group(2).strip()
        content = (m.group(4) or "").strip()
        content = re.sub(r"\n{3,}", "\n\n", content)
        chapters[num] = {
            "title": subtitle,
            "body": content,
            "excerpt": content[:1200].strip(),
        }
    return chapters


def load_patrick_text(path: Path | None = None) -> str:
    path = path or _pd_path(
        "greek", "heraclitus_patrick_1889.txt",
        legacy=ROOT / "data" / "raw_texts" / "patrick_heraclitus_1889.txt",
    )
    if not path.exists():
        raise FileNotFoundError(
            f"Patrick Heraclitus text not found at {path}. "
            "Run: python scripts/fetch_pd_sources.py — or download archive.org/details/fragmentsofworko00hera"
        )
    return path.read_text(encoding="utf-8", errors="replace")


def load_giles_chuang_tzu(path: Path | None = None) -> str:
    path = path or _pd_path(
        "chinese", "zhuangzi_giles_gutenberg_59709.txt",
        legacy=ROOT / "data" / "raw_texts" / "ChaungTzuRaw",
    )
    if not path.exists():
        raise FileNotFoundError(f"Giles Zhuangzi text not found at {path}. Run: python scripts/fetch_pd_sources.py")
    return path.read_text(encoding="utf-8", errors="replace")
