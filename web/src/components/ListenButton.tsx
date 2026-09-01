"use client";

import { useAuthToken, useConvexAuth } from "@convex-dev/auth/react";
import { useEffect, useState, type MouseEvent } from "react";
import { useAuth } from "@/components/AuthProvider";
import { useT } from "@/components/LocaleProvider";
import { InkGlyph, type InkState } from "@/components/InkGlyph";
import { listenConfigured, type ListenSection } from "@/lib/api";
import {
  canListenLocally,
  listenSnapshot,
  reportListenError,
  retainListen,
  subscribeListen,
  toggleListen,
  type ListenPhase,
  type ListenSnap,
} from "@/lib/listenSession";
import type { VerseItem } from "@/lib/types";

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
      <InkGlyph glyph="play" state={state} size={size} mask />
    </span>
  );
}

export function ListenButton({
  verseId,
  section = "all",
  variant = "toolbar",
  verse,
}: {
  verseId: string;
  section?: ListenSection;
  variant?: "toolbar" | "layer" | "header";
  verse?: VerseItem;
}) {
  const t = useT();
  const { user, configured, loading: authLoading } = useAuth();
  const accessToken = useAuthToken();
  const convexAuth = useConvexAuth();
  const [remote, setRemote] = useState(false);
  const [mounted, setMounted] = useState(false);
  const [snap, setSnap] = useState<ListenSnap>(listenSnapshot);

  useEffect(() => {
    setMounted(true);
    let cancelled = false;
    listenConfigured().then((ok) => {
      if (!cancelled) setRemote(ok);
    });
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => subscribeListen(() => setSnap(listenSnapshot())), []);

  useEffect(() => {
    if (section !== "all") return;
    return retainListen();
  }, [verseId, section]);

  const localOk = mounted && canListenLocally();
  if (!mounted || (!remote && !localOk)) return null;

  const mine = snap.verseId === verseId && snap.section === section;
  const phase = mine ? snap.phase : "idle";
  const error = mine ? snap.error : null;
  const caption =
    phase === "loading"
      ? t("listen.preparing")
      : phase === "playing"
        ? t("listen.pause")
        : phase === "paused"
          ? t("listen.resume")
          : section === "all"
            ? t("listen.playAll")
            : t("listen.listen");
  const shell =
    variant === "layer"
      ? "passage-listen passage-listen--layer"
      : variant === "header"
        ? "passage-listen passage-listen--header"
        : "passage-listen passage-listen--toolbar";

  async function onPlay(event: MouseEvent<HTMLButtonElement>) {
    event.preventDefault();
    event.stopPropagation();
    if (phase === "loading") return;
    if (remote && configured && !user && !authLoading) {
      reportListenError(verseId, section, t("listen.signIn"));
      return;
    }
    const token = remote
      ? await resolveListenToken(accessToken, convexAuth?.fetchAccessToken)
      : null;
    if (remote && configured && user && !token) {
      reportListenError(verseId, section, t("listen.sessionOpening"));
      return;
    }
    await toggleListen({
      verseId,
      section,
      accessToken: token,
      signedIn: Boolean(user),
      verse,
      preferLocal: !remote,
    });
  }

  return (
    <div className={shell}>
      <button
        type="button"
        className="passage-listen__btn"
        onClick={(event) => void onPlay(event)}
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
