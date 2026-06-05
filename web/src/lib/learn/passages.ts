import type { LearningStepSpec } from "@/lib/learningPaths";
import type { VerseItem } from "@/lib/types";

export function resolveById(items: VerseItem[], id?: string): VerseItem | null {
  if (!id) return null;
  return items.find((v) => v._id === id || v.sutra_id === id) || null;
}

export function matchStepItem(step: LearningStepSpec, items: VerseItem[]): VerseItem | null {
  const exact = resolveById(items, step.passageId);
  if (exact) return exact;
  const filtered = items.filter((v) => {
    const okTheme = !step.theme || (v.themes || []).includes(step.theme);
    const matureEnough = v.editorial_maturity !== "needs_rewrite" && v.editorial_maturity !== "structural_draft";
    return okTheme && matureEnough;
  });
  return filtered[0] || null;
}

export function isDraftPassage(item: VerseItem | null): boolean {
  return item?.editorial_maturity === "structural_draft" || item?.editorial_maturity === "needs_rewrite";
}
