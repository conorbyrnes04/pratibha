import {
  listenArchive,
  listenAnnounce,
  listenCue,
  listenPassage,
  listenPlan,
  ListenApiError,
  type ListenArchive,
  type ListenPlan,
  type ListenSection,
} from "@/lib/api";

export type ListenPhase = "idle" | "loading" | "playing" | "paused";
export type ListenPart = Exclude<ListenSection, "all">;

export type ListenTrack = {
  verseId: string;
  sections: ListenPart[];
};

export type ListenSnap = {
  verseId: string | null;
  section: ListenSection | null;
  queueKey: string | null;
  phase: ListenPhase;
  error: string | null;
};

type Sub = () => void;
type Prefetch = {
  verseId: string;
  part: ListenPart;
  announce: Promise<Blob | null>;
  passage: Promise<{ blob: Blob; room: string }>;
};

const subs = new Set<Sub>();
const planCache = new Map<string, Promise<ListenPlan | null>>();
const ARCHIVE_TTL_MS = 20_000;
/** ElevenLabs pads short headings; cut the tail so the layer follows immediately. */
const VERSE_GAP_MS = 140;
let archivePromise: Promise<ListenArchive> | null = null;
let archiveAt = 0;
const archiveSubs = new Set<Sub>();
let archivePoll: number | null = null;
let snap: ListenSnap = { verseId: null, section: null, queueKey: null, phase: "idle", error: null };
let token: number = 0;
let speech: HTMLAudioElement | null = null;
let speechUrl: string | null = null;
let accent: HTMLAudioElement | null = null;
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

export function tracksFromArchive(
  verseIds: string[],
  verses: ListenArchive["verses"],
): ListenTrack[] {
  const out: ListenTrack[] = [];
  for (const verseId of verseIds) {
    const sections = verses[verseId];
    if (sections?.length) out.push({ verseId, sections: [...sections] });
  }
  return out;
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
  accent?.pause();
  if (accent) accent.src = "";
  revokeSpeech();
}

function waitCanPlay(el: HTMLAudioElement, ms = 1600): Promise<void> {
  if (el.readyState >= HTMLMediaElement.HAVE_FUTURE_DATA) return Promise.resolve();
  return new Promise((resolve) => {
    const done = () => {
      cleanup();
      resolve();
    };
    const timer = window.setTimeout(done, ms);
    const cleanup = () => {
      window.clearTimeout(timer);
      el.removeEventListener("canplay", done);
      el.removeEventListener("canplaythrough", done);
      el.removeEventListener("error", done);
    };
    el.addEventListener("canplay", done);
    el.addEventListener("canplaythrough", done);
    el.addEventListener("error", done);
  });
}

function armSpeech(el: HTMLAudioElement, blob: Blob): Promise<void> {
  revokeSpeech();
  const url = URL.createObjectURL(blob);
  speechUrl = url;
  el.src = url;
  el.load();
  return waitCanPlay(el);
}

function playArmed(el: HTMLAudioElement): Promise<void> {
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

function roomRootFreq(room: string): number {
  return room === "indic"
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
  osc.type = "sine";
  osc.frequency.value = roomRootFreq(room);
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

/** Two-note turn between layers — distinct from the open/close room cue. */
function playLayerTone(room: string, next: ListenPart): Promise<void> {
  const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
  if (!AudioCtx) return Promise.resolve();
  const ctx = new AudioCtx();
  const now = ctx.currentTime;
  const master = ctx.createGain();
  master.gain.value = 0.07;
  master.connect(ctx.destination);

  const root = roomRootFreq(room);
  const second =
    next === "practice" ? root * 0.75 : next === "commentary" ? root * 1.5 : root * 1.25;

  const note = (freq: number, t0: number, dur: number) => {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    const filter = ctx.createBiquadFilter();
    filter.type = "lowpass";
    filter.frequency.value = 1800;
    filter.Q.value = 0.35;
    osc.type = "sine";
    osc.frequency.value = freq;
    gain.gain.setValueAtTime(0.0001, t0);
    gain.gain.exponentialRampToValueAtTime(0.18, t0 + 0.03);
    gain.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
    osc.connect(filter);
    filter.connect(gain);
    gain.connect(master);
    osc.start(t0);
    osc.stop(t0 + dur);
  };

  note(root, now, 0.14);
  note(second, now + 0.11, 0.16);
  const total = 0.28;
  return new Promise((resolve) => {
    window.setTimeout(() => {
      void ctx.close();
      resolve();
    }, total * 1000 + 40);
  });
}

function tailSeconds(duration: number): number {
  if (!Number.isFinite(duration) || duration <= 0) return 0.28;
  // ElevenLabs pads short headings; eat the silence, keep the spoken word.
  return Math.min(0.62, Math.max(0.22, duration * 0.4));
}

function waitRemaining(el: HTMLAudioElement, remainS: number): Promise<void> {
  return new Promise((resolve, reject) => {
    let timer = 0;
    let settled = false;
    const finish = () => {
      if (settled) return;
      settled = true;
      window.clearTimeout(timer);
      el.removeEventListener("ended", finish);
      el.removeEventListener("error", onError);
      resolve();
    };
    const onError = () => {
      if (settled) return;
      settled = true;
      window.clearTimeout(timer);
      el.removeEventListener("ended", finish);
      el.removeEventListener("error", onError);
      reject(new Error("Playback failed."));
    };
    const tick = () => {
      if (settled) return;
      if (Number.isFinite(el.duration) && el.duration > 0) {
        const left = el.duration - el.currentTime;
        if (left <= remainS || el.ended) {
          finish();
          return;
        }
        timer = window.setTimeout(tick, Math.min(40, Math.max(16, (left - remainS) * 1000)));
        return;
      }
      timer = window.setTimeout(tick, 40);
    };
    el.addEventListener("ended", finish);
    el.addEventListener("error", onError);
    void el.play().then(tick).catch(onError);
  });
}

async function playAnnounceBlob(blob: Blob): Promise<void> {
  const url = URL.createObjectURL(blob);
  const el = new Audio();
  accent = el;
  el.volume = 0.72;
  el.src = url;
  try {
    await waitCanPlay(el, 800);
    await waitRemaining(el, tailSeconds(el.duration));
  } finally {
    el.pause();
    URL.revokeObjectURL(url);
    if (accent === el) accent = null;
  }
}

async function playCueBlob(blob: Blob, volume = 0.58): Promise<void> {
  const url = URL.createObjectURL(blob);
  const el = new Audio();
  accent = el;
  el.volume = volume;
  el.src = url;
  try {
    await new Promise<void>((resolve, reject) => {
      const cleanup = () => {
        el.removeEventListener("ended", onEnded);
        el.removeEventListener("error", onError);
      };
      const onEnded = () => {
        cleanup();
        resolve();
      };
      const onError = () => {
        cleanup();
        reject(new Error("Playback failed."));
      };
      el.addEventListener("ended", onEnded);
      el.addEventListener("error", onError);
      void el.play().catch(onError);
    });
  } finally {
    URL.revokeObjectURL(url);
    if (accent === el) accent = null;
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

async function fetchAnnounce(
  verseId: string,
  section: ListenPart,
  accessToken?: string | null,
): Promise<Blob | null> {
  try {
    return await listenAnnounce(verseId, section, accessToken);
  } catch {
    return null;
  }
}

function sameControl(opts: {
  verseId: string;
  section: ListenSection;
  queueKey?: string | null;
}): boolean {
  if (opts.queueKey) return snap.queueKey === opts.queueKey;
  return !snap.queueKey && snap.verseId === opts.verseId && snap.section === opts.section;
}

function nextSlot(tracks: ListenTrack[], trackIndex: number, partIndex: number): {
  verseId: string;
  part: ListenPart;
} | null {
  const track = tracks[trackIndex];
  if (track && partIndex + 1 < track.sections.length) {
    return { verseId: track.verseId, part: track.sections[partIndex + 1] };
  }
  const upcoming = tracks[trackIndex + 1];
  if (upcoming?.sections[0]) return { verseId: upcoming.verseId, part: upcoming.sections[0] };
  return null;
}

function prefetchSlot(
  verseId: string,
  part: ListenPart,
  accessToken: string | null | undefined,
  reuse: Map<ListenPart, Blob>,
): Prefetch {
  const cached = reuse.get(part);
  return {
    verseId,
    part,
    announce: cached ? Promise.resolve(cached) : fetchAnnounce(verseId, part, accessToken),
    passage: listenPassage(verseId, accessToken, part),
  };
}

export function reportListenError(
  verseId: string,
  section: ListenSection,
  message: string,
  queueKey?: string | null,
) {
  emit({ verseId, section, queueKey: queueKey ?? null, phase: "idle", error: message });
}

export async function toggleListen(opts: {
  verseId: string;
  section: ListenSection;
  queue?: ListenTrack[];
  queueKey?: string | null;
  accessToken?: string | null;
  signedIn?: boolean;
}): Promise<void> {
  const { verseId, section, queue, queueKey = null, accessToken, signedIn } = opts;
  if (snap.phase === "playing" && sameControl(opts)) {
    speech?.pause();
    emit({ phase: "paused" });
    return;
  }
  if (snap.phase === "paused" && sameControl(opts) && speech?.src) {
    await speech.play();
    emit({ phase: "playing" });
    return;
  }

  stopNow();
  const run = token;
  emit({ verseId, section, queueKey, phase: "loading", error: null });

  try {
    const tracks: ListenTrack[] = queue?.length
      ? queue
      : await (async () => {
          const plan = await loadListenPlan(verseId);
          const archived = plan?.sections || [];
          if (!archived.length) throw new Error("This passage has not been spoken yet.");
          if (section !== "all" && !archived.includes(section)) {
            throw new Error("This layer has not been spoken yet.");
          }
          return [
            {
              verseId,
              sections: section === "all" ? archived : [section],
            },
          ];
        })();
    if (!tracks.length) throw new Error("This passage has not been spoken yet.");

    const firstPlan = await loadListenPlan(tracks[0].verseId);
    const room = firstPlan?.room || "unmarked";
    const el = speech ?? new Audio();
    speech = el;
    const announceReuse = new Map<ListenPart, Blob>();
    let ahead: Prefetch | null = prefetchSlot(
      tracks[0].verseId,
      tracks[0].sections[0],
      accessToken,
      announceReuse,
    );

    await playCue(room, "open", accessToken);
    let firstPart = true;
    for (let trackIndex = 0; trackIndex < tracks.length; trackIndex++) {
      const track = tracks[trackIndex];
      for (let partIndex = 0; partIndex < track.sections.length; partIndex++) {
        if (run !== token) return;
        const part = track.sections[partIndex];
        const current =
          ahead && ahead.verseId === track.verseId && ahead.part === part
            ? ahead
            : prefetchSlot(track.verseId, part, accessToken, announceReuse);
        const upcoming = nextSlot(tracks, trackIndex, partIndex);
        ahead = upcoming
          ? prefetchSlot(upcoming.verseId, upcoming.part, accessToken, announceReuse)
          : null;
        const armP = current.passage.then(({ blob }) => armSpeech(el, blob));

        if (!firstPart) {
          if (partIndex === 0) {
            await new Promise((resolve) => window.setTimeout(resolve, VERSE_GAP_MS));
          } else {
            await playLayerTone(room, part);
          }
          if (run !== token) return;
        }
        firstPart = false;
        const announceBlob = await current.announce;
        if (run !== token) return;
        if (announceBlob && !announceReuse.has(part)) announceReuse.set(part, announceBlob);
        if (announceBlob) {
          try {
            await playAnnounceBlob(announceBlob);
          } catch {
            // Missing heading must not fail Listen — the passage still plays.
          }
          if (run !== token) return;
        }
        await armP;
        if (run !== token) return;
        emit({
          verseId: track.verseId,
          section: queueKey || section === "all" ? "all" : part,
          queueKey,
          phase: "playing",
          error: null,
        });
        await playArmed(el);
      }
    }
    if (run !== token) return;
    await playCue(room, "close", accessToken);
    if (run === token) emit({ phase: "idle", error: null, queueKey: null });
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
  emit({ verseId: null, section: null, queueKey: null, phase: "idle", error: null });
}
