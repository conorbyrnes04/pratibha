import type { LearningStepSpec } from "@/lib/learningPaths";
import type { VerseItem } from "@/lib/types";

export function resolveById(items: VerseItem[], id?: string): VerseItem | null {
  if (!id) return null;
  return items.find((v) => v._id === id || v.sutra_id === id) || null;
}

/**
 * Resolve the step's pinned passage only. Never invent a substitute from theme
 * overlap — a missing pin must surface as missing, not as the wrong text.
 */
export function matchStepItem(step: LearningStepSpec, items: VerseItem[]): VerseItem | null {
  return resolveById(items, step.passageId);
}

export function isDraftPassage(item: VerseItem | null): boolean {
  // The rawest tiers, where path teaching outruns the passage's own layers.
  const m = item?.editorial_maturity;
  return m === "seed" || m === "draft" || m === "structural_draft" || m === "needs_rewrite";
}
