import {
  listenCue,
  listenPassage,
  listenPlan,
  ListenApiError,
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
let snap: ListenSnap = { verseId: null, section: null, phase: "idle", error: null };
let token: number = 0;
let speech: HTMLAudioElement | null = null;
let speechUrl: string | null = null;

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
  master.gain.value = edge === "open" ? 0.18 : 0.12;
  master.connect(ctx.destination);

  const dur = edge === "open" ? 1.6 : 1.15;
  if (room === "dakota") {
    const buffer = ctx.createBuffer(1, Math.floor(ctx.sampleRate * dur), ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < data.length; i += 1) {
      data[i] = (Math.random() * 2 - 1) * (1 - i / data.length);
    }
    const src = ctx.createBufferSource();
    src.buffer = buffer;
    const filter = ctx.createBiquadFilter();
    filter.type = "bandpass";
    filter.frequency.value = 380;
    filter.Q.value = 0.7;
    src.connect(filter);
    filter.connect(master);
    src.start(now);
  } else {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
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
                  : 174;
    osc.type = room === "sinosphere" ? "triangle" : "sine";
    osc.frequency.value = freq;
    gain.gain.setValueAtTime(0.0001, now);
    gain.gain.exponentialRampToValueAtTime(0.22, now + 0.04);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + dur);
    osc.connect(gain);
    gain.connect(master);
    osc.start(now);
    osc.stop(now + dur);
  }

  return new Promise((resolve) => {
    window.setTimeout(() => {
      void ctx.close();
      resolve();
    }, dur * 1000 + 40);
  });
}

async function playCue(
  room: string,
  edge: "open" | "close",
  accessToken?: string | null,
): Promise<void> {
  try {
    const blob = await listenCue(room, edge, accessToken);
    const el = speech ?? new Audio();
    speech = el;
    await playBlob(el, blob);
  } catch {
    await playRoomTone(room, edge);
  }
}

export async function toggleListen(opts: {
  verseId: string;
  section: ListenSection;
  accessToken?: string | null;
}): Promise<void> {
  const { verseId, section, accessToken } = opts;
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
    const plan = await listenPlan(verseId);
    const room = plan?.room || "unmarked";
    const queue: Array<Exclude<ListenSection, "all">> =
      section === "all"
        ? plan?.sections?.length
          ? plan.sections
          : ["translation", "commentary", "practice"]
        : [section];

    const el = speech ?? new Audio();
    speech = el;

    for (const part of queue) {
      if (run !== token) return;
      await playCue(room, "open", accessToken);
      if (run !== token) return;
      const { blob } = await listenPassage(verseId, accessToken, part);
      if (run !== token) return;
      emit({ phase: "playing", section: section === "all" ? "all" : part });
      await playBlob(el, blob);
      if (run !== token) return;
      await playCue(room, "close", accessToken);
    }
    if (run === token) emit({ phase: "idle", error: null });
  } catch (err) {
    if (run !== token) return;
    const status = err instanceof ListenApiError ? err.status : 0;
    const message =
      status === 401
        ? "Sign in to listen."
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
