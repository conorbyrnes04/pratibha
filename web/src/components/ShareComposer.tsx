"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { createPortal, flushSync } from "react-dom";
import Link from "next/link";
import { toBlob } from "html-to-image";
import { toast } from "sonner";
import { useMutation, useQuery } from "convex/react";
import { api } from "../../convex/_generated/api";
import { useAuth } from "@/components/AuthProvider";
import { CONVEX_ENABLED } from "@/lib/convexConfigured";
import type { VerseItem } from "@/lib/types";
import { layerText } from "@/lib/verseLayers";
import { displayCollectionName } from "@/lib/collectionLabels";
import { displayPassageTitle } from "@/lib/passageTitles";
import { stripMarkdown } from "@/lib/textPreview";
import { GlyphMala } from "@/components/GlyphMala";
import { recordPractice, recordStudy, unlockedMarks, unlockProgress } from "@/lib/glyphUnlock";
import { BookMarked, Copy, Download, Share2, Shuffle } from "lucide-react";
import {
  SHARE_MARK_GROUPS,
  SHARE_INKS,
  SHARE_TEXT_MODES,
  SHARE_ASPECT_RATIOS,
  SHARE_SOCIAL,
  folioCandidates,
  nextFolioLine,
  pickFolioLine,
  clipShareText,
  shareCaption,
  sharePagePath,
  tweetIntentUrl,
  whatsappIntentUrl,
  verseShareMark,
  isShareForceMark,
  isShareInk,
  isShareTextMode,
  type ShareForceMark,
  type ShareInk,
  type ShareTextMode,
  type ShareAspectRatio,
  type ShareSocialId,
} from "@/lib/shareCard";
import { SHARE_DEST_ICONS } from "@/components/ShareDestIcons";
import { ShareCard } from "@/components/ShareCard";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { enableHoloMotion } from "@/lib/useHoloTilt";
import { bakeHoloFoil, holoHueFromSeed } from "@/lib/bakeHoloFoil";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { InkGlyph } from "@/components/InkGlyph";
import { useT } from "@/components/LocaleProvider";
import { shareGroupKey, shareInkKey } from "@/i18n";

function verseCopy(item: VerseItem) {
  return {
    title: displayPassageTitle(item),
    collection: displayCollectionName(item.collection) || item.collection,
    original: stripMarkdown(layerText(item, "original")),
    iast: stripMarkdown(layerText(item, "iast")),
    translation: stripMarkdown(layerText(item, "translation") || item.translation || ""),
  };
}

type ShareComposerProps = {
  item: VerseItem;
  designOpen?: boolean;
  onDesignOpenChange?: (open: boolean) => void;
};

type ShareCloud = {
  addVerse: (args: {
    verseId: string;
    verseTitle: string;
    note?: string;
    mark: ShareForceMark;
    ink: ShareInk;
    textMode: ShareTextMode;
    line?: number;
    aspectRatio: ShareAspectRatio;
    holographic: boolean;
    reading?: string;
  }) => Promise<unknown>;
  upsertCommentary?: (args: {
    verseId: string;
    verseTitle: string;
    body: string;
    status: "private" | "offered";
  }) => Promise<unknown>;
  manuscript?: {
    entries: {
      verseId: string;
      mark?: string;
      ink?: string;
      textMode?: string;
      line?: number;
      aspectRatio?: string;
      note?: string;
      holographic?: boolean;
      reading?: string;
    }[];
  } | null;
  commentary?: { body?: string } | null;
};

export function ShareComposer(props: ShareComposerProps) {
  if (!CONVEX_ENABLED) return <ShareComposerInner {...props} />;
  return <ShareComposerCloud {...props} />;
}

function ShareComposerCloud(props: ShareComposerProps) {
  const addVerse = useMutation(api.manuscripts.addVerse);
  const upsertCommentary = useMutation(api.studentCommentaries.upsert);
  const { user } = useAuth();
  const manuscript = useQuery(api.manuscripts.getMine, user ? {} : "skip");
  const commentary = useQuery(
    api.studentCommentaries.getMine,
    user ? { verseId: props.item._id } : "skip",
  );
  return (
    <ShareComposerInner
      {...props}
      cloud={{ addVerse, upsertCommentary, manuscript, commentary }}
    />
  );
}

function ShareComposerInner({
  item,
  designOpen,
  onDesignOpenChange,
  cloud,
}: ShareComposerProps & { cloud?: ShareCloud }) {
  const t = useT();
  const copy = useMemo(() => verseCopy(item), [item]);
  const verseMark = useMemo(() => verseShareMark(item), [item]);
  const [mark, setMark] = useState<ShareForceMark>(verseMark);
  const [ink, setInk] = useState<ShareInk>("gold");
  const [textMode, setTextMode] = useState<ShareTextMode>(copy.original ? "both" : "translation");
  const [line, setLine] = useState<number | undefined>(undefined);
  const [aspectRatio, setAspectRatio] = useState<ShareAspectRatio>("post");
  const [internalOpen, setInternalOpen] = useState(false);
  const sheetOpen = designOpen ?? internalOpen;
  function setSheetOpen(open: boolean) {
    onDesignOpenChange?.(open);
    if (designOpen === undefined) setInternalOpen(open);
  }
  const [folioNote, setFolioNote] = useState("");
  const [readingDraft, setReadingDraft] = useState("");
  const [wroteReading, setWroteReading] = useState(false);
  const [printReading, setPrintReading] = useState(false);
  const [holographic, setHolographic] = useState(false);
  const [busy, setBusy] = useState<string | null>(null);
  const [openMarks, setOpenMarks] = useState<Set<ShareForceMark>>(() => new Set([verseMark, "lotus", "circle", "moon", "fire", "tree", "heart", "water", "mountain"]));
  const cardRef = useRef<HTMLDivElement>(null);
  const exportRef = useRef<HTMLDivElement>(null);
  const [canOsShare, setCanOsShare] = useState(false);
  const { user } = useAuth();
  const manuscript = cloud?.manuscript;
  const commentary = cloud?.commentary;
  const earnedHolo = wroteReading || Boolean(commentary?.body?.trim());
  const readingText = (readingDraft || commentary?.body || "").trim();
  const printedReading = printReading && readingText ? clipShareText(readingText, 220) : undefined;
  const extraVerseIds = manuscript?.entries.map((entry) => entry.verseId) ?? [];

  const candidates = useMemo(
    () =>
      folioCandidates({
        original: copy.original,
        iast: copy.iast,
        translation: copy.translation,
        mode: textMode,
      }),
    [copy, textMode],
  );
  const picked = pickFolioLine(candidates, line);
  const displayCopy = picked
    ? {
        title: copy.title,
        collection: copy.collection,
        original: picked.source === "translation" ? undefined : picked.text,
        translation: picked.source === "translation" ? picked.text : undefined,
        reading: printedReading,
      }
    : { ...copy, reading: printedReading };
  const displayMode = picked
    ? picked.source === "translation"
      ? "translation"
      : "original"
    : textMode;

  const options = { verseId: item._id, mark, ink, textMode, line };
  const availableModes = SHARE_TEXT_MODES.filter((mode) => {
    if (mode.id === "original" || mode.id === "both") return Boolean(copy.original);
    return Boolean(copy.translation);
  });
  const canShuffle = candidates.length > 0 && (candidates.length > 1 || Boolean(picked) || (copy.original || copy.translation || "").length > (candidates[0]?.text.length || 0) + 8);
  const progress = unlockProgress(openMarks);

  function refreshUnlocks() {
    setOpenMarks(unlockedMarks({ verseMark, extraVerseIds }));
  }

  function noteStudy() {
    recordStudy(item._id, verseMark);
    refreshUnlocks();
  }

  useEffect(() => {
    refreshUnlocks();
    const dwell = window.setTimeout(() => noteStudy(), 8000);
    return () => window.clearTimeout(dwell);
    // Current verse + manuscript entries are the only study inputs.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [item._id, verseMark, extraVerseIds.join("|")]);

  useEffect(() => {
    setWroteReading(false);
    setReadingDraft("");
    setPrintReading(false);
  }, [item._id]);

  useEffect(() => {
    if (commentary?.body) setReadingDraft(commentary.body);
  }, [commentary?.body]);

  useEffect(() => {
    if (!sheetOpen) return;
    const entry = manuscript?.entries.find((row) => row.verseId === item._id);
    if (entry?.mark && isShareForceMark(entry.mark)) setMark(entry.mark);
    if (entry?.ink && isShareInk(entry.ink)) setInk(entry.ink);
    if (entry?.textMode && isShareTextMode(entry.textMode)) setTextMode(entry.textMode);
    if (typeof entry?.line === "number") setLine(entry.line);
    if (entry?.aspectRatio === "story" || entry?.aspectRatio === "post") {
      setAspectRatio(entry.aspectRatio);
    }
    setFolioNote(entry?.note || "");
    setPrintReading(Boolean(entry?.reading?.trim()));
    const shine = Boolean(entry?.holographic) || earnedHolo;
    setHolographic(shine);
    if (shine) enableHoloMotion();
    // Hydrate once when the builder opens for this verse.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sheetOpen, item._id]);

  useEffect(() => {
    if (!earnedHolo) return;
    setHolographic(true);
    enableHoloMotion();
  }, [earnedHolo]);

  useEffect(() => {
    setCanOsShare(typeof navigator !== "undefined" && typeof navigator.share === "function");
  }, []);

  const holoHue = holoHueFromSeed(
    `${item._id}|${mark}|${ink}|${displayCopy.reading || ""}|${displayCopy.title || ""}`,
  );

  async function pngBlob(): Promise<Blob> {
    const wrap = exportRef.current || cardRef.current;
    if (!wrap) throw new Error(t("share.renderFailed"));
    await Promise.race([
      document.fonts.ready.then(() => undefined).catch(() => undefined),
      new Promise<void>((resolve) => window.setTimeout(resolve, 400)),
    ]);
    const readyUntil = Date.now() + 500;
    while (Date.now() < readyUntil) {
      const card = wrap.querySelector(".share-card") as HTMLElement | null;
      const markReady = Boolean(wrap.querySelector(".share-card__glyph svg"));
      if (card && card.offsetWidth > 8 && markReady) break;
      await new Promise((resolve) => window.setTimeout(resolve, 40));
    }
    await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
    const node = (wrap.querySelector(".share-card") as HTMLElement | null) || wrap;
    const width = Math.max(1, Math.round(node.offsetWidth));
    const height = Math.max(1, Math.round(node.offsetHeight));
    if (width < 8 || height < 8) throw new Error(t("share.renderFailed"));
    const blob = await Promise.race([
      toBlob(node, {
        pixelRatio: 2,
        cacheBust: false,
        skipFonts: true,
        backgroundColor: "#0a0a0f",
        width,
        height,
        filter: (el) => !(el instanceof Element && el.classList.contains("share-card__foil")),
        style: {
          transform: "none",
          transformOrigin: "center top",
          width: `${width}px`,
          height: `${height}px`,
          margin: "0",
          left: "0",
          top: "0",
          opacity: "1",
        },
      }),
      new Promise<null>((_, reject) => {
        window.setTimeout(() => reject(new Error(t("share.renderFailed"))), 8000);
      }),
    ]);
    if (!blob) throw new Error(t("share.renderFailed"));
    if (node.classList.contains("share-card--holo")) {
      return bakeHoloFoil(blob, holoHue);
    }
    return blob;
  }

  function captionAndUrl() {
    const pageUrl = `${window.location.origin}${sharePagePath(options)}`;
    const caption = shareCaption({
      title: copy.title,
      translation: picked?.text || displayCopy.translation || copy.translation,
      readUrl: pageUrl,
    });
    return { caption, pageUrl };
  }

  function downloadBlob(blob: Blob, name: string) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = name;
    a.click();
    URL.revokeObjectURL(url);
  }

  function friendlyShareError(err: unknown, fallback: string) {
    const msg = err instanceof Error ? err.message : fallback;
    if (/not authenticated|sign in|convex client|convex provider/i.test(msg)) return fallback;
    return msg;
  }

  async function saveImage() {
    setBusy("save");
    try {
      const blob = await pngBlob();
      downloadBlob(blob, `pratibha-${item._id}.png`);
      const { caption } = captionAndUrl();
      void navigator.clipboard.writeText(caption).catch(() => {});
      toast.success(t("share.savedCaption"));
    } catch (err) {
      toast.error(friendlyShareError(err, t("share.saveFailed")));
    } finally {
      setBusy(null);
    }
  }

  function destHint(dest?: ShareSocialId) {
    if (dest === "instagram_story") return t("share.destStory");
    if (dest === "instagram_post") return t("share.destPost");
    if (dest === "tiktok") return t("share.destTiktok");
    if (dest === "signal") return t("share.destSignal");
    return t("share.destAnywhere");
  }

  async function handOffFolio(dest?: ShareSocialId) {
    recordPractice(`share:${item._id}`);
    refreshUnlocks();
    setBusy(dest ?? "share");
    try {
      const blob = await pngBlob();
      const file = new File([blob], `pratibha-${item._id}.png`, { type: "image/png" });
      const { caption, pageUrl } = captionAndUrl();
      void navigator.clipboard.writeText(caption).catch(() => {});
      if (navigator.share) {
        try {
          const withFile = { files: [file], title: copy.title, text: caption };
          if (!navigator.canShare || navigator.canShare({ files: [file] })) {
            await navigator.share(withFile);
            return;
          }
          await navigator.share({ title: copy.title, text: caption });
          downloadBlob(blob, file.name);
          toast.success(t("share.captionHandoff"));
          return;
        } catch (err) {
          if (err instanceof Error && err.name === "AbortError") return;
        }
      }
      downloadBlob(blob, file.name);
      if (dest === "x") {
        window.open(tweetIntentUrl(caption, pageUrl), "_blank", "noopener,noreferrer");
        toast.success(t("share.savedX"));
        return;
      }
      if (dest === "whatsapp") {
        window.open(whatsappIntentUrl(caption), "_blank", "noopener,noreferrer");
        toast.success(t("share.savedWhatsapp"));
        return;
      }
      toast.success(t("share.savedDest", { hint: destHint(dest) }));
    } catch (err) {
      if (err instanceof Error && err.name === "AbortError") return;
      toast.error(friendlyShareError(err, t("share.shareFailed")));
    } finally {
      setBusy(null);
    }
  }

  async function shareFolio() {
    await handOffFolio();
  }

  async function shareTo(dest: ShareSocialId) {
    const next: ShareAspectRatio | undefined =
      dest === "instagram_story" || dest === "tiktok"
        ? "story"
        : dest === "instagram_post"
          ? "post"
          : undefined;
    if (next && next !== aspectRatio) {
      flushSync(() => setAspectRatio(next));
    }
    await handOffFolio(dest);
  }

  async function copyLink() {
    const path = sharePagePath(options);
    const url = `${window.location.origin}${path}`;
    await navigator.clipboard.writeText(url);
    toast.success(t("share.linkCopied"));
  }

  async function keepCard() {
    if (!user) {
      window.location.href = `/login?next=/read/${encodeURIComponent(item._id)}`;
      return;
    }
    setBusy("keep");
    try {
      if (!cloud?.addVerse) {
        toast.error(t("share.signInKeep"));
        return;
      }
      const payload = {
        verseId: item._id,
        verseTitle: copy.title,
        note: folioNote || undefined,
        mark,
        ink,
        textMode,
        line,
        aspectRatio,
        holographic: holographic && earnedHolo,
        reading: printedReading || "",
      };
      try {
        await cloud.addVerse(payload);
      } catch (err) {
        const { reading: _reading, ...rest } = payload;
        await cloud.addVerse(rest);
      }
      recordPractice(`manuscript:${item._id}`);
      if (folioNote.trim()) recordPractice(`manuscript:note:${item._id}`);
      refreshUnlocks();
      toast.success(t("share.kept"));
    } catch (err) {
      toast.error(friendlyShareError(err, t("share.keepFailed")));
    } finally {
      setBusy(null);
    }
  }

  const inManuscript = Boolean(manuscript?.entries.some((entry) => entry.verseId === item._id));

  async function saveReading() {
    if (!user) {
      window.location.href = `/login?next=/read/${encodeURIComponent(item._id)}`;
      return;
    }
    if (!cloud?.upsertCommentary) {
      toast.error(t("share.signInReading"));
      return;
    }
    setBusy("reading");
    try {
      await cloud.upsertCommentary({
        verseId: item._id,
        verseTitle: copy.title,
        body: readingDraft,
        status: "private",
      });
      recordPractice(`commentary:${item._id}`);
      setWroteReading(true);
      setHolographic(true);
      enableHoloMotion();
      if (inManuscript) {
        await cloud.addVerse({
          verseId: item._id,
          verseTitle: copy.title,
          note: folioNote || undefined,
          mark,
          ink,
          textMode,
          line,
          aspectRatio,
          holographic: true,
          reading: printedReading || "",
        }).catch(() => undefined);
      }
      toast.success(t("share.readingSaved"));
    } catch (err) {
      toast.error(friendlyShareError(err, t("share.readingFailed")));
    } finally {
      setBusy(null);
    }
  }

  return (
    <Sheet
      open={sheetOpen}
      onOpenChange={(open) => {
        setSheetOpen(open);
        if (open) noteStudy();
      }}
    >
      <SheetTrigger render={<Button type="button" size="sm" className="share-trigger" />}>
        <InkGlyph glyph={verseMark} ink="#121018" className="share-trigger__glyph" />
        {t("share.trigger")}
      </SheetTrigger>
      <SheetContent
        side="bottom"
        className="flex h-[92vh] max-h-[92vh] flex-col overflow-hidden border-t border-amber-200/15 bg-[#0b0b14] sm:max-w-none"
      >
        <SheetHeader className="shrink-0">
          <SheetTitle className="text-amber-100">{t("share.build")}</SheetTitle>
          <SheetDescription className="soft">
            {t("share.buildLede")}
            {progress.remaining > 0 ? ` ${t("share.marksRemain")}` : ` ${t("share.marksAllOpen")}`}
          </SheetDescription>
          <div className="mt-3">
            <GlyphMala unlocked={openMarks} />
          </div>
        </SheetHeader>
        <div className="share-folio-studio min-h-0 flex-1">
          <div ref={cardRef} className="share-folio-studio__preview">
            <div className="share-card-preview">
              <ShareCard
                mark={mark}
                ink={ink}
                textMode={displayMode}
                copy={displayCopy}
                fillWindow={Boolean(picked)}
                aspectRatio={aspectRatio}
                holographic={holographic && earnedHolo}
                holoHue={holoHue}
              />
            </div>
          </div>
          <div className="share-folio-send">
            <fieldset>
              <legend className="passage-layer__label">{t("share.send")}</legend>
              <p className="soft mb-3 text-sm leading-relaxed">
                {canOsShare ? t("share.sendOs") : t("share.sendSave")}
              </p>
              <div className="flex flex-nowrap gap-1.5 overflow-x-auto">
                {CONVEX_ENABLED ? (
                  user ? (
                    <button
                      type="button"
                      className="share-dest share-dest--first"
                      disabled={busy !== null}
                      onClick={() => void keepCard()}
                    >
                      <BookMarked />
                      {busy === "keep" ? "…" : inManuscript ? t("common.update") : t("common.keep")}
                    </button>
                  ) : (
                    <Link href={`/login?next=/read/${encodeURIComponent(item._id)}`} className="share-dest share-dest--first">
                      <BookMarked />
                      {t("share.manuscript")}
                    </Link>
                  )
                ) : (
                  <Link href={`/login?next=/read/${encodeURIComponent(item._id)}`} className="share-dest share-dest--first">
                    <BookMarked />
                    {t("share.manuscript")}
                  </Link>
                )}
                <button
                  type="button"
                  className="share-dest"
                  disabled={busy !== null}
                  onClick={() => void shareFolio()}
                >
                  <Share2 />
                  {busy === "share" ? "…" : t("share.trigger")}
                </button>
                <button
                  type="button"
                  className="share-dest"
                  disabled={busy !== null}
                  onClick={() => void saveImage()}
                >
                  <Download />
                  {busy === "save" ? "…" : t("common.save")}
                </button>
                <button type="button" className="share-dest" onClick={() => void copyLink()}>
                  <Copy />
                  {t("common.copy")}
                </button>
              </div>
              <div className="mt-2 flex flex-nowrap gap-1.5 overflow-x-auto">
                {SHARE_SOCIAL.map((dest) => {
                  const Icon = SHARE_DEST_ICONS[dest.id];
                  return (
                    <button
                      key={dest.id}
                      type="button"
                      className="share-dest share-dest--brand"
                      disabled={busy !== null}
                      onClick={() => void shareTo(dest.id)}
                      aria-label={dest.label}
                      title={dest.label}
                    >
                      <Icon />
                      <span>{busy === dest.id ? "…" : dest.label}</span>
                    </button>
                  );
                })}
              </div>
            </fieldset>
          </div>
          <div className="share-folio-studio__controls space-y-6">
            {SHARE_MARK_GROUPS.map((group) => {
              const opened = group.marks.filter((slug) => openMarks.has(slug)).length;
              return (
                <fieldset key={group.id}>
                  <legend className="passage-layer__label mb-3">
                    {t(shareGroupKey(group.id))}{" "}
                    <span className="share-unlock-count">
                      {t("share.ofOpen", { opened, total: group.marks.length })}
                    </span>
                  </legend>
                  <div className="flex flex-wrap gap-2">
                    {group.marks.map((slug, markIndex) => {
                      const available = openMarks.has(slug);
                      // Available marks draw their ink stroke in, staggered by position.
                      const unlockIndex = available ? markIndex : -1;
                      return (
                        <button
                          key={slug}
                          type="button"
                          className={`share-chip ${mark === slug ? "share-chip--on" : ""} ${available ? "" : "share-chip--locked"}`}
                          onClick={() => {
                            if (!available) {
                              toast.message(t("share.keepStudying"), {
                                description: t("glyph.unlockHint"),
                              });
                              return;
                            }
                            setMark(slug);
                          }}
                          aria-pressed={mark === slug}
                          aria-label={available ? slug : t("share.sealed", { slug })}
                        >
                          <InkGlyph
                            glyph={slug}
                            ink={SHARE_INKS[ink].hex}
                            className="share-chip__glyph"
                            stroke={unlockIndex >= 0}
                            strokeKey={unlockIndex >= 0 ? `open-${slug}` : undefined}
                            strokeDelay={unlockIndex >= 0 ? unlockIndex * 90 : 0}
                          />
                          <span>{slug}</span>
                        </button>
                      );
                    })}
                  </div>
                </fieldset>
              );
            })}
            <fieldset>
              <legend className="passage-layer__label mb-3">{t("share.ink")}</legend>
              <div className="flex flex-wrap gap-2">
                {(Object.keys(SHARE_INKS) as ShareInk[]).map((key) => (
                  <button
                    key={key}
                    type="button"
                    className={`share-chip ${ink === key ? "share-chip--on" : ""}`}
                    onClick={() => setInk(key)}
                    aria-pressed={ink === key}
                  >
                    <span className="share-chip__swatch" style={{ background: SHARE_INKS[key].hex }} />
                    {t(shareInkKey(key))}
                  </button>
                ))}
              </div>
            </fieldset>
            <fieldset>
              <legend className="passage-layer__label mb-3">{t("share.format")}</legend>
              <p className="soft mb-3 text-sm leading-relaxed">
                {t("share.formatLede")}
              </p>
              <div className="flex flex-wrap gap-2">
                {(Object.keys(SHARE_ASPECT_RATIOS) as ShareAspectRatio[]).map((key) => (
                  <button
                    key={key}
                    type="button"
                    className={`share-chip ${aspectRatio === key ? "share-chip--on" : ""}`}
                    onClick={() => setAspectRatio(key)}
                    aria-pressed={aspectRatio === key}
                  >
                    {t(`share.${key}`)}
                  </button>
                ))}
              </div>
            </fieldset>
            <fieldset id="share-keep">
              <legend className="passage-layer__label mb-3">{t("share.thisCard")}</legend>
              {earnedHolo || readingText ? (
                <div className="mb-3 flex flex-wrap gap-2">
                  {earnedHolo ? (
                    <button
                      type="button"
                      className={`share-chip ${holographic ? "share-chip--on" : ""}`}
                      onClick={() => {
                        const next = !holographic;
                        setHolographic(next);
                        if (next) enableHoloMotion();
                      }}
                      aria-pressed={holographic}
                    >
                      {t("share.holo")}
                    </button>
                  ) : null}
                  {readingText ? (
                    <button
                      type="button"
                      className={`share-chip ${printReading ? "share-chip--on" : ""}`}
                      onClick={() => setPrintReading((on) => !on)}
                      aria-pressed={printReading}
                    >
                      {t("share.printReading")}
                    </button>
                  ) : null}
                </div>
              ) : (
                <p className="soft mb-3 text-sm leading-relaxed">
                  {t("share.writeReading")}
                </p>
              )}
              {user && cloud?.upsertCommentary ? (
                <div className="space-y-3">
                  <Textarea
                    value={readingDraft}
                    onChange={(e) => setReadingDraft(e.target.value)}
                    placeholder={t("commentary.placeholder")}
                    rows={4}
                  />
                  {!earnedHolo ? (
                    <Button
                      type="button"
                      size="sm"
                      disabled={!readingDraft.trim() || busy !== null}
                      onClick={() => void saveReading()}
                    >
                      {busy === "reading" ? t("common.saving") : t("share.saveReading")}
                    </Button>
                  ) : null}
                </div>
              ) : !earnedHolo ? (
                <Link href={`/login?next=/read/${encodeURIComponent(item._id)}`} className="share-dest share-dest--first">
                  {t("share.signInReading")}
                </Link>
              ) : null}
              <Textarea
                className="mt-3"
                value={folioNote}
                onChange={(e) => setFolioNote(e.target.value)}
                placeholder={t("manuscript.notePlaceholder")}
                rows={2}
              />
            </fieldset>
            {availableModes.length > 1 ? (
              <fieldset>
                <legend className="passage-layer__label mb-3">{t("share.text")}</legend>
                <div className="flex flex-wrap gap-2">
                  {availableModes.map((mode) => (
                    <button
                      key={mode.id}
                      type="button"
                      className={`share-chip ${textMode === mode.id ? "share-chip--on" : ""}`}
                      onClick={() => {
                        setTextMode(mode.id);
                        setLine(undefined);
                      }}
                      aria-pressed={textMode === mode.id}
                    >
                      {t(`share.${mode.id}`)}
                    </button>
                  ))}
                </div>
              </fieldset>
            ) : null}
            <div className="passage-endmatter__actions">
              {canShuffle ? (
                <Button
                  type="button"
                  size="sm"
                  variant="secondary"
                  onClick={() => setLine(nextFolioLine(candidates.length, line))}
                >
                  <Shuffle />
                  {t("share.shuffle")}
                </Button>
              ) : null}
            </div>
          </div>
        </div>
        {sheetOpen
          ? createPortal(
              <div ref={exportRef} className="share-card-export" aria-hidden>
                <ShareCard
                  mark={mark}
                  ink={ink}
                  textMode={displayMode}
                  copy={displayCopy}
                  fillWindow={Boolean(picked)}
                  aspectRatio={aspectRatio}
                  holographic={holographic && earnedHolo}
                  holoHue={holoHue}
                  flat
                />
              </div>,
              document.body,
            )
          : null}
      </SheetContent>
    </Sheet>
  );
}
