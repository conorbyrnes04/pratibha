import { stepKey } from "@/lib/learn/progress";
import { findTraditionTrail } from "@/lib/learn/traditionTrails";
import { LEARNING_TRACKS, type LearningStepSpec, type LearningTrack } from "@/lib/learningPaths";

/** Line draws, then the destination glyph forms. */
export const TRAIL_SAND_DRAW_MS = 1400;
export const TRAIL_GLYPH_FORM_MS = 1050;
export const TRAIL_ARRIVE_TOTAL_MS = TRAIL_SAND_DRAW_MS + TRAIL_GLYPH_FORM_MS + 200;

export type TrailNode = {
  trackId: string;
  stepId: string;
  stepIndex: number;
  track: LearningTrack;
  title: string;
  orientation: string;
  key: string;
  sectionIndex: number;
  sectionLabel: string;
  isFirstInSection: boolean;
};

/** One continuous trail for the essential spine, or a chosen tradition. */
export function buildTrail(pathId?: string | null): TrailNode[] {
  const nodes: TrailNode[] = [];
  const trackIds = findTraditionTrail(pathId).trackIds;

  trackIds.forEach((trackId, sectionIndex) => {
    const track = LEARNING_TRACKS.find((t) => t.id === trackId);
    if (!track) return;

    track.steps.forEach((step, stepIndex) => {
      nodes.push({
        trackId,
        stepId: step.id,
        stepIndex,
        track,
        title: step.title,
        orientation: step.orientation,
        key: stepKey(trackId, step.id),
        sectionIndex,
        sectionLabel: track.title,
        isFirstInSection: stepIndex === 0,
      });
    });
  });

  return nodes;
}

export function trailCurrentIndex(progress: Record<string, boolean>, pathId?: string | null): number {
  const nodes = buildTrail(pathId);
  const idx = nodes.findIndex((node) => !progress[node.key]);
  return idx === -1 ? Math.max(0, nodes.length - 1) : idx;
}

export type TrailSit = {
  node: TrailNode;
  step: LearningStepSpec;
  index: number;
  total: number;
  walked: number;
  complete: boolean;
};

/** The gate Today should open — first unfinished node on the essential spine. */
export function currentTrailSit(progress: Record<string, boolean>, pathId?: string | null): TrailSit | null {
  const nodes = buildTrail(pathId);
  if (nodes.length === 0) return null;
  const walked = nodes.filter((node) => progress[node.key]).length;
  const complete = walked >= nodes.length;
  const index = complete ? nodes.length - 1 : nodes.findIndex((node) => !progress[node.key]);
  const node = nodes[index];
  if (!node) return null;
  const step = node.track.steps[node.stepIndex];
  if (!step) return null;
  return { node, step, index, total: nodes.length, walked, complete };
}
