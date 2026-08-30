import React, { createContext, useContext, ReactNode } from "react";

// Placeholder for Convex integration
// Due to BigInt compatibility issues on native Lynx (PrimJS), we'll use HTTP for Convex
// On Web target, this works fine as browsers have BigInt support

interface ConvexContextType {
  isReady: boolean;
}

const ConvexContext = createContext<ConvexContextType>({ isReady: false });

export function ConvexProvider({ children }: { children: ReactNode }) {
  // For now, we'll implement HTTP-based Convex communication
  // to avoid BigInt issues mentioned in get-convex/convex-js#71
  
  const value: ConvexContextType = {
    isReady: true,
  };

  return <ConvexContext.Provider value={value}>{children}</ConvexContext.Provider>;
}

export function useConvex() {
  return useContext(ConvexContext);
}
