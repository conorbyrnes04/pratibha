import type { VerseItem } from "@/lib/types";
import { Badge } from "@/components/ui/badge";

/** True when the source-language layer was withdrawn or never verified against PD. */
export function hasUnverifiedOriginal(item: VerseItem | null | undefined): boolean {
  const rel = item?.provenance?.original_reliability || "";
  return /UNVERIFIED|ORIGINAL_REMOVED/i.test(rel);
}

export function OriginalReliabilityBadge({ item }: { item: VerseItem | null }) {
  if (!item || !hasUnverifiedOriginal(item)) return null;
  const removed = /ORIGINAL_REMOVED/i.test(item.provenance?.original_reliability || "");
  return (
    <Badge
      variant="outline"
      className="mt-2 h-auto rounded-full border-rose-300/30 bg-rose-300/5 px-3 py-1 font-sans text-[10px] uppercase tracking-[0.12em] text-rose-100/80"
    >
      {removed
        ? "Original withdrawn · English is editorial — not a verified quotation"
        : "Original unverified · treat source language as paraphrase pending edition check"}
    </Badge>
  );
}
