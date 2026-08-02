"use client";

/**
 * Test sandbox for the Stripe Press–style 3D tome shelf.
 * Not linked from production Library — open /dev/tome-shelf locally.
 */

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { TomeShelf } from "@/components/tome3d";
import { getVerses } from "@/lib/api";
import { catalogMaturityKey, readCatalogCache } from "@/lib/catalogCache";
import { buildLibraryTomes } from "@/lib/libraryTomes";
import type { VerseItem } from "@/lib/types";

export default function DevTomeShelfPage() {
  const router = useRouter();
  const [items, setItems] = useState<VerseItem[]>([]);
  const [status, setStatus] = useState<"loading" | "ready" | "error">("loading");
  const [error, setError] = useState("");

  useEffect(() => {
    const cacheKey = catalogMaturityKey("strong_draft");
    const cached = readCatalogCache(cacheKey);
    if (cached?.items.length) {
      setItems(cached.items);
      setStatus("ready");
    }

    let cancelled = false;
    (async () => {
      try {
        const verses = await getVerses("strong_draft");
        if (cancelled) return;
        setItems(verses);
        setStatus("ready");
        setError("");
      } catch (e) {
        if (cancelled) return;
        if (!cached?.items.length) {
          setStatus("error");
          setError(e instanceof Error ? e.message : "Failed to load catalog");
        }
      }
    })();

    return () => {
      cancelled = true;
    };
  }, []);

  const tomes = useMemo(() => buildLibraryTomes(items), [items]);

  return (
    <main className="page-shell page-shell--library">
      <header className="library-header">
        <div className="library-header__body">
          <p className="passage-reading__meta">Dev · test build</p>
          <h1 className="library-header__title">3D tome shelf</h1>
          <p className="library-header__lede">
            Sandbox for the WebGL shelf. Production Library stays on cards — this route is for local
            iteration only.
          </p>
          <p className="soft font-sans text-sm mt-3">
            <Link href="/read" className="text-amber-100/90 underline-offset-2 hover:underline">
              ← Back to Library
            </Link>
            {" · "}
            <Link href="/dev/system" className="text-amber-100/90 underline-offset-2 hover:underline">
              System kit
            </Link>
          </p>
        </div>
      </header>

      <div className="section-stack section-stack--tight mt-6">
        {status === "loading" ? <p className="soft">Loading catalog…</p> : null}
        {status === "error" ? <p className="soft text-red-200/90">{error}</p> : null}
        {status === "ready" && tomes.length === 0 ? (
          <p className="soft">No tomes in the catalog yet.</p>
        ) : null}
        {tomes.length > 0 ? (
          <TomeShelf
            tomes={tomes}
            onOpen={(collection) => {
              router.push(`/read?collection=${encodeURIComponent(collection)}`);
            }}
          />
        ) : null}
      </div>
    </main>
  );
}
