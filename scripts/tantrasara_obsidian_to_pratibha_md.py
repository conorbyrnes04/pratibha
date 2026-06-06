"""Convert Obsidian Tantrasāra chapters (Śastra vault) → Pratibha MD.

Source: /Users/conorbyrnes04/Documents/Śastra/𐃪 Tantrasāra Ch. {1-5}.md

Usage:
  python scripts/tantrasara_obsidian_to_pratibha_md.py
  python scripts/tantrasara_obsidian_to_pratibha_md.py --with-resonances
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

VAULT = Path("/Users/conorbyrnes04/Documents/Śastra")
OUT = ROOT / "data/pratibha_md/tantrasara.md"

CHAPTER_FILES = [
    (1, "प्रथमह्निकम् · Prathamamāhnikam", "The Nature of Ignorance and the Light of Śiva"),
    (2, "द्वितीयमाह्निकम् · Dvitīyamāhnikam", "Anupāyaprakāśanam · The Revelation of the Pathless Path"),
    (3, "तृतीयमाह्निकम् · Tṛtīyamāhnikam", "Śāmbhavopāyaprakāśanam · The Revelation of the Śāmbhava Path"),
    (4, "चतुर्थमाह्निकम् · Caturthamāhnikam", "Śāktopāyaprakāśanam · The Revelation of the Śakti Path"),
    (5, "पञ्चममाह्निकम् · Pañcamamāhnikam", "Āṇavaprakāśanam · The Revelation of the Āṇava Path"),
]

UNIT_MARKERS = re.compile(
    r"(?m)^## (?:"
    r"Verse \d+"
    r"|Prose Section(?: \d+)?"
    r"|Upodghātaḥ"
    r"|Dhyāna Section"
    r"|Uccāra Section"
    r"|Varṇa Section"
    r"|Closing Distich[^\n]*"
    r")\s*$"
)

HEADER = """# Tantrasāra — Abhinavagupta

**Edition basis:** Abhinavagupta, *Tantrasāra*; English layers from Conor's Śastra vault manuscripts (Wallis/Padoux-informed translations), Sanskrit from received text.

**Translation decisions:**
- `Body` and `Pratibha Translation` reproduce the vault translation verbatim (anchor rendering).
- `### Devanagari` is source-verified from vault `Sanskrit` sections.
- `Pratibha Commentary` is the vault commentary, claim-led where present; traditional Abhinava material integrated where the vault provides it.
- Cross-tradition resonances generated per Pratibha editorial standard where `--with-resonances` is used.

Five āhnikas (daily sections), segmented by verse and prose teaching units.

---
"""

RESONANCE_PROMPT = """Return ONLY JSON: {"resonances":[{"citation":"Tradition/Author, Text, Passage","resonance":"structural homology","divergence":"where parallel breaks"}]}
Provide 2-3 resonances for this Abhinavagupta Tantrasāra unit. Structural homology required."""


def _clean(s: str) -> str:
    s = s.replace("\r\n", "\n").strip()
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s


def _strip_voice(label: str) -> str:
    return re.sub(r"\s*\(Voice \d+[^)]*\)", "", label).strip()


def _parse_glossary(block: str) -> str:
    if not block.strip():
        return ""
    entries: list[str] = []
    chunks = re.split(r"\n(?=\*\*)", block.strip())
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk.startswith("**"):
            continue
        m = re.match(r"\*\*([^*]+)\*\*", chunk)
        if not m:
            continue
        term = m.group(1).strip()
        body = chunk[m.end() :].strip()
        deva = iast = gloss = ""
        for line in body.splitlines():
            line = line.strip().lstrip("- ").strip()
            if line.startswith("Devanāgarī:"):
                deva = line.split(":", 1)[1].strip()
            elif line.startswith("IAST:"):
                iast = line.split(":", 1)[1].strip()
            elif line.startswith("Gloss:"):
                gloss = line.split(":", 1)[1].strip()
            elif line.startswith("Meaning:") and not gloss:
                gloss = line.split(":", 1)[1].strip()
        script = deva or iast
        entry = gloss or "see Tantrasāra context"
        if script:
            entries.append(f"**{term} ({script})** — {entry}")
        else:
            entries.append(f"**{term}** — {entry}")
    return "\n\n".join(entries)


def _extract_sections(block: str) -> dict[str, str]:
    out: dict[str, str] = {}
    pat = re.compile(r"(?m)^#{3,4}\s+(.+?)\s*$")
    matches = list(pat.finditer(block))
    for i, m in enumerate(matches):
        key = _strip_voice(m.group(1)).lower()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(block)
        out[key] = _clean(block[start:end])
    return out


def _pick(sections: dict[str, str], *names: str) -> str:
    for name in names:
        for k, v in sections.items():
            if name in k:
                return v
    return ""


def _unit_label(header_line: str) -> str:
    return header_line.replace("## ", "").strip()


def _thematic_title(block: str, fallback: str) -> str:
    m = re.search(r"(?m)^###\s+(.+?)\s*$", block)
    if m:
        return _strip_voice(m.group(1))
    return fallback


def parse_chapter(path: Path, chapter: int, chapter_title: str) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    units: list[dict] = []
    markers = list(UNIT_MARKERS.finditer(text))
    for i, m in enumerate(markers):
        start = m.start()
        end = markers[i + 1].start() if i + 1 < len(markers) else len(text)
        block = text[start:end]
        label = _unit_label(m.group(0))
        title = _thematic_title(block, label)
        sections = _extract_sections(block)
        sanskrit = _pick(sections, "sanskrit")
        iast = _pick(sections, "transliteration", "iast")
        translation = _pick(sections, "translation")
        commentary = _pick(sections, "commentary")
        practice = _pick(sections, "practice")
        glossary = _pick(sections, "glossary")
        if not translation and not sanskrit:
            continue
        units.append(
            {
                "chapter": chapter,
                "chapter_title": chapter_title,
                "label": label,
                "title": title,
                "sanskrit": sanskrit,
                "iast": iast,
                "body": translation or iast,
                "translation": translation,
                "commentary": commentary,
                "practice": practice,
                "key_terms": _parse_glossary(glossary),
                "resonances": "",
            }
        )
    return units


def render_unit(u: dict) -> str:
    src = f"Abhinavagupta, Tantrasāra, Āhnika {u['chapter']} ({u['label']})"
    deva_note = ""
    deva = u["sanskrit"]
    if not deva:
        deva_note = "*(not in source)*\n\n"
    return "\n".join(
        [
            f"## {u['title']}",
            f"**Source:** {src}",
            "",
            u["body"],
            "",
            "### Devanagari",
            deva_note + deva if deva else deva_note.strip(),
            "",
            "### IAST",
            "",
            u["iast"],
            "",
            "### Pratibha Translation",
            "",
            u["translation"] or u["body"],
            "",
            "### Pratibha Commentary",
            "",
            u["commentary"] or "(commentary pending)",
            "",
            "### Key Terms",
            "",
            u["key_terms"] or "",
            "",
            "### Cross-Tradition Resonances",
            "",
            u["resonances"] or "",
            "",
            "### Practice (Abhyasa)",
            "",
            u["practice"] or "",
            "",
            "---",
            "",
        ]
    )


async def add_resonances(units: list[dict], model: str) -> None:
    from app.llm import smart_chat

    for u in units:
        if u["resonances"]:
            continue
        prompt = (
            f"{RESONANCE_PROMPT}\n\n"
            f"Unit: {u['title']}\nChapter: {u['chapter']}\n"
            f"Passage:\n{u['body'][:2000]}\n\n"
            f"Commentary excerpt:\n{u['commentary'][:1500]}"
        )
        for attempt in range(5):
            try:
                raw = await smart_chat(
                    [{"role": "user", "content": prompt}],
                    primary_model=model,
                    temperature=0.35,
                )
                start, end = raw.find("{"), raw.rfind("}")
                data = json.loads(raw[start : end + 1])
                lines = []
                for r in data.get("resonances") or []:
                    if not isinstance(r, dict):
                        continue
                    line = f"**{r.get('citation', '').strip()}:** {r.get('resonance', '').strip()}"
                    div = str(r.get("divergence") or "").strip()
                    if div:
                        line += f"\n*Divergence:* {div}"
                    lines.append(line)
                u["resonances"] = "\n\n".join(lines)
                print(f"  resonances OK: {u['title']}", flush=True)
                break
            except httpx.HTTPStatusError as e:
                if e.response.status_code in (429, 500, 502, 503, 504) and attempt < 4:
                    await asyncio.sleep(min(60, 5 * (2**attempt)))
                    continue
                print(f"  resonances FAILED {u['title']}: {e}", flush=True)
                break
            except Exception as e:
                if attempt < 4:
                    await asyncio.sleep(2)
                    continue
                print(f"  resonances FAILED {u['title']}: {e}", flush=True)
        await asyncio.sleep(2)


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", default=str(VAULT))
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--with-resonances", action="store_true")
    ap.add_argument("--model", default="")
    args = ap.parse_args()

    vault = Path(args.vault)
    all_units: list[dict] = []
    for num, _mahnika, subtitle in CHAPTER_FILES:
        path = vault / f"𐃪 Tantrasāra Ch. {num}.md"
        if not path.exists():
            raise FileNotFoundError(path)
        units = parse_chapter(path, num, subtitle)
        print(f"Chapter {num}: {len(units)} units")
        all_units.extend(units)

    if args.with_resonances:
        from app.config import settings

        model = args.model or settings.DEFAULT_MODEL
        print(f"Generating resonances for {len(all_units)} units ({model})...")
        await add_resonances(all_units, model)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(HEADER + "".join(render_unit(u) for u in all_units), encoding="utf-8")
    print(f"Wrote {len(all_units)} units → {out}")


if __name__ == "__main__":
    asyncio.run(main())
