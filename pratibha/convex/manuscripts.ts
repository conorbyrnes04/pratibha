import { getAuthUserId } from "@convex-dev/auth/server";
import { v } from "convex/values";
import { mutation, query } from "./_generated/server";
import { assertDisplayName, assertMargin, slugify } from "./textRules";

const MAX_ENTRIES = 40;

async function requireUser(ctx: Parameters<typeof getAuthUserId>[0]) {
  const userId = await getAuthUserId(ctx);
  if (!userId) throw new Error("Sign in to keep a manuscript.");
  return userId;
}

async function uniqueSlug(ctx: { db: any }, base: string): Promise<string> {
  const bytes = new Uint8Array(8);
  crypto.getRandomValues(bytes);
  const alphabet = "abcdefghijklmnopqrstuvwxyz0123456789";
  const suffix = Array.from(bytes, (b) => alphabet[b % alphabet.length]).join("");
  let slug = `${base}-${suffix}`;
  let n = 0;
  while (true) {
    const hit = await ctx.db
      .query("manuscripts")
      .withIndex("by_slug", (q: any) => q.eq("slug", slug))
      .unique();
    if (!hit) return slug;
    n += 1;
    slug = `${base}-${suffix}${n}`;
  }
}

async function getOrCreateManuscript(ctx: { db: any }, userId: string) {
  const existing = await ctx.db
    .query("manuscripts")
    .withIndex("by_user", (q: any) => q.eq("userId", userId))
    .unique();
  if (existing) return existing;
  const now = Date.now();
  const profile = await ctx.db
    .query("profiles")
    .withIndex("by_user", (q: any) => q.eq("userId", userId))
    .unique();
  const displayName = profile?.displayName || "Student";
  const slug = await uniqueSlug(ctx, slugify(displayName));
  const id = await ctx.db.insert("manuscripts", {
    userId,
    slug,
    title: `${displayName}'s manuscript`,
    displayName,
    visibility: "private",
    createdAt: now,
    updatedAt: now,
  });
  return await ctx.db.get(id);
}

function publicEntries(entries: Array<{
  verseId: string;
  verseTitle: string;
  note?: string;
  sortOrder: number;
}>) {
  return [...entries]
    .sort((a, b) => a.sortOrder - b.sortOrder)
    .map((e) => ({
      verseId: e.verseId,
      verseTitle: e.verseTitle,
      note: e.note || "",
      sortOrder: e.sortOrder,
    }));
}

export const getMine = query({
  args: {},
  handler: async (ctx) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) return null;
    const manuscript = await ctx.db
      .query("manuscripts")
      .withIndex("by_user", (q) => q.eq("userId", userId))
      .unique();
    if (!manuscript) return null;
    const entries = await ctx.db
      .query("manuscript_entries")
      .withIndex("by_manuscript", (q) => q.eq("manuscriptId", manuscript._id))
      .collect();
    return {
      ...manuscript,
      entries: publicEntries(entries),
    };
  },
});

export const hasVerse = query({
  args: { verseId: v.string() },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) return false;
    const manuscript = await ctx.db
      .query("manuscripts")
      .withIndex("by_user", (q) => q.eq("userId", userId))
      .unique();
    if (!manuscript) return false;
    const hit = await ctx.db
      .query("manuscript_entries")
      .withIndex("by_manuscript_verse", (q) =>
        q.eq("manuscriptId", manuscript._id).eq("verseId", args.verseId),
      )
      .unique();
    return Boolean(hit);
  },
});

export const getBySlug = query({
  args: { slug: v.string() },
  handler: async (ctx, args) => {
    const manuscript = await ctx.db
      .query("manuscripts")
      .withIndex("by_slug", (q) => q.eq("slug", args.slug.trim().toLowerCase()))
      .unique();
    if (!manuscript) return null;
    const userId = await getAuthUserId(ctx);
    if (manuscript.visibility !== "public" && manuscript.userId !== userId) {
      return null;
    }
    const entries = await ctx.db
      .query("manuscript_entries")
      .withIndex("by_manuscript", (q) => q.eq("manuscriptId", manuscript._id))
      .collect();
    return {
      slug: manuscript.slug,
      title: manuscript.title,
      displayName: manuscript.displayName,
      visibility: manuscript.visibility,
      updatedAt: manuscript.updatedAt,
      entries: publicEntries(entries),
    };
  },
});

export const addVerse = mutation({
  args: {
    verseId: v.string(),
    verseTitle: v.string(),
    note: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const userId = await requireUser(ctx);
    const manuscript = await getOrCreateManuscript(ctx, userId);
    const existing = await ctx.db
      .query("manuscript_entries")
      .withIndex("by_manuscript_verse", (q) =>
        q.eq("manuscriptId", manuscript._id).eq("verseId", args.verseId),
      )
      .unique();
    if (existing) return existing._id;
    const current = await ctx.db
      .query("manuscript_entries")
      .withIndex("by_manuscript", (q) => q.eq("manuscriptId", manuscript._id))
      .collect();
    if (current.length >= MAX_ENTRIES) {
      throw new Error("A manuscript holds at most 40 verses. Remove one to add another.");
    }
    const note = args.note?.trim() ? assertMargin(args.note) : undefined;
    const now = Date.now();
    const id = await ctx.db.insert("manuscript_entries", {
      manuscriptId: manuscript._id,
      userId,
      verseId: args.verseId,
      verseTitle: args.verseTitle.trim() || args.verseId,
      note,
      sortOrder: current.length,
      createdAt: now,
    });
    await ctx.db.patch(manuscript._id, { updatedAt: now });
    return id;
  },
});

export const removeVerse = mutation({
  args: { verseId: v.string() },
  handler: async (ctx, args) => {
    const userId = await requireUser(ctx);
    const manuscript = await ctx.db
      .query("manuscripts")
      .withIndex("by_user", (q) => q.eq("userId", userId))
      .unique();
    if (!manuscript) return;
    const entry = await ctx.db
      .query("manuscript_entries")
      .withIndex("by_manuscript_verse", (q) =>
        q.eq("manuscriptId", manuscript._id).eq("verseId", args.verseId),
      )
      .unique();
    if (!entry) return;
    await ctx.db.delete(entry._id);
    await ctx.db.patch(manuscript._id, { updatedAt: Date.now() });
  },
});

export const setEntryNote = mutation({
  args: { verseId: v.string(), note: v.string() },
  handler: async (ctx, args) => {
    const userId = await requireUser(ctx);
    const manuscript = await ctx.db
      .query("manuscripts")
      .withIndex("by_user", (q) => q.eq("userId", userId))
      .unique();
    if (!manuscript) throw new Error("No manuscript yet.");
    const entry = await ctx.db
      .query("manuscript_entries")
      .withIndex("by_manuscript_verse", (q) =>
        q.eq("manuscriptId", manuscript._id).eq("verseId", args.verseId),
      )
      .unique();
    if (!entry) throw new Error("That verse is not in your manuscript.");
    const note = args.note.trim() ? assertMargin(args.note) : undefined;
    await ctx.db.patch(entry._id, { note });
    await ctx.db.patch(manuscript._id, { updatedAt: Date.now() });
  },
});

export const moveVerse = mutation({
  args: { verseId: v.string(), direction: v.union(v.literal("up"), v.literal("down")) },
  handler: async (ctx, args) => {
    const userId = await requireUser(ctx);
    const manuscript = await ctx.db
      .query("manuscripts")
      .withIndex("by_user", (q) => q.eq("userId", userId))
      .unique();
    if (!manuscript) return;
    const entries = (
      await ctx.db
        .query("manuscript_entries")
        .withIndex("by_manuscript", (q) => q.eq("manuscriptId", manuscript._id))
        .collect()
    ).sort((a, b) => a.sortOrder - b.sortOrder);
    const index = entries.findIndex((e) => e.verseId === args.verseId);
    if (index < 0) return;
    const swapWith = args.direction === "up" ? index - 1 : index + 1;
    if (swapWith < 0 || swapWith >= entries.length) return;
    const a = entries[index];
    const b = entries[swapWith];
    await ctx.db.patch(a._id, { sortOrder: b.sortOrder });
    await ctx.db.patch(b._id, { sortOrder: a.sortOrder });
    await ctx.db.patch(manuscript._id, { updatedAt: Date.now() });
  },
});

export const updateSettings = mutation({
  args: {
    title: v.optional(v.string()),
    visibility: v.optional(v.union(v.literal("private"), v.literal("public"))),
    displayName: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const userId = await requireUser(ctx);
    const manuscript = await getOrCreateManuscript(ctx, userId);
    const patch: {
      title?: string;
      visibility?: "private" | "public";
      displayName?: string;
      slug?: string;
      updatedAt: number;
    } = { updatedAt: Date.now() };
    if (args.title !== undefined) {
      const title = args.title.trim();
      if (title.length < 2 || title.length > 80) {
        throw new Error("Give the manuscript a title between 2 and 80 characters.");
      }
      patch.title = title;
    }
    if (args.displayName !== undefined) {
      const displayName = assertDisplayName(args.displayName);
      patch.displayName = displayName;
      const profile = await ctx.db
        .query("profiles")
        .withIndex("by_user", (q) => q.eq("userId", userId))
        .unique();
      const now = Date.now();
      if (profile) await ctx.db.patch(profile._id, { displayName, updatedAt: now });
      else {
        await ctx.db.insert("profiles", {
          userId,
          displayName,
          createdAt: now,
          updatedAt: now,
        });
      }
    }
    if (args.visibility === "public") {
      const name = args.displayName
        ? assertDisplayName(args.displayName)
        : manuscript.displayName;
      if (!name || name === "Student") {
        throw new Error("Choose a name before making the manuscript public.");
      }
      patch.visibility = "public";
    } else if (args.visibility === "private") {
      patch.visibility = "private";
    }
    await ctx.db.patch(manuscript._id, patch);
    return manuscript.slug;
  },
});
