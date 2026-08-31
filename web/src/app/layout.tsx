import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";
import { AuthGate } from "@/components/AuthGate";
import { AuthMenu } from "@/components/AuthMenu";
import { AuthProvider } from "@/components/AuthProvider";
import { BrandMark } from "@/components/BrandMark";
import { SiteNav } from "@/components/SiteNav";
import { GlyphUnlockHost } from "@/components/GlyphUnlockHost";
import { Toaster } from "@/components/ui/sonner";
import { ConvexClientProvider } from "@/lib/convexClient";
import { ConvexAuthNextjsServerProvider } from "@convex-dev/auth/nextjs/server";

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || "https://pratibha.agniagama.com";
const SITE_DESCRIPTION =
  "Pratibha is a multi-tradition wisdom study platform: layered canonical texts — original, translation, commentary, key terms, cross-tradition resonances, and practice — across the Upaniṣads, Tao Te Ching, Heraclitus, Patañjali, Kashmir Śaivism, Buddhism, and more, with a source-grounded study companion.";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: "Pratibha — Living Manuscript of World Wisdom",
    template: "%s · Pratibha",
  },
  description: SITE_DESCRIPTION,
  applicationName: "Pratibha",
  keywords: [
    "wisdom texts", "contemplative study", "Upanishads", "Tao Te Ching", "Heraclitus",
    "Patanjali Yoga Sutras", "Kashmir Shaivism", "Vijnana Bhairava", "Buddhism",
    "comparative philosophy", "meditation practice", "commentary",
  ],
  alternates: { canonical: "/" },
  openGraph: {
    type: "website",
    siteName: "Pratibha",
    url: SITE_URL,
    title: "Pratibha — Living Manuscript of World Wisdom",
    description: SITE_DESCRIPTION,
  },
  twitter: {
    card: "summary_large_image",
    title: "Pratibha — Living Manuscript of World Wisdom",
    description: SITE_DESCRIPTION,
  },
  robots: { index: true, follow: true },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const convexEnabled = Boolean((process.env.NEXT_PUBLIC_CONVEX_URL || "").trim());
  const body = (
    <html lang="en">
      <body className="antialiased">
        <ConvexClientProvider>
          <AuthProvider>
            <header className="sticky top-0 z-40 border-b border-[rgb(240_201_121_/_0.12)] bg-[#090912]/82 backdrop-blur-xl">
              <nav className="relative mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
                <Link href="/" className="group flex items-center gap-3 leading-none">
                  <BrandMark
                    size="md"
                    className="opacity-95 transition group-hover:opacity-100 group-hover:brightness-110"
                  />
                  <span>
                    <span className="block text-2xl font-semibold tracking-[-0.04em] text-amber-100">Pratibha</span>
                    <span className="mt-1 block font-sans text-xs uppercase tracking-[0.22em] text-stone-300 group-hover:text-amber-200">
                      Living Manuscript
                    </span>
                  </span>
                </Link>
                <div className="flex items-center gap-4 sm:gap-5">
                  <a
                    href="https://agniagama.com"
                    className="hidden font-sans text-xs uppercase tracking-[0.18em] text-stone-400 transition hover:text-amber-200 sm:inline"
                  >
                    Agni Agama
                  </a>
                  <SiteNav />
                  <AuthMenu />
                </div>
              </nav>
            </header>
            <AuthGate>{children}</AuthGate>
            <GlyphUnlockHost />
            <Toaster />
          </AuthProvider>
        </ConvexClientProvider>
      </body>
    </html>
  );
  if (!convexEnabled) return body;
  return <ConvexAuthNextjsServerProvider>{body}</ConvexAuthNextjsServerProvider>;
}
