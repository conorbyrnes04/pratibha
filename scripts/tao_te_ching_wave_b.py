#!/usr/bin/env python3
"""Generate Wave B Tao Te Ching units (chapters 3–81 minus Wave A) into the Pratibha manuscript.

Usage:
  python scripts/tao_te_ching_wave_b.py --dry-run
  python scripts/tao_te_ching_wave_b.py
  python scripts/tao_te_ching_wave_b.py --chapter 33
  python scripts/tao_te_ching_wave_b.py --no-llm   # scaffold only (not recommended)
  python scripts/tao_te_ching_wave_b.py --no-resume  # regenerate all Wave B chapters
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

MANUSCRIPT = ROOT / "data/raw_texts/#Lǎozǐ: Dào Dé Jīng 道德經"
LEGGE = ROOT / "data/raw_texts/pd/chinese/tao_te_ching_legge_gutenberg_216.txt"
CHECKPOINT = ROOT / "data/raw_texts/tao_te_ching_wave_b_checkpoint.json"
CTEXT_URL = "https://api.ctext.org/gettext?urn=ctp:dao-de-jing&format=json"

WAVE_A = {1, 2, 8, 11, 16, 25, 37, 40, 43, 48, 57, 63, 67, 76, 78}
WAVE_B_ALL = sorted(ch for ch in range(1, 82) if ch not in WAVE_A)

TTC_SYSTEM = """You are a Pratibha editor for Lǎozǐ's Dào Dé Jīng (Tao Te Ching). Return ONLY JSON:
{
  "title": "thematic English title (never 'Chapter N')",
  "body": "1-3 sentence lead-in in modern English (not a copy of Legge)",
  "pratibha_translation": "full chapter in fresh English; preserve dào, wúwéi, dé, zìrán in brackets with 汉字 on first key term",
  "commentary": "two paragraphs (~120-180 words). Open with a philosophical claim about this chapter. Name the contested move. Do not paraphrase the translation.",
  "key_terms": [{"term": "pinyin 汉字", "definition": "graph/meaning -> Daoist sense -> translation stakes"}],
  "resonances": [{"citation": "Author, work, passage", "resonance": "structural homology", "divergence": "where the parallel breaks"}],
  "practice": "one executable somatic or ethical instruction from THIS chapter"
}
Rules: 2-4 key_terms; 2-3 resonances each with divergence; no IAST; no § markers — cite other chapters as "chapter N (brief plain-English gloss)"; match Wave A density (shorter than ch.1 exemplar, richer than a stub). Return valid JSON only — no markdown fences."""


def fetch_chinese() -> list[str]:
    with urllib.request.urlopen(CTEXT_URL, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    chapters = data.get("fulltext") or []
    if len(chapters) != 81:
        raise RuntimeError(f"Expected 81 ctext chapters, got {len(chapters)}")
    return [str(c).strip() for c in chapters]


def parse_legge(path: Path) -> dict[int, str]:
    text = path.read_text(encoding="utf-8")
    chapters: dict[int, str] = {}
    current: int | None = None
    buf: list[str] = []
    for line in text.splitlines():
        m = re.match(r"^Ch\. (\d+)\.", line)
        m2 = re.match(r"^(\d+)\. 1\. ", line)
        if m:
            if current is not None:
                chapters[current] = "\n".join(buf).strip()
            current = int(m.group(1))
            buf = [line]
        elif m2 and 1 <= int(m2.group(1)) <= 81:
            if current is not None:
                chapters[current] = "\n".join(buf).strip()
            current = int(m2.group(1))
            buf = [line]
        elif current is not None:
            buf.append(line)
    if current is not None:
        chapters[current] = "\n".join(buf).strip()
    return chapters


def chapters_in_manuscript(text: str) -> set[int]:
    return {int(m.group(1)) for m in re.finditer(r"\*\*Source:\*\*.*?Chapter (\d+)", text)}


def format_chinese(text: str) -> str:
    text = re.sub(r"\s+", "", text)
    parts = re.split(r"(?<=[。；！？])", text)
    lines = [p.strip() for p in parts if p.strip()]
    return "\n".join(lines)


def md_unit(ch: int, chinese: str, payload: dict[str, Any]) -> str:
    title = str(payload.get("title", f"Chapter {ch}")).strip()
    body = str(payload.get("body", "")).strip()
    translation = str(payload.get("pratibha_translation", "")).strip()
    commentary = str(payload.get("commentary", "")).strip()
    practice = str(payload.get("practice", "")).strip()

    key_lines = []
    for item in payload.get("key_terms") or []:
        term = str(item.get("term", "")).strip()
        definition = re.sub(r"\s+", " ", str(item.get("definition", "")).strip())
        if term and definition:
            key_lines.append(f"**{term}** — {definition}")

    res_lines = []
    for item in payload.get("resonances") or []:
        citation = str(item.get("citation", "")).strip().strip("*")
        resonance = re.sub(r"\s+", " ", str(item.get("resonance", "")).strip())
        divergence = re.sub(r"\s+", " ", str(item.get("divergence", "")).strip())
        if citation and resonance:
            block = f"**{citation}:** {resonance}"
            if divergence:
                block += f" *Divergence:* {divergence}"
            res_lines.append(block)

    return f"""## {title}

**Source:** Lǎozǐ, *Dào Dé Jīng* 道德經, Chapter {ch}

{body}

---

### Original (Traditional Chinese)

{format_chinese(chinese)}

### Pratibhā Translation

{translation}

### Pratibhā Commentary

{commentary}

### Key Terms

{chr(10).join(key_lines)}

### Cross-Tradition Resonances

{chr(10).join(res_lines)}

### Practice (Abhyāsa)

{practice}

---
"""


def scaffold_unit(ch: int, chinese: str, legge: str) -> dict[str, Any]:
    lead = re.sub(r"\s+", " ", legge)[:280].strip()
    return {
        "title": f"Chapter {ch}",
        "body": lead,
        "pratibha_translation": lead,
        "commentary": (
            f"Chapter {ch} extends the *Dào Dé Jīng*'s teaching on alignment with the *dào*. "
            "Read against Legge as PD reference; Pratibha translation is the study voice."
        ),
        "key_terms": [{"term": "dào 道", "definition": "way, course, guiding pattern — operative norm of the chapter."}],
        "resonances": [
            {
                "citation": "Zhuangzi, inner chapters",
                "resonance": "shared Daoist suspicion of forced contrivance.",
                "divergence": "narrative parable vs aphoristic chapter.",
            }
        ],
        "practice": f"Read chapter {ch} aloud once, then sit in silence for two minutes before your next action.",
    }


def parse_llm_json(text: str) -> dict[str, Any]:
    """Extract and parse JSON from LLM output, tolerating fences and preamble."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
        text = re.sub(r"\s*```\s*$", "", text)

    # Direct parse first.
    try:
        payload = json.loads(text)
        if isinstance(payload, dict):
            return payload
    except json.JSONDecodeError:
        pass

    # Find outermost {...} block.
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        blob = text[start : end + 1]
        try:
            payload = json.loads(blob)
            if isinstance(payload, dict):
                return payload
        except json.JSONDecodeError:
            # Strip trailing commas before } or ]
            cleaned = re.sub(r",(\s*[}\]])", r"\1", blob)
            payload = json.loads(cleaned)
            if isinstance(payload, dict):
                return payload

    raise ValueError(f"Could not parse JSON from LLM response ({len(text)} chars)")


def _is_rate_limit(exc: Exception) -> bool:
    s = str(exc).lower()
    if "429" in s or "rate limit" in s or "too many requests" in s:
        return True
    status = getattr(exc, "response", None)
    if status is not None and getattr(status, "status_code", None) == 429:
        return True
    return False


def _validate_payload(payload: dict[str, Any]) -> None:
    for key in ("title", "body", "pratibha_translation", "commentary", "practice"):
        if not str(payload.get(key, "")).strip():
            raise ValueError(f"missing or empty {key}")


async def llm_unit(ch: int, chinese: str, legge: str, retries: int = 8) -> dict[str, Any]:
    from app.llm import smart_chat

    user = (
        f"Chapter {ch} of 81\n\n"
        f"Received Chinese (ctext):\n{chinese}\n\n"
        f"Legge (1889) PD reference — do NOT copy verbatim:\n{legge[:2500]}\n\n"
        "Write Pratibha layers at Wave A density."
    )
    last_exc: Exception | None = None
    for attempt in range(retries):
        try:
            text = await smart_chat(
                [{"role": "system", "content": TTC_SYSTEM}, {"role": "user", "content": user}],
                temperature=0.35,
            )
            payload = parse_llm_json(text)
            _validate_payload(payload)
            return payload
        except Exception as exc:
            last_exc = exc
            if attempt + 1 >= retries:
                break
            if _is_rate_limit(exc):
                wait = min(120, 15 * (2**attempt))
            elif isinstance(exc, (json.JSONDecodeError, ValueError)):
                wait = 4 * (attempt + 1)
            else:
                wait = 6 * (attempt + 1)
            print(f"  ch.{ch} attempt {attempt + 1}/{retries} failed ({exc}); retry in {wait}s...", flush=True)
            await asyncio.sleep(wait)
    raise last_exc or RuntimeError(f"LLM failed for chapter {ch}")


def load_checkpoint() -> dict[str, Any]:
    if CHECKPOINT.exists():
        try:
            return json.loads(CHECKPOINT.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {"completed": [], "failed": [], "scaffolded": []}


def save_checkpoint(state: dict[str, Any]) -> None:
    CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
    CHECKPOINT.write_text(json.dumps(state, indent=2), encoding="utf-8")


async def generate_and_append(
    chapters: list[int],
    chinese: list[str],
    legge: dict[int, str],
    use_llm: bool,
    delay_s: float,
    allow_scaffold: bool,
    dry_run: bool,
) -> tuple[list[int], list[int], list[int]]:
    """Generate chapters sequentially, appending each to the manuscript on success."""
    state = load_checkpoint()
    completed: list[int] = list(state.get("completed") or [])
    failed: list[int] = list(state.get("failed") or [])
    scaffolded: list[int] = list(state.get("scaffolded") or [])

    total = len(chapters)
    for i, ch in enumerate(chapters, 1):
        print(f"[{i}/{total}] generating ch.{ch}...", flush=True)
        payload: dict[str, Any] | None = None
        used_scaffold = False

        if use_llm:
            try:
                payload = await llm_unit(ch, chinese[ch - 1], legge.get(ch, ""))
            except Exception as exc:
                print(f"  LLM failed ch.{ch}: {exc}", flush=True)
                if allow_scaffold:
                    print(f"  using scaffold for ch.{ch}", flush=True)
                    payload = scaffold_unit(ch, chinese[ch - 1], legge.get(ch, ""))
                    used_scaffold = True
                    if ch not in scaffolded:
                        scaffolded.append(ch)
                else:
                    if ch not in failed:
                        failed.append(ch)
                    save_checkpoint({"completed": completed, "failed": failed, "scaffolded": scaffolded})
                    continue
        else:
            payload = scaffold_unit(ch, chinese[ch - 1], legge.get(ch, ""))
            used_scaffold = True
            if ch not in scaffolded:
                scaffolded.append(ch)

        block = md_unit(ch, chinese[ch - 1], payload)
        if dry_run:
            preview = ROOT / "data/raw_texts/tao_te_ching_wave_b_preview.md"
            mode = "a" if preview.exists() and i > 1 else "w"
            with preview.open(mode, encoding="utf-8") as f:
                if mode == "w":
                    f.write(f"# Wave B preview — {total} chapters\n\n")
                f.write(block + "\n")
            print(f"  dry-run wrote ch.{ch} to preview", flush=True)
        else:
            existing = MANUSCRIPT.read_text(encoding="utf-8") if MANUSCRIPT.exists() else ""
            existing = strip_footer(existing)
            MANUSCRIPT.write_text(existing + "\n" + block, encoding="utf-8")
            print(f"  appended ch.{ch} to manuscript", flush=True)

        if ch not in completed:
            completed.append(ch)
        if ch in failed:
            failed.remove(ch)
        save_checkpoint({"completed": completed, "failed": failed, "scaffolded": scaffolded})

        if delay_s > 0 and i < total:
            await asyncio.sleep(delay_s)

    return completed, failed, scaffolded


def strip_footer(text: str) -> str:
    return re.sub(
        r"\*Pratibhā corpus entry — Lǎozǐ.*?\*(\n\*.*?\*)?",
        "",
        text,
        flags=re.S,
    ).rstrip()


def update_footer(text: str) -> str:
    present = chapters_in_manuscript(text)
    wave_b_done = sorted(present - WAVE_A)
    wave_a_done = sorted(present & WAVE_A)
    footer = (
        f"*Pratibhā corpus entry — Lǎozǐ, Dào Dé Jīng 道德經 — "
        f"Wave A ({len(wave_a_done)} units) + Wave B ({len(wave_b_done)} units) = {len(present)} chapters*"
    )
    return strip_footer(text) + f"\n\n{footer}\n"


def run_pipeline() -> None:
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/tao_te_ching_md_to_yaml.py"),
            str(MANUSCRIPT),
            str(ROOT / "data/yaml/tao_te_ching"),
        ],
        check=True,
        cwd=ROOT,
    )
    subprocess.run([sys.executable, str(ROOT / "scripts/canonicalize_texts.py")], check=True, cwd=ROOT)


async def main_async(args: argparse.Namespace) -> int:
    chinese = fetch_chinese()
    legge = parse_legge(LEGGE)
    wave_b = list(WAVE_B_ALL)

    if args.chapter:
        if args.chapter in WAVE_A:
            print(f"Chapter {args.chapter} is Wave A (already curated).")
            return 1
        wave_b = [args.chapter]
    elif args.resume and MANUSCRIPT.exists() and not args.dry_run:
        present = chapters_in_manuscript(MANUSCRIPT.read_text(encoding="utf-8"))
        wave_b = [ch for ch in wave_b if ch not in present]
        if wave_b:
            print(f"Resume: skipping {len(present)} chapters already in manuscript")
        else:
            print("All Wave B chapters already present in manuscript.")

    if not wave_b:
        if not args.dry_run and MANUSCRIPT.exists():
            text = update_footer(MANUSCRIPT.read_text(encoding="utf-8"))
            MANUSCRIPT.write_text(text, encoding="utf-8")
            if args.canonicalize:
                run_pipeline()
                print("YAML + canonical updated.")
        return 0

    print(f"Wave B: generating {len(wave_b)} chapters (ch.{wave_b[0]}–{wave_b[-1]})")

    completed, failed, scaffolded = await generate_and_append(
        wave_b,
        chinese,
        legge,
        use_llm=not args.no_llm,
        delay_s=args.delay,
        allow_scaffold=args.allow_scaffold,
        dry_run=args.dry_run,
    )

    if args.dry_run:
        print(f"Dry run complete: {len(completed)} units previewed")
        if failed:
            print(f"Failed: {failed}")
        return 1 if failed else 0

    text = MANUSCRIPT.read_text(encoding="utf-8")
    MANUSCRIPT.write_text(update_footer(text), encoding="utf-8")
    present = chapters_in_manuscript(MANUSCRIPT.read_text(encoding="utf-8"))
    print(f"Manuscript now has {len(present)}/81 chapters")
    if scaffolded:
        print(f"Scaffolded (LLM fallback): {sorted(scaffolded)}")
    if failed:
        print(f"Failed (not written): {sorted(failed)}")
        return 1

    if args.canonicalize:
        run_pipeline()
        print("YAML + canonical updated.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate Tao Te Ching Wave B manuscript units.")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-llm", action="store_true", help="Scaffold without LLM (structural only)")
    ap.add_argument("--allow-scaffold", action="store_true", help="Fall back to scaffold on LLM failure")
    ap.add_argument("--chapter", type=int, help="Generate a single chapter")
    ap.add_argument("--concurrency", type=int, default=1, help="Ignored — always sequential for reliability")
    ap.add_argument("--delay", type=float, default=3.0, help="Seconds between chapters (rate-limit cushion)")
    ap.add_argument("--resume", action="store_true", default=True, help="Skip chapters already in manuscript")
    ap.add_argument("--no-resume", action="store_true", help="Regenerate even if chapter exists")
    ap.add_argument("--canonicalize", action="store_true", default=True)
    ap.add_argument("--no-canonicalize", action="store_true")
    args = ap.parse_args()
    if args.no_canonicalize:
        args.canonicalize = False
    if args.no_resume:
        args.resume = False
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    raise SystemExit(main())
