#!/usr/bin/env python3
"""Add an insider Yoruba source: curated passages from Rev. Samuel Johnson's
The History of the Yorubas (1921) — a Yoruba clergyman's own account of his
people's religion and worldview, balancing A.B. Ellis's outsider record.

Transcribed faithfully from the public-domain 1921 scan (light correction of OCR
artifacts + whitespace). Ceremonial/secret material (Egúngún mysteries, sacrifice
mechanics) is deliberately excluded. Study rendering pending review by
tradition-bearers.
"""
import os
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data/canonical/johnson_yoruba_religion")
COLL = "The Yoruba Faith (Samuel Johnson)"

PROV = ("Original text by Rev. Samuel Johnson (a Yoruba clergyman), The History of the Yorubas "
        "(completed c. 1897; published 1921; public domain). An insider Yoruba account, transcribed "
        "from the 1921 scan with light correction of OCR artifacts. Study rendering pending review by "
        "tradition-bearers.")
NOTE = ("Rev. Samuel Johnson was a Yoruba clergyman; this is an insider Yoruba account of his people's "
        "traditional religion and worldview — a complement to the outsider record of A.B. Ellis. A living "
        "tradition: ceremonial and secret material (e.g. the Egúngún mysteries) is deliberately excluded. "
        "Offered as a study reading pending review by Yoruba tradition-bearers.")

PASSAGES = [
    ("Olorun, the Lord of Heaven",
     "The Yorubas believe in the existence of an Almighty God, whom they term Olorun — that is, Lord of "
     "Heaven. They acknowledge Him as Maker of heaven and earth, but as too exalted to concern Himself "
     "directly with men and their affairs; hence they admit the existence of many gods as intermediaries, "
     "and these they term Orisas."),
    ("The Name Reserved for God Alone",
     "The term Olorun is applied to God alone, and is never used in the plural to denote the Orisas. Kings "
     "and the great ones of the earth may sometimes be called Orisas by way of eulogy; but the term Olorun "
     "is reserved for the Great God alone."),
    ("An Account at the Portals of Heaven",
     "They believe in a future judgment, as may be inferred from the adage: “Whatever we do on earth, we "
     "shall give an account thereof at the portals of heaven.”"),
    ("Father Has Come Again",
     "They believe also in the transmigration of souls — that after a period of time, deceased parents are "
     "born again into the family of their surviving children. It is from this notion that some children are "
     "named Babatunde, ‘Father has come again,’ and Yetunde, ‘Mother has come again.’"),
    ("Shaped by the Hand of Orisala",
     "To Orisala are ascribed creative powers; he is regarded as a co-worker with Olorun. Man is supposed "
     "to have been made by God in a lump, and shaped as he is by Orisala."),
    ("The Ori: the Head as Destiny",
     "The Ori — the head — is the universal household deity, worshipped by both sexes as the god of fate. "
     "It is believed that good or ill fortune attends one according to the decree of this god; and hence it "
     "is propitiated, that good fortune might be the share of its votary."),
    ("Ogun, God of Iron",
     "Ogun is the god of war, and all instruments made of iron are consecrated to him; hence Ogun is the "
     "blacksmiths' god."),
    ("A Vision of the Great God",
     "A young man once fell into a swoon, and having revived, related the vision he had seen. He saw the "
     "Great God seated upon a throne, covered with a flowing garment, attended on His right hand and His "
     "left by Orisala and Ifa, His counsellors."),
]


def build():
    os.makedirs(OUT, exist_ok=True)
    slug = "johnson_yoruba_religion"
    for i, (title, body) in enumerate(PASSAGES, 1):
        uid = f"{slug}.{slug}_{i:03d}"
        unit = {
            "source_id": f"{slug}_{i:03d}".upper(),
            "category": "root_text",
            "work_id": slug,
            "work_title": COLL,
            "unit_id": uid,
            "unit_label": title,
            "title": title,
            "unit_type": "reflection",
            "commentary": "",
            "themes": ["yoruba", "the divine", "destiny"],
            "tags": [slug, "yoruba", "the divine", "destiny"],
            "quality_score": 0,
            "editorial_score": 0,
            "editorial_maturity": "strong_draft",
            "translation_provenance": PROV,
            "pratibha_layers": [{"kind": "original", "label": "Original", "body": body}],
            "provenance": {"collection": COLL, "section": "Religion", "cultural_context": NOTE},
            "original": body,
        }
        with open(os.path.join(OUT, f"{uid.replace('.', '_')}.yml"), "w", encoding="utf-8") as fh:
            yaml.safe_dump(unit, fh, allow_unicode=True, sort_keys=False, width=100)
    return len(PASSAGES)


if __name__ == "__main__":
    print("johnson yoruba:", build(), "passages")
