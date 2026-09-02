"use client";

import { useEffect, useState } from "react";
import {
  WORDMARKS,
  WORDMARK_CYCLE_MS,
  advanceWordmark,
  pickSessionWordmark,
  type WordmarkDef,
} from "@/lib/wordmarks";

export function BrandWordmark() {
  const [mark, setMark] = useState<WordmarkDef>(WORDMARKS[0]);

  useEffect(() => {
    for (const item of WORDMARKS) {
      const preload = new window.Image();
      preload.src = item.src;
    }
    setMark(pickSessionWordmark());
    const id = window.setInterval(() => {
      setMark((current) => advanceWordmark(current.id));
    }, WORDMARK_CYCLE_MS);
    return () => window.clearInterval(id);
  }, []);

  return (
    <span
      className="brand-wordmark brand-wordmark--art brand-wordmark--has-tagline"
      data-wordmark={mark.id}
      suppressHydrationWarning
    >
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={mark.src}
        alt="pratibhā"
        draggable={false}
        className="brand-wordmark__art block h-[2.65rem] w-auto max-w-[min(16rem,58vw)] object-contain object-left"
      />
    </span>
  );
}
