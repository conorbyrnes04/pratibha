"use client";

import { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import { InkGlyph } from "@/components/InkGlyph";
import { LearnTrailReading } from "@/components/learn/LearnTrailReading";
import { PathStepWell } from "@/components/learn/PathStepWell";
import { StepIntegrationGate } from "@/components/learn/StepIntegrationGate";
import { trailSumiGlyph } from "@/lib/sumiGlyphs";
import type { LearningStepSpec, LearningTrack } from "@/lib/learningPaths";
import type { VerseItem } from "@/lib/types";
import { useT } from "@/components/LocaleProvider";
import { useLocalizedStep, useLocalizedTrack } from "@/components/useLocalizedStudy";

export function LearnTrailGate({
  track,
  step,
  items,
  done,
  pathTitle = "The Path",
  pathId,
  leaving = false,
  onComplete,
  onBack,
}: {
  track: LearningTrack;
  step: LearningStepSpec;
  items: VerseItem[];
  done: boolean;
  pathTitle?: string;
  pathId?: string | null;
  leaving?: boolean;
  onComplete: () => void;
  onBack: () => void;
}) {
  const t = useT();
  const study = useLocalizedStep(step);
  const trackStudy = useLocalizedTrack(track);
  const glyph = trailSumiGlyph(step.id);
  const [ready, setReady] = useState(false);
  const [reading, setReading] = useState<VerseItem | null>(null);

  useEffect(() => {
    setReady(true);
  }, []);

  useEffect(() => {
    setReading(null);
  }, [step.id]);

  useEffect(() => {
    if (leaving) setReading(null);
  }, [leaving]);

  useEffect(() => {
    if (leaving) {
      document.body.style.overflow = "";
      return;
    }
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = prev;
    };
  }, [leaving]);

  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if (event.key !== "Escape") return;
      if (reading) {
        event.preventDefault();
        setReading(null);
        return;
      }
      onBack();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onBack, reading]);

  useEffect(() => {
    if (!reading) return;
    const id = window.requestAnimationFrame(() => {
      document.getElementById("learn-trail-reading-back")?.focus();
    });
    return () => window.cancelAnimationFrame(id);
  }, [reading]);

  function closeReading() {
    setReading(null);
  }

  const panel = (
    <div
      className={`learn-trail-gate-layer ${leaving ? "learn-trail-gate-layer--leave" : ""}`}
      data-learn-gate-layer={leaving ? "leave" : "open"}
    >
      <button
        type="button"
        className="learn-trail-gate-layer__scrim"
        aria-label={reading ? t("learn.returnGate") : t("learn.closeGate")}
        onClick={reading ? closeReading : onBack}
      />
      <div className={`learn-trail-gate-stack ${reading ? "learn-trail-gate-stack--reading" : ""}`}>
        <article
          role="dialog"
          aria-modal="true"
          aria-labelledby={reading ? "learn-trail-reading-title" : "learn-trail-gate-title"}
          className="learn-trail-gate"
        >
          <div inert={reading ? true : undefined}>
            <header className="learn-trail-gate__header">
              <button type="button" className="passage-reading__meta learn-trail-gate__back" onClick={onBack}>
                ← {pathTitle}
              </button>
              <p className="mt-4 font-sans text-[11px] uppercase tracking-[0.22em] text-amber-200/50">{trackStudy.title}</p>
              <div className="learn-trail-gate__mark">
                <InkGlyph glyph={glyph} state={done ? "recognized" : "arising"} size="xl" className="learn-trail__glyph" mask />
              </div>
              <h1 id="learn-trail-gate-title" className="library-header__title">
                {study.title}
              </h1>
              <p className="library-header__lede">{study.orientation}</p>
            </header>

            <div className="learn-trail-gate__body">
              <PathStepWell
                trackId={track.id}
                trackTitle={trackStudy.title}
                step={study}
                items={items}
                pathId={pathId}
                onOpenPassage={setReading}
              />
              <StepIntegrationGate
                stepId={step.id}
                integration={study.integration}
                keyIdea={study.keyIdea}
                done={done}
                onComplete={onComplete}
              />
            </div>
          </div>
        </article>
        {reading ? (
          <LearnTrailReading item={reading} gateTitle={study.title} onBack={closeReading} />
        ) : null}
      </div>
    </div>
  );

  if (!ready) return null;
  return createPortal(panel, document.body);
}
