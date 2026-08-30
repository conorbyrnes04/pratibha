import { getAuthUserId } from "@convex-dev/auth/server";
import { v } from "convex/values";
import { mutation, query } from "./_generated/server";

// A verse "appreciation" — one per user per verse, toggled on/off.
// Ported from the social-layer branch's verse likes, adapted to the Circles
// code style (getAuthUserId, numeric createdAt).

export const count = query({
  args: { verseId: v.string() },
  handler: async (ctx, args) => {
    const rows = await ctx.db
      .query("verse_likes")
      .withIndex("by_verse", (q) => q.eq("verseId", args.verseId))
      .collect();
    return rows.length;
  },
});

// Count plus whether the signed-in user has appreciated it — one round-trip
// for the button's full state.
export const meta = query({
  args: { verseId: v.string() },
  handler: async (ctx, args) => {
    const rows = await ctx.db
      .query("verse_likes")
      .withIndex("by_verse", (q) => q.eq("verseId", args.verseId))
      .collect();
    const userId = await getAuthUserId(ctx);
    return {
      count: rows.length,
      mine: userId ? rows.some((r) => r.userId === userId) : false,
      signedIn: Boolean(userId),
    };
  },
});

export const toggle = mutation({
  args: { verseId: v.string() },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) throw new Error("Sign in to appreciate a verse.");

    const existing = await ctx.db
      .query("verse_likes")
      .withIndex("by_user_verse", (q) => q.eq("userId", userId).eq("verseId", args.verseId))
      .unique();

    if (existing) {
      await ctx.db.delete(existing._id);
      return { liked: false };
    }
    await ctx.db.insert("verse_likes", {
      userId,
      verseId: args.verseId,
      createdAt: Date.now(),
    });
    return { liked: true };
  },
});

// Verse ids the signed-in user has appreciated, most recent first.
export const mine = query({
  args: {},
  handler: async (ctx) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) return [];
    const rows = await ctx.db
      .query("verse_likes")
      .withIndex("by_user", (q) => q.eq("userId", userId))
      .collect();
    return rows.sort((a, b) => b.createdAt - a.createdAt).map((r) => r.verseId);
  },
});
