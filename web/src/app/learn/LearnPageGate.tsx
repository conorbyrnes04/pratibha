"use client";

import dynamic from "next/dynamic";

function LearnPageFallback() {
  return (
    <main className="page-shell page-shell--paths">
      <div className="learn-tradition-bar" aria-hidden>
        <div className="learn-tradition-bar__inner" />
      </div>
    </main>
  );
}

const LearnPageClient = dynamic(() => import("./LearnPageClient"), {
  ssr: false,
  loading: LearnPageFallback,
});

export function LearnPageGate() {
  return <LearnPageClient />;
}
