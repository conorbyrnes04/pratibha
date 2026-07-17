#!/usr/bin/env python3
"""Pre-generate cohesive imagery for the Pratibha web app.

Two families of assets:
  - thangka: Himalayan-thangka style (primary collection art / page BGs)
  - nature: photographic natural landscapes that the UI rotates randomly

Images are text-to-image generations from fal.ai (fal-ai/flux/dev) saved as
static assets under web/public/generated/ so the app never calls fal at runtime.

Usage:
    .venv/bin/python scripts/generate_fal_images.py            # generate missing
    .venv/bin/python scripts/generate_fal_images.py --force    # regenerate all
    .venv/bin/python scripts/generate_fal_images.py --family nature
    .venv/bin/python scripts/generate_fal_images.py --only daoism-n01 daoism-n02
    .venv/bin/python scripts/generate_fal_images.py --list

Requires FAL_KEY in .env (format id:secret). The key is never printed.
"""

from __future__ import annotations

import argparse
import os
import sys
import time
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = REPO_ROOT / ".env"
OUT_DIR = REPO_ROOT / "web" / "public" / "generated"

MODEL = "fal-ai/flux/dev"

# The style spine — used VERBATIM for every thangka image.
BASE_PROMPT = (
    "Sacred contemplative artwork in the style of a Himalayan thangka reimagined: "
    "precise hand-drawn linework with fine gold outlines and iconometric symmetry, "
    "translucent layers of luminous anatomy and subtle-body energy channels glowing "
    "from within, rendered in traditional mineral pigments — deep lapis blue, "
    "malachite green, cinnabar red, bone white, burnished gold leaf — on an aged "
    "indigo ground. Meditative, austere, radiant. No text, no faces of specific "
    "deities, museum-quality detail, symmetrical composition."
)

# Photographic style for rotating natural settings (library banner / thumbs).
NATURE_PROMPT = (
    "Cinematic still photography of a real natural landscape, contemplative and "
    "quiet, soft volumetric mist, rich deep tones that suit a dark UI "
    "(indigo shadow, amber rim light, cool teal midtones), shallow depth of field, "
    "no people, no buildings, no text, no logos, no statues, no faces, empty of "
    "human presence, National Geographic quality, 35mm film grain."
)

# size presets accepted by flux/dev
SQUARE = "square_hd"          # 1024x1024 — collection art / tiles
WIDE = "landscape_16_9"       # 1024x576  — page background banners

# Shared steer away from the figurative bias that Flux tends to add when the
# style spine mentions "luminous anatomy". Appended to every motif clause.
_NO_FIGURE = (
    " The ONLY subjects are sacred objects, animals, geometry, or landscape — "
    "absolutely no human figures, no seated meditators, no faces, no bodies, "
    "no silhouettes of people."
)

# {slug, motif clause, image_size, family}
# Mix target: ~50% sacred objects/symbols, ~30% animals, ~20% landscape/abstract.
MANIFEST: list[dict[str, str]] = [
    # ── Page backgrounds (~20% landscape / abstract subtle-body) ──
    {"slug": "bg-hero", "size": WIDE, "family": "thangka",
     "motif": "Wide landscape sacred still-life ONLY: a golden butter lamp with a tall flame rising from a lotus of concentric bindu-light rings. No person, no meditator, no face, no body — lamp, lotus, and light geometry alone"
              + _NO_FIGURE},
    {"slug": "bg-library", "size": WIDE, "family": "thangka",
     "motif": "Wide landscape sacred still-life ONLY: a pair of deer flanking a golden dharma wheel before rows of luminous palm-leaf manuscripts. Animals and objects only"
              + _NO_FIGURE},
    {"slug": "bg-paths", "size": WIDE, "family": "thangka",
     "motif": "Wide landscape of pure abstract subtle-body geometry ONLY: a vertical column of glowing chakra circles along a luminous central channel drawn as gold rings and lines. No body, no silhouette — geometry alone"
              + _NO_FIGURE},
    {"slug": "bg-sources", "size": WIDE, "family": "thangka",
     "motif": "Wide landscape sacred still-life ONLY: an open illuminated manuscript flanked by offering bowls and a conch shell. Objects only"
              + _NO_FIGURE},

    # ── Per-tradition art ──
    # Objects / symbols (~50%)
    {"slug": "heart-sutra", "size": SQUARE, "family": "thangka",
     "motif": "central motif ONLY: a radiant pink lotus beneath aniconic seed-syllable geometry of concentric rings and a single bindu — no letters, no person"
              + _NO_FIGURE},
    {"slug": "nagarjuna", "size": SQUARE, "family": "thangka",
     "motif": "central motif ONLY: a large interlocking endless knot (śrīvatsa) of two-truths symmetry in burnished gold lattice, reflecting itself — no person"
              + _NO_FIGURE},
    {"slug": "upanishads", "size": SQUARE, "family": "thangka",
     "motif": "central motif: a pūrṇa-kumbha kalasha vase overflowing with lotus and concentric mandala light"
              + _NO_FIGURE},
    {"slug": "astavakra", "size": SQUARE, "family": "thangka",
     "motif": "central motif ONLY: a round polished mirror of still water reflecting stars and open sky — object only, no person"
              + _NO_FIGURE},
    {"slug": "kashmir-saiva", "size": SQUARE, "family": "thangka",
     "motif": "central motif ONLY: a golden trident (triśūla) crossed with a vajra (dorje) and a bell (ghanta), surrounded by concentric spanda ripples — ritual implements only, no person"
              + _NO_FIGURE},
    {"slug": "shantideva", "size": SQUARE, "family": "thangka",
     "motif": "Still-life of sacred ritual objects only: a large bronze alms bowl in the center, a white stupa behind it, mala beads coiled in a circle, three butter lamps with flames. Absolutely empty of people — no monk, no Buddha figure, no meditator, no face, no body, no hands"
              + _NO_FIGURE},
    {"slug": "plotinus", "size": SQUARE, "family": "thangka",
     "motif": "central motif ONLY: concentric rings of light and yantra-like triangle symmetry radiating from a single luminous bindu — pure geometry, no person"
              + _NO_FIGURE},
    {"slug": "default", "size": SQUARE, "family": "thangka",
     "motif": "central motif ONLY: a radiant eight-petaled lotus mandala with a central bindu of pure light — flower and geometry only, no person"
              + _NO_FIGURE},

    # Animals (~30%)
    {"slug": "milarepa", "size": SQUARE, "family": "thangka",
     "motif": "central motif: a snow lion before a Himalayan mountain cave under a star-filled sky"
              + _NO_FIGURE},
    {"slug": "tilopa", "size": SQUARE, "family": "thangka",
     "motif": "central motif: a single soaring garuda in a vast open sky of clear light and clouds"
              + _NO_FIGURE},
    {"slug": "patanjali", "size": SQUARE, "family": "thangka",
     "motif": "central motif ONLY: a coiled nāga serpent perfectly stilled in a spiral around a luminous bindu — serpent only, no person"
              + _NO_FIGURE},
    {"slug": "heraclitus", "size": SQUARE, "family": "thangka",
     "motif": "central motif ONLY: a spiraling dragon of living fire coiled through a river of flame — dragon only, no person"
              + _NO_FIGURE},

    # Landscape (~20%)
    {"slug": "daoism", "size": SQUARE, "family": "thangka",
     "motif": "central motif: flowing water winding through mist-veiled valleys and rounded mountains, a solitary crane above"
              + _NO_FIGURE},
]

# Natural landscape variants the UI rotates through (slug-n01 … slug-n03).
# Motifs stay photographic; NATURE_PROMPT supplies the shared look.
NATURE_VARIANTS: dict[str, list[str]] = {
    "daoism": [
        "Mist-veiled karst mountains reflected in a still river at dawn, a lone crane silhouette far away",
        "Bamboo grove fading into soft fog, shafts of amber morning light through green stalks",
        "Empty mountain path winding beside a clear stream under layered blue ridges",
    ],
    "upanishads": [
        "Vast Ganges-like river plain at golden hour, endless sky meeting quiet water",
        "Banyan canopy over a still forest pool, dappled light on dark water",
        "Open monsoon sky after rain over green fields and distant blue hills",
    ],
    "heart-sutra": [
        "Pink lotus pads on a glassy lake at first light, empty of boats",
        "High Himalayan valley lake under a pale dawn sky, windless surface",
        "Soft mist rising from a reed marsh with floating lotus buds",
    ],
    "nagarjuna": [
        "Mirror-still alpine lake reflecting inverted peaks and empty sky",
        "Fog erasing the boundary between sea and cloud on a rocky shore",
        "Bare winter forest reflected in a black ice-rimmed pond",
    ],
    "astavakra": [
        "Starfield mirrored in an utterly still high-altitude lake at night",
        "Clear desert sky over a salt flat that acts as a perfect mirror",
        "Open ocean horizon at twilight with no boats, sky doubling in water",
    ],
    "kashmir-saiva": [
        "Snow peaks above a Kashmir valley meadow at blue hour",
        "Rushing mountain river through dark conifers under storm light",
        "High meadow wildflowers against distant ice ridges at sunset",
    ],
    "shantideva": [
        "Quiet monastery-adjacent pine forest path in soft rain, empty",
        "Terraced hillside of green under low monsoon clouds",
        "Stone-lined mountain spring emerging into moss and fern",
    ],
    "plotinus": [
        "Mediterranean cliff coast at dusk, sea becoming a sheet of bronze light",
        "Olive grove hills fading into violet evening haze",
        "Clear night sky over a silent rocky headland",
    ],
    "milarepa": [
        "Sheer Himalayan cliff face and snow cave mouth under cold starlight",
        "Wind-scoured high plateau with distant white peaks at sunrise",
        "Alpine glacier tongue under a deep indigo sky",
    ],
    "tilopa": [
        "Open sky over endless grasslands with a single bird far above",
        "Thunderheads breaking over a wide river plain at golden hour",
        "Clear high-altitude blue sky above rolling cloud seas",
    ],
    "patanjali": [
        "Serpentine river cutting through layered canyon walls at dawn",
        "Still yoga-like balance of rock pillar and empty desert sky",
        "Coiled roots of an ancient tree beside a quiet forest stream",
    ],
    "heraclitus": [
        "River of living fire-colored autumn leaves under moving water",
        "Volcanic steam vents along a dark rocky coastline at dusk",
        "Bonfire-colored sunset reflected in a fast-moving mountain torrent",
    ],
    "default": [
        "Quiet mountain lake at blue hour with soft mist on the water",
        "Ancient forest path lit by low amber side-light, empty of people",
        "Rolling hills under a vast contemplative sky after rain",
    ],
    "bg-library": [
        "Wide view of misty mountain library of ridges fading into fog at dawn",
        "Wide empty reading-room of nature: still lake, distant peaks, soft light",
        "Wide bamboo and pine forest corridor opening onto a bright valley",
    ],
    "bg-hero": [
        "Wide contemplative sunrise over layered mountain ridges in soft mist",
        "Wide still lake catching first amber light under indigo sky",
        "Wide coastal cliffs and open ocean at blue hour, empty horizon",
    ],
    "bg-paths": [
        "Wide winding mountain trail through high meadows toward distant peaks",
        "Wide forked paths in a misty forest clearing, soft golden light",
        "Wide ridge walk above cloud valleys under clear morning sky",
    ],
    "bg-sources": [
        "Wide high spring source pouring into a clear mountain stream",
        "Wide canyon mouth where a river begins under desert light",
        "Wide waterfall veil into a deep green gorge, soft mist spray",
    ],
}

for _base, _motifs in NATURE_VARIANTS.items():
    _size = WIDE if _base.startswith("bg-") else SQUARE
    for _i, _motif in enumerate(_motifs, start=1):
        MANIFEST.append(
            {
                "slug": f"{_base}-n{_i:02d}",
                "size": _size,
                "family": "nature",
                "motif": _motif,
            }
        )


def load_fal_key() -> str:
    """Read FAL_KEY from the environment or .env. Never print it."""
    key = os.environ.get("FAL_KEY")
    if key:
        return key.strip()
    if ENV_PATH.exists():
        for raw in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            name, _, value = line.partition("=")
            if name.strip() == "FAL_KEY":
                value = value.strip().strip('"').strip("'")
                return value
    raise SystemExit("FAL_KEY not found in environment or .env — aborting.")


def build_prompt(entry: dict[str, str]) -> str:
    # Motif first so Flux privileges the named subject over the style spine.
    spine = NATURE_PROMPT if entry.get("family") == "nature" else BASE_PROMPT
    return f"{entry['motif']}. {spine}"


def download(url: str, dest: Path) -> None:
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    with urllib.request.urlopen(url, timeout=120) as resp:
        tmp.write_bytes(resp.read())
    tmp.replace(dest)


def generate_one(fal_client, entry: dict[str, str], dest: Path, attempts: int = 3) -> bool:
    prompt = build_prompt(entry)
    for attempt in range(1, attempts + 1):
        try:
            result = fal_client.subscribe(
                MODEL,
                arguments={
                    "prompt": prompt,
                    "image_size": entry["size"],
                    "num_inference_steps": 34,
                    "guidance_scale": 4.0,
                    "num_images": 1,
                    "output_format": "jpeg",
                    "enable_safety_checker": True,
                },
                with_logs=False,
            )
            images = (result or {}).get("images") or []
            if not images or not images[0].get("url"):
                raise RuntimeError("no image url in fal response")
            download(images[0]["url"], dest)
            return True
        except Exception as exc:  # noqa: BLE001 — report and retry
            print(f"    attempt {attempt}/{attempts} failed: {exc}")
            if attempt < attempts:
                time.sleep(3 * attempt)
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="regenerate even if the file exists")
    parser.add_argument("--only", nargs="+", metavar="SLUG", help="only generate these slug(s)")
    parser.add_argument(
        "--family",
        choices=("thangka", "nature", "all"),
        default="all",
        help="limit generation to one asset family (default: all)",
    )
    parser.add_argument("--list", action="store_true", help="print the manifest and exit")
    args = parser.parse_args()

    if args.list:
        for e in MANIFEST:
            fam = e.get("family", "thangka")
            print(f"{e['slug']:<18} [{fam:<7}] [{e['size']}]  {e['motif'][:90]}")
        return 0

    entries = MANIFEST
    if args.family != "all":
        entries = [e for e in entries if e.get("family", "thangka") == args.family]
    if args.only:
        wanted = set(args.only)
        entries = [e for e in entries if e["slug"] in wanted]
        missing = wanted - {e["slug"] for e in entries}
        if missing:
            print(f"Unknown slug(s): {', '.join(sorted(missing))}")
            return 2

    os.environ["FAL_KEY"] = load_fal_key()  # consumed by fal_client, not printed
    import fal_client  # noqa: PLC0415 — imported after key is set

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    generated, skipped, failed = [], [], []
    for e in entries:
        dest = OUT_DIR / f"{e['slug']}.jpg"
        if dest.exists() and not args.force:
            skipped.append(e["slug"])
            print(f"skip  {e['slug']} (exists)")
            continue
        print(f"gen   {e['slug']} [{e.get('family', 'thangka')}/{e['size']}] ...")
        if generate_one(fal_client, e, dest):
            generated.append(e["slug"])
            print(f"  ok  -> {dest.relative_to(REPO_ROOT)}")
        else:
            failed.append(e["slug"])
            print(f"  FAIL {e['slug']}")

    print("\n── summary ──")
    print(f"generated: {len(generated)} {generated}")
    print(f"skipped:   {len(skipped)} {skipped}")
    print(f"failed:    {len(failed)} {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
