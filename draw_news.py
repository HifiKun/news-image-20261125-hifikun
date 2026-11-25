#!/usr/bin/env python3
"""Draw the front page for Wednesday 25 November 2026.

One 1024x1024 PNG newspaper front page: masthead, one lead story with
an illustration panel, six picture stories in a 2x3 grid, and three
short briefs at the foot. Everything is drawn with PIL shapes and
DejaVu fonts; no network, no downloaded art.

Run: python3 draw_news.py  ->  writes entry.png next to this file.
"""
import math
from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
MARGIN = 40
PAPER = (248, 244, 235)
INK = (18, 18, 18)
RED = (176, 32, 32)
GREY = (96, 92, 84)
CARD = (255, 255, 255)
CARD_EDGE = (205, 197, 180)
BLUE = (30, 70, 122)
GREEN = (36, 112, 62)
GOLD = (178, 142, 22)
SKY = (214, 230, 240)
SEA = (24, 68, 110)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def fnt(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(d, text, font, width):
    """Split text into lines that fit `width` pixels."""
    out = []
    for chunk in text.split("\n"):
        words = chunk.split()
        line = ""
        for word in words:
            cand = (line + " " + word).strip()
            if d.textlength(cand, font=font) <= width:
                line = cand
            else:
                if line:
                    out.append(line)
                line = word
        if line:
            out.append(line)
    return out


def block(d, x, y, text, font, width, fill=INK, gap=None):
    """Draw a wrapped block of text; return the y below it."""
    if gap is None:
        gap = int(font.size * 1.3)
    for line in wrap_text(d, text, font, width):
        d.text((x, y), line, font=font, fill=fill)
        y += gap
    return y


def hline(d, y, x0=None, x1=None, w=2, fill=INK):
    d.line([(x0 or MARGIN, y), (x1 or PAGE - MARGIN, y)], fill=fill, width=w)


# ---- small pictograms, each drawn inside its own box ----

def pic_flames(d, x, y, w, h):
    """Three flames over a dark sea strip."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + h - 18, x + w, y + h], fill=SEA)
    for cx, s, col in ((x + w * 0.28, 26, RED), (x + w * 0.55, 34, (226, 110, 20)),
                       (x + w * 0.78, 24, RED)):
        cy = y + h - 30
        d.polygon([(cx, cy - s), (cx + s * 0.6, cy - s * 0.1),
                   (cx + s * 0.4, cy + s * 0.5), (cx - s * 0.4, cy + s * 0.5),
                   (cx - s * 0.6, cy - s * 0.1)], fill=col)
        d.ellipse([cx - 5, cy - 4, cx + 5, cy + 6], fill=(255, 214, 90))


def pic_tower(d, x, y, w, h):
    """A tall tower with a blast flash at its foot."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 214))
    bx = x + w * 0.38
    d.rectangle([bx, y + h * 0.22, bx + w * 0.24, y + h], fill=INK)
    d.polygon([(bx - 4, y + h * 0.22), (bx + w * 0.24 + 4, y + h * 0.22),
               (bx + w * 0.12, y + h * 0.06)], fill=INK)
    for wy in range(4):
        d.rectangle([bx + 3, y + h * 0.32 + wy * 16, bx + w * 0.24 - 3,
                     y + h * 0.32 + wy * 16 + 6], fill=(232, 226, 214))
    d.polygon([(x + 12, y + h - 26), (x + 24, y + h - 26), (x + 18, y + h - 8)],
              fill=RED)


def pic_target(d, x, y, w, h):
    """Crosshair over a map pin."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 220))
    cx, cy = x + w // 2, y + h // 2
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=RED, width=4)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=RED)
    d.line([(cx - 34, cy), (cx - 26, cy)], fill=RED, width=4)
    d.line([(cx + 26, cy), (cx + 34, cy)], fill=RED, width=4)
    d.line([(cx, cy - 34), (cx, cy - 26)], fill=RED, width=4)
    d.line([(cx, cy + 26), (cx, cy + 34)], fill=RED, width=4)


def pic_blast(d, x, y, w, h):
    """Starburst blast over a skyline."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 228, 236))
    for bx, bh in ((x + 4, 26), (x + 26, 40), (x + 52, 30)):
        d.rectangle([bx, y + h - bh, bx + 18, y + h], fill=BLUE)
    cx, cy = x + w * 0.68, y + h * 0.38
    pts = []
    for i in range(12):
        ang = i * math.pi / 6
        r = 30 if i % 2 == 0 else 13
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=(226, 110, 20))
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED)


def pic_leaf(d, x, y, w, h):
    """A wilting leaf under a pale sun."""
    d.rectangle([x, y, x + w, y + h], fill=(234, 238, 222))
    d.ellipse([x + w - 26, y + 8, x + w - 6, y + 28], fill=GOLD)
    cx, cy = x + w * 0.42, y + h * 0.55
    d.polygon([(cx, cy - 30), (cx + 24, cy - 6), (cx + 14, cy + 26),
               (cx - 14, cy + 26), (cx - 24, cy - 6)], fill=GREEN)
    d.line([(cx, cy - 30), (cx, cy + 26)], fill=(20, 70, 40), width=3)
    d.line([(cx, cy + 26), (cx + 12, cy + 34)], fill=(20, 70, 40), width=3)


def pic_rocket(d, x, y, w, h):
    """A rocket climbing past stars."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 28, 52))
    for sx, sy in ((x + 10, y + 12), (x + w - 14, y + 22), (x + 18, y + h - 14),
                   (x + w - 22, y + h - 26)):
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    cx = x + w // 2
    d.polygon([(cx, y + 10), (cx + 13, y + 34), (cx - 13, y + 34)], fill=(240, 240, 240))
    d.rectangle([cx - 13, y + 34, cx + 13, y + 62], fill=(200, 205, 215))
    d.polygon([(cx - 13, y + 48), (cx - 24, y + 66), (cx - 13, y + 62)], fill=RED)
    d.polygon([(cx + 13, y + 48), (cx + 24, y + 66), (cx + 13, y + 62)], fill=RED)
    d.polygon([(cx - 6, y + 62), (cx + 6, y + 62), (cx, y + 82)], fill=(255, 190, 60))


def pic_scales(d, x, y, w, h):
    """Scales of justice on a bench."""
    d.rectangle([x, y, x + w, y + h], fill=(236, 230, 220))
    cx, cy = x + w // 2, y + h // 2 + 6
    d.line([(cx, y + 12), (cx, cy + 18)], fill=INK, width=4)
    d.line([(cx - 26, y + 18), (cx + 26, y + 18)], fill=INK, width=4)
    for dx in (-26, 26):
        d.line([(cx + dx, y + 18), (cx + dx, cy)], fill=INK, width=2)
        d.polygon([(cx + dx - 13, cy), (cx + dx + 13, cy),
                   (cx + dx, cy + 12)], fill=INK)
    d.rectangle([cx - 18, cy + 18, cx + 18, cy + 24], fill=INK)


def build():
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.text((PAGE // 2, 16), "THE WORLD", font=fnt(SERIF_B, 92),
           fill=INK, anchor="ma")
    hline(d, 124, w=4)
    d.text((PAGE // 2, 136), "WEDNESDAY, 25 NOVEMBER 2026  ·  WORLD NEWS IN ONE PAGE",
           font=fnt(SANS_B, 23), fill=RED, anchor="ma")
    hline(d, 172, w=2)
    d.text((PAGE // 2, 182), "10 stories, one day — the world on Wednesday 25 November 2026",
           font=fnt(SERIF, 21), fill=GREY, anchor="ma")

    # ---- Lead story: tankers ablaze in the Strait of Hormuz ----
    ly = 216
    d.text((MARGIN, ly), "STRAIT OF HORMUZ", font=fnt(SANS_B, 19), fill=RED)
    y = block(d, MARGIN, ly + 28, "TANKERS ABLAZE\nIN THE STRAIT",
              fnt(SERIF_B, 54), 620, gap=60)
    y = block(d, MARGIN, y + 4,
              "Two oil tankers are struck by naval mines and catch fire "
              "in the Strait of Hormuz. Iran's Revolutionary Guard says "
              "they tried an unauthorised route.",
              fnt(SANS, 22), 600, gap=28)
    pic_flames(d, 688, ly + 8, 296, 196)
    d.text((688, ly + 212), "Two tankers hit mines in the strait",
           font=fnt(SANS, 17), fill=GREY)
    hline(d, 462, w=2)

    # ---- Grid: six picture stories ----
    grid = [
        ("HOUTHIS HIT RIYADH TOWER", "SAUDI ARABIA",
         "A Houthi strike on a Riyadh skyscraper injures 11; the group "
         "also says it hit the Ras Tanura refinery.",
         pic_tower),
        ("HAMAS COLONEL KILLED", "GAZA",
         "Israel kills Mohammad Abuelouf, the Hamas colonel running its "
         "interior security service, and his family.",
         pic_target),
        ("ODESA HIT, KYIV BURNS", "UKRAINE",
         "A Russian strike kills two in Odesa; Kyiv flats burn as Putin "
         "vows revenge for the refinery raids.",
         pic_blast),
        ("COP31 ENDS WITH NO DEAL", "CLIMATE",
         "UN climate talks close with no deal on moving away from fossil "
         "fuels; Pope Leo XIV voices concern.",
         pic_leaf),
        ("PAKISTAN REACHES SPACE", "CHINA · SPACE",
         "China's Shenzhou-24 docks at its station carrying Pakistan's "
         "first astronaut — the first foreigner aboard.",
         pic_rocket),
        ("HUAWEI CONVICTED IN US", "TECH · COURTS",
         "A US court convicts Huawei of conspiring to steal trade secrets "
         "and bank fraud.",
         pic_scales),
    ]
    gx, gy = MARGIN, 478
    cw = (PAGE - 2 * MARGIN - 24) // 2
    chh = 140
    for i, (head, kick, body, pic) in enumerate(grid):
        col, row = i % 2, i // 2
        x = gx + col * (cw + 24)
        top = gy + row * (chh + 10)
        d.rectangle([x, top, x + cw, top + chh], fill=CARD,
                    outline=CARD_EDGE, width=1)
        pic(d, x + 10, top + 10, 78, 78)
        d.text((x + 100, top + 10), kick, font=fnt(SANS_B, 15), fill=RED)
        d.text((x + 100, top + 30), head, font=fnt(SANS_B, 20), fill=INK)
        block(d, x + 14, top + 96, body, fnt(SANS, 16), cw - 28, gap=20)
    hline(d, 930, w=2)

    # ---- Bottom briefs ----
    by = 942
    briefs = [
        ("SUDAN", "RSF drone strikes kill 19 civilians and wound 20 "
         "in two cities, medics say."),
        ("PACIFIC", "Solomon Islands and Australia sign a treaty "
         "barring foreign military bases."),
        ("BANGLADESH", "Garment workers' minimum wage rises 36% to $139 "
         "a month after protests."),
    ]
    bw = (PAGE - 2 * MARGIN - 32) // 3
    for i, (kick, body) in enumerate(briefs):
        x = MARGIN + i * (bw + 16)
        d.text((x, by), kick, font=fnt(SANS_B, 17), fill=RED)
        block(d, x, by + 24, body, fnt(SANS, 15), bw, gap=18)
    hline(d, 1014, w=2)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    build()
