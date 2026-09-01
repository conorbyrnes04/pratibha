"use client";

import { LEARNING_REALMS, RECOMMENDED_SPINE, type LearningTrack } from "@/lib/learningPaths";
import { realmImageSrc } from "@/lib/collectionImages";
import { ArtBackdrop } from "@/components/ArtImage";
import { YantraBreath } from "./YantraBreath";
import { useT } from "@/components/LocaleProvider";

type ProgressMap = Record<string, boolean>;

function stepKey(trackId: string, stepId: string): string {
  return `${trackId}:${stepId}`;
}

function trackDone(t: LearningTrack, progress: ProgressMap): number {
  return t.steps.filter((s) => progress[stepKey(t.id, s.id)]).length;
}

/** Ring radius (% of mandala half-size) by spine index. */
function nodeRadiusPct(spineIndex: number): number {
  if (spineIndex <= 1) return 26;
  if (spineIndex <= 5) return 42;
  return 56;
}

function nodePosition(spineIndex: number, total: number): { x: number; y: number } {
  const angle = ((spineIndex / total) * 360 - 90) * (Math.PI / 180);
  const r = nodeRadiusPct(spineIndex);
  return {
    x: 50 + Math.cos(angle) * r,
    y: 50 + Math.sin(angle) * r,
  };
}

type PathNodeState = {
  track: LearningTrack;
  spineIndex: number;
  done: number;
  total: number;
  complete: boolean;
  isNext: boolean;
  isStart: boolean;
  selected: boolean;
  num: number;
  x: number;
  y: number;
};

type JourneyMandalaProps = {
  trackById: Record<string, LearningTrack>;
  progress: ProgressMap;
  hydrated: boolean;
  selectedTrackId: string;
  recommendedNextId: string;
  anyProgress: boolean;
  onSelectTrack: (trackId: string) => void;
};

function PathNodeButton({
  node,
  onSelect,
}: {
  node: PathNodeState;
  onSelect: (id: string) => void;
}) {
  const t = useT();
  const pct = Math.round((node.done / Math.max(1, node.total)) * 100);
  return (
    <button
      type="button"
      onClick={() => onSelect(node.track.id)}
      aria-pressed={node.selected}
      className={`path-node group absolute z-10 flex -translate-x-1/2 -translate-y-1/2 flex-col items-center text-left transition duration-300 ${
        node.selected ? "path-node--active" : ""
      } ${node.complete ? "path-node--complete" : ""}`}
      style={{ left: `${node.x}%`, top: `${node.y}%` }}
      aria-label={`${node.track.title} — ${node.track.level}. ${t("learn.stepsCount", { done: node.done, total: node.total })}`}
    >
      <span
        className={`path-node__medallion mx-auto flex h-11 w-11 items-center justify-center rounded-full border-2 font-sans text-xs font-bold sm:h-14 sm:w-14 sm:text-sm ${
          node.complete
            ? "border-emerald-300/80 bg-emerald-300/90 text-slate-950"
            : node.isNext || node.isStart
              ? "border-amber-200 bg-amber-200/95 text-slate-950"
              : node.selected
                ? "border-amber-200/70 bg-amber-100/20 text-amber-100"
                : "border-amber-200/25 bg-[#0b0b14]/80 text-amber-100/90"
        }`}
      >
        {node.complete ? "✓" : node.num}
      </span>
      {/* Hover-only detail card — floats above the gate so the pointer stays in the hover zone */}
      <div className="path-node__card absolute bottom-[calc(100%+0.5rem)] left-1/2 z-20 w-48 -translate-x-1/2 rounded-2xl border border-amber-200/35 bg-[#0b0b14]/95 p-3.5 shadow-[0_12px_40px_rgb(0_0_0_/_0.45)] backdrop-blur-md sm:w-52">
        <p className="text-sm font-semibold leading-tight text-amber-50">{node.track.title}</p>
        <p className="mt-1 font-sans text-[10px] uppercase tracking-[0.14em] text-amber-200/60">{node.track.level}</p>
        <p className="soft mt-2 line-clamp-3 text-xs leading-relaxed">{node.track.focus}</p>
        <div className="mt-2.5 h-1 rounded-full bg-white/10">
          <div className="h-1 rounded-full bg-amber-300/80 transition-all" style={{ width: `${pct}%` }} />
        </div>
        <p className="mt-2 font-sans text-[10px] uppercase tracking-[0.12em] text-stone-400">
          {node.complete ? (
            <span className="text-emerald-300/90">{t("common.complete")} ✓</span>
          ) : node.isNext ? (
            <span className="text-amber-200/90">{t("learn.recommendedNext")}</span>
          ) : node.isStart ? (
            <span className="text-amber-200/90">{t("learn.startHere")}</span>
          ) : node.done > 0 ? (
            <span className="text-amber-200/70">{t("learn.inProgress", { done: node.done, total: node.total })}</span>
          ) : (
            t("learn.stepsCount", { done: node.done, total: node.total })
          )}
        </p>
        <span className="mt-2.5 block font-sans text-[10px] font-bold uppercase tracking-[0.14em] text-amber-200/80">
          {t("learn.openPath")}
        </span>
      </div>
    </button>
  );
}

export function JourneyMandala({
  trackById,
  progress,
  hydrated,
  selectedTrackId,
  recommendedNextId,
  anyProgress,
  onSelectTrack,
}: JourneyMandalaProps) {
  const t = useT();
  const safeProgress = hydrated ? progress : {};
  const nodes: PathNodeState[] = RECOMMENDED_SPINE.map((tid, spineIndex) => {
    const track = trackById[tid];
    if (!track) return null;
    const done = trackDone(track, safeProgress);
    const total = track.steps.length;
    const pos = nodePosition(spineIndex, RECOMMENDED_SPINE.length);
    return {
      track,
      spineIndex,
      done,
      total,
      complete: total > 0 && done === total,
      isNext: tid === recommendedNextId && done < total,
      isStart: !anyProgress && tid === RECOMMENDED_SPINE[0],
      selected: selectedTrackId === tid,
      num: spineIndex + 1,
      x: pos.x,
      y: pos.y,
    };
  }).filter((n): n is PathNodeState => Boolean(n));

  const spinePath = nodes
    .map((n) => `${n.x},${n.y}`)
    .join(" ");

  return (
    <section className="journey-mandala mt-14">
      <p className="eyebrow">{t("learn.journey")}</p>
      <p className="soft mt-2 max-w-2xl text-base leading-relaxed">{t("learn.journeyLede")}</p>

      {/* Desktop: radial mandala */}
      <div className="relative mx-auto mt-8 hidden aspect-square w-full max-w-3xl overflow-visible md:block">
        <YantraBreath className="absolute inset-0 h-full w-full opacity-90" />
        <svg className="absolute inset-0 h-full w-full" viewBox="0 0 100 100" aria-hidden preserveAspectRatio="none">
          <polyline
            points={spinePath}
            fill="none"
            stroke="rgb(240 201 121 / 0.22)"
            strokeWidth="0.35"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="journey-spine-line"
          />
          {nodes.map((n) => (
            <line
              key={`spoke-${n.track.id}`}
              x1="50"
              y1="50"
              x2={n.x}
              y2={n.y}
              stroke="rgb(240 201 121 / 0.06)"
              strokeWidth="0.2"
            />
          ))}
        </svg>
        <div className="absolute inset-0">
          {nodes.map((n) => (
            <PathNodeButton key={n.track.id} node={n} onSelect={onSelectTrack} />
          ))}
        </div>
        <p className="absolute bottom-0 left-1/2 -translate-x-1/2 font-sans text-[10px] uppercase tracking-[0.2em] text-amber-200/40">
          Bindu · the heart of the path
        </p>
      </div>

      {/* Mobile: realm arcs with tradition artwork behind each */}
      <div className="mt-8 space-y-10 md:hidden">
        {LEARNING_REALMS.map((realm) => (
          <div key={realm.id} className="realm-arc relative overflow-hidden rounded-3xl border border-amber-200/10 p-5">
            <ArtBackdrop src={realmImageSrc(realm.id)} variant="subtle" position="center 30%" />
            <YantraBreath className="absolute -right-16 -top-16 h-48 w-48 opacity-40" />
            <p className="relative z-10 eyebrow">{realm.title}</p>
            <p className="relative z-10 soft mt-2 text-sm leading-relaxed">{realm.blurb}</p>
            <div className="relative z-10 mt-5 space-y-3">
              {realm.trackIds.map((tid) => {
                const t = trackById[tid];
                if (!t) return null;
                const done = trackDone(t, safeProgress);
                const total = t.steps.length;
                const complete = total > 0 && done === total;
                const spineN = RECOMMENDED_SPINE.indexOf(tid);
                const isNext = t.id === recommendedNextId && !complete;
                const isStart = !anyProgress && t.id === RECOMMENDED_SPINE[0];
                const selected = selectedTrackId === t.id;
                const pct = Math.round((done / Math.max(1, total)) * 100);
                return (
                  <button
                    key={t.id}
                    type="button"
                    onClick={() => onSelectTrack(t.id)}
                    aria-pressed={selected}
                    className={`card relative w-full p-4 text-left transition ${
                      selected ? "border-amber-200/60 bg-amber-100/10" : ""
                    }`}
                  >
                    <div className="flex items-start gap-3">
                      <span
                        className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-full border-2 font-sans text-sm font-bold ${
                          complete
                            ? "border-emerald-300 bg-emerald-300 text-slate-950"
                            : isNext || isStart
                              ? "border-amber-200 bg-amber-200 text-slate-950"
                              : "border-amber-200/30 bg-[#0b0b14] text-amber-100"
                        }`}
                      >
                        {complete ? "✓" : spineN >= 0 ? spineN + 1 : "•"}
                      </span>
                      <div className="min-w-0 flex-1">
                        <h3 className="text-xl leading-tight text-amber-100">{t.title}</h3>
                        <p className="soft mt-1 text-sm">{t.focus}</p>
                        <div className="mt-3 h-1.5 rounded-full bg-white/10">
                          <div className="h-1.5 rounded-full bg-amber-300" style={{ width: `${pct}%` }} />
                        </div>
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
