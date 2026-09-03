import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Oracle",
  description: "Draw a random passage from the Pratibha corpus.",
  alternates: { canonical: "/random" },
};

export default function RandomLayout({ children }: { children: React.ReactNode }) {
  return children;
}
