#!/usr/bin/env python3
"""Generate new sumi ink marks from the Replicate SUMI LoRA and vectorize them.

Uses conorbyrnes04/sumi (same account/pipeline as Mythra Glyphnet).
Requires REPLICATE_API_TOKEN in .env. The token is never printed.

Usage:
    .venv/bin/python scripts/generate_sumi_glyphs.py
    .venv/bin/python scripts/generate_sumi_glyphs.py --only dragon mountain
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps, ImageStat

REPO = Path(__file__).resolve().parent.parent
ENV_PATH = REPO / ".env"
RAW_DIR = REPO / "assets" / "sumi" / "_generated"
SVG_DIR = REPO / "assets" / "sumi" / "svg"
PUBLIC_DIR = REPO / "web" / "public" / "sumi"

SUMI_MODEL = "conorbyrnes04/sumi:d776a9d3c801d49af5b31a9b7553f5d405d33429d39be50e6e749e43726e2222"

STYLE = (
    "sumi-e ink painting, black ink brush on white rice paper, single centered motif, "
    "calligraphic brushstrokes, high contrast, empty corners, "
    "absolutely no text, no letters, no signature, no artist name, no red seal, "
    "no hanko, no stamp, no background scenery, no human face, no photorealism, "
    "icon-ready silhouette"
)

MANIFEST: list[dict[str, str]] = [
    {"slug": "dragon", "subject": "a Chinese dragon in profile, coiled, whiskers and spine, ink brush"},
    {"slug": "mountain", "subject": "a single mountain peak with a few contour strokes"},
    {"slug": "void", "subject": "an open ensō circle, one broken brush ring, emptiness"},
    {"slug": "heart", "subject": "a simple ink heart-shape made of two brush petals, not an emoji"},
    {"slug": "yantra", "subject": "a Sri Yantra of interlocking triangles inside a circle"},
    {"slug": "mirror", "subject": "a round bronze-mirror disk with a simple rim and center boss"},
    {"slug": "tides", "subject": "two horizontal ocean waves, one above the other, rolling left to right, not a spiral"},
    {"slug": "shiva", "subject": "a ritual trident staff, three sharp prongs on a vertical pole, no person, no walking figure"},
    {"slug": "chalice", "subject": "a simple grail cup on a stem, one vessel"},
    {"slug": "vishnu", "subject": "a sudarshana chakra, circular discus with many radiating spokes like a sun-wheel, no person"},
    # Deity emblems — same slugs as the Celtic Glyphnet pantheon. Prompt the
    # attribute, never the body: this LoRA collapses into walking figures.
    {"slug": "zeus", "subject": "a zigzag lightning bolt from top to bottom, three sharp forks like a thunder rune, no person"},
    {"slug": "hera", "subject": "a single peacock feather with one eye-spot, upright plume, no bird body, no person"},
    {"slug": "athena", "subject": "a crested Greek helmet next to a small owl, no person"},
    {"slug": "apollo", "subject": "a Greek lyre musical instrument, two curved horns and visible strings, clearly a harp, no person"},
    {"slug": "artemis", "subject": "a simple archery bow with a taut string and one nocked arrow, plus a crescent moon, no person"},
    {"slug": "hades", "subject": "a two-pronged bident staff standing vertical, no person"},
    {"slug": "persephone", "subject": "a single pomegranate fruit split open showing seeds, no person"},
    {"slug": "dionysus", "subject": "a grape cluster on a vine beside a pine-cone tipped thyrsus staff, no person"},
    {"slug": "eros", "subject": "a small bow and one arrow crossed, no person, no cherub, no face"},
    {"slug": "brahma", "subject": "a four-petaled lotus with a water-pot, no person, no faces"},
    {"slug": "kali", "subject": "a curved sickle sword, crescent blade on a short handle, a small skull beside it, no person, no face"},
    {"slug": "durga", "subject": "a lion in profile with a spear and a small trident, no human rider"},
    {"slug": "lakshmi", "subject": "an open lotus with a overflowing pot of coins, no person"},
    {"slug": "saraswati", "subject": "an Indian veena lute with a long neck and two gourds, no person"},
    {"slug": "ganesha", "subject": "an elephant head in left profile only, huge fan-shaped ear, long curling trunk, one broken tusk, clearly an elephant skull, no human body, no walking figure, no seated god"},
    {"slug": "isis", "subject": "outstretched protective wings around an ankh loop, no person, no face"},
    {"slug": "osiris", "subject": "a djed pillar, stacked vertebrae column, with crook and flail crossed, no person"},
    {"slug": "horus", "subject": "a falcon in profile wearing a sun disk, no person"},
    {"slug": "anubis", "subject": "a jackal or wild dog head facing left, long pointed ears and snout, clearly a canine, no human body"},
    {"slug": "thoth", "subject": "an ibis bird in profile with a long curved beak and a moon disk, no person"},
    {"slug": "odin", "subject": "two ravens facing a vertical spear, no person, no face"},
    {"slug": "thor", "subject": "Mjolnir, a short-handled war hammer with a squared head, no person"},
    {"slug": "freyja", "subject": "a necklace of linked jewels with a falcon wing, no person"},
    {"slug": "loki", "subject": "two intertwined serpents knotted like flame, no person"},
    {"slug": "oshun", "subject": "a ceremonial hand-fan and a small brass mirror above a river curve, no person"},
    {"slug": "shango", "subject": "a double-headed stone axe, two blades on one haft, no person"},
    {"slug": "yemaya", "subject": "a cowrie-shell crescent over rolling ocean waves, no person"},
    {"slug": "quetzalcoatl", "subject": "a feathered serpent in profile, quetzal plumes along a snake body, no person"},
    {"slug": "tezcatlipoca", "subject": "a round smoking obsidian mirror disk with a wisp of smoke, no person"},
    {"slug": "nuwa", "subject": "a coiled Chinese serpent mending a cracked sky-dome, no person, no face"},
    {"slug": "thanatos", "subject": "an inverted extinguished torch, flame pointing down, no person"},
    {"slug": "thunderbird", "subject": "a thunderbird with outstretched wings and a lightning bolt, no person"},
    # Animals — silhouette first. The LoRA collapses vague names into blobs.
    {"slug": "dolphin", "subject": "a dolphin leaping left to right in profile, arched body, clear dorsal fin and beak, marine mammal silhouette, not a circle, not a blob"},
    {"slug": "bee", "subject": "a honeybee in profile, striped abdomen, two veined wings, small antennae, clearly an insect, no hive, no person"},
    {"slug": "crane", "subject": "a Japanese crane standing on one long leg, long neck and pointed beak, folded wings, clearly a wading bird"},
    {"slug": "crow", "subject": "a crow in left profile, thick beak, fan tail, compact black bird, not a raven pair"},
    {"slug": "deer", "subject": "a doe deer in profile, slender legs, no antlers, alert ears, forest animal silhouette"},
    {"slug": "elephant", "subject": "a full Asian elephant walking left in profile, large ear, trunk reaching the ground, four legs, clearly an elephant body"},
    {"slug": "fish", "subject": "a koi carp swimming left, visible eye, gill, dorsal fin, tail fin and scales, clearly a fish body, not a wave, not a circle, not an ensō"},
    {"slug": "hawk", "subject": "a hawk perched in left profile, hooked beak, folded wings, talons, clearly a raptor bird, not a circle, not an ensō"},
    {"slug": "ox", "subject": "an ox or water buffalo in profile, heavy horns, solid body, four legs, farm animal silhouette"},
    {"slug": "swan", "subject": "a swan floating, S-curved neck, one raised wing, clearly a swan not a duck"},
    {"slug": "tiger", "subject": "a tiger walking left in profile, striped body, long tail, clearly a big cat"},
]


def load_token() -> str:
    token = os.environ.get("REPLICATE_API_TOKEN", "").strip()
    if token:
        return token
    if ENV_PATH.exists():
        for raw in ENV_PATH.read_text(encoding="utf-8").splitlines():
            if raw.startswith("REPLICATE_API_TOKEN="):
                return raw.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("REPLICATE_API_TOKEN not found in environment or .env")


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    with urllib.request.urlopen(url, timeout=180) as resp:
        tmp.write_bytes(resp.read())
    tmp.replace(dest)


def output_url(output) -> str:
    first = output[0] if isinstance(output, list) else output
    if isinstance(first, str):
        return first
    return getattr(first, "url", None) or str(first)


def throttle_wait(exc: Exception, fallback: float = 12.0) -> float:
    text = str(exc)
    match = re.search(r"resets in ~(\d+)s", text)
    if match:
        return max(float(match.group(1)) + 1.0, 2.0)
    if "429" in text or "throttled" in text.lower():
        return fallback
    return 0.0


def generate(slug: str, subject: str, dest: Path, attempts: int = 8) -> None:
    import replicate

    prompt = f"sumi {subject}. {STYLE}"
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        print(f"gen   {slug} …" + (f" (retry {attempt})" if attempt > 1 else ""))
        try:
            output = replicate.run(
                SUMI_MODEL,
                input={
                    "prompt": prompt,
                    "output_format": "png",
                    "model": "dev",
                    "go_fast": False,
                    "lora_scale": 1,
                    "megapixels": "1",
                    "num_outputs": 1,
                    "aspect_ratio": "1:1",
                    "guidance_scale": 3,
                    "output_quality": 90,
                    "num_inference_steps": 28,
                },
            )
            download(output_url(output), dest)
            print(f"  ok  {dest.relative_to(REPO)}")
            time.sleep(11)
            return
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            wait_for = throttle_wait(exc)
            print(f"  wait {slug}: {exc}")
            if wait_for:
                print(f"  sleep {wait_for:.0f}s")
                time.sleep(wait_for)
                continue
            if attempt < attempts:
                time.sleep(3)
    raise last_error or RuntimeError(f"{slug} failed")


def prepare_pbm(png: Path, pbm: Path) -> None:
    img = Image.open(png).convert("L")
    # Drop corner seals / signatures the LoRA sometimes adds.
    w, h = img.size
    m = int(min(w, h) * 0.08)
    img = img.crop((m, m, w - m, h - m))
    corners = ImageStat.Stat(img.crop((0, 0, 24, 24))).mean[0]
    if corners < 80:
        img = ImageOps.invert(img)
    img = ImageOps.autocontrast(img)
    img.point(lambda p: 0 if p < 168 else 255).save(pbm)


def vectorize(png: Path, svg: Path) -> None:
    pbm = png.with_suffix(".pbm")
    prepare_pbm(png, pbm)
    subprocess.run(
        [
            "potrace",
            str(pbm),
            "--svg",
            "-o",
            str(svg),
            "--turdsize",
            "2",
            "--alphamax",
            "1.0",
            "--opttolerance",
            "0.4",
        ],
        check=True,
    )
    pbm.unlink(missing_ok=True)
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    (PUBLIC_DIR / svg.name).write_bytes(svg.read_bytes())
    print(f"  svg {svg.relative_to(REPO)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", nargs="+")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    os.environ["REPLICATE_API_TOKEN"] = load_token()
    wanted = {s.lower() for s in args.only} if args.only else None
    entries = [e for e in MANIFEST if wanted is None or e["slug"] in wanted]
    if wanted:
        missing = wanted - {e["slug"] for e in entries}
        if missing:
            print(f"unknown slug(s): {', '.join(sorted(missing))}")
            return 2

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    SVG_DIR.mkdir(parents=True, exist_ok=True)

    failed = []
    for entry in entries:
        slug = entry["slug"]
        png = RAW_DIR / f"{slug}.png"
        svg = SVG_DIR / f"{slug}.svg"
        public = PUBLIC_DIR / f"{slug}.svg"
        if public.exists() and not args.force:
            print(f"skip  {slug} (exists)")
            continue
        try:
            generate(slug, entry["subject"], png)
            vectorize(png, svg)
        except Exception as exc:  # noqa: BLE001
            print(f"  FAIL {slug}: {exc}")
            failed.append(slug)
    print(f"failed: {failed or 'none'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
