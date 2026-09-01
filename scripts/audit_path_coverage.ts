/**
 * Reports which canonical works are walked by learning paths, and which are not.
 * Run from web/: npm run audit:paths
 * Or: npx tsx scripts/audit_path_coverage.ts
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { LEARNING_REALMS, LEARNING_TRACKS, RECOMMENDED_SPINE } from "../web/src/lib/learningPaths.ts";
import { LEARNING_THREADS } from "../web/src/lib/learningThreads.ts";
import { TRADITION_TRAILS, TRADITIONS_COMING } from "../web/src/lib/learn/traditionTrails.ts";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const CANONICAL_DIR = path.join(ROOT, "data", "canonical");
const PIN_FREEZE_PATH = path.join(ROOT, "scripts", "path_pin_freeze.json");

type WorkStats = { dir: string; units: number; ids: Set<string> };

function workOf(unitId: string): string {
  const i = unitId.indexOf(".");
  return i === -1 ? unitId : unitId.slice(0, i);
}

function loadWorks(): Map<string, WorkStats> {
  const works = new Map<string, WorkStats>();
  if (!fs.existsSync(CANONICAL_DIR)) return works;

  for (const ent of fs.readdirSync(CANONICAL_DIR, { withFileTypes: true })) {
    if (!ent.isDirectory()) continue;
    const dir = path.join(CANONICAL_DIR, ent.name);
    const ids = new Set<string>();
    for (const file of fs.readdirSync(dir)) {
      if (!file.endsWith(".yml") && !file.endsWith(".yaml")) continue;
      const text = fs.readFileSync(path.join(dir, file), "utf8");
      const unitMatch = text.match(/^unit_id:\s*(.+)$/m);
      const idMatch = text.match(/^_id:\s*(.+)$/m);
      const id = (unitMatch?.[1] ?? idMatch?.[1] ?? "").trim();
      if (id) ids.add(id);
    }
    if (ids.size === 0) continue;
    const prefix = workOf([...ids][0]!);
    const prev = works.get(prefix);
    if (prev) {
      for (const id of ids) prev.ids.add(id);
      prev.units = prev.ids.size;
    } else {
      works.set(prefix, { dir: ent.name, units: ids.size, ids });
    }
  }
  return works;
}

function main(): void {
  const works = loadWorks();
  const primary = new Map<string, Set<string>>();
  const supporting = new Map<string, Set<string>>();
  const trackRows: string[] = [];

  for (const track of LEARNING_TRACKS) {
    const workCounts = new Map<string, number>();
    for (const step of track.steps) {
      const w = workOf(step.passageId);
      workCounts.set(w, (workCounts.get(w) ?? 0) + 1);
      if (!primary.has(w)) primary.set(w, new Set());
      primary.get(w)!.add(track.id);
      for (const sid of step.supportingPassageIds ?? []) {
        const sw = workOf(sid);
        if (!supporting.has(sw)) supporting.set(sw, new Set());
        supporting.get(sw)!.add(track.id);
      }
    }
    const mix = [...workCounts.entries()]
      .sort((a, b) => b[1] - a[1])
      .map(([w, n]) => `${w}×${n}`)
      .join(", ");
    const onSpine = RECOMMENDED_SPINE.includes(track.id) ? "spine" : "living";
    trackRows.push(
      `${track.id.padEnd(32)} ${track.level.padEnd(14)} ${String(track.steps.length).padStart(2)} steps  ${onSpine.padEnd(6)}  ${mix}`,
    );
  }

  const threadWorks = new Set<string>();
  for (const thread of LEARNING_THREADS) {
    for (const bead of thread.steps) threadWorks.add(workOf(bead.passageId));
  }

  const none: { work: string; units: number }[] = [];
  const supportOnly: { work: string; units: number; tracks: string }[] = [];
  const walked: { work: string; units: number; tracks: string }[] = [];

  for (const [work, stats] of [...works.entries()].sort((a, b) => b[1].units - a[1].units)) {
    const prim = primary.get(work);
    const supp = supporting.get(work);
    if (prim) {
      walked.push({ work, units: stats.units, tracks: [...prim].join(", ") });
    } else if (supp) {
      supportOnly.push({ work, units: stats.units, tracks: [...supp].join(", ") });
    } else {
      none.push({ work, units: stats.units });
    }
  }

  const realmIds = new Set(LEARNING_REALMS.flatMap((r) => r.trackIds));
  const trailIds = new Set(TRADITION_TRAILS.flatMap((t) => t.trackIds));
  const orphans = LEARNING_TRACKS.filter((t) => !trailIds.has(t.id)).map((t) => t.id);
  const realmOrphans = LEARNING_TRACKS.filter((t) => !realmIds.has(t.id)).map((t) => t.id);
  const spineOrphans = LEARNING_TRACKS.filter((t) => !RECOMMENDED_SPINE.includes(t.id)).map((t) => t.id);

  console.log("=== Tracks ===");
  for (const row of trackRows) console.log(row);
  console.log(`\n${LEARNING_TRACKS.length} tracks, ${LEARNING_TRACKS.reduce((n, t) => n + t.steps.length, 0)} gates`);

  console.log("\n=== Trails ===");
  for (const trail of TRADITION_TRAILS) {
    console.log(`${trail.id.padEnd(22)} tracks=${trail.trackIds.length}  ${trail.trackIds.join(", ") || "(empty)"}`);
  }
  for (const trail of TRADITIONS_COMING) {
    console.log(`${trail.id.padEnd(22)} COMING  tracks=${trail.trackIds.length}`);
  }

  console.log("\n=== Pin freeze (existing gates) ===");
  const freezePath = PIN_FREEZE_PATH;
  if (fs.existsSync(freezePath)) {
    const freeze = JSON.parse(fs.readFileSync(freezePath, "utf8")) as { pins?: Record<string, string> };
    const pins = freeze.pins ?? {};
    let broken = 0;
    for (const [key, expected] of Object.entries(pins)) {
      const [trackId, stepId] = key.split(":");
      const track = LEARNING_TRACKS.find((t) => t.id === trackId);
      const step = track?.steps.find((s) => s.id === stepId);
      if (!step) {
        console.log(`BROKEN  missing ${key}`);
        broken += 1;
      } else if (step.passageId !== expected) {
        console.log(`BROKEN  ${key}: ${step.passageId} ≠ ${expected}`);
        broken += 1;
      }
    }
    console.log(broken ? `${broken} freeze break(s).` : `OK — ${Object.keys(pins).length} frozen pins unchanged.`);
  } else {
    console.log("No scripts/path_pin_freeze.json");
  }

  console.log("\n=== Realms ===");
  for (const realm of LEARNING_REALMS) {
    console.log(`${realm.id.padEnd(22)} ${realm.trackIds.join(", ")}`);
  }

  console.log("\n=== Wiring orphans ===");
  console.log(`Not on any tradition trail: ${orphans.join(", ") || "none"}`);
  console.log(`Not in any realm:          ${realmOrphans.join(", ") || "none"}`);
  console.log(`Not on recommended spine:  ${spineOrphans.join(", ") || "none"} (ok for living trails)`);

  console.log("\n=== Works with a primary path gate ===");
  for (const row of walked) {
    const thread = threadWorks.has(row.work) ? "  [thread]" : "";
    console.log(`${String(row.units).padStart(4)}  ${row.work.padEnd(42)} ${row.tracks}${thread}`);
  }

  console.log("\n=== Works cited only as supporting ===");
  if (supportOnly.length === 0) console.log("(none)");
  for (const row of supportOnly) {
    console.log(`${String(row.units).padStart(4)}  ${row.work.padEnd(42)} via ${row.tracks}`);
  }

  console.log("\n=== Works with zero path citations ===");
  for (const row of none) {
    console.log(`${String(row.units).padStart(4)}  ${row.work}`);
  }

  const corpusUnits = [...works.values()].reduce((n, w) => n + w.units, 0);
  const citedWorks = walked.length + supportOnly.length;
  console.log(
    `\nCorpus: ${works.size} works, ${corpusUnits} units. Walked: ${walked.length} works. Supporting-only: ${supportOnly.length}. Uncited: ${none.length}. Trails coming: ${TRADITIONS_COMING.length}.`,
  );
  void citedWorks;
}

main();
