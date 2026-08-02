"""Deterministic IAST -> Devanagari. Verified by round-tripping through the
Gita-era Devanagari->IAST converter: IAST -> Deva -> IAST must equal the source."""
import re

VOWELS = {  # independent : (independent-sign, matra-sign)
    "a": ("अ", ""), "ā": ("आ", "ा"), "i": ("इ", "ि"), "ī": ("ई", "ी"),
    "u": ("उ", "ु"), "ū": ("ऊ", "ू"), "ṛ": ("ऋ", "ृ"), "ṝ": ("ॠ", "ॄ"),
    "ḷ": ("ऌ", "ॢ"), "ḹ": ("ॡ", "ॣ"), "e": ("ए", "े"), "ai": ("ऐ", "ै"),
    "o": ("ओ", "ो"), "au": ("औ", "ौ"),
}
# consonants, longest first so multi-char (kh, ṭh, …) win
CONS = {
    "kh": "ख", "gh": "घ", "ṅ": "ङ", "ch": "छ", "jh": "झ", "ñ": "ञ",
    "ṭh": "ठ", "ḍh": "ढ", "ṇ": "ण", "th": "थ", "dh": "ध",
    "ph": "फ", "bh": "भ", "ś": "श", "ṣ": "ष",
    "k": "क", "g": "ग", "c": "च", "j": "ज", "ṭ": "ट", "ḍ": "ड",
    "t": "त", "d": "द", "n": "न", "p": "प", "b": "ब", "m": "म",
    "y": "य", "r": "र", "l": "ल", "v": "व", "s": "स", "h": "ह", "ḻ": "ळ",
}
MARKS = {"ṃ": "ं", "ḥ": "ः", "ṁ": "ं", "m̐": "ँ", "'": "ऽ"}
VIRAMA = "्"
VOWEL_KEYS = sorted(VOWELS, key=len, reverse=True)
CONS_KEYS = sorted(CONS, key=len, reverse=True)


def iast_to_deva(text: str) -> str:
    out = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        # consonant?
        cons = next((k for k in CONS_KEYS if text.startswith(k, i)), None)
        if cons:
            out.append(CONS[cons]); i += len(cons)
            # following vowel -> matra, else inherent 'a' suppressed via virama
            vow = next((k for k in VOWEL_KEYS if text.startswith(k, i)), None)
            if vow == "a":
                i += 1  # inherent, no sign
            elif vow:
                out.append(VOWELS[vow][1]); i += len(vow)
            else:
                out.append(VIRAMA)
            continue
        vow = next((k for k in VOWEL_KEYS if text.startswith(k, i)), None)
        if vow:
            out.append(VOWELS[vow][0]); i += len(vow); continue
        if ch in MARKS:
            out.append(MARKS[ch]); i += 1; continue
        if ch.isdigit():
            out.append("०१२३४५६७८९"[int(ch)]); i += 1; continue
        out.append(ch); i += 1
    return "".join(out)
