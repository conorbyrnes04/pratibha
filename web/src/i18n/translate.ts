import type { Messages } from "./messages/en";

export type TranslateVars = Record<string, string | number>;

function lookup(messages: Messages, path: string): string | undefined {
  const parts = path.split(".");
  let current: unknown = messages;
  for (const part of parts) {
    if (current == null || typeof current !== "object") return undefined;
    current = (current as Record<string, unknown>)[part];
  }
  return typeof current === "string" ? current : undefined;
}

export function interpolate(template: string, vars?: TranslateVars): string {
  if (!vars) return template;
  return template.replace(/\{(\w+)\}/g, (_, key: string) =>
    vars[key] === undefined ? `{${key}}` : String(vars[key]),
  );
}

export function translate(
  messages: Messages,
  fallback: Messages,
  key: string,
  vars?: TranslateVars,
): string {
  const raw = lookup(messages, key) ?? lookup(fallback, key) ?? key;
  return interpolate(raw, vars);
}
