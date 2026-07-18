export type LearnSearch = {
  trackId: string | null;
  stepId: string | null;
  threadId: string | null;
  beadId: string | null;
};

export type LearnHrefOpts = {
  trackId: string;
  stepId?: string | null;
  threadId?: string | null;
  beadId?: string | null;
};

/** Build /learn deep link. Thread params keep horizontal context across path steps. */
export function learnHref(trackIdOrOpts: string | LearnHrefOpts, stepId?: string | null): string {
  const opts: LearnHrefOpts =
    typeof trackIdOrOpts === "string"
      ? { trackId: trackIdOrOpts, stepId }
      : trackIdOrOpts;

  const params = new URLSearchParams();
  params.set("track", opts.trackId);
  if (opts.stepId && opts.stepId !== "__none__") params.set("step", opts.stepId);
  if (opts.threadId) params.set("thread", opts.threadId);
  if (opts.beadId) params.set("bead", opts.beadId);
  return `/learn?${params.toString()}`;
}

export function parseLearnSearch(search: string): LearnSearch {
  const sp = new URLSearchParams(search);
  return {
    trackId: sp.get("track"),
    stepId: sp.get("step"),
    threadId: sp.get("thread"),
    beadId: sp.get("bead"),
  };
}
