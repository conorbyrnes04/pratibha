/** Frozen holographic sheen for share PNGs. Live cards tilt; captures cannot. */

/** Twelve palettes, 30° apart, so cards actually look different on a phone. */
export function holoHueFromSeed(seed: string): number {
  let h = 2166136261;
  for (let i = 0; i < seed.length; i++) {
    h ^= seed.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return ((h >>> 0) % 12) * 30;
}

function hsla(h: number, s: number, l: number, a: number): string {
  return `hsla(${((h % 360) + 360) % 360}, ${s}%, ${l}%, ${a})`;
}

export function bakeHoloFoil(src: Blob, hue = 0): Promise<Blob> {
  return new Promise((resolve) => {
    const url = URL.createObjectURL(src);
    const img = new Image();
    img.onload = () => {
      URL.revokeObjectURL(url);
      const canvas = document.createElement("canvas");
      canvas.width = img.naturalWidth;
      canvas.height = img.naturalHeight;
      const ctx = canvas.getContext("2d");
      if (!ctx) {
        resolve(src);
        return;
      }
      const w = canvas.width;
      const h = canvas.height;
      ctx.drawImage(img, 0, 0);

      ctx.save();
      const band = ctx.createLinearGradient(w * 0.04, h * 0.1, w * 0.96, h * 0.9);
      band.addColorStop(0.16, "rgba(255,255,255,0)");
      band.addColorStop(0.34, hsla(hue, 95, 78, 0.38));
      band.addColorStop(0.44, hsla(hue + 46, 92, 70, 0.52));
      band.addColorStop(0.52, hsla(hue + 8, 98, 62, 0.78));
      band.addColorStop(0.62, hsla(hue + 110, 88, 68, 0.42));
      band.addColorStop(0.82, "rgba(255,255,255,0)");
      ctx.globalCompositeOperation = "screen";
      ctx.fillStyle = band;
      ctx.fillRect(0, 0, w, h);

      ctx.globalCompositeOperation = "overlay";
      ctx.strokeStyle = hsla(hue, 90, 62, 0.36);
      ctx.lineWidth = Math.max(1, w / 520);
      const step = Math.max(5, Math.round(w / 88));
      ctx.beginPath();
      for (let x = -h; x < w + h; x += step) {
        ctx.moveTo(x, 0);
        ctx.lineTo(x + h * 0.38, h);
      }
      ctx.stroke();
      ctx.restore();

      ctx.globalCompositeOperation = "source-over";
      canvas.toBlob((out) => resolve(out || src), "image/png");
    };
    img.onerror = () => {
      URL.revokeObjectURL(url);
      resolve(src);
    };
    img.src = url;
  });
}
