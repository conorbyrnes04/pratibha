import React, { useEffect, useState } from "react";
import { useConvex } from "../convex/ConvexProvider";
import { useAuth } from "../auth/AuthProvider";

interface JournalNote {
  _id: string;
  passageId: string;
  passageTitle: string;
  body: string;
  tags: string[];
  createdAt: string;
  updatedAt: string;
}

export function JournalPage() {
  const { httpClient } = useConvex();
  const { user } = useAuth();
  const [notes, setNotes] = useState<JournalNote[]>([]);
  const [loading, setLoading] = useState(true);
  const [newNote, setNewNote] = useState("");
  const [newTitle, setNewTitle] = useState("");

  useEffect(() => {
    loadNotes();
  }, []);

  async function loadNotes() {
    if (!httpClient || !user) return;
    try {
      const result = await httpClient.query("journalNotes:list", {});
      setNotes(result || []);
    } catch (error) {
      console.error("Failed to load notes:", error);
    } finally {
      setLoading(false);
    }
  }

  async function createNote() {
    if (!httpClient || !newNote.trim()) return;

    try {
      await httpClient.mutation("journalNotes:upsert", {
        passageId: "manual-entry",
        passageTitle: newTitle.trim() || "Personal Note",
        body: newNote.trim(),
        tags: [],
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      });
      setNewNote("");
      setNewTitle("");
      await loadNotes();
    } catch (error) {
      console.error("Failed to create note:", error);
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
      <text style={{ color: "#f0c979", fontSize: 24, fontWeight: "bold", marginBottom: 8 }}>
        Journal
      </text>
      <text style={{ color: "#999", fontSize: 14, marginBottom: 24 }}>
        {notes.length} {notes.length === 1 ? "entry" : "entries"}
      </text>

      <view style={{ marginBottom: 32, padding: 16, backgroundColor: "#1a1a2e", borderRadius: 8 }}>
        <text style={{ color: "#ccc", fontSize: 14, marginBottom: 12 }}>New Entry</text>
        <input
          type="text"
          value={newTitle}
          onChange={(e: any) => setNewTitle(e.target.value)}
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
          onChange={(e: any) => setNewNote(e.target.value)}
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
          onClick={newNote.trim() ? createNote : undefined}
          style={{
            padding: 10,
            backgroundColor: newNote.trim() ? "#f0c979" : "#666",
            borderRadius: 4,
            cursor: newNote.trim() ? "pointer" : "default",
          }}
        >
          <text style={{ color: "#000", fontSize: 14, fontWeight: "600", textAlign: "center" }}>
            Save Entry
          </text>
        </view>
      </view>

      <view style={{ gap: 16 }}>
        {notes.length === 0 ? (
          <text style={{ color: "#999", fontSize: 14, textAlign: "center", paddingVertical: 40 }}>
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
              <text style={{ color: "#ddd", fontSize: 14, lineHeight: 1.5 }}>
                {note.body}
              </text>
            </view>
          ))
        )}
      </view>
    </view>
  );
}
