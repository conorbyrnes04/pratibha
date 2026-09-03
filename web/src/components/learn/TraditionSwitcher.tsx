"use client";

import { useEffect, useId, useRef, useState } from "react";
import { InkGlyph } from "@/components/InkGlyph";
import { useT } from "@/components/LocaleProvider";
import { useLocalizedTrails } from "@/components/useLocalizedStudy";
import { TRADITION_TRAILS, type TraditionTrail } from "@/lib/learn/traditionTrails";

type TraditionSwitcherProps = {
  pathId: string | null;
  onSelectPath: (pathId: string) => void;
};

export function TraditionSwitcher({ pathId, onSelectPath }: TraditionSwitcherProps) {
  const t = useT();
  const trails = useLocalizedTrails(TRADITION_TRAILS);
  const current = trails.find((trail) => trail.id === pathId) ?? null;
  const [open, setOpen] = useState(false);
  const [previewId, setPreviewId] = useState<string | null>(null);
  const [compact, setCompact] = useState(false);
  const rootRef = useRef<HTMLDivElement | null>(null);
  const nameRef = useRef<HTMLSpanElement | null>(null);
  const menuId = useId();
  const name = current?.title ?? t("learn.choosePath");
  const preview = trails.find((trail) => trail.id === previewId) ?? null;

  useEffect(() => {
    const el = nameRef.current;
    if (!el) return;

    const MAX_REM = 1.22;
    const MIN_REM = 0.68;

    function fit() {
      let rem = MAX_REM;
      el.style.fontSize = `${rem}rem`;
      for (let i = 0; i < 16; i++) {
        const available = el.clientWidth;
        if (available <= 0) return;
        if (el.scrollWidth <= available + 0.5 || rem <= MIN_REM) return;
        rem = Math.max(MIN_REM, rem * (available / el.scrollWidth) * 0.97);
        el.style.fontSize = `${rem}rem`;
      }
    }

    fit();
    void document.fonts?.ready.then(fit);
    const observer = new ResizeObserver(fit);
    observer.observe(el.parentElement ?? el);
    return () => observer.disconnect();
  }, [name]);

  useEffect(() => {
    setOpen(false);
    setPreviewId(null);
  }, [pathId]);

  useEffect(() => {
    if (!open) return;
    function onPointer(event: MouseEvent) {
      if (!rootRef.current?.contains(event.target as Node)) setOpen(false);
    }
    function onKey(event: KeyboardEvent) {
      if (event.key !== "Escape") return;
      event.preventDefault();
      event.stopPropagation();
      setOpen(false);
    }
    document.addEventListener("mousedown", onPointer);
    window.addEventListener("keydown", onKey, true);
    return () => {
      document.removeEventListener("mousedown", onPointer);
      window.removeEventListener("keydown", onKey, true);
    };
  }, [open]);

  useEffect(() => {
    function onScroll() {
      setCompact(window.scrollY > 72);
    }
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  function pick(trail: TraditionTrail) {
    setOpen(false);
    onSelectPath(trail.id);
  }

  const essential = trails.filter((trail) => trail.essential);
  const traditions = trails.filter((trail) => !trail.essential);
  const distinctShort =
    current &&
    current.shortTitle.trim().toLowerCase() !== current.title.trim().toLowerCase()
      ? current.shortTitle
      : null;

  return (
    <div className={`learn-tradition-bar${compact ? " is-compact" : ""}`} ref={rootRef}>
      <div className="learn-tradition-bar__inner">
        <div
          className="learn-tradition-bar__mala"
          role="list"
          onPointerLeave={() => setPreviewId(null)}
        >
          {trails.map((trail) => (
            <button
              key={trail.id}
              type="button"
              role="listitem"
              className={`learn-tradition-bar__bead ${trail.id === pathId ? "is-current" : ""}`}
              aria-label={trail.title}
              aria-current={trail.id === pathId ? "true" : undefined}
              onPointerEnter={() => setPreviewId(trail.id)}
              onFocus={() => setPreviewId(trail.id)}
              onBlur={() => setPreviewId(null)}
              onClick={() => pick(trail)}
            >
              <InkGlyph
                glyph={trail.glyph}
                state={trail.id === pathId ? "recognized" : "arising"}
                size="sm"
                mask
              />
            </button>
          ))}
        </div>
        <p
          className={`learn-tradition-bar__whisper ${preview ? "is-on" : ""}`}
          aria-hidden
        >
          {preview?.title ?? "\u00a0"}
        </p>
        <button
          type="button"
          className="learn-tradition-bar__trigger"
          aria-haspopup="listbox"
          aria-expanded={open}
          aria-controls={menuId}
          aria-label={t("learn.choosePath")}
          onClick={() => setOpen((value) => !value)}
        >
          <span className="learn-tradition-bar__mark">
            <InkGlyph
              glyph={current?.glyph ?? "mandala"}
              state={current ? "arising" : "unmanifest"}
              size="lg"
              mask
            />
          </span>
          <span className="learn-tradition-bar__copy">
            <span className="learn-tradition-bar__name" ref={nameRef}>
              {name}
            </span>
            {distinctShort ? (
              <span className="learn-tradition-bar__short">{distinctShort}</span>
            ) : null}
          </span>
          <span className="learn-tradition-bar__chevron" aria-hidden />
        </button>
        {open ? (
          <ul id={menuId} role="listbox" className="learn-tradition-bar__menu">
            {essential.length > 0 ? (
              <li className="learn-tradition-bar__group" aria-hidden>
                {t("learn.essential")}
              </li>
            ) : null}
            {essential.map((trail) => (
              <li key={trail.id}>
                <button
                  type="button"
                  role="option"
                  aria-selected={trail.id === pathId}
                  className={`learn-tradition-bar__option ${trail.id === pathId ? "is-current" : ""}`}
                  onClick={() => pick(trail)}
                >
                  <InkGlyph glyph={trail.glyph} state={trail.id === pathId ? "arising" : "unmanifest"} size="md" mask />
                  <span>
                    <span className="learn-tradition-bar__option-title">{trail.title}</span>
                    <span className="learn-tradition-bar__option-lede">{trail.shortTitle}</span>
                  </span>
                </button>
              </li>
            ))}
            {traditions.length > 0 ? (
              <li className="learn-tradition-bar__group" aria-hidden>
                {t("learn.traditions")}
              </li>
            ) : null}
            {traditions.map((trail) => (
              <li key={trail.id}>
                <button
                  type="button"
                  role="option"
                  aria-selected={trail.id === pathId}
                  className={`learn-tradition-bar__option ${trail.id === pathId ? "is-current" : ""}`}
                  onClick={() => pick(trail)}
                >
                  <InkGlyph glyph={trail.glyph} state={trail.id === pathId ? "arising" : "unmanifest"} size="md" mask />
                  <span>
                    <span className="learn-tradition-bar__option-title">{trail.title}</span>
                    <span className="learn-tradition-bar__option-lede">{trail.shortTitle}</span>
                  </span>
                </button>
              </li>
            ))}
          </ul>
        ) : null}
      </div>
    </div>
  );
}
