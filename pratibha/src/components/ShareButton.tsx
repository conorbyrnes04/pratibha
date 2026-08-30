import React from "@lynx-js/react";

interface ShareButtonProps {
  verseId: string;
  verseTitle: string;
  verseTranslation: string;
  verseOriginal?: string;
}

export function ShareButton({
  verseId,
  verseTitle,
  verseTranslation,
  verseOriginal,
}: ShareButtonProps) {
  function handleShare() {
    // Native sharing would use platform-specific APIs
    // For now, just log
    console.log("Share verse:", verseId, verseTitle);
  }

  return (
    <view
      bindtap={handleShare}
      style={{
        paddingTop: 8,
        paddingBottom: 8,
        paddingLeft: 12,
        paddingRight: 12,
        backgroundColor: "transparent",
        borderRadius: 4,
        borderWidth: 1,
        borderColor: "#333",
      }}
    >
      <text style={{ color: "#c9a227", fontSize: 14, fontWeight: "500" }}>
        Share ↗
      </text>
    </view>
  );
}
