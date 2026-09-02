import { getAuthUserId } from "@convex-dev/auth/server";
import { v } from "convex/values";
import { mutation, query } from "./_generated/server";
import { logQueryError, optionalUserId } from "./safeAuth";

export const meta = query({
  args: { verseId: v.string() },
  handler: async (ctx, args) => {
    try {
      const userId = await optionalUserId(ctx);
      if (!userId) return { watching: false, signedIn: false };
      const existing = await ctx.db
        .query("circle_watches")
        .withIndex("by_user_verse", (q) => q.eq("userId", userId).eq("verseId", args.verseId))
        .unique();
      return { watching: Boolean(existing), signedIn: true };
    } catch (error) {
      logQueryError("circleWatches.meta", error);
      return { watching: false, signedIn: false };
    }
  },
});

export const mine = query({
  args: {},
  handler: async (ctx) => {
    try {
      const userId = await optionalUserId(ctx);
      if (!userId) return [];
      const rows = await ctx.db
        .query("circle_watches")
        .withIndex("by_user", (q) => q.eq("userId", userId))
        .collect();
      return rows.sort((a, b) => b.createdAt - a.createdAt).map((row) => row.verseId);
    } catch (error) {
      logQueryError("circleWatches.mine", error);
      return [];
    }
  },
});

export const toggle = mutation({
  args: { verseId: v.string() },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) throw new Error("Sign in to watch a door.");
    const verseId = args.verseId.trim();
    if (!verseId) throw new Error("Missing verse.");
    const existing = await ctx.db
      .query("circle_watches")
      .withIndex("by_user_verse", (q) => q.eq("userId", userId).eq("verseId", verseId))
      .unique();
    if (existing) {
      await ctx.db.delete(existing._id);
      return { watching: false };
    }
    await ctx.db.insert("circle_watches", {
      userId,
      verseId,
      createdAt: Date.now(),
    });
    return { watching: true };
  },
});
