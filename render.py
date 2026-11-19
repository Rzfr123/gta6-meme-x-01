#!/usr/bin/env python3
"""Render the gta6-meme-x-01 WASTED drive-by meme (rev 3).

Replaces the rev-2 "99% loading screen" death. Same neon Vice City /
Leonida sunset and GTA death-screen format, new gag: the gamer gets SHOT
in a drive-by while waiting for the game. Fresh original illustration:
a pink convertible speeds away with a muzzle flash, the Hawaiian-shirt
gamer slumps on the curb still clutching his controller, cans scattered.

Layout (1024x1024, base scene is the full-bleed illustration):
  - Wanted stars: 5 gold stars, top-right corner (GTA HUD detail).
  - "WASTED": huge grey death-screen lettering across the open sky,
    y ~250..430, letter-spaced, black outline.
  - Sub-line under it: "CAUSE OF DEATH: SHOT WHILE WAITING FOR GTA 6".
  - Loading bar HUD: dark bar, 99% filled, centred over the sun — the
    wait that got him killed.
  - Bottom punchline bar: translucent black strip (y 908..1024) with the
    REAL make.fun ghost (press-kit mark) at the left and three short lines
    in the left column only (clear of the gamer's face/legs at the right):
    "MEANWHILE MY AI AGENT" / "ALREADY WON REAL MONEY" / "ON make.fun".
All text is drawn with PIL (DejaVu Sans Bold); no text comes from the
generated art. Auto-fit helpers guarantee no line can clip.
"""
import hashlib
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

W = 1024
BASE = ASSETS / "media-generation-gta6-wasted-driveby-vice-city-0-b0d5924a-24f7-4ec1-8828-ba1c08e3a3fa.png"
GHOST = ASSETS / "mark-1024.png"

# Bottom punchline bar geometry. The gamer sits at the lower right
# (head ~x 830..960, legs running to the bottom edge), so the bar text
# must stay in the left column, x <= ~650.
BAR_Y0 = 908
BAR_Y1 = 1024


def fit_font(text, max_w, start, min_size=20):
    """Largest bold font size at which `text` fits max_w."""
    size = start
    while size > min_size:
        f = ImageFont.truetype(BOLD, size)
        if f.getlength(text) <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(BOLD, min_size)


def draw_outlined(draw, xy, text, font, fill="white", stroke="black",
                  stroke_w=None):
    sw = stroke_w if stroke_w is not None else max(2, font.size // 12)
    draw.text(xy, text, font=font, fill=fill, stroke_width=sw,
              stroke_fill=stroke)


def draw_centered(draw, text, font, cx, y, **kw):
    draw_outlined(draw, (cx - font.getlength(text) / 2, y), text, font, **kw)


def draw_spaced(draw, text, font, cx, y, tracking, fill, stroke, stroke_w):
    """Draw `text` centred with extra letter spacing (death-screen feel)."""
    widths = [font.getlength(ch) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill, stroke_width=stroke_w,
                  stroke_fill=stroke)
        x += w + tracking


def draw_star(draw, cx, cy, r, fill, stroke="black", stroke_w=3):
    """Five-pointed wanted star centred at (cx, cy)."""
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill, outline=stroke, width=stroke_w)


def main():
    base = Image.open(BASE).convert("RGB").resize((W, W), Image.LANCZOS)
    ghost = Image.open(GHOST).convert("RGBA")
    canvas = base.copy()
    draw = ImageDraw.Draw(canvas, "RGBA")

    # ---- Wanted stars: 5 stars, top-right (GTA HUD) ----
    star_r, gap, top = 26, 62, 52
    x = W - 24 - star_r
    for _ in range(5):
        draw_star(draw, x, top, star_r, fill="#FFD23F")
        x -= gap

    # ---- WASTED: huge grey death-screen lettering over the open sky ----
    f_wasted = fit_font("WASTED", W - 60, 200)
    tracking = 18
    while (sum(f_wasted.getlength(c) for c in "WASTED")
           + tracking * 5 > W - 40 and f_wasted.size > 60):
        f_wasted = ImageFont.truetype(BOLD, f_wasted.size - 4)
    wasted_y = 258
    draw_spaced(draw, "WASTED", f_wasted, W // 2, wasted_y, tracking,
                fill="#D8D8D8", stroke="black", stroke_w=7)
    wasted_bottom = wasted_y + f_wasted.size + 14

    # ---- Cause of death sub-line: the new drive-by gag ----
    sub = "CAUSE OF DEATH: SHOT WHILE WAITING FOR GTA 6"
    f_sub = fit_font(sub, W - 80, 46)
    draw_centered(draw, sub, f_sub, W // 2, wasted_bottom + 6,
                  fill="white", stroke="black")

    # ---- Loading bar HUD: stuck at 99% — the wait that got him killed ----
    bar_w, bar_h = 560, 30
    bar_x0 = (W - bar_w) // 2
    bar_y0 = wasted_bottom + 6 + f_sub.size + 26
    bar_y1 = bar_y0 + bar_h
    assert bar_y1 < 640, bar_y1  # must stay above the skyline/water
    draw.rectangle([bar_x0 - 3, bar_y0 - 3, bar_x0 + bar_w + 3,
                    bar_y1 + 3], fill="black")
    draw.rectangle([bar_x0, bar_y0, bar_x0 + bar_w, bar_y1],
                   fill="#1A1A22")
    fill_w = int(bar_w * 0.99)
    draw.rectangle([bar_x0, bar_y0, bar_x0 + fill_w, bar_y1],
                   fill="#FF2E88")
    draw.rectangle([bar_x0 + fill_w, bar_y0, bar_x0 + bar_w, bar_y1],
                   fill="#3A3A44")
    f_pct = ImageFont.truetype(BOLD, 34)
    draw_centered(draw, "99%", f_pct, W // 2, bar_y1 + 10,
                  fill="white", stroke="black")

    # ---- Bottom punchline bar: ghost + three short lines, left column ----
    draw.rectangle([0, BAR_Y0, W, BAR_Y1], fill=(0, 0, 0, 178))
    ghost_size = 104
    g = ghost.resize((ghost_size, ghost_size), Image.LANCZOS)
    gy = BAR_Y0 + (BAR_Y1 - BAR_Y0 - ghost_size) // 2
    canvas.paste(g, (14, gy), g)
    draw = ImageDraw.Draw(canvas, "RGBA")
    lines = ["MEANWHILE MY AI AGENT",
             "ALREADY WON REAL MONEY",
             "ON make.fun"]
    f_bot = fit_font(lines[0], 520, 32)
    lh = int(f_bot.size * 1.12)
    block_h = 3 * lh
    assert block_h <= BAR_Y1 - BAR_Y0 - 6, block_h
    y = BAR_Y0 + (BAR_Y1 - BAR_Y0 - block_h) // 2
    cx = 130 + 520 // 2
    for t in lines:
        draw_centered(draw, t, f_bot, cx, y, fill="white", stroke="black")
        y += lh

    out = HERE / "meme.png"
    canvas.save(out, "PNG")
    print("wrote", out, canvas.size)
    print("sha256", hashlib.sha256(out.read_bytes()).hexdigest())
    print("wasted font", f_wasted.size, "sub", f_sub.size,
          "bottom", f_bot.size, "bar_y1", bar_y1)


if __name__ == "__main__":
    main()
