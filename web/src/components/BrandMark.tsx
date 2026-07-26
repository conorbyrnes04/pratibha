type BrandMarkProps = {
  className?: string;
  size?: "sm" | "md" | "lg";
};

const SIZE_CLASS: Record<NonNullable<BrandMarkProps["size"]>, string> = {
  sm: "brand-mark--sm",
  md: "brand-mark--md",
  lg: "brand-mark--lg",
};

/** Pratibha yantra seal — primary site brand mark. */
export function BrandMark({ className = "", size = "md" }: BrandMarkProps) {
  return (
    <span
      className={`brand-mark ${SIZE_CLASS[size]} ${className}`.trim()}
      role="img"
      aria-label="Pratibha"
    >
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src="/brand/yantra-mark.png" alt="" draggable={false} />
    </span>
  );
}
