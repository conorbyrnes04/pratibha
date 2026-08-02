import Link from "next/link";
import type { VariantProps } from "class-variance-authority";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

type Props = React.ComponentProps<typeof Link> &
  VariantProps<typeof buttonVariants> & {
    className?: string;
  };

/**
 * Next.js Link styled as a manuscript Button.
 * Prefer this over Base UI `render={<Link />}` (that pattern crashed the app).
 */
export function KitLink({
  className,
  variant = "default",
  size = "default",
  ...props
}: Props) {
  return (
    <Link className={cn(buttonVariants({ variant, size }), className)} {...props} />
  );
}
