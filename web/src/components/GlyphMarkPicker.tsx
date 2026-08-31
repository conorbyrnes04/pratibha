"use client";

import { toast } from "sonner";
import { InkGlyph } from "@/components/InkGlyph";
import { UNLOCK_HINT } from "@/lib/glyphUnlock";
import { SHARE_INKS, SHARE_MARK_GROUPS, type ShareForceMark, type ShareInk } from "@/lib/shareCard";

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
  const hex = SHARE_INKS[ink].hex;

  return (
    <div className="space-y-6">
      <fieldset>
        <legend className="passage-layer__label mb-3">Ink</legend>
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
              {SHARE_INKS[key].label}
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
        Initials
      </button>
      {SHARE_MARK_GROUPS.map((group) => {
        const opened = group.marks.filter((slug) => openMarks.has(slug)).length;
        return (
          <fieldset key={group.id}>
            <legend className="passage-layer__label mb-3">
              {group.label}{" "}
              <span className="share-unlock-count">
                {opened} of {group.marks.length} open
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
                        toast.message("Keep studying.", { description: UNLOCK_HINT });
                        return;
                      }
                      onChoose(slug);
                    }}
                    aria-pressed={selected === slug}
                    aria-label={available ? `Use ${slug} as your mark` : `${slug}, sealed`}
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
