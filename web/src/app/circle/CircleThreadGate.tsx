"use client";

import dynamic from "next/dynamic";

const CircleThreadPage = dynamic(
  () => import("@/components/CircleThreadPage").then((m) => ({ default: m.CircleThreadPage })),
  { ssr: false },
);

export function CircleThreadGate() {
  return <CircleThreadPage />;
}
