#!/usr/bin/env python3
"""Author publishable commentary + practice for Vijñāna Bhairava units via Claude.

The Vijñāna Bhairava Tantra is 112 meditation techniques (dhāraṇā/yukti). In the
corpus these units carry the actual verse (translation_literal) but only template
filler for commentary/practice. This script generates real editorial commentary
and a concrete, doable practice for each, grounded in that unit's own verse, then
stamps the unit `publishable`.

Design:
- OpenRouter-only, via the app's configured model (Claude Haiku 4.5 by default).
- One structured JSON call per unit → {commentary, practice, key_terms}.
- Idempotent: skips units that already have authored commentary.
- Gated: a unit is only stamped `publishable` if the model returns substantial
  commentary AND a specific (non-generic) practice; otherwise it's left as-is.
- `pratibha_layers` is dropped so the loader re-derives layers from new fields.

Usage:
    python scripts/author_vijnana_bhairava.py --limit 2            # proof, no write
    python scripts/author_vijnana_bhairava.py --limit 2 --write    # write 2
    python scripts/author_vijnana_bhairava.py --write              # full run
"""
from __future__ import annotations

import argparse
import asyncio
import glob
import json
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import settings  # noqa: E402
from app.llm import smart_chat  # noqa: E402
from app.data_loader import _commentary_is_authored, _practice_is_generic  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VB_DIR = os.path.join(ROOT, "data", "canonical", "vijnana_bhairava")

AUTHOR_SYSTEM = """You are the editorial voice of Pratibhā, a serious multi-tradition wisdom study platform. You write publishable study commentary on the Vijñāna Bhairava Tantra — a Kashmir Śaiva text of 112 meditation techniques (dhāraṇā). Each technique is a precise instruction for entering expanded awareness (bhairava-consciousness).

Your commentary must:
- Be grounded in THIS specific verse — its concrete instruction, image, and the faculty it works on (breath, space, sound, gaze, the gap between thoughts, etc.). Never generic spirituality.
- Explain what the technique actually does and why it works in the Trika/Kashmir Śaiva framework (e.g. madhya/the central channel, the gap between two breaths, the collapse of subject-object, spanda/vibration, the pervasion of consciousness).
- Be direct and unhurried, warm but rigorous — the register of a scholar who also practices. No hedging, no throat-clearing, no "this passage invites us to."
- Name the source-language terms where they illuminate (with brief gloss), but do not pad with untranslated Sanskrit.
- Run roughly 900–1600 characters. Substance over length.

The practice must be one concrete, doable instruction a modern reader can actually attempt today, drawn directly from the technique in the verse — not "read this slowly three times."

Return ONLY valid JSON, no prose around it:
{"commentary": "...", "practice": "...", "key_terms": [{"term": "...", "definition": "..."}]}
key_terms: 1–3 genuinely relevant source-language terms with a one-line gloss each. Omit the field or use [] if none add value."""


def _verse_text(item: dict) -> str:
    for key in ("translation_literal", "translation"):
        v = item.get(key)
        if isinstance(v, str) and v.strip() and v.strip() != "None":
            return v.strip()
    return ""


def _needs_authoring(item: dict) -> bool:
    return not _commentary_is_authored(str(item.get("commentary") or ""))


def _extract_json(text: str) -> dict | None:
    text = text.strip()
    # Strip code fences if present.
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.M).strip()
    try:
        return json.loads(text)
    except Exception:
        m = re.search(r"\{.*\}", text, re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                return None
    return None


async def author_unit(item: dict) -> dict | None:
    verse = _verse_text(item)
    if not verse:
        return None
    title = str(item.get("title") or item.get("unit_label") or "").strip()
    themes = item.get("themes")
    theme_str = ", ".join(themes) if isinstance(themes, list) else ""
    user = (
        f"Verse: {title}\n\n"
        f"Technique (translation):\n{verse}\n\n"
        f"Themes: {theme_str or 'n/a'}\n\n"
        "Write the study commentary, practice, and key_terms for this technique as JSON."
    )
    msgs = [
        {"role": "system", "content": AUTHOR_SYSTEM},
        {"role": "user", "content": user},
    ]
    # Author commentary wants more room than chat's default cap.
    text = await smart_chat(msgs, temperature=0.55, max_tokens=1600)
    data = _extract_json(text)
    if not isinstance(data, dict):
        return None
    return data


def _gate(commentary: str, practice: str) -> tuple[bool, str]:
    if not _commentary_is_authored(commentary):
        return False, "commentary too thin"
    if not practice or _practice_is_generic(practice) or len(practice.strip()) < 40:
        return False, "practice missing/generic"
    return True, "ok"


def _key_terms_tail(key_terms) -> str:
    if not isinstance(key_terms, list) or not key_terms:
        return ""
    lines = ["", "Key Terms", ""]
    for kt in key_terms[:3]:
        if isinstance(kt, dict) and kt.get("term") and kt.get("definition"):
            lines.append(f"**{str(kt['term']).strip()}** — {str(kt['definition']).strip()}")
    return "\n".join(lines) if len(lines) > 3 else ""


def write_unit(path: str, item: dict, authored: dict) -> str:
    commentary = str(authored.get("commentary") or "").strip()
    practice = str(authored.get("practice") or "").strip()
    ok, reason = _gate(commentary, practice)
    if not ok:
        return f"deferred ({reason})"
    tail = _key_terms_tail(authored.get("key_terms"))
    full_commentary = (commentary + ("\n" + tail if tail else "")).strip()
    item = dict(item)
    item["commentary"] = full_commentary
    item["practice"] = practice
    item["abhyasa"] = practice
    item["editorial_maturity"] = "publishable"
    item.pop("pratibha_layers", None)  # let the loader re-derive from new fields
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(item, f, allow_unicode=True, sort_keys=False, width=100)
    return "authored"


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="max units to process (0 = all)")
    ap.add_argument("--write", action="store_true", help="write files (default: preview)")
    args = ap.parse_args()

    if not settings.OPENROUTER_API_KEY:
        print("ERROR: OPENROUTER_API_KEY not set (source your .env first).")
        sys.exit(1)

    files = sorted(glob.glob(os.path.join(VB_DIR, "**", "*.yml"), recursive=True))
    todo = []
    for path in files:
        item = yaml.safe_load(open(path, encoding="utf-8"))
        if isinstance(item, dict) and _needs_authoring(item):
            todo.append((path, item))
    if args.limit:
        todo = todo[: args.limit]
    print(f"Vijñāna Bhairava: {len(files)} files, {len(todo)} need authoring "
          f"({'WRITE' if args.write else 'preview'}), model={settings.effective_default_model()}\n")

    counts: dict[str, int] = {}
    for i, (path, item) in enumerate(todo, 1):
        name = os.path.basename(path)
        try:
            authored = await author_unit(item)
        except Exception as e:
            print(f"[{i}/{len(todo)}] {name}: ERROR {e!r}")
            counts["error"] = counts.get("error", 0) + 1
            continue
        if not authored:
            print(f"[{i}/{len(todo)}] {name}: no JSON returned")
            counts["no_json"] = counts.get("no_json", 0) + 1
            continue
        commentary = str(authored.get("commentary") or "").strip()
        practice = str(authored.get("practice") or "").strip()
        if args.write:
            result = write_unit(path, item, authored)
        else:
            ok, reason = _gate(commentary, practice)
            result = "would author" if ok else f"would defer ({reason})"
            print(f"[{i}/{len(todo)}] {name}: {result}")
            print(f"    COMMENTARY ({len(commentary)}c): {commentary[:260]}...")
            print(f"    PRACTICE: {practice[:180]}\n")
        counts[result.split(' (')[0]] = counts.get(result.split(' (')[0], 0) + 1

    print("\nSUMMARY:", ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))


if __name__ == "__main__":
    asyncio.run(main())
