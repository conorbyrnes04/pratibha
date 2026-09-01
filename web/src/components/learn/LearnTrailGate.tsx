"use client";

import { useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { TRAIL_GATE_COMPLETE_MS } from "@/lib/learn/trail";
import { useQuery } from "convex/react";
import { api } from "../../../convex/_generated/api";
import { InkGlyph } from "@/components/InkGlyph";
import { LearnTrailReading } from "@/components/learn/LearnTrailReading";
import { PathStepWell } from "@/components/learn/PathStepWell";
import { StepIntegrationGate } from "@/components/learn/StepIntegrationGate";
import { CircleOfferForm } from "@/components/CircleOfferForm";
import { useAuth } from "@/components/AuthProvider";
import { CONVEX_ENABLED } from "@/lib/convexConfigured";
import { trailSumiGlyph } from "@/lib/sumiGlyphs";
import type { LearningStepSpec, LearningTrack } from "@/lib/learningPaths";
import type { VerseItem } from "@/lib/types";
import { Button } from "@/components/ui/button";
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
  const { user } = useAuth();
  const mine = useQuery(
    api.studentCommentaries.getMine,
    CONVEX_ENABLED && user && step.passageId ? { verseId: step.passageId } : "skip",
  );
  const [ready, setReady] = useState(false);
  const [reading, setReading] = useState<VerseItem | null>(null);
  const [circleBeat, setCircleBeat] = useState(false);
  const [completing, setCompleting] = useState(false);
  const completeTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    setReady(true);
  }, []);

  useEffect(() => {
    setReading(null);
    setCircleBeat(false);
    setCompleting(false);
  }, [step.id]);

  useEffect(() => () => {
    if (completeTimerRef.current) clearTimeout(completeTimerRef.current);
  }, []);

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

  // Hold a brief completion flourish (glyph washes to gold) inside the gate,
  // then hand off to the parent, which dissipates the gate back to the walk.
  function runComplete() {
    if (completing) return;
    setCompleting(true);
    if (completeTimerRef.current) clearTimeout(completeTimerRef.current);
    completeTimerRef.current = setTimeout(() => {
      completeTimerRef.current = null;
      onComplete();
    }, TRAIL_GATE_COMPLETE_MS);
  }

  function onGateRecognized() {
    if (done || !step.passageId || !CONVEX_ENABLED || mine?.status === "offered") {
      runComplete();
      return;
    }
    setCircleBeat(true);
  }

  const integrationSlot = completing ? (
    <div className="learn-gate-complete" role="status" aria-live="polite">
      <p className="learn-gate-complete__mark">{t("learn.stepComplete")}</p>
      <p className="learn-gate-complete__lede">{t("learn.stepCompleteLede")}</p>
    </div>
  ) : (
    <>
      <StepIntegrationGate
        stepId={step.id}
        integration={study.integration}
        keyIdea={study.keyIdea}
        done={done || circleBeat}
        onComplete={onGateRecognized}
      />
      {circleBeat && !done && step.passageId ? (
        <LearnTrailCircleBeat
          verseId={step.passageId}
          verseTitle={study.title}
          onContinue={runComplete}
        />
      ) : null}
    </>
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
              <p className="learn-trail-gate__track">{trackStudy.title}</p>
              <div className="learn-trail-gate__mark">
                <InkGlyph
                  glyph={glyph}
                  state={done || circleBeat || completing ? "recognized" : "arising"}
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

function LearnTrailCircleBeat({
  verseId,
  verseTitle,
  onContinue,
}: {
  verseId: string;
  verseTitle: string;
  onContinue: () => void;
}) {
  const t = useT();
  const { user } = useAuth();
  const mine = useQuery(api.studentCommentaries.getMine, CONVEX_ENABLED && user ? { verseId } : "skip");

  useEffect(() => {
    if (mine?.status === "offered") onContinue();
  }, [mine?.status, onContinue]);

  if (mine?.status === "offered") {
    return <p className="soft mt-6 text-sm">{t("circle.gateOffered")}</p>;
  }

  return (
    <div className="mt-6 max-w-[var(--reading-measure)] border-t border-amber-200/20 pt-6">
      <p className="passage-layer__label">{t("circle.gateOfferTitle")}</p>
      <p className="soft mt-2 text-sm leading-relaxed">{t("circle.gateOfferLede")}</p>
      <CircleOfferForm
        verseId={verseId}
        verseTitle={verseTitle}
        compact
        onOffered={onContinue}
        loginNext="/learn"
      />
      <Button type="button" variant="ghost" size="sm" className="mt-3" onClick={onContinue}>
        {t("circle.gateSkip")}
      </Button>
    </div>
  );
}
