export const SHARE_DEITY_MARKS = [
  "zeus",
  "hera",
  "athena",
  "apollo",
  "artemis",
  "hades",
  "persephone",
  "dionysus",
  "eros",
  "brahma",
  "kali",
  "durga",
  "lakshmi",
  "saraswati",
  "ganesha",
  "isis",
  "osiris",
  "horus",
  "anubis",
  "thoth",
  "odin",
  "thor",
  "freyja",
  "loki",
  "oshun",
  "shango",
  "yemaya",
  "quetzalcoatl",
  "tezcatlipoca",
  "nuwa",
  "thanatos",
  "thunderbird",
] as const;

export const SHARE_FORCE_MARKS = [
  "lotus",
  "moon",
  "fire",
  "serpent",
  "dragon",
  "eye",
  "circle",
  "void",
  "sun",
  "vishnu",
  "ocean",
  "star",
  "lightning",
  "tides",
  "spiral",
  "water",
  "infinity",
  "mandala",
  "yantra",
  "mirror",
  "mountain",
  "heart",
  "chalice",
  "shiva",
  "owl",
  "rose",
  "tree",
  "sage",
  ...SHARE_DEITY_MARKS,
] as const;

export type ShareForceMark = (typeof SHARE_FORCE_MARKS)[number];

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

export function nextFolioLine(count: number, current?: number): number | undefined {
  if (count < 1) return undefined;
  if (!current) return 1;
  return current >= count ? undefined : current + 1;
}
