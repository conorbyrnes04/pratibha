import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Ask Pratibha",
  description: "A source-grounded study companion for the Pratibha manuscript.",
  alternates: { canonical: "/chat" },
  robots: { index: false, follow: false },
};

export default function ChatLayout({ children }: { children: React.ReactNode }) {
  return children;
}
