// Sumi ink marks for the Lynx client.
//
// The web recolors the potrace SVGs via CSS mask; Lynx has no mask pipeline, so
// FastAPI recolors server-side (GET /sumi/{slug}.svg?state=...) and we drop the
// result into a plain <image>. This module maps corpus texts -> a mark and
// builds the recolor URL.

const API_BASE = (process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000").replace(/\/$/, "");

export type InkState = "unmanifest" | "arising" | "recognized";

// The marks that exist as files (assets/sumi/svg). Kept in step with the web
// SUMI_SLUGS so unitSumiGlyph() only ever resolves to a real mark.
const SUMI_SLUGS = [
  "air","anubis","apollo","artemis","athena","bear","bee","brahma","butterfly","chalice","circle",
  "comet","constellation","crane","cross","crow","deer","desert","dionysus","dolphin","dragon","durga",
  "eagle","earth","elephant","eros","eye","fire","fish","fool","fox","freyja","ganesha","hades","hawk",
  "heart","hera","hermit","horse","horus","infinity","isis","kali","king","labyrinth","lakshmi",
  "lightning","lion","loki","lotus","maiden","mandala","mirror","moon","mother","mountain","mushroom",
  "nuwa","oak","ocean","odin","oshun","osiris","ox","phoenix","quetzalcoatl","raven","sage","saraswati",
  "serpent","shango","shiva","spiral","star","sun","swan","thoth","tides","tiger","tree","vishnu",
  "water","wolf","yantra","yemaya","void","play",
] as const;

const SUMI_RULES: Array<{ pattern: RegExp; glyph: string }> = [
  { pattern: /tao|te.?ching|zhuang|chuang|lao.?tzu/i, glyph: "dragon" },
  { pattern: /astavakra|ashtavakra|a[sṣ][tṭ][aā]vakra/i, glyph: "hermit" },
  { pattern: /bhagavad/i, glyph: "vishnu" },
  { pattern: /epictetus|marcus|meditation/i, glyph: "sage" },
  { pattern: /phaedo|plato/i, glyph: "athena" },
  { pattern: /plotinus|ennead/i, glyph: "infinity" },
  { pattern: /milarepa/i, glyph: "mountain" },
  { pattern: /tilopa|maha.?mudra/i, glyph: "water" },
  { pattern: /heart.?s[uū]tra|prajna|prajñā/i, glyph: "lotus" },
  { pattern: /nagarjuna|madhyamaka|mulamadhyamaka|mmk/i, glyph: "void" },
  { pattern: /shantideva|śāntideva|bodhicary/i, glyph: "heart" },
  { pattern: /chandogya/i, glyph: "sun" },
  { pattern: /isavasya|īśāvāsya|isha.?upani/i, glyph: "circle" },
  { pattern: /svetasvatara|śvetāśvatara|heraclitus|fragment/i, glyph: "fire" },
  { pattern: /mandukya|māṇḍūkya|gaudapada|dogen|dōgen|shobogenzo/i, glyph: "moon" },
  { pattern: /vijnana|bhairava|vijñāna/i, glyph: "eye" },
  { pattern: /pratyabhij|ibn|arabi|know yourself/i, glyph: "mirror" },
  { pattern: /spanda/i, glyph: "tides" },
  { pattern: /siva.?s[uū]tra|śiva.?s[uū]tra|shiva.?sutra/i, glyph: "shiva" },
  { pattern: /tantras[aā]ra|abhinavagupta|yogin[iī]h[rṛ]daya|upanishad|upaniṣad/i, glyph: "yantra" },
  { pattern: /patanjali|patañjali|yoga.?s[uū]tra|rumi|poet/i, glyph: "spiral" },
  { pattern: /confucius|analect|zhongyong/i, glyph: "tree" },
  { pattern: /eckhart|abegescheidenheit/i, glyph: "chalice" },
  { pattern: /eastman|ohiyesa|zitkala|dakota|sioux|soul of the indian|indian legends/i, glyph: "eagle" },
  { pattern: /pulaar.?texts|gaden|le.?poular/i, glyph: "horse" },
  { pattern: /pulaar.?tradition|ful[bɓ]e|peul/i, glyph: "ox" },
  { pattern: /senegalese.?animism|serer|pangool|roog/i, glyph: "oak" },
  { pattern: /yoruba|òwe|\bowe\b|orisha|orisa|ifa/i, glyph: "shango" },
];

function isSlug(s: string): boolean {
  return (SUMI_SLUGS as readonly string[]).includes(s);
}

/** Map a corpus text / verse id / tradition to its preferred mark. */
export function sumiGlyph(name?: string): string {
  const raw = (name || "").trim();
  if (!raw) return "lotus";
  for (const rule of SUMI_RULES) {
    if (rule.pattern.test(raw)) return isSlug(rule.glyph) ? rule.glyph : "circle";
  }
  return "circle";
}

const SEMANTIC_RULES: Array<{ pattern: RegExp; glyph: string; weight: number }> = [
  { pattern: /\bbutterfly|蝴蝶/i, glyph: "butterfly", weight: 3 },
  { pattern: /\bdolphin/i, glyph: "dolphin", weight: 3 },
  { pattern: /\bdragon|naga raja/i, glyph: "dragon", weight: 3 },
  { pattern: /\beagle|garuda|garu[dḍ]a/i, glyph: "eagle", weight: 3 },
  { pattern: /\belephant|gaja/i, glyph: "elephant", weight: 3 },
  { pattern: /\bhorse|a[sś]va/i, glyph: "horse", weight: 3 },
  { pattern: /\blion|si[mṃ]ha/i, glyph: "lion", weight: 3 },
  { pattern: /\bserpent|n[aā]ga|kundalin[iī]|snake/i, glyph: "serpent", weight: 3 },
  { pattern: /\bdeer\b|m[rṛ]ga/i, glyph: "deer", weight: 3 },
  { pattern: /\bcrane\b/i, glyph: "crane", weight: 3 },
  { pattern: /\bfish\b|matsya/i, glyph: "fish", weight: 3 },
  { pattern: /\bswan\b|ha[mṃ]sa/i, glyph: "swan", weight: 3 },
  { pattern: /\btiger\b/i, glyph: "tiger", weight: 3 },
  { pattern: /ga[nṇ]e[sś][ah]|ganapati/i, glyph: "ganesha", weight: 3 },
  { pattern: /\bvi[sṣ][nṇ]u|k[rṛ][sṣ][nṇ]a/i, glyph: "vishnu", weight: 3 },
  { pattern: /\b[sś]iva\b|bhairava|rudra|trident/i, glyph: "shiva", weight: 3 },
  { pattern: /\b[sś][uū]nyat[aā]|emptiness|empty of|\bvoid\b/i, glyph: "void", weight: 3 },
  { pattern: /\bagni\b|flame|blaze/i, glyph: "fire", weight: 2 },
  { pattern: /\bocean|sea\b|tide/i, glyph: "ocean", weight: 2 },
  { pattern: /\bmountain|himalay|kail[aā]sa|meru\b/i, glyph: "mountain", weight: 2 },
  { pattern: /\bmoon\b|candra|lunar/i, glyph: "moon", weight: 2 },
  { pattern: /\bsun\b|s[uū]rya|solar/i, glyph: "sun", weight: 2 },
  { pattern: /\blotus|padma/i, glyph: "lotus", weight: 2 },
  { pattern: /\bmirror|pratibimba/i, glyph: "mirror", weight: 2 },
  { pattern: /\beye\b|witness|seer\b/i, glyph: "eye", weight: 2 },
  { pattern: /\bheart\b|h[rṛ]daya/i, glyph: "heart", weight: 1 },
  { pattern: /\bwater|river|ga[nṅ]g[aā]/i, glyph: "water", weight: 1 },
  { pattern: /\bfire\b/i, glyph: "fire", weight: 1 },
];

export function verseSumiGlyph(input: {
  collection?: string;
  title?: string;
  translation?: string;
  themes?: string[];
}): string {
  const tight = [input.title, ...(input.themes || [])].filter(Boolean).join(" \n ");
  const body = (input.translation || "").slice(0, 800);
  let best: { glyph: string; score: number } | undefined;
  for (const rule of SEMANTIC_RULES) {
    let score = 0;
    if (tight && rule.pattern.test(tight)) score += rule.weight * 3;
    else if (body && rule.pattern.test(body)) score += rule.weight;
    if (!score) continue;
    if (!best || score > best.score) best = { glyph: rule.glyph, score };
  }
  if (best && best.score >= 3 && isSlug(best.glyph)) return best.glyph;
  return sumiGlyph(input.collection);
}

/** Stable per-unit mark — same id always draws the same mark. */
export function unitSumiGlyph(seed?: string): string {
  const key = (seed || "").trim() || "pratibha";
  let h = 2166136261;
  for (let i = 0; i < key.length; i += 1) {
    h ^= key.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return SUMI_SLUGS[Math.abs(h) % SUMI_SLUGS.length]!;
}

/** URL for a mark recolored to an ink state (served by FastAPI). */
export function sumiUrl(glyph: string, state: InkState = "arising"): string {
  return `${API_BASE}/sumi/${glyph}.svg?state=${state}`;
}
