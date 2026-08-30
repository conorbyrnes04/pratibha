import { action } from "./_generated/server";
import { v } from "convex/values";

// Blocklist of inappropriate terms (case-insensitive)
const BLOCKLIST = [
  // Common profanity
  "fuck", "shit", "bitch", "asshole", "damn", "hell",
  // Slurs and hate speech
  "nigger", "faggot", "retard", "cunt", "whore", "slut",
  // Sexual vulgarity
  "porn", "xxx", "sex", "dick", "pussy", "cock", "penis", "vagina",
];

// Spam patterns
const SPAM_PATTERNS = [
  /(.)\1{10,}/, // Repeated characters (10+ times)
  /\b(\w+)\s+\1\s+\1\b/i, // Same word repeated 3+ times
];

/**
 * Check comment content against blocklist and spam patterns
 */
export function checkBlocklist(text: string): { passed: boolean; reason?: string } {
  const lowerText = text.toLowerCase();

  // Check blocklist
  for (const term of BLOCKLIST) {
    if (lowerText.includes(term)) {
      return { passed: false, reason: "Contains inappropriate language" };
    }
  }

  // Check spam patterns
  for (const pattern of SPAM_PATTERNS) {
    if (pattern.test(text)) {
      return { passed: false, reason: "Appears to be spam" };
    }
  }

  return { passed: true };
}

/**
 * Call OpenAI Moderation API to check content
 * Returns true if content passes (not flagged)
 */
export const moderateWithOpenAI = action({
  args: { text: v.string() },
  handler: async (ctx, args): Promise<{ passed: boolean; reason?: string }> => {
    const apiKey = process.env.OPENAI_API_KEY;

    // If no API key, skip OpenAI check (blocklist still applies elsewhere)
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
        body: JSON.stringify({
          input: args.text,
        }),
      });

      if (!response.ok) {
        console.error("OpenAI moderation API error:", response.statusText);
        // Fail open - allow content if API fails
        return { passed: true };
      }

      const data = await response.json();
      const result = data.results[0];

      // Check specific categories: hate, harassment, sexual
      if (result.categories.hate || result.categories.harassment || result.categories.sexual) {
        return {
          passed: false,
          reason: "Content flagged by moderation system",
        };
      }

      return { passed: true };
    } catch (error) {
      console.error("OpenAI moderation error:", error);
      // Fail open - allow content if API fails
      return { passed: true };
    }
  },
});
