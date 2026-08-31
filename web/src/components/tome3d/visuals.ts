import type { LibraryTome } from "@/lib/libraryTomes";
import { DEFAULT_TOME_VISUAL, type TomePalette, type TomeVisual } from "./types";

const TRADITION_PALETTES: Record<string, TomePalette> = {
  Vedānta: {
    background: "#16141f",
    cloth: "#1a2438",
    accent: "#d8a84a",
    paper: "#e8e0d0",
  },
  Yoga: {
    background: "#1c1610",
    cloth: "#3d2a18",
    accent: "#e0b56a",
    paper: "#efe6d4",
  },
  "Kashmir Śaiva": {
    background: "#140c10",
    cloth: "#2a1018",
    accent: "#c9a227",
    paper: "#e6dcc8",
  },
  Buddhist: {
    background: "#1a100c",
    cloth: "#5c2418",
    accent: "#e8b060",
    paper: "#f0e6d2",
  },
  Daoist: {
    background: "#0c1210",
    cloth: "#121816",
    accent: "#6a9e86",
    paper: "#e4e8dc",
  },
  Confucian: {
    background: "#1a0e0c",
    cloth: "#5a1c18",
    accent: "#f0d9a8",
    paper: "#f2ebe0",
  },
  Greek: {
    background: "#121418",
    cloth: "#2a3038",
    accent: "#d8d2c4",
    paper: "#f0ece4",
  },
  Christian: {
    background: "#140c10",
    cloth: "#3a1420",
    accent: "#d8a84a",
    paper: "#ebe2d2",
  },
  Sufi: {
    background: "#0c1218",
    cloth: "#142028",
    accent: "#4ec4b0",
    paper: "#e4ebe6",
  },
  Yoruba: {
    background: "#1a120c",
    cloth: "#3a2410",
    accent: "#e0a84a",
    paper: "#f0e6d2",
  },
  Dakota: {
    background: "#12140c",
    cloth: "#243018",
    accent: "#c4b070",
    paper: "#ebe6d8",
  },
  Hebrew: {
    background: "#141210",
    cloth: "#2a2418",
    accent: "#d8c48a",
    paper: "#f0eadc",
  },
};

function thicknessForCount(count: number): number {
  // Map passage count into Stripe-like book depth range.
  const t = 1.6 + Math.min(count, 120) / 120 * 1.8;
  return Math.round(t * 100) / 100;
}

function foilForTradition(tradition: string): number {
  if (tradition === "Vedānta" || tradition === "Kashmir Śaiva") return 0.55;
  if (tradition === "Christian" || tradition === "Sufi") return 0.45;
  if (tradition === "Daoist") return 0.25;
  return 0.35;
}

export function tomeVisualFor(tome: LibraryTome): TomeVisual {
  const palette = TRADITION_PALETTES[tome.tradition] ?? DEFAULT_TOME_VISUAL.palette;
  return {
    palette,
    thickness: thicknessForCount(tome.count),
    foil: foilForTradition(tome.tradition),
  };
}
