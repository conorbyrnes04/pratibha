"use client";

import { useEffect, useState } from "react";

type Tilt = { x: number; y: number };

let tilt: Tilt = { x: 0, y: 0 };
const subs = new Set<(t: Tilt) => void>();
let armed = false;
let permAsked = false;

function clamp(n: number) {
  return Math.max(-1, Math.min(1, n));
}

function publish(next: Tilt) {
  tilt = { x: clamp(next.x), y: clamp(next.y) };
  for (const fn of subs) fn(tilt);
}

function onPointer(e: PointerEvent) {
  const x = (e.clientX / Math.max(1, window.innerWidth)) * 2 - 1;
  const y = (e.clientY / Math.max(1, window.innerHeight)) * 2 - 1;
  publish({ x, y });
}

function onOrient(e: DeviceOrientationEvent) {
  publish({
    x: (e.gamma ?? 0) / 28,
    y: ((e.beta ?? 45) - 45) / 28,
  });
}

async function requestOrient() {
  if (permAsked) return;
  permAsked = true;
  const DOE = DeviceOrientationEvent as unknown as {
    requestPermission?: () => Promise<string>;
  };
  if (typeof DOE.requestPermission === "function") {
    try {
      const state = await DOE.requestPermission();
      if (state !== "granted") return;
    } catch {
      return;
    }
  }
  window.addEventListener("deviceorientation", onOrient, true);
}

function arm() {
  if (armed) return;
  armed = true;
  window.addEventListener("pointermove", onPointer, { passive: true });
  void requestOrient();
}

export function useHoloTilt(enabled: boolean): Tilt {
  const [t, setT] = useState<Tilt>(tilt);
  useEffect(() => {
    if (!enabled) return;
    arm();
    subs.add(setT);
    setT(tilt);
    return () => {
      subs.delete(setT);
    };
  }, [enabled]);
  return enabled ? t : { x: 0, y: 0 };
}

export function enableHoloMotion() {
  arm();
}
