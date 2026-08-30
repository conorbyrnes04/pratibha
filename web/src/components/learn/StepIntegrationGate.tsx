"use client";

import { useEffect, useId, useState } from "react";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

export type ThemeGateSpec = {
  move: string;
  /** Tradition of the previous bead, if any. */
  previousTradition?: string | null;
};

type StepIntegrationGateProps = {
  stepId: string;
  integration: string;
  /** Key idea used for a short recall check before unlock (path mode). */
  keyIdea?: string;
  done: boolean;
  onComplete: () => void;
  /** Override primary button label (e.g. thread auto-advance). */
  completeLabel?: string;
  /** Theme mode: recall the move and name the divergence. */
  theme?: ThemeGateSpec | null;
};

export function StepIntegrationGate({
  stepId,
  integration,
  keyIdea,
  done,
  onComplete,
  completeLabel,
  theme,
}: StepIntegrationGateProps) {
  const [recall, setRecall] = useState("");
  const [divergence, setDivergence] = useState("");
  const [revealed, setRevealed] = useState(false);
  const [ready, setReady] = useState(false);
  const checkboxId = useId();
  const recallId = useId();
  const divergenceId = useId();

  useEffect(() => {
    setRecall("");
    setDivergence("");
    setRevealed(false);
    setReady(false);
  }, [stepId, done, theme?.move]);

  if (done) return null;

  const isTheme = Boolean(theme?.move);
  const recallPrompt = isTheme ? theme!.move : keyIdea;
  const recallOk = !recallPrompt || revealed;
  const divergenceNeeded = isTheme && Boolean(theme?.previousTradition);
  const divergenceOk = !divergenceNeeded || divergence.trim().length >= 12;

  return (
    <div className="max-w-[var(--reading-measure)] border-t border-emerald-300/25 pt-4">
      <p className="font-sans text-xs uppercase tracking-[0.16em] text-emerald-200/80">
        {isTheme ? "Theme gate · before the next bead" : "Gate · before you move on"}
      </p>
      <p className="mt-2 text-sm leading-relaxed text-stone-200">{integration}</p>

      {recallPrompt ? (
        <div className="mt-4 space-y-3">
          <Label htmlFor={recallId} className="font-sans text-xs uppercase tracking-[0.14em] text-amber-200/75">
            Recall · without looking up
          </Label>
          <p className="text-sm leading-relaxed text-stone-300">
            {isTheme
              ? "In one or two sentences, restate this bead's move in the theme — why it is here."
              : "In one or two sentences, restate the key idea of this gate from memory."}
          </p>
          <Textarea
            id={recallId}
            rows={3}
            value={recall}
            onChange={(e) => setRecall(e.target.value)}
            placeholder="Write from memory…"
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
              {isTheme ? "Reveal the move" : "Reveal key idea"}
            </Button>
          ) : (
            <div className="rounded-xl border border-amber-200/20 bg-amber-200/5 px-3 py-3">
              <p className="font-sans text-[10px] uppercase tracking-[0.14em] text-amber-200/70">
                {isTheme ? "The move" : "Key idea"}
              </p>
              <p className="mt-1 text-sm leading-relaxed text-stone-100">{recallPrompt}</p>
              {recall.trim() ? (
                <p className="soft mt-2 text-xs leading-relaxed">Your recall: {recall.trim()}</p>
              ) : null}
            </div>
          )}
        </div>
      ) : null}

      {divergenceNeeded ? (
        <div className="mt-4 space-y-3">
          <Label htmlFor={divergenceId} className="font-sans text-xs uppercase tracking-[0.14em] text-amber-200/75">
            Divergence
          </Label>
          <p className="text-sm leading-relaxed text-stone-300">
            Where does this tradition part from {theme?.previousTradition}? One sentence is enough.
          </p>
          <Textarea
            id={divergenceId}
            rows={2}
            value={divergence}
            onChange={(e) => setDivergence(e.target.value)}
            placeholder="This tradition parts by…"
            className="min-h-[4rem] border-[rgb(240_201_121_/_0.2)] bg-transparent"
          />
        </div>
      ) : null}

      <Label
        htmlFor={checkboxId}
        className={`mt-4 flex cursor-pointer items-start gap-3 text-sm leading-relaxed font-normal text-stone-200 ${
          !recallOk || !divergenceOk ? "opacity-50" : ""
        }`}
      >
        <Checkbox
          id={checkboxId}
          checked={ready}
          disabled={!recallOk || !divergenceOk}
          onCheckedChange={(checked) => setReady(checked === true)}
          className="mt-0.5 border-amber-200/40 data-checked:border-amber-200 data-checked:bg-amber-200 data-checked:text-[#121018]"
        />
        <span>I recognize this in experience — or I&apos;m willing to keep practicing at this gate.</span>
      </Label>
      <Button
        type="button"
        onClick={onComplete}
        disabled={!ready || !recallOk || !divergenceOk}
        className="mt-4"
      >
        {completeLabel || "Mark complete"}
      </Button>
    </div>
  );
}
