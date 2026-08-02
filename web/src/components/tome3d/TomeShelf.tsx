"use client";

import dynamic from "next/dynamic";
import type { TomeShelfProps } from "./types";

const TomeShelfCanvas = dynamic(
  () => import("./TomeShelfCanvas").then((m) => m.TomeShelfCanvas),
  {
    ssr: false,
    loading: () => (
      <div className="tome-shelf-3d__loading" aria-hidden>
        <p className="soft font-sans text-sm">Setting the shelf…</p>
      </div>
    ),
  },
);

export function TomeShelf({ tomes, onOpen, className }: TomeShelfProps) {
  if (tomes.length === 0) return null;

  return (
    <div className={["tome-shelf-3d", className].filter(Boolean).join(" ")}>
      <TomeShelfCanvas tomes={tomes} onOpen={onOpen} />

      {/* Keyboard / SR accessible twin of the 3D stack */}
      <ul className="tome-shelf-3d__a11y">
        {tomes.map((tome) => (
          <li key={tome.collection}>
            <button type="button" onClick={() => onOpen(tome.collection)}>
              {tome.displayName}
              <span>
                {tome.author} · {tome.tradition} · {tome.count}{" "}
                {tome.count === 1 ? "passage" : "passages"}
              </span>
            </button>
          </li>
        ))}
      </ul>

      <p className="tome-shelf-3d__hint soft font-sans text-xs">
        Scroll to browse · hover to lift · click to open
      </p>
    </div>
  );
}
