#!/usr/bin/env python3
"""Add units to slim English-PD prose collections. The unit body is a VERBATIM
passage copied from the public-domain source (asteya-safe — never model-generated);
Terra (OpenRouter) authors ONLY the study apparatus (commentary/key_terms/
resonances/practice), grounded in that passage. Appends to existing units with
continued numbering. Config-driven; resumable-ish (dedupes against existing bodies).

  python scripts/expand_pd_prose.py --work cloud --n 15
"""
import argparse, asyncio, glob, os, re, sys
import yaml
sys.path.insert(0, "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha")
from app.llm import smart_chat
from faithful_expand_upanishads import _lenient_json

ROOT = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha"
PD = os.path.join(ROOT, "data/raw_texts/pd")
CANON = os.path.join(ROOT, "data/canonical")
TERRA = "openai/gpt-5.6-terra"

CFG = {
    "cloud": dict(
        src=os.path.join(PD, "thecloudofunknowingbamccann_djvu.txt"),
        coll_dir="the_cloud_of_unknowing", work_id="the_cloud_of_unknowing",
        work_title="The Cloud of Unknowing", coll="The Cloud of Unknowing",
        prov="English from Justin McCann's edition of The Cloud of Unknowing (1924, public domain). Study rendering.",
        context="The Cloud of Unknowing, a 14th-c. English apophatic contemplative treatise (unknowing, the cloud of forgetting, naked intent of the will toward God)",
        start=r"THE FIRST CHAPTER", split=r"THE [A-Z]+(?:-[A-Z]+)? CHAPTER", kind="chapter"),
    "johnson": dict(
        src=os.path.join(PD, "historyofyorubas00john_djvu.txt"),
        coll_dir="johnson_yoruba_religion", work_id="johnson_yoruba_religion",
        work_title="The Yoruba Faith (Samuel Johnson)", coll="The Yoruba Faith (Samuel Johnson)",
        prov=("English follows Samuel Johnson, The History of the Yorubas (1921, public domain). "
              "Recorded by a Yoruba Anglican clergyman; colonial-era framing. Study rendering pending "
              "review by Yoruba tradition-bearers."),
        context="Samuel Johnson's account of Yoruba religion (Olorun the Supreme Being, the orisas, worship, sacrifice, destiny)",
        start=r"^RELIGION\s*$", end_after=1400, split=None, kind="paragraph"),
}

AUTH = """You author the study apparatus for ONE passage of {ctx}. You are given the exact verbatim
passage (public domain). Do NOT rewrite or restate the passage; write ABOUT it, faithfully.
Return ONLY JSON:
{{"title":"<short evocative English title, no numbers>",
  "commentary":"<700-1100 chars, rigorous, grounded in THIS passage, no filler>",
  "key_terms":[{{"term":"<term present in passage>","gloss":"<one line>"}}, ...2-4],
  "resonances":[{{"ref":"<recognizable text/figure>","parallel":"<real parallel>","divergence":"<one honest divergence>"}}, ...2-3],
  "practice":"<2-3 sentence contemplative exercise drawn from the passage>"}}"""


def clean(s):
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\b(RELIGION|THE HISTORY OF THE YORUBAS)\s*\d*\b", "", s).strip()
    return s


def garbled(s):
    if re.search(r"[%£¥{}|\\<>@#*_=+~`]", s):
        return True
    if re.search(r"\b[a-z]{1,2}[A-Z]{2}", s):
        return True
    letters = sum(c.isalpha() or c.isspace() or c in ".,;:'\"?!-—()" for c in s)
    return letters / max(1, len(s)) < 0.92


def extract(cfg):
    txt = open(cfg["src"], encoding="utf-8", errors="replace").read()
    lines = txt.splitlines()
    # find start
    si = 0
    for i, l in enumerate(lines):
        if re.search(cfg["start"], l):
            si = i; break
    region = "\n".join(lines[si: si + cfg.get("end_after", 100000)])
    passages = []
    if cfg["kind"] == "chapter":
        chunks = re.split(cfg["split"], region)
        for c in chunks[1:]:
            p = clean(c)
            if 160 <= len(p) <= 700 and not garbled(p):
                passages.append(p[:700].rsplit(".", 1)[0] + "." if "." in p[:700] else p[:700])
    else:  # paragraph
        para = re.split(r"\n\s*\n", region)
        for p in para:
            p = clean(p)
            if 180 <= len(p) <= 650 and not garbled(p) and p.count(" ") > 20:
                passages.append(p)
    # dedupe
    out, seen = [], set()
    for p in passages:
        k = p[:40].lower()
        if k not in seen:
            seen.add(k); out.append(p)
    return out


async def author(passage, cfg, sem):
    async with sem:
        for attempt in range(3):
            try:
                r = await smart_chat(
                    [{"role": "system", "content": AUTH.format(ctx=cfg["context"])},
                     {"role": "user", "content": f"PASSAGE (verbatim, public domain):\n{passage}\n\nReturn JSON."}],
                    primary_model=TERRA, temperature=0.4, max_tokens=1400)
                j = _lenient_json(r)
                if j and j.get("commentary"):
                    return j
            except Exception as e:
                if "402" in str(e):
                    return {"_nocredits": True}
                await asyncio.sleep(2 * (attempt + 1))
    return None


def existing_bodies(coll_dir):
    bodies = set()
    n = 0
    for f in glob.glob(os.path.join(CANON, coll_dir, "*.yml")):
        n += 1
        d = yaml.safe_load(open(f)) or {}
        bodies.add((d.get("translation") or "")[:40].lower())
    return bodies, n


async def main(work, n):
    cfg = CFG[work]
    passages = extract(cfg)
    have, start_n = existing_bodies(cfg["coll_dir"])
    passages = [p for p in passages if p[:40].lower() not in have][:n]
    print(f"[{work}] {len(passages)} new passages to author (existing units: {start_n})")
    sem = asyncio.Semaphore(4)
    apparats = await asyncio.gather(*(author(p, cfg, sem) for p in passages))
    written = 0
    for i, (p, ap) in enumerate(zip(passages, apparats), start=1):
        if not ap:
            continue
        if ap.get("_nocredits"):
            print("  OpenRouter credits exhausted — stopping."); break
        idx = start_n + written + 1
        slug = cfg["work_id"]
        uid = f"{slug}.{slug}_{idx:03d}"
        kt = "\n\n".join(f"**{t.get('term','')}** — {t.get('gloss','')}" for t in (ap.get("key_terms") or []))
        rz = "\n\n".join(f"**{r.get('ref','')}:** {r.get('parallel','')} Divergence: {r.get('divergence','')}"
                         for r in (ap.get("resonances") or []))
        layers = [{"kind": "translation", "label": "Translation", "body": p}]
        if ap.get("commentary"): layers.append({"kind": "commentary", "label": "Commentary", "body": ap["commentary"]})
        if kt: layers.append({"kind": "key_terms", "label": "Key Terms", "body": kt})
        if rz: layers.append({"kind": "resonances", "label": "Resonances", "body": rz})
        if ap.get("practice"): layers.append({"kind": "practice", "label": "Practice", "body": ap["practice"]})
        unit = {
            "source_id": f"{slug}_{idx:03d}".upper(), "category": "root_text",
            "work_id": slug, "work_title": cfg["work_title"], "unit_id": uid,
            "unit_label": ap.get("title") or f"{cfg['work_title']} {idx}",
            "title": ap.get("title") or f"{cfg['work_title']} {idx}", "unit_type": "reflection",
            "commentary": ap.get("commentary", ""), "themes": [], "tags": [slug],
            "quality_score": 0, "editorial_score": 0, "editorial_maturity": "strong_draft",
            "translation_provenance": cfg["prov"], "pratibha_layers": layers,
            "provenance": {"collection": cfg["coll"], "cultural_context": cfg["prov"]},
            "translation": p, "practice": ap.get("practice", ""), "abhyasa": ap.get("practice", ""),
        }
        with open(os.path.join(CANON, cfg["coll_dir"], f"{uid.replace('.', '_')}.yml"), "w") as fh:
            yaml.safe_dump(unit, fh, allow_unicode=True, sort_keys=False, width=100)
        written += 1
    print(f"[{work}] wrote {written} new units; collection now {start_n + written}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True, choices=list(CFG))
    ap.add_argument("--n", type=int, default=15)
    args = ap.parse_args()
    asyncio.run(main(args.work, args.n))
