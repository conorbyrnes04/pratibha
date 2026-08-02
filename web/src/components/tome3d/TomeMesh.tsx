"use client";

import { useFrame, type ThreeEvent } from "@react-three/fiber";
import { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import type { LibraryTome } from "@/lib/libraryTomes";
import { createCoverTexture, createSpineTexture } from "./coverTexture";
import { tomeVisualFor } from "./visuals";

/**
 * Stripe Press layout: book as a horizontal slab.
 * X = spine length · Y = thickness · Z = cover depth
 * +Z = spine facing camera, +Y = cover on top.
 */
export const BOOK_LENGTH = 11.2;
export const BOOK_DEPTH = 7.1;

type TomeMeshProps = {
  item: LibraryTome;
  hovered?: boolean;
  /** Hero / opening pose — cover faces the reader */
  opening?: boolean;
  /** Dim + push back while another book opens */
  retiring?: boolean;
  coverTwist?: number;
  onClick?: (event: ThreeEvent<MouseEvent>) => void;
  onPointerOver?: (event: ThreeEvent<PointerEvent>) => void;
  onPointerOut?: (event: ThreeEvent<PointerEvent>) => void;
};

export function tomeThickness(item: LibraryTome): number {
  return 0.85 + tomeVisualFor(item).thickness * 0.22;
}

export function TomeMesh({
  item,
  hovered = false,
  opening = false,
  retiring = false,
  coverTwist = 0,
  onClick,
  onPointerOver,
  onPointerOut,
}: TomeMeshProps) {
  const rootRef = useRef<THREE.Group>(null);
  const thickness = tomeThickness(item);
  const [materials, setMaterials] = useState<THREE.Material[] | null>(null);

  useEffect(() => {
    const v = tomeVisualFor(item);
    const input = {
      title: item.displayName,
      author: item.author,
      tradition: item.tradition,
      glyph: item.glyph,
      palette: v.palette,
    };
    const coverMap = createCoverTexture(input);
    const spineMap = createSpineTexture(input);

    const cloth = new THREE.MeshPhysicalMaterial({
      color: v.palette.cloth,
      roughness: 0.7 - v.foil * 0.15,
      metalness: 0.08 + v.foil * 0.25,
      clearcoat: v.foil * 0.3,
      clearcoatRoughness: 0.5,
    });
    const paper = new THREE.MeshStandardMaterial({
      color: v.palette.paper,
      roughness: 0.94,
      metalness: 0,
    });
    const cover = new THREE.MeshPhysicalMaterial({
      map: coverMap,
      roughness: 0.58 - v.foil * 0.15,
      metalness: 0.1 + v.foil * 0.25,
      clearcoat: 0.2 + v.foil * 0.3,
      clearcoatRoughness: 0.4,
    });
    const spine = new THREE.MeshPhysicalMaterial({
      map: spineMap,
      roughness: 0.55,
      metalness: 0.12 + v.foil * 0.2,
      clearcoat: 0.15 + v.foil * 0.25,
      clearcoatRoughness: 0.45,
    });

    const next = [paper, paper, cover, cloth, spine, paper];
    for (const m of next) {
      m.transparent = true;
      m.opacity = 1;
    }
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

    // Spine browse → tip cover at reader. Opening → Stripe detail pose (cover-forward).
    let targetX = -0.78;
    let targetY = coverTwist * 0.14;
    let targetZ = 0;
    let targetLift = hovered ? 0.85 : 0.15;
    let targetXPos = 0;
    let targetScale = 1;

    if (opening) {
      // Cover faces camera, pulls toward reader (Stripe activeBook feel).
      targetX = -1.15;
      targetY = 0.42;
      targetZ = 0.12;
      targetLift = 4.8;
      targetXPos = -1.2;
      targetScale = 1.12;
    } else if (retiring) {
      targetX = -0.55;
      targetLift = -2.5;
      targetXPos = 2.5;
      targetScale = 0.92;
    } else if (hovered) {
      targetX = -0.95;
      targetLift = 1.1;
    }

    const speed = opening || retiring ? 6 : 10;
    const k = 1 - Math.exp(-speed * dt);
    root.rotation.x += (targetX - root.rotation.x) * k;
    root.rotation.y += (targetY - root.rotation.y) * k;
    root.rotation.z += (targetZ - root.rotation.z) * k;
    root.position.z += (targetLift - root.position.z) * k;
    root.position.x += (targetXPos - root.position.x) * k;
    const s = root.scale.x + (targetScale - root.scale.x) * k;
    root.scale.setScalar(s);

    if (materials) {
      const opacity = retiring ? 0.35 : 1;
      for (const m of materials) {
        m.transparent = retiring;
        m.opacity += (opacity - m.opacity) * k;
        m.depthWrite = !retiring;
      }
    }
  });

  return (
    <group
      ref={rootRef}
      onClick={(e) => {
        e.stopPropagation();
        if (!opening && !retiring) onClick?.(e);
      }}
      onPointerOver={(e) => {
        e.stopPropagation();
        if (opening || retiring) return;
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
          <boxGeometry args={[BOOK_LENGTH, thickness, BOOK_DEPTH]} />
        </mesh>
      ) : null}
    </group>
  );
}
