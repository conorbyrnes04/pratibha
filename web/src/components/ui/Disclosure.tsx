import type { ReactNode } from "react";

type DisclosureProps = {
  /** Summary text shown on the always-visible row. */
  summary: ReactNode;
  /** Optional secondary text shown next to the summary. */
  hint?: ReactNode;
  /** Whether the panel starts open. */
  defaultOpen?: boolean;
  className?: string;
  children: ReactNode;
};

function Chevron() {
  return (
    <svg
      className="disclosure__chevron"
      width="16"
      height="16"
      viewBox="0 0 16 16"
      fill="none"
      aria-hidden
    >
      <path
        d="M6 4l4 4-4 4"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

/**
 * Disclosure — styled progressive-disclosure block built on native
 * <details>/<summary>. Use to hide dense secondary content (extra
 * layers, appendices, advanced options) behind a single tap so the
 * default view stays calm.
 */
export function Disclosure({ summary, hint, defaultOpen, className, children }: DisclosureProps) {
  return (
    <details className={`disclosure ${className ?? ""}`.trim()} open={defaultOpen}>
      <summary>
        <span className="flex items-center gap-2">
          <Chevron />
          <span>{summary}</span>
        </span>
        {hint ? (
          <span className="font-sans text-xs uppercase tracking-[0.14em] text-stone-400">{hint}</span>
        ) : null}
      </summary>
      <div className="disclosure__panel">{children}</div>
    </details>
  );
}
