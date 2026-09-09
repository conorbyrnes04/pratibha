import { makeFunctionReference } from "convex/server";

/** Same deployment as web — function names, not a second Convex folder. */
export const api = {
  auth: {
    currentUser: makeFunctionReference<"query">("auth:currentUser"),
  },
  account: {
    deleteAccount: makeFunctionReference<"mutation">("account:deleteAccount"),
  },
  journalNotes: {
    list: makeFunctionReference<"query">("journalNotes:list"),
    upsert: makeFunctionReference<"mutation">("journalNotes:upsert"),
    remove: makeFunctionReference<"mutation">("journalNotes:remove"),
  },
  learnProgress: {
    get: makeFunctionReference<"query">("learnProgress:get"),
    upsert: makeFunctionReference<"mutation">("learnProgress:upsert"),
  },
};
