"use client";

import type { ReactNode } from "react";
import { ArtBackdrop } from "@/components/ArtImage";
import { cn } from "@/lib/utils";

type ReadingShellProps = {
  children: ReactNode;
  /** Collection art as soft atmosphere behind the header — not a hero card. */
  artSrcs?: string[];
  className?: string;
};

/**
 * Editorial reading column (Medium/Substack measure).
 * Atmosphere art is optional and masked; primary layers stay unboxed.
 */
export function ReadingShell({ children, artSrcs, className }: ReadingShellProps) {
  const hasArt = Boolean(artSrcs && artSrcs.length > 0);

  return (
    <div className={cn("passage-reading", className)}>
      {hasArt ? (
        <div className="passage-reading__atmosphere" aria-hidden>
          <ArtBackdrop srcs={artSrcs} variant="subtle" opacity={0.11} priority />
        </div>
      ) : null}
      <div className="passage-reading__column">{children}</div>
    </div>
  );
}
