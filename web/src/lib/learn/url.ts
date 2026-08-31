export type LearnSearch = {
  traditionId: string | null;
  trackId: string | null;
  stepId: string | null;
  threadId: string | null;
  beadId: string | null;
};

export type LearnHrefOpts = {
  traditionId?: string | null;
  trackId?: string | null;
  stepId?: string | null;
  threadId?: string | null;
  beadId?: string | null;
};

export type LearnView = "chooser" | "trail" | "journey" | "bead" | "lineage";

export function learnViewFromSearch(search: LearnSearch): LearnView {
  if (search.threadId && search.beadId) return "bead";
  if (search.threadId) return "journey";
  if (search.trackId) return "lineage";
  if (search.traditionId) return "trail";
  return "chooser";
}

/** Build /learn deep link. Thread-only URLs omit track so the theme stays primary. */
export function learnHref(trackIdOrOpts: string | LearnHrefOpts, stepId?: string | null): string {
  const opts: LearnHrefOpts =
    typeof trackIdOrOpts === "string"
      ? { trackId: trackIdOrOpts, stepId }
      : trackIdOrOpts;

  const params = new URLSearchParams();
  if (opts.traditionId) params.set("tradition", opts.traditionId);
  if (opts.trackId) params.set("track", opts.trackId);
  if (opts.stepId && opts.stepId !== "__none__") params.set("step", opts.stepId);
  if (opts.threadId) params.set("thread", opts.threadId);
  if (opts.beadId) params.set("bead", opts.beadId);
  const qs = params.toString();
  return qs ? `/learn?${qs}` : "/learn";
}

export function parseLearnSearch(search: string): LearnSearch {
  const sp = new URLSearchParams(search);
  return {
    traditionId: sp.get("tradition"),
    trackId: sp.get("track"),
    stepId: sp.get("step"),
    threadId: sp.get("thread"),
    beadId: sp.get("bead"),
  };
}
