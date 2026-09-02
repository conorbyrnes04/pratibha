import { getAuthUserId } from "@convex-dev/auth/server";
import { v } from "convex/values";
import { mutation, query } from "./_generated/server";
import type { Doc } from "./_generated/dataModel";
import { assertCommentary, assertDisplayName } from "./textRules";

const MAX_WRITES_PER_HOUR = 10;
const FEED_LIMIT = 40;
const VERSE_LIMIT = 40;

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

function publicReading(row: Doc<"student_commentaries">, userId: string | null) {
  return {
    _id: row._id,
    displayName: row.displayName,
    body: row.body,
    verseId: row.verseId,
    verseTitle: row.verseTitle,
    createdAt: row.createdAt,
    updatedAt: row.updatedAt,
    lastActivityAt: row.lastActivityAt ?? row.updatedAt,
    replyCount: row.replyCount ?? 0,
    sitCount: row.sitCount ?? 0,
    mine: Boolean(userId && row.userId === userId),
  };
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

export const getOffered = query({
  args: { id: v.id("student_commentaries") },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    const row = await ctx.db.get(args.id);
    if (!row || row.status !== "offered") return null;
    return publicReading(row, userId);
  },
});

export const listOffered = query({
  args: { verseId: v.string() },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    const rows = await ctx.db
      .query("student_commentaries")
      .withIndex("by_verse_status", (q) => q.eq("verseId", args.verseId).eq("status", "offered"))
      .collect();
    return rows
      .sort((a, b) => a.createdAt - b.createdAt)
      .slice(0, VERSE_LIMIT)
      .map((row) => publicReading(row, userId));
  },
});

export const listRecent = query({
  args: { limit: v.optional(v.number()) },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    const limit = Math.min(Math.max(args.limit ?? FEED_LIMIT, 1), 60);
    const rows = await ctx.db
      .query("student_commentaries")
      .withIndex("by_status_created", (q) => q.eq("status", "offered"))
      .order("desc")
      .take(limit);
    return rows
      .sort((a, b) => (b.lastActivityAt ?? b.updatedAt) - (a.lastActivityAt ?? a.updatedAt))
      .map((row) => publicReading(row, userId));
  },
});

export const listMineOffered = query({
  args: {},
  handler: async (ctx) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) return [];
    const rows = await ctx.db
      .query("student_commentaries")
      .withIndex("by_user_updated", (q) => q.eq("userId", userId))
      .collect();
    return rows
      .filter((row) => row.status === "offered" && (row.replyCount ?? 0) > 0)
      .sort((a, b) => (b.lastActivityAt ?? b.updatedAt) - (a.lastActivityAt ?? a.updatedAt))
      .slice(0, 3)
      .map((row) => publicReading(row, userId));
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
      open: true,
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
        lastActivityAt: offered ? now : existing.lastActivityAt,
        replyCount: existing.replyCount ?? 0,
        sitCount: existing.sitCount ?? 0,
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
      replyCount: 0,
      sitCount: 0,
      lastActivityAt: now,
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
