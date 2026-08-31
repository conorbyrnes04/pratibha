"use client";

import { useAuthToken } from "@convex-dev/auth/react";
import { useEffect, useState } from "react";
import { listenConfigured, type ListenSection } from "@/lib/api";
import {
  listenSnapshot,
  stopListen,
  subscribeListen,
  toggleListen,
  type ListenSnap,
} from "@/lib/listenSession";

export function ListenButton({
  verseId,
  section = "all",
  variant = "toolbar",
}: {
  verseId: string;
  section?: ListenSection;
  variant?: "toolbar" | "layer";
}) {
  const accessToken = useAuthToken();
  const [available, setAvailable] = useState(false);
  const [snap, setSnap] = useState<ListenSnap>(listenSnapshot);

  useEffect(() => {
    let cancelled = false;
    listenConfigured().then((ok) => {
      if (!cancelled) setAvailable(ok);
    });
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => subscribeListen(() => setSnap(listenSnapshot())), []);

  useEffect(() => {
    if (section !== "all") return;
    return () => stopListen();
  }, [verseId, section]);

  if (!available) return null;

  const mine = snap.verseId === verseId && snap.section === section;
  const phase = mine ? snap.phase : "idle";
  const error = mine ? snap.error : null;
  const label =
    phase === "loading"
      ? "Preparing…"
      : phase === "playing"
        ? "Pause"
        : phase === "paused"
          ? "Resume"
          : section === "all"
            ? "Play all"
            : "Listen";

  return (
    <div className={variant === "layer" ? "passage-listen passage-listen--layer" : "passage-listen"}>
      <button
        type="button"
        className="passage-reading__toggle"
        onClick={(event) => {
          event.preventDefault();
          event.stopPropagation();
          void toggleListen({ verseId, section, accessToken });
        }}
        disabled={phase === "loading"}
        aria-pressed={phase === "playing"}
      >
        {label}
      </button>
      {error ? <p className="passage-listen__error">{error}</p> : null}
    </div>
  );
}
