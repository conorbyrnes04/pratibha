"use client";

import Link from "next/link";
import { useT } from "@/components/LocaleProvider";
import { useLocalizedFields, useLocalizedStep, useLocalizedVerse } from "@/components/useLocalizedStudy";
import { InkGlyph } from "@/components/InkGlyph";
import { buttonVariants } from "@/components/ui/button";
import { ESSENTIAL_TRAIL_ID } from "@/lib/learn/traditionTrails";
import { learnHref } from "@/lib/learn/url";
import type { TrailSit } from "@/lib/learn/trail";
import { trailSumiGlyph } from "@/lib/sumiGlyphs";
import { displayCollectionName } from "@/lib/collectionLabels";
import { passagePreview } from "@/lib/verseLayers";
import type { VerseItem } from "@/lib/types";

function gateChatHref(verse: VerseItem | null, step: TrailSit["step"], back: string) {
  const params = new URLSearchParams();
  if (verse) params.set("verse_id", verse._id);
  params.set("mode", step.chatMode || "question");
  params.set("q", step.chatPrompt);
  params.set("back", back);
  return `/chat?${params.toString()}`;
}

export function TodayGate({
  sit,
  verse,
}: {
  sit: TrailSit;
  verse: VerseItem | null;
}) {
  const t = useT();
  const { node, walked, total, complete, rested, next } = sit;
  const step = useLocalizedStep(sit.step);
  const localizedVerse = useLocalizedVerse(verse);
  const extras = useLocalizedFields({
    section: node.sectionLabel,
    next_title: next?.title || "",
  });
  const gateHref = learnHref({
    pathId: ESSENTIAL_TRAIL_ID,
    trackId: node.trackId,
    stepId: node.stepId,
  });
  const trailHref = learnHref({ pathId: ESSENTIAL_TRAIL_ID });
  const nextHref = next
    ? learnHref({
        pathId: ESSENTIAL_TRAIL_ID,
        trackId: next.trackId,
        stepId: next.stepId,
      })
    : trailHref;
  const askHref = gateChatHref(localizedVerse, step, "/");
  const glyph = trailSumiGlyph(node.stepId);
  const begin = walked === 0 && !complete && !rested;
  const pathDone = complete && !rested;
  const recognized = complete || rested;

  let title = step.title;
  let lede = step.orientation;
  if (pathDone) {
    title = t("gate.pathComplete");
    lede = t("gate.pathCompleteLede");
  } else if (complete && rested) {
    title = t("gate.enoughToday");
    lede = t("gate.enoughLastGate");
  } else if (rested && next) {
    title = t("gate.enoughToday");
    lede = t("gate.tomorrowOpens", { title: extras.fields.next_title || next.title });
  }

  return (
    <section id="daily" className="today-gate scroll-mt-24">
      <div className="today-gate__mark" aria-hidden>
        <InkGlyph
          glyph={glyph}
          state={recognized ? "recognized" : "arising"}
          size="xl"
          mask
        />
      </div>

      <p className="passage-reading__meta">{extras.fields.section || node.sectionLabel}</p>
      <h2 className="library-header__title">{title}</h2>
      <p className="library-header__lede">{lede}</p>

      {!pathDone ? (
        <div className="today-gate__teaching">
          {rested ? (
            <p className="today-gate__key">{step.title}</p>
          ) : (
            <p className="today-gate__key">{step.keyIdea}</p>
          )}
          {localizedVerse ? (
            <p className="today-gate__verse">
              <span className="today-gate__verse-src">
                {displayCollectionName(localizedVerse.collection) || localizedVerse.collection}
              </span>
              {passagePreview(localizedVerse)}
            </p>
          ) : null}
          {!rested ? (
            <p className="today-gate__practice">
              <span>{t("common.practice")}</span> {step.practice}
            </p>
          ) : null}
        </div>
      ) : null}

      <div className="passage-reading__nav">
        {pathDone ? (
          <>
            <Link href={trailHref} className={buttonVariants()}>
              {t("gate.seeTrail")}
            </Link>
            <Link href="/read" className={buttonVariants({ variant: "secondary" })}>
              {t("gate.openLibrary")}
            </Link>
          </>
        ) : rested ? (
          <>
            <Link href={trailHref} className={buttonVariants()}>
              {t("gate.seeTrail")}
            </Link>
            {verse ? (
              <Link href={askHref} className={buttonVariants({ variant: "secondary" })}>
                {t("gate.askGate")}
              </Link>
            ) : (
              <Link href={gateHref} className={buttonVariants({ variant: "secondary" })}>
                {t("gate.revisitGate")}
              </Link>
            )}
          </>
        ) : (
          <>
            <Link href={gateHref} className={buttonVariants()}>
              {begin ? t("gate.beginPath") : t("gate.enterGate")}
            </Link>
            {verse ? (
              <Link href={askHref} className={buttonVariants({ variant: "secondary" })}>
                {t("gate.askGate")}
              </Link>
            ) : (
              <Link href={trailHref} className={buttonVariants({ variant: "secondary" })}>
                {t("gate.seeTrail")}
              </Link>
            )}
          </>
        )}
      </div>

      <p className="today-gate__count">
        {pathDone
          ? t("gate.gatesWalked", { count: total })
          : rested && next
            ? t("gate.walkedTodayTomorrow", { title: extras.fields.next_title || next.title })
            : rested
              ? t("gate.walkedToday")
              : walked === 0
                ? t("gate.firstGate")
                : t("gate.progress", {
                    walked,
                    walkedLabel: walked === 1 ? t("gate.gateOne") : t("gate.gateMany"),
                    remain: total - walked,
                    remainLabel: total - walked === 1 ? t("gate.remainOne") : t("gate.remainMany"),
                  })}
      </p>
      {rested && next && nextHref !== trailHref ? (
        <p className="today-gate__continue">
          <Link href={nextHref}>{t("gate.walkOneMore")}</Link>
        </p>
      ) : null}
    </section>
  );
}
