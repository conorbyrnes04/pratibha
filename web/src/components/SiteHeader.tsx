"use client";

import Link from "next/link";
import { AuthMenu } from "@/components/AuthMenu";
import { BrandMark } from "@/components/BrandMark";
import { LanguagePicker } from "@/components/LanguagePicker";
import { SiteNav } from "@/components/SiteNav";
import { useT } from "@/components/LocaleProvider";

export function SiteHeader() {
  const t = useT();
  return (
    <header className="sticky top-0 z-40 border-b border-[rgb(240_201_121_/_0.12)] bg-[#090912]/82 backdrop-blur-xl">
      <nav className="relative mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        <Link href="/" className="group flex items-center gap-3 leading-none">
          <BrandMark
            size="md"
            className="opacity-95 transition group-hover:opacity-100 group-hover:brightness-110"
          />
          <span>
            <span className="block text-2xl font-semibold tracking-[-0.04em] text-amber-100">
              {t("brand.name")}
            </span>
            <span className="mt-1 block font-sans text-xs uppercase tracking-[0.22em] text-stone-300 group-hover:text-amber-200">
              {t("brand.tagline")}
            </span>
          </span>
        </Link>
        <div className="flex items-center gap-3 sm:gap-5">
          <a
            href="https://agniagama.com"
            className="hidden font-sans text-xs uppercase tracking-[0.18em] text-stone-400 transition hover:text-amber-200 lg:inline"
          >
            {t("brand.agniAgama")}
          </a>
          <SiteNav />
          <LanguagePicker />
          <AuthMenu />
        </div>
      </nav>
    </header>
  );
}
