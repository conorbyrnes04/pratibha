"use client";

import { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import { loadSumiTrace, type SumiTrace } from "@/lib/sumiTrace";
import { InkGlyph } from "@/components/InkGlyph";

const PLAY_MS = 2600;

export function GlyphUnlockStage({
  slug,
  ink,
  onDone,
}: {
  slug: string;
  ink: string;
  onDone: () => void;
}) {
  const [trace, setTrace] = useState<SumiTrace | null | undefined>(undefined);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    setReady(true);
  }, []);

  useEffect(() => {
    let live = true;
    setTrace(undefined);
    void loadSumiTrace(slug).then((next) => {
      if (live) setTrace(next);
    });
    return () => {
      live = false;
    };
  }, [slug]);

  useEffect(() => {
    if (trace === undefined) return;
    const id = window.setTimeout(onDone, PLAY_MS);
    return () => window.clearTimeout(id);
  }, [slug, trace, onDone]);

  if (!ready || trace === undefined) return null;

  const mark = (
    <div className="glyph-unlock" style={{ ["--unlock-ink" as string]: ink }} aria-hidden>
      {trace ? (
        <svg className="glyph-unlock__svg" viewBox={trace.viewBox} role="img">
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
      ) : (
        <InkGlyph glyph={slug} ink={ink} size="hero" stroke strokeKey={`unlock-${slug}`} />
      )}
    </div>
  );

  return createPortal(mark, document.body);
}
