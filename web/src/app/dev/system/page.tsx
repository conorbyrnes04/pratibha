"use client";

import { useState } from "react";
import { toast } from "sonner";
import { BrandMark } from "@/components/BrandMark";
import { FilterSelect } from "@/components/FilterSelect";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  Empty,
  EmptyDescription,
  EmptyHeader,
  EmptyTitle,
} from "@/components/ui/empty";
import { Input } from "@/components/ui/input";
import { KitLink } from "@/components/ui/kit-link";
import { Label } from "@/components/ui/label";
import { Progress } from "@/components/ui/progress";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { Skeleton } from "@/components/ui/skeleton";
import { Textarea } from "@/components/ui/textarea";

const TOKEN_SWATCHES = [
  { name: "--background", value: "#090912" },
  { name: "--foreground", value: "#f6efe4" },
  { name: "--card", value: "#171421" },
  { name: "--popover", value: "#211a2a" },
  { name: "--accent", value: "#d8a84a" },
  { name: "--accent-bright", value: "#f0c979" },
  { name: "--muted", value: "#a89882" },
  { name: "--lapis", value: "#324867" },
];

function Section({
  title,
  hint,
  children,
}: {
  title: string;
  hint?: string;
  children: React.ReactNode;
}) {
  return (
    <section className="manuscript-card p-5 sm:p-6">
      <h2 className="layer-heading">{title}</h2>
      {hint ? <p className="soft mt-2 max-w-2xl text-sm leading-relaxed">{hint}</p> : null}
      <div className="mt-5">{children}</div>
    </section>
  );
}

export default function DevSystemPage() {
  const [filterValue, setFilterValue] = useState("all");
  const [selectValue, setSelectValue] = useState("gold");
  const [checked, setChecked] = useState(false);
  const [progress, setProgress] = useState(42);
  const [layerOpen, setLayerOpen] = useState(false);

  return (
    <main className="page-shell max-w-4xl">
      <header className="manuscript-card overflow-hidden p-6 sm:p-8">
        <p className="eyebrow">Internal · Phase 4</p>
        <h1 className="mt-3 text-4xl font-semibold leading-none tracking-[-0.03em] text-amber-100 sm:text-5xl">
          Kit system
        </h1>
        <p className="soft mt-4 max-w-2xl text-lg leading-relaxed">
          Pratibha-skinned Monad / shadcn primitives. Not a stock Plex demo — tokens and type stay
          manuscript. Learn visualizations (PathTree, Threads, Yantra) are intentionally absent.
        </p>
        <div className="mt-6 flex flex-wrap gap-3">
          <KitLink href="/learn" variant="secondary" size="sm">
            Paths (custom)
          </KitLink>
          <KitLink href="/read" variant="secondary" size="sm">
            Library
          </KitLink>
          <KitLink href="/glossary" variant="secondary" size="sm">
            Glossary
          </KitLink>
        </div>
      </header>

      <div className="section-stack mt-8">
        <Section title="Tokens" hint="Mapped Monad slots → Pratibha palette (dark default).">
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            {TOKEN_SWATCHES.map((swatch) => (
              <div key={swatch.name} className="overflow-hidden rounded-xl border border-white/10">
                <div className="h-14" style={{ background: swatch.value }} />
                <div className="bg-black/30 px-2 py-2 font-sans text-[10px] tracking-wide text-stone-300">
                  <div>{swatch.name}</div>
                  <div className="text-stone-500">{swatch.value}</div>
                </div>
              </div>
            ))}
          </div>
          <p className="soft mt-4 font-sans text-sm">
            UI: Alegreya Sans · Reading: Cormorant Garamond · Scripts: Noto Devanagari / Tibetan /
            Arabic
          </p>
        </Section>

        <Section title="Button + KitLink">
          <div className="flex flex-wrap gap-2">
            <Button>Default</Button>
            <Button variant="secondary">Secondary</Button>
            <Button variant="ghost">Ghost</Button>
            <Button variant="destructive">Destructive</Button>
            <Button size="sm">Small</Button>
            <Button size="lg">Large</Button>
            <Button disabled>Disabled</Button>
            <KitLink href="/dev/system" variant="secondary" size="sm">
              KitLink
            </KitLink>
          </div>
        </Section>

        <Section title="Input · Textarea · Label">
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="sys-input">Lemma search</Label>
              <Input id="sys-input" placeholder="Search lemmas, scripts…" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="sys-note">Journal note</Label>
              <Textarea id="sys-note" rows={3} placeholder="Write a practice observation…" />
            </div>
          </div>
        </Section>

        <Section
          title="Select + FilterSelect"
          hint="Library / Chat / Oracle use FilterSelect (Base UI Combobox) with gold/lapis chrome."
        >
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="space-y-2">
              <Label>Kit Select</Label>
              <Select value={selectValue} onValueChange={(v) => setSelectValue(String(v ?? "gold"))}>
                <SelectTrigger className="w-full min-w-[12rem]">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="gold">Gold tone</SelectItem>
                  <SelectItem value="lapis">Lapis tone</SelectItem>
                  <SelectItem value="ink">Ink tone</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <FilterSelect
              label="Manuscript Combobox"
              tone={filterValue === "lapis" ? "lapis" : "gold"}
              value={filterValue}
              onChange={setFilterValue}
              options={[
                { value: "all", label: "All texts", hint: "shelf" },
                { value: "bg", label: "Bhagavad Gītā", icon: "ॐ", hint: "sanskrit" },
                { value: "lapis", label: "Lapis filter tone", hint: "demo" },
                { value: "en", label: "Enchiridion", hint: "greek" },
              ]}
            />
          </div>
        </Section>

        <Section title="Checkbox · Badge · Progress">
          <Label className="flex cursor-pointer items-start gap-3 font-normal text-stone-200">
            <Checkbox
              checked={checked}
              onCheckedChange={(v) => setChecked(v === true)}
              className="mt-0.5 border-amber-200/40 data-checked:border-amber-200 data-checked:bg-amber-200 data-checked:text-[#121018]"
            />
            <span>Gate checkbox — recognize this in experience</span>
          </Label>
          <div className="mt-4 flex flex-wrap gap-2">
            <Badge>Default</Badge>
            <Badge variant="secondary">Secondary</Badge>
            <Badge variant="outline">Outline</Badge>
            <Badge
              variant="outline"
              className="h-auto rounded-full border-amber-200/25 bg-amber-100/5 px-3 py-1 font-sans text-[10px] uppercase tracking-[0.12em] text-amber-200/75"
            >
              Corpus in progress · strong draft
            </Badge>
          </div>
          <div className="mt-5 space-y-2">
            <div className="flex items-center justify-between font-sans text-xs uppercase tracking-[0.18em] text-stone-400">
              <span>Progress</span>
              <span>{progress}%</span>
            </div>
            <Progress
              value={progress}
              className="w-full gap-0 [&_[data-slot=progress-track]]:h-3 [&_[data-slot=progress-track]]:bg-white/10 [&_[data-slot=progress-indicator]]:bg-amber-300"
            />
            <div className="flex gap-2">
              <Button size="sm" variant="secondary" onClick={() => setProgress((p) => Math.max(0, p - 10))}>
                −10
              </Button>
              <Button size="sm" variant="secondary" onClick={() => setProgress((p) => Math.min(100, p + 10))}>
                +10
              </Button>
            </div>
          </div>
        </Section>

        <Section title="Dialog · Sheet">
          <div className="flex flex-wrap gap-2">
            <Dialog>
              <DialogTrigger render={<Button variant="secondary" />}>Open dialog</DialogTrigger>
              <DialogContent className="border border-amber-200/20 bg-[#171421] sm:max-w-md">
                <DialogHeader>
                  <DialogTitle className="text-xl text-amber-100">Confirm action</DialogTitle>
                  <DialogDescription className="soft text-base">
                    Manuscript dialog chrome — used for path reset on Learn.
                  </DialogDescription>
                </DialogHeader>
                <DialogFooter className="border-amber-200/10 bg-transparent">
                  <Button variant="secondary">Cancel</Button>
                  <Button>Confirm</Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>
            <Sheet>
              <SheetTrigger render={<Button variant="secondary" />}>Open sheet</SheetTrigger>
              <SheetContent className="border-l border-amber-200/15 bg-[#0b0b14] sm:max-w-md">
                <SheetHeader>
                  <SheetTitle className="text-amber-100">Sheet / drawer</SheetTitle>
                  <SheetDescription className="soft">
                    Same family as mobile SiteNav. Keep manuscript surfaces, not stock cards.
                  </SheetDescription>
                </SheetHeader>
                <p className="mt-6 soft text-sm leading-relaxed">
                  Use for secondary navigation and mobile chrome — not for passage bodies.
                </p>
              </SheetContent>
            </Sheet>
          </div>
        </Section>

        <Section
          title="Collapsible"
          hint="Passage LayerBlock uses this for long appendixes. Keep source-script fonts on Original layers."
        >
          <Collapsible open={layerOpen} onOpenChange={setLayerOpen}>
            <CollapsibleTrigger className="flex w-full items-center justify-between text-left">
              <span className="layer-heading">Appendix layer</span>
              <span className="font-sans text-xs text-stone-400">{layerOpen ? "Collapse" : "Expand"}</span>
            </CollapsibleTrigger>
            <CollapsibleContent>
              <p className="reading-prose mt-4 text-stone-200">
                Collapsed layers expand in place. Do not replace LayerBlock with generic Accordion
                cards that drop Devanagari / Tibetan treatment.
              </p>
            </CollapsibleContent>
          </Collapsible>
        </Section>

        <Section title="Empty · Skeleton · Toast">
          <Empty className="border border-dashed border-amber-200/20 bg-black/20">
            <EmptyHeader>
              <EmptyTitle className="text-amber-100">No matching lemmas</EmptyTitle>
              <EmptyDescription className="soft">
                Empty states stay quiet — no dashboard chrome.
              </EmptyDescription>
            </EmptyHeader>
          </Empty>
          <div className="mt-4 space-y-2">
            <Skeleton className="h-4 w-2/3 bg-white/10" />
            <Skeleton className="h-4 w-1/2 bg-white/10" />
            <Skeleton className="h-24 w-full rounded-xl bg-white/5" />
          </div>
          <Button
            className="mt-4"
            variant="secondary"
            onClick={() => toast("Progress saved", { description: "Sonner toast on manuscript dark." })}
          >
            Fire toast
          </Button>
        </Section>

        <Section
          title="Pratibha-only (do not kit-replace)"
          hint="Escalate before swapping these for stock Cards or Accordion."
        >
          <ul className="soft list-inside list-disc space-y-1 text-sm leading-relaxed">
            <li>BrandMark · Glyph · InkGlyph · YantraBreath</li>
            <li>LayerBlock + source-script Original layers</li>
            <li>PathTree · ThreadsConstellation · JourneyMandala</li>
            <li>ThemeConstellation · ArtImage / collection art</li>
            <li>Lexicon flip card / SRS core</li>
          </ul>
          <div className="mt-5">
            <BrandMark size="md" className="opacity-90" />
          </div>
        </Section>

        <Separator className="bg-amber-200/15" />
        <p className="soft pb-8 text-center font-sans text-xs tracking-wide text-stone-500">
          /dev/system · Phase 4 showcase · light theme deferred
        </p>
      </div>
    </main>
  );
}
