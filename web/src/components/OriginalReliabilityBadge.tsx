import type { VerseItem } from "@/lib/types";
import { Badge } from "@/components/ui/badge";

/** True when there is no verified source-language original — the unit is carried
 * by Pratibha's own English rendering (original withdrawn, unverified, or an
 * interpretive reflection rather than a sourced quotation). */
export function hasUnverifiedOriginal(item: VerseItem | null | undefined): boolean {
  const rel = item?.provenance?.original_reliability || "";
  return /UNVERIFIED|ORIGINAL_REMOVED|INTERPRETIVE/i.test(rel);
}

/** Public-facing label for units without a verified source original. Framed
 * positively and honestly as Pratibha's own translation rather than a warning. */
export function OriginalReliabilityBadge({ item }: { item: VerseItem | null }) {
  if (!item || !hasUnverifiedOriginal(item)) return null;
  return (
    <Badge
      variant="outline"
      className="mt-2 h-auto rounded-full border-[rgb(240_201_121_/_0.28)] bg-[rgb(240_201_121_/_0.06)] px-3 py-1 font-sans text-[10px] uppercase tracking-[0.12em] text-amber-100/80"
    >
      Pratibha translation
    </Badge>
  );
}
