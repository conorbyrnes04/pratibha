import { useEffect, useMemo, useState } from "@lynx-js/react";
import { C, SERIF } from "../lib/theme";
import { HERO_QUOTE_DWELL_MS, heroQuotesFor, nextHeroQuoteIndex } from "../lib/heroQuotes";
import { SumiGlyph } from "./SumiGlyph";
import { sumiGlyph } from "../lib/sumi";

export function CollectionGate({
  collection,
  collapse,
  fallbackQuotes = [],
  onExpand,
  onDescend,
}: {
  collection: string;
  /** 0 = fully open, 1 = fully shrunk. */
  collapse: number;
  fallbackQuotes?: string[];
  onExpand: () => void;
  onDescend: () => void;
}) {
  const quotes = useMemo(
    () => heroQuotesFor(collection, fallbackQuotes),
    [collection, fallbackQuotes],
  );
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (quotes.length === 0) return;
    setIndex(Math.floor(Math.random() * quotes.length));
    if (quotes.length < 2) return;
    const id = setInterval(() => {
      setIndex((i) => nextHeroQuoteIndex(i, quotes.length));
    }, HERO_QUOTE_DWELL_MS);
    return () => clearInterval(id);
  }, [collection, quotes]);

  const quote = quotes[index] || "";
  const t = Math.max(0, Math.min(1, collapse));
  const size = Math.round(280 - t * 150);
  const quoteOpacity = 1 - Math.min(1, t * 1.4);
  const chevronOpacity = 1 - Math.min(1, t * 2.2);

  function onFaceTap() {
    if (t > 0.2) {
      onExpand();
      return;
    }
    if (quotes.length > 1) setIndex((i) => nextHeroQuoteIndex(i, quotes.length));
  }

  return (
    <view style={{ alignItems: "center", marginBottom: 18, marginTop: 8 }}>
      <view
        bindtap={onFaceTap}
        style={{
          position: "relative",
          width: `${size}px`,
          height: `${size}px`,
          borderRadius: `${size / 2}px`,
          backgroundColor: C.card,
          alignItems: "center",
          justifyContent: "center",
          overflow: "hidden",
        }}
      >
        <SumiGlyph glyph={sumiGlyph(collection) || "mandala"} state="arising" size={Math.round(size * 0.46)} breath />
        {quote && quoteOpacity > 0.05 ? (
          <view
            style={{
              position: "absolute",
              left: 16,
              right: 16,
              alignItems: "center",
              opacity: quoteOpacity,
            }}
          >
            <text
              style={{
                color: C.gold,
                fontSize: size > 200 ? 16 : 13,
                lineHeight: 1.4,
                textAlign: "center",
                fontFamily: SERIF,
              }}
            >
              “{quote}”
            </text>
          </view>
        ) : null}
      </view>
      {chevronOpacity > 0.08 ? (
        <view bindtap={onDescend} style={{ alignItems: "center", marginTop: 12, opacity: chevronOpacity }}>
          <text style={{ color: C.gold, fontSize: 14, lineHeight: 0.7 }}>⌄</text>
          <text style={{ color: C.gold, fontSize: 14, lineHeight: 0.7, opacity: 0.7 }}>⌄</text>
          <text style={{ color: C.gold, fontSize: 14, lineHeight: 0.7, opacity: 0.45 }}>⌄</text>
        </view>
      ) : null}
    </view>
  );
}

export function firstCatalogLine(text: string): string {
  const clean = text.replace(/\s+/g, " ").trim();
  const m = clean.match(/^(.+?[.!?])(?:\s|$)/);
  return m?.[1] || clean.slice(0, 140);
}
