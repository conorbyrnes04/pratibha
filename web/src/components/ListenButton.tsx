"use client";

import { useAuthToken, useConvexAuth } from "@convex-dev/auth/react";
import { useEffect, useState } from "react";
import { useAuth } from "@/components/AuthProvider";
import { SpandaMedallion, type InkState } from "@/components/InkGlyph";
import { listenConfigured, type ListenSection } from "@/lib/api";
import {
  listenSnapshot,
  reportListenError,
  stopListen,
  subscribeListen,
  toggleListen,
  type ListenPhase,
  type ListenSnap,
} from "@/lib/listenSession";

async function resolveListenToken(
  snapshot: string | null | undefined,
  fetchAccessToken?: (args: { forceRefreshToken: boolean }) => Promise<string | null | undefined>,
): Promise<string | null> {
  if (snapshot) return snapshot;
  if (!fetchAccessToken) return null;
  const current = await fetchAccessToken({ forceRefreshToken: false });
  if (current) return current;
  const refreshed = await fetchAccessToken({ forceRefreshToken: true });
  return refreshed || null;
}

function SumiPlayMark({ phase, size }: { phase: ListenPhase; size: "xs" | "sm" }) {
  const state: InkState = phase === "playing" ? "recognized" : "arising";
  return (
    <span className={`sumi-play sumi-play--${phase}`} aria-hidden>
      <SpandaMedallion glyph="triangle" state={state} size={size} mask />
    </span>
  );
}

export function ListenButton({
  verseId,
  section = "all",
  variant = "toolbar",
}: {
  verseId: string;
  section?: ListenSection;
  variant?: "toolbar" | "layer";
}) {
  const { user, configured, loading: authLoading } = useAuth();
  const accessToken = useAuthToken();
  const convexAuth = useConvexAuth();
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
  const caption =
    phase === "loading"
      ? "Preparing"
      : phase === "playing"
        ? "Pause"
        : phase === "paused"
          ? "Resume"
          : section === "all"
            ? "Play all"
            : "Listen";
  const shell =
    variant === "layer"
      ? "passage-listen passage-listen--layer"
      : "passage-listen passage-listen--toolbar";

  async function onPlay() {
    if (phase === "loading") return;
    if (configured && !user && !authLoading) {
      reportListenError(verseId, section, "Sign in to listen.");
      return;
    }
    const token = await resolveListenToken(accessToken, convexAuth?.fetchAccessToken);
    if (configured && user && !token) {
      reportListenError(verseId, section, "Your session is still opening. Try again in a moment.");
      return;
    }
    await toggleListen({
      verseId,
      section,
      accessToken: token,
      signedIn: Boolean(user),
    });
  }

  return (
    <div className={shell}>
      <button
        type="button"
        className="passage-listen__btn"
        onClick={() => void onPlay()}
        disabled={phase === "loading"}
        aria-pressed={phase === "playing"}
        aria-label={caption}
        title={caption}
      >
        <SumiPlayMark phase={phase} size={variant === "layer" ? "xs" : "sm"} />
        <span className="passage-listen__caption">{caption}</span>
      </button>
      {error ? <p className="passage-listen__error">{error}</p> : null}
    </div>
  );
}
