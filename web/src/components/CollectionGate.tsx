"use client";

import { type ReactNode, useEffect, useMemo, useState } from "react";
import { AnimatePresence, motion, useReducedMotion, useScroll, useTransform } from "motion/react";
import { HERO_QUOTE_DWELL_MS, heroQuotesFor, nextHeroQuoteIndex } from "@/lib/heroQuotes";
import { useLocale, useT } from "@/components/LocaleProvider";
import { useLocalizedHeroQuotes } from "@/components/useLocalizedStudy";

type CollectionGateProps = {
  collection: string;
  title: string;
  mandalaSrc?: string | null;
  layoutId?: string;
  fallbackQuotes?: string[];
  glyph?: ReactNode;
  listen?: ReactNode;
};

export function CollectionGate({
  collection,
  title,
  mandalaSrc,
  layoutId,
  fallbackQuotes = [],
  glyph,
  listen,
}: CollectionGateProps) {
  const quotes = useMemo(
    () => heroQuotesFor(collection, fallbackQuotes),
    [collection, fallbackQuotes],
  );
  const reduceMotion = useReducedMotion();
  const { locale } = useLocale();
  const { scrollY } = useScroll();
  const scale = useTransform(scrollY, [0, 380], [1, 0.42]);
  const quoteOpacity = useTransform(scrollY, [0, 200, 360], [1, 0.78, 0]);
  const chevronOpacity = useTransform(scrollY, [0, 160, 260], [1, 0.7, 0]);
  const [index, setIndex] = useState(0);
  const { quote, pending } = useLocalizedHeroQuotes(quotes, index);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "auto" });
  }, [collection]);

  useEffect(() => {
    if (quotes.length === 0) return;
    setIndex(Math.floor(Math.random() * quotes.length));
  }, [collection, quotes]);

  useEffect(() => {
    if (reduceMotion || quotes.length < 2 || (locale !== "en" && pending)) return;
    const id = window.setInterval(() => {
      setIndex((i) => nextHeroQuoteIndex(i, quotes.length));
    }, HERO_QUOTE_DWELL_MS);
    return () => window.clearInterval(id);
  }, [locale, pending, quotes, reduceMotion]);

  const t = useT();

  function expandAgain() {
    window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" });
  }

  function onMandalaClick() {
    if (scrollY.get() > 56) {
      expandAgain();
      return;
    }
    if (quotes.length > 1) setIndex((i) => nextHeroQuoteIndex(i, quotes.length));
  }

  function descend() {
    document.getElementById("collection-text")?.scrollIntoView({
      behavior: reduceMotion ? "auto" : "smooth",
      block: "start",
    });
  }

  return (
    <section className="collection-gate" aria-label={t("reader.opening", { title })}>
      <div className="collection-gate__stage">
        <motion.div className="collection-gate__orb" style={{ scale }}>
        <button
          type="button"
          className="collection-gate__face"
          onClick={onMandalaClick}
          aria-label={
            quote
              ? t("reader.cycleQuote", { title, quote })
              : t("reader.returnOpening", { title })
          }
        >
          {mandalaSrc ? (
            <motion.span
              layoutId={layoutId}
              transition={{ type: "spring", stiffness: 260, damping: 32, mass: 0.9 }}
              className="collection-gate__mandala"
              style={{ backgroundImage: `url(${mandalaSrc})` }}
            />
          ) : (
            <span className="collection-gate__glyph">{glyph}</span>
          )}
          {quote ? (
            <motion.span className="collection-gate__quote" style={{ opacity: quoteOpacity }}>
              <AnimatePresence mode="wait">
                <motion.span
                  key={`${collection}-${index}-${quote}`}
                  initial={reduceMotion ? false : { opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={reduceMotion ? undefined : { opacity: 0 }}
                  transition={{ duration: reduceMotion ? 0 : 1.8, ease: [0.4, 0, 0.2, 1] }}
                >
                  “{quote}”
                </motion.span>
              </AnimatePresence>
            </motion.span>
          ) : null}
        </button>
        <motion.button
          type="button"
          className="hero-descent"
          style={{ opacity: chevronOpacity }}
          onClick={descend}
          aria-label={t("reader.scrollText")}
        >
          <span className="hero-descent__arrow" aria-hidden />
          <span className="hero-descent__arrow" aria-hidden />
          <span className="hero-descent__arrow" aria-hidden />
        </motion.button>
        </motion.div>
      </div>
      {listen ? <div className="collection-gate__listen">{listen}</div> : null}
    </section>
  );
}
