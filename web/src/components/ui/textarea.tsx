import * as React from "react";

import { cn } from "@/lib/utils";

/** Manuscript-tuned textarea — matches Input. */
function Textarea({ className, ...props }: React.ComponentProps<"textarea">) {
  return (
    <textarea
      data-slot="textarea"
      className={cn(
        "flex field-sizing-content min-h-24 w-full rounded-2xl border border-[rgb(240_201_121_/_0.16)] bg-[rgb(5_5_10_/_0.62)] px-3 py-3 font-sans text-sm text-foreground outline-none transition-[border-color,box-shadow] placeholder:text-[var(--muted-2)] focus-visible:border-[rgb(240_201_121_/_0.52)] focus-visible:shadow-[0_0_0_3px_rgb(216_168_74_/_0.12)] disabled:cursor-not-allowed disabled:opacity-50",
        className,
      )}
      {...props}
    />
  );
}

export { Textarea };
