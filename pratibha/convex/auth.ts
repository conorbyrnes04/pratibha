import { convexAuth } from "@convex-dev/auth/server";
import { Password } from "@convex-dev/auth/providers/Password";
import Google from "@auth/core/providers/google";
import { query } from "./_generated/server";
import { getAuthUserId } from "@convex-dev/auth/server";

const providers = [
  Password({
    validatePasswordRequirements: (password: string) => {
      if (password.length < 10) {
        throw new Error("Password must be at least 10 characters.");
      }
    },
  }),
];

// Only add Google OAuth if credentials are configured
if (process.env.GOOGLE_CLIENT_ID && process.env.GOOGLE_CLIENT_SECRET) {
  providers.push(
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    })
  );
}

export const { auth, signIn, signOut, store } = convexAuth({
  providers,
  callbacks: {
    async redirect({ redirectTo }) {
      const siteUrl = process.env.SITE_URL || "http://localhost:3000";
      const allowed = [
        siteUrl,
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3004",
        "https://pratibha.agniagama.com",
      ].filter(Boolean) as string[];
      for (const origin of allowed) {
        if (redirectTo.startsWith(origin)) return redirectTo;
      }
      if (
        redirectTo.startsWith("http://192.168.") ||
        redirectTo.startsWith("http://10.") ||
        redirectTo.includes(".convex.site") ||
        redirectTo.includes(".convex.cloud")
      ) {
        return redirectTo;
      }
      return allowed[0] || siteUrl;
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
