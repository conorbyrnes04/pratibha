// Native-safe key/value storage.
//
// On the Lynx Web target `localStorage` exists; on native (PrimJS) it does not,
// so touching it directly throws. This shim uses `localStorage` when available
// and falls back to an in-memory map otherwise, so auth/token code is identical
// across targets. In-memory means native sessions don't survive an app restart
// yet — a persistent native store (e.g. Lynx storage module) is a later task.

const memory = new Map<string, string>();

const ls: Storage | null = (() => {
  try {
    if (typeof localStorage !== "undefined") {
      // Probe: some environments define localStorage but throw on access.
      localStorage.getItem("__probe__");
      return localStorage;
    }
  } catch {
    /* fall through to memory */
  }
  return null;
})();

export const storage = {
  get(key: string): string | null {
    if (ls) {
      try {
        return ls.getItem(key);
      } catch {
        /* fall through */
      }
    }
    return memory.has(key) ? memory.get(key)! : null;
  },
  set(key: string, value: string): void {
    if (ls) {
      try {
        ls.setItem(key, value);
        return;
      } catch {
        /* fall through */
      }
    }
    memory.set(key, value);
  },
  remove(key: string): void {
    if (ls) {
      try {
        ls.removeItem(key);
      } catch {
        /* fall through */
      }
    }
    memory.delete(key);
  },
};

export const TOKEN_KEY = "convex_token";
export const REFRESH_TOKEN_KEY = "convex_refresh_token";
