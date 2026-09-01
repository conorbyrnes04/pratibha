import { RECOMMENDED_SPINE } from "@/lib/learningPaths";
import type { SumiSlug } from "@/lib/sumiGlyphs";

export const ESSENTIAL_TRAIL_ID = "essential";

export type TraditionTrail = {
  id: string;
  title: string;
  shortTitle: string;
  lede: string;
  glyph: SumiSlug;
  essential?: boolean;
  comingSoon?: boolean;
  trackIds: string[];
};

/** Sequential paths, each a philosophical language. */
export const TRADITION_TRAILS: TraditionTrail[] = [
  {
    id: ESSENTIAL_TRAIL_ID,
    title: "The Path",
    shortTitle: "The Path",
    lede: "A single spine through the gates, one tradition after another.",
    glyph: "mandala",
    essential: true,
    trackIds: [...RECOMMENDED_SPINE],
  },
  {
    id: "kashmir-shaivism",
    title: "Kashmir Śaivism",
    shortTitle: "Śaivism",
    lede: "Recognition: you are the Consciousness you have been seeking. Then the pulse as method, Lalla's mouth in the house, the doorways and the cakra, then Abhinava's straight speech — not a second recognition.",
    glyph: "shiva",
    trackIds: [
      "recognizing-awareness",
      "heart-of-recognition",
      "three-doors-of-shiva",
      "the-sacred-tremor",
      "lallas-house",
      "the-112-doorways",
      "descent-of-the-cakra",
      "straight-speech",
    ],
  },
  {
    id: "bhagavad-gita",
    title: "Bhagavad Gītā",
    shortTitle: "Gītā",
    lede: "Act without seizing; serve without owning the fruit.",
    glyph: "vishnu",
    trackIds: ["action-without-contraction"],
  },
  {
    id: "vedanta",
    title: "Vedānta & Upaniṣads",
    shortTitle: "Vedānta",
    lede: "The witness behind waking, dream, and sleep — you are That.",
    glyph: "yantra",
    trackIds: ["you-are-that"],
  },
  {
    id: "tao",
    title: "Tao",
    shortTitle: "Tao",
    lede: "The nameless source; the ten thousand things arise and return.",
    glyph: "dragon",
    trackIds: ["nameless-source"],
  },
  {
    id: "greek",
    title: "Greek & Neoplatonist",
    shortTitle: "Greek",
    lede: "The One overflows; the soul returns by becoming sunlike.",
    glyph: "infinity",
    trackIds: ["become-sunlike"],
  },
  {
    id: "stoic",
    title: "Stoic",
    shortTitle: "Stoic",
    lede: "Some things are up to you. Train the ruling faculty on those.",
    glyph: "sage",
    trackIds: ["what-is-up-to-you"],
  },
  {
    id: "christian-mysticism",
    title: "Christian Mysticism",
    shortTitle: "Christian",
    lede: "Divine darkness, then the living saying, then address: the kingdom is not a spectacle; the mouth that remains speaks to the Face.",
    glyph: "chalice",
    trackIds: ["divine-darkness", "the-living-saying", "before-the-face"],
  },
  {
    id: "yoga",
    title: "Yoga",
    shortTitle: "Yoga",
    lede: "Stillness of the mind's turnings; then the body's fire as a staircase, not a catalogue.",
    glyph: "spiral",
    trackIds: ["seer-in-its-nature", "the-body-of-hatha"],
  },
  {
    id: "buddhism",
    title: "Buddhism",
    shortTitle: "Buddhism",
    lede: "Emptiness, compassion, then the cut that leaves no mark to stand on.",
    glyph: "lotus",
    trackIds: ["emptiness-and-compassion", "cutting-the-diamond"],
  },
  {
    id: "yoruba",
    title: "Yoruba",
    shortTitle: "Yoruba",
    lede: "Òwe — the horse of conversation. Wisdom that travels by speech.",
    glyph: "oshun",
    trackIds: ["the-horse-of-conversation"],
  },
  {
    id: "sufi",
    title: "Sufi",
    shortTitle: "Sufi",
    lede: "The Beloved hides in plain sight; love is the way — identity, unveiling, the valleys, then the reed.",
    glyph: "crane",
    trackIds: [
      "the-beloved-in-plain-sight",
      "know-yourself",
      "unveiling-the-veiled",
      "the-seven-valleys",
      "the-reed-complains",
    ],
  },
  {
    id: "confucian",
    title: "Confucian",
    shortTitle: "Confucian",
    lede: "Virtue is not remote. Cultivate what is near; the Mean is equilibrium, not mediocrity.",
    glyph: "oak",
    trackIds: ["humaneness-at-hand"],
  },
];

export const TRADITIONS_COMING: TraditionTrail[] = [];

export function findTraditionTrail(id?: string | null): TraditionTrail {
  return TRADITION_TRAILS.find((trail) => trail.id === id) ?? TRADITION_TRAILS[0]!;
}

export function isEssentialTrail(id?: string | null): boolean {
  return id === ESSENTIAL_TRAIL_ID;
}

export function isWalkableTrail(id?: string | null): boolean {
  return Boolean(id && TRADITION_TRAILS.some((trail) => trail.id === id));
}

/** Dedicated tradition first; otherwise The Path if the track lives on the spine. */
export function pathIdForTrack(trackId: string): string {
  const dedicated = TRADITION_TRAILS.find((trail) => !trail.essential && trail.trackIds.includes(trackId));
  if (dedicated) return dedicated.id;
  const essential = TRADITION_TRAILS.find((trail) => trail.essential && trail.trackIds.includes(trackId));
  if (essential) return essential.id;
  return ESSENTIAL_TRAIL_ID;
}
