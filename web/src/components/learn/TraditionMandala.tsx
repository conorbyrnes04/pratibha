"use client";

import { useEffect, useState } from "react";
import { InkGlyph, SpandaMedallion, type InkState } from "@/components/InkGlyph";
import { YantraBreath } from "@/components/learn/YantraBreath";
import { buildMandalaRings, type TrailNode } from "@/lib/learn/trail";
import type { ProgressMap } from "@/lib/learn/progress";
import type { TraditionTrail } from "@/lib/learn/traditionTrails";
import { trailSumiGlyph } from "@/lib/sumiGlyphs";

type TraditionMandalaProps = {
  trail: TraditionTrail;
  nodes: TrailNode[];
  progress: ProgressMap;
  currentIndex: number;
  tomorrowKey?: string | null;
  drawingKey?: string | null;
  finishingKey?: string | null;
  onOpenGate: (trackId: string, stepId: string) => void;
};

function markState(
  node: TrailNode,
  index: number,
  progress: ProgressMap,
  currentIndex: number,
  tomorrowKey?: string | null,
  drawingKey?: string | null,
  finishingKey?: string | null,
): InkState {
  const done = Boolean(progress[node.key]);
  const arriving = drawingKey === node.key;
  const finishing = finishingKey === node.key;
  const isTomorrow = Boolean(tomorrowKey && node.key === tomorrowKey && !done && !arriving);
  const isCurrent = index === currentIndex && !done && !isTomorrow && !arriving;
  if (done && !finishing) return "recognized";
  if (isCurrent || arriving || finishing || isTomorrow) return "arising";
  return "unmanifest";
}

export function TraditionMandala({
  trail,
  nodes,
  progress,
  currentIndex,
  tomorrowKey,
  drawingKey,
  finishingKey,
  onOpenGate,
}: TraditionMandalaProps) {
  const [live, setLive] = useState(false);
  useEffect(() => {
    setLive(true);
  }, []);
  const shownProgress = live ? progress : {};
  const shownIndex = live ? currentIndex : 0;
  const shownTomorrow = live ? tomorrowKey : null;
  const rings = buildMandalaRings(trail.id);
  const indexByKey = new Map(nodes.map((node, i) => [node.key, i]));
  const walked = nodes.filter((node) => shownProgress[node.key]).length;
  const binduState: InkState =
    walked === 0 ? "unmanifest" : walked >= nodes.length ? "recognized" : "arising";

  return (
    <div className="tradition-mandala" aria-label={trail.title}>
      <div className="tradition-mandala__field" aria-hidden>
        <YantraBreath className="tradition-mandala__yantra" />
        <span className="tradition-mandala__wash">
          <InkGlyph glyph={trail.glyph} state="unmanifest" size="hero" mask />
        </span>
      </div>

      <div className="tradition-mandala__stage">
        <svg className="tradition-mandala__rings" viewBox="0 0 100 100" aria-hidden preserveAspectRatio="xMidYMid meet">
          {rings.map((ring) => (
            <circle
              key={ring.trackId}
              cx="50"
              cy="50"
              r={ring.radius}
              fill="none"
              stroke="rgb(240 201 121 / 0.16)"
              strokeWidth="0.28"
            />
          ))}
        </svg>

        {rings.map((ring) =>
          ring.marks.map(({ node, x, y }) => {
            const index = indexByKey.get(node.key) ?? -1;
            const state = markState(node, index, shownProgress, shownIndex, shownTomorrow, drawingKey, finishingKey);
            const openable = state !== "unmanifest" || index <= shownIndex;
            const glyph = trailSumiGlyph(node.stepId);
            const label = node.title;
            const left = `${Math.round(x * 100) / 100}%`;
            const top = `${Math.round(y * 100) / 100}%`;
            return (
              <button
                key={node.key}
                type="button"
                className={`tradition-mandala__mark tradition-mandala__mark--${state}`}
                style={{ left, top }}
                title={label}
                disabled={!openable}
                aria-label={label}
                onClick={() => {
                  if (!openable) return;
                  onOpenGate(node.trackId, node.stepId);
                }}
              >
                <InkGlyph glyph={glyph} state={state} size={state === "arising" ? "sm" : "xs"} mask />
              </button>
            );
          }),
        )}

        <div className="tradition-mandala__bindu">
          <SpandaMedallion glyph={trail.glyph} state={binduState} size="xl" mask />
        </div>
      </div>
    </div>
  );
}
