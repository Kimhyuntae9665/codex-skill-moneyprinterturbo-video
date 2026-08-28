#!/usr/bin/env python3
"""Build rights-cleared 1080x1920 infographic frames for the MCD example."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH = 1080
HEIGHT = 1920
BG_TOP = (18, 15, 20)
BG_BOTTOM = (42, 19, 22)
WHITE = (249, 247, 242)
MUTED = (190, 184, 181)
RED = (218, 41, 28)
GOLD = (255, 188, 13)
GREEN = (45, 168, 112)
BLUE = (55, 129, 210)
CARD = (40, 34, 39)
CARD_2 = (53, 43, 47)
OUTLINE = (91, 73, 78)


def parse_args() -> argparse.Namespace:
    skill_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "generated-materials",
    )
    parser.add_argument(
        "--font",
        type=Path,
        default=skill_root / "assets" / "fonts" / "NotoSansKR-Bold.ttf",
    )
    return parser.parse_args()


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size)


def gradient() -> Image.Image:
    colors = []
    for y in range(HEIGHT):
        ratio = y / (HEIGHT - 1)
        colors.append(tuple(
            round(BG_TOP[index] * (1 - ratio) + BG_BOTTOM[index] * ratio)
            for index in range(3)
        ))
    column = Image.new("RGB", (1, HEIGHT))
    column.putdata(colors)
    return column.resize((WIDTH, HEIGHT))


def rounded(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    fill: tuple[int, int, int],
    radius: int = 34,
    outline: tuple[int, int, int] | None = None,
    width: int = 2,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def centered_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    value: str,
    face: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int] = WHITE,
    spacing: int = 14,
) -> None:
    draw.multiline_text(
        xy,
        value,
        font=face,
        fill=fill,
        anchor="mm",
        align="center",
        spacing=spacing,
    )


def header(draw: ImageDraw.ImageDraw, fonts: dict[str, ImageFont.FreeTypeFont]) -> None:
    rounded(draw, (70, 58, 470, 124), (80, 24, 27), radius=30)
    centered_text(draw, (270, 91), "MCD BUSINESS MODEL", fonts["eyebrow"], GOLD)
    draw.text((975, 82), "2025 10-K", font=fonts["small"], fill=MUTED, anchor="ra")


def footer(draw: ImageDraw.ImageDraw, fonts: dict[str, ImageFont.FreeTypeFont]) -> None:
    draw.line((70, 1765, 1010, 1765), fill=OUTLINE, width=2)
    draw.text(
        (70, 1795),
        "교육용 요약 · 출처: McDonald's 2025 Form 10-K",
        font=fonts["tiny"],
        fill=MUTED,
    )
    draw.text((1010, 1795), "@ MPT EXAMPLE", font=fonts["tiny"], fill=GOLD, anchor="ra")


def title(
    draw: ImageDraw.ImageDraw,
    fonts: dict[str, ImageFont.FreeTypeFont],
    value: str,
    subtitle: str | None = None,
) -> None:
    centered_text(draw, (540, 250), value, fonts["title"], WHITE, spacing=8)
    if subtitle:
        centered_text(draw, (540, 370), subtitle, fonts["body"], MUTED)


def arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[int, int],
    end: tuple[int, int],
    color: tuple[int, int, int] = GOLD,
    width: int = 18,
) -> None:
    draw.line((*start, *end), fill=color, width=width)
    ex, ey = end
    sx, sy = start
    if abs(ex - sx) >= abs(ey - sy):
        direction = 1 if ex > sx else -1
        draw.polygon(
            [(ex, ey), (ex - direction * 38, ey - 28), (ex - direction * 38, ey + 28)],
            fill=color,
        )
    else:
        direction = 1 if ey > sy else -1
        draw.polygon(
            [(ex, ey), (ex - 28, ey - direction * 38), (ex + 28, ey - direction * 38)],
            fill=color,
        )


def burger(draw: ImageDraw.ImageDraw, center: tuple[int, int], scale: float = 1.0) -> None:
    cx, cy = center
    w = int(310 * scale)
    h = int(80 * scale)
    draw.pieslice(
        (
            cx - w // 2,
            int(cy - 150 * scale),
            cx + w // 2,
            int(cy + 40 * scale),
        ),
        180,
        360,
        fill=GOLD,
    )
    rounded(draw, (cx - w // 2, int(cy - 22 * scale), cx + w // 2, int(cy + 30 * scale)), GREEN, radius=20)
    rounded(draw, (cx - w // 2, int(cy + 40 * scale), cx + w // 2, int(cy + 40 * scale + h)), RED, radius=22)
    rounded(draw, (cx - w // 2, int(cy + 135 * scale), cx + w // 2, int(cy + 215 * scale)), GOLD, radius=28)
    for dx in (-80, -25, 35, 90):
        draw.ellipse((cx + dx - 5, cy - 100, cx + dx + 5, cy - 90), fill=WHITE)


def key_icon(draw: ImageDraw.ImageDraw, center: tuple[int, int], scale: float = 1.0) -> None:
    cx, cy = center
    r = int(86 * scale)
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=GOLD, width=max(8, int(24 * scale)))
    draw.ellipse((cx - r // 3, cy - r // 3, cx + r // 3, cy + r // 3), fill=BG_TOP)
    draw.line((cx + r - 8, cy, cx + 250 * scale, cy), fill=GOLD, width=max(8, int(28 * scale)))
    draw.line((cx + 185 * scale, cy, cx + 185 * scale, cy + 65 * scale), fill=GOLD, width=max(8, int(28 * scale)))
    draw.line((cx + 235 * scale, cy, cx + 235 * scale, cy + 50 * scale), fill=GOLD, width=max(8, int(28 * scale)))


def store_icon(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    active: bool = True,
) -> None:
    x1, y1, x2, y2 = box
    color = GOLD if active else (83, 72, 74)
    draw.rectangle((x1 + 8, y1 + 40, x2 - 8, y2), fill=CARD_2, outline=color, width=4)
    draw.polygon([(x1, y1 + 45), ((x1 + x2) // 2, y1), (x2, y1 + 45)], fill=color)
    door_w = (x2 - x1) // 4
    draw.rectangle((((x1 + x2) // 2 - door_w // 2), y2 - 48, ((x1 + x2) // 2 + door_w // 2), y2), fill=color)


def building_icon(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    x1, y1, x2, y2 = box
    draw.rectangle(box, fill=CARD_2, outline=GOLD, width=6)
    for row in range(3):
        for col in range(3):
            wx = x1 + 35 + col * 70
            wy = y1 + 40 + row * 70
            draw.rounded_rectangle((wx, wy, wx + 38, wy + 42), radius=6, fill=BLUE)
    draw.rectangle(((x1 + x2) // 2 - 35, y2 - 90, (x1 + x2) // 2 + 35, y2), fill=GOLD)
    draw.polygon([(x1 - 25, y1), ((x1 + x2) // 2, y1 - 90), (x2 + 25, y1)], fill=RED)


def person_icon(draw: ImageDraw.ImageDraw, center: tuple[int, int]) -> None:
    cx, cy = center
    draw.ellipse((cx - 62, cy - 160, cx + 62, cy - 36), fill=GOLD)
    draw.rounded_rectangle((cx - 120, cy - 20, cx + 120, cy + 250), radius=50, fill=BLUE)
    draw.line((cx - 70, cy + 75, cx - 155, cy + 185), fill=WHITE, width=22)
    draw.line((cx + 70, cy + 75, cx + 155, cy + 185), fill=WHITE, width=22)


def frame_1(image: Image.Image, draw: ImageDraw.ImageDraw, fonts: dict) -> None:
    title(draw, fonts, "햄버거 회사가\n임대료를 받는 이유")
    rounded(draw, (90, 500, 990, 1260), CARD, outline=OUTLINE)
    burger(draw, (300, 760), 0.9)
    arrow(draw, (475, 850), (610, 850), width=16)
    key_icon(draw, (725, 850), 0.9)
    centered_text(draw, (540, 1135), "햄버거  →  매장  →  반복 수익", fonts["body"], WHITE)


def frame_2(image: Image.Image, draw: ImageDraw.ImageDraw, fonts: dict) -> None:
    title(draw, fonts, "2025년 말\n약 95%가 가맹점")
    rounded(draw, (90, 480, 990, 1250), CARD, outline=OUTLINE)
    start_x, start_y = 145, 560
    for index in range(20):
        row, col = divmod(index, 5)
        x = start_x + col * 165
        y = start_y + row * 155
        store_icon(draw, (x, y, x + 105, y + 105), active=index < 19)
    centered_text(draw, (540, 1200), "매장 수 기준 · 부동산 소유 비율 아님", fonts["small"], MUTED)


def frame_3(image: Image.Image, draw: ImageDraw.ImageDraw, fonts: dict) -> None:
    title(draw, fonts, "일반적인 가맹 계약은\n역할을 나눕니다")
    rounded(draw, (70, 500, 520, 1260), CARD, outline=GOLD)
    rounded(draw, (560, 500, 1010, 1260), CARD, outline=BLUE)
    building_icon(draw, (165, 650, 425, 1010))
    person_icon(draw, (785, 790))
    centered_text(draw, (295, 1130), "본사\n토지·건물 소유\n또는 장기 임차", fonts["body"], WHITE)
    centered_text(draw, (785, 1130), "가맹점주\n장비·매장 운영", fonts["body"], WHITE)
    rounded(draw, (280, 1315, 800, 1385), (80, 24, 27), radius=28)
    centered_text(draw, (540, 1350), "conventional franchise 기준", fonts["small"], GOLD)


def frame_4(image: Image.Image, draw: ImageDraw.ImageDraw, fonts: dict) -> None:
    title(draw, fonts, "매장 매출이 생기면\n두 흐름이 본사로")
    rounded(draw, (110, 500, 970, 1210), CARD, outline=OUTLINE)
    rounded(draw, (350, 570, 730, 730), RED, radius=40)
    centered_text(draw, (540, 650), "매장 매출", fonts["headline"], WHITE)
    arrow(draw, (540, 755), (330, 915), color=GOLD)
    arrow(draw, (540, 755), (750, 915), color=GOLD)
    rounded(draw, (120, 920, 500, 1100), CARD_2, outline=GOLD)
    rounded(draw, (580, 920, 960, 1100), CARD_2, outline=BLUE)
    centered_text(draw, (310, 1010), "임대료\n최저액 + 매출연동", fonts["body"], GOLD)
    centered_text(draw, (770, 1010), "로열티\n매출연동", fonts["body"], (135, 191, 255))
    centered_text(draw, (540, 1300), "브랜드와 입지 계약에서 나오는 본사 매출", fonts["small"], MUTED)


def frame_5(image: Image.Image, draw: ImageDraw.ImageDraw, fonts: dict) -> None:
    title(draw, fonts, "2025년 가맹 매출의\n두 핵심 숫자")
    rounded(draw, (80, 500, 1000, 850), CARD, outline=GOLD)
    rounded(draw, (80, 900, 1000, 1250), CARD, outline=BLUE)
    draw.text((135, 575), "임대료", font=fonts["body"], fill=GOLD)
    draw.text((945, 650), "$10.442B", font=fonts["number"], fill=WHITE, anchor="ra")
    draw.text((135, 975), "로열티", font=fonts["body"], fill=(135, 191, 255))
    draw.text((945, 1050), "$6.018B", font=fonts["number"], fill=WHITE, anchor="ra")
    centered_text(draw, (540, 1340), "McDonald's Corporation 매출 · 이익 아님", fonts["small"], MUTED)


def frame_6(image: Image.Image, draw: ImageDraw.ImageDraw, fonts: dict) -> None:
    title(draw, fonts, "숫자를 이렇게\n읽으면 안 됩니다")
    rounded(draw, (90, 510, 990, 1240), CARD, outline=OUTLINE)
    centered_text(draw, (540, 680), "본사 가맹 매출", fonts["headline"], WHITE)
    centered_text(draw, (540, 830), "≠", fonts["huge"], RED)
    centered_text(draw, (540, 980), "전 세계 매장 판매액", fonts["headline"], WHITE)
    draw.line((180, 1110, 900, 1110), fill=OUTLINE, width=3)
    centered_text(draw, (540, 1180), "매출  ≠  이익", fonts["body"], GOLD)


def frame_7(image: Image.Image, draw: ImageDraw.ImageDraw, fonts: dict) -> None:
    title(draw, fonts, "모든 매장 땅을\n본사가 가진 것은 아닙니다")
    rounded(draw, (90, 500, 990, 1240), CARD, outline=OUTLINE)
    rounded(draw, (150, 590, 930, 790), CARD_2, outline=GOLD)
    centered_text(draw, (540, 690), "일반 가맹\n본사 부동산 소유·장기 임차", fonts["body"], WHITE)
    rounded(draw, (150, 860, 930, 1060), CARD_2, outline=BLUE)
    centered_text(draw, (540, 960), "일부 라이선스 사업자\n부동산 자본 직접 부담", fonts["body"], WHITE)
    centered_text(draw, (540, 1165), "계약 유형과 국가에 따라 구조가 다름", fonts["small"], MUTED)


def frame_8(image: Image.Image, draw: ImageDraw.ImageDraw, fonts: dict) -> None:
    title(draw, fonts, "부동산만이 아니라\n시스템이 핵심")
    rounded(draw, (90, 480, 990, 1240), CARD, outline=OUTLINE)
    nodes = [
        ((310, 660), "좋은 입지", GOLD),
        ((770, 660), "브랜드", RED),
        ((770, 1040), "운영 시스템", BLUE),
        ((310, 1040), "반복 수익", GREEN),
    ]
    for (cx, cy), label, color in nodes:
        rounded(draw, (cx - 170, cy - 75, cx + 170, cy + 75), CARD_2, outline=color)
        centered_text(draw, (cx, cy), label, fonts["body"], WHITE)
    arrow(draw, (500, 660), (580, 660), color=GOLD, width=10)
    arrow(draw, (770, 755), (770, 925), color=RED, width=10)
    arrow(draw, (580, 1040), (500, 1040), color=BLUE, width=10)
    arrow(draw, (310, 945), (310, 775), color=GREEN, width=10)
    centered_text(draw, (540, 1340), "프랜차이즈 기업의 강력한 수익 구조", fonts["small"], MUTED)


FRAME_BUILDERS = [frame_1, frame_2, frame_3, frame_4, frame_5, frame_6, frame_7, frame_8]


def main() -> int:
    args = parse_args()
    font_path = args.font.expanduser().resolve()
    if not font_path.is_file():
        raise SystemExit(f"font not found: {font_path}")
    output = args.output.expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    fonts = {
        "tiny": font(font_path, 26),
        "small": font(font_path, 34),
        "eyebrow": font(font_path, 30),
        "body": font(font_path, 48),
        "headline": font(font_path, 62),
        "title": font(font_path, 72),
        "number": font(font_path, 92),
        "huge": font(font_path, 128),
    }
    frame_paths: list[str] = []
    for index, builder in enumerate(FRAME_BUILDERS, start=1):
        image = gradient()
        draw = ImageDraw.Draw(image)
        header(draw, fonts)
        footer(draw, fonts)
        builder(image, draw, fonts)
        frame_path = output / f"{index:02d}-mcd-frame.png"
        image.save(frame_path, format="PNG", optimize=True)
        frame_paths.append(str(frame_path))
    manifest = {
        "status": "created",
        "resolution": [WIDTH, HEIGHT],
        "frame_count": len(frame_paths),
        "frames": frame_paths,
        "visual_rights": "Original geometric artwork generated by this repository",
        "trademarks": "No McDonald's logo or commercial photography included",
        "data_source": "McDonald's 2025 Form 10-K",
    }
    manifest_path = output / "materials-manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
