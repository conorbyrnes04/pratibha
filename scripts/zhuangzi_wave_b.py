#!/usr/bin/env python3
"""Generate Wave B Zhuangzi teaching units (chapters 16-33) into the Pratibha manuscript.

Usage:
  python scripts/zhuangzi_wave_b.py --dry-run
  python scripts/zhuangzi_wave_b.py
  python scripts/zhuangzi_wave_b.py --chapter 16
  python scripts/zhuangzi_wave_b.py --no-llm
  python scripts/zhuangzi_wave_b.py --no-resume
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.zhuangzi_chinese import CHAPTER_NAMES, fetch_all, format_chinese, parse_giles

MANUSCRIPT = ROOT / "data/raw_texts/#Zhuangzi_pratibha_manuscript.md"
CHECKPOINT = ROOT / "data/raw_texts/zhuangzi_wave_b_checkpoint.json"

WAVE_A = set(range(1, 16))
WAVE_B_ALL = list(range(16, 34))

ZHUANGZI_SYSTEM = """You are a Pratibha editor for Zhuangzi (*Nanhua Jing*). Return ONLY JSON:
{
  "title": "thematic English title (never 'Chapter N')",
  "body": "2-4 sentence lead-in in modern English for ONE focal passage - not a verbatim Giles copy",
  "pratibha_translation": "focused excerpt only (4-10 sentences) of the chapter's central teaching - NOT the full chapter",
  "commentary": "two short paragraphs (~80-120 words total). Open with a philosophical claim. Name the contested move.",
  "key_terms": [{"term": "pinyin hanzi", "definition": "graph/meaning -> Zhuangzi sense -> translation stakes"}],
  "resonances": [{"citation": "Author, work, passage", "resonance": "structural homology", "divergence": "where the parallel breaks"}],
  "practice": "one executable somatic or ethical instruction from THIS passage"
}
Rules: 2-4 key_terms; 2-3 resonances with divergence; no IAST; escape all quotes inside JSON strings; keep total JSON under 3500 characters; match Wave A excerpt density (one teaching movement per unit). Return valid JSON only - no markdown fences."""


def md_unit(ch: int, chinese: str, giles_title: str, payload: dict[str, Any]) -> str:
    title = str(payload.get("title", f"Chapter {ch}")).strip()
    body = str(payload.get("body", "")).strip()
    translation = str(payload.get("pratibha_translation", "")).strip()
    commentary = str(payload.get("commentary", "")).strip()
    practice = str(payload.get("practice", "")).strip()
    cn = CHAPTER_NAMES.get(ch, "")

    key_lines = []
    for item in payload.get("key_terms") or []:
        term = str(item.get("term", "")).strip()
        definition = re.sub(r"\s+", " ", str(item.get("definition", "")).strip())
        if term and definition:
            key_lines.append(f"**{term}** - {definition}")

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
**Source:** Zhuangzi, Chapter {ch} (*{cn}*, "{giles_title}")

{body}

---

### Original
{format_chinese(chinese)}

### IAST
*(Chinese source text; no Sanskrit original. Pinyin with tones for key terms is provided in Key Terms.)*

### Pratibha Translation
{translation}

### Pratibha Commentary
{commentary}

### Key Terms
{chr(10).join(key_lines)}

### Cross-Tradition Resonances
{chr(10).join(res_lines)}

### Practice (Abhyasa)
{practice}

---
"""


def scaffold_unit(ch: int, chinese: str, giles: str, giles_title: str) -> dict[str, Any]:
    lead = re.sub(r"\s+", " ", giles)[:320].strip()
    cn = CHAPTER_NAMES.get(ch, "")
    return {
        "title": f"{giles_title} ({cn})",
        "body": lead,
        "pratibha_translation": lead,
        "commentary": (
            f"Chapter {ch} (*{cn}*) extends Zhuangzi's critique of forced cultivation and scale-locked judgment. "
            "Read against Giles as PD reference; Pratibha translation is the study voice."
        ),
        "key_terms": [{"term": "dao", "definition": "way, course - operative norm of the chapter."}],
        "resonances": [
            {
                "citation": "Laozi, Dao De Jing",
                "resonance": "shared suspicion of contrived virtue and ornamental ritual.",
                "divergence": "Zhuangzi narrates through parable; Laozi compresses into aphorism.",
            }
        ],
        "practice": f"Read chapter {ch} aloud once, then sit in silence for two minutes before your next action.",
    }


def parse_llm_json(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
        text = re.sub(r"\s*```\s*$", "", text)
    try:
        payload = json.loads(text)
        if isinstance(payload, dict):
            return payload
    except json.JSONDecodeError:
        pass
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        blob = text[start : end + 1]
        try:
            return json.loads(blob)
        except json.JSONDecodeError:
            cleaned = re.sub(r",(\s*[}\]])", r"\1", blob)
            return json.loads(cleaned)
    raise ValueError(f"Could not parse JSON from LLM response ({len(text)} chars)")


def _is_rate_limit(exc: Exception) -> bool:
    s = str(exc).lower()
    return "429" in s or "rate limit" in s or "too many requests" in s


def _validate_payload(payload: dict[str, Any]) -> None:
    for key in ("title", "body", "pratibha_translation", "commentary", "practice"):
        if not str(payload.get(key, "")).strip():
            raise ValueError(f"missing or empty {key}")


async def llm_unit(ch: int, chinese: str, giles: str, giles_title: str, retries: int = 8) -> dict[str, Any]:
    from app.llm import chat_completion, settings

    cn = CHAPTER_NAMES.get(ch, "")
    user = (
        f"Chapter {ch} of 33 - {cn} ({giles_title})\n\n"
        f"Received Chinese (Haodoo traditional text, excerpt):\n{chinese[:1200]}\n\n"
        f"Giles (1889) PD reference - do NOT copy verbatim:\n{giles[:1500]}\n\n"
        "Select ONE focal passage and write Pratibha layers at Wave A Zhuangzi density."
    )
    last_exc: Exception | None = None
    for attempt in range(retries):
        try:
            model = settings.effective_default_model()
            r = await chat_completion(
                [{"role": "system", "content": ZHUANGZI_SYSTEM}, {"role": "user", "content": user}],
                model,
                temperature=0.35,
                max_tokens=2000,
            )
            data = r.json()
            text = data["choices"][0]["message"]["content"].strip()
            payload = parse_llm_json(text)
            _validate_payload(payload)
            return payload
        except Exception as exc:
            last_exc = exc
            if attempt + 1 >= retries:
                break
            wait = min(120, 15 * (2**attempt)) if _is_rate_limit(exc) else 4 * (attempt + 1)
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


def chapters_in_manuscript(text: str) -> set[int]:
    return {int(m.group(1)) for m in re.finditer(r"\*\*Source:\*\* Zhuangzi, Chapter (\d+)", text)}


def strip_footer(text: str) -> str:
    return re.sub(
        r"\*Pratibha corpus entry - Zhuangzi.*?\*(\n\*.*?\*)?",
        "",
        text,
        flags=re.S,
    ).rstrip()


def update_footer(text: str) -> str:
    present = chapters_in_manuscript(text)
    wave_a = sorted(present & WAVE_A)
    wave_b = sorted(present - WAVE_A)
    footer = (
        f"*Pratibha corpus entry - Zhuangzi ({len(wave_a)} Wave A + {len(wave_b)} Wave B = {len(present)} units)*\n"
        f"*Wave A: chapters {', '.join(str(c) for c in wave_a)}; Wave B: chapters {', '.join(str(c) for c in wave_b)}*"
    )
    return strip_footer(text) + f"\n\n{footer}\n"


async def generate_and_append(
    chapters: list[int],
    chinese: dict[int, str],
    giles: dict[int, dict[str, str]],
    use_llm: bool,
    delay_s: float,
    allow_scaffold: bool,
    dry_run: bool,
    resume: bool,
) -> tuple[list[int], list[int], list[int]]:
    state = load_checkpoint()
    completed: list[int] = list(state.get("completed") or [])
    failed: list[int] = list(state.get("failed") or [])
    scaffolded: list[int] = list(state.get("scaffolded") or [])

    if resume:
        chapters = [ch for ch in chapters if ch not in completed]

    total = len(chapters)
    for i, ch in enumerate(chapters, 1):
        print(f"[{i}/{total}] generating ch.{ch}...", flush=True)
        g = giles.get(ch, {})
        giles_body = g.get("body", "")
        giles_title = g.get("title", f"Chapter {ch}")
        zh = chinese.get(ch, "")
        payload: dict[str, Any] | None = None

        if use_llm:
            try:
                payload = await llm_unit(ch, zh, giles_body, giles_title)
            except Exception as exc:
                print(f"  LLM failed ch.{ch}: {exc}", flush=True)
                if allow_scaffold:
                    payload = scaffold_unit(ch, zh, giles_body, giles_title)
                    if ch not in scaffolded:
                        scaffolded.append(ch)
                else:
                    if ch not in failed:
                        failed.append(ch)
                    save_checkpoint({"completed": completed, "failed": failed, "scaffolded": scaffolded})
                    continue
        else:
            payload = scaffold_unit(ch, zh, giles_body, giles_title)
            if ch not in scaffolded:
                scaffolded.append(ch)

        block = md_unit(ch, zh, giles_title, payload)
        if dry_run:
            preview = ROOT / "data/raw_texts/zhuangzi_wave_b_preview.md"
            mode = "a" if preview.exists() and i > 1 else "w"
            with preview.open(mode, encoding="utf-8") as f:
                if mode == "w":
                    f.write(f"# Zhuangzi Wave B preview - {total} chapters\n\n")
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


def run_pipeline() -> None:
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/zhuangzi_pratibha_md_to_yaml.py"),
            str(MANUSCRIPT),
            str(ROOT / "data/yaml/zhuangzi_pratibha"),
        ],
        check=True,
        cwd=ROOT,
    )
    subprocess.run([sys.executable, str(ROOT / "scripts/canonicalize_texts.py")], check=True, cwd=ROOT)


async def main_async(args: argparse.Namespace) -> int:
    chinese = fetch_all()
    giles = parse_giles()
    wave_b = list(WAVE_B_ALL)

    if args.chapter:
        if args.chapter in WAVE_A:
            print(f"Chapter {args.chapter} is Wave A (already curated).")
            return 1
        wave_b = [args.chapter]

    if args.no_resume:
        save_checkpoint({"completed": [], "failed": [], "scaffolded": []})

    completed, failed, scaffolded = await generate_and_append(
        wave_b,
        chinese,
        giles,
        use_llm=not args.no_llm,
        delay_s=args.delay,
        allow_scaffold=not args.strict,
        dry_run=args.dry_run,
        resume=not args.no_resume,
    )

    if not args.dry_run and completed:
        text = MANUSCRIPT.read_text(encoding="utf-8")
        MANUSCRIPT.write_text(update_footer(text), encoding="utf-8")
        if args.pipeline:
            print("Running yaml + canonicalize pipeline...", flush=True)
            run_pipeline()

    print(f"Done: {len(completed)} completed, {len(failed)} failed, {len(scaffolded)} scaffolded", flush=True)
    return 0 if not failed else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Zhuangzi Wave B generator (chapters 16-33)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-llm", action="store_true")
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument("--strict", action="store_true", help="Do not fall back to scaffold on LLM failure")
    parser.add_argument("--chapter", type=int)
    parser.add_argument("--delay", type=float, default=2.0)
    parser.add_argument("--pipeline", action="store_true", help="Run md_to_yaml + canonicalize after generation")
    args = parser.parse_args()
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    raise SystemExit(main())
