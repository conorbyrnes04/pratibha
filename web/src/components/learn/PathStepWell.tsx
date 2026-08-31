"use client";

import { useEffect, useState, type ReactNode } from "react";
import Link from "next/link";
import { getVerse } from "@/lib/api";
import { JournalPanel } from "@/components/JournalPanel";
import { ListenButton } from "@/components/ListenButton";
import { OriginalReliabilityBadge } from "@/components/OriginalReliabilityBadge";
import { PassageMaturityBadge } from "@/components/learn/PassageMaturityBadge";
import { buttonVariants } from "@/components/ui/button";
import { matchStepItem, resolveById } from "@/lib/learn/passages";
import { learnHref } from "@/lib/learn/url";
import type { LearningStepSpec } from "@/lib/learningPaths";
import { learnStepContextId } from "@/lib/journalStorage";
import { displayCollectionName } from "@/lib/collectionLabels";
import { displayPassageLocation, displayPassageTitle } from "@/lib/passageTitles";
import type { VerseItem } from "@/lib/types";
import { passagePreview } from "@/lib/verseLayers";

function actionLabel(chatMode?: string): string {
  if (chatMode === "practice") return "Practice with it";
  if (chatMode === "compare") return "Compare traditions";
  if (chatMode === "explain") return "Understand it";
  return "Ask about it";
}

function PassageCard({
  item,
  primary = false,
  backHref,
  onOpen,
}: {
  item: VerseItem;
  primary?: boolean;
  backHref?: string;
  onOpen?: (item: VerseItem) => void;
}) {
  const className = `library-passage ${primary ? "" : "opacity-90"}`;
  const inner = (
    <>
      <p className="library-passage__meta">
        {displayCollectionName(item.collection)}
        {displayPassageLocation(item) ? ` · ${displayPassageLocation(item)}` : ""}
      </p>
      <h5 className="library-passage__title">{displayPassageTitle(item)}</h5>
      {primary ? <p className="library-passage__preview line-clamp-2">{passagePreview(item)}</p> : null}
    </>
  );
  if (onOpen) {
    return (
      <button type="button" className={className} onClick={() => onOpen(item)}>
        {inner}
      </button>
    );
  }
  const href = backHref
    ? `/read/${encodeURIComponent(item._id)}?back=${encodeURIComponent(backHref)}`
    : `/read/${encodeURIComponent(item._id)}`;
  return (
    <Link href={href} className={className}>
      {inner}
    </Link>
  );
}

type PathStepWellProps = {
  trackId: string;
  trackTitle: string;
  step: LearningStepSpec;
  items: VerseItem[];
  pathId?: string | null;
  onOpenPassage?: (item: VerseItem) => void;
  children?: ReactNode;
};

export function PathStepWell({
  trackId,
  trackTitle,
  step,
  items,
  pathId,
  onOpenPassage,
  children,
}: PathStepWellProps) {
  const [pinned, setPinned] = useState<VerseItem | null>(null);
  const catalogItem = matchStepItem(step, items);
  const item = catalogItem || pinned;

  useEffect(() => {
    if (catalogItem || !step.passageId) {
      setPinned(null);
      return;
    }
    let cancelled = false;
    getVerse(step.passageId)
      .then((verse) => {
        if (!cancelled) setPinned(verse);
      })
      .catch(() => {
        if (!cancelled) setPinned(null);
      });
    return () => {
      cancelled = true;
    };
  }, [catalogItem, step.passageId]);

  const supporting = (step.supportingPassageIds || [])
    .map((id) => resolveById(items, id))
    .filter((v): v is VerseItem => Boolean(v));
  const backHref = learnHref({
    pathId,
    trackId,
    stepId: step.id,
  });
  const readHref = item
    ? `/read/${encodeURIComponent(item._id)}?back=${encodeURIComponent(backHref)}`
    : `/read`;
  const chatParams = new URLSearchParams();
  if (item) chatParams.set("verse_id", item._id);
  chatParams.set("mode", step.chatMode || "question");
  chatParams.set("q", step.chatPrompt);
  chatParams.set("back", backHref);
  const chatHref = `/chat?${chatParams.toString()}`;

  return (
    <div className="mt-4 space-y-4">
      {children}

      <p className="reading-prose max-w-[var(--reading-measure)] leading-relaxed text-stone-200">
        {step.teaching}
      </p>

      <div className="passage-practice--plain mt-6">
        <p className="passage-layer__label">Key idea</p>
        <p className="passage-practice__body">{step.keyIdea}</p>
      </div>

      {step.misconception ? (
        <div className="mt-5 max-w-[var(--reading-measure)] border-t border-rose-300/20 pt-4">
          <p className="font-sans text-xs uppercase tracking-[0.16em] text-rose-200/80">
            Common misunderstanding
          </p>
          <p className="mt-2 text-sm leading-relaxed text-stone-200">{step.misconception}</p>
        </div>
      ) : null}

      <div>
        <p className="layer-heading">Study these passages</p>
        <div className="mt-2 space-y-2">
          {item ? (
            <>
              <PassageCard item={item} primary backHref={backHref} onOpen={onOpenPassage} />
              <PassageMaturityBadge item={item} />
              <OriginalReliabilityBadge item={item} />
              <ListenButton verseId={item._id} />
            </>
          ) : (
            <p className="rounded-2xl border border-rose-300/25 bg-rose-300/5 p-3 font-sans text-sm text-stone-200">
              Primary passage missing from the Library
              {step.passageId ? (
                <>
                  {" "}
                  (<code className="text-rose-100/90">{step.passageId}</code>)
                </>
              ) : null}
              . Supporting texts below may still be available; the path pin needs a corpus fix.
            </p>
          )}
          {supporting.map((sv) => (
            <PassageCard key={sv._id} item={sv} backHref={backHref} onOpen={onOpenPassage} />
          ))}
        </div>
      </div>

      <div className="passage-practice--plain">
        <p className="passage-layer__label">Practice</p>
        <p className="passage-practice__body">{step.practice}</p>
      </div>

      {item ? (
        <JournalPanel passage={item} prompt={step.journalPrompt} />
      ) : (
        <JournalPanel
          contextId={learnStepContextId(trackId, step.id)}
          contextTitle={`${trackTitle} · ${step.title}`}
          prompt={step.journalPrompt}
        />
      )}

      <div className="flex flex-wrap gap-2 pt-1">
        {item && onOpenPassage ? (
          <button type="button" className={buttonVariants({ size: "sm" })} onClick={() => onOpenPassage(item)}>
            Open passage
          </button>
        ) : (
          <Link href={readHref} className={buttonVariants({ size: "sm" })}>
            {item ? "Open in Library" : "Browse Library"}
          </Link>
        )}
        <Link href={chatHref} className={buttonVariants({ variant: "secondary", size: "sm" })}>
          {pathId ? "Ask this gate" : actionLabel(step.chatMode)}
        </Link>
        <Link href="/journal" className={buttonVariants({ variant: "secondary", size: "sm" })}>
          All journal notes
        </Link>
      </div>
    </div>
  );
}
