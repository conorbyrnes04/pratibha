import type { VerseItem } from "@/lib/types";
import { isDraftPassage } from "@/lib/learn/passages";
import { maturityLabel } from "@/lib/verseLayers";

export function PassageMaturityBadge({ item }: { item: VerseItem | null }) {
  if (!item || !isDraftPassage(item)) return null;
  return (
    <p className="mt-2 inline-flex rounded-full border border-amber-200/25 bg-amber-100/5 px-3 py-1 font-sans text-[10px] uppercase tracking-[0.12em] text-amber-200/75">
      Corpus in progress · {maturityLabel(item.editorial_maturity)} — path teaching is complete; layers still deepening
    </p>
  );
}
