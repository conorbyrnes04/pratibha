import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Sources",
  description: "Where each text in Pratibha comes from, grouped by tradition.",
  alternates: { canonical: "/sources" },
};

export default function SourcesLayout({ children }: { children: React.ReactNode }) {
  return children;
}
