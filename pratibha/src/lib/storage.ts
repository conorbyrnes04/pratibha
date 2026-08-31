// Native-safe key/value storage.
//
// Preference order:
// 1. `localStorage` on the Lynx Web target
// 2. Lynx Explorer `NativeLocalStorageModule` (survives app restart)
// 3. In-memory map (last resort — lost on process death)

const memory = new Map<string, string>();

const ls: Storage | null = (() => {
  try {
    if (typeof localStorage !== "undefined") {
      // Probe: some environments define localStorage but throw on access.
      localStorage.getItem("__probe__");
      return localStorage;
    }
  } catch {
    /* fall through */
  }
  return null;
})();

type NativeKv = {
  setStorageItem?: (key: string, value: string) => void;
  getStorageItem?: (key: string, callback?: (value: string) => void) => string | null | void;
  removeStorageItem?: (key: string) => void;
  clearStorage?: () => void;
};

function nativeKv(): NativeKv | null {
  try {
    // Lynx Explorer ships NativeLocalStorageModule in many builds.
    const mods = (globalThis as { NativeModules?: { NativeLocalStorageModule?: NativeKv } })
      .NativeModules;
    const mod = mods?.NativeLocalStorageModule;
    if (mod?.setStorageItem && mod.getStorageItem) return mod;
  } catch {
    /* no native store */
  }
  return null;
}

export const storage = {
  get(key: string): string | null {
    if (ls) {
      try {
        return ls.getItem(key);
      } catch {
        /* fall through */
      }
    }
    const native = nativeKv();
    if (native?.getStorageItem) {
      try {
        const value = native.getStorageItem(key);
        if (typeof value === "string" && value.length > 0) return value;
        if (value === null) return null;
      } catch {
        /* fall through */
      }
    }
    return memory.has(key) ? memory.get(key)! : null;
  },
  set(key: string, value: string): void {
    memory.set(key, value);
    if (ls) {
      try {
        ls.setItem(key, value);
        return;
      } catch {
        /* fall through */
      }
    }
    const native = nativeKv();
    if (native?.setStorageItem) {
      try {
        native.setStorageItem(key, value);
      } catch {
        /* memory already set */
      }
    }
  },
  remove(key: string): void {
    memory.delete(key);
    if (ls) {
      try {
        ls.removeItem(key);
      } catch {
        /* fall through */
      }
    }
    const native = nativeKv();
    if (native?.removeStorageItem) {
      try {
        native.removeStorageItem(key);
        return;
      } catch {
        /* fall through */
      }
    }
    if (native?.setStorageItem) {
      try {
        native.setStorageItem(key, "");
      } catch {
        /* ignore */
      }
    }
  },
};

export const TOKEN_KEY = "convex_token";
export const REFRESH_TOKEN_KEY = "convex_refresh_token";
