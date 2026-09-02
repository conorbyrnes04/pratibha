import type { Metadata, Viewport } from "next";
import Script from "next/script";
import "./globals.css";
import { AuthGate } from "@/components/AuthGate";
import { AuthProvider } from "@/components/AuthProvider";
import { GlyphUnlockHost } from "@/components/GlyphUnlockHost";
import { LocaleProvider } from "@/components/LocaleProvider";
import { SiteHeader } from "@/components/SiteHeader";
import { SiteDock } from "@/components/SiteNav";
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
    images: [
      {
        url: "/brand/og-cover.jpg",
        width: 1200,
        height: 630,
        alt: "Pratibha — a yantra mandala over a living manuscript field",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Pratibha — Living Manuscript of World Wisdom",
    description: SITE_DESCRIPTION,
    images: ["/brand/og-cover.jpg"],
  },
  robots: { index: true, follow: true },
  icons: {
    icon: [
      { url: "/brand/yantra-seal-32.png", type: "image/png", sizes: "32x32" },
      { url: "/brand/yantra-seal-48.png", type: "image/png", sizes: "48x48" },
      { url: "/brand/yantra-seal-192.png", type: "image/png", sizes: "192x192" },
    ],
    apple: [{ url: "/brand/yantra-seal-180.png", sizes: "180x180", type: "image/png" }],
  },
};

export const viewport: Viewport = {
  themeColor: "#090912",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const convexEnabled = Boolean((process.env.NEXT_PUBLIC_CONVEX_URL || "").trim());
  const body = (
    <html lang="en" suppressHydrationWarning>
      <body className="antialiased">
        {/* Warm the Google Fonts connections early so the render-blocking @import
         * in globals.css resolves faster (reduces FOUT / layout shift). */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <Script id="pratibha-locale" strategy="beforeInteractive">
          {`(function(){try{var l=localStorage.getItem("pratibha.locale.v1");var ok={"en":1,"fr":1,"es":1,"pt-BR":1,"zh":1,"ru":1,"ja":1,"ar":1};if(!l||!ok[l])return;document.documentElement.lang=l==="zh"?"zh-Hans":l;document.documentElement.dir=l==="ar"?"rtl":"ltr";}catch(e){}})();`}
        </Script>
        <a href="#main-content" className="skip-link">
          Skip to content
        </a>
        <ConvexClientProvider>
          <AuthProvider>
            <LocaleProvider>
              <SiteHeader />
              <SiteDock />
              <div id="main-content">
                <AuthGate>{children}</AuthGate>
              </div>
              <GlyphUnlockHost />
              <Toaster />
            </LocaleProvider>
          </AuthProvider>
        </ConvexClientProvider>
      </body>
    </html>
  );
  if (!convexEnabled) return body;
  return <ConvexAuthNextjsServerProvider>{body}</ConvexAuthNextjsServerProvider>;
}
