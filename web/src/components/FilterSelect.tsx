"use client";

import { useId, useMemo } from "react";
import { Combobox } from "@base-ui/react/combobox";
import { cn } from "@/lib/utils";
import { useT } from "@/components/LocaleProvider";

export type FilterSelectOption = {
  value: string;
  label: string;
  hint?: string;
  icon?: string;
};

type FilterSelectProps = {
  label: string;
  value: string;
  onChange: (value: string) => void;
  options: FilterSelectOption[];
  /** Gold for collections, lapis for themes */
  tone?: "gold" | "lapis";
  placeholder?: string;
};

/**
 * Manuscript filter control — Base UI Combobox with searchable popup.
 * Keeps filter-select CSS (gold/lapis) so Library / Chat / Oracle stay on-brand.
 */
export function FilterSelect({
  label,
  value,
  onChange,
  options,
  tone = "gold",
  placeholder,
}: FilterSelectProps) {
  const t = useT();
  const inputId = useId();
  const resolvedPlaceholder = placeholder ?? t("common.choose");
  const selected = useMemo(
    () => options.find((option) => option.value === value) ?? null,
    [options, value],
  );
  const toneClass = tone === "lapis" ? "filter-select--lapis" : "filter-select--gold";

  return (
    <Combobox.Root
      items={options}
      value={selected}
      onValueChange={(next) => {
        if (next) onChange(next.value);
      }}
      itemToStringLabel={(item) => item.label}
      isItemEqualToValue={(a, b) => a.value === b.value}
      filter={(item, query) => {
        const q = query.trim().toLowerCase();
        if (!q) return true;
        return [item.label, item.hint, item.value]
          .filter(Boolean)
          .some((field) => String(field).toLowerCase().includes(q));
      }}
    >
      <div className={cn("filter-select", toneClass)}>
        <label htmlFor={inputId} className="layer-heading mb-2 block">
          {label}
        </label>
        <Combobox.InputGroup className="filter-select__trigger relative">
          {selected?.icon ? (
            <span className="filter-select__icon absolute left-4 top-1/2 -translate-y-1/2" aria-hidden>
              {selected.icon}
            </span>
          ) : null}
          <Combobox.Input
            id={inputId}
            placeholder={resolvedPlaceholder}
            className={cn(
              "filter-select__label h-full w-full min-w-0 border-0 bg-transparent py-[0.82rem] pr-10 text-left outline-none placeholder:text-[var(--muted-2)]",
              selected?.icon ? "pl-10" : "pl-4",
            )}
          />
          <Combobox.Trigger
            className="filter-select__chevron absolute inset-y-0 right-0 flex items-center border-0 bg-transparent px-3"
            aria-label={t("common.openMenu", { label })}
          >
            ▾
          </Combobox.Trigger>
        </Combobox.InputGroup>

        <Combobox.Portal>
          <Combobox.Positioner className="outline-none" sideOffset={8}>
            <Combobox.Popup className="filter-select__menu relative z-50 w-[var(--anchor-width)] max-w-[var(--available-width)] outline-none">
              <Combobox.Empty>
                <div className="px-3 py-3 font-sans text-sm text-[var(--muted-2)]">{t("filter.noMatches")}</div>
              </Combobox.Empty>
              <Combobox.List className="max-h-[min(16.5rem,var(--available-height))] overflow-y-auto overscroll-contain outline-none">
                {(item: FilterSelectOption) => (
                  <Combobox.Item
                    key={item.value}
                    value={item}
                    className="filter-select__option data-highlighted:border-[rgb(240_201_121_/_0.14)] data-highlighted:bg-[rgb(240_201_121_/_0.07)] data-selected:border-[rgb(240_201_121_/_0.34)] data-selected:bg-[rgb(240_201_121_/_0.1)]"
                  >
                    <span className="filter-select__option-label">
                      {item.icon ? <span className="filter-select__option-icon">{item.icon}</span> : null}
                      <span className="filter-select__option-text">{item.label}</span>
                    </span>
                    {item.hint ? <span className="filter-select__option-hint">{item.hint}</span> : null}
                  </Combobox.Item>
                )}
              </Combobox.List>
            </Combobox.Popup>
          </Combobox.Positioner>
        </Combobox.Portal>
      </div>
    </Combobox.Root>
  );
}
