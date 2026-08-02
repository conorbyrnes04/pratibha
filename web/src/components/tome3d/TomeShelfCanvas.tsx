"use client";

import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { ContactShadows } from "@react-three/drei";
import { useEffect, useRef, useState, type MutableRefObject } from "react";
import * as THREE from "three";
import type { LibraryTome } from "@/lib/libraryTomes";
import { TomeMesh, tomeThickness } from "./TomeMesh";

const OPEN_MS = 780;

type SceneProps = {
  tomes: LibraryTome[];
  onOpen: (collection: string) => void;
  reducedMotion: boolean;
  scrubIndexRef: MutableRefObject<number | null>;
  onFocusChange: (tome: LibraryTome | null, index: number) => void;
  onOpeningChange: (opening: boolean) => void;
  wheelTarget: HTMLElement | null;
};

function gapFor(item: LibraryTome): number {
  return tomeThickness(item) + 0.42;
}

function buildOffsets(tomes: LibraryTome[]): { offsets: number[]; total: number } {
  const offsets: number[] = [];
  let cursor = 0;
  for (const tome of tomes) {
    offsets.push(cursor);
    cursor += gapFor(tome);
  }
  return { offsets, total: cursor };
}

function ShelfScene({
  tomes,
  onOpen,
  reducedMotion,
  scrubIndexRef,
  onFocusChange,
  onOpeningChange,
  wheelTarget,
}: SceneProps) {
  const stackRef = useRef<THREE.Group>(null);
  const [hovered, setHovered] = useState<string | null>(null);
  const [openingId, setOpeningId] = useState<string | null>(null);
  const pointer = useRef({ x: 0, y: 0 });
  const targetScroll = useRef(0);
  const smoothScroll = useRef(0);
  const openTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const { camera, size } = useThree();
  const { offsets, total } = buildOffsets(tomes);
  const maxScroll = Math.max(0, total - (tomes[0] ? gapFor(tomes[0]) : 2));

  useEffect(() => {
    if (camera instanceof THREE.PerspectiveCamera) {
      // Fill the frame — less empty sky above the stack.
      camera.fov = size.width < 640 ? 30 : 24;
      camera.position.set(0.8, -0.4, 30);
      camera.rotation.set(-0.08, 0, 0);
      camera.near = 0.1;
      camera.far = 160;
      camera.updateProjectionMatrix();
    }
  }, [camera, size.width]);

  useEffect(() => {
    return () => {
      if (openTimer.current) clearTimeout(openTimer.current);
    };
  }, []);

  useEffect(() => {
    const el = wheelTarget;
    if (!el) return;
    const onWheel = (e: WheelEvent) => {
      if (openingId) return;
      e.preventDefault();
      scrubIndexRef.current = null;
      targetScroll.current = THREE.MathUtils.clamp(
        targetScroll.current + e.deltaY * 0.016,
        0,
        maxScroll,
      );
    };
    el.addEventListener("wheel", onWheel, { passive: false });
    return () => el.removeEventListener("wheel", onWheel);
  }, [wheelTarget, maxScroll, scrubIndexRef, openingId]);

  useEffect(() => {
    const onMove = (e: PointerEvent) => {
      pointer.current = {
        x: (e.clientX / window.innerWidth) * 2 - 1,
        y: (e.clientY / window.innerHeight) * 2 - 1,
      };
    };
    window.addEventListener("pointermove", onMove, { passive: true });
    return () => window.removeEventListener("pointermove", onMove);
  }, []);

  const focusRef = useRef<string | null>(null);

  function beginOpen(collection: string) {
    if (openingId) return;
    scrubIndexRef.current = null;
    // Scroll selected book to center before / during the hero pose.
    const idx = tomes.findIndex((t) => t.collection === collection);
    if (idx >= 0) {
      const y = offsets[idx];
      if (y !== undefined) {
        targetScroll.current = THREE.MathUtils.clamp(y, 0, maxScroll);
      }
    }

    if (reducedMotion) {
      onOpen(collection);
      return;
    }

    setOpeningId(collection);
    onOpeningChange(true);
    openTimer.current = setTimeout(() => {
      onOpen(collection);
      // Keep pose until unmount / navigation; don't reset mid-flight.
    }, OPEN_MS);
  }

  useFrame((_, dt) => {
    if (!openingId) {
      const scrub = scrubIndexRef.current;
      if (scrub !== null) {
        const y = offsets[scrub];
        if (y !== undefined) {
          targetScroll.current = THREE.MathUtils.clamp(y, 0, maxScroll);
        }
      }
    }

    const follow = openingId ? 10 : scrubIndexRef.current !== null ? 14 : 7;
    const k = reducedMotion ? 1 : 1 - Math.exp(-follow * dt);
    smoothScroll.current += (targetScroll.current - smoothScroll.current) * k;
    if (stackRef.current) {
      stackRef.current.position.y = smoothScroll.current;
    }

    let bestIndex = 0;
    let bestDist = Infinity;
    for (let i = 0; i < tomes.length; i++) {
      const y = -offsets[i]! + smoothScroll.current;
      const d = Math.abs(y);
      if (d < bestDist) {
        bestDist = d;
        bestIndex = i;
      }
    }
    const best = tomes[bestIndex] ?? null;
    const id = best?.collection ?? null;
    if (id !== focusRef.current) {
      focusRef.current = id;
      onFocusChange(best, bestIndex);
    }
  });

  return (
    <>
      <color attach="background" args={["#1a1614"]} />
      <ambientLight intensity={0.62} />
      <directionalLight position={[6, 12, 10]} intensity={1.2} castShadow />
      <directionalLight position={[-8, 4, 4]} intensity={0.42} color="#d4c4a8" />
      <spotLight
        position={[2, 8, 16]}
        angle={0.5}
        penumbra={0.85}
        intensity={1}
        color="#f2e2c0"
      />

      {/* Nudge stack up so the first spines sit in the upper half of the frame */}
      <group ref={stackRef} position={[1.1, 1.6, 0]}>
        {tomes.map((tome, i) => {
          const isOpening = openingId === tome.collection;
          const isRetiring = Boolean(openingId && !isOpening);
          return (
            <group key={tome.collection} position={[0, -offsets[i]!, 0]}>
              <TomeMesh
                item={tome}
                hovered={!openingId && hovered === tome.collection}
                opening={isOpening}
                retiring={isRetiring}
                coverTwist={
                  !openingId && hovered === tome.collection ? pointer.current.x : 0
                }
                onPointerOver={() => setHovered(tome.collection)}
                onPointerOut={() => setHovered((h) => (h === tome.collection ? null : h))}
                onClick={() => beginOpen(tome.collection)}
              />
            </group>
          );
        })}
      </group>

      <ContactShadows position={[1.1, -9, 0]} opacity={0.32} scale={40} blur={2.2} far={18} />
    </>
  );
}

export function TomeShelfCanvas({
  tomes,
  onOpen,
  onFocusChange,
  onOpeningChange,
  scrubIndexRef,
  wheelTarget,
}: {
  tomes: LibraryTome[];
  onOpen: (collection: string) => void;
  onFocusChange?: (tome: LibraryTome | null, index: number) => void;
  onOpeningChange?: (opening: boolean) => void;
  scrubIndexRef: MutableRefObject<number | null>;
  wheelTarget: HTMLElement | null;
}) {
  const [reducedMotion, setReducedMotion] = useState(false);
  const focusCb = onFocusChange ?? (() => {});
  const openingCb = onOpeningChange ?? (() => {});

  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReducedMotion(mq.matches);
    const onChange = () => setReducedMotion(mq.matches);
    mq.addEventListener("change", onChange);
    return () => mq.removeEventListener("change", onChange);
  }, []);

  return (
    <Canvas
      className="tome-shelf-3d__canvas"
      camera={{ position: [0.8, -0.4, 30], fov: 24, near: 0.1, far: 160 }}
      dpr={[1, 2]}
      gl={{ antialias: true, alpha: false, powerPreference: "high-performance" }}
      shadows
    >
      <ShelfScene
        tomes={tomes}
        onOpen={onOpen}
        reducedMotion={reducedMotion}
        scrubIndexRef={scrubIndexRef}
        onFocusChange={focusCb}
        onOpeningChange={openingCb}
        wheelTarget={wheelTarget}
      />
    </Canvas>
  );
}
