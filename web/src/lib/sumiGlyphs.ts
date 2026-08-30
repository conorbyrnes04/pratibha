/**
 * Sumi-e ink marks shipped under /public/sumi.
 *
 * These are flat black potrace fills — designed to be recolored via CSS
 * mask (see components/InkGlyph.tsx), never rendered as raw black-on-white
 * <img> like the Mythra Glyphnet set in lib/glyphs.ts. In the Sumi/Spanda
 * system the dark UI is the void (anuttara); the ink glyph is ābhāsa, the
 * "shining forth," so it is always painted in a state color — ash, bone, or
 * gold — never left as source-black.
 */

export const SUMI_SLUGS = [
  "air",
  "anubis",
  "apollo",
  "artemis",
  "athena",
  "bear",
  "brahma",
  "butterfly",
  "celtic_key",
  "celtic_star",
  "chalice",
  "circle",
  "comet",
  "constellation",
  "cross",
  "desert",
  "dionysus",
  "dolphin",
  "dragon",
  "durga",
  "eagle",
  "earth",
  "eros",
  "eye",
  "fire",
  "fool",
  "fox",
  "freyja",
  "ganesha",
  "hades",
  "heart",
  "hera",
  "hermit",
  "horse",
  "horus",
  "infinity",
  "isis",
  "kali",
  "king",
  "labyrinth",
  "lakshmi",
  "lightning",
  "lion",
  "loki",
  "lotus",
  "maiden",
  "mandala",
  "mirror",
  "moon",
  "mother",
  "mountain",
  "mushroom",
  "nuwa",
  "oak",
  "ocean",
  "odin",
  "oshun",
  "osiris",
  "owl",
  "persephone",
  "quetzalcoatl",
  "rainbow",
  "raven",
  "rose",
  "sage",
  "saraswati",
  "serpent",
  "shaman",
  "shango",
  "shiva",
  "spider",
  "spiral",
  "stag",
  "star",
  "storm",
  "sun",
  "tezcatlipoca",
  "thanatos",
  "thor",
  "thoth",
  "thunderbird",
  "tides",
  "tree",
  "triangle",
  "turtle",
  "vine",
  "vishnu",
  "void",
  "volcano",
  "warrior",
  "water",
  "whale",
  "wolf",
  "yantra",
  "yemaya",
  "yin_yang",
  "zeus",
] as const;

export type SumiSlug = (typeof SUMI_SLUGS)[number];

export function sumiSrc(slug: SumiSlug | string): string {
  return `/sumi/${slug}.svg`;
}

function normalizeKey(name: string): string {
  return name.normalize("NFD").replace(/\p{M}/gu, "").toLowerCase();
}

/**
 * Map a corpus text / tradition name to a sumi mark. Mirrors the shape of
 * GLYPH_RULES in lib/glyphs.ts, but every target is constrained to a slug
 * that actually exists in SUMI_SLUGS (the sumi set is much smaller than the
 * Glyphnet set, so several picks stand in for an unavailable "ideal" glyph —
 * each of those is called out with a comment).
 */
const SUMI_RULES: Array<{ pattern: RegExp; glyph: SumiSlug }> = [
  { pattern: /tao|te.?ching|tao_te_ching|zhuang|chuang|lao.?tzu|chuang_tzu/i, glyph: "dragon" },
  { pattern: /astavakra|ashtavakra|a[sṣ][tṭ][aā]vakra/i, glyph: "hermit" },
  { pattern: /bhagavad/i, glyph: "vishnu" },
  { pattern: /epictetus/i, glyph: "sage" },
  { pattern: /phaedo|plato/i, glyph: "athena" },
  { pattern: /plotinus|ennead/i, glyph: "infinity" },
  { pattern: /milarepa|jetsun.?kahbum|tibet.?s.?great.?yogi/i, glyph: "mountain" },
  { pattern: /tilopa|maha.?mudra|ganges.?mahamudra/i, glyph: "water" },
  { pattern: /heart.?s[uū]tra|prajnaparamita|prajñāpāramitā/i, glyph: "lotus" },
  { pattern: /nagarjuna|madhyamaka|mulamadhyamakakarika|mmk/i, glyph: "void" },
  { pattern: /shantideva|śāntideva|bodhicary/i, glyph: "heart" },
  { pattern: /chandogya|khandogya|khândogya/i, glyph: "sun" },
  { pattern: /isavasya|īśāvāsya|isha.?upani/i, glyph: "circle" },
  { pattern: /svetasvatara|śvetāśvatara/i, glyph: "fire" },
  { pattern: /mandukya|māṇḍūkya|gaudapada|gauḍapāda/i, glyph: "moon" },
  { pattern: /upanishad|upaniṣad/i, glyph: "yantra" },
  { pattern: /vijnana|bhairava|vijñāna.?bhairava/i, glyph: "eye" },
  { pattern: /pratyabhij/i, glyph: "mirror" },
  { pattern: /spanda/i, glyph: "tides" },
  { pattern: /tantras[aā]ra|abhinavagupta/i, glyph: "yantra" },
  { pattern: /yogin[iī]h[rṛ]daya|yogini.?hrdaya|heart of the yogini/i, glyph: "yantra" },
  { pattern: /siva.?s[uū]tra|śiva.?s[uū]tra|shiva.?sutra/i, glyph: "shiva" },
  { pattern: /vijnana|bhairava|shiva|siva|tantra|spanda|yogin[iī]|yogini_hrdaya|pratyabhij/i, glyph: "shiva" },
  { pattern: /heraclitus|fragment/i, glyph: "fire" },
  { pattern: /patanjali|patañjali|yoga.?s[uū]tras?|raja.?yoga/i, glyph: "spiral" },
  { pattern: /ibn|arabi|know yourself/i, glyph: "mirror" },
  { pattern: /confucius|analect|zhongyong/i, glyph: "tree" },
  { pattern: /marcus|meditation/i, glyph: "sage" },
  { pattern: /rumi|poet/i, glyph: "spiral" },
  { pattern: /dogen|dōgen|shobogenzo|shōbōgenzō/i, glyph: "moon" },
  { pattern: /eckhart|meister_eckhart|abegescheidenheit|abgeschiedenheit/i, glyph: "chalice" },
];

function asSumiGlyph(slug: string): SumiSlug {
  return (SUMI_SLUGS as readonly string[]).includes(slug) ? (slug as SumiSlug) : "circle";
}

/** Map a corpus text / tradition name to a preferred sumi mark. */
export function sumiGlyph(name?: string): SumiSlug {
  const raw = (name || "").trim();
  if (!raw || raw.toLowerCase() === "all") return "lotus";
  const key = normalizeKey(raw);
  for (const rule of SUMI_RULES) {
    if (rule.pattern.test(raw) || rule.pattern.test(key)) return asSumiGlyph(rule.glyph);
  }
  return "circle";
}

/** Stable "random" sumi mark for a passage — same id always gets the same mark. */
export function unitSumiGlyph(seed?: string): SumiSlug {
  const key = (seed || "").trim() || "pratibha";
  let h = 2166136261;
  for (let i = 0; i < key.length; i += 1) {
    h ^= key.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  const idx = Math.abs(h) % SUMI_SLUGS.length;
  return SUMI_SLUGS[idx]!;
}
