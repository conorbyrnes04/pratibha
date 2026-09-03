import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Glossary",
  description: "Lemmas across the traditions in the Pratibha corpus.",
};

export default function GlossaryLayout({ children }: { children: React.ReactNode }) {
  return children;
}
