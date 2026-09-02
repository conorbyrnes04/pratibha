import type { MetadataRoute } from "next";
import { getVerses } from "@/lib/api";
import { isReaderFacingUnit } from "@/lib/corpusFilters";

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || "https://pratibha.agniagama.com";

const STATIC_PATHS = [
  "/",
  "/read",
  "/learn",
  "/circle",
  "/glossary",
  "/glossary/study",
  "/random",
  "/sources",
  "/chat",
];

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const now = new Date();
  const staticEntries: MetadataRoute.Sitemap = STATIC_PATHS.map((path) => ({
    url: `${SITE_URL}${path}`,
    lastModified: now,
    changeFrequency: "weekly",
    priority: path === "/" ? 1 : 0.7,
  }));

  let passageEntries: MetadataRoute.Sitemap = [];
  try {
    const verses = await getVerses("strong_draft");
    passageEntries = verses
      .filter(isReaderFacingUnit)
      .map((verse) => ({
        url: `${SITE_URL}/read/${encodeURIComponent(verse._id)}`,
        lastModified: now,
        changeFrequency: "monthly" as const,
        priority: 0.5,
      }));
  } catch {
    // A cold or unreachable corpus API should not break the sitemap — ship the
    // static routes and let the next crawl pick up passages.
    passageEntries = [];
  }

  return [...staticEntries, ...passageEntries];
}
