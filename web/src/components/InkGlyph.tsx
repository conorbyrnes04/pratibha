import type { CSSProperties } from "react";
import { sumiSrc } from "@/lib/sumiGlyphs";

export type InkState = "unmanifest" | "arising" | "recognized";
export type InkSize = "xs" | "sm" | "md" | "lg" | "xl" | "hero";

type InkGlyphProps = {
  glyph: string;
  /** Degree of manifestation: ash (un-arisen) -> bone (present) -> gold (recognized). */
  state?: InkState;
  size?: InkSize;
  className?: string;
  /** Decorative by default; set label for informative icons. */
  label?: string;
};

const SIZE_CLASS: Record<InkSize, string> = {
  xs: "ink-glyph--xs",
  sm: "ink-glyph--sm",
  md: "ink-glyph--md",
  lg: "ink-glyph--lg",
  xl: "ink-glyph--xl",
  hero: "ink-glyph--hero",
};

const STATE_CLASS: Record<InkState, string> = {
  unmanifest: "ink--unmanifest",
  arising: "ink--arising",
  recognized: "ink--recognized",
};

/**
 * Sumi ink mark — recolored via CSS mask (never a raw <img>), so it always
 * reads as ābhāsa shining forth from the void ground rather than a
 * black-on-white sticker. Color is entirely a function of `state`.
 */
export function InkGlyph({ glyph, state = "arising", size = "md", className = "", label }: InkGlyphProps) {
  return (
    <span
      className={`ink-glyph ${SIZE_CLASS[size]} ${STATE_CLASS[state]} ${className}`.trim()}
      style={{
        WebkitMaskImage: `url(${sumiSrc(glyph)})`,
        maskImage: `url(${sumiSrc(glyph)})`,
      }}
      role={label ? "img" : undefined}
      aria-label={label}
      aria-hidden={label ? undefined : true}
    />
  );
}

type SpandaMedallionProps = {
  glyph: string;
  state?: InkState;
  size?: InkSize;
  /** Optional hue passthrough (e.g. per-thread tinting); sets --thread-hue. */
  hue?: number;
  className?: string;
};

/**
 * Round medallion: a rough, slightly gapped ensō brush ring around a
 * centered InkGlyph. The ring closes and glows gold only once the node has
 * "recognized itself" (pratyabhijñā) — until then it's an ash or bone arc.
 */
export function SpandaMedallion({ glyph, state = "unmanifest", size = "md", hue, className = "" }: SpandaMedallionProps) {
  const breathing = state === "arising" ? "spanda-breath" : "";
  const blooming = state === "recognized" ? "ink-bloom" : "";
  return (
    <span
      className={`spanda-medallion ${STATE_CLASS[state]} ${breathing} ${blooming} ${className}`.trim()}
      style={hue !== undefined ? ({ "--thread-hue": hue } as CSSProperties) : undefined}
    >
      <svg className="spanda-medallion__enso" viewBox="0 0 100 100" aria-hidden focusable="false">
        <circle
          className="spanda-medallion__ring"
          cx="50"
          cy="50"
          r="44"
          fill="none"
          strokeWidth="4"
          strokeLinecap="round"
          /* A closed ring for "recognized"; a gapped, slightly rough arc otherwise —
             the ensō hasn't fully drawn itself shut yet. */
          strokeDasharray={state === "recognized" ? "none" : "252 24"}
          strokeDashoffset={state === "recognized" ? 0 : 18}
          transform="rotate(-96 50 50)"
        />
      </svg>
      <InkGlyph glyph={glyph} state={state} size={size} className="spanda-medallion__glyph" />
    </span>
  );
}
