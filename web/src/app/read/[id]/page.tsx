import type { Metadata } from "next";
import { cache } from "react";
import { getVerse } from "@/lib/api";
import { displayCollectionName } from "@/lib/collectionLabels";
import { displayPassageLocation, displayPassageTitle } from "@/lib/passageTitles";
import { passagePreview } from "@/lib/verseLayers";
import { firstSentence } from "@/lib/textPreview";
import { PassageReader } from "./PassageReader";

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || "https://pratibha.agniagama.com";

// Request-scoped so generateMetadata and the page share a single fetch.
const loadVerse = cache(async (id: string) => {
  try {
    return await getVerse(id);
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
  const canonical = `/read/${encodeURIComponent(id)}`;

  const verse = await loadVerse(id);

  if (!verse) {
    // Unknown passage — let the not-found UI handle it, but don't advertise it.
    return {
      title: "Passage",
      alternates: { canonical },
      robots: { index: false, follow: true },
    };
  }

  const title = displayPassageTitle(verse);
  const collection = displayCollectionName(verse.collection) || verse.collection || "";
  const location = displayPassageLocation(verse);
  const source = [collection, location].filter(Boolean).join(" · ");
  const preview = firstSentence(passagePreview(verse) || "").trim();
  const description = preview || `${title}${source ? ` — ${source}` : ""}`;
  const ogTitle = source ? `${title} · ${source}` : title;

  return {
    title,
    description,
    alternates: { canonical },
    openGraph: {
      type: "article",
      title: ogTitle,
      description,
      url: `${SITE_URL}${canonical}`,
    },
    twitter: {
      card: "summary_large_image",
      title: ogTitle,
      description,
    },
  };
}

export default async function VerseDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  // Server-fetch the passage so its content is present in the initial HTML for
  // crawlers/social previews. The client reader hydrates and enhances (related,
  // localization, siblings). We intentionally do not `notFound()` on a null:
  // the corpus API cold-starts, and a transient null must not 404 a real passage
  // (unknown ids are marked `noindex` in generateMetadata above).
  const verse = await loadVerse(id);
  return <PassageReader initialItem={verse} />;
}
