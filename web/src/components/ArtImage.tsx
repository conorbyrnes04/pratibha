"use client";

import { useEffect, useState, type CSSProperties, type ReactNode } from "react";
import { ART_OVERLAY, pickArtSrc, type ArtOverlayKind } from "@/lib/collectionImages";
import { useT } from "@/components/LocaleProvider";

/**
 * Thangka-style artwork helpers with graceful degradation.
 *
 * If a generated asset is missing (or fails to load) the element simply removes
 * itself, so the existing design shows through with no broken-image icon and no
 * layout jump — the art is always additive, never load-bearing.
 */

type ArtBackdropVariant = "hero" | "card" | "banner" | "subtle";

const VARIANT_DEFAULTS: Record<
  ArtBackdropVariant,
  { opacity: number; overlay: ArtOverlayKind; position: string }
> = {
  hero: { opacity: 0.42, overlay: "hero", position: "center 28%" },
  card: { opacity: 0.28, overlay: "card", position: "center 22%" },
  banner: { opacity: 0.48, overlay: "banner", position: "center 30%" },
  subtle: { opacity: 0.18, overlay: "card", position: "center 25%" },
};

type ArtBackdropProps = {
  /** Public path, e.g. "/generated/bg-hero.jpg". */
  src?: string;
  /** Optional rotating pool — when set, cycles through natural variants. */
  srcs?: string[];
  /** Rotation interval in ms when `srcs` has 2+ images (default 18s). */
  rotateMs?: number;
  /** Preset density / scrim — prefer this over one-off opacity values. */
  variant?: ArtBackdropVariant;
  /** Base opacity of the artwork layer (0–1). Overrides variant default. */
  opacity?: number;
  /** Extra classes for the artwork <img> (positioning is handled here). */
  className?: string;
  /** Overlay gradient classes for text legibility. Overrides variant default. */
  overlayClassName?: string;
  /** Named overlay from ART_OVERLAY when overlayClassName is omitted. */
  overlay?: ArtOverlayKind;
  /** object-position, defaults from variant. */
  position?: string;
  /** Eager-load hero art above the fold. */
  priority?: boolean;
};

/**
 * Absolutely-positioned, full-bleed background artwork + legibility overlay.
 * Drop inside a `position: relative; overflow: hidden` container; keep real
 * content in a sibling with a higher stacking context (e.g. `relative z-10`).
 * Pass `srcs` to crossfade through nature photo variants.
 */
export function ArtBackdrop({
  src,
  srcs,
  rotateMs = 18000,
  variant = "hero",
  opacity,
  className = "",
  overlayClassName,
  overlay,
  position,
  priority = false,
}: ArtBackdropProps) {
  const defaults = VARIANT_DEFAULTS[variant];
  const pool = (srcs && srcs.length > 0 ? srcs : src ? [src] : []).filter(Boolean);
  const [index, setIndex] = useState(0);
  const [failed, setFailed] = useState<Set<string>>(() => new Set());
  const [phase, setPhase] = useState<"loading" | "ready" | "error">("loading");

  const poolKey = pool.join("|");
  useEffect(() => {
    setIndex(0);
    setFailed(new Set());
    setPhase("loading");
  }, [poolKey]);

  const livePool = pool.filter((p) => !failed.has(p));
  const activeSrc = livePool.length > 0 ? livePool[index % livePool.length] : null;

  useEffect(() => {
    if (livePool.length < 2 || rotateMs <= 0) return;
    const id = window.setInterval(() => {
      setIndex((i) => (i + 1) % livePool.length);
    }, rotateMs);
    return () => window.clearInterval(id);
  }, [livePool.length, poolKey, rotateMs]);

  if (!activeSrc || phase === "error") return null;

  const resolvedOpacity = opacity ?? defaults.opacity;
  const resolvedPosition = position ?? defaults.position;
  const resolvedOverlay =
    overlayClassName ?? ART_OVERLAY[overlay ?? defaults.overlay];
  const imgStyle = {
    "--art-opacity": String(resolvedOpacity),
    objectPosition: resolvedPosition,
  } as CSSProperties;

  return (
    <div aria-hidden className="pointer-events-none absolute inset-0 overflow-hidden">
      {phase === "loading" ? <div className="art-placeholder absolute inset-0" /> : null}
      <img
        key={activeSrc}
        src={activeSrc}
        alt=""
        loading={priority ? "eager" : "lazy"}
        decoding="async"
        onLoad={() => setPhase("ready")}
        onError={() => {
          setFailed((prev) => {
            const next = new Set(prev);
            next.add(activeSrc);
            return next;
          });
          setPhase("loading");
        }}
        style={imgStyle}
        className={`art-reveal absolute inset-0 h-full w-full object-cover ${
          phase === "ready" ? "art-reveal--in" : ""
        } ${className}`}
      />
      <div className={`absolute inset-0 ${resolvedOverlay}`} />
    </div>
  );
}

/** Stable random pick from a pool (client-only; avoids SSR flicker). */
export function useArtSrc(pool: string[], seed?: string): string {
  const [src, setSrc] = useState(() => pickArtSrc(pool, seed ?? "0"));
  useEffect(() => {
    setSrc(pickArtSrc(pool, seed));
  }, [pool.join("|"), seed]);
  return src;
}

type ArtThumbProps = {
  src: string;
  alt?: string;
  className?: string;
  imgClassName?: string;
  /** Soft vignette + gold rim for medallion / chip use. */
  framed?: boolean;
};

/**
 * Artwork thumbnail (collection medallion / banner tile). Removes itself
 * on error so callers keep a stable fallback (icon/glyph) beside it.
 */
export function ArtThumb({
  src,
  alt = "",
  className = "",
  imgClassName = "",
  framed = false,
}: ArtThumbProps) {
  const [phase, setPhase] = useState<"loading" | "ready" | "error">("loading");
  const [activeSrc, setActiveSrc] = useState(src);

  useEffect(() => {
    setActiveSrc(src);
    setPhase("loading");
  }, [src]);

  if (phase === "error") return null;
  const imgStyle = { "--art-opacity": "1" } as CSSProperties;
  return (
    <span
      className={`relative block overflow-hidden ${framed ? "art-frame" : ""} ${className}`}
    >
      {phase === "loading" ? <span className="art-placeholder absolute inset-0" /> : null}
      <img
        src={activeSrc}
        alt={alt}
        loading="lazy"
        decoding="async"
        ref={(node) => {
          if (node?.complete && node.naturalWidth > 0) setPhase("ready");
        }}
        onLoad={() => setPhase("ready")}
        onError={() => {
          // Nature variant missing → fall back to primary thangka (`foo-n01` → `foo`).
          const fallback = activeSrc.replace(/-n\d{2}(?=\.jpg$)/, "");
          if (fallback !== activeSrc) {
            setActiveSrc(fallback);
            setPhase("loading");
            return;
          }
          setPhase("error");
        }}
        style={imgStyle}
        className={`art-reveal h-full w-full object-cover ${
          phase === "ready" ? "art-reveal--in" : ""
        } ${imgClassName}`}
      />
      {framed ? <span className="art-frame__rim" aria-hidden /> : null}
    </span>
  );
}

type ArtChipProps = {
  src: string;
  title: string;
  subtitle?: string;
  className?: string;
  children?: ReactNode;
};

/**
 * Compact passage / collection chip with a side strip of artwork —
 * for chat pinned-passage and similar study surfaces.
 */
export function ArtChip({ src, title, subtitle, className = "", children }: ArtChipProps) {
  const t = useT();
  return (
    // Overflow stays visible so FilterSelect menus aren't clipped; art is clipped on its own layer.
    <div className={`art-chip relative ${className}`}>
      <div className="pointer-events-none absolute inset-0 overflow-hidden rounded-[22px]">
        <ArtBackdrop src={src} variant="subtle" overlay="chip" position="center 20%" />
      </div>
      <div className="relative z-10 flex gap-3">
        <ArtThumb
          src={src}
          framed
          className="h-14 w-14 shrink-0 rounded-xl"
          imgClassName="[object-position:center_28%]"
        />
        <div className="min-w-0 flex-1">
          <p className="layer-heading">{t("chat.pinnedPassage")}</p>
          <h2 className="mt-1 text-xl leading-tight text-amber-100 sm:text-2xl">{title}</h2>
          {subtitle ? <p className="soft mt-1 font-sans text-sm">{subtitle}</p> : null}
          {children}
        </div>
      </div>
    </div>
  );
}
