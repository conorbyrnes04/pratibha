"use client";

import { InkGlyph } from "@/components/InkGlyph";
import { PathStepWell } from "@/components/learn/PathStepWell";
import { StepIntegrationGate } from "@/components/learn/StepIntegrationGate";
import { Button } from "@/components/ui/button";
import { trailSumiGlyph } from "@/lib/sumiGlyphs";
import type { LearningStepSpec, LearningTrack } from "@/lib/learningPaths";
import type { VerseItem } from "@/lib/types";

export function LearnTrailGate({
  track,
  step,
  items,
  done,
  pathTitle = "The Path",
  pathId,
  onComplete,
  onBack,
}: {
  track: LearningTrack;
  step: LearningStepSpec;
  items: VerseItem[];
  done: boolean;
  pathTitle?: string;
  pathId?: string | null;
  onComplete: () => void;
  onBack: () => void;
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
        {done ? (
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
