import * as THREE from "three";
import type { CoverDrawInput } from "./types";

const COVER_W = 512;
const COVER_H = 768;
const SPINE_W = 128;
const SPINE_H = 768;

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
    lines[maxLines - 1] = last.replace(/\s+\S*$/, "") + "…";
  }
  return lines;
}

function paintCloth(ctx: CanvasRenderingContext2D, w: number, h: number, color: string) {
  ctx.fillStyle = color;
  ctx.fillRect(0, 0, w, h);
  // Subtle grain
  const image = ctx.getImageData(0, 0, w, h);
  const data = image.data;
  for (let i = 0; i < data.length; i += 4) {
    const n = (Math.random() - 0.5) * 12;
    data[i] = Math.max(0, Math.min(255, data[i] + n));
    data[i + 1] = Math.max(0, Math.min(255, data[i + 1] + n));
    data[i + 2] = Math.max(0, Math.min(255, data[i + 2] + n));
  }
  ctx.putImageData(image, 0, 0);
}

function finishTexture(canvas: HTMLCanvasElement): THREE.CanvasTexture {
  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  texture.anisotropy = 8;
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

  // Accent frame
  ctx.strokeStyle = palette.accent;
  ctx.globalAlpha = 0.55;
  ctx.lineWidth = 3;
  ctx.strokeRect(36, 36, COVER_W - 72, COVER_H - 72);
  ctx.globalAlpha = 0.25;
  ctx.strokeRect(48, 48, COVER_W - 96, COVER_H - 96);
  ctx.globalAlpha = 1;

  // Medallion
  const cx = COVER_W / 2;
  const cy = COVER_H * 0.32;
  ctx.beginPath();
  ctx.arc(cx, cy, 64, 0, Math.PI * 2);
  ctx.strokeStyle = palette.accent;
  ctx.lineWidth = 2;
  ctx.globalAlpha = 0.7;
  ctx.stroke();
  ctx.globalAlpha = 1;
  ctx.fillStyle = palette.accent;
  ctx.globalAlpha = 0.15;
  ctx.fill();
  ctx.globalAlpha = 1;

  // Tradition
  ctx.fillStyle = palette.accent;
  ctx.font = '600 18px "Alegreya Sans", ui-sans-serif, system-ui, sans-serif';
  ctx.textAlign = "center";
  ctx.fillText(tradition.toUpperCase(), cx, cy + 120);

  // Title
  ctx.fillStyle = palette.paper;
  ctx.font = '600 42px "Cormorant Garamond", Georgia, serif';
  const titleLines = wrapLines(ctx, title, COVER_W - 100, 4);
  let y = COVER_H * 0.58;
  for (const line of titleLines) {
    ctx.fillText(line, cx, y);
    y += 48;
  }

  // Author
  ctx.fillStyle = palette.accent;
  ctx.globalAlpha = 0.85;
  ctx.font = 'italic 22px "Cormorant Garamond", Georgia, serif';
  const authorLines = wrapLines(ctx, author, COVER_W - 110, 2);
  y += 18;
  for (const line of authorLines) {
    ctx.fillText(line, cx, y);
    y += 28;
  }
  ctx.globalAlpha = 1;

  // Bottom rule
  ctx.strokeStyle = palette.accent;
  ctx.globalAlpha = 0.4;
  ctx.beginPath();
  ctx.moveTo(COVER_W * 0.28, COVER_H - 72);
  ctx.lineTo(COVER_W * 0.72, COVER_H - 72);
  ctx.stroke();
  ctx.globalAlpha = 1;

  return finishTexture(canvas);
}

export function createSpineTexture(input: CoverDrawInput, thicknessPx = SPINE_W): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = Math.max(64, Math.round(thicknessPx));
  canvas.height = SPINE_H;
  const ctx = canvas.getContext("2d");
  if (!ctx) return finishTexture(canvas);

  const { palette, title, author } = input;
  paintCloth(ctx, canvas.width, canvas.height, palette.cloth);

  ctx.save();
  ctx.translate(canvas.width / 2, canvas.height / 2);
  ctx.rotate(-Math.PI / 2);

  ctx.fillStyle = palette.paper;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.font = '600 28px "Cormorant Garamond", Georgia, serif';
  const max = SPINE_H - 80;
  let label = title;
  while (ctx.measureText(label).width > max && label.length > 4) {
    label = label.slice(0, -2);
  }
  if (label !== title) label = `${label}…`;
  ctx.fillText(label, 0, -6);

  ctx.fillStyle = palette.accent;
  ctx.globalAlpha = 0.8;
  ctx.font = 'italic 16px "Cormorant Garamond", Georgia, serif';
  let authorLabel = author;
  while (ctx.measureText(authorLabel).width > max * 0.7 && authorLabel.length > 4) {
    authorLabel = authorLabel.slice(0, -2);
  }
  ctx.fillText(authorLabel, 0, 22);
  ctx.restore();

  // Top/bottom accent bands
  ctx.fillStyle = palette.accent;
  ctx.globalAlpha = 0.35;
  ctx.fillRect(0, 18, canvas.width, 4);
  ctx.fillRect(0, canvas.height - 22, canvas.width, 4);
  ctx.globalAlpha = 1;

  return finishTexture(canvas);
}
