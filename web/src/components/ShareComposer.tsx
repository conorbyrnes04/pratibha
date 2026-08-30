"use client";

import { useMemo, useRef, useState } from "react";
import { toBlob } from "html-to-image";
import { toast } from "sonner";
import type { VerseItem } from "@/lib/types";
import { layerText } from "@/lib/verseLayers";
import { displayCollectionName } from "@/lib/collectionLabels";
import { displayPassageTitle } from "@/lib/passageTitles";
import { stripMarkdown } from "@/lib/textPreview";
import { Shuffle } from "lucide-react";
import {
  SHARE_CORE_MARKS,
  SHARE_DEITY_MARKS,
  SHARE_INKS,
  SHARE_TEXT_MODES,
  SHARE_ASPECT_RATIOS,
  defaultShareMark,
  folioCandidates,
  nextFolioLine,
  pickFolioLine,
  shareCaption,
  sharePagePath,
  type ShareForceMark,
  type ShareInk,
  type ShareTextMode,
  type ShareAspectRatio,
} from "@/lib/shareCard";
import { ShareCard } from "@/components/ShareCard";
import { Button } from "@/components/ui/button";
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

export function ShareComposer({ item }: { item: VerseItem }) {
  const copy = useMemo(() => verseCopy(item), [item]);
  const [mark, setMark] = useState<ShareForceMark>(() => defaultShareMark(item.collection));
  const [ink, setInk] = useState<ShareInk>("gold");
  const [textMode, setTextMode] = useState<ShareTextMode>(copy.original ? "both" : "translation");
  const [line, setLine] = useState<number | undefined>(undefined);
  const [aspectRatio, setAspectRatio] = useState<ShareAspectRatio>("post");
  const [busy, setBusy] = useState(false);
  const cardRef = useRef<HTMLDivElement>(null);

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

  async function pngBlob(): Promise<Blob> {
    const node = cardRef.current;
    if (!node) throw new Error("Could not render the page.");
    const blob = await toBlob(node, {
      pixelRatio: 4,
      cacheBust: true,
      backgroundColor: "#0a0a0f",
    });
    if (!blob) throw new Error("Could not render the page.");
    return blob;
  }

  async function share() {
    setBusy(true);
    try {
      const blob = await pngBlob();
      const file = new File([blob], `pratibha-${item._id}.png`, { type: "image/png" });
      const caption = shareCaption({
        title: copy.title,
        translation: picked?.text || displayCopy.translation || copy.translation,
        readUrl: `${window.location.origin}/read/${encodeURIComponent(item._id)}`,
      });
      if (navigator.share && navigator.canShare?.({ files: [file] })) {
        await navigator.share({ files: [file], text: caption });
        return;
      }
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = file.name;
      a.click();
      URL.revokeObjectURL(url);
      await navigator.clipboard.writeText(caption);
      toast.success("Image saved. Caption copied.");
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Could not share.");
    } finally {
      setBusy(false);
    }
  }

  async function shareToInstagram(destination: "story" | "post") {
    setBusy(true);
    try {
      const targetRatio: ShareAspectRatio = destination === "story" ? "story" : "post";
      const prevRatio = aspectRatio;
      
      if (targetRatio !== prevRatio) {
        setAspectRatio(targetRatio);
        await new Promise(resolve => setTimeout(resolve, 100));
      }

      const blob = await pngBlob();
      const fileName = `pratibha-${destination}-${item._id}.png`;
      const file = new File([blob], fileName, { type: "image/png" });
      const caption = shareCaption({
        title: copy.title,
        translation: picked?.text || displayCopy.translation || copy.translation,
        readUrl: `${window.location.origin}/read/${encodeURIComponent(item._id)}`,
      });

      const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

      if (navigator.share && navigator.canShare?.({ files: [file] })) {
        await navigator.share({ files: [file], text: caption });
        if (targetRatio !== prevRatio) setAspectRatio(prevRatio);
        return;
      }

      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = fileName;
      a.click();
      URL.revokeObjectURL(url);

      await navigator.clipboard.writeText(caption);

      let igWindow: Window | null = null;
      if (isMobile) {
        const scheme = destination === "story" ? "instagram-stories://share" : "instagram://library";
        igWindow = window.open(scheme, "_blank");
      } else {
        igWindow = window.open("instagram://", "_blank");
      }

      if (!igWindow || igWindow.closed) {
        toast.success(
          `Image saved for Instagram ${destination === "story" ? "Story" : "Post"}. Caption copied. Open Instagram and select the image.`,
          { duration: 6000 }
        );
      } else {
        toast.success(`Image saved. Caption copied. Opening Instagram...`);
      }

      if (targetRatio !== prevRatio) setAspectRatio(prevRatio);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Could not share to Instagram.");
    } finally {
      setBusy(false);
    }
  }

  async function copyLink() {
    const path = sharePagePath(options);
    const url = `${window.location.origin}${path}`;
    await navigator.clipboard.writeText(url);
    toast.success("Link copied.");
  }

  return (
    <Sheet>
      <SheetTrigger
        render={<Button type="button" variant="ghost" size="sm" className="border border-white/10" />}
      >
        Share this page
      </SheetTrigger>
      <SheetContent
        side="bottom"
        className="max-h-[92vh] border-t border-amber-200/15 bg-[#0b0b14] sm:max-w-none"
      >
        <SheetHeader>
          <SheetTitle className="text-amber-100">Share this page</SheetTitle>
          <SheetDescription className="soft">
            A folio of the verse — choose the mark, the ink, and the words.
          </SheetDescription>
        </SheetHeader>
        <div className="grid gap-8 overflow-y-auto px-4 pb-8 lg:grid-cols-[minmax(0,280px)_1fr] lg:items-start">
          <div ref={cardRef} className="share-card-preview mx-auto">
            <ShareCard
              mark={mark}
              ink={ink}
              textMode={displayMode}
              copy={displayCopy}
              fillWindow={Boolean(picked)}
              aspectRatio={aspectRatio}
            />
          </div>
          <div className="space-y-6">
            <fieldset>
              <legend className="passage-layer__label mb-3">Mark</legend>
              <div className="flex flex-wrap gap-2">
                {SHARE_CORE_MARKS.map((slug) => (
                  <button
                    key={slug}
                    type="button"
                    className={`share-chip ${mark === slug ? "share-chip--on" : ""}`}
                    onClick={() => setMark(slug)}
                    aria-pressed={mark === slug}
                    aria-label={slug}
                  >
                    <InkGlyph glyph={slug} ink={SHARE_INKS[ink].hex} className="share-chip__glyph" />
                    <span>{slug}</span>
                  </button>
                ))}
              </div>
            </fieldset>
            <fieldset>
              <legend className="passage-layer__label mb-3">Gods and goddesses</legend>
              <div className="flex flex-wrap gap-2">
                {SHARE_DEITY_MARKS.map((slug) => (
                  <button
                    key={slug}
                    type="button"
                    className={`share-chip ${mark === slug ? "share-chip--on" : ""}`}
                    onClick={() => setMark(slug)}
                    aria-pressed={mark === slug}
                    aria-label={slug}
                  >
                    <InkGlyph glyph={slug} ink={SHARE_INKS[ink].hex} className="share-chip__glyph" />
                    <span>{slug}</span>
                  </button>
                ))}
              </div>
            </fieldset>
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
                variant="secondary"
                disabled={busy}
                onClick={() => void shareToInstagram("story")}
              >
                {busy ? "Making Story…" : "Instagram Story"}
              </Button>
              <Button
                type="button"
                size="sm"
                variant="secondary"
                disabled={busy}
                onClick={() => void shareToInstagram("post")}
              >
                {busy ? "Making Post…" : "Instagram Post"}
              </Button>
              <Button type="button" size="sm" disabled={busy} onClick={() => void share()}>
                {busy ? "Making the page…" : "Share image"}
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
