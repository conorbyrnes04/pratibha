import * as React from "react";
import { Input as InputPrimitive } from "@base-ui/react/input";

import { cn } from "@/lib/utils";

/** Manuscript-tuned field — gold border, ink fill. */
function Input({ className, type, ...props }: React.ComponentProps<"input">) {
  return (
    <InputPrimitive
      type={type}
      data-slot="input"
      className={cn(
        "h-10 w-full min-w-0 rounded-xl border border-[rgb(240_201_121_/_0.16)] bg-[rgb(5_5_10_/_0.62)] px-3 py-2 font-sans text-sm text-foreground outline-none transition-[border-color,box-shadow] placeholder:text-[var(--muted-2)] focus-visible:border-[rgb(240_201_121_/_0.52)] focus-visible:shadow-[0_0_0_3px_rgb(216_168_74_/_0.12)] disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50",
        className,
      )}
      {...props}
    />
  );
}

export { Input };
