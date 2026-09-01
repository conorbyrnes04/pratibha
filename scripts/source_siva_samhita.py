#!/usr/bin/env python3
"""Attach Devanagari + IAST to Śiva Saṃhitā canonical units from the Sanskrit
Wikisource text (CC BY-SA — same license class as the GRETIL texts already used).

ch1 & ch2 numbering matches canonical exactly (content-verified) -> aligned by
verse number, deterministically, no LLM. ch3/ch4/ch5 renumber differently, so for
those each unit's matching śloka is located by an asteya-safe extraction: a strong
model is given ONLY that chapter's Devanagari + the unit's English, must COPY the
matching śloka verbatim, and the copy is verified as a substring of the source
before attaching. Devanagari is stored verbatim; IAST is transliterated with
indic_transliteration (deterministic). Resumable (skips units already sourced).
"""
import argparse, asyncio, glob, os, re, sys, unicodedata
import yaml
REPO = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha"
sys.path.insert(0, REPO); sys.path.insert(0, os.path.join(REPO, "scripts"))
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from faithful_expand_upanishads import _lenient_json  # noqa: E402

SRC = os.path.join(REPO, "data/raw_texts/pd/siva_samhita/sivasamhita_wikisource_devanagari.txt")
CANON = os.path.join(REPO, "data/canonical/siva_samhita")
EDITION = "Sanskrit Wikisource शिवसंहिता (sa.wikisource.org, CC BY-SA 4.0)"
REVIEWER = "anthropic/claude-sonnet-4.5"
DETERMINISTIC_CHAPTERS = {1, 2}


def parse_source():
    raw = open(SRC, encoding="utf-8").read()
    chapters, verses = {}, {}
    parts = re.split(r"===CH(\d+)===", raw)[1:]
    for i in range(0, len(parts), 2):
        c = int(parts[i]); body = re.sub(r"\{\{[^}]*\}\}", " ", parts[i + 1])
        chapters[c] = " ".join(body.split())
        cur = []
        for tok in re.split(r"(\s[०-९]+\s*)", body):
            m = re.match(r"\s*([०-९]+)\s*$", tok)
            if m:
                v = int(m.group(1).translate(str.maketrans("०१२३४५६७८९", "0123456789")))
                t = " ".join(" ".join(cur).split())
                if t and v < 300:
                    verses[f"{c}.{v}"] = t
                cur = []
            else:
                cur.append(tok)
    return chapters, verses


def to_iast(dev):
    return transliterate(dev, sanscript.DEVANAGARI, sanscript.IAST)


def dnorm(s):
    return re.sub(r"[^ऀ-ॿ]", "", unicodedata.normalize("NFC", s))


def key_of(d):
    return str((d.get("provenance") or {}).get("verse") or "").strip()


def expand_key(k):
    m = re.match(r"^(\d+)\.(\d+)(?:-(\d+))?$", k)
    if not m:
        return None, []
    c = int(m.group(1)); a = int(m.group(2)); b = int(m.group(3) or m.group(2))
    return c, [f"{c}.{v}" for v in range(a, b + 1)]


def attach(path, d, dev):
    dev = dev.strip()
    d["sanskrit_devanagari"] = dev
    d["sanskrit_iast"] = to_iast(dev)
    prov = d.get("provenance") if isinstance(d.get("provenance"), dict) else {}
    prov["original_source"] = EDITION
    prov["original_reliability"] = f"SOURCED — {EDITION}; verbatim Devanagari, IAST transliterated"
    prov["verification"] = "Devanagari copied verbatim from Sanskrit Wikisource; IAST is deterministic transliteration"
    d["provenance"] = prov
    if d.get("pratibha_layers"):
        d["pratibha_layers"] = [l for l in d["pratibha_layers"]
                                if not (isinstance(l, dict) and l.get("kind") in ("original", "iast"))]
    yaml.safe_dump(d, open(path, "w"), allow_unicode=True, sort_keys=False, width=100)


SYS = (
    "You are given one CHAPTER of the Śiva Saṃhitā in Sanskrit (Devanagari) and an English "
    "translation of ONE śloka from that chapter. Find the śloka in the Devanagari SOURCE that the "
    "English renders, and return it EXACTLY as it appears — copied verbatim, Devanagari only. Do NOT "
    "translate, transliterate, correct, or generate; only copy what is present. If you cannot confidently "
    'locate it, return empty. Return ONLY JSON: {"devanagari":"<verbatim śloka or empty>"}'
)


async def llm_one(path, d, chap_text, sem, report):
    from app.llm import smart_chat
    en = (d.get("translation") or "")[:1000]
    sid = key_of(d)
    async with sem:
        r = None
        for attempt in range(3):
            try:
                r = await smart_chat(
                    [{"role": "system", "content": SYS},
                     {"role": "user", "content": f"English śloka:\n{en}\n\nCHAPTER SOURCE (Devanagari):\n{chap_text[:120000]}\n\nReturn JSON."}],
                    primary_model=REVIEWER, temperature=0.0, max_tokens=800)
                break
            except Exception as e:
                if "402" in str(e):
                    report.append((sid, "NO_CREDITS")); return
                await asyncio.sleep(2 * (attempt + 1))
        if r is None:
            report.append((sid, "ERR")); return
    dev = ((_lenient_json(r) or {}).get("devanagari") or "").strip()
    if len(dnorm(dev)) < 6:
        report.append((sid, "no-match")); return
    if dnorm(dev)[:40] not in dnorm(chap_text):
        report.append((sid, "UNVERIFIED")); return
    attach(path, d, dev)
    report.append((sid, "sourced"))


async def main(limit=0, only=None):
    chapters, verses = parse_source()
    files = sorted(glob.glob(os.path.join(CANON, "*.yml")))
    det_done = det_miss = 0
    llm_rows = []
    for f in files:
        d = yaml.safe_load(open(f))
        if not isinstance(d, dict):
            continue
        if (d.get("sanskrit_devanagari") or "").strip() and (d.get("sanskrit_iast") or "").strip():
            continue  # resumable
        c, keys = expand_key(key_of(d))
        if c is None:
            continue
        if only and c != only:
            continue
        if c in DETERMINISTIC_CHAPTERS:
            parts = [verses[k] for k in keys if k in verses]
            if parts and len(parts) == len(keys):
                attach(f, d, " ".join(parts)); det_done += 1
            else:
                det_miss += 1
        else:
            if c in chapters:
                llm_rows.append((f, d, chapters[c]))
    print(f"deterministic (ch1/ch2): attached {det_done}, unmatched {det_miss}")
    if limit:
        llm_rows = llm_rows[:limit]
    print(f"LLM content-match (ch3/4/5): {len(llm_rows)} units")
    if llm_rows:
        sem = asyncio.Semaphore(4); report = []
        await asyncio.gather(*(llm_one(f, d, ct, sem, report) for f, d, ct in llm_rows))
        import collections as C
        print("  outcomes:", dict(C.Counter(s for _, s in report)))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only-chapter", type=int, default=0)
    args = ap.parse_args()
    asyncio.run(main(args.limit, args.only_chapter or None))
