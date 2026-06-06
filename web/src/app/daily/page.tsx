'use client';

import { useEffect } from "react";

/** Legacy route: /daily bookmarks land on the home daily header. */
export default function DailyRedirectPage() {
  useEffect(() => {
    window.location.replace("/#daily");
  }, []);

  return <main className="page-shell soft">Opening today&apos;s passage…</main>;
}
