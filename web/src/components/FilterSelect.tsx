"use client";

import dynamic from "next/dynamic";
import { cn } from "@/lib/utils";
import type { FilterSelectProps } from "./filterSelectTypes";

export type { FilterSelectOption, FilterSelectProps } from "./filterSelectTypes";

const FilterSelectLoaded = dynamic(
  () => import("./FilterSelectInner").then((m) => ({ default: m.FilterSelectInner })),
  {
    ssr: false,
    loading: () => (
      <div className={cn("filter-select")} aria-hidden>
        <div className="layer-heading mb-2 block">&nbsp;</div>
        <div className="filter-select__trigger relative min-h-[2.8rem]" />
      </div>
    ),
  },
);

/**
 * Manuscript filter control — Base UI Combobox with searchable popup.
 * Combobox stays out of the Worker SSR graph (Cloudflare 3 MiB cap).
 */
export function FilterSelect(props: FilterSelectProps) {
  return <FilterSelectLoaded {...props} />;
}
