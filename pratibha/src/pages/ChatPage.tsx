import React, { useState } from "react";
import { sendChat, type ChatMessage, type ChatSource } from "../lib/corpus";
import { C, SERIF } from "../lib/theme";

function sourceLabel(source: ChatSource): string {
  const meta = source.metadata || {};
  const title = String(meta.title || "").trim();
  const ref = String(meta.reference || "").trim();
  if (ref && title) return `${ref} — ${title}`;
  if (title) return title;
  const collection = String(meta.collection || "").trim();
  return collection || "Source passage";
}

export function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [sources, setSources] = useState<ChatSource[]>([]);
  const [useRag, setUseRag] = useState(true);

  async function send() {
    const text = draft.trim();
    if (!text || busy) return;
    const next = [...messages, { role: "user" as const, content: text }];
    setMessages(next);
    setDraft("");
    setBusy(true);
    setError("");
    try {
      const reply = await sendChat(next, { useRag, chatMode: "question" });
      setMessages([...next, { role: "assistant", content: reply.answer || "" }]);
      setSources(reply.sources || []);
      if (reply.compare_warning) setError(reply.compare_warning);
    } catch (err: any) {
      setError(err.message || "Chat failed. Is FastAPI running with an OpenRouter key?");
    } finally {
      setBusy(false);
    }
  }

  return (
    <scroll-view style={{ flex: 1, backgroundColor: C.bg }}>
      <view style={{ padding: 22 }}>
        <text style={{ color: C.gold, fontSize: 26, fontWeight: "bold", fontFamily: SERIF, marginBottom: 8 }}>
          Chat
        </text>
        <text style={{ color: C.muted, fontSize: 14, marginBottom: 16 }}>
          Ask across the corpus. Retrieval stays on unless you turn it off.
        </text>

        <view
          bindtap={() => setUseRag((v) => !v)}
          style={{
            alignSelf: "flex-start",
            marginBottom: 18,
            paddingTop: 6,
            paddingBottom: 6,
            paddingLeft: 12,
            paddingRight: 12,
            backgroundColor: useRag ? C.gold : C.cardAlt,
            borderRadius: 14,
          }}
        >
          <text style={{ color: useRag ? "#000" : C.goldMuted, fontSize: 12 }}>
            {useRag ? "Retrieval on" : "Retrieval off"}
          </text>
        </view>

        <view style={{ gap: 14, marginBottom: 20 }}>
          {messages.length === 0 ? (
            <text style={{ color: C.faint, fontSize: 14 }}>
              Try: What is the gap between two breaths in the Vijñāna Bhairava?
            </text>
          ) : (
            messages.map((msg, i) => (
              <view
                key={String(i)}
                style={{
                  padding: 14,
                  backgroundColor: msg.role === "user" ? C.cardAlt : C.card,
                  borderRadius: 8,
                  borderLeftWidth: 3,
                  borderLeftColor: msg.role === "user" ? C.goldMuted : C.gold,
                }}
              >
                <text style={{ color: C.faint, fontSize: 11, letterSpacing: 1, textTransform: "uppercase", marginBottom: 6 }}>
                  {msg.role === "user" ? "You" : "Pratibha"}
                </text>
                <text style={{ color: C.read, fontSize: 15, lineHeight: 1.6 }}>{msg.content}</text>
              </view>
            ))
          )}
        </view>

        {sources.length ? (
          <view style={{ marginBottom: 20, gap: 8 }}>
            <text style={{ color: C.goldMuted, fontSize: 11, letterSpacing: 1.5, textTransform: "uppercase" }}>
              Sources
            </text>
            {sources.slice(0, 6).map((source, i) => (
              <text key={String(i)} style={{ color: C.muted, fontSize: 13 }}>
                {sourceLabel(source)}
              </text>
            ))}
          </view>
        ) : null}

        {error ? (
          <text style={{ color: C.danger, fontSize: 13, marginBottom: 12 }}>{error}</text>
        ) : null}

        <textarea
          value={draft}
          bindinput={(e: any) => setDraft(e.detail?.value ?? e.target?.value ?? "")}
          placeholder="Ask a question…"
          rows={3}
          style={{
            width: "100%",
            padding: 10,
            marginBottom: 12,
            backgroundColor: C.card,
            border: "1px solid #333",
            borderRadius: 6,
            color: "#fff",
            fontSize: 14,
            fontFamily: "inherit",
          }}
        />
        <view
          bindtap={draft.trim() && !busy ? send : undefined}
          style={{
            padding: 12,
            backgroundColor: draft.trim() && !busy ? C.gold : "#666",
            borderRadius: 6,
          }}
        >
          <text style={{ color: "#000", fontSize: 14, fontWeight: "600", textAlign: "center" }}>
            {busy ? "Listening…" : "Ask"}
          </text>
        </view>
      </view>
    </scroll-view>
  );
}
