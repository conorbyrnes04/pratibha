#!/usr/bin/env python3
"""Merge duplicate texts: normalize provenance.collection / collection / work_title
so each canonical dir presents as ONE collection on the shelf."""
import glob, sys, yaml
sys.path.insert(0, "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha")
from app.collection_aliases import canonical_slug  # noqa

ROOT = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha/data/canonical"

TARGETS = {
    "marcus_aurelius_meditations": "Marcus Aurelius — Meditations",
    "epictetus_works": "Epictetus — Enchiridion",
    "nagarjuna_mulamadhyamakakarika": "Mūlamadhyamakakārikā (Nāgārjuna)",
    "katha_upanishad": "Kaṭha Upaniṣad",
    "parmenides_fragments": "Parmenides — On Nature",
    "phaedo_plato": "Phaedo (Plato)",
    "milarepa_songs": "Songs of Milarepa",
    "svetasvatara_upanishad": "Śvetāśvatara Upaniṣad",
    "pseudo_dionysius": "Pseudo-Dionysius — The Divine Names",
}

apply = "--write" in sys.argv


def main():
    for d, name in TARGETS.items():
        files = glob.glob(f"{ROOT}/{d}/*.yml")
        changed = 0
        for f in files:
            u = yaml.safe_load(open(f, encoding="utf-8")) or {}
            prov = u.get("provenance")
            dirty = False
            if isinstance(prov, dict) and prov.get("collection") != name:
                prov["collection"] = name
                dirty = True
            if u.get("collection") not in (None, name) or (u.get("collection") and u.get("collection") != name):
                if u.get("collection") is not None:
                    u["collection"] = name
                    dirty = True
            if u.get("work_title") and u.get("work_title") != name:
                u["work_title"] = name
                dirty = True
            if dirty:
                changed += 1
                if apply:
                    with open(f, "w", encoding="utf-8") as fh:
                        yaml.safe_dump(u, fh, allow_unicode=True, sort_keys=False, width=100)
        cslug = canonical_slug(name)
        flag = "OK" if cslug == d else f"!! canonical_slug -> {cslug} (need alias -> {d})"
        print(f"{d}: -> {name!r} | {changed}/{len(files)} units {'rewritten' if apply else 'to change'} | {flag}")


if __name__ == "__main__":
    main()
