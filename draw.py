#!/usr/bin/env python3
"""Draw the v2 entry image for make.fun news-image-20261124.

A one-page newspaper front page summing up Tuesday 24 November 2026,
built from the full day's news (v1 was drawn at 07:30 CST, when only
~7 hours of the day had passed anywhere). Lead: Nvidia brings back
Jensen Huang after Trump steps in; the Tuesday session stalls the
market rebound; tankers hit mines in Hormuz; a Hamas security chief
is killed in Gaza; a Russian strike hits Zaporizhzhia; new US tariffs
loom; US consumer confidence jumps; China extends its export-ban
suspension.

Local build step only: the graded entrypoint is main.py, which copies
the PNG this script produces. Run:  python3 draw.py
Output: entry.png, 1024x1024, deterministic (no randomness, no
dates embedded in the file).
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (246, 241, 229)      # warm newsprint
INK = (26, 26, 26)           # near-black
FAINT = (90, 84, 70)         # captions / footer
RED = (179, 38, 30)          # lead kicker, accents
BLUE = (31, 78, 121)         # section labels
GREEN = (34, 139, 34)        # rising market line
AMBER = (214, 90, 20)        # warning / flame
BOX = (236, 228, 207)        # pictogram tile
BOX_EDGE = (216, 205, 178)   # tile border
RULE = (26, 26, 26)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centred(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


def hline(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# --- pictograms, each drawn inside a 72x72 tile at (x, y) -----------------

def icon_chart_up(d, x, y):
    d.rectangle([x, y, x + 71, y + 71], fill=BOX, outline=BOX_EDGE)
    d.line([(x + 14, y + 58), (x + 14, y + 14)], fill=INK, width=3)
    d.line([(x + 14, y + 58), (x + 60, y + 58)], fill=INK, width=3)
    pts = [(x + 18, y + 52), (x + 30, y + 44), (x + 42, y + 32), (x + 56, y + 20)]
    d.line(pts, fill=GREEN, width=4, joint="curve")
    d.polygon([(x + 56, y + 20), (x + 48, y + 20), (x + 54, y + 28)], fill=GREEN)


def icon_warning(d, x, y):
    d.rectangle([x, y, x + 71, y + 71], fill=BOX, outline=BOX_EDGE)
    d.polygon([(x + 36, y + 10), (x + 61, y + 58), (x + 11, y + 58)],
              fill=AMBER, outline=(146, 64, 8))
    f = font(SANS_BOLD, 30)
    d.text((x + 36 - d.textlength("!", font=f) / 2, y + 22), "!",
           font=f, fill=PAPER)


def icon_scales(d, x, y):
    d.rectangle([x, y, x + 71, y + 71], fill=BOX, outline=BOX_EDGE)
    d.line([(x + 36, y + 14), (x + 36, y + 58)], fill=BLUE, width=3)
    d.line([(x + 16, y + 20), (x + 56, y + 20)], fill=BLUE, width=3)
    d.line([(x + 20, y + 20), (x + 20, y + 40)], fill=BLUE, width=2)
    d.line([(x + 52, y + 20), (x + 52, y + 40)], fill=BLUE, width=2)
    d.pieslice([x + 11, y + 40, x + 29, y + 52], 0, 180, fill=BLUE)
    d.pieslice([x + 43, y + 40, x + 61, y + 52], 0, 180, fill=BLUE)
    d.line([(x + 28, y + 58), (x + 44, y + 58)], fill=BLUE, width=3)


def icon_aid(d, x, y):
    d.rectangle([x, y, x + 71, y + 71], fill=BOX, outline=BOX_EDGE)
    d.ellipse([x + 14, y + 14, x + 58, y + 58], outline=BLUE, width=3)
    d.rectangle([x + 33, y + 22, x + 39, y + 50], fill=BLUE)
    d.rectangle([x + 22, y + 33, x + 50, y + 39], fill=BLUE)


def icon_burst(d, x, y):
    d.rectangle([x, y, x + 71, y + 71], fill=BOX, outline=BOX_EDGE)
    cx, cy = x + 36, y + 36
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        r = 26 if i % 2 == 0 else 11
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=AMBER)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=PAPER)


def icon_flame(d, x, y):
    d.rectangle([x, y, x + 71, y + 71], fill=BOX, outline=BOX_EDGE)
    d.polygon([(x + 36, y + 12), (x + 50, y + 36), (x + 44, y + 52),
               (x + 28, y + 52), (x + 22, y + 36)], fill=AMBER)
    d.polygon([(x + 36, y + 30), (x + 44, y + 44), (x + 36, y + 54),
               (x + 28, y + 44)], fill=(232, 164, 32))


def icon_globe(d, x, y):
    d.rectangle([x, y, x + 71, y + 71], fill=BOX, outline=BOX_EDGE)
    d.ellipse([x + 14, y + 14, x + 58, y + 58], outline=BLUE, width=3)
    d.ellipse([x + 28, y + 14, x + 44, y + 58], outline=BLUE, width=2)
    d.line([(x + 14, y + 36), (x + 58, y + 36)], fill=BLUE, width=2)


def icon_chip(d, x, y):
    d.rectangle([x, y, x + 71, y + 71], fill=BOX, outline=BOX_EDGE)
    d.rectangle([x + 22, y + 22, x + 50, y + 50], outline=INK, width=3)
    d.rectangle([x + 30, y + 30, x + 42, y + 42], fill=BLUE)
    for px in (x + 28, x + 36, x + 44):
        d.line([(px, y + 14), (px, y + 22)], fill=INK, width=2)
        d.line([(px, y + 50), (px, y + 58)], fill=INK, width=2)
    for py in (y + 28, y + 36, y + 44):
        d.line([(x + 14, py), (x + 22, py)], fill=INK, width=2)
        d.line([(x + 50, py), (x + 58, py)], fill=INK, width=2)


ICONS = {
    "chart_up": icon_chart_up,
    "warning": icon_warning,
    "scales": icon_scales,
    "aid": icon_aid,
    "burst": icon_burst,
    "flame": icon_flame,
    "globe": icon_globe,
    "chip": icon_chip,
}

STORIES = [
    ("flame", "WAR · HORMUZ", RED,
     "Tankers hit mines in Strait of Hormuz",
     "Iran says three tankers hit mines and caught fire; Tehran refuses talks."),
    ("burst", "WAR · GAZA", RED,
     "Israeli strike kills Hamas security chief",
     "Naeem Abu Nahel dies in a Gaza City strike with six others, two of them police."),
    ("warning", "WAR · ZAPORIZHZHIA", RED,
     "Russian strike kills 2, wounds 40",
     "Overnight strike hits a Zaporizhzhia apartment block; four children among the wounded."),
    ("globe", "TRADE · WASHINGTON", BLUE,
     "Trump poised to unveil new tariffs",
     "Probe into excess capacity in 16 trading partners due; new import duties expected."),
    ("chart_up", "ECONOMY · NEW YORK", BLUE,
     "US consumer confidence jumps",
     "Index hits 103.3, highest since Jan 2025, well above the 92.5 forecast."),
    ("chip", "TRADE · BEIJING", BLUE,
     "China extends export-ban suspension",
     "US-bound gallium, germanium and antimony stay open until Jan 27."),
]


def draw_cell(d, x, y, w, h, story):
    key, kicker, colour, headline, body = story
    ICONS[key](d, x, y + 6)
    tx = x + 88
    tw = w - 88
    kf = font(SANS_BOLD, 15)
    d.text((tx, y + 6), kicker, font=kf, fill=colour)
    hf = font(SANS_BOLD, 24)
    lines = wrap(d, headline, hf, tw)[:2]
    ly = y + 28
    for line in lines:
        d.text((tx, ly), line, font=hf, fill=INK)
        ly += 30
    bf = font(SANS, 18)
    blines = wrap(d, body, bf, tw)[:2]
    by = ly + 4
    for line in blines:
        d.text((tx, by), line, font=bf, fill=INK)
        by += 23


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 40
    cx = W // 2
    right = W - mx

    hline(d, mx, right, 30, 3)
    hline(d, mx, right, 36, 1)
    centred(d, cx, 52, "The World in One Page", font(SERIF_BOLD, 56))
    centred(d, cx, 128, "—  TUESDAY, 24 NOVEMBER 2026  —",
            font(SANS_BOLD, 22), fill=FAINT)
    hline(d, mx, right, 168, 2)

    # Lead story: Nvidia brings back Jensen Huang.
    d.text((mx, 190), "TECH · NEW YORK", font=font(SANS_BOLD, 20), fill=RED)
    d.text((mx, 216), "Nvidia brings back Huang", font=font(SANS_BOLD, 54), fill=INK)
    stand = ("Trump says he struck the deal to restore the chief after he quit "
             "over a spy affair; shares soar 31.5%, then fall 5.9%.")
    sf = font(SANS, 23)
    ly = 292
    for line in wrap(d, stand, sf, right - mx):
        d.text((mx, ly), line, font=sf, fill=INK)
        ly += 31

    # Markets strip: Tuesday session.
    hline(d, mx, right, 372, 1)
    centred(d, cx, 384, "S&P 500 -0.5%  ·  NASDAQ -1.5%  ·  DOW +0.9%  ·  BRENT +2%",
            font(SANS_BOLD, 20))
    hline(d, mx, right, 416, 1)

    # Grid: 2 columns x 3 rows of stories.
    gx, gy = mx, 436
    col_w = (right - mx - 20) // 2
    row_h, gap = 168, 14
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        draw_cell(d, gx + col * (col_w + 20), gy + row * (row_h + gap),
                  col_w, row_h, story)

    # Footer.
    hline(d, mx, right, 972, 1)
    centred(d, cx, 984, "The day's news, Tuesday 24 November 2026 · Drawn from wire reports",
            font(SANS, 15), fill=FAINT)

    img.save(OUT, format="PNG")
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
