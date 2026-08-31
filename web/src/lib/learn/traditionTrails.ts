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
    lede: "Recognition: you are the Consciousness you have been seeking.",
    glyph: "shiva",
    trackIds: ["heart-of-recognition", "three-doors-of-shiva", "the-112-doorways", "descent-of-the-cakra"],
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
    trackIds: ["recognizing-awareness"],
  },
  {
    id: "tao",
    title: "Tao",
    shortTitle: "Tao",
    lede: "The nameless source; the ten thousand things arise and return.",
    glyph: "dragon",
    trackIds: ["letting-go-death-emptiness"],
  },
  {
    id: "greek",
    title: "Greek & Neoplatonist",
    shortTitle: "Greek",
    lede: "The One overflows; the soul returns by becoming sunlike.",
    glyph: "infinity",
    trackIds: ["the-one-and-the-many"],
  },
  {
    id: "yoga",
    title: "Yoga (Patañjali)",
    shortTitle: "Yoga",
    lede: "Stillness of the mind's turnings; the seer rests in its own nature.",
    glyph: "spiral",
    trackIds: ["seer-in-its-nature"],
  },
  {
    id: "buddhism",
    title: "Buddhism",
    shortTitle: "Buddhism",
    lede: "Emptiness, compassion, the groundless ground.",
    glyph: "lotus",
    trackIds: ["emptiness-and-compassion"],
  },
  {
    id: "yoruba",
    title: "Yoruba",
    shortTitle: "Yoruba",
    lede: "Òwe — the horse of conversation. Wisdom that travels by speech.",
    glyph: "oshun",
    trackIds: ["the-horse-of-conversation"],
  },
];

export const TRADITIONS_COMING: TraditionTrail[] = [
  {
    id: "sufi",
    title: "Sufi",
    shortTitle: "Sufi",
    lede: "The Beloved hides in plain sight; love is the way.",
    glyph: "spiral",
    comingSoon: true,
    trackIds: [],
  },
  {
    id: "christian-mysticism",
    title: "Christian Mysticism",
    shortTitle: "Christian",
    lede: "The divine darkness; unknowing as the highest knowing.",
    glyph: "chalice",
    comingSoon: true,
    trackIds: [],
  },
];

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
