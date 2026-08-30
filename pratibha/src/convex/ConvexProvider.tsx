import React, { createContext, useContext, ReactNode } from "react";
import { createHttpClient } from "./httpClient";

interface ConvexContextType {
  isReady: boolean;
  httpClient: ReturnType<typeof createHttpClient> | null;
}

const ConvexContext = createContext<ConvexContextType>({
  isReady: false,
  httpClient: null,
});

export function ConvexProvider({ children }: { children: ReactNode }) {
  const httpClient = createHttpClient();

  const value: ConvexContextType = {
    isReady: true,
    httpClient,
  };

  return <ConvexContext.Provider value={value}>{children}</ConvexContext.Provider>;
}

export function useConvex() {
  return useContext(ConvexContext);
}
