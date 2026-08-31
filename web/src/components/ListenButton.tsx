"use client";

import { useAuthToken } from "@convex-dev/auth/react";
import { useEffect, useRef, useState } from "react";
import { listenConfigured, listenPassage, ListenApiError } from "@/lib/api";

type Phase = "idle" | "loading" | "playing" | "paused";

export function ListenButton({ verseId }: { verseId: string }) {
  const accessToken = useAuthToken();
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const objectUrlRef = useRef<string | null>(null);
  const [available, setAvailable] = useState(false);
  const [phase, setPhase] = useState<Phase>("idle");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    listenConfigured().then((ok) => {
      if (!cancelled) setAvailable(ok);
    });
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    return () => {
      audioRef.current?.pause();
      if (objectUrlRef.current) URL.revokeObjectURL(objectUrlRef.current);
    };
  }, []);

  useEffect(() => {
    audioRef.current?.pause();
    setPhase("idle");
    setError(null);
    if (objectUrlRef.current) {
      URL.revokeObjectURL(objectUrlRef.current);
      objectUrlRef.current = null;
    }
    if (audioRef.current) audioRef.current.src = "";
  }, [verseId]);

  if (!available) return null;

  async function onToggle() {
    const audio = audioRef.current;
    if (phase === "playing" && audio) {
      audio.pause();
      setPhase("paused");
      return;
    }
    if (phase === "paused" && audio?.src) {
      await audio.play();
      setPhase("playing");
      return;
    }
    setError(null);
    setPhase("loading");
    try {
      const { blob } = await listenPassage(verseId, accessToken);
      if (objectUrlRef.current) URL.revokeObjectURL(objectUrlRef.current);
      const url = URL.createObjectURL(blob);
      objectUrlRef.current = url;
      const player = audioRef.current ?? new Audio();
      audioRef.current = player;
      player.src = url;
      player.onended = () => setPhase("idle");
      player.onerror = () => {
        setError("Playback failed.");
        setPhase("idle");
      };
      await player.play();
      setPhase("playing");
    } catch (err) {
      const status = err instanceof ListenApiError ? err.status : 0;
      if (status === 401) {
        setError("Sign in to listen.");
      } else if (status === 429) {
        setError("Listen is resting. Try again in a minute.");
      } else {
        setError(err instanceof Error ? err.message : "Could not speak this passage.");
      }
      setPhase("idle");
    }
  }

  const label =
    phase === "loading" ? "Preparing…" : phase === "playing" ? "Pause" : phase === "paused" ? "Resume" : "Listen";

  return (
    <div className="passage-listen">
      <button
        type="button"
        className="passage-reading__toggle"
        onClick={onToggle}
        disabled={phase === "loading"}
        aria-pressed={phase === "playing"}
      >
        {label}
      </button>
      {error ? <p className="passage-listen__error">{error}</p> : null}
    </div>
  );
}