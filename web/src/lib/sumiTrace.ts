import { sumiSrc } from "@/lib/sumiGlyphs";

export type SumiTrace = {
  viewBox: string;
  transform?: string;
  paths: string[];
  /** Stroke width in the path's user space — potrace groups are often scale(0.1). */
  strokeWidth: number;
};

type RawSumi = {
  viewBox: string;
  transform?: string;
  paths: string[];
};

const rawCache = new Map<string, RawSumi>();
const inkCache = new Map<string, SumiTrace>();
const drawCache = new Map<string, SumiTrace>();

function viewBoxOf(svg: SVGSVGElement): string {
  const existing = svg.getAttribute("viewBox");
  if (existing) return existing;
  const w = parseFloat(svg.getAttribute("width") || "100");
  const h = parseFloat(svg.getAttribute("height") || "100");
  return `0 0 ${w} ${h}`;
}

function viewSize(viewBox: string): { width: number; height: number } {
  const parts = viewBox.split(/[\s,]+/).map(Number);
  return { width: parts[2] || 256, height: parts[3] || parts[2] || 256 };
}

function scaleOf(transform?: string): number {
  const match = /scale\(\s*([-\d.]+)/.exec(transform || "");
  return Math.abs(parseFloat(match?.[1] || "1")) || 1;
}

function measurePaths(paths: string[]): { d: string; area: number; length: number; width: number; height: number }[] {
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("width", "0");
  svg.setAttribute("height", "0");
  svg.style.cssText = "position:absolute;visibility:hidden;pointer-events:none";
  document.body.appendChild(svg);
  const measured = paths.map((d) => {
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", d);
    svg.appendChild(path);
    const box = path.getBBox();
    return {
      d,
      area: box.width * box.height,
      length: path.getTotalLength(),
      width: box.width,
      height: box.height,
    };
  });
  svg.remove();
  return measured;
}

function strokeWidthFor(viewBox: string, transform?: string): number {
  const { width } = viewSize(viewBox);
  return (6 * width) / 220 / scaleOf(transform);
}

function withStroke(raw: RawSumi, paths: string[]): SumiTrace {
  return {
    viewBox: raw.viewBox,
    transform: raw.transform,
    paths,
    strokeWidth: strokeWidthFor(raw.viewBox, raw.transform),
  };
}

/** Crop to the remaining ink so a landscape paper plate does not squash the mark. */
function tightViewBox(paths: string[], transform?: string): string | null {
  if (typeof document === "undefined" || !paths.length) return null;
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("width", "0");
  svg.setAttribute("height", "0");
  svg.style.cssText = "position:absolute;visibility:hidden;pointer-events:none";
  const outer = document.createElementNS("http://www.w3.org/2000/svg", "g");
  const inner = document.createElementNS("http://www.w3.org/2000/svg", "g");
  if (transform) inner.setAttribute("transform", transform);
  for (const d of paths) {
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", d);
    inner.appendChild(path);
  }
  outer.appendChild(inner);
  svg.appendChild(outer);
  document.body.appendChild(svg);
  const box = outer.getBBox();
  svg.remove();
  if (!Number.isFinite(box.width) || !Number.isFinite(box.height) || box.width < 2 || box.height < 2) {
    return null;
  }
  const pad = Math.max(box.width, box.height) * 0.08;
  return `${box.x - pad} ${box.y - pad} ${box.width + pad * 2} ${box.height + pad * 2}`;
}

/** Longest contours only — potrace leaves dozens of seal specks. */
function pickContours(paths: string[]): string[] {
  const measured = measurePaths(paths.filter((d) => d.length > 80))
    .filter((entry) => Number.isFinite(entry.length) && entry.length > 24)
    .sort((a, b) => b.length - a.length);
  const longest = measured[0]?.length ?? 0;
  const floor = Math.max(24, longest * 0.06);
  return measured
    .filter((entry) => entry.length >= floor)
    .slice(0, 12)
    .map((entry) => entry.d);
}

/**
 * Ink only: drop a full-canvas paper plate and the rice-dust specks that
 * otherwise haze into a pale rectangle on a dark page.
 */
function pickInk(paths: string[], viewBox: string, transform?: string): string[] {
  const { width, height } = viewSize(viewBox);
  const scale = scaleOf(transform);
  const worldW = width / scale;
  const worldH = height / scale;
  const all = measurePaths(paths).filter((entry) => entry.area > 0);
  const ink = all.filter((entry) => entry.width < worldW * 0.94 || entry.height < worldH * 0.94);
  const pool = ink.length ? ink : all;
  const largest = Math.max(...pool.map((entry) => entry.area), 1);
  return pool
    .filter((entry) => entry.area >= largest * 0.035)
    .sort((a, b) => b.area - a.area)
    .slice(0, 8)
    .map((entry) => entry.d);
}

async function loadRaw(slug: string): Promise<RawSumi | null> {
  const hit = rawCache.get(slug);
  if (hit) return hit;
  const res = await fetch(sumiSrc(slug));
  if (!res.ok) return null;
  const doc = new DOMParser().parseFromString(await res.text(), "image/svg+xml");
  const svg = doc.querySelector("svg");
  if (!svg) return null;
  const paths = [...svg.querySelectorAll("path")]
    .map((path) => path.getAttribute("d") || "")
    .filter(Boolean);
  if (!paths.length) return null;
  const raw: RawSumi = {
    viewBox: viewBoxOf(svg),
    transform: svg.querySelector("g")?.getAttribute("transform") || undefined,
    paths,
  };
  rawCache.set(slug, raw);
  return raw;
}

export async function loadSumiTrace(slug: string): Promise<SumiTrace | null> {
  const hit = drawCache.get(slug);
  if (hit) return hit;
  const raw = await loadRaw(slug);
  if (!raw) return null;
  const paths = pickContours(raw.paths);
  if (!paths.length) return null;
  const next = withStroke(raw, paths);
  drawCache.set(slug, next);
  return next;
}

/** Full ink silhouette for sitting on the void — no paper plate. */
export async function loadSumiInk(slug: string): Promise<SumiTrace | null> {
  const cacheKey = `${slug}:tight3`;
  const hit = inkCache.get(cacheKey);
  if (hit) return hit;
  const raw = await loadRaw(slug);
  if (!raw) return null;
  const paths = pickInk(raw.paths, raw.viewBox, raw.transform);
  if (!paths.length) return null;
  const viewBox = tightViewBox(paths, raw.transform) ?? raw.viewBox;
  const next = withStroke({ ...raw, viewBox }, paths);
  inkCache.set(cacheKey, next);
  return next;
}
