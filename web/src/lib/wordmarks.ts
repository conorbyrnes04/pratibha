/** Header lockups 5b–5g — same Cormorant italic, rotating through the set. */

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

export const WORDMARK_CYCLE_MS = 4000;

const LAST_KEY = "pratibha.wordmark.last";
const NAV_KEY = "pratibha.wordmark.nav";

let pickedThisLoad: WordmarkDef | null = null;

export function wordmarkById(id: string | null | undefined): WordmarkDef {
  return WORDMARKS.find((m) => m.id === id) ?? WORDMARKS[0];
}

export function nextWordmark(id: string | null | undefined): WordmarkDef {
  const idx = WORDMARKS.findIndex((m) => m.id === id);
  return WORDMARKS[(idx + 1) % WORDMARKS.length];
}

function persist(mark: WordmarkDef): WordmarkDef {
  try {
    localStorage.setItem(LAST_KEY, mark.id);
  } catch {
    /* private mode */
  }
  pickedThisLoad = mark;
  return mark;
}

function navigationStamp(): string {
  return String(performance.timeOrigin);
}

/** Advance once per full document load, including hard refresh. */
export function pickSessionWordmark(): WordmarkDef {
  if (typeof window === "undefined") return WORDMARKS[0];
  if (pickedThisLoad) return pickedThisLoad;
  try {
    const stamp = navigationStamp();
    if (sessionStorage.getItem(NAV_KEY) === stamp && pickedThisLoad) {
      return pickedThisLoad;
    }
    sessionStorage.setItem(NAV_KEY, stamp);
    return persist(nextWordmark(localStorage.getItem(LAST_KEY)));
  } catch {
    return persist(WORDMARKS[0]);
  }
}

export function advanceWordmark(currentId: string): WordmarkDef {
  return persist(nextWordmark(currentId));
}
