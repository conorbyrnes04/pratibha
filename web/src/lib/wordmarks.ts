/** Header lockups 5b–5g — same Cormorant italic, fading through the set. */

export type WordmarkId = (typeof WORDMARKS)[number]["id"];

export type WordmarkDef = {
  id: WordmarkId;
  src: string;
};

export const WORDMARKS = [
  { id: "5b", src: "/brand/wordmarks/5b.png" },
  { id: "5c", src: "/brand/wordmarks/5c.png" },
  { id: "5d", src: "/brand/wordmarks/5d.png" },
  { id: "5e", src: "/brand/wordmarks/5e.png" },
  { id: "5f", src: "/brand/wordmarks/5f.png" },
  { id: "5g", src: "/brand/wordmarks/5g.png" },
] as const;

export const WORDMARK_CYCLE_MS = 9000;

const LAST_KEY = "pratibha.wordmark.last";

let current: WordmarkDef | null = null;
const listeners = new Set<(mark: WordmarkDef) => void>();

type Clock = {
  lastTickAt: number;
  timer: number | null;
  step: () => void;
};

function clock(): Clock {
  const w = window as Window & { __pratibhaWordmarkClock?: Clock };
  if (!w.__pratibhaWordmarkClock) {
    w.__pratibhaWordmarkClock = { lastTickAt: Date.now(), timer: null, step: () => undefined };
  }
  return w.__pratibhaWordmarkClock;
}

export function wordmarkById(id: string | null | undefined): WordmarkDef {
  return WORDMARKS.find((m) => m.id === id) ?? WORDMARKS[0];
}

export function nextWordmark(id: string | null | undefined): WordmarkDef {
  const idx = WORDMARKS.findIndex((m) => m.id === id);
  return WORDMARKS[(idx + 1) % WORDMARKS.length];
}

function persist(mark: WordmarkDef): WordmarkDef {
  current = mark;
  try {
    localStorage.setItem(LAST_KEY, mark.id);
  } catch {
    /* private mode */
  }
  return mark;
}

function notify(mark: WordmarkDef): void {
  for (const listener of listeners) listener(mark);
}

function sitting(): WordmarkDef {
  if (current) return current;
  try {
    return wordmarkById(localStorage.getItem(LAST_KEY));
  } catch {
    return WORDMARKS[0];
  }
}

function stepCycle(): void {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const shared = clock();
  const now = Date.now();
  if (now - shared.lastTickAt < WORDMARK_CYCLE_MS) return;
  shared.lastTickAt = now;
  notify(persist(nextWordmark(sitting().id)));
}

function ensureCycle(): void {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const shared = clock();
  shared.step = stepCycle;
  if (shared.timer != null) return;
  shared.lastTickAt = Date.now();
  shared.timer = window.setInterval(() => clock().step(), 500);
}

/** One lockup for this page; remounts keep it. A new document advances one step. */
export function subscribeWordmark(listener: (mark: WordmarkDef) => void): () => void {
  if (!current) {
    let last: string | null = null;
    try {
      last = localStorage.getItem(LAST_KEY);
    } catch {
      last = null;
    }
    persist(nextWordmark(last));
  }
  listener(current);
  listeners.add(listener);
  ensureCycle();
  return () => {
    listeners.delete(listener);
  };
}
