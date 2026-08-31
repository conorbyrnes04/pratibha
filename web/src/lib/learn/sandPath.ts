export type SandPoint = { x: number; y: number };

export type SandBounds = {
  width: number;
  height: number;
};

function hash32(value: string): number {
  let h = 2166136261;
  for (let i = 0; i < value.length; i++) {
    h ^= value.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

function rng(seed: number): () => number {
  let a = seed || 1;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function clamp(n: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, n));
}

function fmt(n: number): string {
  return n.toFixed(1);
}

function confine(point: SandPoint, from: SandPoint, to: SandPoint, bounds?: SandBounds): SandPoint {
  const pad = 18;
  const minX = bounds ? pad : Math.min(from.x, to.x) - 90;
  const maxX = bounds ? bounds.width - pad : Math.max(from.x, to.x) + 90;
  const minY = Math.min(from.y, to.y) + 8;
  const maxY = Math.max(from.y, to.y) - 8;
  return {
    x: clamp(point.x, minX, Math.max(minX + 1, maxX)),
    y: clamp(point.y, Math.min(minY, maxY), Math.max(minY, maxY)),
  };
}

/**
 * A stick dragged through sand. Seed picks a personality — C, S, wave, or hook —
 * so neighboring stretches do not rhyme. The last beat still aims into `to`.
 */
export function sandPathD(from: SandPoint, to: SandPoint, seed: string, bounds?: SandBounds): string {
  const rand = rng(hash32(seed));
  const dx = to.x - from.x;
  const dy = to.y - from.y;
  const dist = Math.hypot(dx, dy);
  if (dist < 8) return `M ${fmt(from.x)} ${fmt(from.y)} L ${fmt(to.x)} ${fmt(to.y)}`;

  const heading = Math.atan2(dy, dx);
  const ux = Math.cos(heading);
  const uy = Math.sin(heading);
  const nx = -uy;
  const ny = ux;
  const side = rand() > 0.5 ? 1 : -1;
  const sameSide = rand() < 0.32;
  const s1 = side;
  const s2 = sameSide ? side : -side;
  const a1 = (0.28 + rand() * 0.22) * dist;
  const a2 = (0.16 + rand() * 0.16) * dist;
  const t1 = 0.26 + rand() * 0.12;
  const t2 = 0.78 + rand() * 0.08;

  const c1 = confine(
    {
      x: from.x + dx * t1 + nx * a1 * s1,
      y: from.y + dy * t1 + ny * a1 * s1 * (0.28 + rand() * 0.22),
    },
    from,
    to,
    bounds,
  );
  const c2 = confine(
    {
      x: to.x - ux * (28 + rand() * 18) + nx * a2 * s2,
      y: to.y - uy * (28 + rand() * 18) + ny * a2 * s2 * 0.2,
    },
    from,
    to,
    bounds,
  );

  return `M ${fmt(from.x)} ${fmt(from.y)} C ${fmt(c1.x)} ${fmt(c1.y)}, ${fmt(c2.x)} ${fmt(c2.y)}, ${fmt(to.x)} ${fmt(to.y)}`;
}
