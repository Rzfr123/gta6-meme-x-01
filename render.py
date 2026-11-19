#!/usr/bin/env python3
"""Render the gta6-meme-x-01 Drake-format meme (rev 1).

Layout (1024x1024 total):
  Top half    (y 0..506):  text block left  | reject panel right (512x512)
  Divider: white 12px bar (y 506..518)
  Bottom half (y 518..1024): approve panel left (512x506) | ghost + text right
The approve character points right, straight at the real make.fun ghost,
so the ghost is part of the scene, not a corner sticker.
Text: DejaVu Sans Bold, white fill, thick black outline (classic meme style),
auto-shrunk so no line can ever clip (lesson from v1 of the previous meme).
"""
import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

W = 1024
HALF = 512
DIV = 12  # white divider height between the two halves
TOP_H = 506
BOT_H = W - TOP_H - DIV  # 506

REJECT = ASSETS / "media-generation-drake-reject-panel-0-fdf72acd-0eed-4c7f-9089-f09bc4166a97.webp"
APPROVE = ASSETS / "media-generation-drake-approve-panel-0-1d31e28e-b07e-48dc-8ec6-8a401b9b6f98.webp"
GHOST = ASSETS / "mark-1024.png"


def fit_font(lines, max_w, start, min_size=20):
    """Largest bold font size at which every line fits max_w."""
    size = start
    while size > min_size:
        f = ImageFont.truetype(BOLD, size)
        if all(f.getlength(t) <= max_w for t in lines):
            return f
        size -= 2
    return ImageFont.truetype(BOLD, min_size)


def draw_lines(draw, lines, font, cx, y, fill="white", stroke="black",
               spacing=None):
    """Draw centred outlined lines; returns y after the last line."""
    sw = max(2, font.size // 10)
    lh = spacing or int(font.size * 1.18)
    for t in lines:
        w = font.getlength(t)
        draw.text((cx - w / 2, y), t, font=font, fill=fill,
                  stroke_width=sw, stroke_fill=stroke)
        y += lh
    return y


def main():
    reject = Image.open(REJECT).convert("RGB").resize((HALF, TOP_H))
    approve = Image.open(APPROVE).convert("RGB").resize((HALF, BOT_H))
    ghost = Image.open(GHOST).convert("RGBA")

    # Panel background colour (sampled from a corner of the art) so the
    # text blocks blend seamlessly with the illustrations.
    bg = reject.getpixel((5, 5))

    canvas = Image.new("RGB", (W, W), "white")
    canvas.paste(reject, (HALF, 0))
    canvas.paste(approve, (0, TOP_H + DIV))
    draw = ImageDraw.Draw(canvas)

    # ---- Top-left text block (reject): beige, matches the panel bg ----
    draw.rectangle([0, 0, HALF, TOP_H], fill=bg)
    top_big = ["WAITING", "13 YEARS", "FOR GTA 6"]
    f_big = fit_font(top_big, HALF - 40, 78)
    top_small = ["STILL STUCK", "AT 99%"]
    f_small = fit_font(top_small, HALF - 40, 52)
    block_h = len(top_big) * int(f_big.size * 1.18) + 14 + \
        len(top_small) * int(f_small.size * 1.18)
    y = (TOP_H - block_h) // 2
    y = draw_lines(draw, top_big, f_big, HALF // 2, y)
    y = draw_lines(draw, top_small, f_small, HALF // 2, y + 14)

    # ---- Bottom-right block (approve): ghost + text ----
    draw.rectangle([HALF, TOP_H + DIV, W, W], fill=bg)
    bot_lines = ["MY AI AGENT", "ALREADY WON", "REAL MONEY", "ON make.fun"]
    f_bot = fit_font(bot_lines, HALF - 40, 50)
    ghost_size = 230
    g = ghost.resize((ghost_size, ghost_size), Image.LANCZOS)
    text_h = len(bot_lines) * int(f_bot.size * 1.18)
    block_h = ghost_size + 14 + text_h
    # v2: block must fit inside BOT_H with margin on both sides; v1's
    # 518px block overflowed the 506px half and clipped "ON make.fun".
    assert block_h <= BOT_H - 12, block_h
    y0 = TOP_H + DIV + (BOT_H - block_h) // 2
    canvas.paste(g, (HALF + (HALF - ghost_size) // 2, y0), g)
    draw_lines(draw, bot_lines, f_bot, HALF + HALF // 2,
               y0 + ghost_size + 14)

    out = HERE / "meme.png"
    canvas.save(out, "PNG")
    print("wrote", out, canvas.size)
    print("sha256", hashlib.sha256(out.read_bytes()).hexdigest())
    print("top font", f_big.size, "small", f_small.size, "bottom", f_bot.size)


if __name__ == "__main__":
    main()
