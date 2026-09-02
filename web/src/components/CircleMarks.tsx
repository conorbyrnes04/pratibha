"use client";

import { useMutation, useQuery } from "convex/react";
import { api } from "../../convex/_generated/api";
import type { Id } from "../../convex/_generated/dataModel";
import { useAuth } from "@/components/AuthProvider";
import { CONVEX_ENABLED } from "@/lib/convexConfigured";
import { QuietBoundary } from "@/components/SanghaBoundary";
import { useT } from "@/components/LocaleProvider";

export function CircleSitButton({ commentaryId }: { commentaryId: Id<"student_commentaries"> }) {
  return (
    <QuietBoundary>
      <CircleSitButtonInner commentaryId={commentaryId} />
    </QuietBoundary>
  );
}

function CircleSitButtonInner({ commentaryId }: { commentaryId: Id<"student_commentaries"> }) {
  const t = useT();
  const { user } = useAuth();
  const meta = useQuery(api.circleSits.meta, CONVEX_ENABLED ? { commentaryId } : "skip");
  const toggle = useMutation(api.circleSits.toggle);

  if (meta === undefined) return null;
  const count = meta.count;
  const label =
    count === 0 ? null : count === 1 ? t("circle.satOne") : t("circle.satCount", { count });

  return (
    <span className="inline-flex flex-wrap items-center gap-x-3 gap-y-1">
      {label ? (
        <span className="font-sans text-[11px] uppercase tracking-[0.14em] text-stone-500">{label}</span>
      ) : null}
      {user ? (
        <button
          type="button"
          className="font-sans text-[11px] uppercase tracking-[0.14em] text-amber-200/70 hover:text-amber-100"
          onClick={() => void toggle({ commentaryId }).catch(() => undefined)}
        >
          {meta.mine ? t("circle.satWithMine") : t("circle.satWith")}
        </button>
      ) : null}
    </span>
  );
}

export function CircleWatchButton({ verseId }: { verseId: string }) {
  return (
    <QuietBoundary>
      <CircleWatchButtonInner verseId={verseId} />
    </QuietBoundary>
  );
}

function CircleWatchButtonInner({ verseId }: { verseId: string }) {
  const t = useT();
  const { user } = useAuth();
  const meta = useQuery(api.circleWatches.meta, CONVEX_ENABLED && user ? { verseId } : "skip");
  const toggle = useMutation(api.circleWatches.toggle);
  if (!user) return null;

  return (
    <button
      type="button"
      className="font-sans text-xs uppercase tracking-[0.16em] text-amber-200/70 hover:text-amber-100"
      onClick={() => void toggle({ verseId }).catch(() => undefined)}
    >
      {meta?.watching ? t("circle.watching") : t("circle.watch")}
    </button>
  );
}
