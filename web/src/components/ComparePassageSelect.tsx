"use client";

import { useMemo, useState } from "react";
import type { VerseItem } from "@/lib/types";
import { displayPassageTitle } from "@/lib/passageTitles";
import { sortComparePassages } from "@/lib/corpusFilters";

type ComparePassageSelectProps = {
  label: string;
  collection: string;
  passages: VerseItem[];
  value: string;
  onChange: (verseId: string) => void;
  tone?: "gold" | "lapis";
};

export function ComparePassageSelect({
  label,
  collection,
  passages,
  value,
  onChange,
  tone = "gold",
}: ComparePassageSelectProps) {
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState("");

  const options = useMemo(() => sortComparePassages(passages, collection), [collection, passages]);

  const filtered = useMemo(() => {
    const needle = search.trim().toLowerCase();
    if (!needle) return options;
    return options.filter((item) => {
      const blob = [
        displayPassageTitle(item),
        item.reference,
        item.sutra_id,
        item.title,
        ...(item.themes || []),
      ]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();
      return blob.includes(needle);
    });
  }, [options, search]);

  const selected = options.find((item) => item._id === value);
  const toneClass = tone === "lapis" ? "filter-select--lapis" : "filter-select--gold";

  return (
    <div className={`filter-select ${toneClass}`}>
      <p className="layer-heading mb-2">{label}</p>
      <button
        type="button"
        aria-haspopup="listbox"
        aria-expanded={open}
        onClick={() => setOpen((prev) => !prev)}
        className="filter-select__trigger"
      >
        <span className="filter-select__value">
          <span className="filter-select__label">
            {selected ? displayPassageTitle(selected) : "Any passage in collection"}
          </span>
        </span>
        <span className="filter-select__chevron" aria-hidden>
          {open ? "▴" : "▾"}
        </span>
      </button>
      {open ? (
        <div className="filter-select__menu p-2">
          <input
            type="search"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder={`Search ${collection || "collection"}…`}
            className="input-field mb-2 w-full rounded-xl px-3 py-2 text-sm"
            autoFocus
          />
          <ul role="listbox" className="max-h-56 overflow-y-auto">
            <li role="presentation">
              <button
                type="button"
                role="option"
                aria-selected={!value}
                onClick={() => {
                  onChange("");
                  setOpen(false);
                  setSearch("");
                }}
                className={`filter-select__option w-full${!value ? " filter-select__option--active" : ""}`}
              >
                <span className="filter-select__option-text soft">Any passage (collection-wide retrieval)</span>
              </button>
            </li>
            {filtered.length === 0 ? (
              <li className="px-3 py-2 text-sm soft">No passages match.</li>
            ) : (
              filtered.map((item) => {
                const active = item._id === value;
                return (
                  <li key={item._id} role="presentation">
                    <button
                      type="button"
                      role="option"
                      aria-selected={active}
                      onClick={() => {
                        onChange(item._id);
                        setOpen(false);
                        setSearch("");
                      }}
                      className={`filter-select__option w-full${active ? " filter-select__option--active" : ""}`}
                    >
                      <span className="filter-select__option-text">{displayPassageTitle(item)}</span>
                    </button>
                  </li>
                );
              })
            )}
          </ul>
        </div>
      ) : null}
    </div>
  );
}
