"use client";

import { toast } from "sonner";
import { InkGlyph } from "@/components/InkGlyph";
import { SHARE_INKS, SHARE_MARK_GROUPS, type ShareForceMark, type ShareInk } from "@/lib/shareCard";
import { shareGroupKey, shareInkKey } from "@/i18n";
import { useT } from "@/components/LocaleProvider";

export function GlyphMarkPicker({
  selected,
  ink,
  openMarks,
  onChoose,
  onInk,
}: {
  selected: ShareForceMark | null;
  ink: ShareInk;
  openMarks: Set<ShareForceMark>;
  onChoose: (mark: ShareForceMark | null) => void;
  onInk: (ink: ShareInk) => void;
}) {
  const t = useT();
  const hex = SHARE_INKS[ink].hex;

  return (
    <div className="space-y-6">
      <fieldset>
        <legend className="passage-layer__label mb-3">{t("share.ink")}</legend>
        <div className="flex flex-wrap gap-2">
          {(Object.keys(SHARE_INKS) as ShareInk[]).map((key) => (
            <button
              key={key}
              type="button"
              className={`share-chip ${ink === key ? "share-chip--on" : ""}`}
              onClick={() => onInk(key)}
              aria-pressed={ink === key}
            >
              <span className="share-chip__swatch" style={{ background: SHARE_INKS[key].hex }} />
              {t(shareInkKey(key))}
            </button>
          ))}
        </div>
      </fieldset>
      <button
        type="button"
        className={`share-chip ${selected === null ? "share-chip--on" : ""}`}
        onClick={() => onChoose(null)}
        aria-pressed={selected === null}
      >
        {t("common.initials")}
      </button>
      {SHARE_MARK_GROUPS.map((group) => {
        const opened = group.marks.filter((slug) => openMarks.has(slug)).length;
        return (
          <fieldset key={group.id}>
            <legend className="passage-layer__label mb-3">
              {t(shareGroupKey(group.id))}{" "}
              <span className="share-unlock-count">
                {t("share.ofOpen", { opened, total: group.marks.length })}
              </span>
            </legend>
            <div className="flex flex-wrap gap-2">
              {group.marks.map((slug) => {
                const available = openMarks.has(slug);
                return (
                  <button
                    key={slug}
                    type="button"
                    className={`share-chip ${selected === slug ? "share-chip--on" : ""} ${available ? "" : "share-chip--locked"}`}
                    onClick={() => {
                      if (!available) {
                        toast.message(t("share.keepStudying"), { description: t("glyph.unlockHint") });
                        return;
                      }
                      onChoose(slug);
                    }}
                    aria-pressed={selected === slug}
                    aria-label={available ? t("glyph.useMark", { slug }) : t("share.sealed", { slug })}
                  >
                    <InkGlyph glyph={slug} ink={hex} className="share-chip__glyph" />
                    <span>{slug}</span>
                  </button>
                );
              })}
            </div>
          </fieldset>
        );
      })}
    </div>
  );
}
