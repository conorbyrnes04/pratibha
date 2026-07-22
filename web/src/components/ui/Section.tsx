import type { ReactNode } from "react";

type SectionProps = {
  /** Small uppercase kicker above the title. */
  eyebrow?: ReactNode;
  /** Section heading. Rendered as an h2 by default. */
  title?: ReactNode;
  /** Supporting lead paragraph under the title. */
  lead?: ReactNode;
  /** Optional right-aligned action (link/button) beside the header. */
  action?: ReactNode;
  /** Heading element to render for the title. */
  as?: "h1" | "h2" | "h3";
  className?: string;
  children?: ReactNode;
};

/**
 * Section — the canonical page block with breathing room.
 *
 * Wrap major page regions in <Section> and group them inside a
 * `.section-stack` container so vertical rhythm is consistent
 * everywhere instead of ad-hoc mt-8/mt-12/mt-14 per page.
 */
export function Section({
  eyebrow,
  title,
  lead,
  action,
  as: Heading = "h2",
  className,
  children,
}: SectionProps) {
  const hasHeader = eyebrow || title || lead || action;
  return (
    <section className={className}>
      {hasHeader ? (
        <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
          <div className="section-head">
            {eyebrow ? <p className="eyebrow">{eyebrow}</p> : null}
            {title ? (
              <Heading className="mt-3 text-balance text-3xl font-semibold leading-tight text-stone-100 sm:text-4xl">
                {title}
              </Heading>
            ) : null}
            {lead ? <p className="section-lead mt-4">{lead}</p> : null}
          </div>
          {action ? <div className="shrink-0">{action}</div> : null}
        </div>
      ) : null}
      {children}
    </section>
  );
}
