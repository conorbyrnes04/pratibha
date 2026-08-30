import { action } from "./_generated/server";
import { v } from "convex/values";

/**
 * Word-boundary filter for user-authored text (comments, manuscript notes).
 *
 * This corpus discusses embodiment, kāma, hell-realms, damnation, and
 * ordinary English "sex" / "hell" in translation. Substring checks and
 * anatomical/theological terms produce false positives on the texts
 * themselves. Only slurs and clear profanity belong here.
 */
const BLOCKED_WORDS = [
  "fuck",
  "shit",
  "bitch",
  "asshole",
  "cunt",
  "whore",
  "slut",
  "nigger",
  "faggot",
  "retard",
  "porn",
  "xxx",
] as const;

const SPAM_PATTERNS = [
  /(.)\1{10,}/,
  /\b(\w+)\s+\1\s+\1\b/i,
];

function escapeRegExp(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

const BLOCKED_WORD_RE = new RegExp(
  `\\b(?:${BLOCKED_WORDS.map(escapeRegExp).join("|")})\\b`,
  "i",
);

export function checkBlocklist(text: string): { passed: boolean; reason?: string } {
  if (BLOCKED_WORD_RE.test(text)) {
    return { passed: false, reason: "Contains inappropriate language" };
  }

  for (const pattern of SPAM_PATTERNS) {
    if (pattern.test(text)) {
      return { passed: false, reason: "Appears to be spam" };
    }
  }

  return { passed: true };
}

export const moderateWithOpenAI = action({
  args: { text: v.string() },
  handler: async (_ctx, args): Promise<{ passed: boolean; reason?: string }> => {
    const apiKey = process.env.OPENAI_API_KEY;
    if (!apiKey) {
      return { passed: true };
    }

    try {
      const response = await fetch("https://api.openai.com/v1/moderations", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${apiKey}`,
        },
        body: JSON.stringify({ input: args.text }),
      });

      if (!response.ok) {
        console.error("OpenAI moderation API error:", response.statusText);
        return { passed: true };
      }

      const data = await response.json();
      const result = data.results[0];
      const categories = result.categories ?? {};

      // Do not flag generic "sexual" — tantra, kāma, and embodiment talk
      // will trip it. Hate, harassment, and sexual content involving minors
      // are the only model categories we reject.
      if (
        categories.hate ||
        categories.harassment ||
        categories["sexual/minors"] ||
        categories["hate/threatening"] ||
        categories["harassment/threatening"]
      ) {
        return {
          passed: false,
          reason: "Content flagged by moderation system",
        };
      }

      return { passed: true };
    } catch (error) {
      console.error("OpenAI moderation error:", error);
      return { passed: true };
    }
  },
});
