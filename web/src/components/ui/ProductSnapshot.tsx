import Link from "next/link";
import { InkGlyph } from "@/components/InkGlyph";
import type { SumiSlug } from "@/lib/sumiGlyphs";

export type ProductChip = {
  href: string;
  label: string;
  /** One short line for title/tooltip only — not rendered as body copy. */
  hint?: string;
  glyph: SumiSlug;
};

type ProductSnapshotProps = {
  items: ProductChip[];
  /** Highlight the chip whose href matches this path. */
  activeHref?: string;
  className?: string;
};

/**
 * ProductSnapshot — quiet Sumi ink strip of app surfaces (not a card grid).
 * One row on desktop; horizontal scroll on mobile so nothing orphans.
 */
export function ProductSnapshot({ items, activeHref, className }: ProductSnapshotProps) {
  return (
    <nav
      aria-label="Pratibha surfaces"
      className={`product-snapshot ${className ?? ""}`.trim()}
    >
      {items.map((item) => {
        const active = activeHref === item.href;
        return (
          <Link
            key={item.href}
            href={item.href}
            title={item.hint}
            className={`product-chip${active ? " product-chip--active" : ""}`}
          >
            <InkGlyph glyph={item.glyph} state={active ? "recognized" : "arising"} size="sm" />
            <span className="product-chip__label">{item.label}</span>
          </Link>
        );
      })}
    </nav>
  );
}
