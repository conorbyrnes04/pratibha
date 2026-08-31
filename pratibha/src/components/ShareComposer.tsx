import { useState } from "@lynx-js/react";
import { getLayer, type Passage } from "../lib/corpus";
import { useAuth } from "../auth/AuthProvider";
import { useConvex } from "../convex/ConvexProvider";
import { isConvexConfigured } from "../convex/httpClient";
import {
  SHARE_MARK_GROUPS,
  SHARE_INKS,
  SHARE_SOCIAL,
  nextFolioLine,
  sharePageUrl,
  tweetIntentUrl,
  verseShareMark,
  whatsappIntentUrl,
  type ShareForceMark,
  type ShareInk,
  type ShareSocialId,
  type ShareTextMode,
} from "../lib/shareCard";
import { C } from "../lib/theme";

export function ShareComposer({
  passage,
  open,
  onOpenChange,
}: {
  passage: Passage;
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
}) {
  const hasOriginal = Boolean(getLayer(passage, "original"));
  const [internalOpen, setInternalOpen] = useState(false);
  const isOpen = open ?? internalOpen;
  function setOpen(next: boolean) {
    onOpenChange?.(next);
    if (open === undefined) setInternalOpen(next);
  }
  const [mark, setMark] = useState<ShareForceMark>(() => verseShareMark(passage));
  const [ink, setInk] = useState<ShareInk>("gold");
  const [textMode, setTextMode] = useState<ShareTextMode>(hasOriginal ? "both" : "translation");
  const [line, setLine] = useState<number | undefined>(undefined);
  const [copied, setCopied] = useState(false);
  const [destUrl, setDestUrl] = useState("");
  const [msBusy, setMsBusy] = useState(false);
  const { user } = useAuth();
  const { httpClient } = useConvex();

  const pageUrl = sharePageUrl(passage._id, mark, ink, textMode, line);

  function copyLink() {
    "background only";
    setCopied(true);
  }

  function addToManuscript() {
    "background only";
    if (!httpClient || !user || !isConvexConfigured()) {
      setDestUrl("Sign in to add this to your manuscript.");
      return;
    }
    setMsBusy(true);
    void httpClient
      .mutation("manuscripts:addVerse", { verseId: passage._id, verseTitle: passage.title || passage._id })
      .then(() => setDestUrl("Added to your manuscript."))
      .catch((err: { message?: string }) => setDestUrl(err?.message || "Could not add to your manuscript."))
      .finally(() => setMsBusy(false));
  }

  if (!isOpen) {
    return (
      <view
        bindtap={() => setOpen(true)}
        style={{
          paddingTop: 8,
          paddingBottom: 8,
          paddingLeft: 14,
          paddingRight: 14,
          backgroundColor: C.gold,
          borderRadius: 999,
          alignSelf: "flex-start",
          marginBottom: 20,
        }}
      >
        <text style={{ color: "#121018", fontSize: 13, fontWeight: "700" }}>Share</text>
      </view>
    );
  }

  return (
    <view style={{ marginBottom: 28 }}>
      <text style={{ color: C.goldMuted, fontSize: 11, letterSpacing: 1.5, textTransform: "uppercase", marginBottom: 10 }}>
        Share
      </text>
      <text style={{ color: C.muted, fontSize: 13, lineHeight: 1.5, marginBottom: 12 }}>
        Keep it in your manuscript, or open a destination. Compose the folio on the web for the image.
      </text>
      <text style={{ color: C.faint, fontSize: 11, letterSpacing: 1, textTransform: "uppercase", marginBottom: 8 }}>
        Send to
      </text>
      <view style={{ flexDirection: "row", flexWrap: "wrap", gap: 8, marginBottom: 12 }}>
        <Chip label={msBusy ? "…" : "Manuscript"} active={false} onTap={addToManuscript} />
        {SHARE_SOCIAL.map((dest) => (
          <Chip
            key={dest.id}
            label={dest.label}
            active={false}
            onTap={() => setDestUrl(lynxDestUrl(dest.id, pageUrl))}
          />
        ))}
      </view>
      {SHARE_MARK_GROUPS.map((group) => (
        <view key={group.id} style={{ marginBottom: 12 }}>
          <text style={{ color: C.faint, fontSize: 11, letterSpacing: 1, textTransform: "uppercase", marginBottom: 8 }}>
            {group.label}
          </text>
          <view style={{ flexDirection: "row", flexWrap: "wrap", gap: 8 }}>
            {group.marks.map((slug) => (
              <Chip key={slug} label={slug} active={mark === slug} onTap={() => setMark(slug)} />
            ))}
          </view>
        </view>
      ))}
      <text style={{ color: C.faint, fontSize: 11, letterSpacing: 1, textTransform: "uppercase", marginBottom: 8 }}>
        Ink
      </text>
      <view style={{ flexDirection: "row", flexWrap: "wrap", gap: 8, marginBottom: 12 }}>
        {(Object.keys(SHARE_INKS) as ShareInk[]).map((key) => (
          <Chip key={key} label={SHARE_INKS[key].label} active={ink === key} onTap={() => setInk(key)} />
        ))}
      </view>
      <text style={{ color: C.faint, fontSize: 11, letterSpacing: 1, textTransform: "uppercase", marginBottom: 8 }}>
        Text
      </text>
      <view style={{ flexDirection: "row", flexWrap: "wrap", gap: 8, marginBottom: 14 }}>
        <Chip
          label="Translation"
          active={textMode === "translation"}
          onTap={() => {
            setTextMode("translation");
            setLine(undefined);
          }}
        />
        {hasOriginal ? (
          <>
            <Chip
              label="Original"
              active={textMode === "original"}
              onTap={() => {
                setTextMode("original");
                setLine(undefined);
              }}
            />
            <Chip
              label="Both"
              active={textMode === "both"}
              onTap={() => {
                setTextMode("both");
                setLine(undefined);
              }}
            />
          </>
        ) : null}
        <Chip label="Shuffle line" active={Boolean(line)} onTap={() => setLine(nextFolioLine(8, line))} />
      </view>
      <text style={{ color: C.muted, fontSize: 13, lineHeight: 1.5, marginBottom: 10 }}>
        {copied ? "Share this link from the web app:" : destUrl || "Open this link to share the image:"}
      </text>
      <text style={{ color: C.gold, fontSize: 12, lineHeight: 1.45, marginBottom: 12 }}>{destUrl || pageUrl}</text>
      <view style={{ flexDirection: "row", gap: 8 }}>
        <view
          bindtap={copyLink}
          style={{ padding: 10, backgroundColor: C.gold, borderRadius: 6 }}
        >
          <text style={{ color: "#000", fontSize: 13, fontWeight: "600" }}>Show link</text>
        </view>
        <view bindtap={() => setOpen(false)} style={{ padding: 10 }}>
          <text style={{ color: C.muted, fontSize: 13 }}>Close</text>
        </view>
      </view>
    </view>
  );
}

function lynxDestUrl(id: ShareSocialId, folioUrl: string): string {
  if (id === "x") return tweetIntentUrl("A page from Pratibha", folioUrl);
  if (id === "whatsapp") return whatsappIntentUrl(folioUrl);
  if (id === "instagram") return "https://www.instagram.com/";
  if (id === "tiktok") return "https://www.tiktok.com/upload";
  return folioUrl;
}

function Chip({ label, active, onTap }: { label: string; active: boolean; onTap: () => void }) {
  return (
    <view
      bindtap={onTap}
      style={{
        paddingTop: 6,
        paddingBottom: 6,
        paddingLeft: 10,
        paddingRight: 10,
        backgroundColor: active ? C.gold : C.cardAlt,
        borderRadius: 14,
      }}
    >
      <text style={{ color: active ? "#000" : C.goldMuted, fontSize: 12 }}>{label}</text>
    </view>
  );
}
