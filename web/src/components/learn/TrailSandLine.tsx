"use client";

import { useId } from "react";
import { sandPathD, type SandPoint } from "@/lib/learn/sandPath";

export type TrailSandMark = SandPoint & {
  key: string;
  top: number;
  bottom: number;
};

type TrailSandLineProps = {
  marks: TrailSandMark[];
  width: number;
  height: number;
  /** The node that just appeared — its incoming line draws itself. */
  drawingKey?: string | null;
};

export function TrailSandLine({ marks, width, height, drawingKey }: TrailSandLineProps) {
  const rawId = useId().replace(/:/g, "");
  const glowId = `sand-glow-${rawId}`;
  const grainId = `sand-grain-${rawId}`;

  if (width < 8 || height < 8 || marks.length < 2) return null;

  const segments = marks.slice(0, -1).map((from, i) => {
    const to = marks[i + 1];
    const dx = to.x - from.x;
    const dy = to.y - from.y;
    const span = Math.hypot(dx, dy) || 1;
    const fromR = Math.max(18, (from.bottom - from.top) * 0.38);
    const toR = Math.max(18, (to.bottom - to.top) * 0.38);
    const start = { x: from.x + (dx / span) * fromR, y: from.y + (dy / span) * fromR };
    const end = { x: to.x - (dx / span) * toR, y: to.y - (dy / span) * toR };
    const arriving = drawingKey === to.key;
    const live = i === marks.length - 2;
    return {
      key: `${from.key}→${to.key}`,
      d: sandPathD(start, end, `${from.key}|${to.key}`, { width, height }),
      arriving,
      live,
    };
  });

  return (
    <svg
      className="learn-trail__sand"
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      fill="none"
      aria-hidden
    >
      <defs>
        <filter id={glowId} x="-30%" y="-18%" width="160%" height="136%">
          <feGaussianBlur stdDeviation="3.2" result="blur" />
          <feMerge>
            <feMergeNode in="blur" />
          </feMerge>
        </filter>
        <filter id={grainId} x="-10%" y="-10%" width="120%" height="120%">
          <feTurbulence type="fractalNoise" baseFrequency="0.75" numOctaves="2" seed="4" result="n" />
          <feDisplacementMap in="SourceGraphic" in2="n" scale="0.85" />
        </filter>
      </defs>

      {segments.map((seg) => (
        <g
          key={seg.arriving ? `${seg.key}-arrive` : seg.key}
          className={
            seg.arriving
              ? "learn-trail__sand-seg learn-trail__sand-seg--draw"
              : seg.live
                ? "learn-trail__sand-seg learn-trail__sand-seg--live"
                : "learn-trail__sand-seg learn-trail__sand-seg--walked"
          }
          data-sand-arriving={seg.arriving ? "true" : undefined}
        >
          <path
            d={seg.d}
            className="learn-trail__sand-glow"
            pathLength={1}
            filter={`url(#${glowId})`}
          />
          <path
            d={seg.d}
            className="learn-trail__sand-groove"
            pathLength={1}
            filter={`url(#${grainId})`}
          />
          <path d={seg.d} className="learn-trail__sand-ridge" pathLength={1} />
          <path d={seg.d} className="learn-trail__sand-spark" pathLength={1} />
        </g>
      ))}
    </svg>
  );
}
