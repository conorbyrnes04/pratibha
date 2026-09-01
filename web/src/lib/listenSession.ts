import {
  listenArchive,
  listenCue,
  listenPassage,
  listenPlan,
  ListenApiError,
  type ListenArchive,
  type ListenPlan,
  type ListenSection,
} from "@/lib/api";

export type ListenPhase = "idle" | "loading" | "playing" | "paused";

export type ListenSnap = {
  verseId: string | null;
  section: ListenSection | null;
  phase: ListenPhase;
  error: string | null;
};

type Sub = () => void;

const subs = new Set<Sub>();
const planCache = new Map<string, Promise<ListenPlan | null>>();
const ARCHIVE_TTL_MS = 20_000;
let archivePromise: Promise<ListenArchive> | null = null;
let archiveAt = 0;
const archiveSubs = new Set<Sub>();
let archivePoll: ReturnType<typeof setInterval> | null = null;
let snap: ListenSnap = { verseId: null, section: null, phase: "idle", error: null };
let token: number = 0;
let speech: HTMLAudioElement | null = null;
let speechUrl: string | null = null;
let retainers = 0;

function emit(next: Partial<ListenSnap>) {
  snap = { ...snap, ...next };
  subs.forEach((fn) => fn());
}

export function listenSnapshot(): ListenSnap {
  return snap;
}

export function subscribeListen(fn: Sub): () => void {
  subs.add(fn);
  return () => {
    subs.delete(fn);
  };
}

export function subscribeListenArchive(fn: Sub): () => void {
  archiveSubs.add(fn);
  if (typeof window !== "undefined" && archivePoll == null) {
    archivePoll = window.setInterval(() => {
      archivePromise = null;
      archiveAt = 0;
      planCache.clear();
      void loadListenArchive();
    }, ARCHIVE_TTL_MS);
  }
  return () => {
    archiveSubs.delete(fn);
    if (archiveSubs.size === 0 && archivePoll != null) {
      window.clearInterval(archivePoll);
      archivePoll = null;
    }
  };
}

export function loadListenArchive(): Promise<ListenArchive> {
  const now = Date.now();
  if (!archivePromise || now - archiveAt > ARCHIVE_TTL_MS) {
    archivePromise = listenArchive();
    archiveAt = now;
    planCache.clear();
    void archivePromise.then(() => {
      archiveSubs.forEach((fn) => fn());
    });
  }
  return archivePromise;
}

export function loadListenPlan(verseId: string): Promise<ListenPlan | null> {
  let hit = planCache.get(verseId);
  if (!hit) {
    hit = listenPlan(verseId);
    planCache.set(verseId, hit);
  }
  return hit;
}

/** Keep playback alive while any Path/read "Play all" control is still mounted. */
export function retainListen(): () => void {
  retainers += 1;
  return () => {
    retainers = Math.max(0, retainers - 1);
    if (retainers === 0) stopListen();
  };
}

function revokeSpeech() {
  if (speechUrl) {
    URL.revokeObjectURL(speechUrl);
    speechUrl = null;
  }
}

function stopNow() {
  token += 1;
  speech?.pause();
  if (speech) speech.src = "";
  revokeSpeech();
}

function playBlob(el: HTMLAudioElement, blob: Blob): Promise<void> {
  revokeSpeech();
  const url = URL.createObjectURL(blob);
  speechUrl = url;
  el.src = url;
  return new Promise((resolve, reject) => {
    const onEnded = () => {
      cleanup();
      resolve();
    };
    const onError = () => {
      cleanup();
      reject(new Error("Playback failed."));
    };
    const cleanup = () => {
      el.removeEventListener("ended", onEnded);
      el.removeEventListener("error", onError);
    };
    el.addEventListener("ended", onEnded);
    el.addEventListener("error", onError);
    void el.play().catch(onError);
  });
}

function playRoomTone(room: string, edge: "open" | "close"): Promise<void> {
  const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
  if (!AudioCtx) return Promise.resolve();
  const ctx = new AudioCtx();
  const now = ctx.currentTime;
  const master = ctx.createGain();
  master.gain.value = edge === "open" ? 0.08 : 0.05;
  master.connect(ctx.destination);

  const dur = edge === "open" ? 0.85 : 0.7;
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  const filter = ctx.createBiquadFilter();
  filter.type = "lowpass";
  filter.frequency.value = 1400;
  filter.Q.value = 0.4;
  const freq =
    room === "indic"
      ? 196
      : room === "sinosphere"
        ? 220
        : room === "yoruba"
          ? 98
          : room === "hebrew"
            ? 311
            : room === "hellenic"
              ? 165
              : room === "sufi"
                ? 147
                : room === "dakota"
                  ? 110
                  : 174;
  osc.type = "sine";
  osc.frequency.value = freq;
  gain.gain.setValueAtTime(0.0001, now);
  gain.gain.exponentialRampToValueAtTime(0.16, now + 0.05);
  gain.gain.exponentialRampToValueAtTime(0.0001, now + dur);
  osc.connect(filter);
  filter.connect(gain);
  gain.connect(master);
  osc.start(now);
  osc.stop(now + dur);

  return new Promise((resolve) => {
    window.setTimeout(() => {
      void ctx.close();
      resolve();
    }, dur * 1000 + 40);
  });
}

async function playCueBlob(blob: Blob, volume = 0.58): Promise<void> {
  const url = URL.createObjectURL(blob);
  const el = new Audio();
  el.volume = volume;
  el.src = url;
  try {
    await new Promise<void>((resolve, reject) => {
      const done = () => {
        el.removeEventListener("ended", onEnded);
        el.removeEventListener("error", onError);
        resolve();
      };
      const onEnded = () => done();
      const onError = () => {
        el.removeEventListener("ended", onEnded);
        el.removeEventListener("error", onError);
        reject(new Error("Playback failed."));
      };
      el.addEventListener("ended", onEnded);
      el.addEventListener("error", onError);
      void el.play().catch(onError);
    });
  } finally {
    URL.revokeObjectURL(url);
  }
}

async function playCue(
  room: string,
  edge: "open" | "close",
  accessToken?: string | null,
): Promise<void> {
  try {
    const blob = await listenCue(room, edge, accessToken);
    await playCueBlob(blob);
  } catch {
    await playRoomTone(room, edge);
  }
}

export function reportListenError(
  verseId: string,
  section: ListenSection,
  message: string,
) {
  emit({ verseId, section, phase: "idle", error: message });
}

export async function toggleListen(opts: {
  verseId: string;
  section: ListenSection;
  accessToken?: string | null;
  signedIn?: boolean;
}): Promise<void> {
  const { verseId, section, accessToken, signedIn } = opts;
  if (snap.phase === "playing" && snap.verseId === verseId && snap.section === section) {
    speech?.pause();
    emit({ phase: "paused" });
    return;
  }
  if (snap.phase === "paused" && snap.verseId === verseId && snap.section === section && speech?.src) {
    await speech.play();
    emit({ phase: "playing" });
    return;
  }

  stopNow();
  const run = token;
  emit({ verseId, section, phase: "loading", error: null });

  try {
    const plan = await loadListenPlan(verseId);
    const archived = plan?.sections || [];
    if (!archived.length) {
      throw new Error("This passage has not been spoken yet.");
    }
    if (section !== "all" && !archived.includes(section)) {
      throw new Error("This layer has not been spoken yet.");
    }
    const room = plan?.room || "unmarked";
    const queue: Array<Exclude<ListenSection, "all">> =
      section === "all" ? archived : [section];

    const el = speech ?? new Audio();
    speech = el;

    await playCue(room, "open", accessToken);
    for (const part of queue) {
      if (run !== token) return;
      const { blob } = await listenPassage(verseId, accessToken, part);
      if (run !== token) return;
      emit({ phase: "playing", section: section === "all" ? "all" : part });
      await playBlob(el, blob);
    }
    if (run !== token) return;
    await playCue(room, "close", accessToken);
    if (run === token) emit({ phase: "idle", error: null });
  } catch (err) {
    if (run !== token) return;
    const status = err instanceof ListenApiError ? err.status : 0;
    const message =
      status === 401
        ? signedIn
          ? "Listen could not verify your session. Refresh and try again."
          : "Sign in to listen."
        : status === 404
          ? "This passage has not been spoken yet."
          : status === 429
            ? "Listen is resting. Try again in a minute."
            : err instanceof Error
              ? err.message
              : "Could not speak this passage.";
    emit({ phase: "idle", error: message });
  }
}

export function stopListen() {
  stopNow();
  emit({ verseId: null, section: null, phase: "idle", error: null });
}
