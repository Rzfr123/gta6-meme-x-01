#!/usr/bin/env python3
"""Render the gta6-meme-x-01 satire meme (rev 4).

Replaces the rev-3 drive-by death. Same neon Vice City / Leonida sunset
and GTA "WASTED" death-screen format, new gag: GTA 6's own flaws kill the
gamer. Fresh original illustration: the Hawaiian-shirt gamer slumped
asleep on the waterfront curb, cobwebbed, clutching his controller next
to a tower of old torn calendars, a dusty console and empty cans — he
waited so long the wait itself got him.

Layout (1024x1024, base scene is the full-bleed illustration):
  - Wanted stars: 5 gold stars, top-right corner (GTA HUD detail).
  - "WASTED": huge grey death-screen lettering across the open sky,
    y ~200..380, letter-spaced, black outline.
  - Cause of death sub-line: "CAUSE OF DEATH: 13 YEARS, 2 DELAYS,
    99% LOADING" — the wait, the delays, the loading screen.
  - Loading bar HUD: dark bar, 99% filled, centred over the sun, with
    "99% - EST. TIME: 13 YEARS" under it (the download that never ends).
  - Tagline under the bar: "BACK IN VICE CITY. AGAIN. (SINCE 2002)" —
    the same city as 2002.
  - Bottom punchline bar: translucent black strip (y 908..1024) with the
    REAL make.fun ghost (press-kit mark) at the left and three short lines
    in the left column only (clear of the gamer at the right):
    "MEANWHILE MY AI AGENT" / "ALREADY WON REAL MONEY" / "ON make.fun".
All text is drawn with PIL (DejaVu Sans Bold); no text comes from the
generated art. Auto-fit helpers guarantee no line can clip. No specs,
prices or review scores are invented anywhere in the meme.
"""
import hashlib
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

W = 1024
BASE = ASSETS / "media-generation-gta6-satire-vice-city-base-0-980f51f6-e46d-4a15-86ce-758cce7961f3.png"
GHOST = ASSETS / "mark-1024.png"

# Bottom punchline bar geometry. The gamer sits at the lower right
# (head ~x 640..770, legs/shoe running to the bottom edge), so the bar
# text must stay in the left column, x <= ~650.
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
    wasted_y = 200
    draw_spaced(draw, "WASTED", f_wasted, W // 2, wasted_y, tracking,
                fill="#D8D8D8", stroke="black", stroke_w=7)
    wasted_bottom = wasted_y + f_wasted.size + 14

    # ---- Cause of death sub-line: the satire — wait, delays, loading.
    # Two short lines so each can stay big enough to read at 480px.
    sub_lines = ["CAUSE OF DEATH:",
                 "13 YEARS, 2 DELAYS, 99% LOADING"]
    f_sub = fit_font(sub_lines[1], W - 80, 42)
    sub_y = wasted_bottom + 6
    for t in sub_lines:
        draw_centered(draw, t, f_sub, W // 2, sub_y,
                      fill="white", stroke="black")
        sub_y += int(f_sub.size * 1.08)
    sub_bottom = sub_y

    # ---- Loading bar HUD: stuck at 99% — the download that never ends ----
    bar_w, bar_h = 560, 30
    bar_x0 = (W - bar_w) // 2
    bar_y0 = sub_bottom + 24
    bar_y1 = bar_y0 + bar_h
    assert bar_y1 < 600, bar_y1  # must stay above the skyline/water
    draw.rectangle([bar_x0 - 3, bar_y0 - 3, bar_x0 + bar_w + 3,
                    bar_y1 + 3], fill="black")
    draw.rectangle([bar_x0, bar_y0, bar_x0 + bar_w, bar_y1],
                   fill="#1A1A22")
    fill_w = int(bar_w * 0.99)
    draw.rectangle([bar_x0, bar_y0, bar_x0 + fill_w, bar_y1],
                   fill="#FF2E88")
    draw.rectangle([bar_x0 + fill_w, bar_y0, bar_x0 + bar_w, bar_y1],
                   fill="#3A3A44")
    pct = "99% - EST. TIME: 13 YEARS"
    f_pct = fit_font(pct, W - 120, 32)
    draw_centered(draw, pct, f_pct, W // 2, bar_y1 + 10,
                  fill="white", stroke="black")
    pct_bottom = bar_y1 + 10 + f_pct.size

    # ---- Same-city tagline: back in Vice City again, since 2002.
    # Left-of-centre over the open water so it never crosses the busy
    # calendar stack at the right (v1 defect: "(SINCE 2002)" sat on the
    # beige calendar pages, yellow-on-beige, weak contrast at 480px).
    tag = "BACK IN VICE CITY. AGAIN. (SINCE 2002)"
    f_tag = fit_font(tag, 660, 30)
    tag_y = pct_bottom + 14
    assert tag_y + f_tag.size < 640, tag_y  # must stay above the skyline
    draw_centered(draw, tag, f_tag, 390, tag_y,
                  fill="#FFD23F", stroke="black")

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
          "pct", f_pct.size, "tag", f_tag.size, "bottom", f_bot.size,
          "bar_y1", bar_y1, "tag_y", tag_y)


if __name__ == "__main__":
    main()
