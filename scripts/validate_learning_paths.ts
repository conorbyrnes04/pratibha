/**
 * Validates learning paths, threads, realms, and spine against the canonical corpus.
 * Run: npx tsx scripts/validate_learning_paths.ts
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { LEARNING_REALMS, LEARNING_TRACKS, RECOMMENDED_SPINE } from "../web/src/lib/learningPaths.ts";
import { LEARNING_THREADS } from "../web/src/lib/learningThreads.ts";
import { TRADITION_TRAILS } from "../web/src/lib/learn/traditionTrails.ts";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const CANONICAL_DIR = path.join(ROOT, "data", "canonical");
const PIN_FREEZE_PATH = path.join(ROOT, "scripts", "path_pin_freeze.json");

function loadCorpusUnitIds(): Set<string> {
  const ids = new Set<string>();
  function walk(dir: string) {
    for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, ent.name);
      if (ent.isDirectory()) walk(full);
      else if (ent.name.endsWith(".yml") || ent.name.endsWith(".yaml")) {
        const text = fs.readFileSync(full, "utf8");
        const unitMatch = text.match(/^unit_id:\s*(.+)$/m);
        const idMatch = text.match(/^_id:\s*(.+)$/m);
        if (unitMatch) ids.add(unitMatch[1].trim());
        else if (idMatch) ids.add(idMatch[1].trim());
      }
    }
  }
  if (fs.existsSync(CANONICAL_DIR)) walk(CANONICAL_DIR);
  return ids;
}

type Issue = { level: "error" | "warn"; message: string };

function main(): number {
  const corpus = loadCorpusUnitIds();
  const issues: Issue[] = [];
  const trackIds = new Set<string>();
  const stepByKey = new Map<string, { passageId: string; title: string }>();
  for (const track of LEARNING_TRACKS) {
    if (trackIds.has(track.id)) {
      issues.push({ level: "error", message: `Duplicate track id: ${track.id}` });
    }
    trackIds.add(track.id);
    for (const step of track.steps) {
      stepByKey.set(`${track.id}:${step.id}`, { passageId: step.passageId, title: step.title });
      const refs = [step.passageId, ...(step.supportingPassageIds || [])];
      for (const ref of refs) {
        if (!corpus.has(ref)) {
          issues.push({ level: "error", message: `Missing corpus unit: ${ref} (${track.id} / ${step.id})` });
        }
        if (ref.includes("plotinus") && corpus.has(ref)) {
          // warn only — plotinus units may be structural_draft while paths still pin them
        }
      }
    }
  }

  if (fs.existsSync(PIN_FREEZE_PATH)) {
    const freeze = JSON.parse(fs.readFileSync(PIN_FREEZE_PATH, "utf8")) as { pins?: Record<string, string> };
    for (const [key, expected] of Object.entries(freeze.pins ?? {})) {
      const step = stepByKey.get(key);
      if (!step) {
        issues.push({
          level: "error",
          message: `Pin freeze: missing gate ${key} (TTS-locked; do not delete or rename)`,
        });
        continue;
      }
      if (step.passageId !== expected) {
        issues.push({
          level: "error",
          message: `Pin freeze: ${key} passageId ${step.passageId} ≠ frozen ${expected}`,
        });
      }
    }
  }

  for (const tid of RECOMMENDED_SPINE) {
    if (!trackIds.has(tid)) {
      issues.push({ level: "error", message: `RECOMMENDED_SPINE references unknown track: ${tid}` });
    }
  }
  for (const tid of trackIds) {
    if (!RECOMMENDED_SPINE.includes(tid)) {
      issues.push({ level: "warn", message: `Track not on RECOMMENDED_SPINE: ${tid}` });
    }
  }

  for (const trail of TRADITION_TRAILS) {
    for (const tid of trail.trackIds) {
      if (!trackIds.has(tid)) {
        issues.push({ level: "error", message: `Trail "${trail.id}" references unknown track: ${tid}` });
      }
    }
  }

  const realmTrackIds = new Set<string>();
  for (const realm of LEARNING_REALMS) {
    for (const tid of realm.trackIds) {
      realmTrackIds.add(tid);
      if (!trackIds.has(tid)) {
        issues.push({ level: "error", message: `Realm "${realm.id}" references unknown track: ${tid}` });
      }
    }
  }
  for (const tid of trackIds) {
    if (!realmTrackIds.has(tid)) {
      issues.push({ level: "warn", message: `Track not in any LEARNING_REALM: ${tid}` });
    }
  }

  if (LEARNING_THREADS.length > 8) {
    issues.push({
      level: "warn",
      message: `Expected at most 8 threads in this pass; found ${LEARNING_THREADS.length}`,
    });
  }

  const threadIds = new Set<string>();
  for (const thread of LEARNING_THREADS) {
    if (threadIds.has(thread.id)) {
      issues.push({ level: "error", message: `Duplicate thread id: ${thread.id}` });
    }
    threadIds.add(thread.id);

    if (!thread.thesis?.trim()) {
      issues.push({ level: "error", message: `Thread "${thread.id}" is missing thesis` });
    }
    if (!thread.arc?.trim()) {
      issues.push({ level: "error", message: `Thread "${thread.id}" is missing arc` });
    }
    if (!thread.practice?.trim()) {
      issues.push({ level: "error", message: `Thread "${thread.id}" is missing practice` });
    }
    if (!thread.integration?.trim()) {
      issues.push({ level: "error", message: `Thread "${thread.id}" is missing integration` });
    }
    if (thread.steps.length < 6) {
      issues.push({
        level: "warn",
        message: `Thread "${thread.id}" has ${thread.steps.length} beads (plan asked 6–8)`,
      });
    }

    const beadIds = new Set<string>();
    for (const bead of thread.steps) {
      if (beadIds.has(bead.id)) {
        issues.push({ level: "error", message: `Thread "${thread.id}" has duplicate bead id "${bead.id}"` });
      }
      beadIds.add(bead.id);

      if (!bead.move?.trim()) {
        issues.push({ level: "error", message: `Thread "${thread.id}" bead "${bead.id}" is missing move` });
      }
      if (!bead.homology?.trim()) {
        issues.push({ level: "error", message: `Thread "${thread.id}" bead "${bead.id}" is missing homology` });
      }
      if (!bead.divergence?.trim()) {
        issues.push({ level: "error", message: `Thread "${thread.id}" bead "${bead.id}" is missing divergence` });
      }

      const key = `${bead.trackId}:${bead.stepId}`;
      const step = stepByKey.get(key);
      if (!step) {
        issues.push({
          level: "error",
          message: `Thread "${thread.id}" bead "${bead.id}" references missing step ${key}`,
        });
        continue;
      }
      if (step.passageId !== bead.passageId) {
        issues.push({
          level: "error",
          message: `Thread "${thread.id}" bead "${bead.id}" passageId ${bead.passageId} ≠ path step ${step.passageId}`,
        });
      }
    }
  }

  const errors = issues.filter((i) => i.level === "error");
  const warns = issues.filter((i) => i.level === "warn");

  console.log(`Corpus units indexed: ${corpus.size}`);
  console.log(`Paths: ${LEARNING_TRACKS.length}, steps: ${stepByKey.size}, threads: ${LEARNING_THREADS.length}`);

  for (const w of warns) console.warn(`WARN: ${w.message}`);
  for (const e of errors) console.error(`ERROR: ${e.message}`);

  if (errors.length === 0) {
    console.log(warns.length ? `OK with ${warns.length} warning(s).` : "OK — all learning path references valid.");
    return 0;
  }
  console.error(`Failed with ${errors.length} error(s).`);
  return 1;
}

process.exit(main());
