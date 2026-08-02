"use client";

import { useEffect, useMemo, useRef, useState, type ReactNode } from "react";
import {
  RECOMMENDED_SPINE,
  type LearningRealm,
  type LearningTrack,
} from "@/lib/learningPaths";
import { Glyph } from "@/components/Glyph";
import type { GlyphSlug } from "@/lib/glyphs";
import { InkGlyph, SpandaMedallion } from "@/components/InkGlyph";
import { sumiGlyph, unitSumiGlyph, type SumiSlug } from "@/lib/sumiGlyphs";

type ProgressMap = Record<string, boolean>;

type Focus =
  | { level: "root" }
  | { level: "realm"; realmId: string }
  | { level: "path"; realmId: string; trackId: string };

type PathTreeProps = {
  realms: LearningRealm[];
  trackById: Record<string, LearningTrack>;
  progress: ProgressMap;
  /** Wait for localStorage progress to avoid SSR mismatch. */
  hydrated: boolean;
  /** Path currently open in the detail section below. */
  selectedTrackId: string;
  recommendedNextId: string;
  anyProgress: boolean;
  /** Open a whole path in the detail section (and scroll to it). */
  onSelectTrack: (trackId: string) => void;
  /** Open a specific gate in the detail section (and scroll to it). */
  onOpenGate: (trackId: string, stepId: string) => void;
};

const REALM_GLYPH: Record<string, GlyphSlug> = {
  foundations: "roots",
  trika: "shiva",
  vedanta: "void",
  bridges: "bridge",
};

function realmGlyph(id: string): GlyphSlug {
  return REALM_GLYPH[id] ?? "lotus";
}

const REALM_SUMI: Record<string, SumiSlug> = {
  foundations: "tree",
  trika: "eye",
  vedanta: "circle",
  bridges: "infinity",
};

function realmSumi(id: string): SumiSlug {
  return REALM_SUMI[id] ?? "lotus";
}

function stepKey(trackId: string, stepId: string): string {
  return `${trackId}:${stepId}`;
}

function trackDone(t: LearningTrack, progress: ProgressMap): number {
  return t.steps.filter((s) => progress[stepKey(t.id, s.id)]).length;
}

type Agg = { done: number; total: number; complete: boolean; started: boolean; pct: number };

function aggregate(done: number, total: number): Agg {
  const safeTotal = Math.max(1, total);
  return {
    done,
    total,
    complete: total > 0 && done >= total,
    started: done > 0,
    pct: Math.round((done / safeTotal) * 100),
  };
}

function realmAggregate(
  realm: LearningRealm,
  trackById: Record<string, LearningTrack>,
  progress: ProgressMap,
): Agg {
  let done = 0;
  let total = 0;
  for (const tid of realm.trackIds) {
    const t = trackById[tid];
    if (!t) continue;
    done += trackDone(t, progress);
    total += t.steps.length;
  }
  return aggregate(done, total);
}

/** Small glanceable completion ring. */
function ProgressRing({
  pct,
  complete,
  next,
  children,
}: {
  pct: number;
  complete?: boolean;
  next?: boolean;
  children?: ReactNode;
}) {
  const r = 15;
  const c = 2 * Math.PI * r;
  const dash = (Math.min(100, Math.max(0, pct)) / 100) * c;
  const stroke = complete ? "rgb(110 231 183)" : next ? "rgb(240 201 121)" : "rgb(240 201 121 / 0.75)";
  return (
    <span className="relative flex h-11 w-11 shrink-0 items-center justify-center sm:h-12 sm:w-12">
      <svg viewBox="0 0 36 36" className="h-full w-full -rotate-90" aria-hidden>
        <circle cx="18" cy="18" r={r} fill="none" stroke="rgb(255 255 255 / 0.10)" strokeWidth="2.5" />
        <circle
          cx="18"
          cy="18"
          r={r}
          fill="none"
          stroke={stroke}
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeDasharray={`${dash} ${c}`}
          className="transition-[stroke-dasharray] duration-500"
        />
      </svg>
      <span className="absolute inset-0 flex items-center justify-center text-[11px] font-bold text-amber-50">
        {children}
      </span>
    </span>
  );
}

/** Breadcrumb of connected nodes showing the branch you've descended. */
function TreeTrail({
  focus,
  realmTitle,
  trackTitle,
  onZoom,
}: {
  focus: Focus;
  realmTitle?: string;
  trackTitle?: string;
  onZoom: (f: Focus) => void;
}) {
  const crumbs: Array<{ key: string; label: string; glyph: GlyphSlug; focus: Focus; active: boolean }> = [
    {
      key: "root",
      label: "The Journey",
      glyph: "mandala",
      focus: { level: "root" },
      active: focus.level === "root",
    },
  ];
  if (focus.level !== "root") {
    crumbs.push({
      key: "realm",
      label: realmTitle ?? "Realm",
      glyph: realmGlyph(focus.realmId),
      focus: { level: "realm", realmId: focus.realmId },
      active: focus.level === "realm",
    });
  }
  if (focus.level === "path") {
    crumbs.push({
      key: "path",
      label: trackTitle ?? "Path",
      glyph: "gateway",
      focus,
      active: true,
    });
  }

  return (
    <nav className="flex flex-wrap items-center gap-x-1 gap-y-2" aria-label="Map location">
      {crumbs.map((crumb, i) => (
        <span key={crumb.key} className="flex items-center gap-1">
          {i > 0 ? (
            <span className="px-0.5 font-sans text-amber-200/30" aria-hidden>
              ›
            </span>
          ) : null}
          <button
            type="button"
            onClick={() => onZoom(crumb.focus)}
            aria-current={crumb.active ? "true" : undefined}
            className={`flex items-center gap-1.5 rounded-full border px-2.5 py-1 font-sans text-[11px] uppercase tracking-[0.14em] transition ${
              crumb.active
                ? "border-amber-200/45 bg-amber-200/10 text-amber-100"
                : "border-white/10 text-amber-200/60 hover:border-amber-200/35 hover:text-amber-100"
            }`}
          >
            <Glyph name={crumb.glyph} size="xs" className="opacity-80" />
            <span className="max-w-[9rem] truncate">{crumb.label}</span>
          </button>
        </span>
      ))}
    </nav>
  );
}

/** A single branch node: medallion on the rail + a glanceable card body. */
function BranchNode({
  index,
  count,
  medallion,
  onClick,
  ariaLabel,
  highlight,
  children,
}: {
  index: number;
  count: number;
  medallion: ReactNode;
  onClick: () => void;
  ariaLabel: string;
  highlight?: boolean;
  children: ReactNode;
}) {
  const isFirst = index === 0;
  const isLast = index === count - 1;
  return (
    <li className="relative flex gap-3 sm:gap-4">
      {/* Rail column: connects medallions into one descending branch. */}
      <div className="relative flex w-11 shrink-0 flex-col items-center sm:w-12">
        <span
          aria-hidden
          className={`w-[1.5px] flex-none bg-gradient-to-b from-amber-200/25 to-amber-200/25 blur-[0.2px] ${
            isFirst ? "h-3 opacity-0" : "h-3"
          }`}
        />
        {medallion}
        <span
          aria-hidden
          className={`w-[1.5px] flex-1 bg-gradient-to-b from-amber-200/25 to-amber-200/10 blur-[0.2px] ${
            isLast ? "opacity-0" : ""
          }`}
        />
        {/* horizontal stub into the card */}
        <span
          aria-hidden
          className="absolute left-1/2 top-[calc(0.75rem+1.375rem)] h-px w-3 -translate-y-1/2 bg-amber-200/25 sm:top-[calc(0.75rem+1.5rem)]"
        />
      </div>
      <button
        type="button"
        onClick={onClick}
        aria-label={ariaLabel}
        className={`group mb-3 flex-1 rounded-2xl border p-4 text-left transition hover:-translate-y-0.5 sm:p-5 ${
          highlight
            ? "border-amber-200/55 bg-amber-100/[0.07]"
            : "border-white/10 bg-black/15 hover:border-amber-200/35"
        }`}
      >
        {children}
      </button>
    </li>
  );
}

function StatePill({ agg, next, start }: { agg: Agg; next?: boolean; start?: boolean }) {
  if (agg.complete) {
    return (
      <span className="rounded-full border border-emerald-300/40 bg-emerald-300/10 px-2.5 py-0.5 font-sans text-[10px] uppercase tracking-[0.12em] text-emerald-200">
        Complete
      </span>
    );
  }
  if (next) {
    return (
      <span className="rounded-full border border-amber-200/45 bg-amber-200/10 px-2.5 py-0.5 font-sans text-[10px] uppercase tracking-[0.12em] text-amber-100">
        Recommended next
      </span>
    );
  }
  if (start) {
    return (
      <span className="rounded-full border border-amber-200/45 bg-amber-200/10 px-2.5 py-0.5 font-sans text-[10px] uppercase tracking-[0.12em] text-amber-100">
        Start here
      </span>
    );
  }
  if (agg.started) {
    return (
      <span className="rounded-full border border-amber-200/25 px-2.5 py-0.5 font-sans text-[10px] uppercase tracking-[0.12em] text-amber-200/70">
        In progress
      </span>
    );
  }
  return (
    <span className="rounded-full border border-white/10 px-2.5 py-0.5 font-sans text-[10px] uppercase tracking-[0.12em] text-stone-400">
      Not started
    </span>
  );
}

export function PathTree({
  realms,
  trackById,
  progress,
  hydrated,
  selectedTrackId,
  recommendedNextId,
  anyProgress,
  onSelectTrack,
  onOpenGate,
}: PathTreeProps) {
  const safeProgress = hydrated ? progress : {};
  const [focus, setFocus] = useState<Focus>({ level: "root" });
  const contentRef = useRef<HTMLDivElement | null>(null);
  const userNavigatedRef = useRef(false);

  const realmForTrack = useMemo(() => {
    const m: Record<string, string> = {};
    for (const r of realms) for (const tid of r.trackIds) m[tid] = r.id;
    return m;
  }, [realms]);

  // On an external path selection (hero / deep link) that the user did not
  // trigger from the tree, descend the map to that path's gates so the map
  // reflects where they are.
  // Initialised to the mount-time selection so a plain visit stays at the calm
  // root view; only a later change (deep link / hero) descends the map.
  const lastSyncedTrack = useRef<string | null>(selectedTrackId);
  useEffect(() => {
    if (lastSyncedTrack.current === selectedTrackId) return;
    lastSyncedTrack.current = selectedTrackId;
    if (userNavigatedRef.current) return;
    const realmId = realmForTrack[selectedTrackId];
    if (realmId) setFocus({ level: "path", realmId, trackId: selectedTrackId });
  }, [selectedTrackId, realmForTrack]);

  function zoom(f: Focus) {
    userNavigatedRef.current = true;
    setFocus(f);
  }

  const overall = useMemo(() => {
    let done = 0;
    let total = 0;
    let pathsComplete = 0;
    const totalPaths = RECOMMENDED_SPINE.length;
    for (const tid of RECOMMENDED_SPINE) {
      const t = trackById[tid];
      if (!t) continue;
      const d = trackDone(t, safeProgress);
      done += d;
      total += t.steps.length;
      if (t.steps.length > 0 && d >= t.steps.length) pathsComplete += 1;
    }
    return { ...aggregate(done, total), pathsComplete, totalPaths };
  }, [trackById, safeProgress]);

  const activeRealm =
    focus.level !== "root" ? realms.find((r) => r.id === focus.realmId) : undefined;
  const activeTrack =
    focus.level === "path" ? trackById[focus.trackId] : undefined;

  return (
    <div className="path-tree relative overflow-hidden border-t border-[rgb(240_201_121_/_0.14)] pt-5 sm:pt-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <TreeTrail
          focus={focus}
          realmTitle={activeRealm?.title}
          trackTitle={activeTrack?.title}
          onZoom={zoom}
        />
        <p className="font-sans text-[11px] uppercase tracking-[0.16em] text-amber-200/55">
          {hydrated ? `${overall.pathsComplete}/${overall.totalPaths} paths` : "…"}
        </p>
      </div>

      <div ref={contentRef} className="mt-6">
        {focus.level === "root" ? (
          <RootView
            realms={realms}
            trackById={trackById}
            progress={safeProgress}
            hydrated={hydrated}
            overall={overall}
            recommendedRealmId={realmForTrack[recommendedNextId]}
            onOpenRealm={(realmId) => zoom({ level: "realm", realmId })}
          />
        ) : null}

        {focus.level === "realm" && activeRealm ? (
          <RealmView
            realm={activeRealm}
            trackById={trackById}
            progress={safeProgress}
            recommendedNextId={recommendedNextId}
            anyProgress={anyProgress}
            selectedTrackId={selectedTrackId}
            onOpenPath={(trackId) =>
              zoom({ level: "path", realmId: activeRealm.id, trackId })
            }
          />
        ) : null}

        {focus.level === "path" && activeTrack && activeRealm ? (
          <GateView
            track={activeTrack}
            progress={safeProgress}
            onOpenGate={(stepId) => {
              onOpenGate(activeTrack.id, stepId);
            }}
            onOpenFullPath={() => onSelectTrack(activeTrack.id)}
          />
        ) : null}
      </div>
    </div>
  );
}

function RootView({
  realms,
  trackById,
  progress,
  hydrated,
  overall,
  recommendedRealmId,
  onOpenRealm,
}: {
  realms: LearningRealm[];
  trackById: Record<string, LearningTrack>;
  progress: ProgressMap;
  hydrated: boolean;
  overall: Agg & { pathsComplete: number; totalPaths: number };
  recommendedRealmId?: string;
  onOpenRealm: (realmId: string) => void;
}) {
  return (
    <div>
      {/* Root node */}
      <div className="flex items-center gap-4 rounded-2xl border border-amber-200/20 bg-amber-100/[0.04] p-4 sm:p-5">
        <ProgressRing pct={hydrated ? overall.pct : 0} complete={overall.complete}>
          <InkGlyph glyph="mandala" state="arising" size="sm" />
        </ProgressRing>
        <div className="min-w-0">
          <p className="eyebrow">Root · the whole journey</p>
          <h3 className="mt-1 text-2xl leading-tight text-amber-100">Four realms, eight paths</h3>
          <p className="soft mt-1 text-sm leading-relaxed">
            Choose a realm to branch into its paths, then descend a path gate by gate.
          </p>
        </div>
      </div>

      {/* Realm branches */}
      <p className="mt-6 mb-3 font-sans text-[11px] uppercase tracking-[0.18em] text-amber-200/50">
        Realms branch from here
      </p>
      <ul className="grid list-none gap-3 sm:grid-cols-2">
        {realms.map((realm) => {
          const agg = realmAggregate(realm, trackById, progress);
          const isNext = realm.id === recommendedRealmId && !agg.complete;
          return (
            <li key={realm.id}>
              <button
                type="button"
                onClick={() => onOpenRealm(realm.id)}
                aria-label={`Open realm ${realm.title}. ${agg.done} of ${agg.total} gates complete.`}
                className={`group flex h-full w-full flex-col rounded-2xl border p-5 text-left transition hover:-translate-y-0.5 ${
                  isNext
                    ? "border-amber-200/50 bg-amber-100/[0.06]"
                    : "border-white/10 bg-black/15 hover:border-amber-200/35"
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <ProgressRing pct={agg.pct} complete={agg.complete} next={isNext}>
                    <InkGlyph
                      glyph={realmSumi(realm.id)}
                      state={agg.complete ? "recognized" : isNext ? "arising" : "unmanifest"}
                      size="sm"
                    />
                  </ProgressRing>
                  <span className="font-sans text-[10px] uppercase tracking-[0.14em] text-stone-400">
                    {realm.trackIds.length} paths
                  </span>
                </div>
                <h4 className="mt-3 text-xl leading-tight text-amber-100">{realm.title}</h4>
                <p className="soft mt-2 line-clamp-2 text-sm leading-relaxed">{realm.blurb}</p>
                <div className="mt-4 flex items-center justify-between">
                  <StatePill agg={agg} next={isNext} />
                  <span className="font-sans text-[11px] uppercase tracking-[0.14em] text-amber-200/70 transition group-hover:text-amber-100">
                    Branch in →
                  </span>
                </div>
              </button>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

function RealmView({
  realm,
  trackById,
  progress,
  recommendedNextId,
  anyProgress,
  selectedTrackId,
  onOpenPath,
}: {
  realm: LearningRealm;
  trackById: Record<string, LearningTrack>;
  progress: ProgressMap;
  recommendedNextId: string;
  anyProgress: boolean;
  selectedTrackId: string;
  onOpenPath: (trackId: string) => void;
}) {
  const agg = realmAggregate(realm, trackById, progress);
  return (
    <div>
      <div className="flex items-center gap-4 rounded-2xl border border-amber-200/20 bg-amber-100/[0.04] p-4 sm:p-5">
        <ProgressRing pct={agg.pct} complete={agg.complete}>
          <InkGlyph glyph={realmSumi(realm.id)} state={agg.complete ? "recognized" : "arising"} size="sm" />
        </ProgressRing>
        <div className="min-w-0">
          <p className="eyebrow">Realm</p>
          <h3 className="mt-1 text-2xl leading-tight text-amber-100">{realm.title}</h3>
          <p className="soft mt-1 text-sm leading-relaxed">{realm.blurb}</p>
        </div>
      </div>

      <p className="mt-6 mb-3 font-sans text-[11px] uppercase tracking-[0.18em] text-amber-200/50">
        Paths in this realm
      </p>
      <ul className="list-none">
        {realm.trackIds.map((tid, i) => {
          const t = trackById[tid];
          if (!t) return null;
          const pathAgg = aggregate(trackDone(t, progress), t.steps.length);
          const spineN = RECOMMENDED_SPINE.indexOf(tid);
          const isNext = tid === recommendedNextId && !pathAgg.complete;
          const isStart = !anyProgress && tid === RECOMMENDED_SPINE[0];
          const isCurrent = tid === selectedTrackId;
          return (
            <BranchNode
              key={tid}
              index={i}
              count={realm.trackIds.length}
              highlight={isNext || isCurrent}
              onClick={() => onOpenPath(tid)}
              ariaLabel={`Open path ${t.title}. ${pathAgg.done} of ${pathAgg.total} gates complete.`}
              medallion={
                <span className="relative z-10 flex h-11 w-11 shrink-0 items-center justify-center sm:h-12 sm:w-12">
                  <SpandaMedallion
                    glyph={sumiGlyph(t.title)}
                    state={pathAgg.complete ? "recognized" : isNext || isStart ? "arising" : "unmanifest"}
                    size="md"
                  />
                  {spineN >= 0 ? (
                    <span
                      aria-hidden
                      className="absolute -bottom-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full border border-amber-200/30 bg-[#0b0b14] font-sans text-[9px] font-bold text-amber-200/70"
                    >
                      {spineN + 1}
                    </span>
                  ) : null}
                </span>
              }
            >
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  <p className="font-sans text-[10px] uppercase tracking-[0.14em] text-amber-200/60">
                    {t.level} · {t.steps.length} gates
                  </p>
                  <h4 className="mt-1 text-lg leading-tight text-amber-100">{t.title}</h4>
                  <p className="soft mt-1.5 line-clamp-2 text-sm leading-relaxed">{t.focus}</p>
                </div>
                <span className="mt-1 hidden shrink-0 font-sans text-[11px] uppercase tracking-[0.12em] text-stone-400 sm:block">
                  {pathAgg.done}/{pathAgg.total}
                </span>
              </div>
              <div className="mt-3 flex items-center justify-between gap-3">
                <StatePill agg={pathAgg} next={isNext} start={isStart} />
                <span className="font-sans text-[11px] uppercase tracking-[0.14em] text-amber-200/70 transition group-hover:text-amber-100">
                  See gates →
                </span>
              </div>
            </BranchNode>
          );
        })}
      </ul>
    </div>
  );
}

function GateView({
  track,
  progress,
  onOpenGate,
  onOpenFullPath,
}: {
  track: LearningTrack;
  progress: ProgressMap;
  onOpenGate: (stepId: string) => void;
  onOpenFullPath: () => void;
}) {
  const done = trackDone(track, progress);
  const agg = aggregate(done, track.steps.length);
  const nextIndex = track.steps.findIndex((s) => !progress[stepKey(track.id, s.id)]);
  const activeIndex = nextIndex === -1 ? -1 : nextIndex;

  return (
    <div>
      <div className="rounded-2xl border border-amber-200/20 bg-amber-100/[0.04] p-4 sm:p-5">
        <div className="flex items-start gap-4">
          <ProgressRing pct={agg.pct} complete={agg.complete}>
            {agg.complete ? "✓" : `${agg.pct}%`}
          </ProgressRing>
          <div className="min-w-0 flex-1">
            <p className="eyebrow">Path · {track.level}</p>
            <h3 className="mt-1 text-2xl leading-tight text-amber-100">{track.title}</h3>
            <p className="soft mt-1 line-clamp-2 text-sm leading-relaxed">{track.focus}</p>
          </div>
        </div>
        <div className="mt-4 flex flex-wrap items-center justify-between gap-3">
          <span className="font-sans text-[11px] uppercase tracking-[0.14em] text-stone-400">
            {agg.done}/{agg.total} gates · {track.estimatedSessions}
          </span>
          <button
            type="button"
            onClick={onOpenFullPath}
            className="rounded-full border border-amber-200/40 bg-amber-200/10 px-4 py-1.5 font-sans text-[11px] uppercase tracking-[0.14em] text-amber-100 transition hover:border-amber-200/60"
          >
            Open full path ↓
          </button>
        </div>
      </div>

      <p className="mt-6 mb-3 font-sans text-[11px] uppercase tracking-[0.18em] text-amber-200/50">
        Gates descend in order — tap one to study it
      </p>
      <ul className="list-none">
        {track.steps.map((s, i) => {
          const gateDone = !!progress[stepKey(track.id, s.id)];
          const isCurrent = i === activeIndex;
          return (
            <BranchNode
              key={s.id}
              index={i}
              count={track.steps.length}
              highlight={isCurrent}
              onClick={() => onOpenGate(s.id)}
              ariaLabel={`Open gate ${i + 1}: ${s.title}.${gateDone ? " Complete." : ""}`}
              medallion={
                <SpandaMedallion
                  glyph={unitSumiGlyph(s.id)}
                  state={gateDone ? "recognized" : isCurrent ? "arising" : "unmanifest"}
                  size="md"
                />
              }
            >
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  <p className="font-sans text-[10px] uppercase tracking-[0.14em] text-amber-200/60">
                    Gate {i + 1}
                    {isCurrent ? " · next up" : gateDone ? " · complete" : ""}
                  </p>
                  <h4 className="mt-1 text-lg leading-tight text-stone-100">{s.title}</h4>
                  <p className="soft mt-1.5 line-clamp-2 text-sm leading-relaxed">{s.orientation}</p>
                </div>
                <span className="mt-1 shrink-0 font-sans text-[11px] uppercase tracking-[0.14em] text-amber-200/70 transition group-hover:text-amber-100">
                  Study →
                </span>
              </div>
            </BranchNode>
          );
        })}
      </ul>
    </div>
  );
}
