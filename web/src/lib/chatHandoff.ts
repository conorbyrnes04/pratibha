const HANDOFF_KEY = "pratibha.chat.handoff.v1";

/** Stash a gate/journal prompt so `/chat` can open without a huge `?q=` URL. */
export function stashChatPrompt(verseId: string | undefined, prompt: string): void {
  if (typeof window === "undefined") return;
  const text = prompt.trim();
  if (!text) return;
  sessionStorage.setItem(
    HANDOFF_KEY,
    JSON.stringify({ verseId: verseId || "", prompt: text }),
  );
}

export function takeChatPrompt(verseId?: string | null): string {
  if (typeof window === "undefined") return "";
  try {
    const raw = sessionStorage.getItem(HANDOFF_KEY);
    if (!raw) return "";
    sessionStorage.removeItem(HANDOFF_KEY);
    const parsed = JSON.parse(raw) as { verseId?: string; prompt?: string };
    if (!parsed.prompt) return "";
    if (verseId && parsed.verseId && parsed.verseId !== verseId) return "";
    return parsed.prompt;
  } catch {
    return "";
  }
}

/** Turn `[1]` citation marks into in-page links, leaving markdown links alone. */
export function linkCitationMarks(markdown: string): string {
  return markdown.replace(/\[(\d{1,2})\](?!\()/g, "[$1](#chat-source-$1)");
}
