import { v } from "convex/values";
import { mutation, query } from "./_generated/server";
import { getAuthUserId } from "@convex-dev/auth/server";

export const get = query({
  args: {},
  handler: async (ctx) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) {
      return null;
    }
    const progress = await ctx.db
      .query("learn_progress")
      .withIndex("by_user", (q) => q.eq("userId", userId))
      .first();
    return progress;
  },
});

export const upsert = mutation({
  args: {
    progress: v.any(),
    completedAt: v.any(),
  },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) {
      throw new Error("Not authenticated");
    }

    const existing = await ctx.db
      .query("learn_progress")
      .withIndex("by_user", (q) => q.eq("userId", userId))
      .first();

    const data = {
      userId,
      progress: args.progress,
      completedAt: args.completedAt,
      updatedAt: new Date().toISOString(),
    };

    if (existing) {
      await ctx.db.patch(existing._id, data);
      return existing._id;
    } else {
      return await ctx.db.insert("learn_progress", data);
    }
  },
});
