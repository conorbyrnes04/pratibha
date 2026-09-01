import { Redirect, useLocalSearchParams } from "expo-router";

export default function ChatTabRedirect() {
  const params = useLocalSearchParams<{ q?: string; verse_id?: string; mode?: string }>();
  return (
    <Redirect
      href={{
        pathname: "/ask",
        params: {
          ...(typeof params.q === "string" ? { q: params.q } : {}),
          ...(typeof params.verse_id === "string" ? { verse_id: params.verse_id } : {}),
          ...(typeof params.mode === "string" ? { mode: params.mode } : {}),
        },
      } as never}
    />
  );
}
