"use client";

import type { VerseItem } from "@/lib/types";
import { isDraftPassage } from "@/lib/learn/passages";
import { maturityLabel } from "@/lib/verseLayers";
import { Badge } from "@/components/ui/badge";
import { useT } from "@/components/LocaleProvider";

export function PassageMaturityBadge({ item }: { item: VerseItem | null }) {
  const t = useT();
  if (!item || !isDraftPassage(item)) return null;
  return (
    <Badge
      variant="outline"
      className="mt-2 h-auto rounded-full border-amber-200/25 bg-amber-100/5 px-3 py-1 font-sans text-[10px] uppercase tracking-[0.12em] text-amber-200/75"
    >
      {t("learn.draftBadge", { label: maturityLabel(item.editorial_maturity) })}
    </Badge>
  );
}
