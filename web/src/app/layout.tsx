import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

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
        <header className="border-b border-amber-200/10 bg-slate-950/95 backdrop-blur">
          <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
            <Link href="/" className="text-xl font-semibold text-amber-200">
              Pratibha
            </Link>
            <div className="flex items-center gap-4 text-sm">
              <Link href="/read" className="nav-link">
                Read
              </Link>
              <Link href="/daily" className="nav-link">
                Daily
              </Link>
              <Link href="/random" className="nav-link">
                Random
              </Link>
              <Link href="/chat" className="nav-link">
                Study Chat
              </Link>
              <Link href="/learn" className="nav-link">
                Learning Paths
              </Link>
            </div>
          </nav>
        </header>
        {children}
      </body>
    </html>
  );
}
