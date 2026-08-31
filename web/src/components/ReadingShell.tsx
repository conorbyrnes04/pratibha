"use client";

import type { ReactNode } from "react";
import { ArtBackdrop } from "@/components/ArtImage";
import { cn } from "@/lib/utils";

type ReadingShellProps = {
  children: ReactNode;
  /** Collection art as soft atmosphere behind the header — not a hero card. */
  artSrcs?: string[];
  /** Red Book mandala shown clearly as a living colophon below the passage. */
  mandalaSrc?: string;
  className?: string;
};

/**
 * Editorial reading column (Medium/Substack measure).
 * Atmosphere art is optional and masked; primary layers stay unboxed.
 * The collection's Red Book mandala closes the passage as a living, turning seal.
 * Continuous motion is CSS (robust in production), not JS.
 */
export function ReadingShell({ children, artSrcs, mandalaSrc, className }: ReadingShellProps) {
  const hasArt = Boolean(artSrcs && artSrcs.length > 0);

  return (
    <div className={cn("passage-reading", className)}>
      {hasArt ? (
        <div className="passage-reading__atmosphere" aria-hidden>
          <ArtBackdrop srcs={artSrcs} variant="subtle" opacity={0.11} priority />
        </div>
      ) : null}
      <div className="passage-reading__column">
        {children}
        {mandalaSrc ? (
          <figure className="passage-reading__mandala">
            <span className="passage-reading__mandala-halo" aria-hidden />
            <img className="passage-reading__mandala-img" src={mandalaSrc} alt="" aria-hidden />
            <figcaption className="passage-reading__mandala-seal">Liber Novus</figcaption>
          </figure>
        ) : null}
      </div>
    </div>
  );
}
