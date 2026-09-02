"use client";

import { Component, useCallback, useState, type ReactNode } from "react";
import { useT } from "@/components/LocaleProvider";

class SanghaCatch extends Component<
  { children: ReactNode; fallback: ReactNode },
  { failed: boolean }
> {
  state = { failed: false };

  static getDerivedStateFromError() {
    return { failed: true };
  }

  render() {
    return this.state.failed ? this.props.fallback : this.props.children;
  }
}

export function SanghaBoundary({
  children,
  silent = false,
}: {
  children: ReactNode;
  silent?: boolean;
}) {
  const t = useT();
  const [generation, setGeneration] = useState(0);
  const retry = useCallback(() => setGeneration((n) => n + 1), []);

  const fallback = silent ? null : (
    <div className="mt-6">
      <p className="soft text-sm">{t("circle.unavailable")}</p>
      <button
        type="button"
        className="mt-2 font-sans text-xs uppercase tracking-[0.16em] text-amber-200 hover:text-amber-100"
        onClick={retry}
      >
        {t("common.tryAgain")}
      </button>
    </div>
  );

  return (
    <SanghaCatch key={generation} fallback={fallback}>
      {children}
    </SanghaCatch>
  );
}

/** Swallow optional Circle chrome (sit/watch) so a missing table cannot take down readings. */
export function QuietBoundary({ children }: { children: ReactNode }) {
  return <SanghaBoundary silent>{children}</SanghaBoundary>;
}
