"use client";

import { useEffect, useId, useState } from "react";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { useT } from "@/components/LocaleProvider";

type StepIntegrationGateProps = {
  stepId: string;
  integration: string;
  /** Key idea used for a short recall check before unlock. */
  keyIdea?: string;
  done: boolean;
  onComplete: () => void;
  completeLabel?: string;
};

export function StepIntegrationGate({
  stepId,
  integration,
  keyIdea,
  done,
  onComplete,
  completeLabel,
}: StepIntegrationGateProps) {
  const t = useT();
  const [recall, setRecall] = useState("");
  const [revealed, setRevealed] = useState(false);
  const [ready, setReady] = useState(false);
  const checkboxId = useId();
  const recallId = useId();

  useEffect(() => {
    setRecall("");
    setRevealed(false);
    setReady(false);
  }, [stepId, done]);

  if (done) return null;

  const recallPrompt = keyIdea;
  const recallOk = !recallPrompt || revealed;

  return (
    <div className="max-w-[var(--reading-measure)] border-t border-emerald-300/25 pt-4">
      <p className="font-sans text-xs uppercase tracking-[0.16em] text-emerald-200/80">
        {t("learn.gateBefore")}
      </p>
      <p className="mt-2 text-sm leading-relaxed text-stone-200">{integration}</p>

      {recallPrompt ? (
        <div className="mt-4 space-y-3">
          <Label htmlFor={recallId} className="font-sans text-xs uppercase tracking-[0.14em] text-amber-200/75">
            {t("learn.recallLabel")}
          </Label>
          <p className="text-sm leading-relaxed text-stone-300">{t("learn.recallLede")}</p>
          <Textarea
            id={recallId}
            rows={3}
            value={recall}
            onChange={(e) => setRecall(e.target.value)}
            placeholder={t("learn.recallPlaceholder")}
            className="min-h-[5.5rem] border-[rgb(240_201_121_/_0.2)] bg-transparent"
            disabled={revealed}
          />
          {!revealed ? (
            <Button
              type="button"
              variant="secondary"
              size="sm"
              disabled={recall.trim().length < 12}
              onClick={() => setRevealed(true)}
            >
              {t("learn.reveal")}
            </Button>
          ) : (
            <div className="rounded-xl border border-amber-200/20 bg-amber-200/5 px-3 py-3">
              <p className="font-sans text-[10px] uppercase tracking-[0.14em] text-amber-200/70">
                {t("learn.keyIdea")}
              </p>
              <p className="mt-1 text-sm leading-relaxed text-stone-100">{recallPrompt}</p>
              {recall.trim() ? (
                <p className="soft mt-2 text-xs leading-relaxed">{t("learn.yourRecall", { text: recall.trim() })}</p>
              ) : null}
            </div>
          )}
        </div>
      ) : null}

      <Label
        htmlFor={checkboxId}
        className={`mt-4 flex cursor-pointer items-start gap-3 text-sm leading-relaxed font-normal text-stone-200 ${
          !recallOk ? "opacity-50" : ""
        }`}
      >
        <Checkbox
          id={checkboxId}
          checked={ready}
          disabled={!recallOk}
          onCheckedChange={(checked) => setReady(checked === true)}
          className="mt-0.5 border-amber-200/40 data-checked:border-amber-200 data-checked:bg-amber-200 data-checked:text-[#121018]"
        />
        <span>{t("learn.recognize")}</span>
      </Label>
      <Button
        type="button"
        onClick={onComplete}
        disabled={!ready || !recallOk}
        className="mt-4"
      >
        {completeLabel || t("learn.markComplete")}
      </Button>
    </div>
  );
}
