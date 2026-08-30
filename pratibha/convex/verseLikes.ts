import { v } from "convex/values";
import { mutation, query } from "./_generated/server";
import { getAuthUserId } from "@convex-dev/auth/server";

/**
 * Get like count for a verse
 */
export const getLikeCount = query({
  args: { verseId: v.string() },
  handler: async (ctx, args) => {
    const likes = await ctx.db
      .query("verse_likes")
      .withIndex("by_verse", (q) => q.eq("verseId", args.verseId))
      .collect();
    return likes.length;
  },
});

/**
 * Check if current user has liked a verse
 */
export const hasUserLiked = query({
  args: { verseId: v.string() },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) {
      return false;
    }

    const existing = await ctx.db
      .query("verse_likes")
      .withIndex("by_user_verse", (q) =>
        q.eq("userId", userId).eq("verseId", args.verseId)
      )
      .first();

    return !!existing;
  },
});

/**
 * Toggle like on a verse (like if not liked, unlike if already liked)
 */
export const toggleLike = mutation({
  args: { verseId: v.string() },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) {
      throw new Error("Must be logged in to like verses");
    }

    const existing = await ctx.db
      .query("verse_likes")
      .withIndex("by_user_verse", (q) =>
        q.eq("userId", userId).eq("verseId", args.verseId)
      )
      .first();

    if (existing) {
      // Unlike
      await ctx.db.delete(existing._id);
      return { liked: false };
    } else {
      // Like
      await ctx.db.insert("verse_likes", {
        userId,
        verseId: args.verseId,
        createdAt: Date.now(),
      });
      return { liked: true };
    }
  },
});

/**
 * Get all verses liked by a user
 */
export const getUserLikes = query({
  args: {},
  handler: async (ctx) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) {
      return [];
    }

    const likes = await ctx.db
      .query("verse_likes")
      .withIndex("by_user", (q) => q.eq("userId", userId))
      .order("desc")
      .collect();

    return likes.map((like) => like.verseId);
  },
});
