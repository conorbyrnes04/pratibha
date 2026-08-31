"use client";

import Link from "next/link";
import { InkGlyph } from "@/components/InkGlyph";
import { PathStepWell } from "@/components/learn/PathStepWell";
import { StepIntegrationGate } from "@/components/learn/StepIntegrationGate";
import { Button, buttonVariants } from "@/components/ui/button";
import { trailSumiGlyph } from "@/lib/sumiGlyphs";
import type { LearningStepSpec, LearningTrack } from "@/lib/learningPaths";
import type { VerseItem } from "@/lib/types";

export function LearnTrailGate({
  track,
  step,
  items,
  done,
  walkedToday = false,
  pathTitle = "The Path",
  pathId,
  nextTitle,
  onComplete,
  onBack,
  onContinue,
}: {
  track: LearningTrack;
  step: LearningStepSpec;
  items: VerseItem[];
  done: boolean;
  walkedToday?: boolean;
  pathTitle?: string;
  pathId?: string | null;
  nextTitle?: string | null;
  onComplete: () => void;
  onBack: () => void;
  onContinue?: () => void;
}) {
  const glyph = trailSumiGlyph(step.id);

  return (
    <article className="learn-trail-gate">
      <header className="library-header">
        <div className="library-header__body">
          <button type="button" className="passage-reading__meta learn-trail-gate__back" onClick={onBack}>
            ← {pathTitle}
          </button>
          <p className="mt-4 font-sans text-[11px] uppercase tracking-[0.22em] text-amber-200/50">{track.title}</p>
          <div className="learn-trail-gate__mark">
            <InkGlyph glyph={glyph} state={done ? "recognized" : "arising"} size="xl" className="learn-trail__glyph" mask />
          </div>
          <h1 className="library-header__title">{step.title}</h1>
          <p className="library-header__lede">{step.orientation}</p>
        </div>
      </header>

      <div className="learn-trail-gate__body">
        <PathStepWell
          trackId={track.id}
          trackTitle={track.title}
          step={step}
          items={items}
          pathId={pathId}
        />
        <StepIntegrationGate
          stepId={step.id}
          integration={step.integration}
          keyIdea={step.keyIdea}
          done={done}
          onComplete={onComplete}
        />
        {done && walkedToday ? (
          <div className="learn-trail-gate__rest">
            <p className="passage-reading__meta">Walked today</p>
            <p className="library-header__lede">
              {nextTitle
                ? `Enough for today. Tomorrow opens ${nextTitle}.`
                : "Enough for today. You finished the last gate on this path."}
            </p>
            <div className="passage-reading__nav">
              <Link href="/" className={buttonVariants()}>
                Return to Today
              </Link>
              <Button type="button" variant="secondary" onClick={onBack}>
                See the trail
              </Button>
            </div>
            {nextTitle && onContinue ? (
              <p className="today-gate__continue">
                <button type="button" onClick={onContinue}>
                  Walk one more anyway
                </button>
              </p>
            ) : null}
          </div>
        ) : done ? (
          <div className="flex justify-center pt-6">
            <Button type="button" onClick={onBack}>
              Return to the path
            </Button>
          </div>
        ) : null}
      </div>
    </article>
  );
}
