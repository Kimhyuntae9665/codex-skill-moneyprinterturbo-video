from __future__ import annotations

import argparse
from functools import lru_cache
import json
import math
from pathlib import Path
import shutil
import subprocess
import urllib.request

from PIL import Image, ImageDraw, ImageFont


W, H, FPS = 720, 1280, 30
BOUNDARIES = [0.0, 4.0, 7.45, 10.95, 15.15, 19.75, 23.95, 29.05, 33.30, 38.35, 41.55, 45.75, 50.00, 54.00, 58.50]
SCENES = [BOUNDARIES[i + 1] - BOUNDARIES[i] for i in range(len(BOUNDARIES) - 1)]
TOTAL = BOUNDARIES[-1]

BG = "#F3EFE7"
PAPER = "#FFFDF8"
INK = "#171A1D"
MUTED = "#697177"
GRID = "#E5DDD0"
RED = "#E23A2A"
RED_DARK = "#9A241B"
GOLD = "#FFC72C"
GOLD_DARK = "#B98200"
BLUE = "#2477B3"
BLUE_DARK = "#174E76"
GREEN = "#16886D"
TEAL = "#183F48"
WHITE = "#FFFFFF"
FONT_DIR = Path(__file__).resolve().parents[3] / "assets" / "fonts"

TITLES = [
    ("PRICE DIVERGENCE", "기술주가 오를 때, MCD는 하락"),
    ("CONDITIONAL IDEA", "몰빵이 아닌 분할매수 후보"),
    ("GLOBAL FRANCHISE", "4만 6천 매장의 네트워크"),
    ("REAL ESTATE ENGINE", "토지·건물에서 반복 현금흐름"),
    ("CASH TO OWNERS", "배당과 순현금 자사주매입"),
    ("SHAREHOLDER RETURN", "3.9% 현금환원 + 50년 인상"),
    ("YIELD SIGNAL", "현재 2.79% · 최근 80개월 2위"),
    ("HISTORY CHECK", "높지만 역대급 바닥은 아니다"),
    ("DIFFERENT RHYTHM", "MCD beta 0.42 · QQQ 1.25"),
    ("PORTFOLIO ROLE", "기술주와 덜 겹치는 현금흐름"),
    ("RISK CHECK", "부채와 미국 객수 둔화"),
    ("ENTRY 01", "260달러대에서 작게 시작"),
    ("ENTRY 02", "245~250달러 · 배당률 약 3%"),
    ("DECISION RULE", "객수 회복 뒤 확대 · 훼손 시 취소"),
]


@lru_cache(maxsize=128)
def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / "NotoSansKR-Bold.ttf"), size=size)


def clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def ease(v: float) -> float:
    v = clamp(v)
    return 1.0 - (1.0 - v) ** 3


def smooth(v: float) -> float:
    v = clamp(v)
    return v * v * (3.0 - 2.0 * v)


def back(v: float) -> float:
    v = clamp(v)
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (v - 1) ** 3 + c1 * (v - 1) ** 2


def phase(t: float, start: float, end: float, easing=ease) -> float:
    return easing((t - start) / max(0.001, end - start))


def rr(draw: ImageDraw.ImageDraw, box, radius: int, fill: str, outline: str | None = None, width: int = 1) -> None:
    draw.rounded_rectangle(tuple(int(v) for v in box), radius=radius, fill=fill, outline=outline, width=width)


def txt(draw: ImageDraw.ImageDraw, xy, value: str, size: int, fill: str = INK, anchor: str = "la", max_width: int | None = None) -> None:
    use = size
    if max_width:
        while use > 12:
            box = draw.multiline_textbbox((0, 0), value, font=font(use), spacing=4, align="left")
            if box[2] - box[0] <= max_width:
                break
            use -= 1
    if "\n" in value:
        draw.multiline_text(xy, value, font=font(use), fill=fill, anchor=anchor, spacing=4, align="center" if anchor[0] == "m" else "left")
    else:
        draw.text(xy, value, font=font(use), fill=fill, anchor=anchor)


def center(draw: ImageDraw.ImageDraw, y: int, value: str, size: int, fill: str = INK) -> None:
    txt(draw, (W // 2, y), value, size, fill, "ma", 620)


def alpha_rr(image: Image.Image, box, radius: int, fill, outline=None, width: int = 1) -> None:
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(tuple(int(v) for v in box), radius=radius, fill=fill, outline=outline, width=width)
    image.paste(layer, (0, 0), layer)


def arrow(draw: ImageDraw.ImageDraw, a, b, color: str, width: int = 6, head: int = 14) -> None:
    a = tuple(int(v) for v in a)
    b = tuple(int(v) for v in b)
    draw.line((a, b), fill=color, width=width)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    p1 = (b[0] - head * math.cos(ang - 0.55), b[1] - head * math.sin(ang - 0.55))
    p2 = (b[0] - head * math.cos(ang + 0.55), b[1] - head * math.sin(ang + 0.55))
    draw.polygon((b, p1, p2), fill=color)


def base_frame(global_t: float, scene_index: int) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)
    offset = int((global_t * 11) % 52)
    for x in range(-52 + offset, W + 52, 52):
        draw.line((x, 78, x, 995), fill=GRID, width=1)
    for y in range(100 - offset, 1000, 52):
        draw.line((0, y, W, y), fill=GRID, width=1)
    draw.rectangle((0, 0, W, 74), fill=INK)
    txt(draw, (34, 37), "MCD · INVESTMENT CASE", 17, WHITE, "lm")
    txt(draw, (683, 37), "DATA 2026.08.31", 12, "#CED2D4", "rm")
    # The caption lane is a permanent reserved rectangle. No scene object may enter it.
    alpha_rr(image, (38, 1002, 682, 1182), 24, (23, 26, 29, 226))
    draw = ImageDraw.Draw(image)
    txt(draw, (59, 1028), f"{scene_index + 1:02d} / 14", 12, "#AEB6BA")
    return image, draw


def scene_title(draw: ImageDraw.ImageDraw, t: float, eyebrow: str, title: str) -> None:
    p = back(phase(t, 0.02, 0.42))
    x = int(46 + 54 * (1 - p))
    txt(draw, (x, 112), eyebrow, 16, RED)
    txt(draw, (x, 146), title, 33, INK, "la", 624)
    line = phase(t, 0.15, 0.60)
    draw.rounded_rectangle((46, 211, 46 + int(120 * line), 218), radius=3, fill=GOLD)


def apply_content_camera(image: Image.Image, scene_index: int, local_t: float) -> None:
    """Apply a bounded continuous camera move only to the evidence stage.

    The header, title, source rail and caption lane stay fixed, so added motion
    cannot reintroduce the layout drift that the user rejected in v6/v7.
    """
    top, bottom = 224, 948
    region = image.crop((0, top, W, bottom))
    shot_p = smooth(local_t / SCENES[scene_index])
    if scene_index % 4 == 1:
        zoom = 1.044 - .030 * shot_p
    else:
        zoom = 1.012 + .032 * shot_p
    rw, rh = int(W * zoom), int((bottom-top) * zoom)
    moved = region.resize((rw, rh), Image.Resampling.BICUBIC)
    span_x, span_y = rw-W, rh-(bottom-top)
    direction = 1 if scene_index % 2 == 0 else -1
    pan = direction * math.sin(shot_p * math.pi) * min(7, span_x*.25)
    crop_x = int(span_x*.5 + pan)
    crop_y = int(span_y*(.34 + .24*shot_p))
    image.paste(moved.crop((crop_x,crop_y,crop_x+W,crop_y+(bottom-top))),(0,top))


def source(draw: ImageDraw.ImageDraw, value: str) -> None:
    txt(draw, (48, 968), value, 12, MUTED, "la", 620)


def iso_box(draw: ImageDraw.ImageDraw, x: float, y: float, w: float, h: float, d: float, front: str, side: str, top: str) -> None:
    x, y, w, h, d = map(int, (x, y, w, h, d))
    draw.polygon(((x, y), (x + d, y - d), (x + w + d, y - d), (x + w, y)), fill=top)
    draw.polygon(((x + w, y), (x + w + d, y - d), (x + w + d, y + h - d), (x + w, y + h)), fill=side)
    draw.rectangle((x, y, x + w, y + h), fill=front)


def golden_arches(draw: ImageDraw.ImageDraw, cx: float, baseline: float, width: float, height: float, stroke: int, reveal: float = 1.0) -> None:
    left, right = [], []
    for i in range(30):
        u = i / 29
        left.append((cx - width / 2 + width / 2 * u, baseline - height * 4 * u * (1 - u)))
        right.append((cx + width / 2 * u, baseline - height * 4 * u * (1 - u)))
    n = max(2, int(30 * clamp(reveal)))
    draw.line(left[:n], fill=GOLD, width=stroke, joint="curve")
    draw.line(right[:n], fill=GOLD, width=stroke, joint="curve")


def store_model(draw: ImageDraw.ImageDraw, cx: float, base: float, scale: float, build: float = 1.0, cars: int = 0) -> None:
    p_land = phase(build, 0.00, 0.28)
    p_body = phase(build, 0.18, 0.70)
    p_roof = phase(build, 0.55, 1.00)
    s = scale
    if p_land:
        draw.polygon(((cx - 136*s, base + 85*s), (cx + 122*s, base + 85*s), (cx + 174*s, base + 42*s), (cx - 83*s, base + 42*s)), fill="#C7B89E")
        draw.line((cx - 80*s, base + 43*s, cx + 171*s, base + 43*s), fill="#8D806D", width=max(2, int(3*s)))
    if p_body:
        bh = 160 * s * p_body
        iso_box(draw, cx - 94*s, base + 38*s - bh, 188*s, bh, 40*s, "#EDE8DE", "#BBB4A8", PAPER)
        wy = base + 4*s
        draw.rectangle((cx - 70*s, wy - 28*s, cx - 16*s, wy + 27*s), fill="#365762")
        draw.rectangle((cx + 3*s, wy - 28*s, cx + 68*s, wy + 27*s), fill="#365762")
    if p_roof:
        ry = base - 123*s*p_body
        draw.polygon(((cx - 106*s, ry), (cx + 108*s, ry), (cx + 150*s, ry - 37*s), (cx - 65*s, ry - 37*s)), fill=RED)
        draw.rectangle((cx - 106*s, ry, cx + 108*s, ry + 13*s), fill=RED_DARK)
        golden_arches(draw, cx + 17*s, ry - 7*s, 78*s, 69*s, max(3, int(8*s)), p_roof)
    for i in range(cars):
        q = back(phase(build, 0.38 + i*.09, 0.78 + i*.09))
        x = cx - 116*s + i*72*s
        y = base + (112 + 24*(1-q))*s
        rr(draw, (x, y, x+50*s, y+21*s), max(3, int(5*s)), BLUE if i % 2 else RED)
        draw.ellipse((x+7*s, y+15*s, x+18*s, y+26*s), fill=INK)
        draw.ellipse((x+34*s, y+15*s, x+45*s, y+26*s), fill=INK)


@lru_cache(maxsize=1)
def world_rings() -> tuple[tuple[tuple[float, float], ...], ...]:
    url = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_land.geojson"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "MPT-MCD-v8"})
        with urllib.request.urlopen(req, timeout=15) as response:
            payload = json.load(response)
        rings = []
        for feature in payload.get("features", []):
            geometry = feature.get("geometry") or {}
            coords = geometry.get("coordinates") or []
            polygons = [coords] if geometry.get("type") == "Polygon" else coords
            for polygon in polygons:
                if not polygon:
                    continue
                outer = polygon[0]
                stride = max(1, len(outer) // 240)
                ring = tuple((float(lon), float(lat)) for lon, lat, *_ in outer[::stride])
                if len(ring) >= 3:
                    rings.append(ring)
        if rings:
            return tuple(rings)
    except Exception:
        pass
    return (
        ((-168, 70), (-135, 72), (-103, 55), (-83, 25), (-112, 16), (-137, 42)),
        ((-82, 12), (-63, 7), (-45, -23), (-68, -55), (-80, -15)),
        ((-12, 70), (42, 68), (60, 45), (22, 34), (-10, 46)),
        ((-18, 35), (28, 37), (51, 8), (31, -35), (5, -25), (-16, 8)),
        ((42, 67), (105, 75), (172, 55), (154, 14), (95, 8), (60, 35)),
        ((112, -12), (154, -10), (168, -40), (132, -47)),
    )


def draw_hook(draw: ImageDraw.ImageDraw, t: float) -> None:
    p = phase(t, 0.10, 1.60)
    x0, x1, y0, y1 = 68, 652, 322, 745
    rr(draw, (54, 278, 666, 785), 28, PAPER, "#D4CDC1", 2)
    for k in range(5):
        y = 342 + k*83
        draw.line((x0, y, x1, y), fill="#DED8CE", width=1)
    blue_pts, red_pts = [], []
    for i in range(90):
        u = i / 89
        x = x0 + (x1-x0)*u
        blue_pts.append((x, 620 - 225*u + 20*math.sin(i*.27)))
        red_pts.append((x, 420 + 215*u + 21*math.sin(i*.23+1.1)))
    n = max(2, int(90*p))
    draw.line(blue_pts[:n], fill=BLUE, width=7, joint="curve")
    draw.line(red_pts[:n], fill=RED, width=8, joint="curve")
    if p > .68:
        q = back(phase(t, 1.0, 1.75))
        rr(draw, (76, 807, 319, 920), 22, "#E7F0F6")
        txt(draw, (99, 839), "QQQ", 17, BLUE)
        txt(draw, (287, 866), f"+{18.1*q:.1f}%", 34, BLUE, "ra")
        rr(draw, (400, 807, 644, 920), 22, "#FCE5E1")
        txt(draw, (423, 839), "MCD", 17, RED)
        txt(draw, (612, 866), f"-{20.3*q:.1f}%", 34, RED, "ra")
    source(draw, "Yahoo adjusted close · 6개월")


def draw_candidate(draw: ImageDraw.ImageDraw, t: float) -> None:
    store_model(draw, 360, 585, 1.16, phase(t, 0.0, 1.45), cars=3)
    gate_p = phase(t, 1.20, 2.35)
    draw.arc((102, 728, 618, 908), 190, 190 + int(160*gate_p), fill=GOLD, width=10)
    cards = (("1차", RED), ("2차", GOLD_DARK), ("확인", GREEN))
    for i, (label, color) in enumerate(cards):
        q = back(phase(t, .65+i*.30, 1.38+i*.30))
        x = 69 + i*198
        y = int(825 + 55*(1-q))
        rr(draw, (x, y, x+172, y+76), 19, color)
        txt(draw, (x+86, y+38), label, 25, WHITE, "mm")
    center(draw, 938, "한 번에 사지 않는 구조", 20, MUTED)


def draw_network(draw: ImageDraw.ImageDraw, t: float) -> None:
    # Flat vector projection: the map, metric and captions occupy separate lanes.
    left, top, right, bottom = 70, 300, 650, 716
    rr(draw, (54, 272, 666, 746), 30, TEAL)
    def project(lon: float, lat: float) -> tuple[float, float]:
        return (left + (lon+180)/360*(right-left), top + (90-lat)/180*(bottom-top))
    for ring in world_rings():
        pts = [project(lon, lat) for lon, lat in ring if -88 < lat < 88]
        if len(pts) >= 3:
            draw.polygon(pts, fill="#D7D0BB", outline="#B6AD96")
    for lon in (-120, -60, 0, 60, 120):
        x, _ = project(lon, 0)
        draw.line((x, top+14, x, bottom-14), fill="#31565E", width=1)
    for lat in (-45, 0, 45):
        _, y = project(0, lat)
        draw.line((left+10, y, right-10, y), fill="#31565E", width=1)
    hub = project(-87.6, 41.9)
    nodes = ((-118,34),(-74,41),(-46,-23),(-.1,51.5),(28,-26),(55,25),(121,31),(139,35),(151,-34))
    for i, (lon, lat) in enumerate(nodes):
        q = back(phase(t, .20+i*.15, .72+i*.15))
        x, y = project(lon, lat)
        if q > 0:
            draw.line((hub[0],hub[1],x,y), fill="#D9A925", width=2)
            r = 5 + 5*q + 2*math.sin(t*5+i)
            draw.ellipse((x-r,y-r,x+r,y+r), fill=RED, outline=WHITE, width=1)
    hr = 12*back(phase(t,.05,.55))
    draw.ellipse((hub[0]-hr,hub[1]-hr,hub[0]+hr,hub[1]+hr),fill=GOLD,outline=WHITE,width=2)
    count = int(46028 * phase(t, .35, 2.70))
    txt(draw, (70, 785), f"{count:,}", 64, INK)
    txt(draw, (72, 875), "RESTAURANTS", 14, MUTED)
    rr(draw, (435, 812, 650, 912), 22, PAPER, "#D0C8BA", 2)
    txt(draw, (542, 842), "약 95%", 34, RED, "mm")
    txt(draw, (542, 885), "FRANCHISED", 14, MUTED, "mm")
    source(draw, "McDonald's Q2 2026 Form 10-Q · nodes are regional schematic")


def draw_property(draw: ImageDraw.ImageDraw, t: float) -> None:
    # An exploded architectural stack proves the model before cash-flow arrows appear.
    q1 = back(phase(t, 0.00, .85))
    q2 = back(phase(t, .45, 1.35))
    q3 = back(phase(t, .95, 1.85))
    cx = 278
    land_y = 792 - 38*q1
    draw.polygon(((105,land_y),(390,land_y),(455,land_y-55),(170,land_y-55)),fill="#C6A777",outline="#816943")
    txt(draw,(118,land_y+32),"LAND",15,GOLD_DARK)
    if q2:
        store_model(draw,cx,620-52*q2,.72,q2,cars=0)
        txt(draw,(118,596),"BUILDING",15,RED)
    if q3:
        y = 308 + 45*(1-q3)
        rr(draw,(134,y,420,y+122),15,"#C9D0D2","#68777B",2)
        draw.rectangle((153,y+18,402,y+48),fill="#4D5C61")
        for x in (195,270,345):
            draw.ellipse((x-23,y+20,x+23,y+45),fill="#20272A")
        rr(draw,(155,y+62,260,y+106),7,"#9CA7AA")
        rr(draw,(280,y+62,399,y+106),7,"#E4E8E8")
        txt(draw,(118,y-24),"EQUIPMENT",15,BLUE)
    flow = phase(t,1.80,3.25)
    if flow:
        arrow(draw,(455,495),(548,495),GOLD_DARK,6)
        arrow(draw,(455,665),(548,665),BLUE,6)
        rr(draw,(532,434,668,548),20,"#FFF1C9",GOLD_DARK,2)
        txt(draw,(600,471),"RENT",16,GOLD_DARK,"mm")
        txt(draw,(600,516),f"${5.26*flow:.2f}B",28,INK,"mm")
        rr(draw,(532,604,668,718),20,"#E5F0F7",BLUE,2)
        txt(draw,(600,641),"ROYALTY",16,BLUE,"mm")
        txt(draw,(600,686),f"${3.10*flow:.2f}B",28,INK,"mm")
    source(draw,"Traditional franchise structure · H1 2026")


def draw_return(draw: ImageDraw.ImageDraw, t: float) -> None:
    p = phase(t, .05, .75)
    rr(draw,(242,278,478,390),22,INK)
    center(draw,323,"FREE CASH FLOW",18,WHITE)
    shaft_y = 398 + 38*math.sin(min(1,p)*math.pi)
    arrow(draw,(360,shaft_y),(188,540),GOLD_DARK,7)
    arrow(draw,(360,shaft_y),(532,540),RED,7)
    for x,label,value,color,start in ((58,"DIVIDEND",5.23,GOLD_DARK,.42),(377,"NET BUYBACK",2.09,RED,.74)):
        q=back(phase(t,start,start+.80)); y=int(562+58*(1-q))
        rr(draw,(x,y,x+285,y+272),24,PAPER,"#CFC7BA",2)
        txt(draw,(x+28,y+38),label,16,color)
        txt(draw,(x+28,y+92),f"${value*q:.2f}B",38,INK)
        if label=="DIVIDEND":
            for i in range(5):
                h=25+12*i
                iso_box(draw,x+32+i*45,y+227-h,30,h,8,GOLD,"#C39100","#FFE189")
        else:
            for i in range(15):
                gx=x+32+(i%5)*45; gy=y+168+(i//5)*27
                alive = i >= int(15*phase(t,1.25,3.6)) or i%4 != 0
                draw.rectangle((gx,gy,gx+30,gy+18),fill=RED if alive else "#E9E3D9")
    source(draw,"TTM cash flows · FY2025 + H1'26 − H1'25")


def draw_shareholder(draw: ImageDraw.ImageDraw, t: float) -> None:
    p=phase(t,.08,1.65)
    draw.arc((68,316,356,604),-90,-90+359*p,fill=RED,width=32)
    draw.arc((105,353,319,567),-90,-90+359*p,fill=GOLD,width=15)
    txt(draw,(212,448),f"{3.92*p:.2f}%",47,INK,"mm")
    txt(draw,(212,514),"CASH YIELD",14,MUTED,"mm")
    draw.line((405,330,405,821),fill="#D5CEC2",width=2)
    years=int(50*phase(t,.35,2.35))
    txt(draw,(455,338),f"{years}",66,RED)
    txt(draw,(458,409),"YEARS",16,MUTED)
    for i in range(10):
        q=back(phase(t,.45+i*.10,1.15+i*.10))
        x=444+(i%5)*43; y=610-(i//5)*76
        iso_box(draw,x,y-52*q,30,52*q,8,GOLD,"#B88600","#FFE68D")
    txt(draw,(448,690),"1976 → 2026",20,INK)
    rr(draw,(72,742,648,900),24,PAPER,"#CEC6B8",2)
    txt(draw,(103,783),"배당 + 순현금 자사주매입",17,MUTED)
    txt(draw,(103,845),"$7.32B / $186.49B",30,INK)
    source(draw,"Cash-yield approximation · dividend streak from 2025 10-K")


def draw_yield_signal(draw: ImageDraw.ImageDraw, t: float) -> None:
    q=phase(t,.05,1.40)
    rr(draw,(60,286,346,730),28,PAPER,"#CFC7B9",2)
    txt(draw,(90,330),"TTM DIVIDEND",14,GOLD_DARK)
    txt(draw,(316,375),"$7.35",34,INK,"ra")
    draw.line((92,450,314,450),fill="#BCB5AA",width=3)
    txt(draw,(90,485),"PRICE",14,RED)
    txt(draw,(316,530),"$263.54",34,INK,"ra")
    arrow(draw,(203,590),(203,630),INK,5)
    txt(draw,(203,680),f"{2.79*q:.2f}%",52,RED,"mm")
    rr(draw,(382,286,660,730),28,INK)
    txt(draw,(521,334),"MONTH-END RANK",14,"#BDC5C8","ma")
    for i in range(10):
        y=398+i*25
        active=i<max(1,int(10*phase(t,.5,2.15)))
        draw.rounded_rectangle((425,y,617,y+12),radius=6,fill=RED if active and i>=8 else "#5D666B")
    txt(draw,(521,642),"2 / 80",48,WHITE,"mm")
    txt(draw,(521,692),"2020년 이후",16,"#C7CED1","mm")
    center(draw,838,"최근 구간에서는 확실히 높은 배당률",24,INK)
    source(draw,"TTM dividend / raw close · calendar month-end rank")


def draw_history(draw: ImageDraw.ImageDraw, t: float) -> None:
    x0,y0,x1,y1=70,807,650,318
    rr(draw,(54,278,666,858),28,PAPER,"#D3CCBF",2)
    draw.line((x0,y0,x1,y0),fill="#BDB7AC",width=2)
    values=[]
    for i in range(144):
        v=.40+.18*math.sin(i*.13)+.10*math.sin(i*.31)
        if 34<i<46: v+=.31
        if i>118: v+=.14*(i-118)/25
        values.append(v)
    pts=[(x0+(x1-x0)*i/(len(values)-1), y0-v*(y0-y1)) for i,v in enumerate(values)]
    n=max(2,int(len(pts)*phase(t,.05,2.0)))
    draw.line(pts[:n],fill=INK,width=6,joint="curve")
    peak=pts[40]; cur=pts[-1]
    if n>42:
        draw.ellipse((peak[0]-11,peak[1]-11,peak[0]+11,peak[1]+11),fill=GOLD_DARK)
        rr(draw,(95,304,284,390),18,"#FFF0C0")
        txt(draw,(189,335),"2015",15,GOLD_DARK,"mm")
        txt(draw,(189,370),"3.58%",26,INK,"mm")
        arrow(draw,(225,390),peak,GOLD_DARK,4,10)
    if n>140:
        draw.ellipse((cur[0]-12,cur[1]-12,cur[0]+12,cur[1]+12),fill=RED)
        rr(draw,(467,420,637,506),18,"#FCE5E1")
        txt(draw,(552,451),"현재",15,RED,"mm")
        txt(draw,(552,486),"2.79%",26,INK,"mm")
    rr(draw,(164,884,556,944),18,"#E8E3D9")
    txt(draw,(360,914),"2010년 이후 상위 약 38%",20,MUTED,"mm")
    source(draw,"Dividend-yield schematic · anchors from monthly observations")


def draw_beta(draw: ImageDraw.ImageDraw, t: float) -> None:
    specs=(("MCD",.42,RED,380),("SPY",1.00,INK,610),("QQQ",1.25,BLUE,840))
    for label,beta,color,y in specs:
        rr(draw,(66,y-80,654,y+80),24,PAPER,"#D2CABE",2)
        draw.line((145,y,568,y),fill="#D6D0C5",width=2)
        pts=[]
        for i in range(90):
            x=150+i*4.65
            wave=(math.sin(i*.34-t*3.2)*34+math.sin(i*.11)*12)*beta
            pts.append((x,y+wave))
        n=max(2,int(90*phase(t,.05,1.75)))
        draw.line(pts[:n],fill=color,width=7,joint="curve")
        txt(draw,(115,y),label,18,color,"mm")
        rr(draw,(578,y-35,638,y+35),15,color)
        txt(draw,(608,y),f"{beta:.2f}",16,WHITE,"mm")
    source(draw,"Beta-amplitude schematic · 5-year weekly estimates vs SPY")


def draw_diversify(draw: ImageDraw.ImageDraw, t: float) -> None:
    rr(draw,(58,286,662,784),28,TEAL)
    for i,(label,color,base,amp,offset) in enumerate((("MCD",RED,430,49,0),("QQQ",BLUE,635,104,1.15))):
        pts=[]
        for j in range(100):
            u=j/99
            x=105+510*u
            split=max(0,(j-38)/62)
            y=base+amp*math.sin(j*.18+offset+split*2.5)
            pts.append((x,y))
        n=max(2,int(100*phase(t,.05,1.9)))
        draw.line(pts[:n],fill=color,width=7,joint="curve")
        txt(draw,(92,base),label,17,color,"rm")
    q=back(phase(t,1.25,2.35))
    rr(draw,(176,820,544,928),22,"#E2EFEB",GREEN,2)
    txt(draw,(360,853),"상관계수",15,GREEN,"mm")
    txt(draw,(360,898),f"{.28*q:.2f}",38,INK,"mm")
    source(draw,"Co-movement schematic · weekly correlation 0.28 · 역상관 아님")


def draw_risk(draw: ImageDraw.ImageDraw, t: float) -> None:
    txt(draw,(70,292),"TOTAL DEBT",15,RED)
    txt(draw,(70,342),"$40.6B",47,INK)
    for i in range(8):
        q=back(phase(t,.15+i*.10,.75+i*.10))
        x=75+(i%4)*106; y=690-(i//4)*107
        iso_box(draw,x,y-75*q,78,75*q,20,RED if i>=6 else "#5A6267","#353A3D","#899196")
    rr(draw,(494,302,650,742),24,"#E4E9E9")
    txt(draw,(572,338),"US GUEST",14,MUTED,"mm")
    txt(draw,(572,371),"COUNTS",14,MUTED,"mm")
    # A visible queue shrinks: a concrete state change, not a generic warning icon.
    for i in range(5):
        gone=i<int(5*phase(t,1.1,3.25))
        if gone:
            continue
        y=671-i*61
        x=522+6*math.sin(t*2+i)
        rr(draw,(x,y,x+92,y+32),8,BLUE if i%2 else GOLD)
        draw.ellipse((x+12,y+25,x+27,y+40),fill=INK)
        draw.ellipse((x+66,y+25,x+81,y+40),fill=INK)
    rr(draw,(66,804,654,919),22,"#FCE5E1",RED,2)
    txt(draw,(99,843),"낮은 beta ≠ 낮은 기업 위험",23,RED)
    txt(draw,(99,886),"부채와 객수는 반드시 별도 확인",18,INK)
    source(draw,"McDonald's Q2 2026 Form 10-Q")


def draw_entry_one(draw: ImageDraw.ImageDraw, t: float) -> None:
    # The store descends to the first price floor; the amount is intentionally unspecified.
    shaft=(117,288,603,852)
    rr(draw,shaft,28,"#E6E1D7","#C8C0B3",2)
    for y in (425,610,795):
        draw.line((143,y,577,y),fill="#C6BFB3",width=3)
    travel=phase(t,.15,1.8)
    platform_y=333+295*travel
    # The price rail sits behind the building, so it cannot read as a strike-through.
    draw.line((137,628,583,628),fill=RED,width=8)
    store_model(draw,360,platform_y,.66,1.0,cars=1)
    rr(draw,(174,700,546,850),25,PAPER,RED,3)
    txt(draw,(202,742),"1차",18,RED)
    txt(draw,(202,800),"260달러대",36,INK)
    txt(draw,(518,805),"작게",19,MUTED,"ra")
    source(draw,"Educational staging scenario · not personalized advice")


def draw_entry_two(draw: ImageDraw.ImageDraw, t: float) -> None:
    rr(draw,(68,286,652,560),28,PAPER,"#D1C9BC",2)
    txt(draw,(103,332),"PRICE BAND",15,GOLD_DARK)
    band=phase(t,.10,1.40)
    draw.rounded_rectangle((103,405,103+int(514*band),482),radius=25,fill="#FFE39A")
    draw.line((205,385,205,510),fill=GOLD_DARK,width=5)
    draw.line((548,385,548,510),fill=GOLD_DARK,width=5)
    txt(draw,(376,443),"$245  ─  $250",33,INK,"mm")
    rr(draw,(68,602,652,912),28,TEAL)
    txt(draw,(103,647),"DIVIDEND YIELD",15,"#CBD4D5")
    y0=835
    draw.line((112,y0,608,y0),fill="#5E777C",width=16)
    q=phase(t,.65,2.65)
    x=112+496*q
    draw.line((112,y0,x,y0),fill=GOLD,width=16)
    draw.ellipse((x-18,y0-18,x+18,y0+18),fill=RED,outline=WHITE,width=3)
    txt(draw,(112,748),"2.79%",24,WHITE)
    txt(draw,(608,748),"≈ 3.0%",24,GOLD,"ra")
    source(draw,"Approximate yield at staged price range")


def draw_final(draw: ImageDraw.ImageDraw, t: float) -> None:
    # Strong brand lockup first, then two clean decision gates. Nothing is crossed out.
    reveal=phase(t,.05,1.20)
    golden_arches(draw,360,482,300,290,34,reveal)
    rr(draw,(82,556,638,703),24,"#E2EFEB",GREEN,3)
    draw.ellipse((111,594,167,650),fill=GREEN)
    txt(draw,(139,622),"✓",27,WHITE,"mm")
    txt(draw,(194,597),"객수 회복 확인",21,GREEN)
    txt(draw,(194,643),"그때 비중 확대",27,INK)
    q=back(phase(t,1.20,2.15))
    y=int(868+100*(1-q))
    rr(draw,(82,y-112,638,y),24,"#FCE5E1",RED,3)
    draw.ellipse((111,y-83,167,y-27),fill=RED)
    txt(draw,(139,y-55),"!",27,WHITE,"mm")
    txt(draw,(194,y-87),"객수·FCF·배당 커버리지 훼손",17,RED)
    txt(draw,(194,y-43),"투자 아이디어 취소",25,INK)
    # A short return of the opening lines creates a seamless replay cue.
    loop=phase(t,3.05,4.15)
    if loop:
        red_pts=[]; blue_pts=[]
        for i in range(34):
            u=i/33
            if u>loop: break
            x=87+546*u
            red_pts.append((x,900+22*u+7*math.sin(u*11)))
            blue_pts.append((x,934-30*u+7*math.sin(u*10+1)))
        if len(red_pts)>1:
            draw.line(red_pts,fill=RED,width=5,joint="curve")
            draw.line(blue_pts,fill=BLUE,width=5,joint="curve")
    source(draw,"Educational analysis · not personalized investment advice")


DRAWERS = [
    draw_hook, draw_candidate, draw_network, draw_property, draw_return, draw_shareholder,
    draw_yield_signal, draw_history, draw_beta, draw_diversify, draw_risk,
    draw_entry_one, draw_entry_two, draw_final,
]


def render(output: Path) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg is required")
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        ffmpeg, "-y", "-hide_banner", "-loglevel", "warning", "-f", "rawvideo",
        "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an",
        "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-preset", "medium",
        "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(output),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    frames = int(round(TOTAL * FPS))
    try:
        for frame_index in range(frames):
            gt = frame_index / FPS
            scene_index = min(len(SCENES)-1, max(i for i, start in enumerate(BOUNDARIES[:-1]) if start <= gt))
            lt = gt - BOUNDARIES[scene_index]
            image, draw = base_frame(gt, scene_index)
            DRAWERS[scene_index](draw, lt)
            apply_content_camera(image, scene_index, lt)
            draw = ImageDraw.Draw(image)
            # Repaint title at native scale; all motion stays below this fixed rail.
            scene_title(draw, lt, *TITLES[scene_index])
            # Fast editorial cut, restricted to the content region and never touching captions.
            if scene_index and lt < .16:
                cut = phase(lt, 0, .16)
                x = int(-100 + (W+200)*cut)
                draw.polygon(((x-32,224),(x+16,224),(x-24,994),(x-72,994)),fill=GOLD)
            if scene_index and lt < .065:
                layer=Image.new("RGBA",(W,H),(0,0,0,0))
                layer_draw=ImageDraw.Draw(layer)
                layer_draw.rectangle((0,224,W,994),fill=(255,255,255,int(80*(1-lt/.065))))
                image=Image.alpha_composite(image.convert("RGBA"),layer).convert("RGB")
            assert process.stdin is not None
            process.stdin.write(image.tobytes())
    finally:
        if process.stdin:
            process.stdin.close()
    if process.wait() != 0:
        raise RuntimeError(f"ffmpeg failed with exit code {process.returncode}")


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    render(args.output.resolve())
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
