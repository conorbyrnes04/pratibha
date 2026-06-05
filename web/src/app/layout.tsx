import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";
import { SiteNav } from "@/components/SiteNav";

export const metadata: Metadata = {
  title: "Pratibha",
  description: "A study companion for timeless wisdom texts",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        <header className="sticky top-0 z-40 border-b border-[rgb(240_201_121_/_0.12)] bg-[#090912]/82 backdrop-blur-xl">
          <nav className="relative mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
            <Link href="/" className="group leading-none">
              <span className="block text-2xl font-semibold tracking-[-0.04em] text-amber-100">Pratibha</span>
              <span className="mt-1 block font-sans text-[10px] uppercase tracking-[0.28em] text-stone-400 group-hover:text-amber-200">
                Living Manuscript
              </span>
            </Link>
            <SiteNav />
          </nav>
        </header>
        {children}
      </body>
    </html>
  );
}
