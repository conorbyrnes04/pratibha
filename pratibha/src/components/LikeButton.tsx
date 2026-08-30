import React, { useState, useEffect } from "@lynx-js/react";
import { convexFetch } from "../convex/httpClient";
import { useAuth } from "../auth/AuthProvider";

interface LikeButtonProps {
  verseId: string;
}

export function LikeButton({ verseId }: LikeButtonProps) {
  const { user } = useAuth();
  const [likeCount, setLikeCount] = useState<number>(0);
  const [isLiked, setIsLiked] = useState<boolean>(false);
  const [loading, setLoading] = useState(false);
  const [dataLoaded, setDataLoaded] = useState(false);

  useEffect(() => {
    if (!dataLoaded) {
      loadLikeData();
    }
  }, [verseId, user, dataLoaded]);

  async function loadLikeData() {
    try {
      const count = await convexFetch("verseLikes:getLikeCount", { verseId }, "query");
      setLikeCount(count);

      if (user) {
        const liked = await convexFetch("verseLikes:hasUserLiked", { verseId }, "query");
        setIsLiked(liked);
      }
      setDataLoaded(true);
    } catch (error) {
      console.error("Failed to load like data:", error);
    }
  }

  async function handleLike() {
    if (!user) {
      console.log("Sign in required to like verses");
      return;
    }

    if (loading) return;

    setLoading(true);
    try {
      const result = await convexFetch("verseLikes:toggleLike", { verseId }, "mutation");
      setIsLiked(result.liked);
      setLikeCount((prev) => (result.liked ? prev + 1 : prev - 1));
    } catch (error: any) {
      console.error("Failed to toggle like:", error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <view
      bindtap={handleLike}
      style={{
        display: "linear",
        flexDirection: "row",
        alignItems: "center",
        opacity: loading ? 0.6 : 1,
        paddingTop: 8,
        paddingBottom: 8,
        paddingLeft: 12,
        paddingRight: 12,
        borderRadius: 4,
        backgroundColor: isLiked ? "rgba(201, 162, 39, 0.15)" : "transparent",
      }}
    >
      <text style={{ fontSize: 18, color: isLiked ? "#c9a227" : "#666", marginRight: 8 }}>
        {isLiked ? "♥" : "♡"}
      </text>
      <text style={{ color: "#999", fontSize: 14, fontWeight: "500" }}>
        {likeCount}
      </text>
    </view>
  );
}
