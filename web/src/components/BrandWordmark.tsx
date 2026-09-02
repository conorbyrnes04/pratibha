"use client";

import { useEffect, useState } from "react";
import { WORDMARKS, subscribeWordmark, type WordmarkDef } from "@/lib/wordmarks";
import { useT } from "@/components/LocaleProvider";

export function BrandWordmark() {
  const t = useT();
  const [mark, setMark] = useState<WordmarkDef>(WORDMARKS[0]);

  useEffect(() => {
    for (const item of WORDMARKS) {
      const preload = new window.Image();
      preload.src = item.src;
    }
    return subscribeWordmark(setMark);
  }, []);

  return (
    <span
      className="brand-wordmark brand-wordmark--art brand-wordmark--has-tagline"
      data-wordmark={mark?.id ?? ""}
      suppressHydrationWarning
    >
      {WORDMARKS.map((item) => {
        const on = item.id === mark.id;
        return (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            key={item.id}
            src={item.src}
            alt={on ? t("brand.name") : ""}
            aria-hidden={on ? undefined : true}
            draggable={false}
            className={`brand-wordmark__art${on ? " is-on" : ""}`}
          />
        );
      })}
    </span>
  );
}
