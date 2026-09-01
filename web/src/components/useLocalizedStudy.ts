"use client";

import { useEffect, useMemo, useState } from "react";
import { useLocale } from "@/components/LocaleProvider";
import type { LearningStepSpec, LearningTrack } from "@/lib/learningPaths";
import type { TraditionTrail } from "@/lib/learn/traditionTrails";
import {
  applyVerseCardFields,
  applyVerseStudyFields,
  extractVerseCardFields,
  extractVerseStudyFields,
  localizeStudyFields,
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
  const [resolvedKey, setResolvedKey] = useState(`${locale}:${sourceKey}`);
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
          setResolved(parsed);
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

  const ready = resolvedKey === `${locale}:${sourceKey}`;
  return { fields: locale === "en" || !ready ? parsed : resolved, pending };
}

export function useLocalizedVerse(item: VerseItem | null): VerseItem | null {
  const source = useMemo(() => (item ? extractVerseStudyFields(item) : {}), [item]);
  const { fields } = useLocalizedFields(source);
  return useMemo(() => (item ? applyVerseStudyFields(item, fields) : null), [item, fields]);
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
