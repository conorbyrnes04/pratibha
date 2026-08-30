import { useState } from "@lynx-js/react";
import { getLayer, type Passage } from "../lib/corpus";
import {
  SHARE_FORCE_MARKS,
  SHARE_INKS,
  nextFolioLine,
  sharePageUrl,
  type ShareForceMark,
  type ShareInk,
  type ShareTextMode,
} from "../lib/shareCard";
import { C } from "../lib/theme";

export function ShareComposer({ passage }: { passage: Passage }) {
  const hasOriginal = Boolean(getLayer(passage, "original"));
  const [open, setOpen] = useState(false);
  const [mark, setMark] = useState<ShareForceMark>("lotus");
  const [ink, setInk] = useState<ShareInk>("gold");
  const [textMode, setTextMode] = useState<ShareTextMode>(hasOriginal ? "both" : "translation");
  const [line, setLine] = useState<number | undefined>(undefined);
  const [copied, setCopied] = useState(false);

  const pageUrl = sharePageUrl(passage._id, mark, ink, textMode, line);

  function copyLink() {
    "background only";
    setCopied(true);
  }

  if (!open) {
    return (
      <view
        bindtap={() => setOpen(true)}
        style={{
          paddingTop: 8,
          paddingBottom: 8,
          paddingLeft: 12,
          paddingRight: 12,
          backgroundColor: C.cardAlt,
          borderRadius: 6,
          alignSelf: "flex-start",
          marginBottom: 20,
        }}
      >
        <text style={{ color: C.gold, fontSize: 13 }}>Share this page</text>
      </view>
    );
  }

  return (
    <view style={{ marginBottom: 28 }}>
      <text style={{ color: C.goldMuted, fontSize: 11, letterSpacing: 1.5, textTransform: "uppercase", marginBottom: 10 }}>
        Share this page
      </text>
      <text style={{ color: C.muted, fontSize: 13, lineHeight: 1.5, marginBottom: 12 }}>
        Compose on the web to save the image. The link below opens the same folio.
      </text>
      <text style={{ color: C.faint, fontSize: 11, letterSpacing: 1, textTransform: "uppercase", marginBottom: 8 }}>
        Mark
      </text>
      <view style={{ flexDirection: "row", flexWrap: "wrap", gap: 8, marginBottom: 12 }}>
        {SHARE_FORCE_MARKS.map((slug) => (
          <Chip key={slug} label={slug} active={mark === slug} onTap={() => setMark(slug)} />
        ))}
      </view>
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
        {copied ? "Share this link from the web app:" : "Open this link to share the image:"}
      </text>
      <text style={{ color: C.gold, fontSize: 12, lineHeight: 1.45, marginBottom: 12 }}>{pageUrl}</text>
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
