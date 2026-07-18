import { glyphSrc, type GlyphSlug } from "@/lib/glyphs";

type GlyphProps = {
  name: GlyphSlug;
  className?: string;
  /** Decorative by default; set label for informative icons. */
  label?: string;
  size?: "xs" | "sm" | "md" | "lg" | "xl" | "hero";
};

const SIZE_CLASS: Record<NonNullable<GlyphProps["size"]>, string> = {
  xs: "glyph--xs",
  sm: "glyph--sm",
  md: "glyph--md",
  lg: "glyph--lg",
  xl: "glyph--xl",
  hero: "glyph--hero",
};

/** Mythra Glyphnet mark — gold SVG asset, sized for UI chrome. */
export function Glyph({ name, className = "", label, size = "md" }: GlyphProps) {
  return (
    <span
      className={`glyph ${SIZE_CLASS[size]} ${className}`.trim()}
      role={label ? "img" : "presentation"}
      aria-label={label}
      aria-hidden={label ? undefined : true}
    >
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src={glyphSrc(name)} alt="" draggable={false} />
    </span>
  );
}

/** Thin divider with a centered glyph — replaces bare hairline ornaments. */
export function GlyphOrnament({ name = "lotus", className = "" }: { name?: GlyphSlug; className?: string }) {
  return (
    <div className={`glyph-ornament ${className}`.trim()} aria-hidden>
      <span className="glyph-ornament__line" />
      <Glyph name={name} size="sm" className="glyph-ornament__mark" />
      <span className="glyph-ornament__line" />
    </div>
  );
}
