'use client';

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useRef, useState } from "react";
import { getVerses } from "@/lib/api";
import { DailySitCard } from "@/components/learn/DailySitCard";
import { JourneyMandala } from "@/components/learn/JourneyMandala";
import { StepIntegrationGate } from "@/components/learn/StepIntegrationGate";
import { ThreadContextBar } from "@/components/learn/ThreadContextBar";
import { ThreadsConstellation } from "@/components/learn/ThreadsConstellation";
import { YantraBreath } from "@/components/learn/YantraBreath";
import { JournalPanel } from "@/components/JournalPanel";
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
  findBead,
  findThread,
  threadsForPathStep,
} from "@/lib/learningThreads";
import { learnStepContextId } from "@/lib/journalStorage";
import { generatedArtPool } from "@/lib/collectionImages";
import { ArtBackdrop } from "@/components/ArtImage";
import { Glyph } from "@/components/Glyph";
import type { VerseItem } from "@/lib/types";
import { passagePreview } from "@/lib/verseLayers";
import { displayCollectionName } from "@/lib/collectionLabels";
import { displayPassageTitle } from "@/lib/passageTitles";

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
    <Link
      href={href}
      className={`citation-card block p-3 transition hover:border-amber-300/40 ${primary ? "" : "opacity-90"}`}
    >
      <p className="font-sans text-[11px] uppercase tracking-[0.16em] text-amber-200/70">
        {displayCollectionName(item.collection)}
        {item.section ? ` · ${item.section}` : ""}
      </p>
      <h5 className="mt-1 text-base leading-tight text-amber-100">{displayPassageTitle(item)}</h5>
      {primary ? <p className="soft mt-1 line-clamp-2 text-sm leading-relaxed">{passagePreview(item)}</p> : null}
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
    setActiveThreadId(threadId);
    setActiveBeadId(beadId);
    setSelectedTrackId(bead.trackId);
    setOpenStepId(bead.stepId);
    pendingScrollRef.current = bead.stepId;
    syncUrl(bead.trackId, bead.stepId, { threadId, beadId });
  }

  function leaveThread() {
    clearThreadMode();
    syncUrl(selectedTrackId, openStepId === "__none__" ? null : openStepId, null);
  }

  function backToThreadMap() {
    requestAnimationFrame(() => {
      document.getElementById("threads")?.scrollIntoView({ behavior: "smooth", block: "start" });
      if (activeThreadId) {
        document.getElementById(`thread-${activeThreadId}`)?.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    });
  }

  function openStep(stepId: string, isOpen: boolean) {
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
    openStep(stepId, openStepId === stepId);
  }

  return (
    <main className="page-shell">
      <div className="relative">
        <Glyph
          name="mandala"
          size="hero"
          className="pointer-events-none absolute -right-4 -top-6 opacity-[0.12] sm:-right-2 sm:top-0"
        />
        <p className="eyebrow">Guided study</p>
        <h1 className="mt-3 text-5xl font-semibold leading-none tracking-[-0.04em] text-stone-100 sm:text-6xl">Paths</h1>
        <p className="soft mt-4 max-w-2xl text-xl leading-relaxed">
          Paths descend like a cakra — gate by gate. Threads trace one golden insight across traditions. Each step is a
          practice, not a playlist item.
        </p>
      </div>

      <section className="mt-7">
        <button
          type="button"
          onClick={() => continueTo(heroTrack.id, heroNextStep.id)}
          className="resume-hero card group w-full overflow-hidden border-amber-200/40 p-5 text-left transition hover:-translate-y-0.5 sm:p-6"
        >
          <ArtBackdrop srcs={generatedArtPool("bg-paths")} variant="card" />
          <div className="relative z-10">
            <p className="font-sans text-xs uppercase tracking-[0.18em] text-amber-200/80">{heroLabel}</p>
            <div className="mt-3 flex flex-wrap items-end justify-between gap-4">
              <div>
                <h2 className="text-3xl leading-none text-amber-100 sm:text-4xl">{heroTrack.title}</h2>
                <p className="soft mt-2 max-w-xl text-sm leading-relaxed">
                  {startedTrackId
                    ? `Next · Step ${heroNextIndex + 1}: ${heroNextStep.title}`
                    : heroTrack.focus}
                </p>
              </div>
              <span className="btn-primary px-5 py-2 text-sm">{startedTrackId ? "Continue →" : "Begin →"}</span>
            </div>
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

      <ThreadsConstellation
        progress={progress}
        hydrated={hydrated}
        activeThreadId={activeThreadId}
        activeBeadId={activeBeadId}
        onOpenBead={openBead}
      />

      <JourneyMandala
        trackById={trackById}
        progress={progress}
        hydrated={hydrated}
        selectedTrackId={selectedTrackId}
        recommendedNextId={recommendedNextId}
        anyProgress={hydrated && anyProgress}
        onSelectTrack={selectTrack}
      />

      <section ref={pathSectionRef} className="manuscript-card relative mt-8 scroll-mt-24 overflow-hidden p-5 sm:p-7">
        <YantraBreath className="pointer-events-none absolute -right-24 -top-24 h-64 w-64 opacity-[0.18] sm:h-80 sm:w-80" />
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
        <div className="relative flex flex-wrap items-start justify-between gap-4">
          <div className="max-w-3xl">
            <p className="eyebrow">{activeThreadId ? "Path gate · on thread" : "Current path"}</p>
            <h2 className="mt-3 text-4xl font-semibold leading-none text-amber-100 sm:text-5xl">{track.title}</h2>
            <p className="soft mt-3 text-lg leading-relaxed">{track.outcome}</p>
            <p className="mt-4 leading-relaxed text-stone-300">{track.arc}</p>
            <p className="mt-3 font-sans text-xs uppercase tracking-[0.18em] text-stone-400">
              {track.level} · {track.estimatedSessions}
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <button
              type="button"
              onClick={exportProgress}
              disabled={!hydrated}
              className="btn-secondary px-4 py-2 text-sm disabled:opacity-40"
            >
              Export progress
            </button>
            <button
              type="button"
              onClick={openImportPicker}
              disabled={!hydrated}
              className="btn-secondary px-4 py-2 text-sm disabled:opacity-40"
            >
              Import progress
            </button>
            <button
              type="button"
              disabled={!hydrated}
              onClick={() => {
                if (
                  typeof window !== "undefined" &&
                  window.confirm(`Reset progress on “${track.title}”? This cannot be undone.`)
                ) {
                  resetTrack(track.id, track);
                }
              }}
              className="btn-secondary px-4 py-2 text-sm disabled:opacity-40"
            >
              Reset path
            </button>
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
          <div className="mt-2 h-3 rounded-full bg-white/10">
            <div
              className={`h-3 rounded-full bg-amber-300 transition-[width] duration-300 ${hydrated ? "" : "animate-pulse"}`}
              style={{ width: hydrated ? `${pct}%` : "12%" }}
            />
          </div>
        </div>

        <div className="relative mt-8 space-y-5">
          <div className="absolute bottom-8 left-6 top-8 hidden w-px bg-gradient-to-b from-transparent via-amber-200/25 to-transparent sm:block" />
          {track.steps.map((s, idx) => {
            const done = !!progress[stepKey(track.id, s.id)];
            const current = idx === activeIndex && !done;
            const isOpen = openStepId === s.id || (openStepId === null && current);
            const item = matchStepItem(s, items);
            const supporting = (s.supportingPassageIds || [])
              .map((id) => resolveById(items, id))
              .filter((v): v is VerseItem => Boolean(v));
            const memberships = threadsForPathStep(track.id, s.id);
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

                <div className={`rounded-3xl border p-5 ${current ? "border-amber-200/60 bg-amber-100/10" : "border-amber-200/15 bg-black/10"}`}>
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <p className="font-sans text-xs uppercase tracking-[0.2em] text-amber-200/80">
                      Step {idx + 1} {current ? "• next up" : done ? "• complete" : ""}
                    </p>
                    {done ? (
                      <button
                        type="button"
                        onClick={() => toggle(track.id, s.id)}
                        className="rounded-full border border-emerald-300/50 px-3 py-1 font-sans text-xs text-emerald-200"
                      >
                        Done · reopen
                      </button>
                    ) : (
                      <button
                        type="button"
                        onClick={() => openStep(s.id, isOpen)}
                        className="rounded-full border border-amber-200/30 px-3 py-1 font-sans text-xs text-amber-100"
                      >
                        {isOpen ? "Collapse" : "Open step"}
                      </button>
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
                      <span className="font-sans text-[9px] uppercase tracking-[0.14em] text-stone-500">Also on</span>
                      {memberships.map(({ thread, bead }) => {
                        const onThis =
                          activeThreadId === thread.id && activeBeadId === bead.id;
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
                      <p className="reading-prose leading-relaxed text-stone-200">{s.teaching}</p>

                      <div className="practice-card p-4">
                        <p className="layer-heading">Key idea</p>
                        <p className="mt-2 leading-relaxed text-amber-50">{s.keyIdea}</p>
                      </div>

                      {s.misconception ? (
                        <div className="rounded-2xl border border-rose-300/25 bg-rose-300/5 p-4">
                          <p className="font-sans text-xs uppercase tracking-[0.16em] text-rose-200/80">Common misunderstanding</p>
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
                                  (<code className="text-rose-100/90">{s.passageId}</code>)
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

                      <div className="card p-4">
                        <p className="layer-heading">Practice</p>
                        <p className="mt-2 leading-relaxed text-stone-200">{s.practice}</p>
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
                        onComplete={() => toggle(track.id, s.id)}
                      />

                      <div className="flex flex-wrap gap-2 pt-1">
                        <Link href={readHref} className="btn-primary px-4 py-2 text-sm">
                          {openLabel}
                        </Link>
                        <Link href={chatHref} className="btn-secondary px-4 py-2 text-sm">
                          {actionLabel(s.chatMode)}
                        </Link>
                        <Link href="/journal" className="btn-secondary px-4 py-2 text-sm">
                          All journal notes
                        </Link>
                      </div>
                    </div>
                  ) : null}
                </div>
              </article>
            );
          })}
        </div>
      </section>
    </main>
  );
}
