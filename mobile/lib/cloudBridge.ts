import type { JournalNote } from "@shared/types";
import type { CompletedAtMap, ProgressMap } from "@/lib/storage";

export type CloudBridge = {
  signedIn: boolean;
  pushNote: (note: JournalNote) => Promise<string | undefined>;
  deleteNote: (id: string) => Promise<void>;
  pushProgress: (progress: ProgressMap, completedAt: CompletedAtMap) => Promise<void>;
};

let bridge: CloudBridge | null = null;

export function setCloudBridge(next: CloudBridge | null): void {
  bridge = next;
}

export function getCloudBridge(): CloudBridge | null {
  return bridge;
}

export function isLocalOnlyId(id: string): boolean {
  return id.startsWith("jn_") || id.startsWith("note_") || id.includes("-");
}
