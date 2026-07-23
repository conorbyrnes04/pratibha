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
  "bear",
  "butterfly",
  "celtic_key",
  "celtic_star",
  "circle",
  "comet",
  "constellation",
  "cross",
  "desert",
  "dolphin",
  "eagle",
  "earth",
  "eye",
  "fire",
  "fool",
  "fox",
  "hermit",
  "horse",
  "infinity",
  "king",
  "labyrinth",
  "lightning",
  "lion",
  "lotus",
  "maiden",
  "mandala",
  "moon",
  "mother",
  "mushroom",
  "oak",
  "ocean",
  "owl",
  "rainbow",
  "raven",
  "rose",
  "sage",
  "serpent",
  "shaman",
  "spider",
  "spiral",
  "stag",
  "star",
  "storm",
  "sun",
  "tree",
  "triangle",
  "turtle",
  "vine",
  "volcano",
  "warrior",
  "water",
  "whale",
  "wolf",
  "yin_yang",
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
  // dragon isn't in the sumi set; serpent carries the same watercourse-way charge.
  { pattern: /tao|te.?ching|tao_te_ching|zhuang|chuang|lao.?tzu|chuang_tzu/i, glyph: "serpent" },
  // Astavakra before the generic "bhagavad" rule so it doesn't inherit the Gītā's mark.
  { pattern: /astavakra|ashtavakra|a[sṣ][tṭ][aā]vakra/i, glyph: "hermit" },
  // vishnu isn't in the sumi set; sun stands in for Krishna as the radiance of dharma.
  { pattern: /bhagavad/i, glyph: "sun" },
  { pattern: /epictetus/i, glyph: "sage" },
  // athena isn't in the sumi set; owl is her emblematic bird — same wisdom register.
  { pattern: /phaedo|plato/i, glyph: "owl" },
  { pattern: /plotinus|ennead/i, glyph: "infinity" },
  // mountain isn't in the sumi set; moon stands in per spec.
  { pattern: /milarepa|jetsun.?kahbum|tibet.?s.?great.?yogi/i, glyph: "moon" },
  { pattern: /tilopa|maha.?mudra|ganges.?mahamudra/i, glyph: "water" },
  { pattern: /heart.?s[uū]tra|prajnaparamita|prajñāpāramitā/i, glyph: "lotus" },
  // void isn't in the sumi set; circle (ensō) is the classic figure for emptiness.
  { pattern: /nagarjuna|madhyamaka|mulamadhyamakakarika|mmk/i, glyph: "circle" },
  // heart isn't in the sumi set; rose stands in for the Bodhicaryāvatāra's compassion.
  { pattern: /shantideva|śāntideva|bodhicary/i, glyph: "rose" },
  { pattern: /chandogya|khandogya|khândogya/i, glyph: "sun" },
  // circle-wholeness isn't in the sumi set; circle (ensō) reads the same way.
  { pattern: /isavasya|īśāvāsya|isha.?upani/i, glyph: "circle" },
  { pattern: /svetasvatara|śvetāśvatara/i, glyph: "fire" },
  { pattern: /mandukya|māṇḍūkya|gaudapada|gauḍapāda/i, glyph: "moon" },
  // yantra isn't in the sumi set; mandala is the nearest sacred-diagram mark.
  { pattern: /upanishad|upaniṣad/i, glyph: "mandala" },
  { pattern: /vijnana|bhairava|vijñāna.?bhairava/i, glyph: "eye" },
  // mirror isn't in the sumi set; star stands in for pratyabhijñā's self-luminous recognition.
  { pattern: /pratyabhij/i, glyph: "star" },
  // tides isn't in the sumi set; lightning carries spanda's pulse/vibration charge.
  { pattern: /spanda/i, glyph: "lightning" },
  { pattern: /tantras[aā]ra|abhinavagupta/i, glyph: "mandala" },
  // yantra isn't in the sumi set; mandala stands in again.
  { pattern: /yogin[iī]h[rṛ]daya|yogini.?hrdaya|heart of the yogini/i, glyph: "mandala" },
  // shiva isn't in the sumi set; eye matches the broad tantra/shiva rule below.
  { pattern: /siva.?s[uū]tra|śiva.?s[uū]tra|shiva.?sutra/i, glyph: "eye" },
  { pattern: /vijnana|bhairava|shiva|siva|tantra|spanda|yogin[iī]|yogini_hrdaya|pratyabhij/i, glyph: "eye" },
  { pattern: /heraclitus|fragment/i, glyph: "fire" },
  { pattern: /patanjali|patañjali|yoga.?s[uū]tras?|raja.?yoga/i, glyph: "spiral" },
  // mirror isn't in the sumi set; moon carries the reflective charge Ibn Arabi's imagery wants.
  { pattern: /ibn|arabi|know yourself/i, glyph: "moon" },
  { pattern: /confucius|analect|zhongyong/i, glyph: "tree" },
  { pattern: /marcus|meditation/i, glyph: "sage" },
  { pattern: /rumi|poet/i, glyph: "spiral" },
  { pattern: /dogen|dōgen|shobogenzo|shōbōgenzō/i, glyph: "moon" },
  // chalice isn't in the sumi set; cross stands in for Eckhart's Christian mysticism.
  { pattern: /eckhart|meister_eckhart|abegescheidenheit|abgeschiedenheit/i, glyph: "cross" },
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
