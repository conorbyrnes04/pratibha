"use client";

import { useEffect, useState } from "react";
import { GLYPH_UNLOCK_EVENT, glyphMalaStats, unlockedMarks } from "@/lib/glyphUnlock";
import type { ShareForceMark } from "@/lib/shareCard";
import { useT } from "@/components/LocaleProvider";

export function GlyphMala({
  unlocked,
  compact = false,
}: {
  unlocked?: Set<ShareForceMark>;
  compact?: boolean;
}) {
  const [marks, setMarks] = useState<Set<ShareForceMark> | null>(unlocked ?? null);

  useEffect(() => {
    if (unlocked) {
      setMarks(unlocked);
      return;
    }
    function refresh() {
      setMarks(unlockedMarks({}));
    }
    refresh();
    window.addEventListener(GLYPH_UNLOCK_EVENT, refresh);
    return () => window.removeEventListener(GLYPH_UNLOCK_EVENT, refresh);
  }, [unlocked]);

  const t = useT();
  const stats = glyphMalaStats(marks ?? new Set());
  const pct = stats.total ? (stats.opened / stats.total) * 100 : 0;

  return (
    <div
      className={`glyph-mala${compact ? " glyph-mala--compact" : ""}${stats.complete ? " glyph-mala--complete" : ""}`}
      role="progressbar"
      aria-label={t("glyph.mala")}
      aria-valuemin={0}
      aria-valuemax={stats.total}
      aria-valuenow={stats.opened}
      aria-valuetext={
        stats.complete
          ? t("glyph.complete")
          : t("glyph.ofOpen", { opened: stats.opened, total: stats.total })
      }
    >
      <div className="glyph-mala__rail" aria-hidden>
        <span className="glyph-mala__fill" style={{ width: `${pct}%` }} />
      </div>
      {compact ? null : (
        <p className="glyph-mala__count">
          {stats.complete
            ? t("glyph.completeCount")
            : t("glyph.ofOpenShort", { opened: stats.opened, total: stats.total })}
        </p>
      )}
    </div>
  );
}
