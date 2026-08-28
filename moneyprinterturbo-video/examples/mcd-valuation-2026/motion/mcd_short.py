from __future__ import annotations

import csv
from datetime import datetime
import os
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageOps
from manim import (
    AnimationGroup,
    BackgroundRectangle,
    BLACK,
    Circle,
    Create,
    DashedLine,
    Dot,
    DOWN,
    FadeIn,
    FadeOut,
    Group,
    ImageMobject,
    LaggedStart,
    LEFT,
    Line,
    ORIGIN,
    Rectangle,
    RIGHT,
    RoundedRectangle,
    Scene,
    Text,
    UP,
    VGroup,
    config,
    interpolate_color,
    linear,
)


config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 30
config.background_color = "#0E1113"

ROOT = Path(__file__).resolve().parents[1]
ASSETS = Path(os.environ.get("MCD_ASSETS_DIR", ROOT / "assets")).resolve()
RESEARCH = Path(os.environ.get("MCD_RESEARCH_DIR", ROOT / "research")).resolve()
FONT_FILE = Path(
    os.environ.get(
        "MCD_FONT_FILE",
        Path(__file__).resolve().parents[3] / "assets" / "fonts" / "NotoSansKR-Bold.ttf",
    )
).resolve()

CARBON = "#0E1113"
BONE = "#F4F0E8"
SLATE = "#7B848A"
BRASS = "#BA8F73"
RED = "#D23A34"
FOG = "#D8DDD9"
INK = "#202529"

SAFE_LEFT = -3.65
SAFE_RIGHT = 2.55
SAFE_CENTER_X = (SAFE_LEFT + SAFE_RIGHT) / 2
SOURCE_Y = -1.85


def register_font() -> str:
    try:
        import manimpango

        manimpango.register_font(str(FONT_FILE))
    except Exception:
        pass
    return "Noto Sans KR"


FONT = register_font()


def txt(
    value: str,
    size: float,
    color: str = BONE,
    weight: str = "NORMAL",
    line_spacing: float = -1,
) -> Text:
    return Text(
        value,
        font=FONT,
        font_size=size,
        color=color,
        weight=weight,
        line_spacing=line_spacing,
    )


def source_chip(value: str) -> VGroup:
    label = txt(value, 24, FOG)
    rule = Line(LEFT * 0.32, RIGHT * 0.32, color=BRASS, stroke_width=3)
    content = VGroup(rule, label).arrange(RIGHT, buff=0.18)
    if content.width > SAFE_RIGHT - SAFE_LEFT - 0.24:
        content.scale_to_fit_width(SAFE_RIGHT - SAFE_LEFT - 0.24)
    background = BackgroundRectangle(
        content,
        color=CARBON,
        fill_opacity=0.72,
        buff=0.12,
    )
    group = VGroup(background, content)
    group.move_to([SAFE_LEFT + group.width / 2, SOURCE_Y, 0])
    return group


def section_label(index: str, value: str) -> VGroup:
    number = txt(index, 25, BRASS, "BOLD")
    label = txt(value.upper(), 24, SLATE, "BOLD")
    rule = Line(ORIGIN, RIGHT * 0.72, color=SLATE, stroke_width=2)
    group = VGroup(number, rule, label).arrange(RIGHT, buff=0.18)
    group.move_to([SAFE_LEFT + group.width / 2, 6.7, 0])
    return group


def cover_image(path: Path, brightness: float = 0.6) -> ImageMobject:
    crop_boxes = {
        "mcd-bethesda-modern-ccby4": (3400, 0, 5733, 4147),
        "mcd-downey-historic-cc0": (1600, 0, 3075, 2622),
    }
    with Image.open(path) as opened:
        image = ImageOps.exif_transpose(opened).convert("RGB")
        crop_box = crop_boxes.get(path.stem)
        if crop_box is None:
            raise ValueError(f"missing reviewed 9:16 crop for {path.name}")
        image = image.crop(crop_box).resize((1080, 1920), Image.Resampling.LANCZOS)
        image = ImageEnhance.Brightness(image).enhance(brightness)
        array = np.array(image)
    result = ImageMobject(array)
    result.set_width(config.frame_width)
    result.set_height(config.frame_height)
    return result


def asset_photos() -> list[Path]:
    candidates = [
        path
        for path in sorted(ASSETS.glob("*"))
        if path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
        and "contact" not in path.stem.lower()
    ]
    if len(candidates) < 2:
        raise FileNotFoundError("two rights-cleared building photos are required")
    return candidates[:2]


def asset_credit(path: Path) -> str:
    credits = {
        "mcd-bethesda-modern-ccby4": "PHOTO · G. EDWARD JOHNSON · CC BY 4.0 · 9:16 CROP",
        "mcd-downey-historic-cc0": "PHOTO · NORTHWALKER · CC0 · COMMONS",
    }
    try:
        return credits[path.stem]
    except KeyError as exc:
        raise ValueError(f"missing on-screen photo credit for {path.name}") from exc


def price_points() -> list[tuple[datetime, float]]:
    path = RESEARCH / "price_history.csv"
    rows: list[tuple[datetime, float]] = []
    chart_start = datetime(2026, 2, 27)
    chart_end = datetime(2026, 8, 27)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            date_value = row.get("date") or row.get("Date")
            close_value = (
                row.get("raw_close")
                or row.get("close")
                or row.get("Close")
                or row.get("raw_close_usd")
            )
            if not date_value or not close_value:
                continue
            try:
                trade_date = datetime.fromisoformat(date_value)
                if chart_start <= trade_date <= chart_end:
                    rows.append((trade_date, float(close_value)))
            except ValueError:
                continue
    if len(rows) < 2:
        raise ValueError("price_history.csv needs raw closes from 2026-02-27 through 2026-08-27")
    if rows[0] != (chart_start, 341.06) or rows[-1] != (chart_end, 260.06):
        raise ValueError("price-history endpoints do not match the verified raw-close comparison")
    return rows


def left_align(group: VGroup, y: float, max_width: float = SAFE_RIGHT - SAFE_LEFT) -> VGroup:
    if group.width > max_width:
        group.scale_to_fit_width(max_width)
    group.move_to([SAFE_LEFT + group.width / 2, y, 0])
    return group


class MCDValuationShort(Scene):
    def construct(self) -> None:
        photo_one, photo_two = asset_photos()
        prices = price_points()

        self.scene_hook(photo_one)
        self.scene_drawdown(prices)
        self.scene_valuation()
        self.scene_franchise()
        self.scene_revenue()
        self.scene_dividend()
        self.scene_risks()
        self.scene_close(photo_two)

    def scene_hook(self, photo: Path) -> None:
        image = cover_image(photo, 0.52)
        shade = Rectangle(
            width=9,
            height=16,
            fill_color=BLACK,
            fill_opacity=0.28,
            stroke_opacity=0,
        )
        eyebrow = txt("MCD · VALUATION BRIEF", 26, BRASS, "BOLD")
        headline = VGroup(
            txt("맥도날드 주가", 77, BONE, "BOLD"),
            txt("정말 싸졌을까?", 77, BONE, "BOLD"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        rule = Line(ORIGIN, RIGHT * 1.1, color=BRASS, stroke_width=6)
        stack = VGroup(eyebrow, rule, headline).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        left_align(stack, 2.0)
        credit = source_chip(asset_credit(photo))

        self.add(image, shade)
        self.play(
            AnimationGroup(
                image.animate.scale(1.015),
                FadeIn(stack, shift=UP * 0.18),
                FadeIn(credit),
                lag_ratio=0,
            ),
            run_time=0.9,
        )
        self.play(image.animate.scale(1.025), run_time=1.7, rate_func=linear)
        self.play(FadeOut(Group(image, shade, stack, credit)), run_time=0.5)

    def scene_drawdown(self, rows: list[tuple[datetime, float]]) -> None:
        header = section_label("01", "raw-close drawdown")
        title = left_align(txt("같은 가격 기준으로 다시 계산", 48, BONE, "BOLD"), 5.65)

        dates = [row[0] for row in rows]
        values = [row[1] for row in rows]
        min_value = min(values)
        max_value = max(values)
        x_left, x_right = SAFE_LEFT, SAFE_RIGHT - 0.1
        y_bottom, y_top = 0.35, 4.35
        span = max(max_value - min_value, 1)
        points = []
        for index, value in enumerate(values):
            ratio_x = index / max(len(values) - 1, 1)
            ratio_y = (value - min_value) / span
            points.append([x_left + ratio_x * (x_right - x_left), y_bottom + ratio_y * (y_top - y_bottom), 0])

        grid = VGroup(
            *[
                DashedLine(
                    [x_left, y_bottom + i * (y_top - y_bottom) / 3, 0],
                    [x_right, y_bottom + i * (y_top - y_bottom) / 3, 0],
                    dash_length=0.08,
                    color=SLATE,
                    stroke_opacity=0.25,
                    stroke_width=1,
                )
                for i in range(4)
            ]
        )
        line = VGroup(
            *[
                Line(points[i], points[i + 1], color=RED, stroke_width=5)
                for i in range(len(points) - 1)
            ]
        )
        start_dot = Dot(points[0], radius=0.085, color=BONE)
        end_dot = Dot(points[-1], radius=0.1, color=RED)
        start_value = txt("$341.06", 38, BONE, "BOLD")
        start_value.move_to([x_left + start_value.width / 2, points[0][1] - 0.38, 0])
        end_value = txt("$260.06", 40, RED, "BOLD")
        end_value.move_to([x_right - end_value.width / 2, points[-1][1] + 0.62, 0])
        start_date = txt(dates[0].strftime("2026.%m.%d"), 22, SLATE).next_to(start_value, DOWN, buff=0.08)
        end_date = txt(dates[-1].strftime("2026.%m.%d"), 22, SLATE).next_to(end_value, UP, buff=0.08)
        start_callout = VGroup(start_value, start_date)
        end_callout = VGroup(end_value, end_date)
        start_back = BackgroundRectangle(start_callout, color=CARBON, fill_opacity=0.84, buff=0.07, stroke_opacity=0)
        end_back = BackgroundRectangle(end_callout, color=CARBON, fill_opacity=0.84, buff=0.07, stroke_opacity=0)
        drop = txt("-23.8%", 102, RED, "BOLD")
        drop.move_to([SAFE_LEFT + drop.width / 2, -0.35, 0])
        basis = left_align(txt("비조정 종가 → 비조정 종가", 28, SLATE, "BOLD"), -1.35)
        source = source_chip("시장 데이터: ChartExchange · 계산: 260.06 / 341.06 - 1")
        group = VGroup(header, title, grid, line, start_dot, end_dot, start_back, end_back, start_callout, end_callout, drop, basis, source)

        self.play(FadeIn(VGroup(header, title, grid)), run_time=0.5)
        self.play(Create(line), run_time=2.2)
        self.play(LaggedStart(FadeIn(start_dot), FadeIn(start_back), FadeIn(start_callout), FadeIn(end_dot), FadeIn(end_back), FadeIn(end_callout), lag_ratio=0.08), run_time=0.8)
        self.play(FadeIn(drop, shift=UP * 0.1), FadeIn(basis), FadeIn(source), run_time=0.6)
        self.wait(4.3)
        self.play(FadeOut(group), run_time=0.6)

    def scene_valuation(self) -> None:
        header = section_label("02", "valuation context")
        title = left_align(txt("최근 5년에는 낮다", 55, BONE, "BOLD"), 5.6)
        pe = txt("21.1×", 110, BRASS, "BOLD")
        pe.move_to([SAFE_LEFT + pe.width / 2, 3.85, 0])
        median = txt("5년 중앙값 26.2×", 38, FOG, "BOLD")
        median.next_to(pe, DOWN, aligned_edge=LEFT, buff=0.12)

        gauge_left, gauge_right, gauge_y = SAFE_LEFT, SAFE_RIGHT - 0.15, 1.75
        gauge = Line([gauge_left, gauge_y, 0], [gauge_right, gauge_y, 0], color=SLATE, stroke_width=5)
        current_x = gauge_left + (21.1 - 18) / 12 * (gauge_right - gauge_left)
        median_x = gauge_left + (26.2 - 18) / 12 * (gauge_right - gauge_left)
        current_tick = Line([current_x, gauge_y - 0.22, 0], [current_x, gauge_y + 0.22, 0], color=BRASS, stroke_width=8)
        median_tick = Line([median_x, gauge_y - 0.18, 0], [median_x, gauge_y + 0.18, 0], color=BONE, stroke_width=4)
        gauge_labels = VGroup(
            txt("18×", 23, SLATE).move_to([gauge_left, gauge_y - 0.42, 0]),
            txt("30×", 23, SLATE).move_to([gauge_right, gauge_y - 0.42, 0]),
            txt("현재", 24, BRASS, "BOLD").move_to([current_x, gauge_y + 0.45, 0]),
            txt("중앙", 24, BONE).move_to([median_x, gauge_y + 0.45, 0]),
        )
        delta = txt("중앙값 대비 -19%", 44, BRASS, "BOLD")
        left_align(delta, 0.45)
        source = source_chip("StockResearch · TTM P/E · 공급자별 산식 차이")
        first = VGroup(header, title, pe, median, gauge, current_tick, median_tick, gauge_labels, delta, source)

        self.play(FadeIn(VGroup(header, title, pe, median)), run_time=0.6)
        self.play(Create(gauge), FadeIn(VGroup(current_tick, median_tick)), run_time=1.2)
        self.play(FadeIn(gauge_labels), FadeIn(delta), FadeIn(source), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(first), run_time=0.5)

        header2 = section_label("02", "valuation context")
        title2 = left_align(txt("하지만 20년의 극단값은 아니다", 50, BONE, "BOLD"), 5.55)
        percentile = txt("40 / 100", 104, FOG, "BOLD")
        left_align(percentile, 3.8)
        note = left_align(txt("관측치 40%는 지금보다 낮았다", 38, SLATE, "BOLD"), 2.75)
        rail = Line([SAFE_LEFT, 1.4, 0], [SAFE_RIGHT - 0.1, 1.4, 0], color=SLATE, stroke_width=6)
        filled = Line([SAFE_LEFT, 1.4, 0], [SAFE_LEFT + (SAFE_RIGHT - 0.1 - SAFE_LEFT) * 0.4, 1.4, 0], color=BRASS, stroke_width=8)
        marker = Dot([SAFE_LEFT + (SAFE_RIGHT - 0.1 - SAFE_LEFT) * 0.4, 1.4, 0], radius=0.11, color=BRASS)
        endpoints = VGroup(
            txt("더 낮은 P/E", 23, SLATE).move_to([SAFE_LEFT + 0.55, 0.95, 0]),
            txt("더 높은 P/E", 23, SLATE).move_to([SAFE_RIGHT - 0.7, 0.95, 0]),
        )
        verdict_box = RoundedRectangle(width=6.15, height=1.15, corner_radius=0.12, stroke_color=RED, stroke_width=2, fill_color=RED, fill_opacity=0.08)
        verdict_box.move_to([SAFE_CENTER_X, -0.35, 0])
        verdict = txt("최근 5년 저점권  ≠  역사적 바닥", 36, BONE, "BOLD").move_to(verdict_box)
        source2 = source_chip("TGMCharts · 20년 관측 분포 · 현재 약 40백분위")
        second = VGroup(header2, title2, percentile, note, rail, filled, marker, endpoints, verdict_box, verdict, source2)

        self.play(FadeIn(VGroup(header2, title2, percentile, note)), run_time=0.6)
        self.play(Create(rail), Create(filled), FadeIn(marker), run_time=1.1)
        self.play(FadeIn(endpoints), FadeIn(verdict_box), FadeIn(verdict), FadeIn(source2), run_time=0.6)
        self.wait(5.5)
        self.play(FadeOut(second), run_time=0.5)

    def scene_franchise(self) -> None:
        header = section_label("03", "franchise footprint")
        title = left_align(txt("햄버거 뒤의 가맹 네트워크", 50, BONE, "BOLD"), 5.55)
        count = txt("46,028", 112, BONE, "BOLD")
        left_align(count, 3.75)
        count_label = txt("전 세계 매장", 32, SLATE, "BOLD").next_to(count, DOWN, aligned_edge=LEFT, buff=0.08)

        bar_outline = RoundedRectangle(width=6.15, height=0.72, corner_radius=0.1, stroke_color=SLATE, stroke_width=2)
        bar_outline.move_to([SAFE_CENTER_X, 1.75, 0])
        fill = Rectangle(width=6.15 * 0.956, height=0.68, fill_color=BRASS, fill_opacity=1, stroke_opacity=0)
        fill.align_to(bar_outline, LEFT).move_to([bar_outline.get_left()[0] + fill.width / 2, 1.75, 0])
        franchise = txt("약 95% 가맹", 56, CARBON, "BOLD").move_to(fill)
        qualifier = left_align(txt("매장 수 기준 · 토지 소유 비중 아님", 29, SLATE, "BOLD"), 0.65)
        source = source_chip("McDonald's Q2 2026 Form 10-Q")
        group = VGroup(header, title, count, count_label, bar_outline, fill, franchise, qualifier, source)

        self.play(FadeIn(VGroup(header, title, count, count_label)), run_time=0.5)
        self.play(Create(bar_outline), FadeIn(fill, shift=RIGHT * 0.15), FadeIn(franchise), run_time=1.0)
        self.play(FadeIn(qualifier), FadeIn(source), run_time=0.4)
        self.wait(1.5)
        self.play(FadeOut(group), run_time=0.6)

    def scene_revenue(self) -> None:
        header = section_label("04", "franchised revenue")
        title = left_align(txt("2026 상반기 가맹 매출", 50, BONE, "BOLD"), 5.55)
        total = txt("$8.399B", 105, BONE, "BOLD")
        left_align(total, 4.15)

        total_width = 6.15
        rent_width = total_width * 5.264 / 8.399
        royalty_width = total_width * 3.096 / 8.399
        fee_width = total_width - rent_width - royalty_width
        start_x = SAFE_LEFT
        bar_y = 2.5
        rent = Rectangle(width=rent_width, height=0.78, fill_color=BRASS, fill_opacity=1, stroke_opacity=0)
        rent.move_to([start_x + rent_width / 2, bar_y, 0])
        royalty = Rectangle(width=royalty_width, height=0.78, fill_color=FOG, fill_opacity=1, stroke_opacity=0)
        royalty.move_to([start_x + rent_width + royalty_width / 2, bar_y, 0])
        fee = Rectangle(width=max(fee_width, 0.035), height=0.78, fill_color=RED, fill_opacity=1, stroke_opacity=0)
        fee.move_to([start_x + rent_width + royalty_width + max(fee_width, 0.035) / 2, bar_y, 0])

        rent_label = left_align(txt("임대료  $5.264B", 40, BRASS, "BOLD"), 1.3)
        royalty_label = left_align(txt("로열티  $3.096B", 40, FOG, "BOLD"), 0.6)
        fees_label = left_align(txt("초기 수수료  $0.039B", 28, SLATE), -0.05)
        warning_box = RoundedRectangle(width=6.15, height=0.9, corner_radius=0.1, stroke_color=RED, stroke_width=2, fill_color=RED, fill_opacity=0.07)
        warning_box.move_to([SAFE_CENTER_X, -0.95, 0])
        warning = txt("가맹 매출  ≠  이익·현금흐름", 35, BONE, "BOLD").move_to(warning_box)
        source = source_chip("SEC XBRL R26 · USD billions")
        group = VGroup(header, title, total, rent, royalty, fee, rent_label, royalty_label, fees_label, warning_box, warning, source)

        self.play(FadeIn(VGroup(header, title, total)), run_time=0.5)
        self.play(LaggedStart(FadeIn(rent, shift=RIGHT * 0.25), FadeIn(royalty, shift=RIGHT * 0.25), FadeIn(fee), lag_ratio=0.18), run_time=1.5)
        self.play(LaggedStart(FadeIn(rent_label), FadeIn(royalty_label), FadeIn(fees_label), lag_ratio=0.08), FadeIn(warning_box), FadeIn(warning), FadeIn(source), run_time=0.8)
        self.wait(3.7)
        self.play(FadeOut(group), run_time=0.6)

    def scene_dividend(self) -> None:
        header = section_label("05", "dividend record")
        title = left_align(txt("배당은 오래 버텼다", 54, BONE, "BOLD"), 5.6)
        years = txt("49년", 116, BRASS, "BOLD")
        left_align(years, 4.0)
        descriptor = txt("연속 연간 인상", 37, FOG, "BOLD").next_to(years, RIGHT, buff=0.25)

        x_left, x_right, y = SAFE_LEFT, SAFE_RIGHT - 0.1, 2.45
        timeline = Line([x_left, y, 0], [x_right, y, 0], color=SLATE, stroke_width=4)
        ticks = VGroup()
        for index, year in enumerate([1976, 1985, 1995, 2005, 2015, 2025]):
            x = x_left + index / 5 * (x_right - x_left)
            tick = Line([x, y - 0.14, 0], [x, y + 0.14, 0], color=BRASS if year in {1976, 2025} else SLATE, stroke_width=4)
            label = txt(str(year), 22, BRASS if year in {1976, 2025} else SLATE).move_to([x, y - 0.42, 0])
            ticks.add(tick, label)

        metrics = VGroup(
            txt("분기  $1.86", 36, FOG, "BOLD"),
            txt("연환산  $7.44", 36, FOG, "BOLD"),
            txt("수익률  2.86%*", 36, BRASS, "BOLD"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        left_align(metrics, 0.65)
        qualifier = txt("*$260.06 기준 단순 계산 · 미래 배당 보장 아님", 25, SLATE)
        left_align(qualifier, -1.05)
        source = source_chip("McDonald's dividend release · 시장 종가 계산")
        group = VGroup(header, title, years, descriptor, timeline, ticks, metrics, qualifier, source)

        self.play(FadeIn(VGroup(header, title, years, descriptor)), run_time=0.5)
        self.play(Create(timeline), LaggedStart(*[FadeIn(item) for item in ticks], lag_ratio=0.03), run_time=1.5)
        self.play(LaggedStart(*[FadeIn(item, shift=UP * 0.1) for item in metrics], lag_ratio=0.08), FadeIn(qualifier), FadeIn(source), run_time=1.0)
        self.wait(3.8)
        self.play(FadeOut(group), run_time=0.6)

    def scene_risks(self) -> None:
        header = section_label("06", "what can break the thesis")
        title = left_align(txt("싸 보여도 검증은 남는다", 52, BONE, "BOLD"), 5.55)
        debt = txt("$39.863B", 108, RED, "BOLD")
        left_align(debt, 4.15)
        debt_label = left_align(txt("장기부채", 34, SLATE, "BOLD"), 3.05)

        divider = Line([SAFE_LEFT, 2.55, 0], [SAFE_RIGHT - 0.1, 2.55, 0], color=SLATE, stroke_opacity=0.45, stroke_width=2)
        risk_values = [
            ("01", "임대료는 이익이 아니다"),
            ("02", "미국 객수는 감소했다"),
            ("03", "배당은 현금흐름이 지탱해야 한다"),
        ]
        risks = VGroup()
        for index, (number, value) in enumerate(risk_values):
            n = txt(number, 25, BRASS, "BOLD")
            rule = Line(ORIGIN, RIGHT * 0.55, color=SLATE, stroke_width=2)
            label = txt(value, 35, FOG, "BOLD")
            row = VGroup(n, rule, label).arrange(RIGHT, buff=0.18)
            left_align(row, 1.8 - index * 1.05)
            risks.add(row)
        source = source_chip("SEC · MCD Q2 2026 10-Q · 판단 체크리스트")
        group = VGroup(header, title, debt, debt_label, divider, risks, source)

        self.play(FadeIn(VGroup(header, title)), run_time=0.5)
        self.play(FadeIn(debt, shift=UP * 0.12), FadeIn(debt_label), Create(divider), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(row, shift=RIGHT * 0.12) for row in risks], lag_ratio=0.16), FadeIn(source), run_time=1.2)
        self.wait(6.6)
        self.play(FadeOut(group), run_time=0.6)

    def scene_close(self, photo: Path) -> None:
        image = cover_image(photo, 0.46)
        shade = Rectangle(width=9, height=16, fill_color=BLACK, fill_opacity=0.35, stroke_opacity=0)
        top_rule = Line(ORIGIN, RIGHT * 1.2, color=BRASS, stroke_width=6)
        line_one = txt("하락률은 가격", 65, BONE, "BOLD")
        line_two = txt("임대료·로열티는 사업", 65, BRASS, "BOLD")
        end = VGroup(top_rule, line_one, line_two).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        left_align(end, 2.1)
        footer = txt("2026.08.27 US CLOSE  ·  교육용 연구  ·  투자 조언 아님", 24, FOG, "BOLD")
        left_align(footer, -1.65)
        credit = source_chip(asset_credit(photo))
        credit.shift(DOWN * 0.65)

        self.add(image, shade)
        self.play(
            FadeIn(VGroup(end, footer, credit), shift=UP * 0.14),
            image.animate.scale(1.012),
            run_time=0.8,
        )
        self.play(image.animate.scale(1.02), run_time=4.2, rate_func=linear)
