#!/usr/bin/env python3
"""make.fun news-image-20261122 entry r7 — 'Sunday 22 November 2026'.
One broadsheet page: 38 dated stories, 7 regions, drawn with PIL.
Single source of truth: the STORIES list drives the region bar (must sum to 38).
Layout is budgeted top-down so the footer lands inside 1024px.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 24                      # outer margin
CW = W - 2 * M              # content width = 976
INK = (18, 18, 18)
RED = (178, 24, 24)
GREY = (110, 110, 110)
LIGHT = (238, 238, 236)
MIDGREY = (200, 200, 198)
PAPER = (255, 255, 255)
NIGHT = (16, 22, 44)
ORANGE = (232, 120, 30)
GOLD = (212, 160, 40)

CUTOFF = "08:45"

# ---------------------------------------------------------------- fonts
def font(name, size):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVu%s.ttf" % name,
        "/usr/share/fonts/dejavu/DejaVu%s.ttf" % name,
        "/usr/local/share/fonts/DejaVu%s.ttf" % name,
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()

F_KICK = font("Sans-Bold", 14)
F_HEAD = font("Serif-Bold", 48)
F_SUB = font("Serif", 19)
F_SEC = font("Sans-Bold", 12)
F_T = font("Sans-Bold", 15)
F_TL = font("Sans", 11)
F_N = font("Sans-Bold", 21)
F_NL = font("Sans", 10)
F_BAR = font("Sans-Bold", 11)
F_CITY = font("Sans-Bold", 12)
F_HERO = font("Serif-Bold", 16)
F_BODY = font("Sans", 12)
F_SRC = font("Sans", 10)
F_PIN = font("Sans-Bold", 9)
F_PHEAD = font("Sans-Bold", 12)
F_PBODY = font("Sans", 11)
F_LIST = font("Sans", 10)
F_LISTB = font("Sans-Bold", 10)
F_DC = font("Sans", 10)
F_FOOT = font("Sans", 10)

# ---------------------------------------------------------------- stories
# n, city, region, headline (short)
STORIES = [
    (1, "ANTALYA", "GLOBAL", "COP31 puts its final deal to the vote"),
    (2, "KYIV", "EUROPE", "Russia's overnight barrage: 148 drones, 3 missiles"),
    (3, "MANAMA", "MIDDLE EAST", "Iran claims Patriot radar strikes in Bahrain"),
    (4, "GULF OF FINLAND", "EUROPE", "Sparta II still burning"),
    (5, "HONG KONG", "ASIA", "Votes for its Election Committee"),
    (6, "WELLINGTON", "OCEANIA", "India declare on a record 720/9"),
    (7, "LAS VEGAS", "AMERICAS", "Verstappen WINS the Las Vegas GP"),
    (8, "GAZA", "MIDDLE EAST", "Hamas seeks urgent mediator talks"),
    (9, "KRYVYI RIH", "EUROPE", "Strike hits Zelenskyy's home city"),
    (10, "TEHRAN", "MIDDLE EAST", "Iran starts rationing electricity"),
    (11, "NEW DELHI", "ASIA", "Nepal's PM lands on first state visit"),
    (12, "BAYELSA", "AFRICA", "Boat toll rises to 26"),
    (13, "MERCURY ORBIT", "EUROPE", "BepiColombo enters Mercury orbit"),
    (14, "BRUSSELS", "EUROPE", "EU chiefs warn of hybrid warfare"),
    (15, "WASHINGTON", "AMERICAS", "Trump orders $12bn farm aid"),
    (16, "KANDAHAR", "ASIA", "Blast hits Taliban police HQ"),
    (17, "KINSHASA", "AFRICA", "Congo's army claims 30 rebels killed"),
    (18, "MEXICO CITY", "AMERICAS", "Cartel pact ends 200 years of clan rule"),
    (19, "SINGAPORE", "ASIA", "Airshow orders $6.6bn on day one"),
    (20, "JAKARTA", "ASIA", "Prabowo signs tax breaks for 12m workers"),
    (21, "BAGHDAD", "MIDDLE EAST", "Iraq counts ballots"),
    (22, "BERLIN", "EUROPE", "Merz vows aid for Ukraine"),
    (23, "SANTIAGO", "AMERICAS", "Jara wins Chile runoff"),
    (24, "NAIVASHA", "AFRICA", "Rift Valley quake hits Kenya"),
    (25, "TOKYO", "ASIA", "Japan's GDP shrinks 0.4%"),
    (26, "LONDON", "EUROPE", "King Charles opens Parliament"),
    (27, "WARSAW", "EUROPE", "Poland jails Russian agents"),
    (28, "BEIJING", "ASIA", "US and China cut tariffs"),
    (29, "LIMA", "AMERICAS", "Peru orders evacuation"),
    (30, "KABUL", "ASIA", "Afghans mark 4 years of Taliban rule"),
    (31, "DAKAR", "AFRICA", "Senegal bans single-use plastics"),
    (32, "CANBERRA", "OCEANIA", "Australia's PM signs pact with China"),
    (33, "ROME", "EUROPE", "Italy's Meloni backs Ukraine"),
    (34, "OSLO", "EUROPE", "Norway jails diplomat over spy case"),
    (35, "ACCRA", "AFRICA", "Ghana's cedi hits record low"),
    (36, "RIYADH", "MIDDLE EAST", "Saudi coalition downs three Houthi missiles"),
    (37, "COPENHAGEN", "EUROPE", "Denmark expels Russian attaché"),
    (38, "MANILA", "ASIA", "Chinese bomber turns back 170 km from capital"),
]
assert len(STORIES) == 38, len(STORIES)

REGIONS = ["EUROPE", "ASIA", "MIDDLE EAST", "AMERICAS", "AFRICA", "OCEANIA", "GLOBAL"]
REGION_COLORS = {
    "EUROPE": (18, 18, 18), "ASIA": (178, 24, 24), "MIDDLE EAST": (90, 90, 90),
    "AMERICAS": (150, 150, 148), "AFRICA": (60, 60, 60), "OCEANIA": (200, 200, 198),
    "GLOBAL": (212, 160, 40),
}
counts = {r: 0 for r in REGIONS}
for _, _, reg, _ in STORIES:
    counts[reg] += 1
assert sum(counts.values()) == 38, counts

UTC_SLOTS = [
    ("01:24", "BepiColombo enters Mercury orbit"),
    ("01:58", "Bitcoin $60,112"),
    ("03:00", "COP31 objections close"),
    ("04:00", "Vegas GP — Verstappen wins"),
    ("06:00", "COP31 vote opens (slips to 11:00)"),
    ("16:30", "Liverpool v United"),
    ("17:00", "ATP final, Turin"),
]
NUMBERS = [
    ("~200", "nations at COP31"),
    ("148", "drones overnight"),
    ("16", "crew off Sparta II"),
    ("720/9", "India's record"),
    ("856", "Hong Kong candidates"),
    ("26", "dead in Bayelsa"),
]

PANELS = {
    4: ("Russian ship burns a second day; all 16 crew safe; Finland says Ukraine likely behind the hit.", "Reuters"),
    5: ("856 candidates contest 723 seats; polls 9am–6pm.", "Reuters"),
    6: ("Pant 128, Rahul 136; highest total ever in New Zealand.", "Reuters"),
    7: ("Beats Norris and Piastri; Russell hits the wall late, finishes ninth.", "AP"),
    8: ("After an aid strike on Saturday, Hamas calls for a meeting on Sunday.", "Al Jazeera"),
    9: ("Double-tap overnight: two killed, a boy of 7 and a paramedic of 20, and 60 hurt.", "Kyiv Independent"),
    10: ("Two-hour daily cuts begin from Sunday as gas output falls.", "AP"),
    11: ("Balendra Shah arrives; talks with Modi on Monday.", "Reuters"),
    12: ("A mourners' boat capsized on Friday; the toll is reported on Sunday as recovery goes on.", "RIA"),
    13: ("Burn began 18:24 GMT Sat — 01:24 WIB Sun; ESA confirms the orbit.", "ESA"),
}
HEROES = {
    1: ("COP31, ANTALYA",
        "COP31 puts its final deal to the vote",
        "Ten-page final text goes to a closing plenary after objections pushed the vote to 11am. No fossil-fuel mention; 35% power by 2035; 1.5°C miss admitted.",
        "Reuters"),
    2: ("UKRAINE, KYIV",
        "Russia's overnight barrage: 148 drones, 3 missiles",
        "Kyiv counts 148 drones and three ballistic missiles fired overnight; in Kryvyi Rih a double-tap strike kills two and hurts 60.",
        "AP, Kyiv Independent"),
    3: ("BAHRAIN, MANAMA",
        "Iran claims Patriot radar strikes in Bahrain",
        "Tehran says missiles and drones hit US radars at Al-Riffa and Awali; Bahrain says it intercepted the attacks; a facility burned, no casualties.",
        "Al Jazeera, Reuters"),
}

# approx lat/lon for map pins 14-38
PINS = {
    14: (50.85, 4.35), 15: (38.9, -77.0), 16: (31.6, 65.8), 17: (-4.3, 15.3),
    18: (19.4, -99.1), 19: (1.35, 103.8), 20: (-6.2, 106.8), 21: (33.3, 44.4),
    22: (52.5, 13.4), 23: (-33.4, -70.7), 24: (-0.7, 36.4), 25: (35.7, 139.7),
    26: (51.5, -0.1), 27: (52.2, 21.0), 28: (39.9, 116.4), 29: (-12.0, -77.0),
    30: (34.5, 69.2), 31: (14.7, -17.4), 32: (-35.3, 149.1), 33: (41.9, 12.5),
    34: (59.9, 10.7), 35: (5.6, -0.2), 36: (24.7, 46.7), 37: (55.7, 12.6),
    38: (14.6, 121.0),
}
# manual nudges (px) so crowded pins do not overlap: Europe + Gulf + SE Asia
PIN_OFF = {
    14: (-16, 4), 22: (12, 10), 26: (-18, -10), 27: (16, -4), 33: (-2, 14),
    34: (-10, -16), 37: (14, -12), 16: (10, -8), 30: (-12, 6), 21: (12, -8),
    36: (-10, 10), 28: (6, -6), 38: (-4, 6), 19: (10, -8), 20: (-10, 6),
}

# ---------------------------------------------------------------- helpers
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def tw(text, fnt):
    return d.textlength(text, font=fnt)

def wrap(text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(t, fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def fit(text, fnt, width):
    """Shorten with an ellipsis so text fits width on one line."""
    if tw(text, fnt) <= width:
        return text
    while text and tw(text + "…", fnt) > width:
        text = text[:-1].rstrip()
    return text + "…"

def rule(y, color=INK, wdt=2):
    d.line([(M, y), (W - M, y)], fill=color, width=wdt)

def center(text, fnt, y, color=INK):
    d.text(((W - tw(text, fnt)) / 2, y), text, font=fnt, fill=color)

def flame(x, y, s, color=ORANGE):
    d.polygon([(x, y), (x + s * 0.5, y - s), (x + s, y)], fill=color)
    d.polygon([(x + s * 0.25, y), (x + s * 0.5, y - s * 0.55),
               (x + s * 0.75, y)], fill=(232, 60, 20))

# ---------------------------------------------------------------- header
y = 14
center("THE WORLD IN ONE DAY · 38 STORIES · 7 REGIONS · EVERY ONE DATED SUNDAY 22 NOVEMBER 2026",
       F_KICK, y, RED)
y = 32
center("Sunday 22 November 2026", F_HEAD, y)
y = 90
rule(y, INK, 3)
y = 96
sub = ("COP31 puts its final deal to the vote · Russia fires 148 drones at Ukraine · "
       "Iran claims Patriot radar strikes in Bahrain")
for ln in wrap(sub, F_SUB, CW):
    center(ln, F_SUB, y)
    y += 22
y += 2
rule(y, INK, 1)

# ---------------------------------------------------------------- UTC strip
y += 6
d.text((M, y), "THE DAY IN UTC", font=F_SEC, fill=RED)
y += 13
slot_w = (CW - 6 * 6) / 7
for i, (t, label) in enumerate(UTC_SLOTS):
    x0 = M + i * (slot_w + 6)
    d.rectangle([x0, y, x0 + slot_w, y + 44], outline=MIDGREY, width=1)
    d.text((x0 + 6, y + 3), t, font=F_T, fill=RED)
    for j, ln in enumerate(wrap(label, F_TL, slot_w - 12)):
        d.text((x0 + 6, y + 21 + j * 12), ln, font=F_TL, fill=INK)
y += 50

# ---------------------------------------------------------------- number strip
d.text((M, y), "THE DAY IN NUMBERS", font=F_SEC, fill=RED)
y += 13
num_w = (CW - 5 * 6) / 6
for i, (num, label) in enumerate(NUMBERS):
    x0 = M + i * (num_w + 6)
    d.rectangle([x0, y, x0 + num_w, y + 38], fill=LIGHT, outline=MIDGREY, width=1)
    d.text((x0 + 8, y + 2), num, font=F_N, fill=INK)
    d.text((x0 + 8, y + 24), label, font=F_NL, fill=GREY)
y += 46

# ---------------------------------------------------------------- region bar
d.text((M, y), "WHERE THE NEWS HAPPENED — 38 STORIES", font=F_SEC, fill=RED)
y += 13
bx, bw, bh = M, CW, 14
x = bx
for r in REGIONS:
    seg = bw * counts[r] / 38
    d.rectangle([x, y, x + seg, y + bh], fill=REGION_COLORS[r])
    x += seg
y += bh + 4
lx = M
for r in REGIONS:
    lab = "%s %d" % (r, counts[r])
    d.rectangle([lx, y + 2, lx + 9, y + 11], fill=REGION_COLORS[r])
    d.text((lx + 12, y), lab, font=F_BAR, fill=INK)
    lx += tw(lab, F_BAR) + 26
y += 18

# ---------------------------------------------------------------- heroes
def draw_cop31(x0, y0, wdt, hgt):
    d.rectangle([x0, y0, x0 + wdt, y0 + hgt], fill=(235, 240, 245))
    cx, cy, r = x0 + 58, y0 + hgt // 2 + 2, 38
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 130, 180), outline=INK, width=2)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=(255, 255, 255), width=1)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(255, 255, 255), width=1)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 180, 360, fill=(255, 255, 255), width=1)
    dx = x0 + 106
    d.rectangle([dx, y0 + 16, dx + 72, y0 + hgt - 14], fill=PAPER, outline=INK, width=1)
    d.text((dx + 6, y0 + 20), "FINAL TEXT", font=F_SRC, fill=RED)
    for k in range(5):
        d.line([(dx + 6, y0 + 36 + k * 8), (dx + 66, y0 + 36 + k * 8)], fill=GREY, width=1)
    tx = x0 + 196
    d.rounded_rectangle([tx, y0 + 12, tx + 15, y0 + hgt - 26], radius=7, outline=INK, width=2, fill=PAPER)
    d.ellipse([tx - 3, y0 + hgt - 34, tx + 18, y0 + hgt - 14], fill=RED, outline=INK, width=1)
    d.rectangle([tx + 5, y0 + 26, tx + 10, y0 + hgt - 26], fill=RED)
    ccx, ccy, cr = x0 + wdt - 34, y0 + 30, 20
    d.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=PAPER, outline=INK, width=2)
    d.line([(ccx, ccy), (ccx, ccy - cr + 5)], fill=INK, width=2)
    d.line([(ccx, ccy), (ccx - cr + 7, ccy)], fill=INK, width=2)
    d.text((ccx - 13, ccy + cr + 2), "11:00", font=F_SRC, fill=INK)

def draw_ukraine(x0, y0, wdt, hgt):
    d.rectangle([x0, y0, x0 + wdt, y0 + hgt], fill=NIGHT)
    for sx, sy in [(18, 12), (52, 26), (96, 9), (150, 20), (210, 10), (260, 24), (300, 12)]:
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + 2, y0 + sy + 2], fill=(255, 255, 255))
    for ty, tx0, tx1 in [(30, 10, 130), (46, 90, 230), (60, 30, 170)]:
        d.line([(x0 + tx0, y0 + ty), (x0 + tx1, y0 + ty - 10)], fill=(255, 220, 120), width=1)
        d.ellipse([x0 + tx1 - 3, y0 + ty - 13, x0 + tx1 + 3, y0 + ty - 7], fill=(255, 220, 120))
    base = y0 + hgt
    for bx0, bw_, bh_ in [(8, 34, 30), (48, 26, 42), (80, 40, 26), (126, 30, 46), (162, 36, 32),
                          (204, 28, 40), (238, 34, 26), (278, 30, 38)]:
        d.rectangle([x0 + bx0, base - bh_, x0 + bx0 + bw_, base], fill=(8, 12, 26))
        d.rectangle([x0 + bx0 + 6, base - bh_ - 5, x0 + bx0 + bw_ - 6, base - bh_], fill=(8, 12, 26))
    flame(x0 + 52, base, 15)
    flame(x0 + 168, base, 18)
    flame(x0 + 246, base, 13)

def draw_bahrain(x0, y0, wdt, hgt):
    d.rectangle([x0, y0, x0 + wdt, y0 + hgt], fill=NIGHT)
    rx, ry = x0 + 66, y0 + hgt - 18
    for rr in (18, 32, 46, 56):
        d.arc([rx - rr, ry - rr, rx + rr, ry + rr], 180, 360, fill=(120, 200, 120), width=1)
    d.line([(rx, ry), (rx + 40, ry - 40)], fill=(120, 200, 120), width=2)
    d.ellipse([rx - 4, ry - 4, rx + 4, ry + 4], fill=(120, 200, 120))
    base = y0 + hgt
    for bx0, bw_, bh_ in [(150, 40, 34), (196, 30, 48), (232, 44, 28), (282, 26, 40)]:
        d.rectangle([x0 + bx0, base - bh_, x0 + bx0 + bw_, base], fill=(8, 12, 26))
    flame(x0 + 200, base, 20)
    flame(x0 + 236, base, 13)
    for sx, sy in [(250, 16), (280, 28), (300, 10)]:
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3], fill=(255, 120, 60))

hero_y = y + 4
hero_w = (CW - 2 * 12) / 3
hero_h = 78
draw_cop31(M, hero_y, hero_w, hero_h)
draw_ukraine(M + hero_w + 12, hero_y, hero_w, hero_h)
draw_bahrain(M + 2 * (hero_w + 12), hero_y, hero_w, hero_h)
ty = hero_y + hero_h + 6
hero_end = ty
for i, (city, head, body, src) in enumerate(HEROES.values()):
    x0 = M + i * (hero_w + 12)
    d.text((x0, ty), "%d · %s" % (i + 1, city), font=F_CITY, fill=RED)
    yy = ty + 14
    for ln in wrap(head, F_HERO, hero_w):
        d.text((x0, yy), ln, font=F_HERO, fill=INK)
        yy += 19
    for ln in wrap(body, F_BODY, hero_w):
        d.text((x0, yy), ln, font=F_BODY, fill=INK)
        yy += 14
    d.text((x0, yy + 2), "Source: " + src, font=F_SRC, fill=GREY)
    hero_end = max(hero_end, yy + 2 + 12)
y = hero_end + 8

# ---------------------------------------------------------------- panels 4-13
rule(y, INK, 1)
y += 6
d.text((M, y), "THE REST OF THE DAY — 4–13", font=F_SEC, fill=RED)
y += 13
panel_w = (CW - 12) / 2
panel_h = 37
for row in range(5):
    for col in range(2):
        n = 4 + row * 2 + col
        _, city, _, head = STORIES[n - 1]
        body, src = PANELS[n]
        x0 = M + col * (panel_w + 12)
        yy = y + row * panel_h
        d.rectangle([x0, yy + 1, x0 + 22, yy + 23], fill=INK)
        d.text((x0 + 6, yy + 4), str(n), font=F_LISTB, fill=PAPER)
        d.text((x0 + 28, yy), fit("%s — %s" % (city, head), F_PHEAD, panel_w - 28),
               font=F_PHEAD, fill=INK)
        bl = body + "  [" + src + "]"
        blines = wrap(bl, F_PBODY, panel_w - 28)
        d.text((x0 + 28, yy + 14), blines[0] if blines else "", font=F_PBODY, fill=INK)
        if len(blines) > 1:
            d.text((x0 + 28, yy + 26), blines[1], font=F_PBODY, fill=INK)
y += 5 * panel_h + 4

# ---------------------------------------------------------------- map + list 14-38
rule(y, INK, 1)
y += 6
d.text((M, y), "ON THE MAP — 14–38", font=F_SEC, fill=RED)
y += 13
map_y = y
map_h = 50
d.rectangle([M, map_y, W - M, map_y + map_h], fill=(240, 243, 246), outline=MIDGREY, width=1)

def proj(lon, lat):
    fx = (lon + 170) / 360.0
    fy = (75 - lat) / 130.0
    return (M + 8 + fx * (CW - 16), map_y + 4 + fy * (map_h - 8))

CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 69), (-80, 62), (-75, 45), (-80, 32),
     (-95, 20), (-105, 22), (-118, 34), (-125, 49), (-150, 60)],
    [(-78, 8), (-60, 5), (-50, -5), (-40, -15), (-55, -30), (-70, -40),
     (-73, -50), (-70, -20), (-80, -5)],
    [(-10, 36), (-9, 43), (0, 48), (5, 58), (18, 56), (28, 60), (30, 55),
     (20, 45), (12, 42), (3, 38)],
    [(-17, 15), (-10, 30), (10, 37), (30, 32), (35, 28), (43, 12), (51, 11),
     (40, -5), (35, -25), (20, -35), (12, -18), (-5, 5)],
    [(40, 55), (60, 70), (90, 75), (130, 72), (160, 65), (178, 66), (160, 60),
     (140, 40), (122, 30), (105, 10), (100, 8), (80, 8), (60, 25), (45, 30)],
    [(114, -22), (130, -12), (142, -11), (150, -22), (153, -27), (146, -39),
     (140, -38), (129, -32), (115, -33)],
]
for poly in CONTINENTS:
    pts = [proj(lon, lat) for lon, lat in poly]
    d.polygon(pts, fill=(214, 222, 228), outline=(150, 160, 170))
for n, (lat, lon) in PINS.items():
    px, py = proj(lon, lat)
    ox, oy = PIN_OFF.get(n, (0, 0))
    px, py = px + ox, py + oy
    d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED, outline=PAPER, width=1)
    num = str(n)
    d.text((px - tw(num, F_PIN) / 2, py - 5), num, font=F_PIN, fill=PAPER)
y = map_y + map_h + 6

# list in 3 columns, one fitted line per story
list_items = STORIES[13:]
col_w = (CW - 2 * 10) / 3
for idx, (n, city, _, head) in enumerate(list_items):
    col = idx // 9
    row = idx % 9
    x0 = M + col * (col_w + 10)
    yy = y + row * 12.5
    d.text((x0, yy), "%d" % n, font=F_LISTB, fill=RED)
    d.text((x0 + 18, yy), fit("%s — %s" % (city, head), F_LIST, col_w - 18),
           font=F_LIST, fill=INK)
y += 9 * 12.5 + 4

# ---------------------------------------------------------------- date check
rule(y, INK, 1)
y += 6
d.text((M, y), "DATE CHECK", font=F_SEC, fill=RED)
y += 13
dc = ("Wires read up to %s UTC, Sunday 22 November 2026. Left out on purpose, first reported "
      "Friday or Saturday, so NOT shown as Sunday's news: Peru quake (Sat 21 Nov) · Russia's "
      "400-drone, 110-missile barrage (Thursday night into Friday) · the Sinaloa kingpin capture "
      "(Friday night) · the EU–Indonesia signing (Saturday) · the Basra power-plant fire "
      "(Saturday) · Bolsonaro's ICU admission (Saturday) · Cyclone Akvan's landfall (Friday) · "
      "the Sparta II hit (Saturday). Not yet happened: COP31's final adoption, the ATP champion, "
      "the Liverpool–United result. Every story here happened, or was first reported, on Sunday "
      "22 November 2026 in at least one time zone. Officials' counts and claims are attributed."
      % CUTOFF)
for ln in wrap(dc, F_DC, CW):
    d.text((M, y), ln, font=F_DC, fill=INK)
    y += 13
y += 4
rule(y, INK, 1)
y += 6
center("Every story here happened, or was first reported, on Sunday 22 November 2026 in at least "
       "one time zone. Sources named beside each story · original drawings.", F_FOOT, y, GREY)
y += 14
print("final y =", y, "| bar sums to", sum(counts.values()))
assert y <= 1024, y

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
