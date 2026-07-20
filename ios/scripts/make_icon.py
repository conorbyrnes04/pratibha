#!/usr/bin/env python3
"""Generate the Pratibhā app icon — a gold yantra on ink, drawn at 4x and
downsampled for clean antialiased strokes. Opaque, square, full-bleed (no
rounded corners / no alpha), per App Store icon rules.

    uv run --with pillow python ios/scripts/make_icon.py
"""
import math
import os

from PIL import Image, ImageDraw, ImageFilter

SCALE = 4
S = 1024 * SCALE
OUT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "Pratibha", "Resources", "Assets.xcassets", "AppIcon.appiconset", "icon_1024.png",
)

INK_TOP = (7, 7, 13)
INK_BOT = (23, 17, 30)
GOLD = (232, 184, 75)
GOLD_HI = (242, 206, 126)
VERM = (192, 86, 61)
LAPIS = (58, 86, 128)


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def main():
    img = Image.new("RGB", (S, S), INK_TOP)
    px = img.load()
    cx = cy = S / 2

    # Vertical ink gradient + soft central gold glow
    max_d = math.hypot(cx, cy)
    for y in range(S):
        t = y / S
        base = lerp(INK_TOP, INK_BOT, t)
        for x in range(S):
            d = math.hypot(x - cx, y - cy) / max_d
            glow = max(0.0, 1 - d * 1.8) ** 2 * 0.22
            px[x, y] = lerp(base, GOLD_HI, glow)

    draw = ImageDraw.Draw(img)
    lw = 3 * SCALE

    def circle(r, color, width=lw):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=width)

    def triangle(r, up, color, width=lw):
        dx, dy = r * 0.866, r * 0.5
        d = -1 if up else 1
        pts = [(cx, cy + d * r), (cx - dx, cy - d * dy), (cx + dx, cy - d * dy)]
        draw.line(pts + [pts[0]], fill=color, width=width, joint="curve")

    R = S * 0.40
    circle(R, LAPIS)
    circle(R * 0.74, GOLD)
    circle(R * 0.50, VERM)
    triangle(R * 0.64, True, GOLD_HI)
    triangle(R * 0.64, False, GOLD_HI)

    # Bindu: a soft blurred gold glow with a bright core, composited on top
    glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gr = R * 0.26
    gd.ellipse([cx - gr, cy - gr, cx + gr, cy + gr], fill=(*GOLD_HI, 170))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=R * 0.10))
    core = R * 0.07
    gd = ImageDraw.Draw(glow)
    gd.ellipse([cx - core, cy - core, cx + core, cy + core], fill=(*GOLD_HI, 255))
    img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")

    img = img.resize((1024, 1024), Image.LANCZOS)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, "PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
