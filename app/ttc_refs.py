"""Replace academic §N chapter markers with plain-language cross-references."""

from __future__ import annotations

import re
from typing import Any

# Short glosses for chapters that cross-reference each other often in Wave A.
TTC_CHAPTER_GLOSS: dict[int, str] = {
    1: "chapter 1 (the Way that cannot be fully named)",
    2: "chapter 2 (beauty and ugliness arising together)",
    8: "chapter 8 (the highest good is like water)",
    11: "chapter 11 (the empty hub at the center of the wheel)",
    16: "chapter 16 (all things arise and return to the root)",
    25: "chapter 25 (something formless before heaven and earth)",
    33: "chapter 33 (knowing others and knowing yourself)",
    37: "chapter 37 (non-action, nothing left undone)",
    40: "chapter 40 (the Way moves by reversal)",
    43: "chapter 43 (the soft enters where nothing can)",
    48: "chapter 48 (the Way subtracts; learning adds)",
    57: "chapter 57 (govern by not governing)",
    63: "chapter 63 (do the great while it is still small)",
    67: "chapter 67 (the three treasures)",
    76: "chapter 76 (living is soft, death is hard)",
    78: "chapter 78 (water overcomes hardness; true words seem backward)",
    81: "chapter 81 (the book's closing paradox)",
}


def chapter_phrase(chapter: int) -> str:
    return TTC_CHAPTER_GLOSS.get(chapter, f"chapter {chapter}")


def humanize_ttc_refs(text: str) -> str:
    """Turn §78-style markers into readable chapter references."""
    if not text or "§" not in text:
        return text

    def possessive(match: re.Match[str]) -> str:
        n = int(match.group(1))
        short = TTC_CHAPTER_GLOSS.get(n, f"chapter {n}")
        # Drop redundant leading "chapter N" when gloss already includes it.
        if short.startswith(f"chapter {n} ("):
            return f"chapter {n}'s"
        return f"{short}'s"

    def repl(match: re.Match[str]) -> str:
        return chapter_phrase(int(match.group(1)))

    text = re.sub(r"§(\d+)'s", possessive, text)
    text = re.sub(r"§(\d+)", repl, text)
    # Clean up long gloss + possessive: "chapter 78 (...)'s" → "chapter 78's"
    return re.sub(r"chapter (\d+) \([^)]+\)'s", r"chapter \1's", text)


def is_tao_te_ching(item: dict[str, Any]) -> bool:
    blob = " ".join(
        str(item.get(key) or "")
        for key in ("work_id", "collection", "_id", "unit_id", "source_file")
    ).lower()
    return "tao_te_ching" in blob or "tao te ching" in blob


def humanize_ttc_unit(out: dict[str, Any]) -> dict[str, Any]:
    for field in ("translation", "commentary", "abhyasa", "thesis", "insight", "source_excerpt"):
        if out.get(field):
            out[field] = humanize_ttc_refs(str(out[field]))

    layers = out.get("pratibha_layers")
    if not isinstance(layers, list):
        return out

    for layer in layers:
        if not isinstance(layer, dict):
            continue
        if layer.get("body"):
            layer["body"] = humanize_ttc_refs(str(layer["body"]))
        for entry in layer.get("items") or []:
            if not isinstance(entry, dict):
                continue
            for key in ("term", "definition", "citation", "resonance", "divergence"):
                if entry.get(key):
                    entry[key] = humanize_ttc_refs(str(entry[key]))
    return out
