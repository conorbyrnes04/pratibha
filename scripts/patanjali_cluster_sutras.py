"""Merge consecutive Yoga-Sūtra sūtras into thematic clusters (mirroring the
Bhagavad Gita's clustered-unit model). Writes to a STAGING dir — never touches
the live corpus — so the cluster map and merge quality can be reviewed first.

Faithful/mechanical for source + translation (no fabrication); commentary is a
stripped, sub-headed concatenation of the authored per-sūtra commentaries,
flagged for a later unified re-authoring pass.
"""
import glob, os, re, sys
import yaml
sys.path.insert(0, "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha")
from app.data_loader import _strip_layer_tail, _as_text, normalize_unit

ROOT = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha"
SRC = os.path.join(ROOT, "data/canonical/patañjali_yoga_sūtras")
STAGE = os.path.join(ROOT, "data/staging/patanjali_clusters")
DEV = str.maketrans("0123456789", "०१२३४५६७८९")

# Thematic cluster map: (pada, start, end, title). Grounded in the sūtra content
# and the canonical structure of each pāda.
CLUSTERS = [
    # Pāda 1 — Samādhi
    (1, 1, 4,  "The Ground of Yoga — Stilling the Mind, Resting in the Seer"),
    (1, 5, 11, "The Five Movements of the Mind"),
    (1, 12, 16,"Practice and Non-Attachment — Abhyāsa and Vairāgya"),
    (1, 17, 22,"The Two Samādhis and the Aspirant's Intensity"),
    (1, 23, 29,"Devotion to Īśvara and the Syllable OM"),
    (1, 30, 32,"The Obstacles and Their Single Remedy"),
    (1, 33, 39,"Ways to Steady the Mind"),
    (1, 40, 46,"From the Atom to the Infinite — Samādhi With Seed"),
    (1, 47, 51,"Truth-Bearing Wisdom and the Seedless Samādhi"),
    # Pāda 2 — Sādhana
    (2, 1, 2,  "Kriyā Yoga — Yoga in Action"),
    (2, 3, 9,  "The Five Afflictions — the Kleśas"),
    (2, 10, 11,"Dissolving the Afflictions"),
    (2, 12, 14,"Karma and Its Fruits"),
    (2, 15, 17,"All Is Suffering — and Its Cause"),
    (2, 18, 22,"The Seen and Its Purpose — Prakṛti and the Guṇas"),
    (2, 23, 27,"The Conjunction, Its Cause, and Its Ending"),
    (2, 28, 29,"The Eight Limbs Named"),
    (2, 30, 34,"The Restraints and Observances — Yama and Niyama"),
    (2, 35, 39,"The Fruits of the Restraints"),
    (2, 40, 45,"The Fruits of the Observances"),
    (2, 46, 48,"Posture — Āsana"),
    (2, 49, 53,"Breath-Regulation — Prāṇāyāma"),
    (2, 54, 55,"Withdrawal of the Senses — Pratyāhāra"),
    # Pāda 3 — Vibhūti
    (3, 1, 3,  "The Inner Three — Concentration, Meditation, Absorption"),
    (3, 4, 6,  "Saṃyama and Its Gradual Mastery"),
    (3, 7, 8,  "Inner Limbs, Yet Still Outer"),
    (3, 9, 12, "The Transformations of the Mind"),
    (3, 13, 15,"Transformation, Time, and Succession"),
    (3, 16, 22,"Powers of Knowing — Past, Future, and Other Minds"),
    (3, 23, 29,"Saṃyama on Strength, the Body, and the Cosmos"),
    (3, 30, 37,"Saṃyama Within — Body, Senses, and the Self's Distinction"),
    (3, 38, 43,"Subtle Powers — Levitation, Divine Senses, Passing Into Others"),
    (3, 44, 49,"Mastery Over the Elements and the Senses"),
    (3, 50, 55,"Discriminative Knowing and the Threshold of Liberation"),
    # Pāda 4 — Kaivalya
    (4, 1, 3,  "The Sources of the Powers and Nature's Overflow"),
    (4, 4, 6,  "Created Minds and the Meditation-Born Mind"),
    (4, 7, 11, "Karma, Desire, and the Latent Impressions — Vāsanās"),
    (4, 12, 14,"Time, the Object, and the Guṇas"),
    (4, 15, 17,"Mind and Object — the Object's Independence"),
    (4, 18, 21,"The Mind Is Known; the Puruṣa Is the Knower"),
    (4, 22, 26,"The Mind Turned Toward Liberation"),
    (4, 27, 30,"Breaks in Discrimination and the Cloud of Virtue"),
    (4, 31, 34,"Infinite Knowledge and the Aloneness of Kaivalya"),
]


def load_sutras():
    by_key = {}
    for f in glob.glob(os.path.join(SRC, "*.yml")):
        m = re.search(r"ys_(\d)_(\d+)\.yml$", f)
        if m:
            by_key[(int(m.group(1)), int(m.group(2)))] = yaml.safe_load(open(f))
    return by_key


def marker(p, n):
    return f"{str(p).translate(DEV)}.{str(n).translate(DEV)}"


def merge(cluster, by_key):
    pada, a, b, title = cluster
    members = [(n, by_key[(pada, n)]) for n in range(a, b + 1) if (pada, n) in by_key]
    dev, iast, trans, comm, practices, insights = [], [], [], [], [], []
    themes, tags = [], []
    for n, d in members:
        dv = _as_text(d.get("sanskrit_devanagari")).strip()
        if dv:
            dev.append(f"{dv} ॥ {marker(pada, n)} ॥")
        iw = _as_text(d.get("sanskrit_iast")).strip()
        if iw:
            iast.append(f"{iw} || {pada}.{n} ||")
        tr = _as_text(d.get("translation") or d.get("translation_literal")).strip()
        if tr:
            trans.append(f"**{pada}.{n}** {tr}")
        cm = _strip_layer_tail(_as_text(d.get("commentary"))).strip()
        if cm:
            comm.append(f"**Sūtra {pada}.{n}**\n\n{cm}")
        pr = _as_text(d.get("practice") or d.get("abhyasa")).strip()
        if pr:
            practices.append(pr)
        ins = _as_text(d.get("insight")).strip()
        if ins:
            insights.append(ins)
        for t in (d.get("themes") or []):
            if t not in themes:
                themes.append(t)
        for t in (d.get("tags") or []):
            if t not in tags:
                tags.append(t)

    lead = members[0][1]
    rng = f"{pada}_{a:02d}" if a == b else f"{pada}_{a:02d}_{b:02d}"
    out = {
        "source_file": f"data/canonical/patañjali_yoga_sūtras (clustered {pada}.{a}-{pada}.{b})",
        "source_id": f"YS_{rng.upper()}",
        "category": "root_text",
        "work_id": "patañjali_yoga_sūtras",
        "work_title": "Patañjali Yoga Sūtras",
        "unit_id": f"patañjali_yoga_sūtras.ys_{rng}",
        "unit_label": title,
        "title": title,
        "unit_type": "sutra_cluster",
        "sutra_range": f"{pada}.{a}-{pada}.{b}",
        "sanskrit_devanagari": "\n\n".join(dev),
        "sanskrit_iast": "\n\n".join(iast),
        "translation_literal": "\n".join(trans),
        "commentary": "\n\n".join(comm),
        "insight": max(insights, key=len) if insights else "",
        "practice": max(practices, key=len) if practices else "",
        "themes": themes,
        "tags": tags,
        "needs_commentary_reauthor": True,  # flag for the unified-commentary pass
        "provenance": lead.get("provenance"),
        "editorial_maturity": "strong_draft",
    }
    return out


def main():
    write = "--write" in sys.argv
    by_key = load_sutras()
    covered = set()
    if write:
        os.makedirs(STAGE, exist_ok=True)
    rows = []
    for c in CLUSTERS:
        pada, a, b, title = c
        for n in range(a, b + 1):
            covered.add((pada, n))
        unit = merge(c, by_key)
        norm = normalize_unit(unit, "")
        kinds = [L["kind"] for L in norm.get("pratibha_layers", [])]
        rows.append((unit["sutra_range"], len(unit["translation_literal"]), len(unit["commentary"]), kinds, title))
        if write:
            fn = unit["unit_id"].split(".")[-1]
            with open(os.path.join(STAGE, f"patañjali_yoga_sūtras_{fn}.yml"), "w") as fh:
                yaml.safe_dump(unit, fh, allow_unicode=True, sort_keys=False, width=120)
    # coverage check
    allk = set(by_key.keys())
    missing = sorted(allk - covered)
    print(f"clusters: {len(CLUSTERS)}  (from {len(allk)} sūtras)")
    print(f"coverage: {len(covered)}/{len(allk)}  missing={missing}")
    print("sample cluster ranges (range | trans_chars | comm_chars | layers):")
    for r in rows[:6] + rows[-3:]:
        print(f"  {r[0]:9} | tr={r[1]:4} | cm={r[2]:5} | {r[3]}")
    if write:
        print(f"WROTE {len(CLUSTERS)} cluster files to {STAGE}")


if __name__ == "__main__":
    main()
