import { stepKey, type CompletedAtMap } from "@/lib/learn/progress";
import { findTraditionTrail } from "@/lib/learn/traditionTrails";
import { LEARNING_TRACKS, type LearningStepSpec, type LearningTrack } from "@/lib/learningPaths";

export function sameCalendarDay(iso: string, now = new Date()): boolean {
  const then = new Date(iso);
  return (
    then.getFullYear() === now.getFullYear() &&
    then.getMonth() === now.getMonth() &&
    then.getDate() === now.getDate()
  );
}

/** Line draws, then the destination glyph forms (same draw+wash as glyph unlock). */
export const TRAIL_SAND_DRAW_MS = 1400;
export const TRAIL_GLYPH_FORM_MS = 2600;
export const TRAIL_GATE_LEAVE_MS = 560;
export const TRAIL_ARRIVE_TOTAL_MS = TRAIL_SAND_DRAW_MS + TRAIL_GLYPH_FORM_MS + 200;
export const TRAIL_ARRIVE_SESSION_KEY = "pratibha.learn.arrive";

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
  /** A spine gate was finished today — the next node waits until tomorrow. */
  rested: boolean;
  next: TrailNode | null;
};

function sitAt(
  nodes: TrailNode[],
  index: number,
  walked: number,
  complete: boolean,
  rested: boolean,
): TrailSit | null {
  const node = nodes[index];
  if (!node) return null;
  const step = node.track.steps[node.stepIndex];
  if (!step) return null;
  const next = nodes[index + 1] ?? null;
  return { node, step, index, total: nodes.length, walked, complete, rested, next };
}

/** The gate Today should open — first unfinished node, or today's finished gate if the day is walked. */
export function currentTrailSit(
  progress: Record<string, boolean>,
  pathId?: string | null,
  completedAt?: CompletedAtMap,
  now = new Date(),
): TrailSit | null {
  const nodes = buildTrail(pathId);
  if (nodes.length === 0) return null;
  const walked = nodes.filter((node) => progress[node.key]).length;
  const complete = walked >= nodes.length;
  const openIndex = complete ? nodes.length - 1 : nodes.findIndex((node) => !progress[node.key]);
  if (openIndex < 0) return null;

  if (!complete && openIndex > 0 && completedAt) {
    const justWalked = nodes[openIndex - 1];
    const at = completedAt[justWalked.key];
    if (at && sameCalendarDay(at, now)) {
      return sitAt(nodes, openIndex - 1, walked, false, true);
    }
  }

  if (complete && completedAt) {
    const last = nodes[nodes.length - 1];
    const at = last ? completedAt[last.key] : undefined;
    if (at && sameCalendarDay(at, now)) {
      return sitAt(nodes, nodes.length - 1, walked, true, true);
    }
  }

  return sitAt(nodes, openIndex, walked, complete, false);
}
