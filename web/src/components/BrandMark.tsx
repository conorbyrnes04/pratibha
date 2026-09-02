type BrandMarkProps = {
  className?: string;
  size?: "sm" | "md" | "lg";
  /** True when a parent link already names the site (header lockup). */
  decorative?: boolean;
};

const SIZE_CLASS: Record<NonNullable<BrandMarkProps["size"]>, string> = {
  sm: "brand-mark--sm",
  md: "brand-mark--md",
  lg: "brand-mark--lg",
};

/** Pratibha yantra seal — primary site brand mark. */
export function BrandMark({ className = "", size = "md", decorative = false }: BrandMarkProps) {
  return (
    <span
      className={`brand-mark ${SIZE_CLASS[size]} ${className}`.trim()}
      role={decorative ? undefined : "img"}
      aria-label={decorative ? undefined : "Pratibhā"}
      aria-hidden={decorative || undefined}
    >
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src="/brand/yantra-mark.png" alt="" draggable={false} />
    </span>
  );
}
