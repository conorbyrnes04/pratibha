"use client";

import { CircleOfferForm } from "@/components/CircleOfferForm";
import { CircleReadings } from "@/components/CircleReadings";
import { SanghaBoundary } from "@/components/SanghaBoundary";
import { CONVEX_ENABLED } from "@/lib/convexConfigured";
import { useT } from "@/components/LocaleProvider";

export function GateCircleSection({
  verseId,
  verseTitle,
  idea,
  defaultOpen = false,
  onDismiss,
}: {
  verseId: string;
  verseTitle: string;
  idea?: string;
  defaultOpen?: boolean;
  onDismiss?: () => void;
}) {
  const t = useT();
  if (!verseId || !CONVEX_ENABLED) return null;

  return (
    <SanghaBoundary>
      <details className="learn-gate-circle" open={defaultOpen || undefined}>
        <summary className="learn-gate-circle__summary">
          <span>{t("circle.title")}</span>
          <span className="learn-gate-circle__hint">{verseTitle}</span>
        </summary>
        <div className="learn-gate-circle__body">
          {idea ? <p className="learn-gate-circle__idea">{idea}</p> : null}
          <p className="soft text-sm leading-relaxed">{t("circle.ledeVerse")}</p>
          <CircleReadings verseId={verseId} embedded />
          <CircleOfferForm
            verseId={verseId}
            verseTitle={verseTitle}
            compact
            loginNext="/learn"
          />
          {onDismiss ? (
            <button type="button" className="learn-gate-circle__dismiss" onClick={onDismiss}>
              {t("circle.gateSkip")}
            </button>
          ) : null}
        </div>
      </details>
    </SanghaBoundary>
  );
}
