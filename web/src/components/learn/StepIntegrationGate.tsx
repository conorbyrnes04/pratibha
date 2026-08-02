"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";

type StepIntegrationGateProps = {
  stepId: string;
  integration: string;
  done: boolean;
  onComplete: () => void;
  /** Override primary button label (e.g. thread auto-advance). */
  completeLabel?: string;
};

export function StepIntegrationGate({
  stepId,
  integration,
  done,
  onComplete,
  completeLabel,
}: StepIntegrationGateProps) {
  const [ready, setReady] = useState(false);

  useEffect(() => {
    setReady(false);
  }, [stepId, done]);

  if (done) return null;

  return (
    <div className="rounded-2xl border border-emerald-300/25 bg-emerald-300/5 p-4">
      <p className="font-sans text-xs uppercase tracking-[0.16em] text-emerald-200/80">Gate · before you move on</p>
      <p className="mt-2 text-sm leading-relaxed text-stone-200">{integration}</p>
      <label className="mt-4 flex cursor-pointer items-start gap-3 text-sm leading-relaxed text-stone-200">
        <input
          type="checkbox"
          checked={ready}
          onChange={(e) => setReady(e.target.checked)}
          className="mt-1 h-4 w-4 shrink-0 rounded border-amber-200/40 bg-transparent accent-amber-200"
        />
        <span>I recognize this in experience — or I&apos;m willing to keep practicing at this gate.</span>
      </label>
      <Button type="button" onClick={onComplete} disabled={!ready} className="mt-4">
        {completeLabel || "Mark complete"}
      </Button>
    </div>
  );
}
