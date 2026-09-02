import type { Metadata } from "next";
import { CircleThreadGate } from "../CircleThreadGate";

export const metadata: Metadata = {
  title: "Thread",
  description: "A public reading in the Pratibha circle.",
};

export default function CircleReadingPage() {
  return <CircleThreadGate />;
}
