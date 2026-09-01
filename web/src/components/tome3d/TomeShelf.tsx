"use client";

import dynamic from "next/dynamic";
import { useEffect, useRef, useState, type PointerEvent as ReactPointerEvent } from "react";
import type { LibraryTome } from "@/lib/libraryTomes";
import type { TomeShelfProps } from "./types";
import { useT } from "@/components/LocaleProvider";

const TomeShelfCanvas = dynamic(
  () => import("./TomeShelfCanvas").then((m) => m.TomeShelfCanvas),
  {
    ssr: false,
    loading: () => <TomeShelfLoading />,
  },
);

function TomeShelfLoading() {
  const t = useT();
  return (
    <div className="tome-shelf-3d__loading" aria-hidden>
      <p className="soft font-sans text-sm">{t("library.settingShelf")}</p>
    </div>
  );
}

function indexFromPointerY(
  clientY: number,
  rail: HTMLElement,
  count: number,
): number {
  if (count <= 1) return 0;
  const rect = rail.getBoundingClientRect();
  const t = (clientY - rect.top) / Math.max(1, rect.height);
  return Math.round(Math.min(1, Math.max(0, t)) * (count - 1));
}

export function TomeShelf({ tomes, onOpen, className }: TomeShelfProps) {
  const t = useT();
  const rootRef = useRef<HTMLDivElement>(null);
  const railRef = useRef<HTMLElement>(null);
  const scrubIndexRef = useRef<number | null>(null);
  const [wheelTarget, setWheelTarget] = useState<HTMLElement | null>(null);
  const [focus, setFocus] = useState<LibraryTome | null>(tomes[0] ?? null);
  const [focusIndex, setFocusIndex] = useState(0);
  const [railHot, setRailHot] = useState(false);
  const [opening, setOpening] = useState(false);

  useEffect(() => {
    setWheelTarget(rootRef.current);
  }, []);

  function scrubTo(clientY: number) {
    if (opening) return;
    const rail = railRef.current;
    if (!rail || tomes.length === 0) return;
    const i = indexFromPointerY(clientY, rail, tomes.length);
    scrubIndexRef.current = i;
    const tome = tomes[i];
    if (tome) {
      setFocusIndex(i);
      setFocus(tome);
    }
  }

  if (tomes.length === 0) return null;

  return (
    <div
      ref={rootRef}
      className={[
        "tome-shelf-3d",
        opening ? "tome-shelf-3d--opening" : "",
        className,
      ]
        .filter(Boolean)
        .join(" ")}
    >
      <nav
        ref={railRef}
        className={railHot ? "tome-shelf-3d__rail is-hot" : "tome-shelf-3d__rail"}
        aria-label={t("library.browseTexts")}
        onPointerEnter={(e: ReactPointerEvent<HTMLElement>) => {
          if (opening) return;
          setRailHot(true);
          scrubTo(e.clientY);
        }}
        onPointerMove={(e: ReactPointerEvent<HTMLElement>) => scrubTo(e.clientY)}
        onPointerLeave={() => {
          setRailHot(false);
          scrubIndexRef.current = null;
        }}
      >
        <ul className="tome-shelf-3d__ticks">
          {tomes.map((tome, i) => {
            const active = i === focusIndex;
            return (
              <li key={tome.collection} className="tome-shelf-3d__tick-row">
                <button
                  type="button"
                  className={
                    active ? "tome-shelf-3d__tick is-active" : "tome-shelf-3d__tick"
                  }
                  aria-current={active ? "true" : undefined}
                  aria-label={t("library.byAuthor", { title: tome.displayName, author: tome.author })}
                  title={tome.displayName}
                  disabled={opening}
                  onClick={() => {
                    scrubIndexRef.current = i;
                    setFocusIndex(i);
                    setFocus(tome);
                    requestAnimationFrame(() => {
                      if (!railHot) scrubIndexRef.current = null;
                    });
                  }}
                />
                {active ? (
                  <span className="tome-shelf-3d__tick-label" aria-hidden>
                    {tome.displayName}
                  </span>
                ) : null}
              </li>
            );
          })}
        </ul>
      </nav>

      <TomeShelfCanvas
        tomes={tomes}
        onOpen={onOpen}
        wheelTarget={wheelTarget}
        scrubIndexRef={scrubIndexRef}
        onOpeningChange={setOpening}
        onFocusChange={(tome, index) => {
          if (scrubIndexRef.current !== null || opening) return;
          setFocus(tome);
          setFocusIndex(index);
        }}
      />

      {focus && !opening ? (
        <div className="tome-shelf-3d__caption">
          <p className="tome-shelf-3d__caption-title">{focus.displayName}</p>
          <p className="tome-shelf-3d__caption-meta">
            {focus.author}
            <span aria-hidden> · </span>
            {focus.tradition}
          </p>
        </div>
      ) : null}

      <ul className="tome-shelf-3d__a11y">
        {tomes.map((tome) => (
          <li key={tome.collection}>
            <button type="button" onClick={() => onOpen(tome.collection)}>
              {tome.displayName}
              <span>
                {tome.author} · {tome.tradition} · {tome.count}{" "}
                {tome.count === 1 ? t("library.passageOne") : t("library.passageMany")}
              </span>
            </button>
          </li>
        ))}
      </ul>

      <p className="tome-shelf-3d__hint soft font-sans text-xs">
        {opening ? t("common.opening") : t("library.slideTicks")}
      </p>
    </div>
  );
}
