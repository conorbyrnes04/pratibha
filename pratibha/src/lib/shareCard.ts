import { verseSumiGlyph } from "./sumi";
import type { Passage } from "./corpus";

export const SHARE_MARK_GROUPS = [
  {
    id: "animals",
    label: "Animals",
    marks: [
      "bear",
      "bee",
      "butterfly",
      "crane",
      "crow",
      "deer",
      "dolphin",
      "dragon",
      "eagle",
      "elephant",
      "fish",
      "fox",
      "hawk",
      "horse",
      "lion",
      "owl",
      "ox",
      "raven",
      "serpent",
      "spider",
      "stag",
      "swan",
      "tiger",
      "turtle",
      "whale",
      "wolf",
    ],
  },
  {
    id: "plants",
    label: "Plants",
    marks: ["lotus", "mushroom", "oak", "rose", "tree", "vine"],
  },
  {
    id: "objects",
    label: "Objects",
    marks: ["celtic_key", "celtic_star", "chalice", "cross", "eye", "heart", "labyrinth", "mandala", "mirror", "triangle", "yantra"],
  },
  {
    id: "elements",
    label: "Elements",
    marks: ["air", "desert", "earth", "fire", "lightning", "mountain", "ocean", "rainbow", "storm", "tides", "volcano", "water"],
  },
  {
    id: "cosmos",
    label: "Cosmos",
    marks: ["circle", "comet", "constellation", "infinity", "moon", "spiral", "star", "sun", "void", "yin_yang"],
  },
  {
    id: "figures",
    label: "Figures",
    marks: ["fool", "hermit", "king", "maiden", "mother", "sage", "shaman", "warrior"],
  },
  {
    id: "deities",
    label: "Deities",
    marks: [
      "anubis",
      "apollo",
      "artemis",
      "athena",
      "brahma",
      "dionysus",
      "durga",
      "eros",
      "freyja",
      "ganesha",
      "hades",
      "hera",
      "horus",
      "isis",
      "kali",
      "lakshmi",
      "loki",
      "nuwa",
      "odin",
      "oshun",
      "osiris",
      "persephone",
      "quetzalcoatl",
      "saraswati",
      "shango",
      "shiva",
      "tezcatlipoca",
      "thanatos",
      "thor",
      "thoth",
      "thunderbird",
      "vishnu",
      "yemaya",
      "zeus",
    ],
  },
] as const;

export const SHARE_FORCE_MARKS = SHARE_MARK_GROUPS.flatMap((group) => group.marks);

export type ShareForceMark = (typeof SHARE_FORCE_MARKS)[number];

export function isShareForceMark(value: string): value is ShareForceMark {
  return (SHARE_FORCE_MARKS as readonly string[]).includes(value);
}

export function verseShareMark(passage: Passage): ShareForceMark {
  const mapped = verseSumiGlyph({
    collection: passage.collection,
    title: passage.title,
    translation: passage.translation,
    themes: passage.themes,
  });
  if (isShareForceMark(mapped)) return mapped;
  return "lotus";
}

export const SHARE_INKS = {
  ash: { label: "Ash", hex: "#8a8680" },
  bone: { label: "Bone", hex: "#e8e4dc" },
  gold: { label: "Gold", hex: "#f0c979" },
  copper: { label: "Copper", hex: "#c47a3a" },
  moonlight: { label: "Moonlight", hex: "#c5d4e0" },
} as const;

export type ShareInk = keyof typeof SHARE_INKS;
export type ShareTextMode = "original" | "translation" | "both";

const SITE = (process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3000").replace(/\/$/, "");

export function sharePageUrl(
  verseId: string,
  mark: ShareForceMark,
  ink: ShareInk,
  textMode: ShareTextMode,
  line?: number,
): string {
  const params = new URLSearchParams({ g: mark, ink, t: textMode });
  if (line) params.set("l", String(line));
  return `${SITE}/s/${encodeURIComponent(verseId)}?${params.toString()}`;
}

export const SHARE_SOCIAL = [
  { id: "instagram", label: "Instagram" },
  { id: "tiktok", label: "TikTok" },
  { id: "x", label: "X" },
  { id: "whatsapp", label: "WhatsApp" },
  { id: "signal", label: "Signal" },
] as const;

export type ShareSocialId = (typeof SHARE_SOCIAL)[number]["id"];

export function tweetIntentUrl(caption: string, url: string): string {
  return `https://twitter.com/intent/tweet?text=${encodeURIComponent(caption)}&url=${encodeURIComponent(url)}`;
}

export function whatsappIntentUrl(caption: string): string {
  return `https://wa.me/?text=${encodeURIComponent(caption)}`;
}

export function nextFolioLine(count: number, current?: number): number | undefined {
  if (count < 1) return undefined;
  if (!current) return 1;
  return current >= count ? undefined : current + 1;
}
