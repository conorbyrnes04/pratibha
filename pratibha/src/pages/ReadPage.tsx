import React, { useEffect, useState } from "react";

interface Verse {
  _id: string;
  title?: string;
  collection?: string;
  pratibha_layers?: {
    translation?: string;
    original?: string;
    commentary?: string;
  };
}

export function ReadPage() {
  const [verses, setVerses] = useState<Verse[]>([]);
  const [selectedVerse, setSelectedVerse] = useState<Verse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadVerses() {
      try {
        const response = await fetch("http://localhost:8000/verses?limit=20");
        const data = await response.json();
        setVerses(data.verses || []);
      } catch (error) {
        console.error("Failed to load verses:", error);
      } finally {
        setLoading(false);
      }
    }
    loadVerses();
  }, []);

  if (loading) {
    return (
      <view style={{ padding: 20 }}>
        <text style={{ color: "#999" }}>Loading passages...</text>
      </view>
    );
  }

  if (selectedVerse) {
    return (
      <view style={{ padding: 20 }}>
        <view
          onClick={() => setSelectedVerse(null)}
          style={{
            marginBottom: 20,
            paddingVertical: 8,
            paddingHorizontal: 16,
            backgroundColor: "#1a1a2e",
            borderRadius: 4,
            alignSelf: "flex-start",
            cursor: "pointer",
          }}
        >
          <text style={{ color: "#f0c979", fontSize: 14 }}>← Back to list</text>
        </view>

        <text style={{ color: "#999", fontSize: 12, textTransform: "uppercase", marginBottom: 8 }}>
          {selectedVerse.collection || "Passage"}
        </text>
        <text style={{ color: "#f0c979", fontSize: 24, fontWeight: "bold", marginBottom: 24 }}>
          {selectedVerse.title || selectedVerse._id}
        </text>

        {selectedVerse.pratibha_layers?.translation && (
          <view style={{ marginBottom: 24 }}>
            <text style={{ color: "#999", fontSize: 12, marginBottom: 8, textTransform: "uppercase" }}>
              Translation
            </text>
            <text style={{ color: "#ddd", fontSize: 16, lineHeight: 1.6 }}>
              {selectedVerse.pratibha_layers.translation}
            </text>
          </view>
        )}

        {selectedVerse.pratibha_layers?.original && (
          <view style={{ marginBottom: 24 }}>
            <text style={{ color: "#999", fontSize: 12, marginBottom: 8, textTransform: "uppercase" }}>
              Original
            </text>
            <text style={{ color: "#ccc", fontSize: 14, lineHeight: 1.6, fontStyle: "italic" }}>
              {selectedVerse.pratibha_layers.original}
            </text>
          </view>
        )}

        {selectedVerse.pratibha_layers?.commentary && (
          <view style={{ marginBottom: 24 }}>
            <text style={{ color: "#999", fontSize: 12, marginBottom: 8, textTransform: "uppercase" }}>
              Commentary
            </text>
            <text style={{ color: "#ccc", fontSize: 14, lineHeight: 1.6 }}>
              {selectedVerse.pratibha_layers.commentary}
            </text>
          </view>
        )}
      </view>
    );
  }

  return (
    <view style={{ padding: 20 }}>
      <text style={{ color: "#f0c979", fontSize: 24, fontWeight: "bold", marginBottom: 8 }}>
        Library
      </text>
      <text style={{ color: "#999", fontSize: 14, marginBottom: 24 }}>
        Browse the canonical collection
      </text>

      <view style={{ gap: 12 }}>
        {verses.map((verse) => (
          <view
            key={verse._id}
            onClick={() => setSelectedVerse(verse)}
            style={{
              padding: 16,
              backgroundColor: "#1a1a2e",
              borderRadius: 8,
              cursor: "pointer",
              borderLeft: "4px solid #f0c979",
            }}
          >
            {verse.collection && (
              <text style={{ color: "#666", fontSize: 12, marginBottom: 4, textTransform: "uppercase" }}>
                {verse.collection}
              </text>
            )}
            <text style={{ color: "#f0c979", fontSize: 16, fontWeight: "600", marginBottom: 8 }}>
              {verse.title || verse._id}
            </text>
            {verse.pratibha_layers?.translation && (
              <text
                style={{
                  color: "#999",
                  fontSize: 14,
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                  display: "-webkit-box",
                  WebkitLineClamp: 2,
                  WebkitBoxOrient: "vertical",
                }}
              >
                {verse.pratibha_layers.translation}
              </text>
            )}
          </view>
        ))}
      </view>
    </view>
  );
}
