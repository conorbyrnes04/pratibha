"""Extract Patanjali Yoga Sutras from Satchidananda PDF + GRETIL IAST → Pratibha MD.

Usage:
  python scripts/patanjali_yoga_sutras_pdf_to_pratibha_md.py --dry-run
  python scripts/patanjali_yoga_sutras_pdf_to_pratibha_md.py --start 2.24 --end 4.34
  python scripts/patanjali_yoga_sutras_pdf_to_pratibha_md.py --all
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import httpx
from pdfminer.high_level import extract_text

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.llm import smart_chat  # noqa: E402

PDF_PATH = ROOT / "data/raw_texts/Yoga Sutras of Patanjali.pdf"
GRETIL_PATH = ROOT / "data/raw_texts/yoga_sutras_gretil_iast.txt"
OUT_PATH = ROOT / "data/pratibha_md/patanjali_yoga_sutras.md"

PADA_COUNTS = {1: 51, 2: 55, 3: 55, 4: 34}  # GRETIL recension: 195 total

HEADER = """# Yoga Sūtras of Patañjali

**Edition basis:** Swami Satchidananda, *The Yoga Sutras of Patanjali* (Integral Yoga Publications, 1978).

**Sanskrit basis:** GRETIL `patyog_u.htm` (Anandashrama Sanskrit Series 47, 1904; input Philipp A. Maas). Full IAST diacritics in the `### IAST` layer.

**Translation decisions (this batch):**
- Units **before 2.24** (if present) used an earlier Dvivedi (1890) anchor from a prior generation pass.
- From **2.24 onward**, `Body` reproduces Satchidananda's English aphorism where extracted; `Pratibha Translation` is a fresh rendering from Sanskrit.
- The `### Devanagari` layer is an **editorial reconstruction** from GRETIL IAST; it is *not* source-verified against a manuscript.
- Satchidananda's commentary informs `Pratibha Commentary` but is not reproduced wholesale.

One unit per numbered sūtra (four pādas, 195 in the GRETIL recension).

---
"""

SYSTEM_PROMPT = """You are a Pratibha manuscript editor producing one Yoga Sūtra unit in structured JSON.

Return ONLY a JSON object (no markdown fences) with these keys:
{
  "title": "thematic English title (3-8 words; NOT 'Sūtra 1.1')",
  "devanagari": "Devanagari reconstruction of the sūtra from IAST (single or few lines)",
  "pratibha_translation": "present-tense, readable, precise English; preserve technical terms in brackets on first use",
  "commentary": "Pratibha Commentary: >=150 words. Open with explicit philosophical claim. Name contested move. Do NOT open with 'In this passage'. Situate in Yoga/Sāṃkhya tradition. Point to existential application. Integrate insights from Satchidananda commentary when provided.",
  "key_terms": [{"term": "iast_term", "script": "devanagari or transliteration", "entry": "etymology -> tradition meaning -> what default translation misses"}],
  "resonances": [{"citation": "Tradition/Author, Text, Passage", "resonance": "structural homology with specific detail", "divergence": "where parallel breaks and why productive"}],
  "practice": "single executable instruction, second person present tense, derived from THIS sūtra only"
}

Rules:
- key_terms: 2-4 terms doing real philosophical work in THIS sūtra.
- resonances: 2-4 entries with structural homology, specific citation, and divergence clause.
- commentary must be original analysis, not paraphrase of translation or Satchidananda. Never prefix commentary with "Pratibha Commentary:".
- devanagari must be accurate IAST-to-Devanagari (e.g. draṣṭuḥ -> द्रष्टुः, not दर्शुः).
- On first document appearance of yoga, citta, vṛtti, puruṣa, prakṛti, samādhi, īśvara — give robust key_terms entries.
- Output valid JSON only."""

SUTRA_HEAD_RE = re.compile(r"(?m)^(\d+)\.\s+(.+)$")


def parse_gretil(path: Path) -> dict[tuple[int, int], str]:
    text = path.read_text(encoding="utf-8")
    out: dict[tuple[int, int], str] = {}
    for line in text.splitlines():
        m = re.search(r"(.+?)\s*\|\|\s*YS_(\d+)\.(\d+)\s*\|\|", line)
        if m:
            out[(int(m.group(2)), int(m.group(3)))] = m.group(1).strip()
    return out


@dataclass
class AnchorUnit:
    pada: int
    num: int
    sanskrit: str
    aphorism: str
    commentary: str


def extract_pdf_text(pdf_path: Path) -> str:
    return extract_text(str(pdf_path)).replace("\x0c", "\n")


def _book_anchors(text: str) -> dict[int, int]:
    b4 = text.find("Book\tFour\n\nKaivalya")
    gloss = text.find("Glossary\tof\tSanskrit\tTerms", b4 if b4 >= 0 else 0)
    return {
        1: text.find("Book\tOne\n\nSamādhi"),
        2: text.find("Book\tTwo\n\nSādhana"),
        3: text.find("Book\tThree\n\nVibhūti"),
        4: b4,
        5: gloss if gloss > b4 else len(text),
    }


def _split_sutra_block(block: str) -> tuple[str, str, str]:
    """Return (sanskrit_line, english_aphorism, commentary)."""
    paras = [re.sub(r"\s+", " ", p.strip()) for p in re.split(r"\n\s*\n", block.strip()) if p.strip()]
    if not paras:
        return "", "", ""

    sanskrit = paras[0]
    gloss: list[str] = []
    idx = 1
    while idx < len(paras) and "=" in paras[idx] and ";" in paras[idx]:
        gloss.append(paras[idx])
        idx += 1

    aphorism = ""
    commentary_parts: list[str] = []
    if idx < len(paras):
        aphorism = paras[idx]
        idx += 1
    commentary_parts.extend(paras[idx:])
    return sanskrit, aphorism, "\n\n".join(commentary_parts)


def parse_satchidananda(text: str) -> dict[tuple[int, int], AnchorUnit]:
    anchors = _book_anchors(text)
    if any(anchors[p] < 0 for p in range(1, 5)):
        raise ValueError("Could not locate all four book anchors in Satchidananda PDF text")

    units: dict[tuple[int, int], AnchorUnit] = {}
    for pada in range(1, 5):
        sec = text[anchors[pada] : anchors[pada + 1]]
        matches = list(SUTRA_HEAD_RE.finditer(sec))
        expected = 1
        for i, m in enumerate(matches):
            num = int(m.group(1))
            if num != expected or num > PADA_COUNTS[pada]:
                continue
            block = sec[m.end() :]
            nxt = SUTRA_HEAD_RE.search(block)
            if nxt:
                block = block[: nxt.start()]
            sanskrit, aphorism, commentary = _split_sutra_block(block)
            if not sanskrit:
                sanskrit = re.sub(r"\s+", " ", m.group(2)).strip()
            units[(pada, num)] = AnchorUnit(
                pada=pada,
                num=num,
                sanskrit=sanskrit,
                aphorism=aphorism,
                commentary=commentary,
            )
            expected += 1
    return units


def _extract_json(raw: str) -> dict:
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.MULTILINE).strip()
    start, end = raw.find("{"), raw.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("no JSON object in model output")
    return json.loads(raw[start : end + 1])


def _pada_label(pada: int) -> str:
    names = {1: "Samādhi", 2: "Sādhana", 3: "Vibhūti", 4: "Kaivalya"}
    return names[pada]


def render_unit(
    pada: int,
    num: int,
    iast: str,
    anchor: AnchorUnit | None,
    data: dict,
) -> str:
    body = (anchor.aphorism if anchor and anchor.aphorism else iast).strip()
    source = f"Patañjali, Yoga Sūtras {pada}.{num} ({_pada_label(pada)} Pāda)"
    deva_note = "*(editorial reconstruction from IAST; not source-verified)*"
    deva = str(data.get("devanagari") or "").strip()
    deva_block = f"{deva_note}\n\n{deva}" if deva else deva_note

    key_lines = []
    for kt in data.get("key_terms") or []:
        if not isinstance(kt, dict) or not kt.get("term"):
            continue
        script = str(kt.get("script") or "").strip()
        entry = str(kt.get("entry") or "").strip()
        term = str(kt["term"]).strip()
        if script:
            key_lines.append(f"**{term} ({script})** — {entry}")
        else:
            key_lines.append(f"**{term}** — {entry}")

    res_lines = []
    for r in data.get("resonances") or []:
        if not isinstance(r, dict) or not r.get("citation"):
            continue
        line = f"**{str(r['citation']).strip()}:** {str(r.get('resonance') or '').strip()}"
        div = str(r.get("divergence") or "").strip()
        if div:
            line += f"\n*Divergence:* {div}"
        res_lines.append(line)

    return "\n".join(
        [
            f"## {str(data.get('title') or '').strip()}",
            f"**Source:** {source}",
            "",
            body,
            "",
            "---",
            "",
            "### Devanagari",
            deva_block,
            "",
            "### IAST",
            "",
            iast,
            "",
            "### Pratibha Translation",
            "",
            str(data.get("pratibha_translation") or "").strip(),
            "",
            "### Pratibha Commentary",
            "",
            str(data.get("commentary") or "").strip(),
            "",
            "### Key Terms",
            "",
            "\n\n".join(key_lines) if key_lines else "",
            "",
            "### Cross-Tradition Resonances",
            "",
            "\n\n".join(res_lines) if res_lines else "",
            "",
            "### Practice (Abhyasa)",
            "",
            str(data.get("practice") or "").strip(),
            "",
            "---",
            "",
        ]
    )


async def generate_unit(
    pada: int,
    num: int,
    iast: str,
    anchor: AnchorUnit | None,
    model: str,
) -> dict:
    aph = anchor.aphorism if anchor and anchor.aphorism else "(not extracted from PDF)"
    sanskrit = anchor.sanskrit if anchor else ""
    comm = (anchor.commentary if anchor else "")[:8000]
    user = f"""Yoga Sūtra YS {pada}.{num} ({_pada_label(pada)} Pāda)

IAST (authoritative Sanskrit):
{iast}

Satchidananda English aphorism (Body anchor):
{aph}

Satchidananda Sanskrit line (from PDF):
{sanskrit or "(none)"}

Satchidananda commentary (for context only — do not paraphrase wholesale):
{comm if comm else "(none extracted — rely on IAST)"}
"""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user},
    ]
    last_err = ""
    for attempt in range(4):
        if attempt > 0 and last_err:
            messages.append(
                {"role": "user", "content": f"Rejected: {last_err}. Return corrected JSON only."},
            )
        try:
            text = await smart_chat(messages, primary_model=model, temperature=0.35)
        except httpx.HTTPStatusError as e:
            if e.response.status_code in (429, 500, 502, 503, 504) and attempt < 3:
                await asyncio.sleep(min(60, 5 * (2**attempt)))
                last_err = f"HTTP {e.response.status_code}"
                continue
            raise
        try:
            data = _extract_json(text)
        except Exception as e:
            last_err = f"invalid JSON: {e}"
            continue
        commentary = str(data.get("commentary") or "").strip()
        commentary = re.sub(r"^Pratibha Commentary:\s*", "", commentary, flags=re.I)
        data["commentary"] = commentary
        if len(commentary.split()) < 150:
            last_err = f"commentary too short ({len(commentary.split())} words, need >=150)"
            continue
        return data
    raise ValueError(f"YS {pada}.{num} failed: {last_err}")


def iter_sutras(
    pada: int | None,
    start: tuple[int, int] | None,
    end: tuple[int, int] | None,
) -> list[tuple[int, int]]:
    keys: list[tuple[int, int]] = []
    padas = [pada] if pada else [1, 2, 3, 4]
    for p in padas:
        for n in range(1, PADA_COUNTS[p] + 1):
            keys.append((p, n))
    if start:
        keys = [k for k in keys if k >= start]
    if end:
        keys = [k for k in keys if k <= end]
    return keys


def parse_ref(ref: str) -> tuple[int, int]:
    m = re.match(r"(\d+)\.(\d+)", ref.strip())
    if not m:
        raise ValueError(f"expected pada.num like 1.1, got {ref!r}")
    return int(m.group(1)), int(m.group(2))


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", default=str(PDF_PATH))
    ap.add_argument("--gretil", default=str(GRETIL_PATH))
    ap.add_argument("--out", default=str(OUT_PATH))
    ap.add_argument("--pada", type=int, default=0, help="single pāda 1-4 (0 = all)")
    ap.add_argument("--start", default="", help="start sūtra e.g. 2.24")
    ap.add_argument("--end", default="", help="end sūtra e.g. 4.34")
    ap.add_argument("--all", action="store_true", help="generate all 195 sūtras")
    ap.add_argument("--dry-run", action="store_true", help="parse only, no LLM")
    ap.add_argument("--model", default="")
    ap.add_argument("--concurrency", type=int, default=1, help="parallel LLM calls (1 recommended)")
    args = ap.parse_args()

    from app.config import settings

    gretil = parse_gretil(Path(args.gretil))
    pdf_text = extract_pdf_text(Path(args.pdf))
    anchor_units = parse_satchidananda(pdf_text)

    print(f"GRETIL: {len(gretil)} sūtras")
    print(f"Satchidananda extracted: {len(anchor_units)} units")
    for p in range(1, 5):
        missing = [n for n in range(1, PADA_COUNTS[p] + 1) if (p, n) not in anchor_units]
        if missing:
            print(f"  Pada {p} missing PDF extract: {missing}")

    if args.dry_run:
        for p, n in [(1, 1), (2, 24), (3, 1), (4, 34)]:
            a = anchor_units.get((p, n))
            print(f"\nYS {p}.{n} IAST: {gretil.get((p, n), '?')}")
            if a:
                print(f"  aphorism: {a.aphorism[:120]}...")
                print(f"  commentary: {a.commentary[:120]}...")
        return

    start = parse_ref(args.start) if args.start else None
    end = parse_ref(args.end) if args.end else None
    if args.all:
        start, end = None, None
    elif not start and not end and args.pada:
        start, end = (args.pada, 1), (args.pada, PADA_COUNTS[args.pada])

    keys = iter_sutras(args.pada or None, start, end)
    if not keys:
        print("No sūtras selected.")
        return

    model = args.model or settings.DEFAULT_MODEL
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    existing = ""
    if out_path.exists() and out_path.stat().st_size > 0:
        existing = out_path.read_text(encoding="utf-8")
    elif not existing:
        out_path.write_text(HEADER, encoding="utf-8")

    sem = asyncio.Semaphore(max(1, args.concurrency))
    done = 0
    failed: list[str] = []

    async def one(pada: int, num: int) -> None:
        nonlocal done, existing
        tag = f"YS {pada}.{num}"
        marker = f"**Source:** Patañjali, Yoga Sūtras {pada}.{num}"
        if marker in existing:
            print(f"  [{tag}] skip (already in file)")
            return
        iast = gretil.get((pada, num))
        if not iast:
            failed.append(f"{tag}: no GRETIL IAST")
            return
        async with sem:
            try:
                data = await generate_unit(pada, num, iast, anchor_units.get((pada, num)), model)
                block = render_unit(pada, num, iast, anchor_units.get((pada, num)), data)
                with open(out_path, "a", encoding="utf-8") as f:
                    f.write(block)
                existing += block
                done += 1
                print(f"  [{tag}] OK — {data.get('title')}", flush=True)
            except Exception as e:
                failed.append(f"{tag}: {e}")
                print(f"  [{tag}] FAILED: {e}", flush=True)

    pending = [k for k in keys if f"**Source:** Patañjali, Yoga Sūtras {k[0]}.{k[1]}" not in existing]
    print(f"Generating {len(pending)} pending units (of {len(keys)} selected) with model {model} -> {out_path}", flush=True)
    if args.concurrency <= 1:
        for p, n in pending:
            await one(p, n)
    else:
        await asyncio.gather(*[one(p, n) for p, n in pending])
    print(f"\nDone. {done} written, {len(failed)} failed.")
    if failed:
        print("Failures:")
        for f in failed:
            print(f"  {f}")


if __name__ == "__main__":
    asyncio.run(main())
