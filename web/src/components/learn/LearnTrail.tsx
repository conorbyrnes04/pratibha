"use client";

import { useLayoutEffect, useRef, useState } from "react";
import { InkGlyph } from "@/components/InkGlyph";
import { TrailSandLine, type TrailSandMark } from "@/components/learn/TrailSandLine";
import { buildTrail, currentTrailSit, TRAIL_SAND_DRAW_MS } from "@/lib/learn/trail";
import { findTraditionTrail, TRADITION_TRAILS } from "@/lib/learn/traditionTrails";
import { type CompletedAtMap, type ProgressMap } from "@/lib/learn/progress";
import { trailSumiGlyph } from "@/lib/sumiGlyphs";

type LearnTrailProps = {
  pathId: string;
  progress: ProgressMap;
  completedAt?: CompletedAtMap;
  hydrated: boolean;
  /** Open this gate in its own view. */
  onOpenGate: (trackId: string, stepId: string) => void;
  onSelectPath: (pathId: string) => void;
  onBackPaths?: () => void;
  /** Scroll target: the key of the gate we should scroll to. */
  scrollToKey?: string | null;
  /** Freshly unlocked node — paint it on. */
  drawingKey?: string | null;
};

function hashSeed(value: string): number {
  let h = 2166136261;
  for (let i = 0; i < value.length; i++) {
    h ^= value.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

export function LearnTrail({
  pathId,
  progress,
  completedAt,
  hydrated,
  onOpenGate,
  onSelectPath,
  onBackPaths,
  scrollToKey,
  drawingKey,
}: LearnTrailProps) {
  const trail = findTraditionTrail(pathId);
  const nodes = buildTrail(trail.id);
  const nodeRefs = useRef<Record<string, HTMLElement | null>>({});
  const markRefs = useRef<Record<string, HTMLElement | null>>({});
  const stageRef = useRef<HTMLDivElement | null>(null);
  const [stage, setStage] = useState({ width: 0, height: 0, marks: [] as TrailSandMark[] });

  const sit = currentTrailSit(progress, pathId, completedAt);
  let currentIndex = nodes.findIndex((n) => !progress[n.key]);
  if (currentIndex === -1) currentIndex = nodes.length - 1;
  const visible = hydrated ? nodes.slice(0, currentIndex + 1) : nodes.slice(0, 1);
  const rested = Boolean(sit?.rested);
  const tomorrowKey = rested ? sit?.next?.key : null;
  const visibleKey = visible.map((node) => node.key).join("|");

  useLayoutEffect(() => {
    if (!scrollToKey) return;
    const el = nodeRefs.current[scrollToKey];
    if (el) {
      requestAnimationFrame(() => {
        el.scrollIntoView({ behavior: "smooth", block: "center" });
      });
    }
  }, [scrollToKey, drawingKey, pathId]);

  useLayoutEffect(() => {
    const root = stageRef.current;
    if (!root) return;

    const measure = () => {
      const box = root.getBoundingClientRect();
      const marks: TrailSandMark[] = [];
      for (const node of visible) {
        const el = markRefs.current[node.key];
        if (!el) continue;
        const r = el.getBoundingClientRect();
        marks.push({
          key: node.key,
          x: r.left + r.width / 2 - box.left,
          y: r.top + r.height / 2 - box.top,
          top: r.top - box.top,
          bottom: r.bottom - box.top,
        });
      }
      setStage({ width: box.width, height: box.height, marks });
    };

    measure();
    const ro = new ResizeObserver(() => measure());
    ro.observe(root);
    for (const key of visibleKey.split("|")) {
      const el = markRefs.current[key];
      if (el) ro.observe(el);
    }
    window.addEventListener("resize", measure);
    const again = window.setTimeout(measure, 80);
    return () => {
      ro.disconnect();
      window.removeEventListener("resize", measure);
      window.clearTimeout(again);
    };
  }, [visibleKey, drawingKey, hydrated]);

  return (
    <div className="section-stack">
      <header className="library-header">
        <div className="library-header__body">
          <div className="learn-trail__path-row">
            {onBackPaths ? (
              <button
                type="button"
                onClick={onBackPaths}
                className="font-sans text-[10px] uppercase tracking-[0.16em] text-amber-200/55 hover:text-amber-100"
              >
                ← Paths
              </button>
            ) : (
              <p className="passage-reading__meta">Guided study</p>
            )}
            <label className="learn-trail__path-select">
              <select
                aria-label="Choose a path"
                value={trail.id}
                onChange={(event) => onSelectPath(event.target.value)}
              >
                <optgroup label="Essential">
                  {TRADITION_TRAILS.filter((option) => option.essential).map((option) => (
                    <option key={option.id} value={option.id}>
                      {option.shortTitle}
                    </option>
                  ))}
                </optgroup>
                <optgroup label="Traditions">
                  {TRADITION_TRAILS.filter((option) => !option.essential).map((option) => (
                    <option key={option.id} value={option.id}>
                      {option.shortTitle}
                    </option>
                  ))}
                </optgroup>
              </select>
            </label>
          </div>
          <h1 className="library-header__title">{trail.title}</h1>
          <p className="library-header__lede">
            {trail.essential
              ? "This is the walk. Today opens one gate. Finish it, and tomorrow names the next node."
              : trail.lede}
          </p>
        </div>
      </header>

      {rested && sit?.next ? (
        <div className="learn-trail__rest">
          <p className="passage-reading__meta">Walked today</p>
          <p className="library-header__lede">
            Enough for today. Tomorrow opens {sit.next.title}.
          </p>
        </div>
      ) : null}

      <section className="learn-trail mt-8 pb-16">
        <div
          ref={stageRef}
          className="learn-trail__stage relative mx-auto max-w-xl"
          style={{ ["--trail-sand-ms" as string]: `${TRAIL_SAND_DRAW_MS}ms` }}
        >
          <TrailSandLine
            marks={stage.marks}
            width={stage.width}
            height={stage.height}
            drawingKey={drawingKey}
          />

          <ul className="relative z-10 list-none space-y-16">
            {visible.map((node, i) => {
              const done = !!progress[node.key];
              const isTomorrow = Boolean(tomorrowKey && node.key === tomorrowKey && !done);
              const isCurrent = i === currentIndex && !done && !isTomorrow;
              const arriving = drawingKey === node.key;
              const glyph = trailSumiGlyph(node.stepId);
              let state: "recognized" | "arising" | "unmanifest" = "unmanifest";
              if (done) state = "recognized";
              else if (isCurrent) state = "arising";
              const side = i % 2;
              const drift = 12 + (Math.abs(hashSeed(node.key)) % 64);

              return (
                <li
                  key={node.key}
                  ref={(el) => {
                    nodeRefs.current[node.key] = el;
                  }}
                  className="relative"
                >
                  {node.isFirstInSection && i > 0 ? (
                    <div className="mb-10 mt-8 text-center">
                      <p className="font-sans text-[11px] uppercase tracking-[0.22em] text-amber-200/45">
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

                  <div
                    className="relative max-w-[240px]"
                    style={
                      side === 0
                        ? { marginRight: "auto", marginLeft: drift }
                        : { marginLeft: "auto", marginRight: drift }
                    }
                  >
                    <button
                      type="button"
                      onClick={() => onOpenGate(node.trackId, node.stepId)}
                      className={`group relative block w-full text-left transition-all duration-300 hover:scale-102 active:scale-[0.98] ${
                        isCurrent ? "scale-[1.02]" : "scale-100"
                      }`}
                      aria-label={
                        done
                          ? `${node.title} - Complete`
                          : isTomorrow
                            ? `${node.title} - Opens tomorrow`
                            : isCurrent
                              ? `${node.title} - Current gate`
                              : node.title
                      }
                    >
                      <div
                        ref={(el) => {
                          markRefs.current[node.key] = el;
                        }}
                        className={`learn-trail__mark mx-auto flex items-center justify-center transition-all duration-500 ${
                          isCurrent || arriving ? "learn-trail__mark--current h-24 w-24" : "h-20 w-20"
                        }`}
                      >
                        <InkGlyph
                          glyph={glyph}
                          state={state}
                          size={isCurrent || arriving ? "xl" : "lg"}
                          className="learn-trail__glyph"
                          mask
                          stroke={arriving}
                          strokeKey={arriving ? drawingKey : undefined}
                          strokeDelay={arriving ? TRAIL_SAND_DRAW_MS : 0}
                        />
                      </div>

                      <div
                        className={`learn-trail__copy mt-4 text-center ${
                          arriving ? "learn-trail__copy--await" : ""
                        }`}
                      >
                        <h3
                          className={`px-2 text-sm font-medium leading-snug transition-colors duration-300 ${
                            done ? "text-emerald-100" : isCurrent ? "text-amber-100" : "text-stone-400"
                          }`}
                        >
                          {node.title}
                        </h3>
                        {isCurrent || arriving || isTomorrow ? (
                          <p className="mt-2 px-3 text-xs leading-relaxed text-stone-400">
                            {node.orientation.split(".")[0]}.
                          </p>
                        ) : null}
                      </div>

                      {done ? (
                        <div className="mt-3 flex justify-center">
                          <span className="rounded-full border border-emerald-300/35 bg-emerald-300/8 px-2.5 py-0.5 font-sans text-[9px] uppercase tracking-[0.14em] text-emerald-200">
                            Complete
                          </span>
                        </div>
                      ) : isTomorrow ? (
                        <div className="mt-3 flex justify-center">
                          <span className="rounded-full border border-amber-200/30 bg-amber-200/6 px-2.5 py-0.5 font-sans text-[9px] uppercase tracking-[0.14em] text-amber-100/80">
                            Tomorrow
                          </span>
                        </div>
                      ) : null}
                    </button>
                  </div>
                </li>
              );
            })}
          </ul>
        </div>

        {currentIndex >= 0 && currentIndex < nodes.length ? (
          <div className="mt-16 text-center">
            <p className="font-sans text-[11px] uppercase tracking-[0.18em] text-stone-500">
              {rested && sit?.next
                ? `Walked today · tomorrow opens ${sit.next.title}`
                : currentIndex === 0
                  ? "Begin the journey"
                  : currentIndex < nodes.length - 1
                    ? `${currentIndex} ${currentIndex === 1 ? "gate" : "gates"} walked · ${nodes.length - currentIndex} ${
                        nodes.length - currentIndex === 1 ? "remains" : "remain"
                      }`
                    : "The path is complete"}
            </p>
          </div>
        ) : null}
      </section>
    </div>
  );
}
