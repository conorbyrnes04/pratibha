// Extract LEARNING_TRACKS from web/src/lib/learningPaths.ts into paths.json,
// keeping only tracks whose primary passage anchors all exist in corpus.json.
//
// Run from repo root:  node ios/scripts/build_paths_json.mjs
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const tsPath = join(repoRoot, "web", "src", "lib", "learningPaths.ts");
const corpusPath = join(repoRoot, "ios", "Pratibha", "Resources", "corpus.json");
const outPath = join(repoRoot, "ios", "Pratibha", "Resources", "paths.json");

const src = readFileSync(tsPath, "utf8");

// Isolate the array literal assigned to LEARNING_TRACKS via bracket matching.
const marker = "export const LEARNING_TRACKS";
const mi = src.indexOf(marker);
if (mi === -1) throw new Error("LEARNING_TRACKS not found");
const eq = src.indexOf("=", mi);
const startBracket = src.indexOf("[", eq);
let depth = 0, end = -1, inStr = null;
for (let i = startBracket; i < src.length; i++) {
  const c = src[i], prev = src[i - 1];
  if (inStr) {
    if (c === inStr && prev !== "\\") inStr = null;
    continue;
  }
  if (c === '"' || c === "'" || c === "`") { inStr = c; continue; }
  if (c === "[") depth++;
  else if (c === "]") { depth--; if (depth === 0) { end = i; break; } }
}
if (end === -1) throw new Error("Could not bracket-match LEARNING_TRACKS array");

const literal = src.slice(startBracket, end + 1);
// The literal is plain data (object/array literals, string values) — eval as JS.
const tracks = eval("(" + literal + ")");

const corpus = JSON.parse(readFileSync(corpusPath, "utf8"));
const known = new Set(corpus.passages.map((p) => p.id));

const kept = [];
const dropped = [];
for (const t of tracks) {
  const missing = t.steps.filter((s) => !known.has(s.passageId));
  if (missing.length > 0) {
    dropped.push({ id: t.id, missing: missing.map((s) => s.passageId) });
    continue;
  }
  kept.push({
    id: t.id,
    title: t.title,
    level: t.level,
    focus: t.focus,
    outcome: t.outcome,
    description: t.description,
    arc: t.arc,
    estimatedSessions: t.estimatedSessions,
    steps: t.steps.map((s) => ({
      id: s.id,
      title: s.title,
      orientation: s.orientation,
      teaching: s.teaching,
      keyIdea: s.keyIdea,
      misconception: s.misconception ?? "",
      passageId: s.passageId,
      supportingPassageIds: (s.supportingPassageIds ?? []).filter((id) => known.has(id)),
      theme: s.theme ?? "",
      chatMode: s.chatMode ?? "question",
      chatPrompt: s.chatPrompt,
      practice: s.practice,
      journalPrompt: s.journalPrompt,
      integration: s.integration,
    })),
  });
}

const out = { version: 1, pathCount: kept.length, paths: kept };
writeFileSync(outPath, JSON.stringify(out));
console.log(`Wrote ${kept.length} paths -> ${outPath}`);
for (const t of kept) console.log(`  keep  ${t.steps.length} gates  ${t.title}`);
for (const d of dropped) console.log(`  drop  ${d.id}  (missing anchors: ${d.missing.slice(0, 3).join(", ")}${d.missing.length > 3 ? "…" : ""})`);
