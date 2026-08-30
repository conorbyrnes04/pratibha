import { useEffect, useState } from "@lynx-js/react";
import { useConvex } from "../convex/ConvexProvider";
import { useAuth } from "../auth/AuthProvider";
import { isConvexConfigured } from "../convex/httpClient";
import { storage } from "../lib/storage";

interface JournalNote {
  _id: string;
  passageId: string;
  passageTitle: string;
  body: string;
  tags: string[];
  createdAt: string;
  updatedAt: string;
}

const LOCAL_KEY = "pratibha_lynx_journal";

function loadLocal(): JournalNote[] {
  try {
    const raw = storage.get(LOCAL_KEY);
    const parsed = raw ? JSON.parse(raw) : [];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function saveLocal(notes: JournalNote[]) {
  storage.set(LOCAL_KEY, JSON.stringify(notes));
}

export function JournalPage() {
  const { httpClient } = useConvex();
  const { user } = useAuth();
  const [notes, setNotes] = useState<JournalNote[]>([]);
  const [loading, setLoading] = useState(true);
  const [newNote, setNewNote] = useState("");
  const [newTitle, setNewTitle] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    void loadNotes();
  }, [user]);

  async function loadNotes() {
    const local = loadLocal();
    if (httpClient && user && isConvexConfigured()) {
      try {
        const result = (await httpClient.query("journalNotes:list", {})) as JournalNote[];
        const remote = result || [];
        const merged = mergeNotes(local, remote);
        saveLocal(merged);
        setNotes(merged);
        setLoading(false);
        return;
      } catch (err) {
        console.error("Failed to load notes:", err);
      }
    }
    setNotes(local);
    setLoading(false);
  }

  async function createNote() {
    if (!newNote.trim()) return;
    const note: JournalNote = {
      _id: `local_${Date.now()}`,
      passageId: "manual-entry",
      passageTitle: newTitle.trim() || "Personal Note",
      body: newNote.trim(),
      tags: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    try {
      if (httpClient && user && isConvexConfigured()) {
        await httpClient.mutation("journalNotes:upsert", {
          passageId: note.passageId,
          passageTitle: note.passageTitle,
          body: note.body,
          tags: note.tags,
          createdAt: note.createdAt,
          updatedAt: note.updatedAt,
        });
      }
      const next = [note, ...loadLocal()];
      saveLocal(next);
      setNotes(next);
      setNewNote("");
      setNewTitle("");
      setError("");
    } catch (err) {
      console.error("Failed to create note:", err);
      setError("Could not save to Convex. The note stayed on this device.");
      const next = [note, ...loadLocal()];
      saveLocal(next);
      setNotes(next);
      setNewNote("");
      setNewTitle("");
    }
  }

  if (loading) {
    return (
      <view style={{ padding: 20 }}>
        <text style={{ color: "#999" }}>Loading journal...</text>
      </view>
    );
  }

  return (
    <view style={{ padding: 20 }}>
      <text style={{ color: "#f0c979", fontSize: 24, fontWeight: "bold", marginBottom: 8 }}>Journal</text>
      <text style={{ color: "#999", fontSize: 14, marginBottom: 24 }}>
        {notes.length} {notes.length === 1 ? "entry" : "entries"}
        {user ? " · synced when Convex is reachable" : " · saved on this device"}
      </text>
      {error ? (
        <text style={{ color: "#ff6b6b", fontSize: 14, marginBottom: 16 }}>{error}</text>
      ) : null}

      <view style={{ marginBottom: 32, padding: 16, backgroundColor: "#1a1a2e", borderRadius: 8 }}>
        <text style={{ color: "#ccc", fontSize: 14, marginBottom: 12 }}>New Entry</text>
        <input
          type="text"
          value={newTitle}
          bindinput={(e: any) => setNewTitle(e.detail?.value ?? e.target?.value ?? "")}
          placeholder="Title (optional)"
          style={{
            width: "100%",
            padding: 10,
            marginBottom: 12,
            backgroundColor: "#0a0a0f",
            border: "1px solid #333",
            borderRadius: 4,
            color: "#fff",
            fontSize: 14,
          }}
        />
        <textarea
          value={newNote}
          bindinput={(e: any) => setNewNote(e.detail?.value ?? e.target?.value ?? "")}
          placeholder="Write your reflection..."
          rows={4}
          style={{
            width: "100%",
            padding: 10,
            marginBottom: 12,
            backgroundColor: "#0a0a0f",
            border: "1px solid #333",
            borderRadius: 4,
            color: "#fff",
            fontSize: 14,
            fontFamily: "inherit",
          }}
        />
        <view
          bindtap={newNote.trim() ? createNote : undefined}
          style={{
            padding: 10,
            backgroundColor: newNote.trim() ? "#f0c979" : "#666",
            borderRadius: 4,
          }}
        >
          <text style={{ color: "#000", fontSize: 14, fontWeight: "600", textAlign: "center" }}>
            Save Entry
          </text>
        </view>
      </view>

      <view style={{ gap: 16 }}>
        {notes.length === 0 ? (
          <text style={{ color: "#999", fontSize: 14, textAlign: "center" }}>
            No journal entries yet. Create your first one above!
          </text>
        ) : (
          notes.map((note) => (
            <view
              key={note._id}
              style={{
                padding: 16,
                backgroundColor: "#1a1a2e",
                borderRadius: 8,
                borderLeft: "4px solid #f0c979",
              }}
            >
              <text style={{ color: "#f0c979", fontSize: 16, fontWeight: "600", marginBottom: 4 }}>
                {note.passageTitle}
              </text>
              <text style={{ color: "#666", fontSize: 12, marginBottom: 12 }}>
                {new Date(note.updatedAt).toLocaleDateString()}
              </text>
              <text style={{ color: "#ddd", fontSize: 14, lineHeight: 1.5 }}>{note.body}</text>
            </view>
          ))
        )}
      </view>
    </view>
  );
}

function mergeNotes(local: JournalNote[], remote: JournalNote[]): JournalNote[] {
  const byId = new Map<string, JournalNote>();
  for (const note of [...remote, ...local]) {
    const prev = byId.get(note._id);
    if (!prev || note.updatedAt > prev.updatedAt) byId.set(note._id, note);
  }
  return [...byId.values()].sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));
}
