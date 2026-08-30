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
  "air","anubis","apollo","artemis","athena","bear","brahma","butterfly","chalice","circle",
  "comet","constellation","cross","desert","dionysus","dolphin","dragon","durga","eagle","earth",
  "eros","eye","fire","fool","fox","freyja","ganesha","hades","heart","hera","hermit","horse",
  "horus","infinity","isis","kali","king","labyrinth","lakshmi","lightning","lion","loki","lotus",
  "maiden","mandala","mirror","moon","mother","mountain","mushroom","nuwa","oak","ocean","odin",
  "oshun","osiris","phoenix","quetzalcoatl","raven","sage","saraswati","serpent","shango","shiva",
  "spiral","star","sun","swan","thoth","tides","tree","vishnu","water","wolf","yantra","yemaya","void",
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
