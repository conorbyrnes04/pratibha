import type { VerseItem } from "@/lib/types";
import { passageSortKey } from "@/lib/passageTitles";

/** Passages we never surface as "related" — too raw to send a reader to. */
function isReadable(v: VerseItem): boolean {
  // "seed" is source-only with no authored elaboration; everything from "draft"
  // up is readable. (Old "structural_draft"/"needs_rewrite" now normalize to these.)
  return v.editorial_maturity !== "seed" && v.editorial_maturity !== "structural_draft";
}

function maturityBonus(v: VerseItem): number {
  if (v.editorial_maturity === "polished" || v.editorial_maturity === "publishable") return 3;
  if (v.editorial_maturity === "rich") return 2;
  if (v.editorial_maturity === "draft" || v.editorial_maturity === "strong_draft") return 1;
  return 0;
}

type Scored = {
  item: VerseItem;
  score: number;
  shared: number;
};

/**
 * Rank passages by conceptual relatedness to `item`.
 *
 * The old logic sorted same-collection first, then by passage number, so large
 * collections (e.g. the Yoga Sūtras) flooded the list sequentially (1.1, 1.2,
 * 1.3…). This ranks by how many *themes* actually overlap, then enforces
 * cross-tradition diversity with a per-collection cap so the list reflects
 * Pratibha's point: the same idea echoing across traditions.
 */
export function relatedPassages(
  item: VerseItem,
  all: VerseItem[],
  limit = 6,
  perCollectionCap = 2,
): VerseItem[] {
  const mineThemes = new Set(item.themes || []);

  const scored: Scored[] = all
    .filter((v) => v._id !== item._id && isReadable(v))
    .map((v) => {
      const shared = (v.themes || []).filter((t) => mineThemes.has(t)).length;
      const sameCollection = (v.collection || "") === (item.collection || "");
      // Theme overlap dominates; maturity is a light tiebreak; same-collection
      // gets only a whisper so a sibling never outranks a stronger theme match.
      const score = shared * 10 + maturityBonus(v) + (sameCollection ? 1 : 0);
      return { item: v, score, shared };
    })
    .filter((s) => s.shared > 0)
    .sort(
      (a, b) =>
        b.score - a.score ||
        (b.item.editorial_score || 0) - (a.item.editorial_score || 0) ||
        passageSortKey(a.item) - passageSortKey(b.item),
    );

  const picked: VerseItem[] = [];
  const perCollection = new Map<string, number>();

  // Pass 1: diverse — cap how many can come from any single collection.
  for (const s of scored) {
    if (picked.length >= limit) break;
    const key = s.item.collection || "";
    const used = perCollection.get(key) || 0;
    if (used >= perCollectionCap) continue;
    perCollection.set(key, used + 1);
    picked.push(s.item);
  }

  // Pass 2: if themes are sparse and we came up short, top up ignoring the cap.
  if (picked.length < limit) {
    const chosen = new Set(picked.map((p) => p._id));
    for (const s of scored) {
      if (picked.length >= limit) break;
      if (chosen.has(s.item._id)) continue;
      picked.push(s.item);
      chosen.add(s.item._id);
    }
  }

  // Pass 3: still short (passage has no themes at all) — fall back to same-
  // collection neighbours so the panel is never empty.
  if (picked.length < limit) {
    const chosen = new Set(picked.map((p) => p._id));
    const neighbours = all
      .filter(
        (v) =>
          v._id !== item._id &&
          isReadable(v) &&
          !chosen.has(v._id) &&
          (v.collection || "") === (item.collection || ""),
      )
      .sort((a, b) => passageSortKey(a) - passageSortKey(b));
    for (const v of neighbours) {
      if (picked.length >= limit) break;
      picked.push(v);
    }
  }

  return picked;
}
