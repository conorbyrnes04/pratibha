import { API_BASE } from "@/lib/api";

/** Hit FastAPI /me with the Supabase access token (optional wiring check). */
export async function fetchMe(accessToken: string): Promise<{ id: string; email: string | null } | null> {
  const res = await fetch(`${API_BASE}/me`, {
    headers: { Authorization: `Bearer ${accessToken}` },
    cache: "no-store",
  });
  if (!res.ok) return null;
  const data = await res.json();
  return { id: String(data?.id || ""), email: data?.email ? String(data.email) : null };
}
