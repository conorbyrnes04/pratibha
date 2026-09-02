"use client";

import dynamic from "next/dynamic";
import { SanghaBoundary } from "@/components/SanghaBoundary";

const CircleHub = dynamic(
  () => import("@/components/CircleHub").then((m) => ({ default: m.CircleHub })),
  { ssr: false },
);

export function CircleHubGate() {
  return (
    <SanghaBoundary>
      <CircleHub />
    </SanghaBoundary>
  );
}
