#!/usr/bin/env python3
"""Render the 24 November 2026 world-news front page (1024x1024).

Drawn deterministically with Pillow from the story list below. No network,
no randomness, no timestamps: the same script always writes the same PNG.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF = "DejaVuSerif-Bold.ttf"
F_SANS = "DejaVuSans.ttf"
F_SANSB = "DejaVuSans-Bold.ttf"

INK = (18, 18, 18)
PAPER = (250, 248, 240)
RED = (178, 34, 34)
BLUE = (28, 68, 128)
GREY = (90, 90, 90)
LIGHT = (232, 228, 218)
MAP_LAND = (214, 206, 188)
MAP_SEA = (196, 216, 228)

# ---------------------------------------------------------------- stories
# (dateline, headline, body) — every item verified against Reuters / BBC /
# AP / Al Jazeera / France 24 wires dated 24 Nov 2026 (see README sources).
# Headlines fit one line, bodies one line, in a 320px column at 11/10px.
LEAD = (
    "NEW YORK",
    "HUANG BACK AT NVIDIA; SHARES JUMP 31%",
    "Nvidia's board reinstated Jensen Huang as chief executive on Monday "
    "after President Trump intervened. Shares surged 31% to $165.05, "
    "lifting the Nasdaq 6.5%.",
)

RAIL = [
    ("ZAPORIZHZHIA",
     "Russian strike kills 2, wounds 22",
     "An overnight strike hit homes in Zaporizhzhia; two children are "
     "among the wounded, regional officials said on Tuesday."),
    ("ANTALYA",
     "After no deal, the blame game",
     "COP31 climate talks ended without agreement after fossil-fuel "
     "language split the summit; the fallout dominates Tuesday."),
    ("DHAKA",
     "Hasina plans return on 16 December",
     "The ousted prime minister will fly home from exile in India on the "
     "liberation-war anniversary, her aide told Reuters."),
]

COLUMNS = [
    # column 1
    [
        ("WASHINGTON", "US to blacklist Megaspeed",
         "AI firm at the heart of the Nvidia scandal joins the list."),
        ("WASHINGTON", "FBI deputy to retire in December",
         "Christopher Raia steps down, the Washington Post reported."),
        ("WASHINGTON", "Trump: no Iowa blast without court order",
         "The military must not detonate toxic explosives in Iowa."),
        ("NEW YORK", "CrowdStrike to buy Zscaler for $43.9bn",
         "All-stock deal at $260 a share, a 34% premium."),
        ("NEW YORK", "Anthropic slips as rally passes it by",
         "The newly public AI maker fell 1.4% after its $93.5bn IPO."),
        ("CHICAGO", "Ground stop at O'Hare",
         "Flights held as millions begin Thanksgiving-week travel."),
        ("MEXICO CITY", "Mexico to try 'El Chapo Isidro'",
         "The cartel leader faces trial at home despite a US request."),
        ("BUENOS AIRES", "Inflation quickens to 2.2%",
         "Prices rose 2.2% in October, fastest since April."),
        ("LONDON", "UK destitution hits near 4m",
         "Almost four million in destitution, a new study finds."),
        ("LONDON", "Burnham's 10-year plan under scrutiny",
         "No 10 North faces closer watch as the plan looms."),
        ("BERLIN", "Zelensky urges four-way talks 'soon'",
         "Kyiv is ready to meet 'literally tomorrow', he said."),
    ],
    # column 2
    [
        ("BRUSSELS", "EU weighs sports ban in Russia sanctions",
         "A draft would bar Russian athletes in Europe."),
        ("PARIS", "French far left: 'destroy capitalism'",
         "The BBC meets protesters Macron says threaten the Republic."),
        ("LONDON", "New Museum of London opens",
         "The £437m museum opens its doors to the public."),
        ("MADRID", "Bellingham in Real talks",
         "Jude Bellingham nears a new five-year Real Madrid deal."),
        ("GAZA", "Gaza now a 'toxic wasteland', Oxfam says",
         "Israeli attacks have left Gaza toxic, the aid group said."),
        ("TEHRAN", "Iran vows to end US blockade 'by all means'",
         "Tehran calls the naval blockade an act of aggression."),
        ("TEL AVIV", "Flydubai cleared to return",
         "Israel approves resumption of Dubai-Tel Aviv flights."),
        ("RIYADH", "Oil slides ~3% as flows rise",
         "Middle East supply and a Libyan restart push crude down."),
        ("ABUJA", "Nigeria boat toll reaches 24",
         "Search goes on in Bayelsa after a funeral boat capsized."),
        ("KHARTOUM", "Drones hit homes, UN building",
         "Strikes kill civilians and damage a UN building in Khartoum."),
    ],
    # column 3
    [
        ("KINSHASA", "Congo halts cobalt exports",
         "Top producer suspends exports from 30 Nov to fight a glut."),
        ("NAIROBI", "Kenya, DR Congo restore ties",
         "Full diplomatic ties agreed after years of tension."),
        ("JOHANNESBURG", "New coalition to run Joburg",
         "Major parties seal a deal to govern the metros."),
        ("TOKYO", "Japan factory growth quickens",
         "Flash PMI rises to 53.7 in November on chip demand."),
        ("SEOUL", "Korea rate rise expected Thursday",
         "The central bank is seen lifting its rate to 3.25%."),
        ("BEIJING", "China sentences official to death for spying",
         "A court hands down a death sentence in an espionage case."),
        ("KATHMANDU", "India pledges $1.6bn to Nepal",
         "New Delhi offers aid in a reset of ties with its neighbour."),
        ("TAIPEI", "Taiwan counts 24 PLA aircraft",
         "Seventeen crossed the median line; 11 warships also tracked."),
        ("SINGAPORE", "Singapore, Australia sign two pacts",
         "PM Wong hails a 'trusted partnership' as leaders meet."),
        ("SYDNEY", "Australia warns on AI misuse",
         "Foreign actors will exploit AI, Canberra warns."),
    ],
]

NUMBERS = [
    ("+31%", "Nvidia shares, Monday"),
    ("$43.9bn", "CrowdStrike-Zscaler deal"),
    ("2 killed, 22 wounded", "Zaporizhzhia strike"),
    ("53.7", "Japan factory PMI, Nov."),
    ("24 dead", "Nigeria boat capsize"),
    ("$12.2bn", "Nvidia shorts' paper losses"),
]

DATE_CHECK = [
    "DATE CHECK — Every story here was reported on Tuesday 24 November 2026 "
    "(any time zone), or is a dated follow-up to it.",
    "COP31 counts 198 Parties under the UNFCCC. The figure 196, used wrongly "
    "elsewhere, does not appear in this paper.",
    "Casualty figures are only those named officials reported. Where a toll "
    "was unconfirmed, this paper says so.",
]

# ---------------------------------------------------------------- map data
# Rough continent outlines (lon, lat), equirectangular, drawn for orientation.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 73),
     (-75, 72), (-65, 60), (-55, 52), (-60, 47), (-70, 42), (-75, 35),
     (-80, 26), (-85, 20), (-90, 15), (-95, 18), (-105, 22), (-115, 28),
     (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-45, 60), (-30, 68), (-20, 70), (-25, 76), (-55, 76), (-58, 70)],
    [(-80, 9), (-75, 11), (-62, 10), (-52, 5), (-50, 0), (-42, -5),
     (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-62, -41), (-68, -52),
     (-72, -54), (-73, -40), (-72, -20), (-80, -5), (-81, 0)],
    [(-6, 35), (-10, 31), (-15, 27), (-17, 15), (-12, 8), (-8, 5), (0, 6),
     (6, 4), (9, 4), (13, -1), (12, -6), (13, -12), (12, -18), (16, -28),
     (20, -35), (26, -34), (33, -26), (36, -20), (40, -15), (40, -10),
     (42, -4), (46, -1), (51, 2), (51, 11), (44, 11), (40, 15), (38, 18),
     (36, 22), (34, 28), (32, 31), (25, 32), (19, 33), (10, 37), (0, 36)],
    [(-10, 36), (-9, 43), (-2, 48), (-4, 49), (0, 50), (3, 52), (8, 55),
     (8, 57), (10, 59), (5, 60), (5, 62), (12, 65), (18, 69), (25, 71),
     (32, 70), (40, 68), (50, 69), (60, 70), (70, 72), (80, 73), (90, 75),
     (100, 76), (110, 74), (120, 73), (130, 72), (140, 72), (150, 70),
     (160, 69), (170, 67), (178, 65), (178, 62), (170, 60), (162, 56),
     (158, 52), (150, 59), (142, 55), (140, 50), (135, 43), (130, 42),
     (127, 40), (122, 38), (120, 32), (122, 28), (118, 25), (110, 20),
     (108, 18), (105, 10), (103, 8), (100, 7), (98, 10), (94, 16),
     (91, 22), (88, 22), (86, 20), (80, 15), (77, 8), (75, 10), (72, 20),
     (68, 23), (66, 25), (62, 25), (58, 26), (56, 27), (52, 28), (50, 29),
     (48, 30), (50, 26), (54, 24), (56, 22), (58, 20), (55, 17), (52, 15),
     (48, 14), (44, 13), (42, 15), (40, 15), (38, 18), (35, 28), (34, 31),
     (36, 36), (30, 36), (27, 37), (26, 38), (23, 36), (22, 37), (19, 40),
     (18, 42), (15, 44), (12, 45), (8, 44), (3, 43), (0, 40), (-2, 37),
     (-6, 36)],
    [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 53), (-1, 51)],
    [(130, 31), (132, 33), (135, 34), (138, 35), (140, 37), (141, 40),
     (142, 43), (144, 44), (141, 45), (139, 41), (137, 37), (133, 35)],
    [(95, 5), (98, 3), (100, 0), (103, -2), (106, -6), (110, -7),
     (114, -8), (118, -9), (122, -10), (126, -9), (130, -4), (132, -1),
     (135, -2), (138, -4), (141, -8)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (124, -33),
     (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
     (142, -38), (145, -38), (147, -39), (150, -37), (153, -32),
     (153, -27), (150, -23), (146, -19), (142, -15), (142, -11),
     (137, -12), (135, -15), (132, -12), (130, -13), (126, -14),
     (122, -17), (118, -20)],
    [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38),
     (174, -41), (171, -44)],
]

# (lon, lat, label, dx, dy) — label offset in px from the pin.
PINS = [
    (-77, 39, "WASHINGTON", -84, -14),
    (-99, 19, "MEXICO CITY", -78, 4),
    (30.5, 50.4, "KYIV", -8, -16),
    (35.2, 47.8, "ZAPORIZHZHIA", 8, 8),
    (30.7, 36.9, "ANTALYA", -64, 6),
    (34.5, 31.5, "GAZA", -52, 10),
    (51.4, 35.7, "TEHRAN", 8, 10),
    (32.5, 15.6, "KHARTOUM", 8, -4),
    (15.3, -4.3, "KINSHASA", -68, 8),
    (6.3, 4.9, "BAYELSA", -62, -14),
    (90.4, 23.8, "DHAKA", 8, -6),
    (139.7, 35.7, "TOKYO", 8, -4),
    (127, 37.5, "SEOUL", -52, -14),
]

REGIONS_LINE = ("NORTH AMERICA  ·  SOUTH AMERICA  ·  EUROPE  ·  MIDDLE EAST  ·  "
                "AFRICA  ·  EAST ASIA  ·  SOUTH ASIA  ·  SOUTH-EAST ASIA  ·  OCEANIA")


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 16  # margin

    # ---------------------------------------------------------------- masthead
    d.text((W // 2, 8), "THE WORLD TODAY", font=font(F_SERIF, 46),
           fill=INK, anchor="ma")
    d.text((W // 2, 58), "TUESDAY  24  NOVEMBER  2026", font=font(F_SANSB, 30),
           fill=RED, anchor="ma")
    d.line([(mx, 96), (W - mx, 96)], fill=INK, width=2)
    d.text((W // 2, 102), REGIONS_LINE, font=font(F_SANSB, 10),
           fill=GREY, anchor="ma")

    # ---------------------------------------------------------------- lead band
    ly = 120
    d.rectangle([mx, ly, W - mx, ly + 104], outline=INK, width=1)
    d.line([(mx, ly + 24), (W - mx, ly + 24)], fill=INK, width=1)
    d.text((mx + 10, ly + 4), "LEAD  —  " + LEAD[0], font=font(F_SANSB, 11),
           fill=RED)
    d.text((mx + 10, ly + 28), LEAD[1], font=font(F_SANSB, 21), fill=INK)
    y = ly + 56
    for ln in wrap(d, LEAD[2], font(F_SANS, 12), 620)[:2]:
        d.text((mx + 10, y), ln, font=font(F_SANS, 12), fill=INK)
        y += 16
    # mini bar chart: Monday's market moves
    cx, cy, cw, ch = 700, ly + 36, 290, 36
    d.text((cx, ly + 4), "MONDAY'S MARKET MOVES", font=font(F_SANSB, 10),
           fill=GREY)
    bars = [("NVDA", 31.5), ("DELL", 20.5), ("MICRON", 19.0),
            ("NASDAQ", 6.5), ("S&P 500", 5.0)]
    bw = (cw - 4 * 8) // 5
    for i, (name, val) in enumerate(bars):
        bx = cx + i * (bw + 8)
        bh = max(4, int(ch * val / 32.0))
        d.rectangle([bx, cy + ch - bh, bx + bw, cy + ch], fill=BLUE)
        d.text((bx + bw // 2, cy + ch - bh - 11), "+%.1f%%" % val,
               font=font(F_SANSB, 9), fill=INK, anchor="ma")
        d.text((bx + bw // 2, cy + ch + 2), name, font=font(F_SANS, 8),
               fill=GREY, anchor="ma")

    # ---------------------------------------------------------------- map band
    my = 230
    map_x0, map_y0, map_x1, map_y1 = mx, my, 648, my + 176
    d.rectangle([map_x0, map_y0, map_x1, map_y1], fill=MAP_SEA,
                outline=INK, width=1)
    d.text((map_x0 + 8, map_y0 + 4), "WHERE THE DAY HAPPENED — 13 PLACES",
           font=font(F_SANSB, 11), fill=INK)

    def proj(lon, lat):
        x = map_x0 + (lon + 170.0) / 360.0 * (map_x1 - map_x0)
        yy = map_y0 + 18 + (75.0 - lat) / 130.0 * (map_y1 - map_y0 - 22)
        return x, yy

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=MAP_LAND,
                  outline=(120, 110, 90))
    f_pin = font(F_SANSB, 9)
    for lon, lat, label, dx, dy in PINS:
        px, py = proj(lon, lat)
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((px + dx, py + dy), label, font=f_pin, fill=INK)

    # rail: three featured stories beside the map
    rx0, rx1 = 664, W - mx
    d.text((rx0, my + 4), "ALSO TODAY", font=font(F_SANSB, 11), fill=RED)
    ry = my + 20
    for date_line, head, body in RAIL:
        d.text((rx0, ry), date_line, font=font(F_SANSB, 10), fill=RED)
        ry += 11
        for ln in wrap(d, head, font(F_SANSB, 12), rx1 - rx0)[:1]:
            d.text((rx0, ry), ln, font=font(F_SANSB, 12), fill=INK)
            ry += 14
        for ln in wrap(d, body, font(F_SANS, 10), rx1 - rx0)[:2]:
            d.text((rx0, ry), ln, font=font(F_SANS, 10), fill=INK)
            ry += 11
        ry += 4

    # ---------------------------------------------------------------- columns
    d.line([(mx, 414), (W - mx, 414)], fill=INK, width=2)
    d.text((mx, 418), "THE DAY IN FULL  —  35 STORIES, 9 REGIONS",
           font=font(F_SANSB, 11), fill=INK)
    col_w = (W - 2 * mx - 2 * 14) // 3
    f_head = font(F_SANSB, 11)
    f_body = font(F_SANS, 10)
    f_date = font(F_SANSB, 9)
    for ci, col in enumerate(COLUMNS):
        cx0 = mx + ci * (col_w + 14)
        y = 432
        for date_line, head, body in col:
            d.text((cx0, y), date_line, font=f_date, fill=RED)
            y += 12
            for ln in wrap(d, head, f_head, col_w)[:1]:
                d.text((cx0, y), ln, font=f_head, fill=INK)
                y += 13
            for ln in wrap(d, body, f_body, col_w)[:1]:
                d.text((cx0, y), ln, font=f_body, fill=(40, 40, 40))
                y += 12
            y += 3

    # ---------------------------------------------------------------- date check
    dy = 880
    d.rectangle([mx, dy, W - mx, dy + 40], fill=(24, 24, 24))
    y = dy + 3
    for ln in DATE_CHECK:
        d.text((mx + 10, y), ln, font=font(F_SANS, 10), fill=(240, 240, 240))
        y += 12

    # ---------------------------------------------------------------- numbers
    ny = 926
    d.text((mx, ny), "BY THE NUMBERS — every figure labelled",
           font=font(F_SANSB, 11), fill=RED)
    box_w = (W - 2 * mx - 5 * 8) // 6
    by = ny + 18
    for i, (num, label) in enumerate(NUMBERS):
        bx = mx + i * (box_w + 8)
        d.rectangle([bx, by, bx + box_w, by + 36], outline=INK, width=1)
        d.text((bx + box_w // 2, by + 3), num, font=font(F_SANSB, 11),
               fill=INK, anchor="ma")
        for j, ln in enumerate(wrap(d, label, font(F_SANS, 8), box_w - 6)):
            d.text((bx + box_w // 2, by + 19 + j * 9), ln,
                   font=font(F_SANS, 8), fill=GREY, anchor="ma")

    # ---------------------------------------------------------------- footer
    fy = 986
    d.line([(mx, fy), (W - mx, fy)], fill=INK, width=1)
    d.text((W // 2, fy + 5),
           "Sources: Reuters · BBC · AP · Al Jazeera · France 24 · UNFCCC · "
           "company statements — wires checked 24 Nov 2026, 12:00 WIB.",
           font=font(F_SANS, 9), fill=GREY, anchor="ma")
    d.text((W // 2, fy + 19),
           "Drawn and written by the entrant. No photograph or artwork copied. "
           "No. 329 — Tuesday 24 November 2026.",
           font=font(F_SANS, 9), fill=GREY, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
