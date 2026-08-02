'use client';

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useRef, useState } from "react";
import { getVerses } from "@/lib/api";
import { DailySitCard } from "@/components/learn/DailySitCard";
import { PathTree } from "@/components/learn/PathTree";
import { StepIntegrationGate } from "@/components/learn/StepIntegrationGate";
import { ThreadCompleteCard } from "@/components/learn/ThreadCompleteCard";
import { ThreadContextBar } from "@/components/learn/ThreadContextBar";
import { ThreadsConstellation } from "@/components/learn/ThreadsConstellation";
import { JournalPanel } from "@/components/JournalPanel";
import { Section } from "@/components/ui/Section";
import { useLearnProgress } from "@/hooks/useLearnProgress";
import { matchStepItem, resolveById } from "@/lib/learn/passages";
import { stepKey, trackDoneCount } from "@/lib/learn/progress";
import { learnHref, parseLearnSearch } from "@/lib/learn/url";
import {
  LEARNING_REALMS,
  LEARNING_TRACKS,
  RECOMMENDED_SPINE,
  type LearningTrack,
} from "@/lib/learningPaths";
import {
  beadIndex,
  findBead,
  findThread,
  threadsForPathStep,
} from "@/lib/learningThreads";
import { learnStepContextId } from "@/lib/journalStorage";
import type { VerseItem } from "@/lib/types";
import { passagePreview } from "@/lib/verseLayers";
import { displayCollectionName } from "@/lib/collectionLabels";
import { displayPassageLocation, displayPassageTitle } from "@/lib/passageTitles";
import { cn } from "@/lib/utils";
import { Button, buttonVariants } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

function actionLabel(chatMode?: string): string {
  if (chatMode === "practice") return "Practice with it";
  if (chatMode === "compare") return "Compare traditions";
  if (chatMode === "explain") return "Understand it";
  return "Ask about it";
}

function PassageLink({ item, primary = false, backHref }: { item: VerseItem; primary?: boolean; backHref?: string }) {
  const href = backHref
    ? `/read/${encodeURIComponent(item._id)}?back=${encodeURIComponent(backHref)}`
    : `/read/${encodeURIComponent(item._id)}`;
  return (
    <Link href={href} className={`library-passage ${primary ? "" : "opacity-90"}`}>
      <p className="library-passage__meta">
        {displayCollectionName(item.collection)}
        {displayPassageLocation(item) ? ` · ${displayPassageLocation(item)}` : ""}
      </p>
      <h5 className="library-passage__title">{displayPassageTitle(item)}</h5>
      {primary ? <p className="library-passage__preview line-clamp-2">{passagePreview(item)}</p> : null}
    </Link>
  );
}

export default function LearnPage() {
  const router = useRouter();
  const {
    progress,
    hydrated,
    toggle,
    resetTrack,
    exportProgress,
    importProgressFromFile,
    openImportPicker,
    fileInputRef,
  } = useLearnProgress();
  const [importStatus, setImportStatus] = useState<string | null>(null);
  const [items, setItems] = useState<VerseItem[]>([]);
  const [selectedTrackId, setSelectedTrackId] = useState(RECOMMENDED_SPINE[0]);
  const [openStepId, setOpenStepId] = useState<string | null>(null);
  const [activeThreadId, setActiveThreadId] = useState<string | null>(null);
  const [activeBeadId, setActiveBeadId] = useState<string | null>(null);
  const [threadCeremonyId, setThreadCeremonyId] = useState<string | null>(null);
  const [resetOpen, setResetOpen] = useState(false);
  const advanceTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const stepRefs = useRef<Record<string, HTMLElement | null>>({});
  const pathSectionRef = useRef<HTMLElement | null>(null);
  const pendingScrollRef = useRef<string | null>(null);
  const urlReadyRef = useRef(false);

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

  const startedTrackId = useMemo(() => {
    for (const id of RECOMMENDED_SPINE) {
      const t = trackById[id];
      if (!t) continue;
      const d = trackDoneCount(t, progress);
      if (d > 0 && d < t.steps.length) return id;
    }
    return null;
  }, [progress, trackById]);

  const heroTrack = trackById[startedTrackId || recommendedNextId] || LEARNING_TRACKS[0];
  const heroNextStep =
    heroTrack.steps.find((s) => !progress[stepKey(heroTrack.id, s.id)]) || heroTrack.steps[0];
  const heroNextIndex = Math.max(0, heroTrack.steps.findIndex((s) => s.id === heroNextStep.id));
  const heroLabel = startedTrackId
    ? "Continue where you left off"
    : anyProgress
      ? "Recommended next"
      : "Start here";
  const heroRealmId =
    LEARNING_REALMS.find((r) => r.trackIds.includes(heroTrack.id))?.id ?? "foundations";

  const activeThread = activeThreadId ? findThread(activeThreadId) : undefined;
  const activeBead =
    activeThread && activeBeadId ? findBead(activeThread, activeBeadId) : undefined;
  const threadMode = Boolean(activeThread && activeBead && !threadCeremonyId);
  const visibleSteps = useMemo(() => {
    if (threadMode && activeBead) {
      return track.steps.filter((s) => s.id === activeBead.stepId);
    }
    return track.steps;
  }, [threadMode, activeBead, track.steps]);

  useEffect(() => {
    return () => {
      if (advanceTimerRef.current) clearTimeout(advanceTimerRef.current);
    };
  }, []);

  function syncUrl(
    trackId: string,
    stepId?: string | null,
    thread?: { threadId?: string | null; beadId?: string | null } | null,
  ) {
    if (!urlReadyRef.current) return;
    const threadId = thread === null ? null : (thread?.threadId ?? activeThreadId);
    const beadId = thread === null ? null : (thread?.beadId ?? activeBeadId);
    router.replace(
      learnHref({
        trackId,
        stepId,
        threadId: threadId || null,
        beadId: beadId || null,
      }),
      { scroll: false },
    );
  }

  useEffect(() => {
    if (typeof window === "undefined") return;
    const { trackId, stepId, threadId, beadId } = parseLearnSearch(window.location.search);
    if (trackId && LEARNING_TRACKS.some((x) => x.id === trackId)) {
      setSelectedTrackId(trackId);
    }
    if (stepId) {
      setOpenStepId(stepId);
      pendingScrollRef.current = stepId;
    }
    if (threadId && findThread(threadId)) {
      setActiveThreadId(threadId);
      const bead = beadId && findBead(findThread(threadId)!, beadId);
      if (bead) {
        setActiveBeadId(bead.id);
        setSelectedTrackId(bead.trackId);
        setOpenStepId(bead.stepId);
        pendingScrollRef.current = bead.stepId;
      } else if (findThread(threadId)!.steps[0]) {
        const first = findThread(threadId)!.steps[0];
        setActiveBeadId(first.id);
      }
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

  function selectTrack(trackId: string) {
    clearThreadMode();
    setSelectedTrackId(trackId);
    setOpenStepId(null);
    syncUrl(trackId, null, null);
    requestAnimationFrame(() => {
      pathSectionRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  /** Path-mode jump (hero, daily sit, spine) — leaves any active thread. */
  function continueTo(trackId: string, stepId: string) {
    clearThreadMode();
    setSelectedTrackId(trackId);
    setOpenStepId(stepId);
    pendingScrollRef.current = stepId;
    syncUrl(trackId, stepId, null);
  }

  /** Thread-mode jump — keeps horizontal context + next-bead chrome. */
  function openBead(threadId: string, beadId: string) {
    const thread = findThread(threadId);
    const bead = thread && findBead(thread, beadId);
    if (!thread || !bead) return;
    if (advanceTimerRef.current) {
      clearTimeout(advanceTimerRef.current);
      advanceTimerRef.current = null;
    }
    setThreadCeremonyId(null);
    setActiveThreadId(threadId);
    setActiveBeadId(beadId);
    setSelectedTrackId(bead.trackId);
    setOpenStepId(bead.stepId);
    pendingScrollRef.current = bead.stepId;
    syncUrl(bead.trackId, bead.stepId, { threadId, beadId });
  }

  function startThread(threadId: string) {
    const thread = findThread(threadId);
    const first = thread?.steps[0];
    if (!first) return;
    openBead(threadId, first.id);
  }

  function leaveThread() {
    clearThreadMode();
    syncUrl(selectedTrackId, openStepId === "__none__" ? null : openStepId, null);
  }

  /** Finish thread mode but keep the current path gate open. */
  function descendPathFromThread() {
    setActiveThreadId(null);
    setActiveBeadId(null);
    setThreadCeremonyId(null);
    syncUrl(selectedTrackId, openStepId === "__none__" ? null : openStepId, null);
  }

  function backToThreadMap() {
    setThreadCeremonyId(null);
    requestAnimationFrame(() => {
      document.getElementById("threads")?.scrollIntoView({ behavior: "smooth", block: "start" });
      if (activeThreadId) {
        document.getElementById(`thread-${activeThreadId}`)?.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    });
  }

  function goToStepIndex(targetIdx: number) {
    const s = track.steps[targetIdx];
    if (!s) return;
    setOpenStepId(s.id);
    pendingScrollRef.current = s.id;
    syncUrl(track.id, s.id, null);
  }

  function onGateComplete(trackId: string, stepId: string) {
    const key = stepKey(trackId, stepId);
    if (!progress[key]) toggle(trackId, stepId);

    if (!activeThreadId || !activeBeadId) {
      // Path mode: flow straight into the next gate instead of leaving the
      // reader to scroll down and expand another dropdown. A short beat lets
      // the "complete" state register before the next gate opens in place.
      const idx = track.steps.findIndex((x) => x.id === stepId);
      const next = idx >= 0 ? track.steps[idx + 1] : undefined;
      if (next) {
        if (advanceTimerRef.current) clearTimeout(advanceTimerRef.current);
        advanceTimerRef.current = setTimeout(() => {
          setOpenStepId(next.id);
          pendingScrollRef.current = next.id;
          syncUrl(track.id, next.id, null);
          advanceTimerRef.current = null;
        }, 450);
      }
      return;
    }
    const thread = findThread(activeThreadId);
    if (!thread) return;
    const idx = beadIndex(thread, activeBeadId);
    const next = idx >= 0 ? thread.steps[idx + 1] : undefined;
    if (next) {
      if (advanceTimerRef.current) clearTimeout(advanceTimerRef.current);
      advanceTimerRef.current = setTimeout(() => {
        openBead(activeThreadId, next.id);
        advanceTimerRef.current = null;
      }, 450);
      return;
    }
    setThreadCeremonyId(activeThreadId);
    requestAnimationFrame(() => {
      pathSectionRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  function openStep(stepId: string, isOpen: boolean) {
    if (threadMode) {
      // In thread focus, the single gate stays open — collapse would empty the view.
      return;
    }
    if (isOpen) {
      setOpenStepId("__none__");
      syncUrl(selectedTrackId, null);
      return;
    }
    setOpenStepId(stepId);
    const thread = activeThreadId ? findThread(activeThreadId) : undefined;
    const bead = thread && activeBeadId ? findBead(thread, activeBeadId) : undefined;
    const stillOnBead = Boolean(
      bead && bead.stepId === stepId && bead.trackId === selectedTrackId,
    );
    if (!stillOnBead) clearThreadMode();
    syncUrl(selectedTrackId, stepId, stillOnBead ? undefined : null);
    requestAnimationFrame(() => {
      stepRefs.current[stepId]?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  function openOrUnmark(trackId: string, stepId: string, done: boolean) {
    if (done) {
      toggle(trackId, stepId);
      return;
    }
    if (threadMode) return;
    openStep(stepId, openStepId === stepId);
  }

  return (
    <main className="page-shell page-shell--reading">
      <div className="section-stack">
      <div>
      <header className="library-header">
        <div className="library-header__body">
          <p className="passage-reading__meta">Guided study</p>
          <h1 className="library-header__title">Paths</h1>
          <p className="library-header__lede">
            Descend a path gate by gate, or trace one insight across traditions with a thread.
            Each gate is a practice, not a playlist item.
          </p>
        </div>
      </header>

      <section className="mt-6">
        <button
          type="button"
          onClick={() => continueTo(heroTrack.id, heroNextStep.id)}
          className="learn-continue group w-full max-w-[var(--reading-measure)] text-left"
        >
          <p className="passage-reading__meta">{heroLabel}</p>
          <div className="mt-2 flex flex-wrap items-end justify-between gap-3">
            <div className="min-w-0">
              <h2 className="text-2xl font-medium leading-tight tracking-[-0.02em] text-[rgb(250_237_205)] sm:text-[1.65rem]">
                {heroTrack.title}
              </h2>
              <p className="soft mt-1.5 text-sm leading-relaxed">
                {startedTrackId
                  ? `Next · Step ${heroNextIndex + 1}: ${heroNextStep.title}`
                  : heroTrack.focus}
              </p>
            </div>
            <span className={buttonVariants({ size: "sm" })}>
              {startedTrackId ? "Continue →" : "Begin →"}
            </span>
          </div>
        </button>

        <DailySitCard
          track={heroTrack}
          step={heroNextStep}
          stepIndex={heroNextIndex}
          realmId={heroRealmId}
          onBegin={() => continueTo(heroTrack.id, heroNextStep.id)}
        />
      </section>
      </div>

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
          selectedTrackId={selectedTrackId}
          recommendedNextId={recommendedNextId}
          anyProgress={hydrated && anyProgress}
          onSelectTrack={selectTrack}
          onOpenGate={continueTo}
        />
      </Section>

      <section ref={pathSectionRef} className="learn-path scroll-mt-24">
        {(threadMode || threadCeremonyId) && activeThreadId && activeBeadId ? (
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
          <div className="relative mt-2">
            <ThreadCompleteCard
              threadId={threadCeremonyId}
              progress={progress}
              onBackToMap={backToThreadMap}
              onTraceAnother={startThread}
              onDescendPath={descendPathFromThread}
              onLeaveThread={leaveThread}
            />
          </div>
        ) : (
          <>
            <div className="relative flex flex-wrap items-start justify-between gap-4">
              <div className="max-w-[var(--reading-measure)]">
                {threadMode && activeThread && activeBead ? (
                  <>
                    <p className="passage-reading__meta">Thread gate</p>
                    <h2 className="library-header__title mt-2">{activeThread.title}</h2>
                    <p className="library-header__lede">{activeBead.insight}</p>
                    <p className="mt-3 font-sans text-xs uppercase tracking-[0.18em] text-stone-400">
                      {activeBead.tradition} · from path “{track.title}”
                    </p>
                    <p className="mt-2 max-w-[var(--reading-measure)] text-sm leading-relaxed text-stone-400">
                      Other path gates are hidden while you trace this theme. Complete the gate to advance to the next
                      bead.
                    </p>
                  </>
                ) : (
                  <>
                    <p className="passage-reading__meta">Current path</p>
                    <h2 className="library-header__title mt-2">{track.title}</h2>
                    <p className="library-header__lede">{track.outcome}</p>
                    <p className="mt-3 max-w-[var(--reading-measure)] leading-relaxed text-stone-300">{track.arc}</p>
                    <p className="mt-3 font-sans text-xs uppercase tracking-[0.18em] text-stone-400">
                      {track.level} · {track.estimatedSessions}
                    </p>
                  </>
                )}
              </div>
              {!threadMode ? (
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
              ) : (
                <Button type="button" onClick={descendPathFromThread} variant="secondary" size="sm">
                  Show full path
                </Button>
              )}
            </div>
            {importStatus ? (
              <p className="relative mt-3 font-sans text-xs text-amber-200/80" role="status">
                {importStatus}
              </p>
            ) : null}

            {!threadMode ? (
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
            ) : null}

            <div className="relative mt-8 space-y-5">
              {!threadMode ? (
                <div className="absolute bottom-8 left-6 top-8 hidden w-px bg-gradient-to-b from-transparent via-amber-200/25 to-transparent sm:block" />
              ) : null}
              {visibleSteps.map((s) => {
                const pathIdx = track.steps.findIndex((x) => x.id === s.id);
                const idx = pathIdx >= 0 ? pathIdx : 0;
                const done = !!progress[stepKey(track.id, s.id)];
                const current = idx === activeIndex && !done;
                const isOpen = threadMode || openStepId === s.id || (openStepId === null && current);
                const item = matchStepItem(s, items);
                const supporting = (s.supportingPassageIds || [])
                  .map((id) => resolveById(items, id))
                  .filter((v): v is VerseItem => Boolean(v));
                const memberships = threadMode ? [] : threadsForPathStep(track.id, s.id);
                const backHref = learnHref({
                  trackId: track.id,
                  stepId: s.id,
                  threadId: activeThreadId,
                  beadId: activeBeadId,
                });
                const readHref = item
                  ? `/read/${encodeURIComponent(item._id)}?back=${encodeURIComponent(backHref)}`
                  : `/read`;
                const chatHref = item
                  ? `/chat?verse_id=${encodeURIComponent(item._id)}&mode=${encodeURIComponent(s.chatMode || "question")}&q=${encodeURIComponent(s.chatPrompt)}`
                  : `/chat?q=${encodeURIComponent(s.chatPrompt)}`;
                const openLabel = item ? "Open in Library" : "Browse Library";
                const beadNum =
                  threadMode && activeThread && activeBeadId
                    ? beadIndex(activeThread, activeBeadId) + 1
                    : idx + 1;
                const isLastBead =
                  threadMode &&
                  activeThread &&
                  activeBeadId &&
                  beadIndex(activeThread, activeBeadId) >= activeThread.steps.length - 1;
                return (
                  <article
                    key={s.id}
                    ref={(el) => {
                      stepRefs.current[s.id] = el;
                    }}
                    className={`relative scroll-mt-24 ${threadMode ? "" : "sm:pl-16"} ${current || isOpen ? "" : "opacity-90"}`}
                  >
                    {!threadMode ? (
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
                    ) : null}

                    <div
                      className={`learn-gate border-t py-5 ${
                        threadMode || current
                          ? "border-amber-200/35"
                          : "border-[rgb(240_201_121_/_0.12)]"
                      }`}
                    >
                      <div className="flex flex-wrap items-center justify-between gap-3">
                        <p className="font-sans text-xs uppercase tracking-[0.2em] text-amber-200/80">
                          {threadMode
                            ? `Bead ${beadNum}${done ? " • complete" : ""}`
                            : `Step ${idx + 1} ${current ? "• next up" : done ? "• complete" : ""}`}
                        </p>
                        {threadMode ? null : done ? (
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

                      {threadMode ? (
                        <div className="mt-3">
                          <h3 className="text-2xl leading-tight text-stone-100">{s.title}</h3>
                          <p className="soft mt-2 text-base leading-relaxed">{s.orientation}</p>
                        </div>
                      ) : (
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
                      )}

                      {memberships.length > 0 ? (
                        <div className="mt-3 flex flex-wrap items-center gap-2">
                          <span className="font-sans text-[9px] uppercase tracking-[0.14em] text-stone-500">Also on</span>
                          {memberships.map(({ thread, bead }) => {
                            const onThis = activeThreadId === thread.id && activeBeadId === bead.id;
                            return (
                              <button
                                key={`${thread.id}:${bead.id}`}
                                type="button"
                                onClick={() => openBead(thread.id, bead.id)}
                                className={`rounded-full border px-2.5 py-1 font-sans text-[10px] uppercase tracking-[0.12em] transition ${
                                  onThis
                                    ? "border-amber-200/50 bg-amber-200/15 text-amber-100"
                                    : "border-white/12 text-amber-200/70 hover:border-amber-200/35 hover:text-amber-100"
                                }`}
                              >
                                {thread.glyph} {thread.title}
                              </button>
                            );
                          })}
                        </div>
                      ) : null}

                      {isOpen ? (
                        <div className="mt-4 space-y-4">
                          <p className="reading-prose max-w-[var(--reading-measure)] leading-relaxed text-stone-200">
                            {s.teaching}
                          </p>

                          <div className="passage-practice--plain mt-6">
                            <p className="passage-layer__label">Key idea</p>
                            <p className="passage-practice__body">{s.keyIdea}</p>
                          </div>

                          {s.misconception ? (
                            <div className="mt-5 max-w-[var(--reading-measure)] border-t border-rose-300/20 pt-4">
                              <p className="font-sans text-xs uppercase tracking-[0.16em] text-rose-200/80">
                                Common misunderstanding
                              </p>
                              <p className="mt-2 text-sm leading-relaxed text-stone-200">{s.misconception}</p>
                            </div>
                          ) : null}

                          <div>
                            <p className="layer-heading">Study these passages</p>
                            <div className="mt-2 space-y-2">
                              {item ? (
                                <PassageLink item={item} primary backHref={backHref} />
                              ) : (
                                <p className="rounded-2xl border border-rose-300/25 bg-rose-300/5 p-3 font-sans text-sm text-stone-200">
                                  Primary passage missing from the Library
                                  {s.passageId ? (
                                    <>
                                      {" "}
                                      <code className="text-rose-100/90">{s.passageId}</code>)
                                    </>
                                  ) : null}
                                  . Supporting texts below may still be available; the path pin needs a corpus fix.
                                </p>
                              )}
                              {supporting.map((sv) => (
                                <PassageLink key={sv._id} item={sv} backHref={backHref} />
                              ))}
                            </div>
                          </div>

                          <div className="passage-practice--plain">
                            <p className="passage-layer__label">Practice</p>
                            <p className="passage-practice__body">{s.practice}</p>
                          </div>

                          {item ? (
                            <JournalPanel passage={item} prompt={s.journalPrompt} />
                          ) : (
                            <JournalPanel
                              contextId={learnStepContextId(track.id, s.id)}
                              contextTitle={`${track.title} · ${s.title}`}
                              prompt={s.journalPrompt}
                            />
                          )}

                          <StepIntegrationGate
                            stepId={s.id}
                            integration={s.integration}
                            done={done}
                            completeLabel={
                              threadMode
                                ? isLastBead
                                  ? "Mark complete & finish thread"
                                  : "Mark complete & next bead →"
                                : undefined
                            }
                            onComplete={() => onGateComplete(track.id, s.id)}
                          />

                          {threadMode && done ? (
                            <div className="flex flex-wrap gap-2">
                              {!isLastBead ? (
                                <Button
                                  type="button"
                                  size="sm"
                                  onClick={() => {
                                    if (!activeThread || !activeBeadId) return;
                                    const idx = beadIndex(activeThread, activeBeadId);
                                    const next = activeThread.steps[idx + 1];
                                    if (next) openBead(activeThread.id, next.id);
                                  }}
                                >
                                  Next bead →
                                </Button>
                              ) : (
                                <Button
                                  type="button"
                                  size="sm"
                                  onClick={() => {
                                    if (activeThreadId) setThreadCeremonyId(activeThreadId);
                                  }}
                                >
                                  Finish thread
                                </Button>
                              )}
                            </div>
                          ) : null}

                          <div className="flex flex-wrap gap-2 pt-1">
                            <Link href={readHref} className={buttonVariants({ size: "sm" })}>
                              {openLabel}
                            </Link>
                            <Link href={chatHref} className={buttonVariants({ variant: "secondary", size: "sm" })}>
                              {actionLabel(s.chatMode)}
                            </Link>
                            <Link href="/journal" className={buttonVariants({ variant: "secondary", size: "sm" })}>
                              All journal notes
                            </Link>
                          </div>

                          {!threadMode ? (
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
                                  {done ? "Next gate →" : "Skip to next →"}
                                </Button>
                              ) : (
                                <span className="font-sans text-[11px] uppercase tracking-[0.16em] text-amber-200/70">
                                  Path end
                                </span>
                              )}
                            </div>
                          ) : null}
                        </div>
                      ) : null}
                    </div>
                  </article>
                );
              })}
            </div>
          </>
        )}
      </section>

      <ThreadsConstellation
        progress={progress}
        hydrated={hydrated}
        activeThreadId={activeThreadId}
        activeBeadId={activeBeadId}
        onOpenBead={openBead}
      />
      </div>

      <Dialog open={resetOpen} onOpenChange={setResetOpen}>
        <DialogContent className="border border-amber-200/20 bg-[#171421] sm:max-w-md">
          <DialogHeader>
            <DialogTitle className="text-xl text-amber-100">Reset path progress?</DialogTitle>
            <DialogDescription className="soft text-base leading-relaxed">
              Clear all gates on “{track.title}”. This cannot be undone.
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
    </main>
  );
}
