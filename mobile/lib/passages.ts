import type { LearningStepSpec } from "@shared/learningPaths";
import type { VerseItem } from "@shared/types";
import { isReaderFacingUnit } from "@shared/corpusFilters";
import { layerText, passagePreview } from "@/lib/verseLayers";

export function resolveById(items: VerseItem[], id?: string): VerseItem | null {
  if (!id) return null;
  return items.find((v) => v._id === id || v.sutra_id === id) || null;
}

export function pickRandomPassage(items: VerseItem[], collection: string): VerseItem | null {
  const pool = items.filter(
    (x) =>
      isReaderFacingUnit(x) &&
      (collection === "all" || (x.collection || "Unknown").trim() === collection),
  );
  if (pool.length === 0) return null;
  return pool[Math.floor(Math.random() * pool.length)];
}

export function matchStepItem(step: LearningStepSpec, items: VerseItem[]): VerseItem | null {
  const exact = resolveById(items, step.passageId);
  if (exact) return exact;
  return items.filter((v) => {
    const okTheme = !step.theme || (v.themes || []).includes(step.theme);
    const matureEnough =
      v.editorial_maturity !== "needs_rewrite" && v.editorial_maturity !== "structural_draft";
    return okTheme && matureEnough;
  })[0] || null;
}

export { layerText, passagePreview };
