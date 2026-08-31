import type { LibraryTome } from "@/lib/libraryTomes";
import type { SumiSlug } from "@/lib/sumiGlyphs";

/**
 * Visual contract for the Stripe Press–inspired 3D tome shelf.
 * Core mesh/materials and shelf/scene agents both depend on this file.
 */

export type TomePalette = {
  /** Scene / page wash behind the active book */
  background: string;
  /** Spine + cloth base */
  cloth: string;
  /** Title / foil accent (gold-ish) */
  accent: string;
  /** Page-edge paper */
  paper: string;
};

export type TomeVisual = {
  palette: TomePalette;
  /** Book block depth in scene units (Stripe uses ~1.4–3.4 cm-equivalent). */
  thickness: number;
  /** Optional foil intensity 0–1 */
  foil: number;
};

export type Tome3DItem = LibraryTome & {
  visual: TomeVisual;
};

export type TomeShelfProps = {
  tomes: LibraryTome[];
  onOpen: (collection: string) => void;
  className?: string;
};

/** Default visual when tradition-specific styling is unknown. */
export const DEFAULT_TOME_VISUAL: TomeVisual = {
  palette: {
    background: "#211815",
    cloth: "#1a2438",
    accent: "#d8a84a",
    paper: "#e8e0d0",
  },
  thickness: 2.2,
  foil: 0.35,
};

export type CoverDrawInput = {
  title: string;
  author: string;
  tradition: string;
  glyph: SumiSlug;
  palette: TomePalette;
};
