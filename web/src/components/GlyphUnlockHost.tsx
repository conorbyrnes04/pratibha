"use client";

import { useCallback, useEffect, useState } from "react";
import { GlyphUnlockStage } from "@/components/GlyphUnlockStage";
import { GLYPH_UNLOCK_EVENT, releaseUnlockListener, retainUnlockListener } from "@/lib/glyphUnlock";
import { SHARE_INKS, isShareForceMark, type ShareForceMark } from "@/lib/shareCard";

export function GlyphUnlockHost() {
  const [queue, setQueue] = useState<ShareForceMark[]>([]);

  useEffect(() => {
    const queued = retainUnlockListener();
    if (queued.length) setQueue((current) => [...current, ...queued]);
    function onUnlock(event: Event) {
      const marks = (event as CustomEvent<{ marks?: unknown }>).detail?.marks;
      if (!Array.isArray(marks)) return;
      const next = marks.filter((mark): mark is ShareForceMark => typeof mark === "string" && isShareForceMark(mark));
      if (next.length) setQueue((current) => [...current, ...next]);
    }
    window.addEventListener(GLYPH_UNLOCK_EVENT, onUnlock);
    return () => {
      window.removeEventListener(GLYPH_UNLOCK_EVENT, onUnlock);
      releaseUnlockListener();
    };
  }, []);

  const dismiss = useCallback(() => {
    setQueue((current) => current.slice(1));
  }, []);

  if (!queue[0]) return null;
  return <GlyphUnlockStage slug={queue[0]} ink={SHARE_INKS.gold.hex} onDone={dismiss} />;
}
