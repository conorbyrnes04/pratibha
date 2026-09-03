"use client";

import { useAuthToken, useConvexAuth } from "@convex-dev/auth/react";
import { useEffect, useState, type MouseEvent } from "react";
import { useAuth } from "@/components/AuthProvider";
import { useT } from "@/components/LocaleProvider";
import { InkGlyph, type InkSize, type InkState } from "@/components/InkGlyph";
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
  tracksFromArchive,
  type ListenPhase,
  type ListenSnap,
  type ListenTrack,
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

function SumiPlayMark({ phase, size }: { phase: ListenPhase; size: InkSize }) {
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

function markSize(variant: "toolbar" | "layer" | "header" | "collection"): InkSize {
  if (variant === "layer") return "xs";
  if (variant === "collection") return "lg";
  return "sm";
}

export function ListenButton({
  verseId,
  section = "all",
  variant = "toolbar",
  queueKey,
  queueVerseIds,
}: {
  verseId?: string;
  section?: ListenSection;
  variant?: "toolbar" | "layer" | "header" | "collection";
  queueKey?: string;
  queueVerseIds?: string[];
}) {
  const t = useT();
  const { user, configured, loading: authLoading } = useAuth();
  const accessToken = useAuthToken();
  const convexAuth = useConvexAuth();
  const [available, setAvailable] = useState(false);
  const [plan, setPlan] = useState<ListenPlan | null>(null);
  const [queue, setQueue] = useState<ListenTrack[]>([]);
  const [snap, setSnap] = useState<ListenSnap>(listenSnapshot);
  const collection = Boolean(queueKey);
  const queueIdsKey = queueVerseIds?.join("\0") ?? "";

  useEffect(() => {
    let cancelled = false;
    const ids = queueIdsKey ? queueIdsKey.split("\0") : [];
    async function pull() {
      const archive = await loadListenArchive();
      if (cancelled) return;
      if (collection) {
        if (archive.loaded) {
          setAvailable(archive.configured);
        } else {
          const ok = await listenConfigured();
          if (cancelled) return;
          setAvailable(ok);
        }
        setQueue(tracksFromArchive(ids, archive.verses));
        return;
      }
      if (archive.loaded) {
        setAvailable(archive.configured);
        const sections = (verseId && archive.verses[verseId]) || [];
        setPlan({ room: "unmarked", sections });
        return;
      }
      const ok = await listenConfigured();
      if (cancelled) return;
      setAvailable(ok);
      if (!ok || !verseId) return;
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
  }, [verseId, collection, queueIdsKey]);

  useEffect(() => subscribeListen(() => setSnap(listenSnapshot())), []);

  const ready = collection ? available && queue.length > 0 : available && sectionReady(plan, section);
  const leadId = collection ? queue[0]?.verseId || "" : verseId || "";

  useEffect(() => {
    if ((section !== "all" && !collection) || !ready) return;
    return retainListen();
  }, [verseId, section, ready, collection]);

  if (!ready || !leadId) return null;

  const mine = queueKey
    ? snap.queueKey === queueKey
    : !snap.queueKey && snap.verseId === leadId && snap.section === section;
  const phase = mine ? snap.phase : "idle";
  const error = mine ? snap.error : null;
  const caption =
    phase === "loading"
      ? t("listen.preparing")
      : phase === "playing"
        ? t("listen.pause")
        : phase === "paused"
          ? t("listen.resume")
          : collection
            ? t("listen.playCollection")
            : section === "all"
              ? t("listen.playAll")
              : t("listen.listen");
  const shell =
    variant === "layer"
      ? "passage-listen passage-listen--layer"
      : variant === "header"
        ? "passage-listen passage-listen--header"
        : variant === "collection"
          ? "passage-listen passage-listen--collection"
          : "passage-listen passage-listen--toolbar";

  async function onPlay(event: MouseEvent<HTMLButtonElement>) {
    event.preventDefault();
    event.stopPropagation();
    if (phase === "loading") return;
    if (configured && !user && !authLoading) {
      reportListenError(leadId, section, t("listen.signIn"), queueKey);
      return;
    }
    const token = await resolveListenToken(accessToken, convexAuth?.fetchAccessToken);
    if (configured && user && !token) {
      reportListenError(leadId, section, t("listen.sessionOpening"), queueKey);
      return;
    }
    await toggleListen({
      verseId: leadId,
      section,
      queue: collection ? queue : undefined,
      queueKey: collection ? queueKey : undefined,
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
        <SumiPlayMark phase={phase} size={markSize(variant)} />
        <span className="passage-listen__caption">{caption}</span>
      </button>
      {error ? <p className="passage-listen__error">{error}</p> : null}
    </div>
  );
}
