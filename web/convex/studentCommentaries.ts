import { getAuthUserId } from "@convex-dev/auth/server";
import { v } from "convex/values";
import { mutation, query } from "./_generated/server";
import { isCircleVerse } from "./circleVerses";
import { assertCommentary, assertDisplayName } from "./textRules";

const MAX_WRITES_PER_HOUR = 10;

async function requireUser(ctx: Parameters<typeof getAuthUserId>[0]) {
  const userId = await getAuthUserId(ctx);
  if (!userId) throw new Error("Sign in to write a reading.");
  return userId;
}

async function resolveDisplayName(
  ctx: { db: { query: (table: "profiles") => any } },
  userId: string,
  incoming?: string,
): Promise<string> {
  const profile = await ctx.db
    .query("profiles")
    .withIndex("by_user", (q: any) => q.eq("userId", userId))
    .unique();
  if (incoming?.trim()) {
    return assertDisplayName(incoming);
  }
  if (profile?.displayName) return profile.displayName;
  throw new Error("Choose a name before offering a reading.");
}

async function rateLimit(ctx: { db: any }, userId: string) {
  const since = Date.now() - 60 * 60 * 1000;
  const recent = await ctx.db
    .query("student_commentaries")
    .withIndex("by_user_updated", (q: any) => q.eq("userId", userId).gte("updatedAt", since))
    .collect();
  if (recent.length >= MAX_WRITES_PER_HOUR) {
    throw new Error("Please take time to reflect before writing again.");
  }
}

export const getMine = query({
  args: { verseId: v.string() },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) return null;
    return await ctx.db
      .query("student_commentaries")
      .withIndex("by_user_verse", (q) => q.eq("userId", userId).eq("verseId", args.verseId))
      .unique();
  },
});

export const listOffered = query({
  args: { verseId: v.string() },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) return [];
    const rows = await ctx.db
      .query("student_commentaries")
      .withIndex("by_verse_status", (q) => q.eq("verseId", args.verseId).eq("status", "offered"))
      .collect();
    return rows
      .filter((row) => row.userId !== userId)
      .sort((a, b) => a.createdAt - b.createdAt)
      .map((row) => ({
        _id: row._id,
        displayName: row.displayName,
        body: row.body,
        createdAt: row.createdAt,
        verseId: row.verseId,
      }));
  },
});

export const circleMeta = query({
  args: { verseId: v.string() },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    const offered = await ctx.db
      .query("student_commentaries")
      .withIndex("by_verse_status", (q) => q.eq("verseId", args.verseId).eq("status", "offered"))
      .collect();
    return {
      open: isCircleVerse(args.verseId),
      offeredCount: offered.length,
      signedIn: Boolean(userId),
    };
  },
});

export const upsert = mutation({
  args: {
    verseId: v.string(),
    verseTitle: v.string(),
    body: v.string(),
    status: v.union(v.literal("private"), v.literal("offered")),
    displayName: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const userId = await requireUser(ctx);
    const offered = args.status === "offered";
    const body = assertCommentary(args.body, offered);
    const now = Date.now();

    const existing = await ctx.db
      .query("student_commentaries")
      .withIndex("by_user_verse", (q) => q.eq("userId", userId).eq("verseId", args.verseId))
      .unique();

    if (!existing) await rateLimit(ctx, userId);

    let displayName = existing?.displayName || "";
    if (offered) {
      displayName = await resolveDisplayName(ctx, userId, args.displayName);
      const profile = await ctx.db
        .query("profiles")
        .withIndex("by_user", (q) => q.eq("userId", userId))
        .unique();
      if (!profile) {
        await ctx.db.insert("profiles", {
          userId,
          displayName,
          createdAt: now,
          updatedAt: now,
        });
      } else if (args.displayName?.trim()) {
        await ctx.db.patch(profile._id, { displayName, updatedAt: now });
      }
    }

    const verseTitle = args.verseTitle.trim() || args.verseId;
    if (existing) {
      await ctx.db.patch(existing._id, {
        body,
        status: args.status,
        verseTitle,
        displayName: displayName || existing.displayName,
        updatedAt: now,
      });
      return existing._id;
    }

    return await ctx.db.insert("student_commentaries", {
      userId,
      displayName: displayName || "Student",
      verseId: args.verseId,
      verseTitle,
      body,
      status: args.status,
      createdAt: now,
      updatedAt: now,
    });
  },
});

export const withdraw = mutation({
  args: { verseId: v.string() },
  handler: async (ctx, args) => {
    const userId = await requireUser(ctx);
    const existing = await ctx.db
      .query("student_commentaries")
      .withIndex("by_user_verse", (q) => q.eq("userId", userId).eq("verseId", args.verseId))
      .unique();
    if (!existing) throw new Error("No reading to withdraw.");
    await ctx.db.patch(existing._id, { status: "private", updatedAt: Date.now() });
  },
});
