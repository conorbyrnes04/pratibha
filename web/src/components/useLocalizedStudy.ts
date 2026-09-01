"use client";

import { useEffect, useMemo, useState } from "react";
import { useLocale } from "@/components/LocaleProvider";
import type { LearningStepSpec, LearningTrack } from "@/lib/learningPaths";
import type { TraditionTrail } from "@/lib/learn/traditionTrails";
import {
  applyCachedStudyFields,
  applyVerseCardFields,
  applyVerseStudyFields,
  extractVerseCardFields,
  extractVerseStudyFields,
  localizeStudyFields,
  splitCoreStudyFields,
} from "@/lib/studyI18n";
import type { VerseItem } from "@/lib/types";

export function useLocalizedFields(fields: Record<string, string>): {
  fields: Record<string, string>;
  pending: boolean;
} {
  const { locale } = useLocale();
  const sourceKey = useMemo(
    () =>
      JSON.stringify(
        Object.keys(fields)
          .sort()
          .reduce<Record<string, string>>((acc, key) => {
            const value = (fields[key] || "").trim();
            if (value) acc[key] = value;
            return acc;
          }, {}),
      ),
    [fields],
  );
  const parsed = useMemo(() => JSON.parse(sourceKey) as Record<string, string>, [sourceKey]);
  const [resolved, setResolved] = useState<Record<string, string>>(parsed);
  const [resolvedKey, setResolvedKey] = useState("");
  const [pending, setPending] = useState(false);

  useEffect(() => {
    if (locale === "en") {
      setResolved(parsed);
      setResolvedKey(`${locale}:${sourceKey}`);
      setPending(false);
      return;
    }
    let cancelled = false;
    setPending(true);
    localizeStudyFields(locale, parsed)
      .then((next) => {
        if (!cancelled) {
          setResolved({ ...parsed, ...next });
          setResolvedKey(`${locale}:${sourceKey}`);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setResolved(applyCachedStudyFields(locale, parsed));
          setResolvedKey(`${locale}:${sourceKey}`);
        }
      })
      .finally(() => {
        if (!cancelled) setPending(false);
      });
    return () => {
      cancelled = true;
    };
  }, [locale, parsed, sourceKey]);

  const ready = locale === "en" || resolvedKey === `${locale}:${sourceKey}`;
  const next = locale === "en" ? parsed : ready ? resolved : applyCachedStudyFields(locale, parsed);
  return { fields: next, pending };
}

export function useLocalizedHeroQuotes(
  quotes: string[],
  index: number,
): { quote: string; pending: boolean } {
  const { locale } = useLocale();
  const allFields = useMemo(() => {
    const fields: Record<string, string> = {};
    quotes.forEach((line, i) => {
      if (line.trim()) fields[`quote:${i}`] = line;
    });
    return fields;
  }, [quotes]);
  const visibleFields = useMemo(() => {
    const line = (quotes[index] || "").trim();
    return line ? { [`quote:${index}`]: line } : {};
  }, [index, quotes]);
  const visible = useLocalizedFields(visibleFields);
  const all = useLocalizedFields(allFields);
  const source = quotes[index] || "";
  const visibleKey = `quote:${index}`;
  const quote = !visible.pending
    ? visible.fields[visibleKey] || source
    : !all.pending
      ? all.fields[visibleKey] || source
      : applyCachedStudyFields(locale, visibleFields)[visibleKey] || source;
  return { quote, pending: locale !== "en" && quote === source && (visible.pending || all.pending) };
}

export function useLocalizedVerse(item: VerseItem | null): VerseItem | null {
  const source = useMemo(() => (item ? extractVerseStudyFields(item) : {}), [item]);
  const { core, rest } = useMemo(() => splitCoreStudyFields(source), [source]);
  const { fields: coreFields } = useLocalizedFields(core);
  const { fields: restFields } = useLocalizedFields(rest);
  return useMemo(
    () => (item ? applyVerseStudyFields(item, { ...restFields, ...coreFields }) : null),
    [coreFields, item, restFields],
  );
}

export function useLocalizedVerseCards(items: VerseItem[], limit = 40): VerseItem[] {
  const source = useMemo(() => extractVerseCardFields(items, limit), [items, limit]);
  const { fields } = useLocalizedFields(source);
  return useMemo(
    () => items.map((item, idx) => (idx < limit ? applyVerseCardFields(item, fields) : item)),
    [fields, items, limit],
  );
}

export function useLocalizedStep(step: LearningStepSpec): LearningStepSpec {
  const source = useMemo(
    () => ({
      title: step.title,
      teaching: step.teaching,
      key_idea: step.keyIdea,
      misconception: step.misconception || "",
      practice: step.practice,
      journal: step.journalPrompt,
      integration: step.integration,
      orientation: step.orientation,
      chat_prompt: step.chatPrompt,
    }),
    [step],
  );
  const { fields } = useLocalizedFields(source);
  return useMemo(
    () => ({
      ...step,
      title: fields.title || step.title,
      teaching: fields.teaching || step.teaching,
      keyIdea: fields.key_idea || step.keyIdea,
      misconception: fields.misconception || step.misconception,
      practice: fields.practice || step.practice,
      journalPrompt: fields.journal || step.journalPrompt,
      integration: fields.integration || step.integration,
      orientation: fields.orientation || step.orientation,
      chatPrompt: fields.chat_prompt || step.chatPrompt,
    }),
    [fields, step],
  );
}

export function useLocalizedTrack(track: LearningTrack): LearningTrack {
  const source = useMemo(
    () => ({
      title: track.title,
      focus: track.focus,
      outcome: track.outcome,
      description: track.description,
      arc: track.arc,
    }),
    [track],
  );
  const { fields } = useLocalizedFields(source);
  return useMemo(
    () => ({
      ...track,
      title: fields.title || track.title,
      focus: fields.focus || track.focus,
      outcome: fields.outcome || track.outcome,
      description: fields.description || track.description,
      arc: fields.arc || track.arc,
    }),
    [fields, track],
  );
}

export function useLocalizedTrails(trails: TraditionTrail[]): TraditionTrail[] {
  const source = useMemo(() => {
    const fields: Record<string, string> = {};
    for (const trail of trails) {
      fields[`title:${trail.id}`] = trail.title;
      fields[`short_title:${trail.id}`] = trail.shortTitle;
      fields[`lede:${trail.id}`] = trail.lede;
    }
    return fields;
  }, [trails]);
  const { fields } = useLocalizedFields(source);
  return useMemo(
    () =>
      trails.map((trail) => ({
        ...trail,
        title: fields[`title:${trail.id}`] || trail.title,
        shortTitle: fields[`short_title:${trail.id}`] || trail.shortTitle,
        lede: fields[`lede:${trail.id}`] || trail.lede,
      })),
    [fields, trails],
  );
}
