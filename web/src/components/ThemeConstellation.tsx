"use client";

import type { ThemeCount } from "@/lib/corpusFilters";

type ThemeConstellationProps = {
  themes: ThemeCount[];
  active: string;
  onChange: (theme: string) => void;
};

export function ThemeConstellation({ themes, active, onChange }: ThemeConstellationProps) {
  if (themes.length === 0) return null;

  return (
    <section className="theme-constellation">
      <p className="layer-heading">Theme constellation</p>
      <p className="soft mt-1 text-sm">Most frequent threads in the corpus — scroll to explore.</p>
      <div className="theme-constellation__frame mt-3">
        <div className="theme-constellation__track" role="tablist" aria-label="Filter by theme">
          <button
            type="button"
            role="tab"
            aria-selected={active === "all"}
            onClick={() => onChange("all")}
            className={`theme-constellation__bead${active === "all" ? " theme-constellation__bead--active" : ""}`}
          >
            All themes
          </button>
          {themes.map(({ theme, count }) => (
            <button
              key={theme}
              type="button"
              role="tab"
              aria-selected={active === theme}
              onClick={() => onChange(theme)}
              className={`theme-constellation__bead${active === theme ? " theme-constellation__bead--active" : ""}`}
            >
              <span>{theme}</span>
              <span className="theme-constellation__count">{count}</span>
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}
