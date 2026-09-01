"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { useAuth } from "@/components/AuthProvider";
import { GlyphMala } from "@/components/GlyphMala";
import { GlyphMarkPicker } from "@/components/GlyphMarkPicker";
import { LanguagePicker } from "@/components/LanguagePicker";
import { useT } from "@/components/LocaleProvider";
import { Button, buttonVariants } from "@/components/ui/button";
import { useAvatarMark } from "@/lib/useAvatarMark";
import { cn } from "@/lib/utils";

export default function AccountPage() {
  const router = useRouter();
  const t = useT();
  const { configured, loading, user, signOut } = useAuth();
  const { mark, ink, choose, chooseInk, openMarks } = useAvatarMark();

  useEffect(() => {
    if (!loading && configured && !user) {
      router.replace("/login?next=/account");
    }
  }, [loading, configured, user, router]);

  if (!configured) {
    return (
      <main className="mx-auto max-w-lg px-4 py-16">
        <h1 className="text-4xl text-amber-100">{t("auth.account")}</h1>
        <p className="soft mt-4 font-sans text-sm">{t("auth.authUnconfigured")}</p>
      </main>
    );
  }

  if (loading || !user) {
    return (
      <main className="mx-auto max-w-lg px-4 py-16">
        <p className="soft font-sans text-sm">{t("auth.loadingAccount")}</p>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-2xl px-4 py-16">
      <p className="font-sans text-xs uppercase tracking-[0.22em] text-stone-400">{t("auth.account")}</p>
      <h1 className="mt-2 text-4xl text-amber-100">{t("auth.signedIn")}</h1>
      <p className="soft mt-4 font-sans text-sm">{user.email}</p>
      <p className="soft mt-2 font-sans text-sm">{t("account.lede")}</p>
      <div className="mt-8">
        <LanguagePicker variant="panel" />
      </div>
      <div className="mt-10">
        <p className="font-sans text-xs uppercase tracking-[0.22em] text-stone-400">{t("account.marks")}</p>
        <p className="soft mt-2 mb-3 font-sans text-sm">{t("account.marksLede")}</p>
        <GlyphMala />
      </div>
      <div id="mark" className="mt-10 scroll-mt-24">
        <p className="font-sans text-xs uppercase tracking-[0.22em] text-stone-400">{t("account.yourMark")}</p>
        <p className="soft mt-2 mb-4 font-sans text-sm">{t("account.yourMarkLede")}</p>
        <GlyphMarkPicker
          selected={mark}
          ink={ink}
          openMarks={openMarks}
          onChoose={(next) => void choose(next)}
          onInk={(next) => void chooseInk(next)}
        />
      </div>
      <div className="mt-8 flex flex-wrap gap-3">
        <Link href="/journal" className={cn(buttonVariants())}>
          {t("common.openJournal")}
        </Link>
        <Link href="/manuscript" className={cn(buttonVariants({ variant: "secondary" }))}>
          {t("common.yourManuscript")}
        </Link>
        <Button
          type="button"
          variant="secondary"
          onClick={() => {
            void signOut().then(() => router.push("/"));
          }}
        >
          {t("auth.signOut")}
        </Button>
      </div>
    </main>
  );
}
