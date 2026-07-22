import Link from "next/link";
import { Glyph } from "@/components/Glyph";
import type { GlyphSlug } from "@/lib/glyphs";

export type ProductChip = {
  href: string;
  label: string;
  /** One short line describing what this surface does. */
  hint?: string;
  glyph?: GlyphSlug;
};

type ProductSnapshotProps = {
  items: ProductChip[];
  /** Highlight the chip whose href matches this path. */
  activeHref?: string;
  className?: string;
};

/**
 * ProductSnapshot — a compact horizontal row of the app's surfaces
 * ("products across the top"). Gives users a glanceable map of what
 * Pratibha offers without reading dense prose.
 */
export function ProductSnapshot({ items, activeHref, className }: ProductSnapshotProps) {
  return (
    <nav aria-label="Pratibha surfaces" className={`product-snapshot ${className ?? ""}`.trim()}>
      {items.map((item) => {
        const active = activeHref === item.href;
        return (
          <Link
            key={item.href}
            href={item.href}
            className="product-chip"
            style={active ? { borderColor: "rgb(240 201 121 / 0.55)" } : undefined}
          >
            <span className="flex items-center gap-2">
              {item.glyph ? <Glyph name={item.glyph} size="sm" className="opacity-85" /> : null}
              <span className="product-chip__label">{item.label}</span>
            </span>
            {item.hint ? <span className="product-chip__hint">{item.hint}</span> : null}
          </Link>
        );
      })}
    </nav>
  );
}
