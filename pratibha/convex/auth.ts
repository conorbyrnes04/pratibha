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
    async redirect({ url, baseUrl }) {
      // Allow redirects to site URL and common local/dev URLs
      const siteUrl = process.env.SITE_URL;
      const allowedOrigins = [
        baseUrl,
        siteUrl,
        "http://localhost:3000",
        "http://localhost:3004",
        "http://localhost:8000",
      ].filter(Boolean);

      // If url starts with any allowed origin, allow it
      for (const origin of allowedOrigins) {
        if (url.startsWith(origin!)) {
          return url;
        }
      }

      // Default to baseUrl
      return baseUrl;
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
