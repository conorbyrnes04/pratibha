"use client";

import { useEffect, useId, useRef, useState } from "react";

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

export function FilterSelect({
  label,
  value,
  onChange,
  options,
  tone = "gold",
  placeholder = "Choose…",
}: FilterSelectProps) {
  const [open, setOpen] = useState(false);
  const rootRef = useRef<HTMLDivElement>(null);
  const listId = useId();
  const selected = options.find((option) => option.value === value);

  useEffect(() => {
    if (!open) return;
    function onPointerDown(event: MouseEvent) {
      if (!rootRef.current?.contains(event.target as Node)) setOpen(false);
    }
    function onKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") setOpen(false);
    }
    document.addEventListener("mousedown", onPointerDown);
    document.addEventListener("keydown", onKeyDown);
    return () => {
      document.removeEventListener("mousedown", onPointerDown);
      document.removeEventListener("keydown", onKeyDown);
    };
  }, [open]);

  const toneClass = tone === "lapis" ? "filter-select--lapis" : "filter-select--gold";

  return (
    <div ref={rootRef} className={`filter-select ${toneClass}`}>
      <p className="layer-heading mb-2">{label}</p>
      <button
        type="button"
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-controls={listId}
        onClick={() => setOpen((prev) => !prev)}
        className="filter-select__trigger"
      >
        <span className="filter-select__value">
          {selected?.icon ? <span className="filter-select__icon">{selected.icon}</span> : null}
          <span className="filter-select__label">{selected?.label || placeholder}</span>
        </span>
        <span className="filter-select__chevron" aria-hidden>
          {open ? "▴" : "▾"}
        </span>
      </button>
      {open ? (
        <ul id={listId} role="listbox" className="filter-select__menu">
          {options.map((option) => {
            const active = option.value === value;
            return (
              <li key={option.value} role="presentation">
                <button
                  type="button"
                  role="option"
                  aria-selected={active}
                  onClick={() => {
                    onChange(option.value);
                    setOpen(false);
                  }}
                  className={`filter-select__option${active ? " filter-select__option--active" : ""}`}
                >
                  <span className="filter-select__option-label">
                    {option.icon ? <span className="filter-select__option-icon">{option.icon}</span> : null}
                    <span className="filter-select__option-text">{option.label}</span>
                  </span>
                  {option.hint ? <span className="filter-select__option-hint">{option.hint}</span> : null}
                </button>
              </li>
            );
          })}
        </ul>
      ) : null}
    </div>
  );
}
