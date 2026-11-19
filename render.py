#!/usr/bin/env python3
"""Build meme.png (1024x1024) for the gta6-meme-x-01 make.fun bounty.

Layout: an original AI-generated Vice City / Leonida sunset scene with a
gamer slumped at a monitor stuck on a loading bar, plus the REAL make.fun
ghost from the press kit (assets/mark-1024.png) composited into the empty
dark lower third, and big outlined text top and bottom. Deterministic:
same inputs -> same bytes (no timestamps, no randomness).
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "assets",
                    "media-generation-gta6-vice-city-gamer-base-0-579fb561-19f5-4f9a-a14f-4d48822d036a.png")
GHOST = os.path.join(HERE, "assets", "mark-1024.png")
OUT = os.path.join(HERE, "meme.png")

W = H = 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)
YELLOW = (255, 214, 64, 255)
MAGENTA = (226, 0, 140, 255)


def font(size):
    return ImageFont.truetype(BOLD, size)


def fit_font(draw, line, start_size, max_w):
    """Shrink the bold font until the line fits max_w pixels wide."""
    size = start_size
    while size > 20:
        f = ImageFont.truetype(BOLD, size)
        if draw.textbbox((0, 0), line, font=f)[2] <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(BOLD, 20)


def text_center_fit(draw, cx, y, line, size, fill, max_w=980):
    """Draw one centred line, auto-shrunk to fit, with black outline."""
    f = fit_font(draw, line, size, max_w)
    sw = max(3, f.size // 12)
    draw.text((cx, y), line, font=f, fill=fill, anchor="ma",
              stroke_width=sw, stroke_fill=BLACK)


def text_left(draw, x, y, line, size, fill, stroke_w=None):
    f = font(size)
    sw = stroke_w if stroke_w is not None else max(3, size // 12)
    draw.text((x, y), line, font=f, fill=fill, anchor="la",
              stroke_width=sw, stroke_fill=BLACK)


def main():
    base = Image.open(BASE).convert("RGBA").resize((W, H), Image.LANCZOS)
    img = base.copy()
    draw = ImageDraw.Draw(img)

    # --- Top joke: the 13-year wait, over the pink sky -------------------
    # v2: auto-fit so the line can never clip at the right edge (v1 cut "6").
    text_center_fit(draw, W // 2, 28, "WAITED 13 YEARS FOR GTA 6", 62, WHITE)
    text_center_fit(draw, W // 2, 108, "STILL STUCK AT 99%", 58, YELLOW)

    # --- Bottom band: ghost (real press asset) + pitch -------------------
    # Darken the lower third slightly so white text pops on the purple.
    band = Image.new("RGBA", (W, 330), (20, 8, 40, 110))
    img.paste(band, (0, H - 330), band)
    draw = ImageDraw.Draw(img)

    ghost = Image.open(GHOST).convert("RGBA")
    ghost = ghost.resize((310, 310), Image.LANCZOS)
    img.paste(ghost, (W - 330, H - 320), ghost)

    # v2: short lines in the empty LEFT column only (x <= ~360). v1's wide
    # lines ran across the gamer's head and body; the gamer sits centre
    # (x ~380-620), so the left column stays clear of him.
    x = 36
    lines = [
        ("MEANWHILE,", 44, WHITE),
        ("MY AI AGENT", 44, WHITE),
        ("ALREADY WON", 44, YELLOW),
        ("REAL MONEY", 44, YELLOW),
        ("ON make.fun", 44, WHITE),
    ]
    y = H - 308
    for line, size, fill in lines:
        text_left(draw, x, y, line, size, fill)
        y += 60

    img.convert("RGB").save(OUT, "PNG")
    print(f"wrote {OUT} {W}x{H}")


if __name__ == "__main__":
    main()
