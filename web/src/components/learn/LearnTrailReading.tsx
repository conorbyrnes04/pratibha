"use client";

import { useState } from "react";
import { LayerBlock } from "@/components/LayerBlock";
import { ListenButton } from "@/components/ListenButton";
import { OriginalReliabilityBadge } from "@/components/OriginalReliabilityBadge";
import { displayCollectionName } from "@/lib/collectionLabels";
import { displayPassageLocation, displayPassageTitle } from "@/lib/passageTitles";
import type { VerseItem } from "@/lib/types";
import { getStudyLayers, passagePreview } from "@/lib/verseLayers";

export function LearnTrailReading({
  item,
  gateTitle,
  onBack,
}: {
  item: VerseItem;
  gateTitle: string;
  onBack: () => void;
}) {
  const [showOriginal, setShowOriginal] = useState(true);
  const layers = getStudyLayers(item);
  const originalLayer = layers.find((l) => l.kind === "original");
  const iastLayer = layers.find((l) => l.kind === "iast");
  const translationLayer = layers.find((l) => l.kind === "translation");
  const commentaryLayer = layers.find((l) => l.kind === "commentary");
  const practiceLayer = layers.find((l) => l.kind === "practice");
  const passageLocation = displayPassageLocation(item);

  return (
    <div className="learn-trail-reading" aria-labelledby="learn-trail-reading-title">
      <header className="learn-trail-reading__bar">
        <button
          type="button"
          id="learn-trail-reading-back"
          className="passage-reading__meta learn-trail-gate__back"
          onClick={onBack}
        >
          ← This gate
        </button>
        <p className="learn-trail-reading__gate">{gateTitle}</p>
      </header>

      <p className="passage-reading__meta">
        {displayCollectionName(item.collection) || "Pratibha"}
        {passageLocation ? ` · ${passageLocation}` : ""}
      </p>
      <h2 id="learn-trail-reading-title" className="passage-reading__title">
        {displayPassageTitle(item)}
      </h2>
      <OriginalReliabilityBadge item={item} />

      {originalLayer || iastLayer ? (
        <div className="passage-reading__toolbar">
          <button
            type="button"
            className="passage-reading__toggle"
            onClick={() => setShowOriginal((v) => !v)}
          >
            {showOriginal ? "Hide original" : "Show original"}
          </button>
          <ListenButton verseId={item._id} />
        </div>
      ) : (
        <ListenButton verseId={item._id} />
      )}

      {showOriginal && originalLayer ? <LayerBlock layer={originalLayer} variant="plain" /> : null}
      {showOriginal && iastLayer ? <LayerBlock layer={iastLayer} variant="plain" /> : null}
      {translationLayer ? (
        <LayerBlock layer={translationLayer} variant="plain" />
      ) : originalLayer ? null : (
        <section className="passage-layer passage-layer--translation">
          <h2 className="passage-layer__label">Translation</h2>
          <p className="reading-prose mt-4">{passagePreview(item)}</p>
        </section>
      )}
      {commentaryLayer ? <LayerBlock layer={commentaryLayer} variant="plain" /> : null}
      {practiceLayer ? <LayerBlock layer={practiceLayer} variant="plain" /> : null}
    </div>
  );
}
