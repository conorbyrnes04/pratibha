"use client";

import { Canvas, useFrame } from "@react-three/fiber";
import { ContactShadows, Environment } from "@react-three/drei";
import { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import type { LibraryTome } from "@/lib/libraryTomes";
import { TomeMesh } from "./TomeMesh";

const GAP = 5.6;

type SceneProps = {
  tomes: LibraryTome[];
  onOpen: (collection: string) => void;
  reducedMotion: boolean;
};

function ShelfScene({ tomes, onOpen, reducedMotion }: SceneProps) {
  const stackRef = useRef<THREE.Group>(null);
  const tiltRef = useRef<THREE.Group>(null);
  const [hovered, setHovered] = useState<string | null>(null);
  const pointer = useRef({ x: 0, y: 0 });
  const targetScroll = useRef(0);
  const smoothScroll = useRef(0);

  const maxScroll = Math.max(0, (tomes.length - 1) * GAP);

  useEffect(() => {
    const onWheel = (e: WheelEvent) => {
      // Only consume wheel when pointer is over the shelf canvas parent.
      targetScroll.current = THREE.MathUtils.clamp(
        targetScroll.current + e.deltaY * 0.022,
        0,
        maxScroll,
      );
    };
    window.addEventListener("wheel", onWheel, { passive: true });
    return () => window.removeEventListener("wheel", onWheel);
  }, [maxScroll]);

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

  useFrame((_, dt) => {
    const k = reducedMotion ? 1 : 1 - Math.exp(-6 * dt);
    smoothScroll.current += (targetScroll.current - smoothScroll.current) * k;
    if (stackRef.current) {
      stackRef.current.position.y = smoothScroll.current;
    }
    if (tiltRef.current && !reducedMotion) {
      tiltRef.current.rotation.y = THREE.MathUtils.lerp(
        tiltRef.current.rotation.y,
        pointer.current.x * 0.08,
        k,
      );
    }
  });

  return (
    <>
      <color attach="background" args={["#141218"]} />
      <ambientLight intensity={0.55} />
      <directionalLight position={[8, 10, 6]} intensity={1.05} castShadow />
      <directionalLight position={[-6, 4, -4]} intensity={0.35} color="#c4b49a" />
      <spotLight position={[14, 8, 4]} angle={0.4} penumbra={1} intensity={0.55} color="#f0d9a8" />

      <group ref={tiltRef}>
        <group ref={stackRef}>
          {tomes.map((tome, i) => (
            <group key={tome.collection} position={[0, -i * GAP, 0]}>
              <TomeMesh
                item={tome}
                hovered={hovered === tome.collection}
                coverTwist={hovered === tome.collection ? pointer.current.x : 0}
                onPointerOver={() => setHovered(tome.collection)}
                onPointerOut={() => setHovered((h) => (h === tome.collection ? null : h))}
                onClick={() => onOpen(tome.collection)}
              />
            </group>
          ))}
        </group>
      </group>

      <ContactShadows position={[0, -12, 0]} opacity={0.32} scale={48} blur={2.8} far={20} />
      <Environment preset="warehouse" environmentIntensity={0.32} />
    </>
  );
}

export function TomeShelfCanvas({
  tomes,
  onOpen,
}: {
  tomes: LibraryTome[];
  onOpen: (collection: string) => void;
}) {
  const [reducedMotion, setReducedMotion] = useState(false);

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
      camera={{ position: [0, 0, 42], fov: 22, near: 0.1, far: 200 }}
      dpr={[1, 1.75]}
      gl={{ antialias: true, alpha: false }}
      shadows
    >
      <ShelfScene tomes={tomes} onOpen={onOpen} reducedMotion={reducedMotion} />
    </Canvas>
  );
}
