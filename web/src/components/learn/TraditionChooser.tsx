"use client";

import { SpandaMedallion } from "@/components/InkGlyph";
import { LEARNING_TRACKS } from "@/lib/learningPaths";
import { stepKey, type ProgressMap } from "@/lib/learn/progress";
import {
  TRADITION_TRAILS,
  TRADITIONS_COMING,
  type TraditionTrail,
} from "@/lib/learn/traditionTrails";
import { useT } from "@/components/LocaleProvider";
import { useLocalizedTrails } from "@/components/useLocalizedStudy";

type TraditionChooserProps = {
  progress: ProgressMap;
  hydrated: boolean;
  onSelectTradition: (traditionId: string) => void;
};

function trailStats(trail: TraditionTrail, progress: ProgressMap) {
  let completed = 0;
  let total = 0;
  for (const trackId of trail.trackIds) {
    const track = LEARNING_TRACKS.find((item) => item.id === trackId);
    if (!track) continue;
    for (const step of track.steps) {
      total += 1;
      if (progress[stepKey(trackId, step.id)]) completed += 1;
    }
  }
  return { completed, total };
}

function TraditionCard({
  trail,
  progress,
  hydrated,
  disabled,
  onSelect,
}: {
  trail: TraditionTrail;
  progress: ProgressMap;
  hydrated: boolean;
  disabled?: boolean;
  onSelect: (id: string) => void;
}) {
  const t = useT();
  const { completed, total } = trailStats(trail, progress);
  const done = total > 0 && completed === total;
  const started = completed > 0;
  return (
    <li>
      <button
        type="button"
        disabled={disabled}
        onClick={() => onSelect(trail.id)}
        className="w-full text-center disabled:cursor-default"
      >
        <article className="flex h-full flex-col gap-4 rounded-2xl border border-amber-200/15 bg-[#0b0b14]/70 p-5 text-center">
          <div className="flex justify-center">
            <SpandaMedallion
              glyph={trail.glyph}
              state={done ? "recognized" : started ? "arising" : "unmanifest"}
              size="lg"
            />
          </div>
          <div className="flex-1">
            <h2 className="text-lg leading-snug text-amber-50">{trail.title}</h2>
            <p className="mt-2 text-sm leading-relaxed text-stone-400">{trail.lede}</p>
          </div>
          {disabled ? (
            <p className="font-sans text-[10px] uppercase tracking-[0.16em] text-stone-500">{t("common.soon")}</p>
          ) : hydrated ? (
            <p className="font-sans text-[10px] uppercase tracking-[0.16em] text-amber-200/55">
              {done
                ? t("learn.gatesComplete", { total })
                : started
                  ? t("learn.gatesProgress", { completed, total })
                  : total === 1
                    ? t("learn.gatesStartOne", { total })
                    : t("learn.gatesStartMany", { total })}
            </p>
          ) : (
            <p className="font-sans text-[10px] uppercase tracking-[0.16em] text-stone-600">…</p>
          )}
        </article>
      </button>
    </li>
  );
}

export function TraditionChooser({ progress, hydrated, onSelectTradition }: TraditionChooserProps) {
  const t = useT();
  const trails = useLocalizedTrails(TRADITION_TRAILS);
  const coming = useLocalizedTrails(TRADITIONS_COMING);
  return (
    <div className="section-stack">
      <header className="library-header">
        <div className="library-header__body">
          <p className="passage-reading__meta">{t("learn.guided")}</p>
          <h1 className="library-header__title">{t("learn.paths")}</h1>
          <p className="library-header__lede">{t("learn.pathsLede")}</p>
        </div>
      </header>
      <section className="mt-8 pb-8">
        <ul className="mx-auto grid max-w-4xl list-none gap-5 sm:grid-cols-2">
          {trails.map((trail) => (
            <TraditionCard
              key={trail.id}
              trail={trail}
              progress={progress}
              hydrated={hydrated}
              onSelect={onSelectTradition}
            />
          ))}
        </ul>
      </section>
      {coming.length > 0 ? (
        <section className="pb-16">
          <p className="mx-auto mb-4 max-w-4xl font-sans text-[10px] uppercase tracking-[0.18em] text-stone-500">
            {t("learn.coming")}
          </p>
          <ul className="mx-auto grid max-w-4xl list-none gap-5 sm:grid-cols-2">
            {coming.map((trail) => (
              <TraditionCard
                key={trail.id}
                trail={trail}
                progress={progress}
                hydrated={hydrated}
                disabled
                onSelect={() => {}}
              />
            ))}
          </ul>
        </section>
      ) : null}
    </div>
  );
}
