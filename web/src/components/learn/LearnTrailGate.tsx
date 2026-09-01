"use client";

import { useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { TRAIL_GATE_COMPLETE_MS } from "@/lib/learn/trail";
import { InkGlyph } from "@/components/InkGlyph";
import { LearnTrailReading } from "@/components/learn/LearnTrailReading";
import { PathStepWell } from "@/components/learn/PathStepWell";
import { StepIntegrationGate } from "@/components/learn/StepIntegrationGate";
import { trailSumiGlyph } from "@/lib/sumiGlyphs";
import type { LearningStepSpec, LearningTrack } from "@/lib/learningPaths";
import type { VerseItem } from "@/lib/types";
import { useT } from "@/components/LocaleProvider";
import { GateCircleSection } from "@/components/GateCircleSection";
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
  const [completing, setCompleting] = useState(false);
  const completingRef = useRef(false);
  const completeTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const onCompleteRef = useRef(onComplete);
  onCompleteRef.current = onComplete;

  useEffect(() => {
    setReady(true);
  }, []);

  useEffect(() => {
    setReading(null);
    setCompleting(false);
    completingRef.current = false;
    if (completeTimerRef.current) {
      clearTimeout(completeTimerRef.current);
      completeTimerRef.current = null;
    }
  }, [step.id]);

  useEffect(
    () => () => {
      if (completeTimerRef.current) clearTimeout(completeTimerRef.current);
    },
    [],
  );

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

  function dismiss() {
    if (completingRef.current || leaving) return;
    onBack();
  }

  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if (event.key !== "Escape") return;
      if (reading) {
        event.preventDefault();
        setReading(null);
        return;
      }
      dismiss();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [onBack, reading, leaving]);

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

  // Flourish inside the gate, then hand off so the parent can dissipate
  // the overlay and draw the line to the next node. Do not wait on Circle.
  function runComplete() {
    if (completingRef.current || leaving) return;
    completingRef.current = true;
    setCompleting(true);
    if (completeTimerRef.current) clearTimeout(completeTimerRef.current);
    completeTimerRef.current = setTimeout(() => {
      completeTimerRef.current = null;
      onCompleteRef.current();
    }, TRAIL_GATE_COMPLETE_MS);
  }

  const integrationSlot = completing ? (
    <div className="learn-gate-complete" role="status" aria-live="polite">
      <p className="learn-gate-complete__mark">{t("learn.stepComplete")}</p>
      <p className="learn-gate-complete__lede">{t("learn.stepCompleteLede")}</p>
    </div>
  ) : (
    <StepIntegrationGate
      stepId={step.id}
      integration={study.integration}
      keyIdea={study.keyIdea}
      done={done}
      onComplete={runComplete}
    />
  );

  const panel = (
    <div
      className={`learn-trail-gate-layer ${leaving ? "learn-trail-gate-layer--leave" : ""}`}
      data-learn-gate-layer={leaving ? "leave" : "open"}
    >
      <button
        type="button"
        className="learn-trail-gate-layer__scrim"
        aria-label={reading ? t("learn.returnGate") : t("learn.closeGate")}
        onClick={reading ? closeReading : dismiss}
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
              <button type="button" className="passage-reading__meta learn-trail-gate__back" onClick={dismiss}>
                ← {pathTitle}
              </button>
              <p className="learn-trail-gate__track">{trackStudy.title}</p>
              <div className="learn-trail-gate__mark">
                <InkGlyph
                  glyph={glyph}
                  state={done || completing ? "recognized" : "arising"}
                  size="xl"
                  className={`learn-trail__glyph${completing ? " learn-trail__glyph--bloom" : ""}`}
                  mask
                />
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
                integrationSlot={integrationSlot}
              />
              {step.passageId ? (
                <GateCircleSection
                  verseId={step.passageId}
                  verseTitle={study.title}
                  idea={study.keyIdea}
                />
              ) : null}
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
