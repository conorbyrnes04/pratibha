"use client";

import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { getVerses } from "@/lib/api";
import { LearnTrail } from "@/components/learn/LearnTrail";
import { LearnTrailGate } from "@/components/learn/LearnTrailGate";
import { TraditionChooser } from "@/components/learn/TraditionChooser";
import { useLearnProgress } from "@/hooks/useLearnProgress";
import { stepKey } from "@/lib/learn/progress";
import { buildTrail, currentTrailSit, TRAIL_ARRIVE_TOTAL_MS } from "@/lib/learn/trail";
import {
  ESSENTIAL_TRAIL_ID,
  findTraditionTrail,
  isWalkableTrail,
  pathIdForTrack,
} from "@/lib/learn/traditionTrails";
import { learnHref, parseLearnSearch, type LearnHrefOpts } from "@/lib/learn/url";
import { LEARNING_TRACKS } from "@/lib/learningPaths";
import { gateForThreadSearch } from "@/lib/learningThreads";
import type { VerseItem } from "@/lib/types";

export default function LearnPage() {
  const router = useRouter();
  const { progress, completedAt, hydrated, toggle } = useLearnProgress();
  const [items, setItems] = useState<VerseItem[]>([]);
  const [openStepId, setOpenStepId] = useState<string | null>(null);
  const [openStepTrackId, setOpenStepTrackId] = useState<string | null>(null);
  const [drawingKey, setDrawingKey] = useState<string | null>(null);
  const [selectedPathId, setSelectedPathId] = useState<string | null>(ESSENTIAL_TRAIL_ID);
  const advanceTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const pendingScrollRef = useRef<string | null>(null);
  const urlReadyRef = useRef(false);
  const selectedPathIdRef = useRef(selectedPathId);
  selectedPathIdRef.current = selectedPathId;
  const selectedTrail = selectedPathId ? findTraditionTrail(selectedPathId) : null;

  useEffect(() => {
    getVerses("all").then(setItems).catch(() => setItems([]));
  }, []);

  useEffect(() => {
    return () => {
      if (advanceTimerRef.current) clearTimeout(advanceTimerRef.current);
    };
  }, []);

  function syncUrl(opts: LearnHrefOpts = {}) {
    if (!urlReadyRef.current) return;
    const pathId = opts.pathId !== undefined ? opts.pathId : selectedPathIdRef.current;
    router.replace(
      learnHref({
        ...opts,
        pathId: pathId || null,
      }),
      { scroll: false },
    );
  }

  useEffect(() => {
    if (typeof window === "undefined") return;
    const parsed = parseLearnSearch(window.location.search);
    const fromTheme = gateForThreadSearch(parsed.threadId, parsed.beadId);
    const trackId = fromTheme?.trackId ?? parsed.trackId;
    const stepId = fromTheme?.stepId ?? parsed.stepId;
    const knownTrack = Boolean(trackId && LEARNING_TRACKS.some((x) => x.id === trackId));
    const walkable =
      parsed.pathId && isWalkableTrail(parsed.pathId)
        ? parsed.pathId
        : knownTrack && trackId
          ? pathIdForTrack(trackId)
          : ESSENTIAL_TRAIL_ID;

    setSelectedPathId(walkable);
    selectedPathIdRef.current = walkable;
    if (knownTrack && trackId && stepId) {
      setOpenStepTrackId(trackId);
      setOpenStepId(stepId);
    }

    urlReadyRef.current = true;
    const rewriteLegacy = Boolean(parsed.threadId || (parsed.trackId && !parsed.pathId));
    if (rewriteLegacy) {
      router.replace(
        learnHref({
          pathId: walkable,
          trackId: knownTrack && trackId && stepId ? trackId : null,
          stepId: knownTrack && trackId && stepId ? stepId : null,
        }),
        { scroll: false },
      );
    }
  }, [router]);

  function goHome() {
    setOpenStepId(null);
    setOpenStepTrackId(null);
    setSelectedPathId(null);
    selectedPathIdRef.current = null;
    syncUrl({ pathId: null });
  }

  function selectPath(pathId: string) {
    const trail = findTraditionTrail(pathId);
    setOpenStepId(null);
    setOpenStepTrackId(null);
    setDrawingKey(null);
    setSelectedPathId(trail.id);
    selectedPathIdRef.current = trail.id;
    const nodes = buildTrail(trail.id);
    const idx = nodes.findIndex((node) => !progress[node.key]);
    const current = nodes[idx === -1 ? Math.max(0, nodes.length - 1) : idx];
    pendingScrollRef.current = current?.key ?? null;
    syncUrl({ pathId: trail.id });
  }

  function openTrailGate(trackId: string, stepId: string) {
    setOpenStepTrackId(trackId);
    setOpenStepId(stepId);
    syncUrl({ trackId, stepId });
    window.scrollTo({ top: 0, behavior: "auto" });
  }

  function closeTrailGate() {
    const trackId = openStepTrackId;
    const stepId = openStepId;
    setOpenStepId(null);
    setOpenStepTrackId(null);
    syncUrl({});
    if (!trackId || !stepId) return;
    const nodes = buildTrail(selectedPathIdRef.current);
    const idx = nodes.findIndex((node) => node.trackId === trackId && node.stepId === stepId);
    const next = idx >= 0 ? nodes[idx + 1] : undefined;
    if (next && progress[stepKey(trackId, stepId)]) {
      setDrawingKey(next.key);
      pendingScrollRef.current = next.key;
      if (advanceTimerRef.current) clearTimeout(advanceTimerRef.current);
      advanceTimerRef.current = setTimeout(() => {
        setDrawingKey(null);
        advanceTimerRef.current = null;
      }, TRAIL_ARRIVE_TOTAL_MS);
    }
  }

  function onPathGateComplete(trackId: string, stepId: string) {
    const key = stepKey(trackId, stepId);
    if (!progress[key]) toggle(trackId, stepId);
  }

  const gateOpen = Boolean(openStepId && openStepTrackId);

  return (
    <main className="page-shell page-shell--reading">
      <div className="section-stack">
        {!gateOpen && !selectedPathId ? (
          <TraditionChooser
            progress={progress}
            hydrated={hydrated}
            onSelectTradition={selectPath}
          />
        ) : null}

        {!gateOpen && selectedPathId ? (
          <LearnTrail
            pathId={selectedPathId}
            progress={progress}
            completedAt={completedAt}
            hydrated={hydrated}
            onOpenGate={openTrailGate}
            onSelectPath={selectPath}
            onBackPaths={goHome}
            scrollToKey={pendingScrollRef.current}
            drawingKey={drawingKey}
          />
        ) : null}

        {gateOpen && openStepTrackId && openStepId
          ? (() => {
              const gateTrack = LEARNING_TRACKS.find((t) => t.id === openStepTrackId);
              const gateStep = gateTrack?.steps.find((s) => s.id === openStepId);
              if (!gateTrack || !gateStep) return null;
              const trailNodes = buildTrail(selectedPathId);
              const gateIdx = trailNodes.findIndex(
                (node) => node.trackId === openStepTrackId && node.stepId === openStepId,
              );
              const nextNode = gateIdx >= 0 ? trailNodes[gateIdx + 1] : undefined;
              const gateKey = stepKey(openStepTrackId, openStepId);
              const sit = currentTrailSit(progress, selectedPathId, completedAt);
              return (
                <LearnTrailGate
                  track={gateTrack}
                  step={gateStep}
                  items={items}
                  done={Boolean(progress[gateKey])}
                  walkedToday={Boolean(sit?.rested && sit.node.key === gateKey)}
                  pathTitle={selectedTrail?.shortTitle ?? "The Path"}
                  pathId={selectedTrail?.id ?? "essential"}
                  nextTitle={nextNode?.title ?? null}
                  onComplete={() => onPathGateComplete(openStepTrackId, openStepId)}
                  onBack={closeTrailGate}
                  onContinue={
                    nextNode
                      ? () => openTrailGate(nextNode.trackId, nextNode.stepId)
                      : undefined
                  }
                />
              );
            })()
          : null}
      </div>
    </main>
  );
}
