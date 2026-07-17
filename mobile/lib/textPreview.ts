export function stripMarkdown(input: string): string {
  let s = (input || "").replace(/\r\n/g, "\n");
  s = s.replace(/```[\s\S]*?```/g, " ");
  s = s.replace(/`([^`]+)`/g, "$1");
  s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, "$1");
  s = s.replace(/(\*\*|__)(.*?)\1/g, "$2");
  s = s.replace(/(\*|_)(.*?)\1/g, "$2");
  s = s.replace(/^\s{0,3}(#{1,6}|\*|-|\+)\s+/gm, "");
  s = s.replace(/\s+/g, " ").trim();
  return s;
}

export function firstSentence(input: string): string {
  const clean = stripMarkdown(input);
  if (!clean) return "";
  const m = clean.match(/^(.+?[.!?])(?:\s|$)/);
  return m?.[1] || clean;
}
