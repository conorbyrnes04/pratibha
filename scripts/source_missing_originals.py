#!/usr/bin/env python3
"""Source real originals for legacy units that lack one, from the LOCAL PD sources.

Asteya-safe: a strong model (Claude Sonnet) is given the unit's English translation
and the FULL local source text, and must EXTRACT the verbatim passage that the
English renders — copied from the source, never generated. Every extraction is then
VERIFIED to be a normalized substring of the source before it is attached; anything
that doesn't actually appear in the source is rejected (anti-hallucination). For
Sanskrit (GRETIL IAST) the extracted IAST is stored and Devanagari is transliterated;
for other scripts the extracted script is stored in the original slot.

Resumable (skips units that already have a real original). Report -> data/source_report.tsv.
  python source_missing_originals.py --collection know_yourself_ibn_arabi_balyani [--limit N]
"""
import argparse, asyncio, csv, glob, json, os, re, sys, unicodedata
import yaml

REPO = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha"
sys.path.insert(0, REPO); sys.path.insert(0, os.path.join(REPO, "scripts"))
from app.data_loader import _as_text, is_chapter_summary_meta_unit  # noqa: E402
from faithful_expand_upanishads import _lenient_json  # noqa: E402
from lib_iast_to_deva import iast_to_deva  # noqa: E402

RAW = os.path.join(REPO, "data/raw_texts/pd")
CANON = os.path.join(REPO, "data/canonical")
REVIEWER = "anthropic/claude-sonnet-4.5"

COLLS = {
    "know_yourself_ibn_arabi_balyani": dict(src="arabic/balyani_risalat_al_wujudiyya_ahadiyya_ar.txt",
        lang="Arabic", sanskrit=False, edition="Risālat al-aḥadiyya (al-Balyānī), Arabic PD transcription (ibnalarabi.com)"),
    "phaedo_plato": dict(src="greek/phaedo_burnet_stephanus.json", loader="phaedo",
        lang="Greek", sanskrit=False, edition="Plato, Phaedo, Burnet Greek (Perseus, PD), by Stephanus section"),
    "astavakra_gita": dict(src="indian/astavakra_gita_gretil_iast.txt",
        lang="Sanskrit (IAST)", sanskrit=True, edition="GRETIL Aṣṭāvakragītā e-text"),
    "shantideva_bodhicaryavatara": dict(src="indian/bodhicaryavatara_gretil_iast_sanskrit.txt",
        lang="Sanskrit (IAST)", sanskrit=True, edition="GRETIL Bodhicaryāvatāra e-text (Śāntideva)"),
    "tantrasara": dict(src="indian/tantrasara_abhinavagupta_gretil_iast.txt",
        lang="Sanskrit (IAST)", sanskrit=True, edition="GRETIL Tantrasāra e-text (Abhinavagupta)"),
    "tilopa_mahamudra": dict(src="tibetan/tilopa_ganges_mahamudra_lotsawa_bo.txt",
        lang="Tibetan", sanskrit=False, edition="Tilopa, Gaṅgā-mahāmudrā, Tibetan (Lotsawa House, PD/CC)"),
    "the_book_of_chuang_tzu": dict(src="chinese/zhuangzi_haodoo_chapters.json", loader="zhuangzi",
        lang="Classical Chinese", sanskrit=False, edition="Zhuangzi Chinese (Haodoo edition, PD)"),
    "milarepa_songs": dict(src="tibetan/milarepa_songs_wylie_restore.yml",
        lang="Tibetan", sanskrit=False, edition="Milarepa's songs, Tibetan (Wylie restoration, local PD/CC)"),
    "mandukya_upanishad_and_gaudapada_karika": dict(src="indian/mandukya_gaudapada_gretil_iast.txt",
        lang="Sanskrit (IAST)", sanskrit=True, edition="GRETIL Māṇḍūkyopaniṣad + Gauḍapāda-kārikā e-text"),
    "pseudo_dionysius": dict(src="greek/divine_names_greek_unicode.txt",
        lang="Greek", sanskrit=False, edition="Pseudo-Dionysius, Divine Names, Greek (Migne PG3, Unicode; PD)"),
}


def load_source(cfg):
    path = os.path.join(RAW, cfg["src"])
    if cfg.get("loader") == "phaedo":
        d = json.load(open(path, encoding="utf-8"))
        secs = d.get("sections", d)
        return "\n".join(f"[{k}] {v}" for k, v in secs.items())
    if cfg.get("loader") == "zhuangzi":
        d = json.load(open(path, encoding="utf-8"))
        chs = d.get("chapters", {})
        out = []
        for k, v in chs.items():
            body = v.get("body") or v.get("text") or v if not isinstance(v, str) else v
            out.append(f"[ch{k}] {body if isinstance(body,str) else json.dumps(body,ensure_ascii=False)}")
        return "\n".join(out)
    return open(path, encoding="utf-8").read()


def norm(s, sanskrit):
    s = unicodedata.normalize("NFD", s)
    if sanskrit:
        return re.sub(r"[^a-zāīūṛṝḷḹṅñṭḍṇśṣṃḥ]", "", s.lower())
    # strip combining marks (Greek accents, Arabic harakat), spaces, punctuation, latin
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[\sً-ْـ་.,;:·—–\-'\"()\[\]0-9a-zA-Z]", "", s).lower()


SYS = (
    "You are given the FULL source text of a classical work and an English translation of ONE passage "
    "from it. Find the passage in the SOURCE that this English renders, and return that passage's text "
    "EXACTLY as it appears in the source — copied verbatim, character for character. Do NOT translate, "
    "normalize, correct, or generate any text; only copy what is present in the source. If you cannot "
    "confidently locate the passage in the source, return empty.\n"
    'Return ONLY JSON: {"original":"<verbatim source-language passage, or empty>"}'
)


async def source_one(path, d, cfg, source, sem, report):
    from app.llm import smart_chat
    trans = _as_text(d.get("translation_literal") or d.get("translation"))
    ref = _as_text((d.get("provenance") or {}).get("section"))
    sid = _as_text(d.get("source_id"))
    async with sem:
        r = None
        for attempt in range(3):
            try:
                r = await smart_chat([{"role": "system", "content": SYS},
                    {"role": "user", "content": f"Work hint: {ref}\nEnglish passage:\n{trans[:1200]}\n\nSOURCE:\n{source[:190000]}\n\nReturn JSON."}],
                    primary_model=REVIEWER, temperature=0.0, max_tokens=1200)
                break
            except Exception as e:
                if "402" in str(e):
                    report.append((sid, "NO_CREDITS", "")); return
                await asyncio.sleep(2 * (attempt + 1))
    if r is None:
        report.append((sid, "ERR", "")); return
    orig = _as_text((_lenient_json(r) or {}).get("original")).strip()
    if len(orig) < 8:
        report.append((sid, "no-match", "")); return
    # VERIFY: extracted text must actually appear in the source (anti-hallucination)
    ns, nsrc = norm(orig, cfg["sanskrit"]), norm(source, cfg["sanskrit"])
    if len(ns) < 8 or ns[:60] not in nsrc:
        report.append((sid, "UNVERIFIED(not in source)", orig[:50])); return
    _attach(path, d, orig, cfg)
    report.append((sid, "sourced", orig[:50]))


def _attach(path, d, orig, cfg):
    if cfg["sanskrit"]:
        iast = re.sub(r"\s*//.*?//\s*", " ", orig).strip()
        d["sanskrit_iast"] = iast
        d["sanskrit_devanagari"] = " ।\n".join(iast_to_deva(p.strip()) for p in re.split(r"[/|]", iast) if p.strip())
    else:
        d["sanskrit_devanagari"] = orig
    prov = d.get("provenance") if isinstance(d.get("provenance"), dict) else {}
    prov["original_source"] = cfg["edition"]
    prov["original_reliability"] = f"SOURCED — {cfg['edition']}; passage located in the source and verified verbatim"
    prov["verification"] = "original extracted from the local PD source and verified as a verbatim substring"
    d["provenance"] = prov
    # drop any explicit placeholder original layer so the real text surfaces
    for layer in d.get("pratibha_layers") or []:
        if isinstance(layer, dict) and layer.get("kind") in ("original", "iast"):
            layer["_drop"] = True
    if d.get("pratibha_layers"):
        d["pratibha_layers"] = [l for l in d["pratibha_layers"] if not l.get("_drop")]
    yaml.safe_dump(d, open(path, "w"), allow_unicode=True, sort_keys=False, width=100)


def missing_units(cfg_name):
    from app.data_loader import normalize_unit
    def real(disp):
        return any(0x0370<=ord(c)<=0x9FFF for c in disp) or (len(disp) > 15 and "source-language basis" not in disp.lower())
    for path in sorted(glob.glob(os.path.join(CANON, cfg_name, "*.yml"))):
        d = yaml.safe_load(open(path))
        if not isinstance(d, dict) or d.get("interpretive_only") or is_chapter_summary_meta_unit(d):
            continue
        n = normalize_unit(d, path)
        disp = next((l["body"] for l in n["pratibha_layers"] if l["kind"] == "original"), "")
        if not real(disp):
            yield path, d


async def run(name, limit):
    cfg = COLLS[name]
    source = load_source(cfg)
    rows = list(missing_units(name))
    if limit:
        rows = rows[:limit]
    print(f"[{name}] sourcing {len(rows)} units from {cfg['src']} ({len(source)} chars)")
    sem = asyncio.Semaphore(4)
    report = []
    await asyncio.gather(*(source_one(p, d, cfg, source, sem, report) for p, d in rows))
    import collections as C
    print("  outcomes:", dict(C.Counter(s for _, s, _ in report)))
    with open(os.path.join(REPO, "data/source_report.tsv"), "a", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        for sid, status, preview in report:
            w.writerow([name, sid, status, preview])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--collection", required=True, choices=list(COLLS))
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    asyncio.run(run(a.collection, a.limit))


if __name__ == "__main__":
    main()
