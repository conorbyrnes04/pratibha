import { convexAuth } from "@convex-dev/auth/server";
import { Password } from "@convex-dev/auth/providers/Password";
import Google from "@auth/core/providers/google";
import { query } from "./_generated/server";
import { getAuthUserId } from "@convex-dev/auth/server";

export const { auth, signIn, signOut, store } = convexAuth({
  providers: [
    Password,
    // Google OAuth - reads AUTH_GOOGLE_ID and AUTH_GOOGLE_SECRET from env
    // Also supports legacy GOOGLE_CLIENT_ID/GOOGLE_CLIENT_SECRET
    Google({
      clientId: process.env.AUTH_GOOGLE_ID || process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.AUTH_GOOGLE_SECRET || process.env.GOOGLE_CLIENT_SECRET,
    }),
  ],
  callbacks: {
    async redirect({ redirectTo }) {
      // Allow redirects to site URL and common local/dev URLs
      const siteUrl = process.env.SITE_URL;
      const allowedOrigins = [
        siteUrl,
        "http://localhost:3000",
        "http://localhost:3004",
        "http://localhost:8000",
      ].filter(Boolean) as string[];

      // If redirectTo starts with any allowed origin, allow it
      for (const origin of allowedOrigins) {
        if (redirectTo.startsWith(origin)) {
          return redirectTo;
        }
      }

      // For OAuth callbacks, allow the Convex deployment URL
      // (redirectTo will be the callback URL from Google)
      if (redirectTo.includes(".convex.site") || redirectTo.includes(".convex.cloud")) {
        return redirectTo;
      }

      // Default to first allowed origin or empty string
      return allowedOrigins[0] || "";
    },
  },
});

export const currentUser = query({
  args: {},
  handler: async (ctx) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) {
      return null;
    }
    const user = await ctx.db.get(userId);
    return user;
  },
});
