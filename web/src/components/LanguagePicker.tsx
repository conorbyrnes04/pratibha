"use client";

import { useEffect, useRef, useState } from "react";
import { Languages } from "lucide-react";
import { LOCALES, LOCALE_META } from "@/i18n";
import { useLocale } from "@/components/LocaleProvider";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function LanguagePicker({
  variant = "header",
  className,
}: {
  variant?: "header" | "panel";
  className?: string;
}) {
  const { locale, setLocale, t } = useLocale();
  const [open, setOpen] = useState(false);
  const rootRef = useRef<HTMLDivElement>(null);
  const current = LOCALE_META[locale];

  useEffect(() => {
    if (!open) return;
    function onPointerDown(event: MouseEvent) {
      if (!rootRef.current?.contains(event.target as Node)) setOpen(false);
    }
    function onKey(event: KeyboardEvent) {
      if (event.key === "Escape") setOpen(false);
    }
    document.addEventListener("mousedown", onPointerDown);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("mousedown", onPointerDown);
      document.removeEventListener("keydown", onKey);
    };
  }, [open]);

  if (variant === "panel") {
    return (
      <div className={cn("space-y-3", className)}>
        <p className="font-sans text-xs uppercase tracking-[0.22em] text-stone-400">{t("language.title")}</p>
        <p className="soft font-sans text-sm leading-relaxed">{t("language.lede")}</p>
        <div className="grid gap-2 sm:grid-cols-2">
          {LOCALES.map((id) => {
            const meta = LOCALE_META[id];
            const active = id === locale;
            return (
              <button
                key={id}
                type="button"
                onClick={() => setLocale(id)}
                aria-pressed={active}
                className={cn(
                  "rounded-xl border px-3 py-2.5 text-start font-sans text-sm transition",
                  active
                    ? "border-amber-200/45 bg-amber-200/10 text-amber-50"
                    : "border-amber-200/12 bg-white/[0.02] text-stone-200 hover:border-amber-200/28 hover:bg-white/[0.04]",
                )}
              >
                <span className="block">{meta.nativeName}</span>
              </button>
            );
          })}
        </div>
      </div>
    );
  }

  return (
    <div ref={rootRef} className={cn("relative", className)}>
      <Button
        type="button"
        variant="ghost"
        size="sm"
        onClick={() => setOpen((value) => !value)}
        aria-expanded={open}
        aria-haspopup="listbox"
        aria-label={t("language.choose")}
        className="h-9 gap-1.5 px-2 font-sans text-xs tracking-[0.08em] text-stone-300 hover:text-amber-100"
      >
        <Languages className="size-3.5 opacity-80" aria-hidden />
        <span className="hidden sm:inline">{current.nativeName}</span>
      </Button>
      {open ? (
        <div
          role="listbox"
          aria-label={t("language.label")}
          className="absolute inset-inline-end-0 top-[calc(100%+0.55rem)] z-50 min-w-[13.5rem] overflow-hidden rounded-xl border border-amber-200/15 bg-[#12101c]/96 py-1 shadow-2xl backdrop-blur-xl"
        >
          {LOCALES.map((id) => {
            const meta = LOCALE_META[id];
            const active = id === locale;
            return (
              <button
                key={id}
                type="button"
                role="option"
                aria-selected={active}
                onClick={() => {
                  setLocale(id);
                  setOpen(false);
                }}
                className={cn(
                  "block w-full px-3 py-2.5 text-start font-sans text-sm transition hover:bg-white/5 hover:text-amber-100",
                  active ? "text-amber-100" : "text-stone-200",
                )}
              >
                {meta.nativeName}
              </button>
            );
          })}
        </div>
      ) : null}
    </div>
  );
}
