import { Button as ButtonPrimitive } from "@base-ui/react/button";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

/** Manuscript-tuned variants — visual parity with former .btn-primary / .btn-secondary. */
const buttonVariants = cva(
  "group/button inline-flex shrink-0 items-center justify-center border border-transparent bg-clip-padding font-sans font-bold tracking-[0.03em] whitespace-nowrap transition-all outline-none select-none focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--accent-bright)] active:not-aria-[haspopup]:translate-y-px disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4",
  {
    variants: {
      variant: {
        default:
          "rounded-full text-[#121018] bg-gradient-to-br from-[var(--accent-bright)] to-[var(--accent)] shadow-[0_12px_35px_rgb(216_168_74_/_0.18)] hover:-translate-y-px hover:brightness-105",
        secondary:
          "rounded-full border-[rgb(240_201_121_/_0.34)] bg-white/[0.035] text-[var(--accent-bright)] hover:-translate-y-px hover:border-[rgb(240_201_121_/_0.5)] hover:bg-white/[0.06]",
        outline:
          "rounded-full border-border bg-background/40 text-foreground hover:bg-muted hover:text-foreground",
        ghost:
          "rounded-lg text-[var(--muted)] hover:bg-white/[0.05] hover:text-[var(--accent-bright)]",
        destructive:
          "rounded-full bg-[var(--vermillion)]/20 text-[var(--accent-bright)] hover:bg-[var(--vermillion)]/30",
        link: "rounded-sm text-[var(--accent-bright)] underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 gap-1.5 px-4 text-sm",
        sm: "h-8 gap-1 px-3 text-sm",
        lg: "h-11 gap-1.5 px-6 text-sm",
        icon: "size-9 rounded-full",
        "icon-sm": "size-8 rounded-full",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  },
);

function Button({
  className,
  variant = "default",
  size = "default",
  ...props
}: ButtonPrimitive.Props & VariantProps<typeof buttonVariants>) {
  return (
    <ButtonPrimitive
      data-slot="button"
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  );
}

export { Button, buttonVariants };
