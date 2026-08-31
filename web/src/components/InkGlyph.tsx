"use client";

import { useEffect, useState, type CSSProperties } from "react";
import { sumiSrc } from "@/lib/sumiGlyphs";
import { loadSumiInk, type SumiTrace } from "@/lib/sumiTrace";

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
  /** Override the state fill — used by share cards. */
  ink?: string;
  /** Paint the mark as a brush-stroke reveal. Replay when `strokeKey` changes. */
  stroke?: boolean;
  strokeKey?: string | number;
  /** Stagger when several marks open at once. */
  strokeDelay?: number;
  /** Fill the well; crop extra rather than letterboxing a wide mark. */
  cover?: boolean;
  /** Use the CSS mask, not the recropped path-trace (safer in a circular well). */
  mask?: boolean;
};

function viewBoxRatio(viewBox: string): number {
  const parts = viewBox.split(/[\s,]+/).map(Number);
  const width = parts[2] || 1;
  const height = parts[3] || 1;
  return width / height;
}

function isExtremeViewBox(viewBox: string): boolean {
  const ratio = viewBoxRatio(viewBox);
  return ratio > 1.55 || ratio < 0.64;
}

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

function MaskedInk({
  glyph,
  inkClass,
  className,
  ink,
  label,
}: {
  glyph: string;
  inkClass: string;
  className: string;
  ink?: string;
  label?: string;
}) {
  return (
    <span
      className={`${inkClass} ${className}`.trim()}
      style={{
        WebkitMaskImage: `url(${sumiSrc(glyph)})`,
        maskImage: `url(${sumiSrc(glyph)})`,
        ...(ink ? { backgroundColor: ink } : {}),
      }}
      role={label ? "img" : undefined}
      aria-label={label}
      aria-hidden={label ? undefined : true}
    />
  );
}

/**
 * Sumi ink on the void. Prefers the real potrace paths (currentColor fill)
 * so there is no raster mask plate. Falls back to a CSS mask while loading,
 * or when a brush-wipe is requested.
 */
export function InkGlyph({
  glyph,
  state = "arising",
  size = "md",
  className = "",
  label,
  ink,
  stroke = false,
  strokeKey,
  strokeDelay = 0,
  cover = false,
  mask = false,
}: InkGlyphProps) {
  const [trace, setTrace] = useState<SumiTrace | null | undefined>(undefined);

  useEffect(() => {
    if (stroke || mask) return;
    let live = true;
    setTrace(undefined);
    void loadSumiInk(glyph).then((next) => {
      if (live) setTrace(next);
    });
    return () => {
      live = false;
    };
  }, [glyph, stroke, mask]);

  const inkClass = `ink-glyph ${SIZE_CLASS[size]} ${STATE_CLASS[state]}`.trim();

  if (mask) {
    return <MaskedInk glyph={glyph} inkClass={inkClass} className={className} ink={ink} label={label} />;
  }

  if (stroke) {
    const mark = (
      <MaskedInk glyph={glyph} inkClass={`${inkClass} ink-stroke__ink`} className="" ink={ink} label={label} />
    );
    return (
      <span
        key={strokeKey ?? glyph}
        className={`ink-stroke ink-stroke--play ${className}`.trim()}
        style={strokeDelay ? ({ ["--ink-stroke-delay" as string]: `${strokeDelay}ms` } as CSSProperties) : undefined}
      >
        {mark}
      </span>
    );
  }

  if (trace && !isExtremeViewBox(trace.viewBox)) {
    return (
      <svg
        className={`${inkClass} ink-glyph--trace ${className}`.trim()}
        viewBox={trace.viewBox}
        preserveAspectRatio={cover ? "xMidYMid slice" : "xMidYMid meet"}
        style={ink ? ({ color: ink } as CSSProperties) : undefined}
        role={label ? "img" : undefined}
        aria-label={label}
        aria-hidden={label ? undefined : true}
      >
        <g transform={trace.transform} fill="currentColor" fillRule="evenodd">
          {trace.paths.map((d, i) => (
            <path key={`${glyph}-${i}`} d={d} />
          ))}
        </g>
      </svg>
    );
  }

  return <MaskedInk glyph={glyph} inkClass={inkClass} className={className} ink={ink} label={label} />;
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
