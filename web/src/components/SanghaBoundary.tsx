"use client";

import { Component, type ReactNode } from "react";

export class SanghaBoundary extends Component<
  { children: ReactNode },
  { message: string | null }
> {
  state = { message: null as string | null };

  static getDerivedStateFromError(error: Error) {
    return { message: error.message };
  }

  render() {
    if (this.state.message) {
      return (
        <p className="soft mt-6 text-sm">
          The circle is unavailable just now.
        </p>
      );
    }
    return this.props.children;
  }
}

/** Swallow optional Circle chrome (sit/watch) so a missing table cannot take down readings. */
export class QuietBoundary extends Component<{ children: ReactNode }, { failed: boolean }> {
  state = { failed: false };

  static getDerivedStateFromError() {
    return { failed: true };
  }

  render() {
    return this.state.failed ? null : this.props.children;
  }
}
