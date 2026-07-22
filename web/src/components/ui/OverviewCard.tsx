import type { ReactNode } from "react";
import Link from "next/link";
import { Glyph } from "@/components/Glyph";
import type { GlyphSlug } from "@/lib/glyphs";

type OverviewCardProps = {
  eyebrow?: ReactNode;
  title: ReactNode;
  body?: ReactNode;
  /** Small footer line, e.g. a count or status ("12 texts"). */
  stat?: ReactNode;
  /** Decorative glyph shown top-right. */
  glyph?: GlyphSlug;
  /** If provided, the whole card becomes a link. */
  href?: string;
  /** Click handler when used as a button instead of a link. */
  onClick?: () => void;
  className?: string;
  children?: ReactNode;
};

function CardInner({ eyebrow, title, body, stat, glyph, children }: OverviewCardProps) {
  return (
    <>
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          {eyebrow ? <p className="overview-card__eyebrow">{eyebrow}</p> : null}
          <p className="overview-card__title mt-1">{title}</p>
        </div>
        {glyph ? (
          <Glyph
            name={glyph}
            size="md"
            className="shrink-0 opacity-80 transition group-hover:opacity-100 group-hover:scale-105"
          />
        ) : null}
      </div>
      {body ? <p className="overview-card__body">{body}</p> : null}
      {children}
      {stat ? <p className="overview-card__stat">{stat}</p> : null}
    </>
  );
}

/**
 * OverviewCard — glanceable summary tile used across surfaces for
 * "overview cards" (products, tomes, sources, threads, etc.).
 * Renders as a Link, a button, or a static div depending on props.
 */
export function OverviewCard(props: OverviewCardProps) {
  const { href, onClick, className } = props;
  const cls = `overview-card group ${className ?? ""}`.trim();

  if (href) {
    return (
      <Link href={href} className={`${cls} block`}>
        <CardInner {...props} />
      </Link>
    );
  }
  if (onClick) {
    return (
      <button type="button" onClick={onClick} className={`${cls} text-left`}>
        <CardInner {...props} />
      </button>
    );
  }
  return (
    <div className={cls}>
      <CardInner {...props} />
    </div>
  );
}
