"use client";

import { ConvexAuthNextjsProvider } from "@convex-dev/auth/nextjs";
import { ConvexReactClient } from "convex/react";
import { ReactNode, useMemo } from "react";
import { CONVEX_ENABLED, CONVEX_URL } from "@/lib/convexConfigured";

export function ConvexClientProvider({ children }: { children: ReactNode }) {
  const client = useMemo(
    () => (CONVEX_ENABLED ? new ConvexReactClient(CONVEX_URL) : null),
    [],
  );

  if (!client) {
    return <>{children}</>;
  }

  return <ConvexAuthNextjsProvider client={client}>{children}</ConvexAuthNextjsProvider>;
}
