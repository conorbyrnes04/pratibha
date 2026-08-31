"use client";

import { useEffect, useState } from "react";
import { useMutation, useQuery } from "convex/react";
import { api } from "../../convex/_generated/api";
import { useAuth } from "@/components/AuthProvider";
import { CONVEX_ENABLED } from "@/lib/convexConfigured";
import {
  AVATAR_MARK_EVENT,
  DEFAULT_AVATAR_INK,
  loadAvatarChoice,
  resolveAvatarInk,
  resolveAvatarMark,
  saveAvatarChoice,
  type AvatarChoice,
} from "@/lib/avatarMark";
import { GLYPH_UNLOCK_EVENT, unlockedMarks } from "@/lib/glyphUnlock";
import type { ShareForceMark, ShareInk } from "@/lib/shareCard";

export function useAvatarMark() {
  const { user } = useAuth();
  const profile = useQuery(api.profiles.getMine, CONVEX_ENABLED && user ? {} : "skip");
  const setCloudMark = useMutation(api.profiles.setMark);
  const [choice, setChoice] = useState<AvatarChoice>({ mark: null, ink: DEFAULT_AVATAR_INK });
  const [openMarks, setOpenMarks] = useState<Set<ShareForceMark>>(() => new Set());

  useEffect(() => {
    function refresh() {
      const unlocked = unlockedMarks({});
      setOpenMarks(unlocked);
      const local = loadAvatarChoice();
      const cloudMark = resolveAvatarMark(profile?.mark);
      const cloudInk = resolveAvatarInk(profile?.ink);
      const stored = typeof window !== "undefined" && Boolean(localStorage.getItem("pratibha.avatar.mark.v1"));
      const mark = local.mark && unlocked.has(local.mark) ? local.mark : cloudMark;
      const ink = stored ? local.ink : cloudInk;
      const next = { mark, ink };
      setChoice(next);
      if (!stored && (cloudMark || profile?.ink)) saveAvatarChoice(next);
    }
    refresh();
    window.addEventListener(AVATAR_MARK_EVENT, refresh);
    window.addEventListener(GLYPH_UNLOCK_EVENT, refresh);
    return () => {
      window.removeEventListener(AVATAR_MARK_EVENT, refresh);
      window.removeEventListener(GLYPH_UNLOCK_EVENT, refresh);
    };
  }, [profile?.mark, profile?.ink]);

  async function persist(next: AvatarChoice) {
    saveAvatarChoice(next);
    setChoice(next);
    if (CONVEX_ENABLED && user) {
      try {
        await setCloudMark({ mark: next.mark ?? undefined, ink: next.ink });
      } catch {
        try {
          await setCloudMark({ mark: next.mark ?? undefined });
        } catch {
          /* local choice still stands */
        }
      }
    }
  }

  function choose(mark: ShareForceMark | null) {
    return persist({ mark, ink: choice.ink });
  }

  function chooseInk(ink: ShareInk) {
    return persist({ mark: choice.mark, ink });
  }

  return { mark: choice.mark, ink: choice.ink, choose, chooseInk, openMarks };
}
