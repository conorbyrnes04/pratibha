import React, { useState } from "@lynx-js/react";

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
  const [showMenu, setShowMenu] = useState(false);
  const [generating, setGenerating] = useState(false);

  const deepLink = `${window.location.origin}/read/${verseId}`;

  async function generateVerseCard(): Promise<Blob> {
    return new Promise((resolve, reject) => {
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");
      if (!ctx) {
        reject(new Error("Canvas not supported"));
        return;
      }

      // Set canvas size
      canvas.width = 1200;
      canvas.height = 1200;

      // Background
      ctx.fillStyle = "#0f0f1e";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Add border
      ctx.strokeStyle = "#f0c979";
      ctx.lineWidth = 8;
      ctx.strokeRect(40, 40, canvas.width - 80, canvas.height - 80);

      // Set up text
      ctx.textAlign = "center";
      ctx.fillStyle = "#ffffff";

      // Original text (if available)
      let yPosition = 200;
      if (verseOriginal) {
        ctx.font = "italic 32px serif";
        ctx.fillStyle = "#cccccc";
        const originalLines = wrapText(ctx, verseOriginal, canvas.width - 160);
        originalLines.forEach((line, i) => {
          ctx.fillText(line, canvas.width / 2, yPosition + i * 45);
        });
        yPosition += originalLines.length * 45 + 60;
      }

      // Translation
      ctx.font = "36px sans-serif";
      ctx.fillStyle = "#ffffff";
      const translationLines = wrapText(
        ctx,
        verseTranslation.slice(0, 300) + (verseTranslation.length > 300 ? "..." : ""),
        canvas.width - 160
      );
      translationLines.forEach((line, i) => {
        ctx.fillText(line, canvas.width / 2, yPosition + i * 50);
      });
      yPosition += translationLines.length * 50 + 80;

      // Pratibha branding
      ctx.font = "bold 48px sans-serif";
      ctx.fillStyle = "#f0c979";
      ctx.fillText("pratibha", canvas.width / 2, yPosition);
      yPosition += 60;

      // Deep link
      ctx.font = "28px monospace";
      ctx.fillStyle = "#999999";
      ctx.fillText(deepLink, canvas.width / 2, yPosition);

      // Convert to blob
      canvas.toBlob((blob) => {
        if (blob) {
          resolve(blob);
        } else {
          reject(new Error("Failed to generate image"));
        }
      }, "image/png");
    });
  }

  function wrapText(ctx: CanvasRenderingContext2D, text: string, maxWidth: number): string[] {
    const words = text.split(" ");
    const lines: string[] = [];
    let currentLine = "";

    words.forEach((word) => {
      const testLine = currentLine + (currentLine ? " " : "") + word;
      const metrics = ctx.measureText(testLine);

      if (metrics.width > maxWidth && currentLine) {
        lines.push(currentLine);
        currentLine = word;
      } else {
        currentLine = testLine;
      }
    });

    if (currentLine) {
      lines.push(currentLine);
    }

    return lines;
  }

  async function shareToX() {
    const tweetText = `${verseTitle}\n\n"${verseTranslation.slice(0, 200)}${
      verseTranslation.length > 200 ? "..." : ""
    }"\n\n${deepLink}`;

    const tweetUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(tweetText)}`;
    window.open(tweetUrl, "_blank");
    setShowMenu(false);
  }

  async function shareToInstagram() {
    setGenerating(true);
    try {
      const cardBlob = await generateVerseCard();
      const caption = `${verseTitle}\n\n"${verseTranslation.slice(0, 200)}${
        verseTranslation.length > 200 ? "..." : ""
      }"\n\nRead the full verse: ${deepLink}`;

      // Try Web Share API
      if (navigator.share && navigator.canShare && navigator.canShare({ files: [new File([cardBlob], "verse.png")] })) {
        await navigator.share({
          files: [new File([cardBlob], "verse.png", { type: "image/png" })],
          text: caption,
        });
      } else {
        // Fallback: download image + copy caption
        const url = URL.createObjectURL(cardBlob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `pratibha-${verseId}.png`;
        a.click();
        URL.revokeObjectURL(url);

        // Copy caption to clipboard
        await navigator.clipboard.writeText(caption);
        alert("Image downloaded! Caption copied to clipboard. Paste in Instagram.");
      }
    } catch (error) {
      console.error("Failed to share to Instagram:", error);
      alert("Failed to generate share card");
    } finally {
      setGenerating(false);
      setShowMenu(false);
    }
  }

  async function shareToTikTok() {
    setGenerating(true);
    try {
      const cardBlob = await generateVerseCard();
      const caption = `${verseTitle}\n\n"${verseTranslation.slice(0, 200)}${
        verseTranslation.length > 200 ? "..." : ""
      }"\n\nRead the full verse: ${deepLink}`;

      // Try Web Share API
      if (navigator.share && navigator.canShare && navigator.canShare({ files: [new File([cardBlob], "verse.png")] })) {
        await navigator.share({
          files: [new File([cardBlob], "verse.png", { type: "image/png" })],
          text: caption,
        });
      } else {
        // Fallback: download image + copy caption
        const url = URL.createObjectURL(cardBlob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `pratibha-${verseId}.png`;
        a.click();
        URL.revokeObjectURL(url);

        // Copy caption to clipboard
        await navigator.clipboard.writeText(caption);
        alert("Image downloaded! Caption copied to clipboard. Paste in TikTok.");
      }
    } catch (error) {
      console.error("Failed to share to TikTok:", error);
      alert("Failed to generate share card");
    } finally {
      setGenerating(false);
      setShowMenu(false);
    }
  }

  return (
    <view style={{ position: "relative" }}>
      <view
        bindtap={() => setShowMenu(!showMenu)}
        style={{
          paddingVertical: 8,
          paddingHorizontal: 12,
          backgroundColor: "#1a1a2e",
          borderRadius: 4,
          cursor: "pointer",
          border: "1px solid #333",
        }}
      >
        <text style={{ color: "#f0c979", fontSize: 14, fontWeight: "500" }}>
          Share ↗
        </text>
      </view>

      {showMenu && (
        <view
          style={{
            position: "absolute",
            top: "100%",
            left: 0,
            marginTop: 8,
            backgroundColor: "#252540",
            borderRadius: 8,
            border: "1px solid #333",
            padding: 8,
            gap: 4,
            minWidth: 200,
            zIndex: 10,
          }}
        >
          <view
            bindtap={shareToX}
            style={{
              padding: 12,
              cursor: "pointer",
              borderRadius: 4,
              backgroundColor: "transparent",
            }}
          >
            <text style={{ color: "#ddd", fontSize: 14 }}>Share to X</text>
          </view>

          <view
            bindtap={shareToInstagram}
            style={{
              padding: 12,
              cursor: generating ? "default" : "pointer",
              borderRadius: 4,
              backgroundColor: "transparent",
              opacity: generating ? 0.6 : 1,
            }}
          >
            <text style={{ color: "#ddd", fontSize: 14 }}>
              {generating ? "Generating..." : "Share to Instagram"}
            </text>
          </view>

          <view
            bindtap={shareToTikTok}
            style={{
              padding: 12,
              cursor: generating ? "default" : "pointer",
              borderRadius: 4,
              backgroundColor: "transparent",
              opacity: generating ? 0.6 : 1,
            }}
          >
            <text style={{ color: "#ddd", fontSize: 14 }}>
              {generating ? "Generating..." : "Share to TikTok"}
            </text>
          </view>

          <view
            bindtap={() => setShowMenu(false)}
            style={{
              padding: 12,
              cursor: "pointer",
              borderRadius: 4,
              backgroundColor: "transparent",
              marginTop: 4,
              borderTop: "1px solid #333",
            }}
          >
            <text style={{ color: "#999", fontSize: 13 }}>Cancel</text>
          </view>
        </view>
      )}
    </view>
  );
}
