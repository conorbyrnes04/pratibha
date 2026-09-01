"use client";

import { useLayoutEffect, useMemo, useRef, useState } from "react";
import { InkGlyph } from "@/components/InkGlyph";
import { GlyphInkDraw } from "@/components/GlyphInkDraw";
import { TraditionMandala } from "@/components/learn/TraditionMandala";
import { TrailSandLine, type TrailSandMark } from "@/components/learn/TrailSandLine";
import { buildTrail, currentTrailSit, TRAIL_SAND_DRAW_MS } from "@/lib/learn/trail";
import { findTraditionTrail, TRADITION_TRAILS } from "@/lib/learn/traditionTrails";
import { type CompletedAtMap, type ProgressMap } from "@/lib/learn/progress";
import { SHARE_INKS } from "@/lib/shareCard";
import { trailSumiGlyph } from "@/lib/sumiGlyphs";
import { loadSumiTrace } from "@/lib/sumiTrace";
import { useT } from "@/components/LocaleProvider";
import { useLocalizedFields, useLocalizedTrails } from "@/components/useLocalizedStudy";

type LearnTrailProps = {
  pathId: string;
  progress: ProgressMap;
  completedAt?: CompletedAtMap;
  hydrated: boolean;
  /** Open this gate in its own view. */
  onOpenGate: (trackId: string, stepId: string) => void;
  onBackPaths?: () => void;
  /** Scroll target: the key of the gate we should scroll to. */
  scrollToKey?: string | null;
  /** Freshly unlocked node — paint it on after the sand arrives. */
  drawingKey?: string | null;
  /** Gate just marked complete — wash the mark to gold while the line moves on. */
  finishingKey?: string | null;
  /** Retrigger scroll when the hovering gate unmounts. */
  gateOpen?: boolean;
};

export function LearnTrail({
  pathId,
  progress,
  completedAt,
  hydrated,
  onOpenGate,
  onBackPaths,
  scrollToKey,
  drawingKey,
  finishingKey,
  gateOpen = false,
}: LearnTrailProps) {
  const t = useT();
  const trail = findTraditionTrail(pathId);
  const nodes = buildTrail(trail.id);
  const nodeRefs = useRef<Record<string, HTMLElement | null>>({});
  const markRefs = useRef<Record<string, HTMLElement | null>>({});
  const stageRef = useRef<HTMLDivElement | null>(null);
  const [stage, setStage] = useState({ width: 0, height: 0, marks: [] as TrailSandMark[] });

  const sit = currentTrailSit(progress, pathId, completedAt);
  let currentIndex = nodes.findIndex((n) => !progress[n.key]);
  if (currentIndex === -1) currentIndex = nodes.length - 1;
  const drawIndex = drawingKey ? nodes.findIndex((n) => n.key === drawingKey) : -1;
  const finishIndex = finishingKey ? nodes.findIndex((n) => n.key === finishingKey) : -1;
  const visibleEnd = Math.max(currentIndex, drawIndex, finishIndex, 0);
  const visible = hydrated ? nodes.slice(0, visibleEnd + 1) : nodes.slice(0, 1);
  const rested = Boolean(sit?.rested);
  const tomorrowKey = rested ? sit?.next?.key : null;
  const [inkReady, setInkReady] = useState(false);
  const visibleKey = visible.map((node) => node.key).join("|");
  const trails = useLocalizedTrails(TRADITION_TRAILS);
  const trailCopy = trails.find((item) => item.id === trail.id) || trail;
  const teaserFields = useMemo(() => {
    const fields: Record<string, string> = {};
    visible.forEach((node) => {
      fields[`title:${node.key}`] = node.title;
      fields[`orientation:${node.key}`] = node.orientation;
      fields[`section:${node.trackId}`] = node.sectionLabel;
    });
    return fields;
  }, [visible, visibleKey]);
  const { fields: localizedTeasers } = useLocalizedFields(teaserFields);

  useLayoutEffect(() => {
    if (!drawingKey) {
      setInkReady(false);
      return;
    }
    setInkReady(false);
    const id = window.setTimeout(() => setInkReady(true), TRAIL_SAND_DRAW_MS);
    return () => window.clearTimeout(id);
  }, [drawingKey]);

  useLayoutEffect(() => {
    if (!scrollToKey) return;
    const el = nodeRefs.current[scrollToKey];
    if (el) {
      requestAnimationFrame(() => {
        el.scrollIntoView({ behavior: "smooth", block: "center" });
      });
    }
  }, [scrollToKey, drawingKey, pathId, gateOpen]);

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
  }, [visibleKey, drawingKey, finishingKey, hydrated]);

  useLayoutEffect(() => {
    if (!drawingKey) return;
    const node = buildTrail(trail.id).find((item) => item.key === drawingKey);
    if (node) void loadSumiTrace(trailSumiGlyph(node.stepId), true);
  }, [drawingKey, trail.id]);

  useLayoutEffect(() => {
    if (!finishingKey) return;
    const node = buildTrail(trail.id).find((item) => item.key === finishingKey);
    if (node) void loadSumiTrace(trailSumiGlyph(node.stepId), true);
  }, [finishingKey, trail.id]);

  return (
    <div className="section-stack">
      <div>
        <header className="library-header">
          <div className="library-header__body">
            {onBackPaths ? (
              <button
                type="button"
                onClick={onBackPaths}
                className="learn-trail__all-paths"
              >
                {t("learn.backPaths")}
              </button>
            ) : (
              <p className="passage-reading__meta">{t("learn.guided")}</p>
            )}
            <h1 className="library-header__title">{trailCopy.title}</h1>
            <p className="library-header__lede">
              {trail.essential
                ? t("learn.essentialLede")
                : trailCopy.lede}
            </p>
          </div>
        </header>

        <TraditionMandala
          trail={trailCopy}
          nodes={nodes}
          progress={hydrated ? progress : {}}
          currentIndex={hydrated ? currentIndex : 0}
          tomorrowKey={hydrated ? tomorrowKey : null}
          drawingKey={drawingKey}
          finishingKey={finishingKey}
          onOpenGate={onOpenGate}
        />
      </div>

      {rested && sit?.next ? (
        <div className="learn-trail__rest">
          <p className="passage-reading__meta">{t("learn.walkedToday")}</p>
          <p className="library-header__lede">
            {t("learn.enoughTomorrow", {
              title: localizedTeasers[`title:${sit.next.key}`] || sit.next.title,
            })}
          </p>
        </div>
      ) : null}

      <section className="learn-trail pb-16">
        <div
          ref={stageRef}
          className="learn-trail__stage"
          style={{ ["--trail-sand-ms" as string]: `${TRAIL_SAND_DRAW_MS}ms` }}
        >
          <TrailSandLine
            marks={stage.marks}
            width={stage.width}
            height={stage.height}
            drawingKey={drawingKey}
          />

          <ul className="learn-trail__nodes">
            {visible.map((node, i) => {
              const done = !!progress[node.key];
              const arriving = drawingKey === node.key;
              const finishing = finishingKey === node.key;
              const isTomorrow = Boolean(tomorrowKey && node.key === tomorrowKey && !done && !arriving);
              const isCurrent = i === currentIndex && !done && !isTomorrow && !arriving;
              const glyph = trailSumiGlyph(node.stepId);
              let state: "recognized" | "arising" | "unmanifest" = "unmanifest";
              if (done && !finishing) state = "recognized";
              else if (isCurrent || arriving || finishing || isTomorrow) state = "arising";
              const playInk = (arriving && inkReady) || finishing;

              return (
                <li
                  key={node.key}
                  ref={(el) => {
                    nodeRefs.current[node.key] = el;
                  }}
                  className="learn-trail__node"
                >
                  {node.isFirstInSection ? (
                    <div className="learn-trail__section">
                      <p className="learn-trail__section-label">
                        {localizedTeasers[`section:${node.trackId}`] || node.sectionLabel}
                      </p>
                    </div>
                  ) : null}

                  <button
                    type="button"
                    onClick={() => onOpenGate(node.trackId, node.stepId)}
                    className={`learn-trail__gate ${
                      isCurrent || arriving ? "learn-trail__gate--current" : ""
                    }`}
                    aria-label={
                      done
                        ? t("learn.nodeComplete", { title: localizedTeasers[`title:${node.key}`] || node.title })
                        : isTomorrow
                          ? t("learn.nodeTomorrow", { title: localizedTeasers[`title:${node.key}`] || node.title })
                          : isCurrent || arriving
                            ? t("learn.nodeCurrent", { title: localizedTeasers[`title:${node.key}`] || node.title })
                            : localizedTeasers[`title:${node.key}`] || node.title
                    }
                    data-trail-node={node.key}
                    data-trail-arriving={arriving ? "true" : undefined}
                    data-trail-finishing={finishing ? "true" : undefined}
                  >
                    <div
                      ref={(el) => {
                        markRefs.current[node.key] = el;
                      }}
                      className={`learn-trail__mark ${
                        isCurrent || arriving || finishing ? "learn-trail__mark--current" : ""
                      } ${arriving || finishing ? "learn-trail__mark--arrive" : ""}`}
                    >
                      {playInk ? (
                        <GlyphInkDraw
                          key={`${arriving ? "arrive" : "finish"}-${node.key}`}
                          slug={glyph}
                          ink={SHARE_INKS.gold.hex}
                          tight
                          className="learn-trail__glyph"
                        />
                      ) : (
                        <InkGlyph
                          glyph={glyph}
                          state={state}
                          size={isCurrent || arriving || finishing ? "xl" : "lg"}
                          className="learn-trail__glyph"
                          mask
                        />
                      )}
                    </div>

                    <div
                      className={`learn-trail__copy ${
                        arriving ? "learn-trail__copy--await" : ""
                      }`}
                    >
                      <h3
                        className={`learn-trail__title ${
                          done
                            ? "learn-trail__title--done"
                            : isCurrent || arriving
                              ? "learn-trail__title--current"
                              : "learn-trail__title--quiet"
                        }`}
                      >
                        {localizedTeasers[`title:${node.key}`] || node.title}
                      </h3>
                      {isCurrent || arriving || isTomorrow || finishing ? (
                        <p className="learn-trail__orientation">
                          {(localizedTeasers[`orientation:${node.key}`] || node.orientation).split(".")[0]}.
                        </p>
                      ) : null}
                    </div>

                    {done && !finishing && !arriving ? (
                      <span className="learn-trail__badge learn-trail__badge--done">
                        {t("common.complete")}
                      </span>
                    ) : isTomorrow ? (
                      <span className="learn-trail__badge">
                        {t("common.tomorrow")}
                      </span>
                    ) : null}
                  </button>
                </li>
              );
            })}
          </ul>
        </div>

        {currentIndex >= 0 && currentIndex < nodes.length ? (
          <div className="learn-trail__progress">
            <p>
              {rested && sit?.next
                ? t("gate.walkedTodayTomorrow", {
                    title: localizedTeasers[`title:${sit.next.key}`] || sit.next.title,
                  })
                : currentIndex === 0
                  ? t("learn.beginJourney")
                  : currentIndex < nodes.length - 1
                    ? t("gate.progress", {
                        walked: currentIndex,
                        walkedLabel:
                          currentIndex === 1 ? t("gate.gateOne") : t("gate.gateMany"),
                        remain: nodes.length - currentIndex,
                        remainLabel:
                          nodes.length - currentIndex === 1
                            ? t("gate.remainOne")
                            : t("gate.remainMany"),
                      })
                    : t("learn.pathComplete")}
            </p>
          </div>
        ) : null}
      </section>
    </div>
  );
}
