import type { Metadata } from "next";
import { HomePageGate } from "./HomePageGate";

export const metadata: Metadata = {
  alternates: { canonical: "/" },
};

export default function HomePage() {
  return <HomePageGate />;
}
