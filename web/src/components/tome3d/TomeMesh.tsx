"use client";

import { useFrame, type ThreeEvent } from "@react-three/fiber";
import { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import type { LibraryTome } from "@/lib/libraryTomes";
import { createCoverTexture, createSpineTexture } from "./coverTexture";
import { tomeVisualFor } from "./visuals";

const HEIGHT = 10.8;
const WIDTH = 7.2;

type TomeMeshProps = {
  item: LibraryTome;
  hovered?: boolean;
  active?: boolean;
  coverTwist?: number;
  onClick?: (event: ThreeEvent<MouseEvent>) => void;
  onPointerOver?: (event: ThreeEvent<PointerEvent>) => void;
  onPointerOut?: (event: ThreeEvent<PointerEvent>) => void;
};

export function TomeMesh({
  item,
  hovered = false,
  active = false,
  coverTwist = 0,
  onClick,
  onPointerOver,
  onPointerOut,
}: TomeMeshProps) {
  const rootRef = useRef<THREE.Group>(null);
  const thickness = 0.55 + tomeVisualFor(item).thickness * 0.28;
  const [materials, setMaterials] = useState<THREE.Material[] | null>(null);

  useEffect(() => {
    const v = tomeVisualFor(item);
    const depth = 0.55 + v.thickness * 0.28;
    const input = {
      title: item.displayName,
      author: item.author,
      tradition: item.tradition,
      glyph: item.glyph,
      palette: v.palette,
    };
    const coverMap = createCoverTexture(input);
    const spineMap = createSpineTexture(input, 90 + depth * 28);

    const cloth = new THREE.MeshPhysicalMaterial({
      color: v.palette.cloth,
      roughness: 0.72 - v.foil * 0.2,
      metalness: 0.1 + v.foil * 0.3,
      clearcoat: v.foil * 0.35,
      clearcoatRoughness: 0.45,
    });
    const paper = new THREE.MeshStandardMaterial({
      color: v.palette.paper,
      roughness: 0.94,
      metalness: 0,
    });
    const cover = new THREE.MeshPhysicalMaterial({
      map: coverMap,
      roughness: 0.62 - v.foil * 0.18,
      metalness: 0.12 + v.foil * 0.28,
      clearcoat: 0.18 + v.foil * 0.35,
      clearcoatRoughness: 0.4,
    });
    const spine = new THREE.MeshPhysicalMaterial({
      map: spineMap,
      roughness: 0.68,
      metalness: 0.14 + v.foil * 0.22,
      clearcoat: v.foil * 0.3,
      clearcoatRoughness: 0.5,
    });

    // Box faces: +x spine, -x back board, +y/-y page edges, +z cover, -z back
    const next = [spine, cloth, paper, paper, cover, cloth];
    setMaterials(next);

    return () => {
      coverMap.dispose();
      spineMap.dispose();
      for (const m of next) m.dispose();
    };
  }, [item]);

  useFrame((_, dt) => {
    const root = rootRef.current;
    if (!root) return;
    const targetX = hovered ? -0.72 : active ? -0.45 : -0.55;
    const targetY = coverTwist * 0.4;
    const targetZ = hovered ? 0.55 : Math.PI / 4;
    const targetLift = hovered ? 1.35 : 0;
    const k = 1 - Math.exp(-9 * dt);
    root.rotation.x += (targetX - root.rotation.x) * k;
    root.rotation.y += (targetY - root.rotation.y) * k;
    root.rotation.z += (targetZ - root.rotation.z) * k;
    root.position.z += (targetLift - root.position.z) * k;
  });

  return (
    <group
      ref={rootRef}
      onClick={(e) => {
        e.stopPropagation();
        onClick?.(e);
      }}
      onPointerOver={(e) => {
        e.stopPropagation();
        onPointerOver?.(e);
        document.body.style.cursor = "pointer";
      }}
      onPointerOut={(e) => {
        e.stopPropagation();
        onPointerOut?.(e);
        document.body.style.cursor = "auto";
      }}
    >
      {materials ? (
        <mesh castShadow receiveShadow material={materials}>
          <boxGeometry args={[thickness, HEIGHT, WIDTH]} />
        </mesh>
      ) : null}
    </group>
  );
}
