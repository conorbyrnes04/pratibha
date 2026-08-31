import type { Metadata } from "next";
import Link from "next/link";
import { getVerse } from "@/lib/api";
import { layerText } from "@/lib/verseLayers";
import { displayCollectionName } from "@/lib/collectionLabels";
import { displayPassageTitle } from "@/lib/passageTitles";
import { stripMarkdown } from "@/lib/textPreview";
import { folioCandidates, parseShareOptions, pickFolioLine } from "@/lib/shareCard";
import { ShareCard } from "@/components/ShareCard";
import { buttonVariants } from "@/components/ui/button";

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || "https://pratibha.agniagama.com";

type PageProps = {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ g?: string; ink?: string; t?: string; l?: string }>;
};

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { id } = await params;
  const verseId = decodeURIComponent(id);
  const item = await getVerse(verseId);
  const title = item ? displayPassageTitle(item) : "Pratibha";
  const description = stripMarkdown(item ? layerText(item, "translation") : "").slice(0, 180);
  return {
    title,
    description,
    openGraph: {
      title,
      description,
      url: `${SITE_URL}/s/${encodeURIComponent(verseId)}`,
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
    },
  };
}

export default async function SharedPage({ params, searchParams }: PageProps) {
  const { id } = await params;
  const query = await searchParams;
  const verseId = decodeURIComponent(id);
  const item = await getVerse(verseId);
  if (!item) {
    return (
      <main className="page-shell page-shell--reading">
        <h1 className="passage-reading__title">Passage not found</h1>
        <Link href="/" className="mt-6 inline-block text-amber-100 underline">
          Today
        </Link>
      </main>
    );
  }

  const options = parseShareOptions(verseId, query, item);
  const original = stripMarkdown(layerText(item, "original"));
  const iast = stripMarkdown(layerText(item, "iast"));
  const translation = stripMarkdown(layerText(item, "translation") || item.translation || "");
  const picked = pickFolioLine(
    folioCandidates({ original, iast, translation, mode: options.textMode }),
    options.line,
  );
  const copy = {
    title: displayPassageTitle(item),
    collection: displayCollectionName(item.collection) || item.collection,
    original: picked && picked.source !== "translation" ? picked.text : original,
    translation: picked?.source === "translation" ? picked.text : picked ? undefined : translation,
  };
  const displayMode = picked ? (picked.source === "translation" ? "translation" : "original") : options.textMode;

  return (
    <main className="page-shell page-shell--reading">
      <header className="passage-reading__header">
        <p className="passage-reading__meta">A page from Pratibha</p>
        <h1 className="passage-reading__title">{copy.title}</h1>
      </header>
      <div className="share-card-preview mx-auto">
        <ShareCard
          mark={options.mark}
          ink={options.ink}
          textMode={displayMode}
          copy={copy}
          fillWindow={Boolean(picked)}
        />
      </div>
      <div className="passage-reading__nav mt-8">
        <Link href={`/read/${encodeURIComponent(verseId)}`} className={buttonVariants()}>
          Open the passage
        </Link>
      </div>
    </main>
  );
}
