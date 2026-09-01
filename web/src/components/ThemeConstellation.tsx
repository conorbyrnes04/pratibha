"use client";

import type { ThemeCount } from "@/lib/corpusFilters";
import { useT } from "@/components/LocaleProvider";

type ThemeConstellationProps = {
  themes: ThemeCount[];
  active: string;
  onChange: (theme: string) => void;
};

export function ThemeConstellation({ themes, active, onChange }: ThemeConstellationProps) {
  const t = useT();
  if (themes.length === 0) return null;

  return (
    <section className="theme-constellation">
      <p className="layer-heading">{t("theme.title")}</p>
      <p className="soft mt-1 text-sm">{t("theme.lede")}</p>
      <div className="theme-constellation__frame mt-3">
        <div className="theme-constellation__track" role="tablist" aria-label={t("theme.filter")}>
          <button
            type="button"
            role="tab"
            aria-selected={active === "all"}
            onClick={() => onChange("all")}
            className={`theme-constellation__bead${active === "all" ? " theme-constellation__bead--active" : ""}`}
          >
            {t("theme.all")}
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
