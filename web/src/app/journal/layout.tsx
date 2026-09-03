import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Journal",
  description: "Private notes on passages and conversations with Pratibha.",
  alternates: { canonical: "/journal" },
  robots: { index: false, follow: false },
};

export default function JournalLayout({ children }: { children: React.ReactNode }) {
  return children;
}
