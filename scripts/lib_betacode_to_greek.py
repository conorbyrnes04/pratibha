#!/usr/bin/env python3
"""Minimal TLG Betacode -> Unicode polytonic Greek. Emits base letters plus
combining diacritics, then NFC-composes to precomposed glyphs."""
import re, unicodedata

LOWER = {"a":"α","b":"β","g":"γ","d":"δ","e":"ε","z":"ζ","h":"η","q":"θ",
         "i":"ι","k":"κ","l":"λ","m":"μ","n":"ν","c":"ξ","o":"ο","p":"π",
         "r":"ρ","s":"σ","t":"τ","u":"υ","f":"φ","x":"χ","y":"ψ","w":"ω"}
UPPER = {k: v.upper() for k, v in LOWER.items()}
DIA = {")":"̓", "(":"̔", "/":"́", "\\":"̀",
       "=":"͂", "+":"̈", "|":"ͅ"}
PUNCT = {":":"·", ";":";", "'":"’"}
DIA_CHARS = set(DIA)
LETTERS = set(LOWER)


def betacode_to_greek(text: str) -> str:
    out = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        upper = False
        if ch == "*":                     # capital marker; diacritics follow, then letter
            upper = True
            i += 1
            pend = []
            while i < n and text[i] in DIA_CHARS:
                pend.append(DIA[text[i]]); i += 1
            if i < n and text[i].lower() in LETTERS:
                out.append(UPPER[text[i].lower()]); i += 1
                out.extend(pend)
            continue
        low = ch.lower()
        if low in LETTERS:
            # final sigma: 's' not followed by another letter
            if low == "s":
                j = i + 1
                nxt = text[j] if j < n else ""
                base = "ς" if nxt.lower() not in LETTERS else "σ"
            else:
                base = UPPER[low] if ch.isupper() else LOWER[low]
            out.append(base); i += 1
            while i < n and text[i] in DIA_CHARS:
                out.append(DIA[text[i]]); i += 1
            continue
        out.append(PUNCT.get(ch, ch)); i += 1
    return unicodedata.normalize("NFC", "".join(out))


if __name__ == "__main__":
    s = r"*para\ tou= pa/ppou *ou)h/rou to\ kalo/hqes kai\ a)o/rghton."
    print(betacode_to_greek(s))
    print("expected ~ παρὰ τοῦ πάππου Οὐήρου τὸ καλόηθες καὶ ἀόργητον.")
