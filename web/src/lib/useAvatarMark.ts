"use client";

import { useEffect, useState } from "react";
import { useMutation, useQuery } from "convex/react";
import { api } from "../../convex/_generated/api";
import { useAuth } from "@/components/AuthProvider";
import { CONVEX_ENABLED } from "@/lib/convexConfigured";
import { AVATAR_MARK_EVENT, loadAvatarMark, resolveAvatarMark, saveAvatarMark } from "@/lib/avatarMark";
import { GLYPH_UNLOCK_EVENT, unlockedMarks } from "@/lib/glyphUnlock";
import type { ShareForceMark } from "@/lib/shareCard";

export function useAvatarMark() {
  const { user } = useAuth();
  const profile = useQuery(api.profiles.getMine, CONVEX_ENABLED && user ? {} : "skip");
  const setCloudMark = useMutation(api.profiles.setMark);
  const [mark, setMark] = useState<ShareForceMark | null>(null);
  const [openMarks, setOpenMarks] = useState<Set<ShareForceMark>>(() => new Set());

  useEffect(() => {
    function refresh() {
      const unlocked = unlockedMarks({});
      setOpenMarks(unlocked);
      const local = loadAvatarMark();
      const fromCloud = resolveAvatarMark(profile?.mark);
      const next = local && unlocked.has(local) ? local : fromCloud;
      setMark(next);
      if (!local && fromCloud) saveAvatarMark(fromCloud);
    }
    refresh();
    window.addEventListener(AVATAR_MARK_EVENT, refresh);
    window.addEventListener(GLYPH_UNLOCK_EVENT, refresh);
    return () => {
      window.removeEventListener(AVATAR_MARK_EVENT, refresh);
      window.removeEventListener(GLYPH_UNLOCK_EVENT, refresh);
    };
  }, [profile?.mark]);

  async function choose(next: ShareForceMark | null) {
    saveAvatarMark(next);
    setMark(next);
    if (CONVEX_ENABLED && user) {
      try {
        await setCloudMark({ mark: next ?? undefined });
      } catch {
        /* local mark still stands */
      }
    }
  }

  return { mark, choose, openMarks };
}
