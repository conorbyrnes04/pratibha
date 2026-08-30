"use client";

import { useEffect, useRef } from "react";
import { SpandaMedallion } from "@/components/InkGlyph";
import { Button } from "@/components/ui/button";
import { PathStepWell } from "@/components/learn/PathStepWell";
import { StepIntegrationGate } from "@/components/learn/StepIntegrationGate";
import { stepKey, type ProgressMap } from "@/lib/learn/progress";
import { LEARNING_TRACKS, RECOMMENDED_SPINE, type LearningTrack } from "@/lib/learningPaths";
import { unitSumiGlyph } from "@/lib/sumiGlyphs";
import type { VerseItem } from "@/lib/types";

type LearnTrailProps = {
  progress: ProgressMap;
  hydrated: boolean;
  /** Currently open gate (if any). */
  openStepKey?: string | null;
  /** Called when user taps a gate node to open/close it. */
  onToggleGate: (trackId: string, stepId: string, isOpen: boolean) => void;
  /** Called when a gate is completed. */
  onComplete: (trackId: string, stepId: string) => void;
  /** Scroll target: the key of the gate we should scroll to. */
  scrollToKey?: string | null;
  /** Verse items for passages in PathStepWell. */
  items: VerseItem[];
};

type TrailNode = {
  trackId: string;
  stepId: string;
  stepIndex: number;
  track: LearningTrack;
  title: string;
  orientation: string;
  key: string;
  /** Which track section this node belongs to (for section headers). */
  sectionIndex: number;
  sectionLabel: string;
  /** True if this is the first node in a new section. */
  isFirstInSection: boolean;
};

/**
 * Build one continuous trail from RECOMMENDED_SPINE tracks.
 * Each track becomes a "section" (like Duolingo units), and we stitch
 * all their steps into one sequential path.
 */
function buildTrail(): TrailNode[] {
  const nodes: TrailNode[] = [];
  const trackIds = RECOMMENDED_SPINE.length > 0 ? RECOMMENDED_SPINE : LEARNING_TRACKS.map((t) => t.id);

  trackIds.forEach((trackId, sectionIndex) => {
    const track = LEARNING_TRACKS.find((t) => t.id === trackId);
    if (!track) return;

    track.steps.forEach((step, stepIndex) => {
      nodes.push({
        trackId,
        stepId: step.id,
        stepIndex,
        track,
        title: step.title,
        orientation: step.orientation,
        key: stepKey(trackId, step.id),
        sectionIndex,
        sectionLabel: track.title,
        isFirstInSection: stepIndex === 0,
      });
    });
  });

  return nodes;
}

export function LearnTrail({
  progress,
  hydrated,
  openStepKey,
  onToggleGate,
  onComplete,
  scrollToKey,
  items,
}: LearnTrailProps) {
  const nodes = buildTrail();
  const nodeRefs = useRef<Record<string, HTMLElement | null>>({});

  // Find the current gate (first incomplete one) and compute states
  let currentIndex = nodes.findIndex((n) => !progress[n.key]);
  if (currentIndex === -1) currentIndex = nodes.length - 1; // All complete

  // Scroll to target gate when requested
  useEffect(() => {
    if (!scrollToKey) return;
    const el = nodeRefs.current[scrollToKey];
    if (el) {
      requestAnimationFrame(() => {
        el.scrollIntoView({ behavior: "smooth", block: "center" });
      });
    }
  }, [scrollToKey]);

  return (
    <div className="section-stack">
      <header className="library-header">
        <div className="library-header__body">
          <p className="passage-reading__meta">Guided study</p>
          <h1 className="library-header__title">The Path</h1>
          <p className="library-header__lede">
            Follow the trail gate by gate. Each node is one step on the way.
            The path reveals itself as you walk it.
          </p>
        </div>
      </header>

      <section className="learn-trail mt-8 pb-16">
        <ul className="relative mx-auto max-w-md list-none space-y-6">
          {nodes.map((node, i) => {
            const done = !!progress[node.key];
            const isCurrent = i === currentIndex && !done;
            const isLocked = i > currentIndex;
            const isOpen = openStepKey === node.key;
            
            // State for the glyph
            let state: "recognized" | "arising" | "unmanifest" = "unmanifest";
            if (done) state = "recognized";
            else if (isCurrent) state = "arising";

            // Snake pattern: alternate left (0) and right (1) more subtly
            const side = i % 2;
            const offsetClass = side === 0 ? "mr-auto" : "ml-auto";
            const maxWidth = "max-w-[280px]";
            
            // Glyph for this step (stable per step ID)
            const glyph = unitSumiGlyph(node.stepId);

            return (
              <li
                key={node.key}
                ref={(el) => {
                  nodeRefs.current[node.key] = el;
                }}
                className="relative"
              >
                {/* Section header if first in section */}
                {node.isFirstInSection && i > 0 ? (
                  <div className="mb-10 mt-16 text-center">
                    <div className="mx-auto h-px w-24 bg-gradient-to-r from-transparent via-amber-200/25 to-transparent" />
                    <p className="mt-4 font-sans text-[11px] uppercase tracking-[0.22em] text-amber-200/45">
                      {node.sectionLabel}
                    </p>
                  </div>
                ) : node.isFirstInSection ? (
                  <div className="mb-8 text-center">
                    <p className="font-sans text-[11px] uppercase tracking-[0.22em] text-amber-200/45">
                      {node.sectionLabel}
                    </p>
                  </div>
                ) : null}

                <div className={`relative ${offsetClass} ${maxWidth} ${isLocked ? "opacity-35" : "opacity-100"} transition-opacity duration-300`}>
                  {/* Node button */}
                  <button
                    type="button"
                    onClick={() => {
                      if (isLocked) return;
                      onToggleGate(node.trackId, node.stepId, isOpen);
                    }}
                    disabled={isLocked}
                    className={`group relative block w-full text-left transition-all duration-300 ${
                      isLocked ? "cursor-not-allowed" : "hover:scale-102 active:scale-[0.98]"
                    } ${
                      isCurrent && !isOpen ? "scale-[1.02]" : "scale-100"
                    }`}
                    aria-label={
                      done
                        ? `${node.title} - Complete`
                        : isCurrent
                          ? `${node.title} - Current gate`
                          : `${node.title} - Locked`
                    }
                  >
                    {/* Medallion */}
                    <div
                      className={`mx-auto flex items-center justify-center transition-all duration-500 ${
                        isCurrent ? "h-24 w-24" : "h-20 w-20"
                      }`}
                    >
                      <SpandaMedallion
                        glyph={glyph}
                        state={state}
                        size={isCurrent ? "lg" : "md"}
                        className={isCurrent ? "shadow-[0_0_32px_rgba(240,201,121,0.25)]" : ""}
                      />
                    </div>

                    {/* Label below medallion */}
                    <div className="mt-4 text-center">
                      <h3
                        className={`px-4 text-sm font-medium leading-snug transition-colors duration-300 ${
                          done
                            ? "text-emerald-100"
                            : isCurrent
                              ? "text-amber-100"
                              : isLocked
                                ? "text-stone-500"
                                : "text-stone-400"
                        }`}
                      >
                        {node.title}
                      </h3>
                      {(isCurrent || done) && !isOpen ? (
                        <p className="mt-2 px-6 text-xs leading-relaxed text-stone-400">
                          {node.orientation.split('.')[0]}.
                        </p>
                      ) : null}
                    </div>

                    {/* Completion badge */}
                    {done && !isOpen ? (
                      <div className="mt-3 flex justify-center">
                        <span className="rounded-full border border-emerald-300/35 bg-emerald-300/8 px-2.5 py-0.5 font-sans text-[9px] uppercase tracking-[0.14em] text-emerald-200">
                          Complete
                        </span>
                      </div>
                    ) : null}
                  </button>

                  {/* Expanded gate content */}
                  {isOpen ? (
                    <div className="mt-8 space-y-6 rounded-3xl border border-amber-200/15 bg-gradient-to-b from-[#0b0b14]/80 to-[#0b0b14]/60 p-6 backdrop-blur-sm">
                      <div>
                        <p className="font-sans text-[10px] uppercase tracking-[0.18em] text-amber-200/50">
                          {node.sectionLabel}
                        </p>
                        <h3 className="mt-3 text-[1.75rem] leading-[1.2] tracking-[-0.01em] text-stone-100">{node.title}</h3>
                        <p className="soft mt-3 text-[15px] leading-relaxed">{node.orientation}</p>
                      </div>

                      <div className="border-t border-amber-200/10 pt-5">
                        <PathStepWell
                          trackId={node.trackId}
                          trackTitle={node.sectionLabel}
                          step={node.track.steps[node.stepIndex]}
                          items={items}
                        />
                      </div>

                      <div className="border-t border-amber-200/10 pt-5">
                        <StepIntegrationGate
                          stepId={node.stepId}
                          integration={node.track.steps[node.stepIndex].integration}
                          keyIdea={node.track.steps[node.stepIndex].keyIdea}
                          done={done}
                          onComplete={() => onComplete(node.trackId, node.stepId)}
                        />
                      </div>

                      <div className="flex justify-center border-t border-amber-200/8 pt-5">
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          onClick={() => onToggleGate(node.trackId, node.stepId, true)}
                          className="text-stone-500 hover:text-stone-300"
                        >
                          Close
                        </Button>
                      </div>
                    </div>
                  ) : null}

                  {/* Connecting path line to next node */}
                  {i < nodes.length - 1 ? (
                    <div className="absolute left-1/2 top-full flex h-8 w-px -translate-x-1/2 items-center justify-center">
                      <div
                        className={`h-full w-px bg-gradient-to-b transition-all duration-700 ${
                          i < currentIndex
                            ? "from-amber-200/30 via-amber-200/20 to-amber-200/30"
                            : "from-amber-200/10 via-amber-200/5 to-amber-200/10"
                        }`}
                        style={{
                          filter: i < currentIndex ? "blur(0.3px)" : "blur(0.5px)",
                        }}
                      />
                    </div>
                  ) : null}
                </div>
              </li>
            );
          })}
        </ul>

        {/* Footer encouragement */}
        {currentIndex >= 0 && currentIndex < nodes.length ? (
          <div className="mt-16 text-center">
            <p className="font-sans text-[11px] uppercase tracking-[0.18em] text-stone-500">
              {currentIndex === 0
                ? "Begin the journey"
                : currentIndex < nodes.length - 1
                  ? `${currentIndex} ${currentIndex === 1 ? 'gate' : 'gates'} walked · ${nodes.length - currentIndex} ${nodes.length - currentIndex === 1 ? 'remains' : 'remain'}`
                  : "The path is complete"}
            </p>
          </div>
        ) : null}

        {/* Optional: Secondary navigation */}
        <div className="mt-10 text-center">
          <p className="font-sans text-[10px] uppercase tracking-[0.16em] text-stone-600">
            Themes and lineage map coming soon
          </p>
        </div>
      </section>
    </div>
  );
}
