const CONVEX_URL = (process.env.NEXT_PUBLIC_CONVEX_URL || "").replace(/\/$/, "");

interface ConvexHttpClient {
  query: (name: string, args: Record<string, unknown>) => Promise<unknown>;
  mutation: (name: string, args: Record<string, unknown>) => Promise<unknown>;
  action: (name: string, args: Record<string, unknown>) => Promise<unknown>;
}

let authToken: string | null = null;

export function setAuthToken(token: string | null) {
  authToken = token;
}

export function getAuthToken(): string | null {
  return authToken;
}

export function isConvexConfigured(): boolean {
  return Boolean(CONVEX_URL);
}

export async function convexFetch(
  functionName: string,
  args: Record<string, unknown> = {},
  type: "query" | "mutation" | "action" = "query",
): Promise<any> {
  if (!CONVEX_URL) {
    throw new Error("NEXT_PUBLIC_CONVEX_URL not configured");
  }

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };
  if (authToken) {
    headers.Authorization = `Bearer ${authToken}`;
  }

  const response = await fetch(`${CONVEX_URL}/api/${type}`, {
    method: "POST",
    headers,
    body: JSON.stringify({ path: functionName, args, format: "json" }),
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok || data.status === "error") {
    throw new Error(data.errorMessage || data.message || `Convex ${type} failed`);
  }
  return data.value;
}

export function createHttpClient(): ConvexHttpClient {
  return {
    query: (name, args) => convexFetch(name, args, "query"),
    mutation: (name, args) => convexFetch(name, args, "mutation"),
    action: (name, args) => convexFetch(name, args, "action"),
  };
}
