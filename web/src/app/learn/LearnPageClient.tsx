"use client";

import { useRouter } from "next/navigation";
import { useEffect, useMemo, useRef, useState } from "react";
import { getVerses } from "@/lib/api";
import { LearnTrail } from "@/components/learn/LearnTrail";
import { LearnTrailGate } from "@/components/learn/LearnTrailGate";
import { TraditionChooser } from "@/components/learn/TraditionChooser";
import { TraditionSwitcher } from "@/components/learn/TraditionSwitcher";
import { useLearnProgress } from "@/hooks/useLearnProgress";
import { stepKey } from "@/lib/learn/progress";
import {
  buildTrail,
  TRAIL_ARRIVE_SESSION_KEY,
  TRAIL_ARRIVE_TOTAL_MS,
  TRAIL_GATE_LEAVE_MS,
} from "@/lib/learn/trail";
import {
  ESSENTIAL_TRAIL_ID,
  findTraditionTrail,
  isWalkableTrail,
  pathIdForTrack,
} from "@/lib/learn/traditionTrails";
import { learnHref, parseLearnSearch, type LearnHrefOpts } from "@/lib/learn/url";
import { LEARNING_TRACKS } from "@/lib/learningPaths";
import { gateForThreadSearch } from "@/lib/learningThreads";
import { GateCircleSection } from "@/components/GateCircleSection";
import { CONVEX_ENABLED } from "@/lib/convexConfigured";
import type { VerseItem } from "@/lib/types";

export default function LearnPageClient() {
  const router = useRouter();
  const { progress, completedAt, hydrated, toggle } = useLearnProgress();
  const [items, setItems] = useState<VerseItem[]>([]);
  const [openStepId, setOpenStepId] = useState<string | null>(null);
  const [openStepTrackId, setOpenStepTrackId] = useState<string | null>(null);
  const [drawingKey, setDrawingKey] = useState<string | null>(null);
  const [finishingKey, setFinishingKey] = useState<string | null>(null);
  const [gateLeaving, setGateLeaving] = useState(false);
  const [pendingFinishKey, setPendingFinishKey] = useState<string | null>(null);
  const [scrollToKey, setScrollToKey] = useState<string | null>(null);
  const [selectedPathId, setSelectedPathId] = useState<string | null>(ESSENTIAL_TRAIL_ID);
  const [circleInvite, setCircleInvite] = useState<{
    verseId: string;
    verseTitle: string;
    idea?: string;
  } | null>(null);
  const advanceTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const leaveTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const urlReadyRef = useRef(false);
  const completingRef = useRef(false);
  const progressRef = useRef(progress);
  progressRef.current = progress;
  const selectedPathIdRef = useRef(selectedPathId);
  selectedPathIdRef.current = selectedPathId;
  const selectedTrail = selectedPathId ? findTraditionTrail(selectedPathId) : null;

  useEffect(() => {
    getVerses("all").then(setItems).catch(() => setItems([]));
  }, []);

  useEffect(() => {
    return () => {
      if (advanceTimerRef.current) clearTimeout(advanceTimerRef.current);
      if (leaveTimerRef.current) clearTimeout(leaveTimerRef.current);
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
    let pendingArrive = false;
    try {
      pendingArrive = Boolean(sessionStorage.getItem(TRAIL_ARRIVE_SESSION_KEY));
    } catch {
      pendingArrive = false;
    }
    if (knownTrack && trackId && stepId && !pendingArrive) {
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
    setCircleInvite(null);
    setSelectedPathId(null);
    selectedPathIdRef.current = null;
    syncUrl({ pathId: null });
  }

  function selectPath(pathId: string) {
    const trail = findTraditionTrail(pathId);
    setOpenStepId(null);
    setOpenStepTrackId(null);
    setGateLeaving(false);
    setDrawingKey(null);
    setFinishingKey(null);
    setCircleInvite(null);
    setSelectedPathId(trail.id);
    selectedPathIdRef.current = trail.id;
    const nodes = buildTrail(trail.id);
    const idx = nodes.findIndex((node) => !progress[node.key]);
    const current = nodes[idx === -1 ? Math.max(0, nodes.length - 1) : idx];
    setScrollToKey(current?.key ?? null);
    syncUrl({ pathId: trail.id });
  }

  function openTrailGate(trackId: string, stepId: string) {
    setGateLeaving(false);
    setCircleInvite(null);
    setOpenStepTrackId(trackId);
    setOpenStepId(stepId);
    syncUrl({ trackId, stepId });
  }

  function clearArriveSession() {
    try {
      sessionStorage.removeItem(TRAIL_ARRIVE_SESSION_KEY);
    } catch {
      /* ignore */
    }
  }

  function persistArriveSession(nextKey: string | null, finishKey: string) {
    try {
      sessionStorage.setItem(
        TRAIL_ARRIVE_SESSION_KEY,
        JSON.stringify({ nextKey, finishKey, at: Date.now() }),
      );
    } catch {
      /* ignore */
    }
  }

  function beginArrive(nextKey: string | null, finishKey: string) {
    persistArriveSession(nextKey, finishKey);
    setPendingFinishKey(finishKey);
    setFinishingKey(finishKey);
    setDrawingKey(nextKey);
    setScrollToKey(nextKey || finishKey);
    if (advanceTimerRef.current) clearTimeout(advanceTimerRef.current);
    advanceTimerRef.current = setTimeout(() => {
      setDrawingKey(null);
      setFinishingKey(null);
      setPendingFinishKey(null);
      clearArriveSession();
      advanceTimerRef.current = null;
      if (urlReadyRef.current) syncUrl({});
    }, TRAIL_ARRIVE_TOTAL_MS);
  }

  useEffect(() => {
    if (typeof window === "undefined") return;
    try {
      const raw = sessionStorage.getItem(TRAIL_ARRIVE_SESSION_KEY);
      if (!raw) return;
      const saved = JSON.parse(raw) as { nextKey?: string | null; finishKey?: string; at?: number };
      if (!saved?.finishKey || typeof saved.at !== "number" || Date.now() - saved.at > 8000) {
        sessionStorage.removeItem(TRAIL_ARRIVE_SESSION_KEY);
        return;
      }
      setOpenStepId(null);
      setOpenStepTrackId(null);
      beginArrive(saved.nextKey ?? null, saved.finishKey);
    } catch {
      /* ignore */
    }
    // Replay sand+glyph if a URL rewrite remounted the page mid-arrive.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function closeTrailGate() {
    if (gateLeaving || completingRef.current) return;
    setOpenStepId(null);
    setOpenStepTrackId(null);
    setGateLeaving(false);
    syncUrl({});
  }

  function onPathGateComplete(trackId: string, stepId: string) {
    if (!trackId || !stepId || gateLeaving || completingRef.current) return;
    completingRef.current = true;
    const key = stepKey(trackId, stepId);
    if (!progressRef.current[key]) toggle(trackId, stepId);
    setPendingFinishKey(key);
    const nodes = buildTrail(selectedPathIdRef.current);
    const idx = nodes.findIndex((node) => node.key === key);
    const nextKey = idx >= 0 ? nodes[idx + 1]?.key ?? null : null;
    const finished = LEARNING_TRACKS.find((item) => item.id === trackId)?.steps.find((item) => item.id === stepId);
    if (CONVEX_ENABLED && finished?.passageId) {
      setCircleInvite({
        verseId: finished.passageId,
        verseTitle: finished.title,
        idea: finished.keyIdea,
      });
    }
    setGateLeaving(true);
    beginArrive(nextKey, key);
    if (leaveTimerRef.current) clearTimeout(leaveTimerRef.current);
    leaveTimerRef.current = setTimeout(() => {
      setOpenStepId(null);
      setOpenStepTrackId(null);
      setGateLeaving(false);
      completingRef.current = false;
      leaveTimerRef.current = null;
    }, TRAIL_GATE_LEAVE_MS);
  }

  const gateOpen = Boolean(openStepId && openStepTrackId);
  const trailProgress = useMemo(
    () => (pendingFinishKey ? { ...progress, [pendingFinishKey]: true } : progress),
    [progress, pendingFinishKey],
  );
  const trailCompletedAt = useMemo(() => {
    if (!pendingFinishKey || completedAt[pendingFinishKey]) return completedAt;
    return { ...completedAt, [pendingFinishKey]: new Date().toISOString() };
  }, [completedAt, pendingFinishKey]);

  return (
    <main className="page-shell page-shell--paths">
      <TraditionSwitcher pathId={selectedPathId} onSelectPath={selectPath} />
      <div className="section-stack">
        {!selectedPathId ? (
          <TraditionChooser
            progress={progress}
            hydrated={hydrated}
            onSelectTradition={selectPath}
          />
        ) : null}

        {selectedPathId ? (
          <LearnTrail
            pathId={selectedPathId}
            progress={trailProgress}
            completedAt={trailCompletedAt}
            hydrated={hydrated}
            onOpenGate={openTrailGate}
            onBackPaths={goHome}
            scrollToKey={scrollToKey}
            drawingKey={drawingKey}
            finishingKey={finishingKey}
            gateOpen={gateOpen}
            notice={
              circleInvite && !gateOpen ? (
                <GateCircleSection
                  verseId={circleInvite.verseId}
                  verseTitle={circleInvite.verseTitle}
                  idea={circleInvite.idea}
                  defaultOpen
                  onDismiss={() => setCircleInvite(null)}
                />
              ) : null
            }
          />
        ) : null}

        {gateOpen && openStepTrackId && openStepId
          ? (() => {
              const gateTrack = LEARNING_TRACKS.find((t) => t.id === openStepTrackId);
              const gateStep = gateTrack?.steps.find((s) => s.id === openStepId);
              if (!gateTrack || !gateStep) return null;
              const gateKey = stepKey(openStepTrackId, openStepId);
              return (
                <LearnTrailGate
                  track={gateTrack}
                  step={gateStep}
                  items={items}
                  done={Boolean(progress[gateKey]) && pendingFinishKey !== gateKey}
                  leaving={gateLeaving}
                  pathTitle={selectedTrail?.shortTitle ?? "The Path"}
                  pathId={selectedTrail?.id ?? "essential"}
                  onComplete={() => onPathGateComplete(openStepTrackId, openStepId)}
                  onBack={closeTrailGate}
                />
              );
            })()
          : null}
      </div>
    </main>
  );
}
