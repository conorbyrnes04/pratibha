import { unlockedMarks } from "@/lib/glyphUnlock";
import { isShareForceMark, isShareInk, type ShareForceMark, type ShareInk } from "@/lib/shareCard";

const STORAGE_KEY = "pratibha.avatar.mark.v1";
export const AVATAR_MARK_EVENT = "pratibha:avatar-mark";
export const DEFAULT_AVATAR_INK: ShareInk = "gold";

export type AvatarChoice = {
  mark: ShareForceMark | null;
  ink: ShareInk;
};

function unlockedOrNull(candidate: string | null | undefined): ShareForceMark | null {
  if (!candidate || !isShareForceMark(candidate)) return null;
  if (!unlockedMarks({}).has(candidate)) return null;
  return candidate;
}

export function resolveAvatarMark(candidate: string | null | undefined): ShareForceMark | null {
  return unlockedOrNull(candidate);
}

export function resolveAvatarInk(candidate: string | null | undefined): ShareInk {
  return candidate && isShareInk(candidate) ? candidate : DEFAULT_AVATAR_INK;
}

export function loadAvatarChoice(): AvatarChoice {
  if (typeof window === "undefined") return { mark: null, ink: DEFAULT_AVATAR_INK };
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { mark: null, ink: DEFAULT_AVATAR_INK };
    if (isShareForceMark(raw)) {
      return { mark: unlockedOrNull(raw), ink: DEFAULT_AVATAR_INK };
    }
    const parsed = JSON.parse(raw) as { mark?: unknown; ink?: unknown };
    return {
      mark: unlockedOrNull(typeof parsed.mark === "string" ? parsed.mark : null),
      ink: resolveAvatarInk(typeof parsed.ink === "string" ? parsed.ink : null),
    };
  } catch {
    return { mark: null, ink: DEFAULT_AVATAR_INK };
  }
}

export function loadAvatarMark(): ShareForceMark | null {
  return loadAvatarChoice().mark;
}

export function saveAvatarChoice(choice: AvatarChoice): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(STORAGE_KEY, JSON.stringify({ mark: choice.mark, ink: choice.ink }));
  window.dispatchEvent(new CustomEvent(AVATAR_MARK_EVENT, { detail: choice }));
}

export function saveAvatarMark(mark: ShareForceMark | null, ink: ShareInk = loadAvatarChoice().ink): void {
  saveAvatarChoice({ mark, ink });
}
