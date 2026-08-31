"use client";

import type { ReactNode } from "react";
import { motion, useReducedMotion } from "motion/react";
import { ArtBackdrop } from "@/components/ArtImage";
import { cn } from "@/lib/utils";

type ReadingShellProps = {
  children: ReactNode;
  /** Collection art as soft atmosphere behind the header — not a hero card. */
  artSrcs?: string[];
  /** Red Book mandala shown clearly as a colophon below the passage. */
  mandalaSrc?: string;
  className?: string;
};

/**
 * Editorial reading column (Medium/Substack measure).
 * Atmosphere art is optional and masked; primary layers stay unboxed.
 * The collection's Red Book mandala closes the passage as a living seal.
 */
export function ReadingShell({ children, artSrcs, mandalaSrc, className }: ReadingShellProps) {
  const hasArt = Boolean(artSrcs && artSrcs.length > 0);
  const reduce = useReducedMotion();

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
          <motion.figure
            className="passage-reading__mandala"
            initial={reduce ? false : { opacity: 0, scale: 0.85, rotate: -10 }}
            whileInView={{ opacity: 1, scale: 1, rotate: 0 }}
            viewport={{ once: true, margin: "-8%" }}
            transition={{ duration: 0.95, ease: [0.2, 0.7, 0.2, 1] }}
          >
            <motion.img
              src={mandalaSrc}
              alt=""
              aria-hidden
              animate={reduce ? undefined : { rotate: 360 }}
              transition={{ duration: 240, ease: "linear", repeat: Infinity }}
            />
            <figcaption className="passage-reading__mandala-seal">Liber Novus</figcaption>
          </motion.figure>
        ) : null}
      </div>
    </div>
  );
}
