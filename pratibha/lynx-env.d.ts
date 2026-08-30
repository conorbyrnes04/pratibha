/// <reference types="@lynx-js/rspeedy/client" />

declare module "*.json" {
  const value: unknown;
  export default value;
}

// NEXT_PUBLIC_* values are inlined at build time via `define` in lynx.config.ts,
// so `process` is never a real runtime object here — this just types the reads.
declare const process: {
  env: Record<string, string | undefined>;
};
