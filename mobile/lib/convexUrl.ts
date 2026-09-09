import Constants from "expo-constants";

export const PRODUCTION_CONVEX_URL = "https://giant-lapwing-264.convex.cloud";

export function getConvexUrl(): string {
  const extra = Constants.expoConfig?.extra as { convexUrl?: string } | undefined;
  return extra?.convexUrl || process.env.EXPO_PUBLIC_CONVEX_URL || PRODUCTION_CONVEX_URL;
}
