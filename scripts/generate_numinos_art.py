#!/usr/bin/env python3
"""Generate Red Book (Jungian) collection art from the conorbyrnes04/numinos
Flux LoRA (trigger word NUMINOS) on Replicate.

Mirrors scripts/generate_sumi_glyphs.py's call pattern. Token read from .env,
never printed. Images saved as web/public/generated/<slug>.jpg (the slugs
collectionImages.ts maps to), so the existing ArtImage backdrops pick them up.

Usage:
    .venv/bin/python scripts/generate_numinos_art.py --test        # 3 probe images
    .venv/bin/python scripts/generate_numinos_art.py --only kashmir-saiva daoism
    .venv/bin/python scripts/generate_numinos_art.py               # full manifest
"""
from __future__ import annotations
import argparse, os, sys, time, urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ENV_PATH = REPO / ".env"
OUT_DIR = REPO / "web" / "public" / "generated" / "redbook"
TEST_DIR = REPO / "scratch" / "numinos_test"

MODEL = "conorbyrnes04/numinos:dd831ba3f3770def1c44353acf1d8795b05f1c74dc9ebc54bc96c85f1118f845"

# The trigger word carries the trained Red Book style; the reinforcement embraces
# the calligraphy as beauty — flowing gilded marginalia in an INVENTED sacred
# alphabet (never real, readable words / modern type), for full Jungian glory.
STYLE = (
    "Carl Jung Red Book Liber Novus illuminated manuscript painting, luminous "
    "visionary mandala ringed by flowing hand-lettered calligraphic script and "
    "gilded marginalia in an invented sacred alphabet, ornate illuminated "
    "initials and knotwork borders, jewel tones, abundant gold leaf, tempera on "
    "vellum, deep lapis indigo, vermilion and ochre, radiant archetypal "
    "symbolism, symmetrical and reverent, no readable words, no modern "
    "typography, no signature"
)

# One Red Book image per collection. `slug` is the ASCII filename; `match` is a
# regex on the collection's display name (unicode/ASCII variants collapse to one
# image); `subject` is the tradition's own archetypal imagery.
MANIFEST: list[dict[str, str]] = [
    {"slug": "senegalese_animism", "match": r"senegalese.?animism|serer|lasnet|pangool", "subject": "Serer cosaan of the Senegambian coast — Roog named as the sky itself, a great baobab as sanctuary, milk and millet poured at the foot of consecrated trees and stones, pangool ancestor-spirits in the living land, a bird carrying a soul at the moment of death, concentric oral teachings ringing an unseen master who has no statue"},
    {"slug": "pulaar_tradition", "match": r"pulaar.?tradition|ful[bɓ]e|peul", "subject": "Fulɓe pastoral cult of the herd — cattle as the remaining shrine, oxen moving across Sahel pasture, a handful of green leaves thrown toward a tomb, a mother consulted before a great act, the honor-face of gravity, concentric cattle-paths ringing a single living cult with no carved idol"},
    {"slug": "pulaar_texts", "match": r"pulaar.?texts|gaden|le.?poular", "subject": "Futa Toro Pulaar living speech — Ajami pages heard rather than dated, a tale that was here and may never be, the cow and the heifer, a heart that is not a joint, the razor of God and the trusting head, concentric mallol proverbs ringing an open ear"},
    {"slug": "futa_jalon_fulde", "match": r"futa.?jalon|fuuta.?jaloo|reichardt", "subject": "Futa Jalon highland Fulde — a Tijani sheikh sitting between the Prophet's tomb and the pulpit, a vacant honor-mat on the ground, a kettle-drum cut in a town where kin are not, tears after victory on a highland ridge, concentric oral traditions ringing a fire whose end is not seen"},
    {"slug": "conference_of_the_birds", "match": r"attar|mantiq|conference.?of.?the.?birds", "subject": "thirty birds arriving at the Simurgh's court on Mount Qaf, a hoopoe crowned as guide, seven valleys of quest love gnosis detachment unity bewilderment and annihilation, a moth circling a candle, a Chinese feather in a picture-gallery, the Simurgh as a mirror in which thirty birds see themselves, concentric Persian couplets ringing a hoopoe and a sun-bird"},
    {"slug": "kashf_al_mahjub", "match": r"hujwir|kashf.?al.?ma[hḥ]j[uū]b", "subject": "unveiling of the veiled — a Persian Sufi handbook, a patched frock and a lifted veil of light, gnosis flashing into the heart, poverty as essence not rags, stations and states as a ladder, audition as a circle of listeners around a lamp, concentric Arabic and Persian pages ringing an opened veil"},
    {"slug": "gospel_of_mary", "match": r"gospel.?of.?mary", "subject": "the Gospel of Mary — Mary Magdalene receiving a hidden teaching after the resurrection, the Human One within not a second Moses, the soul ascending past Wrath as a garment Desire never knew, Levi defending her worth, a Berlin codex with lost pages, concentric Coptic sayings ringing an unwavering mind"},
    {"slug": "new_testament_logia", "match": r"logia of jesus|new.?testament.?logia", "subject": "the living sayings of Jesus — the kingdom within not coming with observation, a single unsplit eye filling the body with light, the Word shining in darkness the dark cannot grasp, a vine and its branches, Father and Son making an abode, two or three gathered, a lamp on a stand, concentric gospel logia ringing the I am"},
    {"slug": "a_course_in_miracles", "match": r"course in miracles|acim", "subject": "a miracle of love and forgiveness — the peace of God, a radiant Christ-light dissolving fear and illusion, the real world shining beyond the ego's dream, boundless abundance overflowing from a single sun of grace"},
    {"slug": "psalms_tehillim", "match": r"psalm|tehillim|psalter", "subject": "the Hebrew psalter — heavens declaring glory with a tent pitched for the sun, a deer panting toward water-courses, deep calling to deep, a weaned child quieted on its mother, the secret place of the Most High, a shepherd's valley, night sky over Zion, concentric psalms ringing a lamp of Torah"},
    {"slug": "lalla_vakyani", "match": r"lalla|lal.?ded|lalleshwari|vakyani|vākyāni", "subject": "Lal Ded of Kashmir — a wandering woman-yogini of recognition, a single inner lamp blazing in the house of the Self, the unstruck sound as a golden bindu, a cotton-flower being carded into cloth of light, dawn over Dal Lake, the Friend waiting, concentric vakhs ringing a naked dance of Śiva"},
    {"slug": "kabbalah_zohar_yetzirah", "match": r"kabbalah|zohar|yetzirah|sephiroth|sefirot", "subject": "the Tree of Life — ten shining Sephiroth linked by twenty-two paths, the concealed Ancient of Days and the four worlds, Hebrew letters of creation blazing in a mystical mandala, the Ein Sof's boundless light"},
    {"slug": "hatha_yoga_pradipika", "match": r"ha[tṭ]ha|pradipika|pradīpikā", "subject": "haṭha yoga — a seated yogi with the kuṇḍalinī serpent ascending the suṣumnā through blazing cakra-lotuses, the sun and moon (haṭha) united, prāṇa as inner fire rising to a thousand-petalled crown of light"},
    {"slug": "siva_samhita", "match": r"[sś]iva.?sa[mṃ]hit[aā]|shiva.?samhita", "subject": "Śiva teaching Pārvatī the subtle body — the vertebral Mount Meru threaded by nāḍīs and cakra-lotuses, kuṇḍalinī coiled at the root, the non-dual light of pure consciousness crowning the microcosm of the body"},
    {"slug": "astavakra_gita", "match": r"a[sṣ]t[aā]vakra|ashtavakra", "subject": "Advaita nonduality — a single boundless eye of pure awareness, the world dissolving into light, the Self as the sole witness reflected in an empty mirror"},
    {"slug": "bhagavad_gita", "match": r"bhagavad", "subject": "Krishna's cosmic universal form (vishvarupa) revealed to Arjuna, a many-armed radiance of suns and worlds above the field of dharma, a war-chariot"},
    {"slug": "brihadaranyaka_upanishad", "match": r"brihadaranyaka|b[rṛ]had[aā]ra[nṇ]yaka", "subject": "the great forest teaching, neti-neti, the Self as the honey of all beings, a cosmic horse of dawn, the imperishable behind the waters"},
    {"slug": "chandogya_upanishad", "match": r"ch[aā]ndogya|khandogya", "subject": "Tat Tvam Asi — thou art that, the invisible Self hidden in the seed of the great banyan, the syllable OM rising as a sun"},
    {"slug": "confucius_analects", "match": r"confucius|analect", "subject": "the ordered cosmos of the sage, ritual propriety and the rectification of names, the pole star still while all stars turn to it, a jade tablet"},
    {"slug": "dhammapada", "match": r"dhammapada", "subject": "the Buddha's path of mind, twin verses of light and shadow, a white lotus rising from still dark water, the turning dharma-wheel"},
    {"slug": "dogen_shobogenzo", "match": r"d[oō]gen|shobogenzo|sh[oō]b[oō]genz[oō]", "subject": "Shobogenzo being-time (uji), the full moon reflected in a single dewdrop, blue mountains constantly walking, zazen in the treasury of the true dharma eye"},
    {"slug": "eastman_soul_of_the_indian", "match": r"soul of the indian|eastman|ohiyesa", "subject": "the Great Mystery over the Dakota plains, silent solitary worship in wild nature, the sun as the Great-Grandfather, an eagle in a jeweled night sky"},
    {"slug": "ecclesiastes_qoheleth", "match": r"ecclesiastes|qoheleth", "subject": "vanity of vanities, the turning of sun and wind and rivers, a broken golden bowl and silver cord, time and season as a great wheel under heaven"},
    {"slug": "epictetus_works", "match": r"epictetus", "subject": "the Stoic dichotomy of control, a serene figure unmoved amid storm, the inner citadel of the will, chains that bind the body but not the mind"},
    {"slug": "gospel_of_thomas", "match": r"gospel of thomas|thomas", "subject": "the hidden living sayings, the kingdom spread upon the earth yet unseen, the light within the seeker, a single eye made whole, twin become one"},
    {"slug": "heart_sutra", "match": r"heart.?s[uū]tra|vajracchedik|diamond.?s[uū]tra|prajn[aā]p[aā]ramit[aā]", "subject": "form is emptiness and emptiness is form, Avalokiteshvara and the perfection of wisdom, gate gate paragate, a luminous void mandala, the diamond that cuts illusion"},
    {"slug": "heraclitus_fragments", "match": r"heraclitus", "subject": "the ever-living cosmic fire, the river never stepped in twice, the hidden logos, the unseen harmony of opposites, flames kindling and going out in measures"},
    {"slug": "isavasya_upanishad", "match": r"isavasya|[iī][sś][aā]v[aā]sya|isha.?upani", "subject": "the Lord enveloping all that moves in the moving world, a golden disk covering the face of truth, the full poured from the full remaining full"},
    {"slug": "katha_upanishad", "match": r"katha|ka[tṭ]ha", "subject": "Nachiketa before Death (Yama) at the threshold, the razor's edge of the secret path, the chariot of the self, the immortal fire hidden in the cave of the heart"},
    {"slug": "ibn_arabi", "match": r"ibn|arabi|know yourself|balyani", "subject": "he who knows himself knows his Lord, the polished mirror of the heart reflecting the divine names, Sufi unity of being, a single point containing all"},
    {"slug": "mandukya_upanishad", "match": r"mandukya|m[aā][nṇ][dḍ][uū]kya|gaudapada|gau[dḍ]ap[aā]da", "subject": "AUM and the four states — waking, dream, deep sleep, and turiya, the syllable as the whole cosmos, silence at the shining center"},
    {"slug": "marcus_aurelius", "match": r"marcus|meditations|aurelius", "subject": "the Stoic view from above, the ruling reason (hegemonikon), a philosopher-emperor beneath the wheeling constellations, memento mori and the cosmic city"},
    {"slug": "meister_eckhart", "match": r"eckhart", "subject": "the birth of God in the ground of the soul, the silent desert of the Godhead (Grunt), detachment, a dark radiant abyss of apophatic light"},
    {"slug": "milarepa_songs", "match": r"milarepa", "subject": "Tibet's great yogi in his mountain cave, the hermit singing dohas of realization, green nettle and the cold moon, the sky-nature of mahamudra"},
    {"slug": "mundaka_upanishad", "match": r"mundaka|mu[nṇ][dḍ]aka", "subject": "the two birds on one tree — one eating the fruit, one only watching, higher and lower knowledge, the arrow of OM piercing the target of Brahman"},
    {"slug": "nagarjuna", "match": r"nagarjuna|n[aā]g[aā]rjuna|madhyamaka|mulamadhyamaka", "subject": "emptiness (shunyata) and dependent origination, the middle way, Indra's net of jewels reflecting endlessly, the serpent-nagas guarding the wisdom"},
    {"slug": "parmenides", "match": r"parmenides", "subject": "the way of truth — Being is, the veiled goddess revealing the unmoving One, a perfect sphere of what-is, the fork of two roads at the gates of night and day"},
    {"slug": "patanjali_yoga_sutras", "match": r"patanjali|pata[nñ]jali|yoga.?s[uū]tra", "subject": "the eight limbs of yoga, the stilling of the mind's whirlpools (vritti), the seer abiding in its own nature, a coiled kundalini serpent ascending"},
    {"slug": "phaedo_plato", "match": r"phaedo|plato", "subject": "the immortality of the soul, the philosopher's serene death, the ascent from the shadow-cave to the sun of the Good, the eternal Forms"},
    {"slug": "plotinus_enneads", "match": r"plotinus|ennead", "subject": "the One and its overflowing emanation, the soul's return to the Source, concentric rings of Nous and World-Soul, ineffable light beyond being"},
    {"slug": "pratyabhijnahrdayam", "match": r"pratyabhij", "subject": "the heart of recognition — Shiva recognizing himself as all things, the pulse of consciousness, a self-recognizing mandala of light"},
    {"slug": "pseudo_dionysius", "match": r"dionysius|divine names", "subject": "the divine darkness of unknowing, the celestial hierarchy of angels in luminous rings, the ray of sacred darkness, the apophatic ascent beyond names"},
    {"slug": "rumi_mathnawi", "match": r"rumi|r[uū]m[iī]|mathnawi|mathnaw[iī]", "subject": "the reed torn from the reed-bed crying to return home, the whirling of the Sufi dervish, lover and Beloved, the wine of divine union"},
    {"slug": "shantideva", "match": r"shantideva|[sś][aā]ntideva|bodhicary", "subject": "the bodhisattva's vow, the awakening mind (bodhicitta) as a rare jewel, the exchange of self and other, a boundless wheel of compassion"},
    {"slug": "siva_sutra", "match": r"siva.?s[uū]tra|[sś]iva.?s[uū]tra|shiva.?sutra", "subject": "consciousness itself is the Self (caitanyam atma), the three eyes of Shiva, the goddess of speech, tantric awakening of the knower"},
    {"slug": "svetasvatara_upanishad", "match": r"svetasvatara|[sś]vet[aā][sś]vatara", "subject": "the one God hidden in every being, Rudra the cosmic fire, the wheel of Brahman turned by Maya, the swan of the Self floating on the waters"},
    {"slug": "tantrasara", "match": r"tantras[aā]ra|abhinavagupta", "subject": "Abhinavagupta's Tantrasara, the heart of the Trika, the trident and three lotuses of the goddesses, the ascending fire of pure consciousness"},
    {"slug": "tao_te_ching", "match": r"tao|te.?ching|lao.?tzu", "subject": "the Tao that cannot be named, water yielding yet all-overcoming, the uncarved block, the valley spirit, a dragon dissolving into cloud and mist"},
    {"slug": "chuang_tzu", "match": r"chuang|zhuang", "subject": "the butterfly dream of Zhuangzi, the useless tree that lives long, the pipes of heaven, the great fish Kun becoming the vast bird Peng, free and easy wandering"},
    {"slug": "cloud_of_unknowing", "match": r"cloud of unknowing", "subject": "the cloud of unknowing above and the cloud of forgetting below, the sharp dart of longing love piercing the dark, the naked contemplative ascent to God"},
    {"slug": "tilopa_mahamudra", "match": r"tilopa|maha.?mudra", "subject": "the Ganges Mahamudra, the mind left in its own natural ease, the mahasiddha Tilopa with a fish, boundless sky-like awareness"},
    {"slug": "vijnana_bhairava", "match": r"vijnana|bhairava|vij[nñ][aā]na", "subject": "the 112 gateways of the Bhairava tantra, Shiva's third eye and the luminous void between two breaths, dharana centering-techniques, consciousness as vast space"},
    {"slug": "yoga_spandakarika", "match": r"spanda", "subject": "the Spanda — the divine pulse and tremor of consciousness that creates and dissolves the worlds, Shiva's subtle vibration rippling outward"},
    {"slug": "yoginihrdaya", "match": r"yogin[iī]h[rṛ]daya|yogini.?hrdaya|heart of the yogini", "subject": "the heart of the Yogini, the Sri Chakra of nine interlocking enclosures, the goddess Tripura Sundari, the ascent inward through the yantra"},
    {"slug": "johnson_yoruba_religion", "match": r"samuel johnson|yoruba faith|johnson.?yoruba", "subject": "Yoruba theology of Olorun the transcendent Lord of Heaven, a radiant sun-father high above the world, the orisas as luminous intermediary spirits descending in ordered ranks, Ifa palm-nut divination, a vertical heaven-to-earth sacred cosmology"},
    {"slug": "yoruba_proverbs", "match": r"yoruba|[oò]we", "subject": "Yoruba orisha cosmology, a radiant solar mandala crowned by Shango's double thunder-axe, cowrie-shell Ifa divination, west african sacred geometry"},
    {"slug": "zhongyong", "match": r"zhongyong", "subject": "the Doctrine of the Mean, equilibrium and harmony, the unmoving centre between heaven and earth, the sincere sage as the still axis of the turning world"},
    {"slug": "zitkala_sa_legends", "match": r"old indian legends|zitkala", "subject": "Dakota oral legends, Iktomi the trickster in fringed buckskin by the buffalo-skin lodge, spirits of the plains, the sacred fire-circle of storytelling"},
]

# Probe subjects to confirm the model + prompt shape.
TEST = [
    {"slug": "_numinos_pure", "subject": "a radiant central mandala, a serpent circling a golden sun, concentric rings of visionary symbols"},
    {"slug": "_kashmir_saiva", "subject": "Shiva as pure awareness, a great eye opening at the center of a mandala, trident and crescent moon, the void of consciousness"},
    {"slug": "_yoruba", "subject": "Yoruba orisha cosmology, a river mother and a thunder axe, cowrie-shell divination, west african sacred geometry"},
]


def load_token() -> str:
    token = os.environ.get("REPLICATE_API_TOKEN", "").strip()
    if token:
        return token
    if ENV_PATH.exists():
        for raw in ENV_PATH.read_text(encoding="utf-8").splitlines():
            if raw.startswith("REPLICATE_API_TOKEN="):
                return raw.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("REPLICATE_API_TOKEN not found")


def output_url(output) -> str:
    first = output[0] if isinstance(output, list) else output
    return str(first)


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=120) as r:
        dest.write_bytes(r.read())


def generate(slug: str, subject: str, dest: Path, aspect: str = "1:1", attempts: int = 6) -> None:
    import replicate
    prompt = f"NUMINOS. {subject}. {STYLE}"
    for attempt in range(1, attempts + 1):
        print(f"gen   {slug} …" + (f" (retry {attempt})" if attempt > 1 else ""))
        try:
            output = replicate.run(MODEL, input={
                "prompt": prompt,
                "output_format": "jpg",
                "model": "dev",
                "go_fast": False,
                "lora_scale": 1,
                "megapixels": "1",
                "num_outputs": 1,
                "aspect_ratio": aspect,
                "guidance_scale": 3,
                "output_quality": 92,
                "num_inference_steps": 30,
            })
            download(output_url(output), dest)
            print(f"  ok  {dest.relative_to(REPO)}")
            time.sleep(8)
            return
        except Exception as exc:  # noqa: BLE001
            print(f"  err {slug}: {str(exc)[:120]}")
            time.sleep(10)
    raise SystemExit(f"failed: {slug}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--only", nargs="*", default=[])
    ap.add_argument("--aspect", default="1:1")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    os.environ["REPLICATE_API_TOKEN"] = load_token()

    if args.test:
        for item in TEST:
            generate(item["slug"], item["subject"], TEST_DIR / f"{item['slug']}.jpg", args.aspect)
        print(f"\nTest images in {TEST_DIR.relative_to(REPO)}")
        return

    items = MANIFEST
    if args.only:
        want = set(args.only)
        items = [m for m in MANIFEST if m["slug"] in want]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    done = skipped = 0
    for m in items:
        dest = OUT_DIR / f"{m['slug']}.jpg"
        if dest.exists() and not args.force:
            print(f"skip  {m['slug']} (exists)")
            skipped += 1
            continue
        generate(m["slug"], m["subject"], dest, args.aspect)
        done += 1
    print(f"\ngenerated {done} | skipped {skipped} | out: {OUT_DIR.relative_to(REPO)}")


if __name__ == "__main__":
    main()
