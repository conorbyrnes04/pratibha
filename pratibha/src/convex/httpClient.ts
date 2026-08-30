// HTTP client for Convex to avoid BigInt compatibility issues on native Lynx
const CONVEX_URL = process.env.NEXT_PUBLIC_CONVEX_URL || "";

interface ConvexHttpClient {
  query: (name: string, args: any) => Promise<any>;
  mutation: (name: string, args: any) => Promise<any>;
  action: (name: string, args: any) => Promise<any>;
}

let authToken: string | null = null;

export function setAuthToken(token: string | null) {
  authToken = token;
}

export function getAuthToken(): string | null {
  return authToken;
}

export async function convexFetch(
  functionName: string,
  args: any,
  type: "query" | "mutation" | "action" = "query"
): Promise<any> {
  if (!CONVEX_URL) {
    throw new Error("NEXT_PUBLIC_CONVEX_URL not configured");
  }

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (authToken) {
    headers["Authorization"] = `Bearer ${authToken}`;
  }

  // Correct Convex HTTP API format
  const url = `${CONVEX_URL}/api/${type}`;

  const response = await fetch(url, {
    method: "POST",
    headers,
    body: JSON.stringify({
      path: functionName,
      args: args,
      format: "json",
    }),
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Convex ${type} failed: ${error}`);
  }

  const data = await response.json();
  return data.value;
}

export function createHttpClient(): ConvexHttpClient {
  return {
    query: (name: string, args: any) => convexFetch(name, args, "query"),
    mutation: (name: string, args: any) => convexFetch(name, args, "mutation"),
    action: (name: string, args: any) => convexFetch(name, args, "action"),
  };
}
