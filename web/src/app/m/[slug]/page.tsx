"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useQuery } from "convex/react";
import { api } from "../../../../convex/_generated/api";
import { CONVEX_ENABLED } from "@/lib/convexConfigured";
import { ManuscriptFolio } from "@/components/ManuscriptFolio";

export default function PublicManuscriptPage() {
  const params = useParams<{ slug: string }>();
  const slug = decodeURIComponent(params.slug || "");

  if (!CONVEX_ENABLED) {
    return (
      <main className="page-shell page-shell--reading">
        <p className="soft">This manuscript is not available in this build.</p>
      </main>
    );
  }

  return <PublicManuscript slug={slug} />;
}

function PublicManuscript({ slug }: { slug: string }) {
  const manuscript = useQuery(api.manuscripts.getBySlug, { slug });

  if (manuscript === undefined) {
    return (
      <main className="page-shell page-shell--reading">
        <p className="soft">Opening the manuscript…</p>
      </main>
    );
  }

  if (!manuscript) {
    return (
      <main className="page-shell page-shell--reading">
        <h1 className="passage-reading__title">Manuscript not found</h1>
        <p className="soft mt-4">It may be private, or the link is wrong.</p>
        <Link href="/" className="mt-6 inline-block text-amber-100 underline">
          Today
        </Link>
      </main>
    );
  }

  return (
    <main className="page-shell page-shell--reading">
      <header className="passage-reading__header">
        <p className="passage-reading__meta">A student manuscript</p>
        <h1 className="passage-reading__title">{manuscript.title}</h1>
        <p className="passage-reading__deck">
          Gathered by {manuscript.displayName}
          {manuscript.entries.length ? ` · ${manuscript.entries.length} verses` : ""}
        </p>
      </header>

      {manuscript.entries.length === 0 ? (
        <p className="soft">This manuscript is still empty.</p>
      ) : (
        <div className="manuscript-grid">
          {manuscript.entries.map((entry) => (
            <ManuscriptFolio
              key={entry.verseId}
              verseId={entry.verseId}
              verseTitle={entry.verseTitle}
              note={entry.note}
              card={{
                mark: entry.mark,
                ink: entry.ink,
                textMode: entry.textMode,
                line: entry.line,
                aspectRatio: entry.aspectRatio,
                holographic: entry.holographic,
              }}
            />
          ))}
        </div>
      )}
    </main>
  );
}
