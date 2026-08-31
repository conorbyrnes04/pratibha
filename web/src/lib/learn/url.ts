export type LearnSearch = {
  pathId: string | null;
  trackId: string | null;
  stepId: string | null;
  /** Retired theme URLs; canonicalize onto a trail gate. */
  threadId: string | null;
  beadId: string | null;
};

export type LearnHrefOpts = {
  pathId?: string | null;
  trackId?: string | null;
  stepId?: string | null;
};

export type LearnView = "home" | "gate";

export function learnViewFromSearch(search: LearnSearch): LearnView {
  if (search.trackId && search.stepId) return "gate";
  return "home";
}

/** Build /learn deep link. Trails are the only guided walk. */
export function learnHref(trackIdOrOpts: string | LearnHrefOpts, stepId?: string | null): string {
  const opts: LearnHrefOpts =
    typeof trackIdOrOpts === "string"
      ? { trackId: trackIdOrOpts, stepId }
      : trackIdOrOpts;

  const params = new URLSearchParams();
  if (opts.pathId) params.set("path", opts.pathId);
  if (opts.trackId) params.set("track", opts.trackId);
  if (opts.stepId && opts.stepId !== "__none__") params.set("step", opts.stepId);
  const qs = params.toString();
  return qs ? `/learn?${qs}` : "/learn";
}

export function parseLearnSearch(search: string): LearnSearch {
  const sp = new URLSearchParams(search);
  return {
    pathId: sp.get("path"),
    trackId: sp.get("track"),
    stepId: sp.get("step"),
    threadId: sp.get("thread"),
    beadId: sp.get("bead"),
  };
}
