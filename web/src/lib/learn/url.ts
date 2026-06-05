export function learnHref(trackId: string, stepId?: string | null): string {
  const params = new URLSearchParams();
  params.set("track", trackId);
  if (stepId && stepId !== "__none__") params.set("step", stepId);
  return `/learn?${params.toString()}`;
}

export function parseLearnSearch(search: string): { trackId: string | null; stepId: string | null } {
  const sp = new URLSearchParams(search);
  return {
    trackId: sp.get("track"),
    stepId: sp.get("step"),
  };
}
