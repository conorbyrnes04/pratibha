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
          The circle is unavailable just now. The verse is still here.
        </p>
      );
    }
    return this.props.children;
  }
}
