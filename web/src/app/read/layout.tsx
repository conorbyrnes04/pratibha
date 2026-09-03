import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Library",
  description: "Browse the Pratibha corpus by text, theme, and tradition.",
};

export default function ReadLayout({ children }: { children: React.ReactNode }) {
  return children;
}
