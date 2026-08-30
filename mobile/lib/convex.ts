import { ConvexReactClient } from "convex/react";
import Constants from "expo-constants";

const convexUrl = 
  Constants.expoConfig?.extra?.convexUrl || 
  process.env.EXPO_PUBLIC_CONVEX_URL || 
  "https://energized-armadillo-158.convex.cloud";

export const convex = new ConvexReactClient(convexUrl);
