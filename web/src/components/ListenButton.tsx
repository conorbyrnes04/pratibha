"use client";

import { useAuthToken, useConvexAuth } from "@convex-dev/auth/react";
import { useEffect, useState, type MouseEvent } from "react";
import { useAuth } from "@/components/AuthProvider";
import { useT } from "@/components/LocaleProvider";
import { InkGlyph, type InkState } from "@/components/InkGlyph";
import { listenConfigured, type ListenPlan, type ListenSection } from "@/lib/api";
import {
  listenSnapshot,
  loadListenArchive,
  loadListenPlan,
  reportListenError,
  retainListen,
  subscribeListen,
  subscribeListenArchive,
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
      <InkGlyph glyph="play" state={state} size={size} mask />
    </span>
  );
}

function sectionReady(plan: ListenPlan | null, section: ListenSection): boolean {
  if (!plan?.sections.length) return false;
  return section === "all" || plan.sections.includes(section);
}

export function ListenButton({
  verseId,
  section = "all",
  variant = "toolbar",
}: {
  verseId: string;
  section?: ListenSection;
  variant?: "toolbar" | "layer" | "header";
}) {
  const t = useT();
  const { user, configured, loading: authLoading } = useAuth();
  const accessToken = useAuthToken();
  const convexAuth = useConvexAuth();
  const [available, setAvailable] = useState(false);
  const [plan, setPlan] = useState<ListenPlan | null>(null);
  const [snap, setSnap] = useState<ListenSnap>(listenSnapshot);

  useEffect(() => {
    let cancelled = false;
    async function pull() {
      const archive = await loadListenArchive();
      if (cancelled) return;
      if (archive.loaded) {
        setAvailable(archive.configured);
        const sections = archive.verses[verseId] || [];
        setPlan({ room: "unmarked", sections });
        return;
      }
      const ok = await listenConfigured();
      if (cancelled) return;
      setAvailable(ok);
      if (!ok) return;
      const next = await loadListenPlan(verseId);
      if (!cancelled) setPlan(next);
    }
    void pull();
    const stop = subscribeListenArchive(() => {
      void pull();
    });
    return () => {
      cancelled = true;
      stop();
    };
  }, [verseId]);

  useEffect(() => subscribeListen(() => setSnap(listenSnapshot())), []);

  const ready = available && sectionReady(plan, section);

  useEffect(() => {
    if (section !== "all" || !ready) return;
    return retainListen();
  }, [verseId, section, ready]);

  if (!ready) return null;

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
    if (configured && !user && !authLoading) {
      reportListenError(verseId, section, t("listen.signIn"));
      return;
    }
    const token = await resolveListenToken(accessToken, convexAuth?.fetchAccessToken);
    if (configured && user && !token) {
      reportListenError(verseId, section, t("listen.sessionOpening"));
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
