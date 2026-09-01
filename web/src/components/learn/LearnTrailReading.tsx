"use client";

import { useEffect, useState } from "react";
import { LayerBlock } from "@/components/LayerBlock";
import { ListenButton } from "@/components/ListenButton";
import { OriginalReliabilityBadge } from "@/components/OriginalReliabilityBadge";
import { displayCollectionName } from "@/lib/collectionLabels";
import { getVerse } from "@/lib/api";
import { displayPassageLocation, displayPassageTitle } from "@/lib/passageTitles";
import type { VerseItem } from "@/lib/types";
import { getStudyLayers, layerText, passagePreview, practiceText } from "@/lib/verseLayers";
import { useT } from "@/components/LocaleProvider";
import { useLocalizedVerse } from "@/components/useLocalizedStudy";

export function LearnTrailReading({
  item,
  gateTitle,
  onBack,
}: {
  item: VerseItem;
  gateTitle: string;
  onBack: () => void;
}) {
  const t = useT();
  const [showOriginal, setShowOriginal] = useState(true);
  const [full, setFull] = useState<VerseItem | null>(null);

  useEffect(() => {
    let cancelled = false;
    setFull(null);
    getVerse(item._id)
      .then((verse) => {
        if (!cancelled) setFull(verse);
      })
      .catch(() => {
        if (!cancelled) setFull(null);
      });
    return () => {
      cancelled = true;
    };
  }, [item._id]);

  const study = useLocalizedVerse(full || item) || full || item;
  const layers = getStudyLayers(study);
  const originalLayer = layers.find((l) => l.kind === "original");
  const iastLayer = layers.find((l) => l.kind === "iast");
  const translationLayer = layers.find((l) => l.kind === "translation");
  const commentaryBody = layerText(study, "commentary");
  const practice = practiceText(study);
  const passageLocation = displayPassageLocation(item);

  return (
    <div className="learn-trail-reading" aria-labelledby="learn-trail-reading-title">
      <header className="learn-trail-reading__bar">
        <div className="learn-trail-reading__bar-copy">
          <button
            type="button"
            id="learn-trail-reading-back"
            className="passage-reading__meta learn-trail-gate__back"
            onClick={onBack}
          >
            {t("learn.thisGate")}
          </button>
          <p className="learn-trail-reading__gate">{gateTitle}</p>
        </div>
        <ListenButton verseId={item._id} variant="header" />
      </header>

      <p className="passage-reading__meta">
        {displayCollectionName(item.collection) || "Pratibha"}
        {passageLocation ? ` · ${passageLocation}` : ""}
      </p>
      <h2 id="learn-trail-reading-title" className="passage-reading__title">
        {displayPassageTitle(study)}
      </h2>
      <OriginalReliabilityBadge item={study} />

      {originalLayer || iastLayer ? (
        <div className="passage-reading__toolbar">
          <button
            type="button"
            className="passage-reading__toggle"
            onClick={() => setShowOriginal((v) => !v)}
          >
            {showOriginal ? t("layers.hideOriginal") : t("layers.showOriginal")}
          </button>
        </div>
      ) : null}

      {showOriginal && originalLayer ? <LayerBlock layer={originalLayer} variant="plain" /> : null}
      {showOriginal && iastLayer ? <LayerBlock layer={iastLayer} variant="plain" /> : null}
      {translationLayer ? (
        <LayerBlock layer={translationLayer} variant="plain" verseId={item._id} />
      ) : originalLayer ? null : (
        <section className="passage-layer passage-layer--translation">
          <ListenButton verseId={item._id} section="translation" variant="layer" />
          <h2 className="passage-layer__label">{t("layers.translation")}</h2>
          <p className="reading-prose mt-4">{passagePreview(study)}</p>
        </section>
      )}
      {commentaryBody ? (
        <LayerBlock
          layer={{ kind: "commentary", label: t("layers.commentary"), body: commentaryBody }}
          variant="plain"
          verseId={item._id}
        />
      ) : null}
      {practice ? (
        <LayerBlock
          layer={{ kind: "practice", label: t("layers.practice"), body: practice }}
          variant="plain"
          verseId={item._id}
        />
      ) : null}
    </div>
  );
}
