"use client";

import { useRouter } from "next/navigation";
import { useEffect, useMemo, useRef, useState } from "react";
import { getVerses } from "@/lib/api";
import { LearnThemesHome } from "@/components/learn/LearnThemesHome";
import { LearnThreadJourney } from "@/components/learn/LearnThreadJourney";
import { LearnTrail } from "@/components/learn/LearnTrail";
import { LearnTrailGate } from "@/components/learn/LearnTrailGate";
import { TraditionChooser } from "@/components/learn/TraditionChooser";
import { PathStepWell } from "@/components/learn/PathStepWell";
import { PathTree } from "@/components/learn/PathTree";
import { StepIntegrationGate } from "@/components/learn/StepIntegrationGate";
import { ThreadCompleteCard } from "@/components/learn/ThreadCompleteCard";
import { ThreadContextBar } from "@/components/learn/ThreadContextBar";
import { Section } from "@/components/ui/Section";
import { useLearnProgress } from "@/hooks/useLearnProgress";
import { pickDailySit, stepKey, threadKey, trackDoneCount, type DailySitPick } from "@/lib/learn/progress";
import { buildTrail, TRAIL_ARRIVE_TOTAL_MS } from "@/lib/learn/trail";
import {
  ESSENTIAL_TRAIL_ID,
  findTraditionTrail,
  isWalkableTrail,
} from "@/lib/learn/traditionTrails";
import { learnHref, parseLearnSearch, type LearnHrefOpts } from "@/lib/learn/url";
import {
  LEARNING_REALMS,
  LEARNING_TRACKS,
  RECOMMENDED_SPINE,
  type LearningTrack,
} from "@/lib/learningPaths";
import { beadIndex, findBead, findThread, threadsForPathStep } from "@/lib/learningThreads";
import type { VerseItem } from "@/lib/types";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

type PageView = "home" | "gate" | "journey" | "bead" | "lineage";

export default function LearnPage() {
  const router = useRouter();
  const {
    progress,
    completedAt,
    hydrated,
    toggle,
    toggleThread,
    resetTrack,
    exportProgress,
    importProgressFromFile,
    openImportPicker,
    fileInputRef,
  } = useLearnProgress();
  const [importStatus, setImportStatus] = useState<string | null>(null);
  const [items, setItems] = useState<VerseItem[]>([]);
  const [selectedTrackId, setSelectedTrackId] = useState<string | null>(null);
  const [openStepId, setOpenStepId] = useState<string | null>(null);
  const [openStepTrackId, setOpenStepTrackId] = useState<string | null>(null);
  const [activeThreadId, setActiveThreadId] = useState<string | null>(null);
  const [activeBeadId, setActiveBeadId] = useState<string | null>(null);
  const [threadCeremonyId, setThreadCeremonyId] = useState<string | null>(null);
  const [resetOpen, setResetOpen] = useState(false);
  const [skipConfirmIdx, setSkipConfirmIdx] = useState<number | null>(null);
  const [drawingKey, setDrawingKey] = useState<string | null>(null);
  const [selectedPathId, setSelectedPathId] = useState<string | null>(ESSENTIAL_TRAIL_ID);
  const advanceTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const stepRefs = useRef<Record<string, HTMLElement | null>>({});
  const pathSectionRef = useRef<HTMLElement | null>(null);
  const pendingScrollRef = useRef<string | null>(null);
  const urlReadyRef = useRef(false);
  const selectedPathIdRef = useRef(selectedPathId);
  selectedPathIdRef.current = selectedPathId;
  const selectedTrail = selectedPathId ? findTraditionTrail(selectedPathId) : null;

  useEffect(() => {
    getVerses("all").then(setItems).catch(() => setItems([]));
  }, []);

  const track = useMemo(
    () => LEARNING_TRACKS.find((t) => t.id === selectedTrackId) || LEARNING_TRACKS[0],
    [selectedTrackId],
  );
  const completed = track.steps.filter((s) => progress[stepKey(track.id, s.id)]).length;
  const pct = Math.round((completed / Math.max(1, track.steps.length)) * 100);
  const nextIndex = track.steps.findIndex((s) => !progress[stepKey(track.id, s.id)]);
  const activeIndex = nextIndex === -1 ? track.steps.length - 1 : nextIndex;

  const trackById = useMemo(() => {
    const m: Record<string, LearningTrack> = {};
    for (const t of LEARNING_TRACKS) m[t.id] = t;
    return m;
  }, []);

  const anyProgress = useMemo(() => Object.values(progress).some(Boolean), [progress]);

  const recommendedNextId = useMemo(() => {
    for (const id of RECOMMENDED_SPINE) {
      const t = trackById[id];
      if (t && trackDoneCount(t, progress) < t.steps.length) return id;
    }
    return RECOMMENDED_SPINE[RECOMMENDED_SPINE.length - 1];
  }, [progress, trackById]);

  const dailySit = useMemo(() => pickDailySit(progress, completedAt), [progress, completedAt]);

  const activeThread = activeThreadId ? findThread(activeThreadId) : undefined;
  const activeBead =
    activeThread && activeBeadId ? findBead(activeThread, activeBeadId) : undefined;
  const prevBead =
    activeThread && activeBeadId
      ? (() => {
          const idx = beadIndex(activeThread, activeBeadId);
          return idx > 0 ? activeThread.steps[idx - 1] : null;
        })()
      : null;

  const view: PageView = useMemo(() => {
    if (threadCeremonyId) return "bead";
    if (activeThreadId && activeBeadId) return "bead";
    if (activeThreadId) return "journey";
    if (openStepId && openStepTrackId) return "gate";
    if (selectedTrackId) return "lineage";
    return "home";
  }, [threadCeremonyId, activeThreadId, activeBeadId, openStepId, openStepTrackId, selectedTrackId]);

  const beadPathStep = useMemo(() => {
    if (!activeBead) return null;
    const t = LEARNING_TRACKS.find((x) => x.id === activeBead.trackId);
    return t?.steps.find((s) => s.id === activeBead.stepId) ?? null;
  }, [activeBead]);

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
    const { pathId, trackId, stepId, threadId, beadId } = parseLearnSearch(window.location.search);
    const walkable = pathId && isWalkableTrail(pathId) ? pathId : ESSENTIAL_TRAIL_ID;
    if (threadId && findThread(threadId)) {
      setSelectedPathId(null);
      setActiveThreadId(threadId);
      const bead = beadId && findBead(findThread(threadId)!, beadId);
      if (bead) setActiveBeadId(bead.id);
      else setActiveBeadId(null);
    } else if (trackId && stepId && LEARNING_TRACKS.some((x) => x.id === trackId)) {
      setSelectedPathId(walkable);
      setOpenStepTrackId(trackId);
      setOpenStepId(stepId);
    } else if (trackId && LEARNING_TRACKS.some((x) => x.id === trackId)) {
      setSelectedPathId(walkable);
      setSelectedTrackId(trackId);
    } else if (pathId === null && !trackId && !stepId) {
      setSelectedPathId(ESSENTIAL_TRAIL_ID);
    } else {
      setSelectedPathId(walkable);
    }
    urlReadyRef.current = true;
  }, []);

  useEffect(() => {
    const target = pendingScrollRef.current;
    if (!target) return;
    const el = stepRefs.current[target];
    if (el) {
      requestAnimationFrame(() => el.scrollIntoView({ behavior: "auto", block: "start" }));
      pendingScrollRef.current = null;
    }
  });

  function clearThreadMode() {
    setActiveThreadId(null);
    setActiveBeadId(null);
    setThreadCeremonyId(null);
    if (advanceTimerRef.current) {
      clearTimeout(advanceTimerRef.current);
      advanceTimerRef.current = null;
    }
  }

  function goHome() {
    clearThreadMode();
    setSelectedTrackId(null);
    setOpenStepId(null);
    setOpenStepTrackId(null);
    setSelectedPathId(null);
    selectedPathIdRef.current = null;
    syncUrl({ pathId: null });
  }

  function selectPath(pathId: string) {
    const trail = findTraditionTrail(pathId);
    clearThreadMode();
    setSelectedTrackId(null);
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

  function openLineageMap() {
    clearThreadMode();
    setSelectedTrackId(RECOMMENDED_SPINE[0]);
    setOpenStepId(null);
    syncUrl({ trackId: RECOMMENDED_SPINE[0] });
  }

  function selectTrack(trackId: string) {
    clearThreadMode();
    setSelectedTrackId(trackId);
    setOpenStepId(null);
    syncUrl({ trackId });
    requestAnimationFrame(() => {
      pathSectionRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  function continueTo(trackId: string, stepId: string) {
    clearThreadMode();
    setSelectedTrackId(null);
    setOpenStepTrackId(trackId);
    setOpenStepId(stepId);
    syncUrl({ trackId, stepId });
  }

  function openBead(threadId: string, beadId: string) {
    const thread = findThread(threadId);
    const bead = thread && findBead(thread, beadId);
    if (!thread || !bead) return;
    if (advanceTimerRef.current) {
      clearTimeout(advanceTimerRef.current);
      advanceTimerRef.current = null;
    }
    setThreadCeremonyId(null);
    setSelectedTrackId(null);
    setOpenStepId(null);
    setActiveThreadId(threadId);
    setActiveBeadId(beadId);
    syncUrl({ threadId, beadId });
  }

  function openThread(threadId: string) {
    if (!findThread(threadId)) return;
    setThreadCeremonyId(null);
    setSelectedTrackId(null);
    setOpenStepId(null);
    setActiveThreadId(threadId);
    setActiveBeadId(null);
    syncUrl({ threadId });
  }

  function startThread(threadId: string) {
    const thread = findThread(threadId);
    const first = thread?.steps[0];
    if (!first) return;
    openBead(threadId, first.id);
  }

  function leaveThread() {
    goHome();
  }

  function descendPathFromThread() {
    if (!activeBead) {
      goHome();
      return;
    }
    const trackId = activeBead.trackId;
    const stepId = activeBead.stepId;
    setActiveThreadId(null);
    setActiveBeadId(null);
    setThreadCeremonyId(null);
    openTrailGate(trackId, stepId);
  }

  function backToThreadMap() {
    if (activeThreadId) {
      openThread(activeThreadId);
      return;
    }
    goHome();
  }

  function beginSit(sit: DailySitPick) {
    if (sit.mode === "thread") {
      openBead(sit.threadId, sit.beadId);
      return;
    }
    continueTo(sit.track.id, sit.step.id);
  }

  function goToStepIndex(targetIdx: number, opts?: { force?: boolean }) {
    const s = track.steps[targetIdx];
    if (!s) return;
    const currentOpen = openStepId ? track.steps.findIndex((x) => x.id === openStepId) : activeIndex;
    const leavingIncomplete =
      currentOpen >= 0 &&
      currentOpen < targetIdx &&
      !progress[stepKey(track.id, track.steps[currentOpen].id)];
    if (leavingIncomplete && !opts?.force) {
      setSkipConfirmIdx(targetIdx);
      return;
    }
    setOpenStepId(s.id);
    pendingScrollRef.current = s.id;
    syncUrl({ trackId: track.id, stepId: s.id });
  }

  function openTrailGate(trackId: string, stepId: string) {
    clearThreadMode();
    setSelectedTrackId(null);
    setOpenStepTrackId(trackId);
    setOpenStepId(stepId);
    syncUrl({ trackId, stepId });
    window.scrollTo({ top: 0, behavior: "auto" });
  }

  function closeTrailGate() {
    setOpenStepId(null);
    setOpenStepTrackId(null);
    syncUrl({});
  }

  function onPathGateComplete(trackId: string, stepId: string) {
    const key = stepKey(trackId, stepId);
    if (!progress[key]) toggle(trackId, stepId);
    const nodes = buildTrail(selectedPathIdRef.current);
    const idx = nodes.findIndex((node) => node.trackId === trackId && node.stepId === stepId);
    const next = idx >= 0 ? nodes[idx + 1] : undefined;
    setOpenStepId(null);
    setOpenStepTrackId(null);
    syncUrl({});
    if (next) {
      setDrawingKey(next.key);
      pendingScrollRef.current = next.key;
      if (advanceTimerRef.current) clearTimeout(advanceTimerRef.current);
      advanceTimerRef.current = setTimeout(() => {
        setDrawingKey(null);
        advanceTimerRef.current = null;
      }, TRAIL_ARRIVE_TOTAL_MS);
    }
  }

  function onThemeBeadComplete() {
    if (!activeThreadId || !activeBeadId || !activeThread) return;
    const key = threadKey(activeThreadId, activeBeadId);
    if (!progress[key]) toggleThread(activeThreadId, activeBeadId);
    const idx = beadIndex(activeThread, activeBeadId);
    const next = idx >= 0 ? activeThread.steps[idx + 1] : undefined;
    if (next) {
      if (advanceTimerRef.current) clearTimeout(advanceTimerRef.current);
      advanceTimerRef.current = setTimeout(() => {
        openBead(activeThreadId, next.id);
        advanceTimerRef.current = null;
      }, 450);
      return;
    }
    setThreadCeremonyId(activeThreadId);
  }

  function openStep(stepId: string, isOpen: boolean) {
    if (isOpen) {
      setOpenStepId("__none__");
      syncUrl({ trackId: selectedTrackId, stepId: null });
      return;
    }
    setOpenStepId(stepId);
    syncUrl({ trackId: selectedTrackId, stepId });
    requestAnimationFrame(() => {
      stepRefs.current[stepId]?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  function openOrUnmark(trackId: string, stepId: string, done: boolean) {
    if (done) {
      toggle(trackId, stepId);
      return;
    }
    openStep(stepId, openStepId === stepId);
  }

  const beadDone = Boolean(
    activeThreadId && activeBeadId && progress[threadKey(activeThreadId, activeBeadId)],
  );
  const isLastBead =
    Boolean(activeThread && activeBeadId) &&
    beadIndex(activeThread!, activeBeadId!) >= activeThread!.steps.length - 1;

  return (
    <main className="page-shell page-shell--reading">
      <div className="section-stack">
        {view === "home" && !selectedPathId ? (
          <TraditionChooser
            progress={progress}
            hydrated={hydrated}
            onSelectTradition={selectPath}
          />
        ) : null}

        {view === "home" && selectedPathId ? (
          <LearnTrail
            pathId={selectedPathId}
            progress={progress}
            hydrated={hydrated}
            onOpenGate={openTrailGate}
            onSelectPath={selectPath}
            onBackPaths={goHome}
            scrollToKey={pendingScrollRef.current}
            drawingKey={drawingKey}
          />
        ) : null}

        {view === "gate" && openStepTrackId && openStepId
          ? (() => {
              const gateTrack = LEARNING_TRACKS.find((t) => t.id === openStepTrackId);
              const gateStep = gateTrack?.steps.find((s) => s.id === openStepId);
              if (!gateTrack || !gateStep) return null;
              return (
                <LearnTrailGate
                  track={gateTrack}
                  step={gateStep}
                  items={items}
                  done={Boolean(progress[stepKey(openStepTrackId, openStepId)])}
                  pathTitle={selectedTrail?.shortTitle ?? "The Path"}
                  pathId={selectedTrail?.id ?? "essential"}
                  onComplete={() => onPathGateComplete(openStepTrackId, openStepId)}
                  onBack={closeTrailGate}
                />
              );
            })()
          : null}

        {view === "journey" && activeThread ? (
          <LearnThreadJourney
            thread={activeThread}
            progress={progress}
            onOpenBead={openBead}
            onBackHome={goHome}
          />
        ) : null}

        {view === "bead" ? (
          <section ref={pathSectionRef} className="learn-path scroll-mt-24">
            {activeThreadId && activeBeadId ? (
              <ThreadContextBar
                threadId={activeThreadId}
                beadId={activeBeadId}
                progress={progress}
                onOpenBead={openBead}
                onLeaveThread={leaveThread}
                onBackToThread={backToThreadMap}
              />
            ) : null}

            {threadCeremonyId ? (
              <ThreadCompleteCard
                threadId={threadCeremonyId}
                progress={progress}
                onBackToMap={goHome}
                onTraceAnother={startThread}
                onDescendPath={descendPathFromThread}
                onLeaveThread={leaveThread}
              />
            ) : activeThread && activeBead && beadPathStep ? (
              <article className="learn-gate border-t border-amber-200/35 py-5">
                <p className="passage-reading__meta">Bead well</p>
                <h2 className="library-header__title mt-2">{activeThread.title}</h2>
                <p className="library-header__lede">{activeThread.thesis}</p>
                <p className="mt-3 font-sans text-xs uppercase tracking-[0.18em] text-stone-400">
                  {activeBead.tradition} · {beadPathStep.title}
                </p>

                <div className="mt-6 max-w-[var(--reading-measure)] space-y-5 border-t border-[rgb(240_201_121_/_0.14)] pt-5">
                  <div>
                    <p className="passage-layer__label">The move</p>
                    <p className="mt-2 text-base leading-relaxed text-stone-100">{activeBead.move}</p>
                  </div>
                  <div>
                    <p className="passage-layer__label">Homology</p>
                    <p className="mt-2 leading-relaxed text-stone-200">{activeBead.homology}</p>
                  </div>
                  <div>
                    <p className="passage-layer__label">Divergence</p>
                    <p className="mt-2 leading-relaxed text-stone-200">{activeBead.divergence}</p>
                  </div>
                </div>

                <div className="mt-6">
                  <h3 className="text-2xl leading-tight text-stone-100">{beadPathStep.title}</h3>
                  <p className="soft mt-2 text-base leading-relaxed">{beadPathStep.orientation}</p>
                </div>

                <PathStepWell
                  trackId={activeBead.trackId}
                  trackTitle={trackById[activeBead.trackId]?.title || activeBead.trackId}
                  step={beadPathStep}
                  items={items}
                  threadId={activeThreadId}
                  beadId={activeBeadId}
                >
                  {prevBead ? (
                    <div className="max-w-[var(--reading-measure)] border-t border-[rgb(240_201_121_/_0.14)] pt-4">
                      <p className="font-sans text-xs uppercase tracking-[0.16em] text-amber-200/75">
                        Across the theme
                      </p>
                      <p className="mt-2 text-sm leading-relaxed text-stone-300">
                        Previous ({prevBead.tradition}): {prevBead.move}
                      </p>
                    </div>
                  ) : null}
                </PathStepWell>

                <StepIntegrationGate
                  stepId={`${activeThreadId}:${activeBeadId}`}
                  integration={activeThread.integration}
                  theme={{
                    move: activeBead.move,
                    previousTradition: prevBead?.tradition,
                  }}
                  done={beadDone}
                  completeLabel={isLastBead ? "Finish theme" : "Next bead →"}
                  onComplete={onThemeBeadComplete}
                />

                {beadDone ? (
                  <div className="mt-4 flex flex-wrap gap-2">
                    {!isLastBead ? (
                      <Button
                        type="button"
                        size="sm"
                        onClick={() => {
                          if (!activeBeadId) return;
                          const idx = beadIndex(activeThread, activeBeadId);
                          const next = activeThread.steps[idx + 1];
                          if (next) openBead(activeThread.id, next.id);
                        }}
                      >
                        Next bead →
                      </Button>
                    ) : (
                      <Button type="button" size="sm" onClick={() => setThreadCeremonyId(activeThread.id)}>
                        Finish theme
                      </Button>
                    )}
                  </div>
                ) : null}

                <div className="mt-6 flex flex-wrap gap-2 border-t border-[rgb(240_201_121_/_0.1)] pt-4">
                  <Button type="button" variant="secondary" size="sm" onClick={descendPathFromThread}>
                    Descend this lineage
                  </Button>
                </div>
              </article>
            ) : null}
          </section>
        ) : null}

        {view === "lineage" ? (
          <>
            <header className="library-header">
              <div className="library-header__body">
                <button
                  type="button"
                  onClick={goHome}
                  className="font-sans text-[10px] uppercase tracking-[0.16em] text-amber-200/55 hover:text-amber-100"
                >
                  ← Themes
                </button>
                <p className="passage-reading__meta mt-4">Lineage</p>
                <h1 className="library-header__title">Walk a path</h1>
                <p className="library-header__lede">
                  A lineage is the deep well under a bead — one tradition, gate by gate.
                  Themes remain the primary way in.
                </p>
              </div>
            </header>

            <Section
              eyebrow="The map"
              title="Your branching path"
              lead="Start at the root, branch into a realm, then zoom into a path and descend it gate by gate."
            >
              <PathTree
                realms={LEARNING_REALMS}
                trackById={trackById}
                progress={progress}
                hydrated={hydrated}
                selectedTrackId={selectedTrackId ?? RECOMMENDED_SPINE[0]}
                recommendedNextId={recommendedNextId}
                anyProgress={hydrated && anyProgress}
                onSelectTrack={selectTrack}
                onOpenGate={continueTo}
              />
            </Section>

            <section ref={pathSectionRef} className="learn-path scroll-mt-24">
              <div className="relative flex flex-wrap items-start justify-between gap-4">
                <div className="max-w-[var(--reading-measure)]">
                  <p className="passage-reading__meta">Current path</p>
                  <h2 className="library-header__title mt-2">{track.title}</h2>
                  <p className="library-header__lede">{track.outcome}</p>
                  <p className="mt-3 max-w-[var(--reading-measure)] leading-relaxed text-stone-300">{track.arc}</p>
                  <p className="mt-3 font-sans text-xs uppercase tracking-[0.18em] text-stone-400">
                    {track.level} · {track.estimatedSessions}
                  </p>
                </div>
                <div className="flex flex-wrap items-center gap-2">
                  <Button
                    type="button"
                    onClick={exportProgress}
                    disabled={!hydrated}
                    variant="secondary"
                    size="sm"
                    className="disabled:opacity-40"
                  >
                    Export progress
                  </Button>
                  <Button
                    type="button"
                    onClick={openImportPicker}
                    disabled={!hydrated}
                    variant="secondary"
                    size="sm"
                    className="disabled:opacity-40"
                  >
                    Import progress
                  </Button>
                  <Button
                    type="button"
                    disabled={!hydrated}
                    variant="secondary"
                    size="sm"
                    className="disabled:opacity-40"
                    onClick={() => setResetOpen(true)}
                  >
                    Reset path
                  </Button>
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="application/json,.json"
                    className="hidden"
                    onChange={async (e) => {
                      const file = e.target.files?.[0];
                      e.target.value = "";
                      if (!file) return;
                      try {
                        await importProgressFromFile(file);
                        setImportStatus("Progress imported.");
                      } catch {
                        setImportStatus("Could not import that file.");
                      }
                    }}
                  />
                </div>
              </div>
              {importStatus ? (
                <p className="relative mt-3 font-sans text-xs text-amber-200/80" role="status">
                  {importStatus}
                </p>
              ) : null}

              <div className={`relative mt-6 ${hydrated ? "" : "opacity-50"}`}>
                <div className="flex items-center justify-between font-sans text-xs uppercase tracking-[0.18em] text-stone-400">
                  <span>Progress</span>
                  <span>{hydrated ? `${completed}/${track.steps.length} complete` : "…"}</span>
                </div>
                <Progress
                  value={hydrated ? pct : 12}
                  className={cn(
                    "mt-2 w-full gap-0 [&_[data-slot=progress-track]]:h-3 [&_[data-slot=progress-track]]:bg-white/10 [&_[data-slot=progress-indicator]]:bg-amber-300",
                    !hydrated && "[&_[data-slot=progress-indicator]]:animate-pulse",
                  )}
                />
              </div>

              <div className="relative mt-8 space-y-5">
                <div className="absolute bottom-8 left-6 top-8 hidden w-px bg-gradient-to-b from-transparent via-amber-200/25 to-transparent sm:block" />
                {track.steps.map((s) => {
                  const idx = track.steps.findIndex((x) => x.id === s.id);
                  const done = !!progress[stepKey(track.id, s.id)];
                  const current = idx === activeIndex && !done;
                  const isOpen = openStepId === s.id || (openStepId === null && current);
                  const memberships = threadsForPathStep(track.id, s.id);
                  return (
                    <article
                      key={s.id}
                      ref={(el) => {
                        stepRefs.current[s.id] = el;
                      }}
                      className={`relative scroll-mt-24 sm:pl-16 ${current || isOpen ? "" : "opacity-90"}`}
                    >
                      <button
                        type="button"
                        onClick={() => openOrUnmark(track.id, s.id, done)}
                        className={`absolute left-0 top-1 hidden h-12 w-12 items-center justify-center rounded-full border-2 font-sans text-sm font-bold sm:flex ${
                          done
                            ? "border-emerald-300 bg-emerald-300 text-slate-950"
                            : current
                              ? "border-amber-200 bg-amber-200 text-slate-950 shadow-[0_0_0_8px_rgb(240_201_121_/_0.10)]"
                              : "border-amber-200/30 bg-[#0b0b14] text-amber-100"
                        }`}
                        aria-label={done ? `Mark step ${idx + 1} incomplete` : `Open step ${idx + 1}`}
                      >
                        {done ? "✓" : idx + 1}
                      </button>

                      <div
                        className={`learn-gate border-t py-5 ${
                          current ? "border-amber-200/35" : "border-[rgb(240_201_121_/_0.12)]"
                        }`}
                      >
                        <div className="flex flex-wrap items-center justify-between gap-3">
                          <p className="font-sans text-xs uppercase tracking-[0.2em] text-amber-200/80">
                            Step {idx + 1} {current ? "• next up" : done ? "• complete" : ""}
                          </p>
                          {done ? (
                            <Button
                              type="button"
                              variant="ghost"
                              size="sm"
                              onClick={() => toggle(track.id, s.id)}
                              className="rounded-full border border-emerald-300/50 text-emerald-200 hover:bg-emerald-300/10 hover:text-emerald-100"
                            >
                              Done · reopen
                            </Button>
                          ) : (
                            <Button
                              type="button"
                              variant="ghost"
                              size="sm"
                              onClick={() => openStep(s.id, isOpen)}
                              className="rounded-full border border-amber-200/30 text-amber-100 hover:bg-amber-200/10"
                            >
                              {isOpen ? "Collapse" : "Open step"}
                            </Button>
                          )}
                        </div>

                        <button
                          type="button"
                          onClick={() => openStep(s.id, isOpen)}
                          aria-expanded={isOpen}
                          className="mt-3 block w-full text-left"
                        >
                          <h3 className="text-2xl leading-tight text-stone-100">{s.title}</h3>
                          <p className="soft mt-2 text-base leading-relaxed">{s.orientation}</p>
                          {!isOpen ? (
                            <span className="mt-2 inline-block font-sans text-xs uppercase tracking-[0.16em] text-amber-200/70">
                              Open step ↓
                            </span>
                          ) : null}
                        </button>

                        {memberships.length > 0 ? (
                          <div className="mt-3 flex flex-wrap items-center gap-2">
                            <span className="font-sans text-[9px] uppercase tracking-[0.14em] text-stone-500">
                              Also a bead on
                            </span>
                            {memberships.map(({ thread, bead }) => (
                              <button
                                key={`${thread.id}:${bead.id}`}
                                type="button"
                                onClick={() => openBead(thread.id, bead.id)}
                                className="rounded-full border border-white/12 px-2.5 py-1 font-sans text-[10px] uppercase tracking-[0.12em] text-amber-200/70 transition hover:border-amber-200/35 hover:text-amber-100"
                              >
                                {thread.glyph} {thread.title}
                              </button>
                            ))}
                          </div>
                        ) : null}

                        {isOpen ? (
                          <div>
                            <PathStepWell
                              trackId={track.id}
                              trackTitle={track.title}
                              step={s}
                              items={items}
                            />
                            <StepIntegrationGate
                              stepId={s.id}
                              integration={s.integration}
                              keyIdea={s.keyIdea}
                              done={done}
                              onComplete={() => {
                                const key = stepKey(track.id, s.id);
                                if (!progress[key]) toggle(track.id, s.id);
                                const next = track.steps[idx + 1];
                                if (next) {
                                  setOpenStepId(next.id);
                                  pendingScrollRef.current = next.id;
                                  syncUrl({ trackId: track.id, stepId: next.id });
                                }
                              }}
                            />
                            <div className="flex items-center justify-between gap-3 border-t border-white/10 pt-4">
                              <Button
                                type="button"
                                variant="secondary"
                                size="sm"
                                disabled={idx <= 0}
                                className="disabled:opacity-40"
                                onClick={() => goToStepIndex(idx - 1)}
                              >
                                ← Previous
                              </Button>
                              <span className="font-sans text-[11px] uppercase tracking-[0.16em] text-stone-400">
                                Gate {idx + 1} / {track.steps.length}
                              </span>
                              {idx < track.steps.length - 1 ? (
                                <Button type="button" size="sm" onClick={() => goToStepIndex(idx + 1)}>
                                  {done ? "Next gate →" : "Skip gate →"}
                                </Button>
                              ) : (
                                <span className="font-sans text-[11px] uppercase tracking-[0.16em] text-amber-200/70">
                                  Path end
                                </span>
                              )}
                            </div>
                          </div>
                        ) : null}
                      </div>
                    </article>
                  );
                })}
              </div>
            </section>
          </>
        ) : null}
      </div>

      <Dialog open={resetOpen} onOpenChange={setResetOpen}>
        <DialogContent className="border border-amber-200/20 bg-[#171421] sm:max-w-md">
          <DialogHeader>
            <DialogTitle className="text-xl text-amber-100">Reset path progress?</DialogTitle>
            <DialogDescription className="soft text-base leading-relaxed">
              Clear all gates on “{track.title}”. Theme beads stay. This cannot be undone.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter className="border-amber-200/10 bg-transparent">
            <Button type="button" variant="secondary" onClick={() => setResetOpen(false)}>
              Cancel
            </Button>
            <Button
              type="button"
              onClick={() => {
                resetTrack(track.id, track);
                setResetOpen(false);
              }}
            >
              Reset path
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Dialog open={skipConfirmIdx != null} onOpenChange={(open) => !open && setSkipConfirmIdx(null)}>
        <DialogContent className="border border-amber-200/20 bg-[#171421] sm:max-w-md">
          <DialogHeader>
            <DialogTitle className="text-xl text-amber-100">Skip this gate?</DialogTitle>
            <DialogDescription className="soft text-base leading-relaxed">
              Gates ripen through practice and recall. You can skip for now, but returning later will deepen the path.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter className="border-amber-200/10 bg-transparent">
            <Button type="button" variant="secondary" onClick={() => setSkipConfirmIdx(null)}>
              Stay here
            </Button>
            <Button
              type="button"
              onClick={() => {
                const target = skipConfirmIdx;
                setSkipConfirmIdx(null);
                if (target != null) goToStepIndex(target, { force: true });
              }}
            >
              Skip anyway
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </main>
  );
}
