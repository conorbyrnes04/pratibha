"use client";

import { useEffect, useId, useState } from "react";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";

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
  const checkboxId = useId();

  useEffect(() => {
    setReady(false);
  }, [stepId, done]);

  if (done) return null;

  return (
    <div className="rounded-2xl border border-emerald-300/25 bg-emerald-300/5 p-4">
      <p className="font-sans text-xs uppercase tracking-[0.16em] text-emerald-200/80">Gate · before you move on</p>
      <p className="mt-2 text-sm leading-relaxed text-stone-200">{integration}</p>
      <Label
        htmlFor={checkboxId}
        className="mt-4 flex cursor-pointer items-start gap-3 text-sm leading-relaxed font-normal text-stone-200"
      >
        <Checkbox
          id={checkboxId}
          checked={ready}
          onCheckedChange={(checked) => setReady(checked === true)}
          className="mt-0.5 border-amber-200/40 data-checked:border-amber-200 data-checked:bg-amber-200 data-checked:text-[#121018]"
        />
        <span>I recognize this in experience — or I&apos;m willing to keep practicing at this gate.</span>
      </Label>
      <Button type="button" onClick={onComplete} disabled={!ready} className="mt-4">
        {completeLabel || "Mark complete"}
      </Button>
    </div>
  );
}
