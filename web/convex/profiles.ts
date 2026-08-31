import { getAuthUserId } from "@convex-dev/auth/server";
import { v } from "convex/values";
import { mutation, query } from "./_generated/server";
import { assertDisplayName } from "./textRules";

export const getMine = query({
  args: {},
  handler: async (ctx) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) return null;
    return await ctx.db
      .query("profiles")
      .withIndex("by_user", (q) => q.eq("userId", userId))
      .unique();
  },
});

export const setDisplayName = mutation({
  args: { displayName: v.string() },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) throw new Error("Sign in to choose a name.");
    const displayName = assertDisplayName(args.displayName);
    const now = Date.now();
    const existing = await ctx.db
      .query("profiles")
      .withIndex("by_user", (q) => q.eq("userId", userId))
      .unique();
    if (existing) {
      await ctx.db.patch(existing._id, { displayName, updatedAt: now });
      return existing._id;
    }
    return await ctx.db.insert("profiles", {
      userId,
      displayName,
      createdAt: now,
      updatedAt: now,
    });
  },
});

export const setMark = mutation({
  args: { mark: v.optional(v.string()), ink: v.optional(v.string()) },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) throw new Error("Sign in to choose a mark.");
    const mark = args.mark?.trim() || undefined;
    const ink = args.ink?.trim() || undefined;
    if (mark && !/^[a-z0-9_]{2,32}$/.test(mark)) {
      throw new Error("Unknown mark.");
    }
    if (ink && !/^[a-z]{2,16}$/.test(ink)) {
      throw new Error("Unknown ink.");
    }
    const now = Date.now();
    const existing = await ctx.db
      .query("profiles")
      .withIndex("by_user", (q) => q.eq("userId", userId))
      .unique();
    if (existing) {
      await ctx.db.patch(existing._id, {
        mark: mark ?? "",
        ink: ink ?? existing.ink,
        updatedAt: now,
      });
      return existing._id;
    }
    return await ctx.db.insert("profiles", {
      userId,
      displayName: "Student",
      mark: mark ?? "",
      ink,
      createdAt: now,
      updatedAt: now,
    });
  },
});
