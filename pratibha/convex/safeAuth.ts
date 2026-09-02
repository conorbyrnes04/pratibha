import { getAuthUserId } from "@convex-dev/auth/server";

/** Auth lookup that never fails a public query — a session glitch returns signed-out. */
export async function optionalUserId(ctx: Parameters<typeof getAuthUserId>[0]) {
  try {
    return await getAuthUserId(ctx);
  } catch (error) {
    console.error("optionalUserId", error);
    return null;
  }
}

export function logQueryError(name: string, error: unknown) {
  console.error(`[pratibha] ${name}`, error);
}
