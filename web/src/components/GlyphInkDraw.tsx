"use client";

import { useEffect, useRef, useState, type CSSProperties } from "react";
import { InkGlyph } from "@/components/InkGlyph";
import { loadSumiTrace, type SumiTrace } from "@/lib/sumiTrace";

type GlyphInkDrawProps = {
  slug: string;
  ink: string;
  /** Hold the brush until the sand line arrives. */
  delayMs?: number;
  /** Crop the paper plate so the mark fills a trail well. */
  tight?: boolean;
  className?: string;
  onReady?: () => void;
};

/** Same draw-then-wash as the glyph-unlock overlay, for use in a well. */
export function GlyphInkDraw({
  slug,
  ink,
  delayMs = 0,
  tight = false,
  className = "",
  onReady,
}: GlyphInkDrawProps) {
  const [trace, setTrace] = useState<SumiTrace | null | undefined>(undefined);
  const onReadyRef = useRef(onReady);
  onReadyRef.current = onReady;

  useEffect(() => {
    let live = true;
    setTrace(undefined);
    void loadSumiTrace(slug, tight).then((next) => {
      if (live) setTrace(next);
    });
    return () => {
      live = false;
    };
  }, [slug, tight]);

  useEffect(() => {
    if (trace === undefined) return;
    onReadyRef.current?.();
  }, [trace]);

  if (trace === undefined) {
    return <InkGlyph glyph={slug} ink={ink} size="xl" className={className} mask />;
  }

  if (!trace) {
    return (
      <InkGlyph
        glyph={slug}
        ink={ink}
        size="xl"
        className={className}
        stroke
        strokeKey={`draw-${slug}`}
        strokeDelay={delayMs}
      />
    );
  }

  return (
    <svg
      className={`glyph-ink-draw ${className}`.trim()}
      viewBox={trace.viewBox}
      width="100%"
      height="100%"
      preserveAspectRatio="xMidYMid meet"
      role="img"
      aria-hidden
      data-glyph-ink-draw={slug}
      style={
        {
          ["--unlock-ink" as string]: ink,
          ["--glyph-draw-delay" as string]: `${delayMs}ms`,
        } as CSSProperties
      }
    >
      <g transform={trace.transform} fillRule="evenodd">
        {trace.paths.map((d, i) => (
          <g key={`${slug}-${i}`} style={{ ["--ink-i" as string]: i }}>
            <path className="glyph-unlock__wash" d={d} />
            <path
              className="glyph-unlock__draw"
              d={d}
              pathLength={1}
              strokeWidth={trace.strokeWidth || 80}
            />
          </g>
        ))}
      </g>
    </svg>
  );
}
