import { checkBlocklist } from "./moderation";

const MIN_PRIVATE = 10;
const MIN_OFFERED = 40;
const MAX_COMMENTARY = 4000;
const MAX_MARGIN = 280;
const MIN_REPLY = 10;
const MAX_REPLY = 800;
const MIN_NAME = 2;
const MAX_NAME = 40;

export function assertClean(text: string, label: string): string {
  const trimmed = text.trim();
  const check = checkBlocklist(trimmed);
  if (!check.passed) {
    throw new Error(
      `${label} does not meet our guidelines for respectful discourse.`,
    );
  }
  return trimmed;
}

export function assertCommentary(body: string, offered: boolean): string {
  const trimmed = assertClean(body, "This reading");
  if (trimmed.length < (offered ? MIN_OFFERED : MIN_PRIVATE)) {
    throw new Error(
      offered
        ? "Offer a complete reading (at least 40 characters) — say what the line does."
        : "Please write a little more (at least 10 characters).",
    );
  }
  if (trimmed.length > MAX_COMMENTARY) {
    throw new Error("Please keep the reading under 4000 characters.");
  }
  return trimmed;
}

export function assertReply(body: string): string {
  const trimmed = assertClean(body, "This reply");
  if (trimmed.length < MIN_REPLY) {
    throw new Error("Please share a more complete thought (at least 10 characters).");
  }
  if (trimmed.length > MAX_REPLY) {
    throw new Error("Please keep replies under 800 characters.");
  }
  return trimmed;
}

export function assertMargin(note: string): string {
  const trimmed = assertClean(note, "This note");
  if (trimmed.length > MAX_MARGIN) {
    throw new Error("Please keep the margin under 280 characters.");
  }
  return trimmed;
}

export function assertDisplayName(raw: string): string {
  const trimmed = raw.trim().replace(/\s+/g, " ");
  if (trimmed.length < MIN_NAME || trimmed.length > MAX_NAME) {
    throw new Error("Choose a name between 2 and 40 characters.");
  }
  if (trimmed.includes("@") || /https?:\/\//i.test(trimmed)) {
    throw new Error("Use a name, not an email or a link.");
  }
  assertClean(trimmed, "This name");
  return trimmed;
}

export function slugify(name: string): string {
  const base = name
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 28);
  return base || "manuscript";
}
