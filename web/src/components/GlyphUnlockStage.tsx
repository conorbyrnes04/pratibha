"use client";

import { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import { GlyphInkDraw } from "@/components/GlyphInkDraw";

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
  const [ready, setReady] = useState(false);
  const [drawn, setDrawn] = useState(false);

  useEffect(() => {
    setReady(true);
  }, []);

  useEffect(() => {
    setDrawn(false);
  }, [slug]);

  useEffect(() => {
    if (!drawn) return;
    const id = window.setTimeout(onDone, PLAY_MS);
    return () => window.clearTimeout(id);
  }, [slug, drawn, onDone]);

  if (!ready) return null;

  const mark = (
    <div className="glyph-unlock" style={{ ["--unlock-ink" as string]: ink }} aria-hidden>
      <GlyphInkDraw slug={slug} ink={ink} className="glyph-unlock__svg" onReady={() => setDrawn(true)} />
    </div>
  );

  return createPortal(mark, document.body);
}
