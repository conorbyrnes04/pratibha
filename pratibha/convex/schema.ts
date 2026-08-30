import { authTables } from "@convex-dev/auth/server";
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

const schema = defineSchema({
  ...authTables,

  journal_notes: defineTable({
    userId: v.string(),
    passageId: v.string(),
    passageTitle: v.string(),
    body: v.string(),
    tags: v.array(v.string()),
    prompt: v.optional(v.string()),
    kind: v.optional(v.string()),
    question: v.optional(v.string()),
    chatMode: v.optional(v.string()),
    verseId: v.optional(v.string()),
    createdAt: v.string(),
    updatedAt: v.string(),
  })
    .index("by_user", ["userId"])
    .index("by_user_updated", ["userId", "updatedAt"]),

  learn_progress: defineTable({
    userId: v.string(),
    progress: v.any(),
    completedAt: v.any(),
    updatedAt: v.string(),
  }).index("by_user", ["userId"]),

  profiles: defineTable({
    userId: v.string(),
    displayName: v.string(),
    createdAt: v.number(),
    updatedAt: v.number(),
  }).index("by_user", ["userId"]),

  student_commentaries: defineTable({
    userId: v.string(),
    displayName: v.string(),
    verseId: v.string(),
    verseTitle: v.string(),
    body: v.string(),
    status: v.union(v.literal("private"), v.literal("offered"), v.literal("hidden")),
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_user_verse", ["userId", "verseId"])
    .index("by_user_updated", ["userId", "updatedAt"])
    .index("by_verse_status", ["verseId", "status"]),

  manuscripts: defineTable({
    userId: v.string(),
    slug: v.string(),
    title: v.string(),
    displayName: v.string(),
    visibility: v.union(v.literal("private"), v.literal("public")),
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_user", ["userId"])
    .index("by_slug", ["slug"]),

  manuscript_entries: defineTable({
    manuscriptId: v.id("manuscripts"),
    userId: v.string(),
    verseId: v.string(),
    verseTitle: v.string(),
    note: v.optional(v.string()),
    sortOrder: v.number(),
    createdAt: v.number(),
  })
    .index("by_manuscript", ["manuscriptId"])
    .index("by_manuscript_verse", ["manuscriptId", "verseId"])
    .index("by_user", ["userId"]),

  circle_replies: defineTable({
    commentaryId: v.id("student_commentaries"),
    userId: v.string(),
    displayName: v.string(),
    verseId: v.string(),
    body: v.string(),
    status: v.union(v.literal("visible"), v.literal("hidden")),
    createdAt: v.number(),
  })
    .index("by_commentary", ["commentaryId"])
    .index("by_user_commentary", ["userId", "commentaryId"]),
});

export default schema;
