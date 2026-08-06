#!/usr/bin/env python3
"""Independent cross-check + repair of Pratibha translations against the LIVING
scholarly translations — using a model from a DIFFERENT family than the authors.

Why a different family: Terra/Luna (GPT-5.6) wrote and self-checked the corpus, so
they share blind spots. This QA pass uses an independent reviewer (default Claude
Sonnet) that carries knowledge of the standard published translations of each
passage, so it can flag meaning-level errors our same-family check missed (e.g.
Kaṭha 2.9 'no questioner' inversion).

Asteya is preserved: the reviewer's knowledge of living translations is used only to
DETECT divergence; any repair is a FRESH translation rendered from the ORIGINAL in
the reviewer's own words — never copied from a living translation. A second,
third-family model (default Gemini) confirms each applied repair is faithful and an
improvement before it is written.

Resumable (skips units already carrying provenance.qa_crosscheck unless --force),
emits a divergence report, and only rewrites units with a confirmed meaning-error.

  python qa_crosscheck.py --dryrun                 # offline: coverage + cost estimate
  python qa_crosscheck.py --limit 20               # small live probe
  python qa_crosscheck.py --collections katha_upanishad ecclesiastes_qoheleth
  python qa_crosscheck.py                           # full pass
"""
import argparse, asyncio, csv, glob, os, re, sys
import yaml

REPO = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha"
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, "scripts"))
from app.data_loader import _as_text  # noqa: E402
from faithful_expand_upanishads import _lenient_json  # noqa: E402

CANON = os.path.join(REPO, "data/canonical")
REPORT = os.path.join(REPO, "data/qa_crosscheck_report.tsv")

# Three roles, three model families for genuine independence (authors were GPT-5.6):
#  TRIAGE  — cheap, independent, reviews ALL units (broad net, low cost).
#  REVIEWER— strong, independent, adjudicates + repairs only the flagged subset.
#  CONFIRM — third family, confirms an applied repair is faithful & better.
TRIAGE = "google/gemini-2.5-flash"
REVIEWER = "anthropic/claude-sonnet-4.5"
CONFIRMER = "google/gemini-2.5-flash"

GREEK = re.compile(r"[Ͱ-Ͽἀ-ῼ]")
HEBREW = re.compile(r"[֐-׿]")
COPTIC = re.compile(r"[Ⲁ-ⳳ]")
DEVA = re.compile(r"[ऀ-ॿ]")


def original_of(d):
    """Best source-language original for a unit (IAST preferred for Sanskrit;
    otherwise the script sitting in the sanskrit_devanagari slot)."""
    iast = _as_text(d.get("sanskrit_iast"))
    dev = _as_text(d.get("sanskrit_devanagari"))
    # strip our (verse)/[ref] markers for a clean original
    def clean(s):
        return re.sub(r"[\(\[]\s*[\d:.–\-]+\s*[\)\]]", " ", s).strip()
    if iast and re.search(r"[a-zāīūṛṇśṣ]", iast):
        return clean(iast), "Sanskrit (IAST)"
    if dev:
        if GREEK.search(dev): return clean(dev), "Greek"
        if HEBREW.search(dev): return clean(dev), "Hebrew"
        if COPTIC.search(dev): return clean(dev), "Coptic (Sahidic)"
        if DEVA.search(dev): return clean(dev), "Sanskrit (Devanāgarī)"
        return clean(dev), "the original language"      # romanized Pali etc.
    return "", ""


def translation_of(d):
    t = _as_text(d.get("translation_literal") or d.get("translation"))
    if t:
        return t
    for layer in d.get("pratibha_layers") or []:
        if isinstance(layer, dict) and layer.get("kind") == "translation":
            return _as_text(layer.get("body"))
    return ""


def qa_done(d):
    prov = d.get("provenance") if isinstance(d.get("provenance"), dict) else {}
    return bool(prov.get("qa_crosscheck"))


def units(collections, force):
    for path in sorted(glob.glob(os.path.join(CANON, "*", "*.yml"))):
        if os.path.basename(path) in ("index.jsonl",):
            continue
        coll = os.path.basename(os.path.dirname(path))
        if collections and coll not in collections:
            continue
        try:
            d = yaml.safe_load(open(path))
        except Exception:
            continue
        if not isinstance(d, dict) or d.get("interpretive_only"):
            continue
        orig, lang = original_of(d)
        trans = translation_of(d)
        if not orig or len(trans) < 20:
            continue
        if not force and qa_done(d):
            continue
        yield path, d, coll, orig, lang, trans


SYS_REVIEW = (
    "You are a senior scholar of {work}, fluent in its source language and deeply familiar with the "
    "standard PUBLISHED translations of this text (the living scholarly and popular renderings). "
    "You are given the ORIGINAL passage and a NEW independent English translation. "
    "Compare the new translation against your knowledge of how this passage is rendered across the "
    "respected published translations, and judge ONLY meaning-level fidelity — real errors: "
    "mistranslations, inversions of sense, negations added or dropped, wrong referents, omitted or "
    "invented clauses. Ignore matters of style, register, or word-choice where the meaning is sound.\n"
    "If you find a genuine meaning-level error, provide a CORRECTED English translation that fixes it "
    "— rendered faithfully FROM THE ORIGINAL in your own words. Do NOT copy the wording of any "
    "published translation; produce a fresh, accurate rendering.\n"
    'Return ONLY JSON: {"verdict":"sound"|"minor"|"error","issues":["<short specific issue>"],'
    '"corrected_translation":"<full corrected English ONLY if verdict==error, else empty>"}'
)
SYS_CONFIRM = (
    "You independently verify a correction. Given the ORIGINAL passage, the OLD translation, and a "
    "PROPOSED corrected translation, decide whether the proposed version is (a) faithful to the "
    "original and (b) genuinely more accurate than the old one. "
    'Return ONLY JSON: {"accept":true|false,"note":"<short reason>"}'
)


async def _ask(model, sysmsg, usermsg, sem, max_tokens=1500):
    from app.llm import smart_chat
    async with sem:
        for attempt in range(3):
            try:
                return await smart_chat(
                    [{"role": "system", "content": sysmsg}, {"role": "user", "content": usermsg}],
                    primary_model=model, temperature=0.0, max_tokens=max_tokens)
            except Exception as e:
                if "402" in str(e):
                    return "__NO_CREDITS__"
                await asyncio.sleep(2 * (attempt + 1))
    return None


async def review_one(path, d, coll, orig, lang, trans, sem, args, report):
    work = _as_text((d.get("provenance") or {}).get("collection")) or _as_text(d.get("work_title")) or coll
    ref = _as_text((d.get("provenance") or {}).get("section")) or _as_text(d.get("source_id"))
    payload = f"Passage: {work} — {ref}\nORIGINAL ({lang}):\n{orig[:2600]}\n\nNEW TRANSLATION:\n{trans[:2600]}\n\nReturn JSON."
    sysmsg = SYS_REVIEW.replace("{work}", work)

    # Tier 1 — cheap independent triage over every unit
    r = await _ask(args.triage, sysmsg, payload, sem)
    if r == "__NO_CREDITS__":
        return path, "NO_CREDITS", None
    if r is None:
        return path, "ERR", None
    v = _lenient_json(r) or {}
    verdict = v.get("verdict", "sound")
    issues = "; ".join(x for x in (v.get("issues") or []) if x)[:400]
    corrected = _as_text(v.get("corrected_translation")).strip()
    adjudicated_by = args.triage

    # Tier 2 — strong independent reviewer adjudicates only flagged units
    if verdict in ("minor", "error") and args.reviewer and args.reviewer != args.triage:
        r2 = await _ask(args.reviewer, sysmsg, payload, sem)
        if r2 == "__NO_CREDITS__":
            return path, "NO_CREDITS", None
        v2 = _lenient_json(r2) if r2 else None
        if v2:
            verdict = v2.get("verdict", verdict)
            issues = "; ".join(x for x in (v2.get("issues") or []) if x)[:400] or issues
            corrected = _as_text(v2.get("corrected_translation")).strip() or corrected
            adjudicated_by = args.reviewer

    outcome = verdict
    if verdict == "error" and corrected and not args.flag_only:
        # independent confirmation (third family) before we touch the unit
        cr = await _ask(args.confirmer, SYS_CONFIRM,
                        f"ORIGINAL ({lang}): {orig[:2000]}\n\nOLD: {trans[:1500]}\n\nPROPOSED: {corrected[:1500]}\n\nReturn JSON.",
                        sem, max_tokens=300)
        if cr == "__NO_CREDITS__":
            return path, "NO_CREDITS", None
        cj = _lenient_json(cr) if cr else None
        if cj and cj.get("accept"):
            _apply_repair(path, d, corrected, adjudicated_by, args.confirmer, issues)
            outcome = "repaired"
        else:
            outcome = "error_unconfirmed"

    _mark(path, d, f"{adjudicated_by}: {verdict}", issues, outcome != "repaired")
    report.append((coll, _as_text(d.get("source_id")), verdict, outcome, issues,
                   (corrected[:160] if corrected else "")))
    return path, outcome, issues


def _apply_repair(path, d, corrected, reviewer, confirmer, issues):
    d["translation_literal"] = corrected
    if isinstance(d.get("translation"), str):
        d["translation"] = corrected
    for layer in d.get("pratibha_layers") or []:
        if isinstance(layer, dict) and layer.get("kind") == "translation":
            layer["body"] = corrected
    prov = d.get("provenance") if isinstance(d.get("provenance"), dict) else {}
    prov["qa_repair"] = f"translation corrected via independent cross-check ({reviewer}), confirmed ({confirmer}): {issues[:200]}"
    prov["english_source"] = (_as_text(prov.get("english_source")) +
                              " | corrected on independent cross-check with the living scholarly translations (re-rendered from the original, not copied)").strip(" |")
    d["provenance"] = prov
    _write(path, d)


def _mark(path, d, verdict_str, issues, write):
    prov = d.get("provenance") if isinstance(d.get("provenance"), dict) else {}
    prov["qa_crosscheck"] = verdict_str
    if issues:
        prov["qa_issues"] = issues[:300]
    d["provenance"] = prov
    if write:
        _write(path, d)


def _write(path, d):
    yaml.safe_dump(d, open(path, "w"), allow_unicode=True, sort_keys=False, width=100)


async def run(args):
    rows = list(units(set(args.collections or []), args.force))
    if args.limit:
        rows = rows[: args.limit]
    print(f"[qa] {len(rows)} units | triage={args.triage} → reviewer={args.reviewer} → confirm={args.confirmer}")
    if args.dryrun:
        import collections as C
        by = C.Counter(c for _, _, c, _, _, _ in rows)
        toks = sum(len(o) + len(t) for _, _, _, o, _, t in rows) // 3  # ~chars→tokens rough
        print("  by collection (top 12):", dict(sorted(by.items(), key=lambda x: -x[1])[:12]))
        print(f"  Tier-1 triage (cheap, all {len(rows)}): ~{toks:,} in +~{len(rows)*400:,} out tokens")
        print("  Tier-2 reviewer (strong) + confirm: only on flagged units (~10-20%)")
        print("  sample extraction:")
        for path, d, coll, orig, lang, trans in rows[:3]:
            print(f"   · {coll}/{_as_text(d.get('source_id'))} [{lang}] orig<{orig[:38]}…> trans<{trans[:38]}…>")
        return
    sem = asyncio.Semaphore(args.concurrency)
    report = []
    res = await asyncio.gather(*(review_one(p, d, c, o, l, t, sem, args, report)
                                 for (p, d, c, o, l, t) in rows))
    if any(s == "NO_CREDITS" for _, s, _ in res):
        print("  ⚠ OpenRouter returned 402 Insufficient credits — top up, then re-run (resumable).")
    import collections as C
    print("[qa] outcomes:", dict(C.Counter(s for _, s, _ in res)))
    new = not os.path.exists(REPORT)
    with open(REPORT, "a", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        if new:
            w.writerow(["collection", "source_id", "verdict", "outcome", "issues", "corrected_preview"])
        w.writerows(report)
    print(f"[qa] report appended: {REPORT}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--collections", nargs="*", default=[])
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--concurrency", type=int, default=4)
    ap.add_argument("--triage", default=TRIAGE, help="cheap independent model that reviews all units")
    ap.add_argument("--reviewer", default=REVIEWER, help="strong independent model adjudicating flagged units")
    ap.add_argument("--confirmer", default=CONFIRMER, help="third-family model confirming applied repairs")
    ap.add_argument("--flag-only", action="store_true", help="report divergences, do not repair")
    ap.add_argument("--force", action="store_true", help="re-check units already QA'd")
    ap.add_argument("--dryrun", action="store_true", help="offline: coverage + cost estimate, no API")
    args = ap.parse_args()
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
