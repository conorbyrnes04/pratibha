import type { Metadata } from "next";
import { cache } from "react";
import { getLemma } from "@/lib/api";
import { nativeScript, romanization } from "@/lib/lexiconDisplay";
import { LemmaReader } from "./LemmaReader";

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || "https://pratibha.agniagama.com";

const loadLemma = cache(async (id: string) => {
  try {
    return await getLemma(id);
  } catch {
    return null;
  }
});

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>;
}): Promise<Metadata> {
  const { id } = await params;
  const canonical = `/glossary/${encodeURIComponent(id)}`;
  const lemma = await loadLemma(id);

  if (!lemma) {
    return {
      title: "Glossary",
      alternates: { canonical },
      robots: { index: false, follow: true },
    };
  }

  const roman = romanization(lemma.scripts) || lemma.id;
  const native = nativeScript(lemma.scripts);
  const title = native ? `${roman} · ${native}` : roman;
  const description = lemma.senses?.[0]?.short || `${roman} — a key term across traditions in the Pratibha lexicon.`;

  return {
    title,
    description,
    alternates: { canonical },
    openGraph: {
      type: "article",
      title,
      description,
      url: `${SITE_URL}${canonical}`,
    },
    twitter: { card: "summary_large_image", title, description },
  };
}

export default async function GlossaryLemmaPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const lemma = await loadLemma(id);
  return <LemmaReader initialLemma={lemma} />;
}
