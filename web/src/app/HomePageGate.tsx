"use client";

import dynamic from "next/dynamic";
import { useT } from "@/components/LocaleProvider";

function HomePageFallback() {
  const t = useT();
  return (
    <main className="page-shell page-shell--reading">
      <header className="passage-reading__header">
        <p className="passage-reading__meta">{t("today.meta")}</p>
        <h1 className="passage-reading__title">{t("today.opening")}</h1>
        <p className="passage-reading__deck">{t("today.openingLede")}</p>
      </header>
    </main>
  );
}

const HomePageClient = dynamic(() => import("./HomePageClient"), {
  ssr: false,
  loading: HomePageFallback,
});

export function HomePageGate() {
  return <HomePageClient />;
}
