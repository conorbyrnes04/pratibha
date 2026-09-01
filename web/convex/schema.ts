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
    mark: v.optional(v.string()),
    ink: v.optional(v.string()),
    locale: v.optional(v.string()),
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
    mark: v.optional(v.string()),
    ink: v.optional(v.string()),
    textMode: v.optional(v.string()),
    line: v.optional(v.number()),
    aspectRatio: v.optional(v.string()),
    holographic: v.optional(v.boolean()),
    reading: v.optional(v.string()),
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

  // A quiet "appreciation" a reader can leave on a verse (one per user/verse).
  // Kept in sync with pratibha/convex/schema.ts — both apps share one deployment.
  verse_likes: defineTable({
    userId: v.string(),
    verseId: v.string(),
    createdAt: v.number(),
  })
    .index("by_verse", ["verseId"])
    .index("by_user", ["userId"])
    .index("by_user_verse", ["userId", "verseId"]),

  // RAG corpus chunks with embeddings — the Convex-native replacement for the
  // Supabase pgvector `chunks` table. `embedding` is a 1536-dim vector
  // (text-embedding-3-small). `meta` mirrors the pgvector metadata dict so the
  // FastAPI retrieval path (_normalize_meta) is unchanged. Populated by
  // scripts/ingest_convex.py; queried by the `search` action below.
  rag_chunks: defineTable({
    body: v.string(),
    embedding: v.array(v.float64()),
    collection: v.string(),
    section: v.optional(v.string()),
    sourceFile: v.string(),
    // Corpus unit id (meta._id) as a top-level indexed column so the Related
    // panel can look up a unit's stored seed embedding without scanning `meta`.
    unitId: v.optional(v.string()),
    meta: v.any(),
  })
    .vectorIndex("by_embedding", {
      vectorField: "embedding",
      dimensions: 1536,
      filterFields: ["collection"],
    })
    .index("by_source", ["sourceFile"])
    .index("by_unit", ["unitId"]),
});

export default schema;
