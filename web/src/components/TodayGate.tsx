import Link from "next/link";
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
  const { node, step, walked, total, complete, rested, next } = sit;
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
  const askHref = gateChatHref(verse, step, "/");
  const glyph = trailSumiGlyph(node.stepId);
  const begin = walked === 0 && !complete && !rested;
  const pathDone = complete && !rested;
  const recognized = complete || rested;

  let title = step.title;
  let lede = step.orientation;
  if (pathDone) {
    title = "The Path is complete";
    lede =
      "You have walked every gate on the essential spine. The trail is still there if you want to walk it again, or open a tradition from the Path.";
  } else if (complete && rested) {
    title = "Enough for today";
    lede = "You finished the last gate on the essential spine today. The trail is still there if you want to walk it again.";
  } else if (rested && next) {
    title = "Enough for today";
    lede = `Tomorrow opens ${next.title}.`;
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

      <p className="passage-reading__meta">{node.sectionLabel}</p>
      <h2 className="library-header__title">{title}</h2>
      <p className="library-header__lede">{lede}</p>

      {!pathDone ? (
        <div className="today-gate__teaching">
          {rested ? (
            <p className="today-gate__key">{step.title}</p>
          ) : (
            <p className="today-gate__key">{step.keyIdea}</p>
          )}
          {verse ? (
            <p className="today-gate__verse">
              <span className="today-gate__verse-src">
                {displayCollectionName(verse.collection) || verse.collection}
              </span>
              {passagePreview(verse)}
            </p>
          ) : null}
          {!rested ? (
            <p className="today-gate__practice">
              <span>Practice</span> {step.practice}
            </p>
          ) : null}
        </div>
      ) : null}

      <div className="passage-reading__nav">
        {pathDone ? (
          <>
            <Link href={trailHref} className={buttonVariants()}>
              See the trail
            </Link>
            <Link href="/read" className={buttonVariants({ variant: "secondary" })}>
              Open the library
            </Link>
          </>
        ) : rested ? (
          <>
            <Link href={trailHref} className={buttonVariants()}>
              See the trail
            </Link>
            {verse ? (
              <Link href={askHref} className={buttonVariants({ variant: "secondary" })}>
                Ask this gate
              </Link>
            ) : (
              <Link href={gateHref} className={buttonVariants({ variant: "secondary" })}>
                Revisit today&apos;s gate
              </Link>
            )}
          </>
        ) : (
          <>
            <Link href={gateHref} className={buttonVariants()}>
              {begin ? "Begin the path" : "Enter this gate"}
            </Link>
            {verse ? (
              <Link href={askHref} className={buttonVariants({ variant: "secondary" })}>
                Ask this gate
              </Link>
            ) : (
              <Link href={trailHref} className={buttonVariants({ variant: "secondary" })}>
                See the trail
              </Link>
            )}
          </>
        )}
      </div>

      <p className="today-gate__count">
        {pathDone
          ? `${total} gates walked`
          : rested && next
            ? `Walked today · tomorrow opens ${next.title}`
            : rested
              ? "Walked today"
              : walked === 0
                ? "The first gate"
                : `${walked} ${walked === 1 ? "gate" : "gates"} walked · ${total - walked} ${
                    total - walked === 1 ? "remains" : "remain"
                  }`}
      </p>
      {rested && next && nextHref !== trailHref ? (
        <p className="today-gate__continue">
          <Link href={nextHref}>Walk one more anyway</Link>
        </p>
      ) : null}
    </section>
  );
}
