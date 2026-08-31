import { unlockedMarks } from "@/lib/glyphUnlock";
import { isShareForceMark, type ShareForceMark } from "@/lib/shareCard";

const STORAGE_KEY = "pratibha.avatar.mark.v1";
export const AVATAR_MARK_EVENT = "pratibha:avatar-mark";

export function loadAvatarMark(): ShareForceMark | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw || !isShareForceMark(raw)) return null;
    if (!unlockedMarks({}).has(raw)) return null;
    return raw;
  } catch {
    return null;
  }
}

export function saveAvatarMark(mark: ShareForceMark | null): void {
  if (typeof window === "undefined") return;
  if (mark) localStorage.setItem(STORAGE_KEY, mark);
  else localStorage.removeItem(STORAGE_KEY);
  window.dispatchEvent(new CustomEvent(AVATAR_MARK_EVENT, { detail: { mark } }));
}

export function resolveAvatarMark(candidate: string | null | undefined): ShareForceMark | null {
  if (!candidate || !isShareForceMark(candidate)) return null;
  if (!unlockedMarks({}).has(candidate)) return null;
  return candidate;
}
