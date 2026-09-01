import type { Metadata } from "next";
import { LearnPageGate } from "./LearnPageGate";

export const metadata: Metadata = {
  title: "Path",
  description:
    "Walk a tradition as a trail of gates: teaching, passage, and practice, one step at a time.",
};

export default function LearnPage() {
  return <LearnPageGate />;
}
