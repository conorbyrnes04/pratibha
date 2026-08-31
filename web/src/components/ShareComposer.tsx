"use client";

import { useEffect, useMemo, useRef, useState } from "react";
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
import { recordPractice, recordStudy, unlockedMarks, unlockProgress, UNLOCK_HINT } from "@/lib/glyphUnlock";
import { BookMarked, Shuffle } from "lucide-react";
import {
  SHARE_MARK_GROUPS,
  SHARE_INKS,
  SHARE_SOCIAL,
  SHARE_TEXT_MODES,
  folioCandidates,
  nextFolioLine,
  pickFolioLine,
  shareCaption,
  sharePagePath,
  tiktokUploadUrl,
  tweetIntentUrl,
  whatsappIntentUrl,
  verseShareMark,
  isShareForceMark,
  isShareInk,
  isShareTextMode,
  type ShareForceMark,
  type ShareInk,
  type ShareSocialId,
  type ShareTextMode,
  type ShareAspectRatio,
} from "@/lib/shareCard";
import { SHARE_DEST_ICONS } from "@/components/ShareDestIcons";
import { ShareCard } from "@/components/ShareCard";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { enableHoloMotion } from "@/lib/useHoloTilt";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { InkGlyph } from "@/components/InkGlyph";

function verseCopy(item: VerseItem) {
  return {
    title: displayPassageTitle(item),
    collection: displayCollectionName(item.collection) || item.collection,
    original: stripMarkdown(layerText(item, "original")),
    iast: stripMarkdown(layerText(item, "iast")),
    translation: stripMarkdown(layerText(item, "translation") || item.translation || ""),
  };
}

export function ShareComposer({
  item,
  designOpen,
  onDesignOpenChange,
}: {
  item: VerseItem;
  designOpen?: boolean;
  onDesignOpenChange?: (open: boolean) => void;
}) {
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
  const [holographic, setHolographic] = useState(false);
  const addVerse = useMutation(api.manuscripts.addVerse);
  const [busy, setBusy] = useState<string | null>(null);
  const [openMarks, setOpenMarks] = useState<Set<ShareForceMark>>(() => new Set([verseMark, "lotus", "circle", "moon", "fire", "tree", "heart", "water", "mountain"]));
  const cardRef = useRef<HTMLDivElement>(null);
  const { user } = useAuth();
  const manuscript = useQuery(api.manuscripts.getMine, CONVEX_ENABLED && user ? {} : "skip");
  const commentary = useQuery(
    api.studentCommentaries.getMine,
    CONVEX_ENABLED && user ? { verseId: item._id } : "skip",
  );
  const earnedHolo = Boolean(commentary?.body?.trim());
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
      }
    : copy;
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

  async function pngBlob(): Promise<Blob> {
    const wrap = cardRef.current;
    if (!wrap) throw new Error("Could not render the page.");
    const node = (wrap.querySelector(".share-card") as HTMLElement | null) || wrap;
    const width = Math.max(1, Math.round(node.offsetWidth));
    const height = Math.max(1, Math.round(node.offsetHeight));
    const blob = await toBlob(node, {
      pixelRatio: 3,
      cacheBust: true,
      backgroundColor: "#0a0a0f",
      width,
      height,
      style: {
        transform: "none",
        transformOrigin: "center top",
        width: `${width}px`,
        height: `${height}px`,
        margin: "0",
        left: "0",
        top: "0",
      },
      // html-to-image has no `onclone` hook (that is html2canvas); the holographic
      // transform is already flattened by the root `style: { transform: "none" }`
      // override above, so the captured card renders flat.
    });
    if (!blob) throw new Error("Could not render the page.");
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

  function canAttachImage(): boolean {
    if (!navigator.share || !navigator.canShare) return false;
    try {
      const probe = new File([new Uint8Array([0x89])], "pratibha.png", { type: "image/png" });
      return navigator.canShare({ files: [probe] });
    } catch {
      return false;
    }
  }

  async function nativeShare(file: File | null, caption: string): Promise<boolean> {
    if (!navigator.share) return false;
    if (file) {
      const fileOnly = { files: [file], title: copy.title };
      if (navigator.canShare?.(fileOnly)) {
        await navigator.share(fileOnly);
        return true;
      }
      const withCaption = { files: [file], text: caption, title: copy.title };
      if (navigator.canShare?.(withCaption)) {
        await navigator.share(withCaption);
        return true;
      }
      return false;
    }
    const textOnly = { text: caption, title: copy.title };
    if (navigator.canShare?.(textOnly)) {
      await navigator.share(textOnly);
      return true;
    }
    return false;
  }

  function openAppScheme(scheme: string, fallback?: string) {
    const a = document.createElement("a");
    a.href = scheme;
    a.rel = "noopener";
    a.style.display = "none";
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.setTimeout(() => {
      if (document.visibilityState === "visible" && fallback) window.location.href = fallback;
    }, 450);
  }

  function openInstagramApp(destination: "story" | "post") {
    const android = /Android/i.test(navigator.userAgent);
    const mobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
    const scheme = android
      ? "intent://instagram.com/#Intent;package=com.instagram.android;scheme=https;end"
      : destination === "story"
        ? "instagram://story-camera"
        : "instagram://app";
    const fallback = destination === "story" ? "instagram-stories://share" : "instagram://library";
    if (!mobile) {
      window.open("https://www.instagram.com/", "_blank", "noopener,noreferrer");
      return;
    }
    openAppScheme(scheme, fallback);
  }

  async function shareToWhatsApp() {
    setBusy("whatsapp");
    try {
      const blob = await pngBlob();
      const file = new File([blob], `pratibha-${item._id}.png`, { type: "image/png" });
      const { caption } = captionAndUrl();
      void navigator.clipboard.writeText(caption).catch(() => {});
      if (await nativeShare(file, caption)) return;
      downloadBlob(blob, file.name);
      toast.success("Card saved. Attach that image in WhatsApp.", { duration: 6000 });
    } catch (err) {
      if (err instanceof Error && err.name === "AbortError") return;
      toast.error(err instanceof Error ? err.message : "Could not share to WhatsApp.");
    } finally {
      setBusy(null);
    }
  }

  async function shareToInstagram(destination: "story" | "post") {
    const destId = destination === "story" ? "instagram_story" : "instagram_post";
    setBusy(destId);
    setAspectRatio(destination);
    const { caption } = captionAndUrl();
    void navigator.clipboard.writeText(caption).catch(() => {});
    openInstagramApp(destination);
    try {
      await new Promise((resolve) => window.setTimeout(resolve, 80));
      const blob = await pngBlob();
      downloadBlob(blob, `pratibha-${destination}-${item._id}.png`);
      toast.success(
        destination === "story"
          ? "Instagram opened. Story image saved — add it from Recents."
          : "Instagram opened. Post image saved — pick it from Recents.",
        { duration: 6000 },
      );
    } catch (err) {
      if (err instanceof Error && err.name === "AbortError") return;
      toast.error(err instanceof Error ? err.message : "Could not share to Instagram.");
    } finally {
      setBusy(null);
    }
  }

  async function shareTo(dest: ShareSocialId) {
    recordPractice(`share:${item._id}`);
    refreshUnlocks();
    if (dest === "instagram_story" || dest === "instagram_post") {
      await shareToInstagram(dest === "instagram_story" ? "story" : "post");
      return;
    }
    if (dest === "whatsapp") {
      await shareToWhatsApp();
      return;
    }
    setBusy(dest);
    try {
      const { caption, pageUrl } = captionAndUrl();
      if (dest === "x") {
        window.open(tweetIntentUrl(caption, pageUrl), "_blank", "noopener,noreferrer");
        return;
      }
      if (!canAttachImage()) {
        if (dest === "tiktok") window.open(tiktokUploadUrl(), "_blank", "noopener,noreferrer");
        void navigator.clipboard.writeText(caption).catch(() => {});
        toast.success(
          dest === "tiktok"
            ? "Caption copied — post it in TikTok."
            : "Caption copied — open Signal to send.",
        );
        return;
      }
      const blob = await pngBlob();
      const file = new File([blob], `pratibha-${item._id}.png`, { type: "image/png" });
      if (await nativeShare(file, caption)) return;
      downloadBlob(blob, file.name);
      await navigator.clipboard.writeText(caption);
      if (dest === "tiktok") {
        window.open(tiktokUploadUrl(), "_blank", "noopener,noreferrer");
        toast.success("Image saved. Caption copied — post it in TikTok.");
        return;
      }
      toast.success("Image saved. Caption copied — open Signal to send.");
    } catch (err) {
      if (err instanceof Error && err.name === "AbortError") return;
      toast.error(err instanceof Error ? err.message : "Could not share.");
    } finally {
      setBusy(null);
    }
  }

  async function shareMore() {
    setBusy("more");
    try {
      const blob = await pngBlob();
      const file = new File([blob], `pratibha-${item._id}.png`, { type: "image/png" });
      const { caption } = captionAndUrl();
      if (await nativeShare(file, caption)) return;
      downloadBlob(blob, file.name);
      await navigator.clipboard.writeText(caption);
      toast.success("Image saved. Caption copied.");
    } catch (err) {
      if (err instanceof Error && err.name === "AbortError") return;
      toast.error(err instanceof Error ? err.message : "Could not share.");
    } finally {
      setBusy(null);
    }
  }

  async function copyLink() {
    const path = sharePagePath(options);
    const url = `${window.location.origin}${path}`;
    await navigator.clipboard.writeText(url);
    toast.success("Link copied.");
  }

  async function keepCard() {
    if (!user) {
      window.location.href = `/login?next=/read/${encodeURIComponent(item._id)}`;
      return;
    }
    setBusy("keep");
    try {
      await addVerse({
        verseId: item._id,
        verseTitle: copy.title,
        note: folioNote || undefined,
        mark,
        ink,
        textMode,
        line,
        aspectRatio,
        holographic: holographic && earnedHolo,
      });
      recordPractice(`manuscript:${item._id}`);
      if (folioNote.trim()) recordPractice(`manuscript:note:${item._id}`);
      refreshUnlocks();
      toast.success("Card kept in your manuscript.");
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Could not add to your manuscript.");
    } finally {
      setBusy(null);
    }
  }

  const inManuscript = Boolean(manuscript?.entries.some((entry) => entry.verseId === item._id));

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
        Share
      </SheetTrigger>
      <SheetContent
        side="bottom"
        className="flex h-[92vh] max-h-[92vh] flex-col overflow-hidden border-t border-amber-200/15 bg-[#0b0b14] sm:max-w-none"
      >
        <SheetHeader className="shrink-0">
          <SheetTitle className="text-amber-100">Build this card</SheetTitle>
          <SheetDescription className="soft">
            The folio stays in view as you choose a mark, ink, and line.
            {progress.remaining > 0 ? " Marks open as you study the house." : " Every mark is open."}
          </SheetDescription>
          <div className="mt-3">
            <GlyphMala unlocked={openMarks} />
          </div>
        </SheetHeader>
        <div className="share-folio-studio">
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
              />
            </div>
          </div>
          <div className="share-folio-studio__controls space-y-6">
            <fieldset>
              <legend className="passage-layer__label mb-3">Send to</legend>
              <div className="flex flex-wrap gap-2">
                {CONVEX_ENABLED ? (
                  user ? (
                    <button
                      type="button"
                      className="share-dest share-dest--first"
                      disabled={busy !== null}
                      onClick={() => void keepCard()}
                    >
                      <BookMarked />
                      {busy === "keep" ? "…" : inManuscript ? "Update manuscript" : "Keep in manuscript"}
                    </button>
                  ) : (
                    <Link href={`/login?next=/read/${encodeURIComponent(item._id)}`} className="share-dest share-dest--first">
                      <BookMarked />
                      Manuscript
                    </Link>
                  )
                ) : (
                  <Link href={`/login?next=/read/${encodeURIComponent(item._id)}`} className="share-dest share-dest--first">
                    <BookMarked />
                    Manuscript
                  </Link>
                )}
                {SHARE_SOCIAL.map((dest) => {
                  const Icon = SHARE_DEST_ICONS[dest.id];
                  return (
                    <button
                      key={dest.id}
                      type="button"
                      className="share-dest"
                      disabled={busy !== null}
                      onClick={() => void shareTo(dest.id)}
                      aria-label={dest.label}
                    >
                      <Icon />
                      <span>{busy === dest.id ? "…" : dest.label}</span>
                    </button>
                  );
                })}
              </div>
            </fieldset>
            <fieldset id="share-keep">
              <legend className="passage-layer__label mb-3">This card</legend>
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
                  Holographic — from your reading
                </button>
              ) : (
                <p className="soft mb-3 text-sm leading-relaxed">
                  Write your own commentary on this verse to give the card a holographic shine.
                </p>
              )}
              <Textarea
                className="mt-3"
                value={folioNote}
                onChange={(e) => setFolioNote(e.target.value)}
                placeholder="A one-line margin — optional"
                rows={2}
              />
            </fieldset>
            {SHARE_MARK_GROUPS.map((group) => {
              const opened = group.marks.filter((slug) => openMarks.has(slug)).length;
              return (
                <fieldset key={group.id}>
                  <legend className="passage-layer__label mb-3">
                    {group.label}{" "}
                    <span className="share-unlock-count">
                      {opened} of {group.marks.length} open
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
                              toast.message("Keep studying.", {
                                description: UNLOCK_HINT,
                              });
                              return;
                            }
                            setMark(slug);
                          }}
                          aria-pressed={mark === slug}
                          aria-label={available ? slug : `${slug}, sealed`}
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
              <legend className="passage-layer__label mb-3">Ink</legend>
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
                    {SHARE_INKS[key].label}
                  </button>
                ))}
              </div>
            </fieldset>
            {availableModes.length > 1 ? (
              <fieldset>
                <legend className="passage-layer__label mb-3">Text</legend>
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
                      {mode.label}
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
                  Shuffle line
                </Button>
              ) : null}
              <Button
                type="button"
                size="sm"
                disabled={busy !== null}
                onClick={() => void shareMore()}
              >
                {busy === "more" ? "Making the page…" : "More"}
              </Button>
              <Button type="button" size="sm" variant="secondary" onClick={() => void copyLink()}>
                Copy link
              </Button>
            </div>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
}
