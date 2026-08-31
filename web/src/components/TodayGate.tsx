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

export function TodayGate({
  sit,
  verse,
}: {
  sit: TrailSit;
  verse: VerseItem | null;
}) {
  const { node, step, walked, total, complete } = sit;
  const gateHref = learnHref({
    pathId: ESSENTIAL_TRAIL_ID,
    trackId: node.trackId,
    stepId: node.stepId,
  });
  const trailHref = learnHref({ pathId: ESSENTIAL_TRAIL_ID });
  const glyph = trailSumiGlyph(node.stepId);
  const begin = walked === 0 && !complete;

  return (
    <section id="daily" className="today-gate scroll-mt-24">
      <div className="today-gate__mark" aria-hidden>
        <InkGlyph
          glyph={glyph}
          state={complete ? "recognized" : "arising"}
          size="xl"
          mask
        />
      </div>

      <p className="passage-reading__meta">{node.sectionLabel}</p>
      <h2 className="library-header__title">{complete ? "The Path is complete" : step.title}</h2>
      <p className="library-header__lede">
        {complete
          ? "You have walked every gate on the essential spine. The trail is still there if you want to walk it again, or open a tradition from the Path."
          : step.orientation}
      </p>

      {!complete ? (
        <div className="today-gate__teaching">
          <p className="today-gate__key">{step.keyIdea}</p>
          {verse ? (
            <p className="today-gate__verse">
              <span className="today-gate__verse-src">
                {displayCollectionName(verse.collection) || verse.collection}
              </span>
              {passagePreview(verse)}
            </p>
          ) : null}
          <p className="today-gate__practice">
            <span>Practice</span> {step.practice}
          </p>
        </div>
      ) : null}

      <div className="passage-reading__nav">
        {complete ? (
          <>
            <Link href={trailHref} className={buttonVariants()}>
              See the trail
            </Link>
            <Link href="/read" className={buttonVariants({ variant: "secondary" })}>
              Open the library
            </Link>
          </>
        ) : (
          <>
            <Link href={gateHref} className={buttonVariants()}>
              {begin ? "Begin the path" : "Enter this gate"}
            </Link>
            <Link href={trailHref} className={buttonVariants({ variant: "secondary" })}>
              See the trail
            </Link>
          </>
        )}
      </div>

      <p className="today-gate__count">
        {complete
          ? `${total} gates walked`
          : walked === 0
            ? "The first gate"
            : `${walked} ${walked === 1 ? "gate" : "gates"} walked · ${total - walked} ${
                total - walked === 1 ? "remains" : "remain"
              }`}
      </p>
    </section>
  );
}
