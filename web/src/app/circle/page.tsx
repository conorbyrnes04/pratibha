import type { Metadata } from "next";
import { CircleHubGate } from "./CircleHubGate";

export const metadata: Metadata = {
  title: "Circle",
  description:
    "A public house of readings on Pratibha. Offer what a verse asks of you, and reply to one another.",
  alternates: { canonical: "/circle" },
};

export default function CirclePage() {
  return <CircleHubGate />;
}
