import * as THREE from "three";
import type { CoverDrawInput } from "./types";

/** High-res maps — spine text must stay sharp when large in the viewport. */
const COVER_W = 1024;
const COVER_H = 1536;
/** Spine is wide × short: text runs left→right like Stripe Press. */
const SPINE_W = 2048;
const SPINE_H = 384;

function wrapLines(
  ctx: CanvasRenderingContext2D,
  text: string,
  maxWidth: number,
  maxLines: number,
): string[] {
  const words = text.split(/\s+/).filter(Boolean);
  const lines: string[] = [];
  let current = "";
  for (const word of words) {
    const next = current ? `${current} ${word}` : word;
    if (ctx.measureText(next).width <= maxWidth) {
      current = next;
    } else {
      if (current) lines.push(current);
      current = word;
      if (lines.length >= maxLines - 1) break;
    }
  }
  if (current && lines.length < maxLines) lines.push(current);
  if (lines.length === maxLines && words.join(" ").length > lines.join(" ").length) {
    const last = lines[maxLines - 1];
    lines[maxLines - 1] = `${last.replace(/\s+\S*$/, "")}…`;
  }
  return lines;
}

function fitText(
  ctx: CanvasRenderingContext2D,
  text: string,
  maxWidth: number,
  baseSize: number,
  minSize: number,
  font: (size: number) => string,
): { text: string; size: number } {
  let size = baseSize;
  let label = text;
  ctx.font = font(size);
  while (size > minSize && ctx.measureText(label).width > maxWidth) {
    size -= 2;
    ctx.font = font(size);
  }
  while (ctx.measureText(label).width > maxWidth && label.length > 4) {
    label = `${label.slice(0, -2)}…`;
  }
  return { text: label, size };
}

function paintCloth(ctx: CanvasRenderingContext2D, w: number, h: number, color: string) {
  ctx.fillStyle = color;
  ctx.fillRect(0, 0, w, h);
  const image = ctx.getImageData(0, 0, w, h);
  const data = image.data;
  for (let i = 0; i < data.length; i += 4) {
    const n = (Math.random() - 0.5) * 10;
    data[i] = Math.max(0, Math.min(255, data[i] + n));
    data[i + 1] = Math.max(0, Math.min(255, data[i + 1] + n));
    data[i + 2] = Math.max(0, Math.min(255, data[i + 2] + n));
  }
  ctx.putImageData(image, 0, 0);
}

function finishTexture(canvas: HTMLCanvasElement): THREE.CanvasTexture {
  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  texture.anisotropy = 16;
  texture.generateMipmaps = true;
  texture.minFilter = THREE.LinearMipmapLinearFilter;
  texture.magFilter = THREE.LinearFilter;
  texture.needsUpdate = true;
  return texture;
}

export function createCoverTexture(input: CoverDrawInput): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = COVER_W;
  canvas.height = COVER_H;
  const ctx = canvas.getContext("2d");
  if (!ctx) return finishTexture(canvas);

  const { palette, title, author, tradition } = input;
  paintCloth(ctx, COVER_W, COVER_H, palette.cloth);

  ctx.strokeStyle = palette.accent;
  ctx.globalAlpha = 0.55;
  ctx.lineWidth = 5;
  ctx.strokeRect(56, 56, COVER_W - 112, COVER_H - 112);
  ctx.globalAlpha = 0.22;
  ctx.strokeRect(78, 78, COVER_W - 156, COVER_H - 156);
  ctx.globalAlpha = 1;

  const cx = COVER_W / 2;
  const cy = COVER_H * 0.3;
  ctx.beginPath();
  ctx.arc(cx, cy, 90, 0, Math.PI * 2);
  ctx.strokeStyle = palette.accent;
  ctx.lineWidth = 3;
  ctx.globalAlpha = 0.75;
  ctx.stroke();
  ctx.fillStyle = palette.accent;
  ctx.globalAlpha = 0.12;
  ctx.fill();
  ctx.globalAlpha = 1;

  ctx.fillStyle = palette.accent;
  ctx.font = '700 28px "Alegreya Sans", ui-sans-serif, system-ui, sans-serif';
  ctx.textAlign = "center";
  ctx.fillText(tradition.toUpperCase(), cx, cy + 150);

  ctx.fillStyle = palette.paper;
  ctx.font = '600 72px "Cormorant Garamond", Georgia, serif';
  const titleLines = wrapLines(ctx, title, COVER_W - 160, 4);
  let y = COVER_H * 0.52;
  for (const line of titleLines) {
    ctx.fillText(line, cx, y);
    y += 82;
  }

  ctx.fillStyle = palette.accent;
  ctx.globalAlpha = 0.9;
  ctx.font = 'italic 36px "Cormorant Garamond", Georgia, serif';
  for (const line of wrapLines(ctx, author, COVER_W - 180, 2)) {
    ctx.fillText(line, cx, y + 28);
    y += 44;
  }
  ctx.globalAlpha = 1;

  return finishTexture(canvas);
}

/**
 * Spine map: wide canvas, horizontal typography (author · title),
 * matching Stripe Press readability.
 */
export function createSpineTexture(input: CoverDrawInput): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = SPINE_W;
  canvas.height = SPINE_H;
  const ctx = canvas.getContext("2d");
  if (!ctx) return finishTexture(canvas);

  const { palette, title, author, tradition } = input;
  paintCloth(ctx, SPINE_W, SPINE_H, palette.cloth);

  // Edge bands (foil-ish)
  ctx.fillStyle = palette.accent;
  ctx.globalAlpha = 0.4;
  ctx.fillRect(0, 0, 28, SPINE_H);
  ctx.fillRect(SPINE_W - 28, 0, 28, SPINE_H);
  ctx.globalAlpha = 1;

  const midY = SPINE_H / 2;
  const maxTitle = SPINE_W * 0.62;
  const maxAuthor = SPINE_W * 0.22;

  ctx.textBaseline = "middle";
  ctx.textAlign = "left";

  // Author — left, smaller
  ctx.fillStyle = palette.accent;
  const authorFit = fitText(
    ctx,
    author,
    maxAuthor,
    42,
    22,
    (s) => `italic ${s}px "Cormorant Garamond", Georgia, serif`,
  );
  ctx.font = `italic ${authorFit.size}px "Cormorant Garamond", Georgia, serif`;
  ctx.globalAlpha = 0.92;
  ctx.fillText(authorFit.text, 64, midY);
  ctx.globalAlpha = 1;

  // Title — center-weighted, large
  ctx.textAlign = "center";
  ctx.fillStyle = palette.paper;
  const titleFit = fitText(
    ctx,
    title,
    maxTitle,
    78,
    36,
    (s) => `600 ${s}px "Cormorant Garamond", Georgia, serif`,
  );
  ctx.font = `600 ${titleFit.size}px "Cormorant Garamond", Georgia, serif`;
  ctx.fillText(titleFit.text, SPINE_W * 0.55, midY);

  // Tradition mark — right
  ctx.textAlign = "right";
  ctx.fillStyle = palette.accent;
  ctx.globalAlpha = 0.75;
  ctx.font = '700 26px "Alegreya Sans", ui-sans-serif, system-ui, sans-serif';
  const trad = tradition.length > 14 ? `${tradition.slice(0, 12)}…` : tradition;
  ctx.fillText(trad.toUpperCase(), SPINE_W - 56, midY);
  ctx.globalAlpha = 1;

  return finishTexture(canvas);
}
