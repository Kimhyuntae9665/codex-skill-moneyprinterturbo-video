from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
from manim import (
    Arc,
    BackgroundRectangle,
    Circle,
    Create,
    DashedLine,
    Dot,
    DOWN,
    FadeIn,
    FadeOut,
    Group,
    GrowFromEdge,
    LEFT,
    Line,
    MoveAlongPath,
    ORIGIN,
    PI,
    Polygon,
    Rectangle,
    RIGHT,
    RoundedRectangle,
    Scene,
    Text,
    UP,
    VGroup,
    VMobject,
    config,
    linear,
)

from mcd_short import (
    ASSETS,
    BONE,
    BRASS,
    CARBON,
    FOG,
    RED,
    RESEARCH,
    SAFE_CENTER_X,
    SAFE_LEFT,
    SAFE_RIGHT,
    SLATE,
    asset_credit,
    asset_photos,
    cover_image,
    left_align,
    price_points,
    section_label,
    txt,
)


config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 30
config.background_color = CARBON

ELECTRIC = "#46C7F4"
GOLD = "#D5A66F"
DEEP_RED = "#8B2424"
GRID = "#374047"
QUIET = "#080A0C"
SOURCE_SAFE_Y = -1.42
CAPTION_BAND_TOP = -2.28


def load_metrics() -> dict[str, object]:
    path = RESEARCH / "v3_metrics.json"
    metrics = json.loads(path.read_text(encoding="utf-8"))
    risk = metrics["risk_metrics"]
    returns = metrics["shareholder_return"]
    checks = {
        "mcd beta": (risk["mcd_beta_vs_spy"], 0.4767),
        "qqq beta": (risk["qqq_beta_vs_spy"], 1.2516),
        "mcd qqq correlation": (risk["mcd_qqq_correlation"], 0.3274),
        "shareholder yield": (returns["total_cash_shareholder_yield"], 0.0397),
    }
    for label, (actual, expected) in checks.items():
        if round(float(actual), 4) != expected:
            raise ValueError(f"unexpected v4 inherited {label}: {actual}")
    return metrics


def load_dividend_metrics() -> dict[str, object]:
    path = RESEARCH / "v4_metrics.json"
    metrics = json.loads(path.read_text(encoding="utf-8"))
    current = metrics["current"]
    windows = metrics["windows"]
    checks = {
        "current yield": (current["ttm_yield_pct"], 2.8263),
        "2010 median": (windows["since_2010"]["median_yield_pct"], 2.5070),
        "2010 peak": (windows["since_2010"]["peak_yield_pct"], 3.5782),
    }
    for label, (actual, expected) in checks.items():
        if round(float(actual), 4) != expected:
            raise ValueError(f"unexpected v4 {label}: {actual}")
    if windows["since_2020"]["current_rank_high_to_low"] != 2:
        raise ValueError("unexpected v4 since-2020 rank")
    if windows["since_2023"]["current_rank_high_to_low"] != 1:
        raise ValueError("unexpected v4 since-2023 rank")
    return metrics


def dividend_yield_rows() -> list[tuple[str, float]]:
    path = RESEARCH / "dividend_yield_history_v4.csv"
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = [(row["month_end"], float(row["ttm_yield_pct"])) for row in csv.DictReader(handle)]
    if len(rows) != 200 or rows[-1][0] != "2026-08-27":
        raise ValueError("unexpected v4 dividend-yield history")
    return rows


def caption_safe_band() -> VGroup:
    band_height = 3.72
    band = Rectangle(
        width=9,
        height=band_height,
        fill_color=QUIET,
        fill_opacity=0.92,
        stroke_opacity=0,
    ).move_to([0, CAPTION_BAND_TOP - band_height / 2, 0])
    edge = Line(
        [-4.5, CAPTION_BAND_TOP, 0],
        [4.5, CAPTION_BAND_TOP, 0],
        color=SLATE,
        stroke_width=1,
        stroke_opacity=0.18,
    )
    return VGroup(band, edge)


def source_chip_safe(value: str) -> VGroup:
    label = txt(value, 21, FOG)
    rule = Line(LEFT * 0.28, RIGHT * 0.28, color=BRASS, stroke_width=3)
    content = VGroup(rule, label).arrange(RIGHT, buff=0.16)
    if content.width > SAFE_RIGHT - SAFE_LEFT - 0.24:
        content.scale_to_fit_width(SAFE_RIGHT - SAFE_LEFT - 0.24)
    background = BackgroundRectangle(content, color=CARBON, fill_opacity=0.82, buff=0.1)
    group = VGroup(background, content)
    group.move_to([SAFE_LEFT + group.width / 2, SOURCE_SAFE_Y, 0])
    return group


def weekly_returns() -> tuple[list[float], list[float]]:
    path = RESEARCH / "weekly_adjusted_prices_v3.csv"
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 262:
        raise ValueError(f"expected 262 aligned weekly price rows, found {len(rows)}")
    mcd_prices = [float(row["MCD"]) for row in rows]
    qqq_prices = [float(row["QQQ"]) for row in rows]
    mcd = [current / prior - 1 for prior, current in zip(mcd_prices, mcd_prices[1:])]
    qqq = [current / prior - 1 for prior, current in zip(qqq_prices, qqq_prices[1:])]
    return mcd, qqq


def ambient_grid(accent: str = BRASS, opacity: float = 0.1) -> VGroup:
    verticals = [
        Line([x, -2.1, 0], [x, 6.2, 0], color=GRID, stroke_width=1, stroke_opacity=opacity)
        for x in np.linspace(SAFE_LEFT, SAFE_RIGHT - 0.1, 8)
    ]
    horizontals = [
        Line([SAFE_LEFT, y, 0], [SAFE_RIGHT - 0.1, y, 0], color=GRID, stroke_width=1, stroke_opacity=opacity)
        for y in np.linspace(-1.4, 5.7, 8)
    ]
    slash = Polygon(
        [-4.5, 4.7, 0],
        [-3.95, 5.35, 0],
        [3.4, -2.0, 0],
        [2.85, -2.55, 0],
        fill_color=accent,
        fill_opacity=0.025,
        stroke_opacity=0,
    )
    return VGroup(*verticals, *horizontals, slash)


def glow_line(start: list[float], end: list[float], color: str, width: float = 5) -> VGroup:
    return VGroup(
        Line(start, end, color=color, stroke_width=width * 3, stroke_opacity=0.08),
        Line(start, end, color=color, stroke_width=width * 1.8, stroke_opacity=0.16),
        Line(start, end, color=color, stroke_width=width),
    )


def metric_panel(title: str, value: str, x: float, color: str) -> VGroup:
    box = RoundedRectangle(
        width=2.9,
        height=1.55,
        corner_radius=0.12,
        stroke_color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=0.055,
    )
    box.move_to([x, 0.1, 0])
    label = txt(title, 22, SLATE, "BOLD").move_to([x, 0.52, 0])
    number = txt(value, 55, color, "BOLD").move_to([x, -0.05, 0])
    return VGroup(box, label, number)


def return_wave(values: list[float], y: float, color: str) -> VMobject:
    sample = values[-78:]
    limit = max(np.percentile(np.abs(sample), 94), 0.01)
    points = []
    for index, value in enumerate(sample):
        x = SAFE_LEFT + index / (len(sample) - 1) * (SAFE_RIGHT - 0.1 - SAFE_LEFT)
        clipped = max(-limit, min(limit, value))
        points.append([x, y + clipped / limit * 0.23, 0])
    path = VMobject(color=color, stroke_width=3)
    path.set_points_as_corners(points)
    return path


class MCDDividendYieldShort(Scene):
    def construct(self) -> None:
        photo_one, photo_two = asset_photos()
        metrics = load_metrics()
        dividend_metrics = load_dividend_metrics()
        yield_rows = dividend_yield_rows()
        mcd_returns, qqq_returns = weekly_returns()
        prices = price_points()

        self.scene_hook(photo_one)
        self.scene_valuation(prices)
        self.scene_cash_engine()
        self.scene_shareholder_return(metrics)
        self.scene_dividend_yield(dividend_metrics, yield_rows)
        self.scene_market_rhythm(metrics, mcd_returns, qqq_returns)
        self.scene_risk(metrics)
        self.scene_close(photo_two)

    def scene_hook(self, photo: Path) -> None:
        image = cover_image(photo, 0.5)
        shade = Rectangle(width=9, height=16, fill_color="#000000", fill_opacity=0.34, stroke_opacity=0)
        grid = ambient_grid(BRASS, 0.13)
        left_band = Polygon(
            [-4.5, 8, 0],
            [-1.6, 8, 0],
            [-4.5, 3.7, 0],
            fill_color=CARBON,
            fill_opacity=0.75,
            stroke_opacity=0,
        )
        eyebrow = txt("MCD // INCOME SIGNAL v4", 24, GOLD, "BOLD")
        headline = VGroup(
            txt("싼 MCD", 78, BONE, "BOLD"),
            txt("기술주와", 67, BONE, "BOLD"),
            txt("왜 다를까?", 67, ELECTRIC, "BOLD"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        stack = VGroup(eyebrow, Line(ORIGIN, RIGHT * 1.05, color=GOLD, stroke_width=6), headline).arrange(
            DOWN, aligned_edge=LEFT, buff=0.24
        )
        left_align(stack, 2.0)
        tags = VGroup(
            txt("RENT", 21, BRASS, "BOLD"),
            txt("ROYALTY", 21, FOG, "BOLD"),
            txt("BETA", 21, ELECTRIC, "BOLD"),
        ).arrange(RIGHT, buff=0.3)
        left_align(tags, -0.55)
        scan = Line([-4.1, 5.7, 0], [-4.1, -0.9, 0], color=ELECTRIC, stroke_width=2, stroke_opacity=0.65)
        credit = source_chip_safe(asset_credit(photo))
        safe_band = caption_safe_band()

        self.add(image, shade, left_band, grid, safe_band)
        self.play(FadeIn(VGroup(stack, tags, credit), shift=UP * 0.12), Create(scan), run_time=0.6)
        self.play(scan.animate.shift(RIGHT * 6.7), image.animate.scale(1.025), run_time=1.3, rate_func=linear)
        self.play(FadeOut(Group(image, shade, left_band, grid, safe_band, stack, tags, scan, credit)), run_time=0.4)

    def scene_valuation(self, rows: list[tuple[object, float]]) -> None:
        grid = ambient_grid(RED, 0.08)
        safe_band = caption_safe_band()
        header = section_label("01", "valuation reset")
        title = left_align(txt("가격은 싸졌다", 55, BONE, "BOLD"), 5.55)
        values = [row[1] for row in rows]
        x_left, x_right = SAFE_LEFT, SAFE_RIGHT - 0.1
        y_bottom, y_top = 2.05, 4.55
        low, high = min(values), max(values)
        points = [
            [
                x_left + index / (len(values) - 1) * (x_right - x_left),
                y_bottom + (value - low) / (high - low) * (y_top - y_bottom),
                0,
            ]
            for index, value in enumerate(values)
        ]
        chart = VGroup(*[Line(points[i], points[i + 1], color=RED, stroke_width=5) for i in range(len(points) - 1)])
        ghost = txt("-23.8", 132, RED, "BOLD").set_opacity(0.06)
        ghost.move_to([0.0, 3.25, 0])
        start_label = txt("$341.06", 23, BONE, "BOLD").move_to(
            [points[0][0] + 0.48, points[0][1] - 0.45, 0]
        )
        end_label = txt("$260.06", 23, RED, "BOLD").move_to(
            [points[-1][0] - 0.55, points[-1][1] + 0.48, 0]
        )
        start_back = BackgroundRectangle(start_label, color=CARBON, fill_opacity=0.9, buff=0.07, stroke_opacity=0)
        end_back = BackgroundRectangle(end_label, color=CARBON, fill_opacity=0.9, buff=0.07, stroke_opacity=0)
        endpoints = VGroup(
            Dot(points[0], radius=0.08, color=BONE),
            Dot(points[-1], radius=0.1, color=RED),
            start_back,
            end_back,
            start_label,
            end_label,
        )
        decline = metric_panel("6M RAW CLOSE", "-23.8%", -2.08, RED)
        pe = metric_panel("TTM P/E", "21.1×", 1.0, GOLD)
        low_zone = txt("최근 5년 저점권  ·  장기 역사적 바닥 단정 금지", 25, SLATE, "BOLD")
        left_align(low_zone, -0.62)
        source = source_chip_safe("ChartExchange · StockResearch · 동일 기준 계산")
        group = VGroup(safe_band, grid, header, title, ghost, chart, endpoints, decline, pe, low_zone, source)

        self.add(grid, ghost, safe_band)
        self.play(FadeIn(VGroup(header, title)), run_time=0.45)
        self.play(Create(chart), FadeIn(endpoints), run_time=1.1)
        self.play(FadeIn(decline, shift=UP * 0.12), FadeIn(pe, shift=UP * 0.12), FadeIn(low_zone), FadeIn(source), run_time=0.65)
        self.wait(1.75)
        self.play(FadeOut(group), run_time=0.45)

    def scene_cash_engine(self) -> None:
        grid = ambient_grid(BRASS, 0.09)
        safe_band = caption_safe_band()
        header = section_label("02", "real-estate cash engine")
        title = left_align(txt("가맹점에서 두 갈래 현금", 49, BONE, "BOLD"), 5.55)

        building = RoundedRectangle(
            width=2.25,
            height=1.72,
            corner_radius=0.12,
            stroke_color=BRASS,
            stroke_width=4,
            fill_color=BRASS,
            fill_opacity=0.055,
        ).move_to([-2.47, 3.1, 0])
        facade = VGroup(
            Line([-3.25, 3.52, 0], [-1.69, 3.52, 0], color=BRASS, stroke_width=2),
            Line([-3.25, 3.04, 0], [-1.69, 3.04, 0], color=BRASS, stroke_width=2),
            Line([-2.47, 2.25, 0], [-2.47, 3.95, 0], color=BRASS, stroke_width=2),
        )
        store_count = txt("46,028", 39, BONE, "BOLD").move_to([-2.47, 3.15, 0])
        store_label = txt("STORES", 18, SLATE, "BOLD").move_to([-2.47, 2.62, 0])
        junction = Dot([-0.65, 3.1, 0], radius=0.1, color=BONE)
        trunk = glow_line([-1.34, 3.1, 0], [-0.65, 3.1, 0], BRASS, 4)
        rent_flow = glow_line([-0.65, 3.1, 0], [0.15, 3.85, 0], BRASS, 4)
        royalty_flow = glow_line([-0.65, 3.1, 0], [0.15, 2.25, 0], ELECTRIC, 4)

        rent_box = RoundedRectangle(width=2.3, height=1.12, corner_radius=0.1, stroke_color=BRASS, fill_color=BRASS, fill_opacity=0.06)
        rent_box.move_to([1.28, 3.85, 0])
        rent_text = VGroup(txt("임대료", 25, BRASS, "BOLD"), txt("$5.264B", 38, BONE, "BOLD")).arrange(DOWN, buff=0.05).move_to(rent_box)
        royalty_box = RoundedRectangle(width=2.3, height=1.12, corner_radius=0.1, stroke_color=ELECTRIC, fill_color=ELECTRIC, fill_opacity=0.055)
        royalty_box.move_to([1.28, 2.25, 0])
        royalty_text = VGroup(txt("로열티", 25, ELECTRIC, "BOLD"), txt("$3.096B", 38, BONE, "BOLD")).arrange(DOWN, buff=0.05).move_to(royalty_box)

        rail = RoundedRectangle(width=6.15, height=0.72, corner_radius=0.08, stroke_color=SLATE, stroke_width=2)
        rail.move_to([SAFE_CENTER_X, 0.75, 0])
        fill = Rectangle(width=6.15 * 0.956, height=0.66, fill_color=BRASS, fill_opacity=0.95, stroke_opacity=0)
        fill.move_to([rail.get_left()[0] + fill.width / 2, 0.75, 0])
        franchise = txt("약 95% 가맹", 38, CARBON, "BOLD").move_to(fill)
        warning = txt("가맹 매출  ≠  이익·FCF", 28, RED, "BOLD")
        left_align(warning, -0.35)
        source = source_chip_safe("SEC 10-Q · 2026 H1 · XBRL R26")
        group = VGroup(
            safe_band, grid, header, title, building, facade, store_count, store_label, junction, trunk,
            rent_flow, royalty_flow, rent_box, rent_text, royalty_box, royalty_text,
            rail, fill, franchise, warning, source,
        )

        self.add(grid, safe_band)
        self.play(FadeIn(VGroup(header, title)), Create(building), Create(facade), FadeIn(VGroup(store_count, store_label)), run_time=0.5)
        self.play(Create(trunk), Create(rent_flow), Create(royalty_flow), FadeIn(junction), run_time=1.0)
        self.play(FadeIn(VGroup(rent_box, rent_text), shift=RIGHT * 0.12), FadeIn(VGroup(royalty_box, royalty_text), shift=RIGHT * 0.12), Create(rail), GrowFromEdge(fill, LEFT), FadeIn(franchise), FadeIn(warning), FadeIn(source), run_time=1.1)
        self.wait(3.8)
        self.play(FadeOut(group), run_time=0.5)

    def scene_shareholder_return(self, metrics: dict[str, object]) -> None:
        data = metrics["shareholder_return"]
        grid = ambient_grid(GOLD, 0.09)
        safe_band = caption_safe_band()
        header = section_label("03", "shareholder return")
        title = left_align(txt("현금은 주주에게도 흐른다", 49, BONE, "BOLD"), 5.55)

        center = [-1.35, 2.55, 0]
        ring = Circle(radius=1.58, color=SLATE, stroke_width=16, stroke_opacity=0.25).move_to(center)
        dividend_angle = -2 * PI * (float(data["dividend_cash_yield"]) / 0.05)
        buyback_angle = -2 * PI * (float(data["net_buyback_cash_yield"]) / 0.05)
        dividend_arc = Arc(radius=1.58, start_angle=PI / 2, angle=dividend_angle, color=BRASS, stroke_width=18).move_arc_center_to(center)
        buyback_arc = Arc(radius=1.58, start_angle=PI / 2 + dividend_angle, angle=buyback_angle, color=ELECTRIC, stroke_width=18).move_arc_center_to(center)
        total = txt("4.0%", 69, BONE, "BOLD").move_to([center[0], center[1] + 0.12, 0])
        total_label = txt("현금 주주환원률*", 21, SLATE, "BOLD").move_to([center[0], center[1] - 0.55, 0])

        streak_box = RoundedRectangle(width=1.85, height=3.15, corner_radius=0.12, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=0.045)
        streak_box.move_to([1.45, 2.55, 0])
        streak = VGroup(
            txt("50", 79, GOLD, "BOLD"),
            txt("YEARS", 21, SLATE, "BOLD"),
            Line(LEFT * 0.55, RIGHT * 0.55, color=GOLD, stroke_width=3),
            txt("연속 배당", 24, BONE, "BOLD"),
            txt("인상", 24, BONE, "BOLD"),
        ).arrange(DOWN, buff=0.09).move_to(streak_box)

        dividend_row = VGroup(
            Line(ORIGIN, RIGHT * 0.45, color=BRASS, stroke_width=8),
            txt("배당", 27, SLATE, "BOLD"),
            txt("$5.225B", 38, BONE, "BOLD"),
            txt("2.84%", 28, BRASS, "BOLD"),
        ).arrange(RIGHT, buff=0.18)
        left_align(dividend_row, 0.55)
        buyback_row = VGroup(
            Line(ORIGIN, RIGHT * 0.45, color=ELECTRIC, stroke_width=8),
            txt("순현금 매입", 27, SLATE, "BOLD"),
            txt("$2.086B", 38, BONE, "BOLD"),
            txt("1.13%", 28, ELECTRIC, "BOLD"),
        ).arrange(RIGHT, buff=0.18)
        left_align(buyback_row, -0.02)
        qualifier = txt("*TTM 현금 / 현재 시총 근사 · 비현금 희석 전체 미반영", 23, SLATE, "BOLD")
        left_align(qualifier, -0.72)
        source = source_chip_safe("SEC cash flows · FY2025 + H1'26 - H1'25")
        group = VGroup(
            safe_band, grid, header, title, ring, dividend_arc, buyback_arc, total, total_label,
            streak_box, streak, dividend_row, buyback_row, qualifier, source,
        )

        self.add(grid, safe_band)
        self.play(FadeIn(VGroup(header, title, ring, streak_box)), run_time=0.5)
        self.play(Create(dividend_arc), Create(buyback_arc), FadeIn(VGroup(total, total_label)), run_time=1.25)
        self.play(FadeIn(dividend_row, shift=RIGHT * 0.12), FadeIn(buyback_row, shift=RIGHT * 0.12), run_time=0.75)
        self.play(FadeIn(streak, shift=UP * 0.1), FadeIn(qualifier), FadeIn(source), run_time=0.7)
        self.wait(5.95)
        self.play(FadeOut(group), run_time=0.45)

    def scene_dividend_yield(
        self,
        metrics: dict[str, object],
        rows: list[tuple[str, float]],
    ) -> None:
        grid = ambient_grid(GOLD, 0.07)
        safe_band = caption_safe_band()
        header = section_label("04", "dividend yield history")
        title = left_align(txt("배당수익률, 최근엔 높다", 44, BONE, "BOLD"), 5.62)

        current = float(metrics["current"]["ttm_yield_pct"])
        median = float(metrics["windows"]["since_2010"]["median_yield_pct"])
        x_left, x_right = SAFE_LEFT, SAFE_RIGHT - 0.16
        y_bottom, y_top = 1.48, 4.72
        y_min, y_max = 1.8, 3.75

        def value_y(value: float) -> float:
            return y_bottom + (value - y_min) / (y_max - y_min) * (y_top - y_bottom)

        values = [value for _, value in rows]
        points = [
            [
                x_left + index / (len(rows) - 1) * (x_right - x_left),
                value_y(value),
                0,
            ]
            for index, value in enumerate(values)
        ]
        area = Polygon(
            [x_left, y_bottom, 0],
            *points,
            [x_right, y_bottom, 0],
            fill_color=GOLD,
            fill_opacity=0.085,
            stroke_opacity=0,
        )
        line_glow = VMobject(color=GOLD, stroke_width=13, stroke_opacity=0.09)
        line_glow.set_points_as_corners(points)
        chart = VMobject(color=GOLD, stroke_width=4)
        chart.set_points_as_corners(points)

        guides = VGroup()
        guide_labels = VGroup()
        for tick in (2.0, 2.5, 3.0, 3.5):
            y = value_y(tick)
            guides.add(Line([x_left, y, 0], [x_right, y, 0], color=GRID, stroke_width=1.5, stroke_opacity=0.65))
            guide_labels.add(txt(f"{tick:.1f}%", 18, SLATE, "BOLD").move_to([x_left - 0.35, y, 0]))

        median_y = value_y(median)
        median_line = DashedLine(
            [x_left, median_y, 0],
            [x_right, median_y, 0],
            color=ELECTRIC,
            dash_length=0.08,
            stroke_width=2,
            stroke_opacity=0.82,
        )
        median_label = txt(f"중앙값 {median:.2f}%", 20, ELECTRIC, "BOLD").move_to([1.58, median_y + 0.25, 0])

        peak_index = max(range(len(values)), key=values.__getitem__)
        peak_dot = Dot(points[peak_index], radius=0.08, color=GOLD)
        peak_label = txt("2015  3.58%", 21, GOLD, "BOLD").move_to(
            [points[peak_index][0] - 0.2, points[peak_index][1] + 0.37, 0]
        )
        current_dot = Dot(points[-1], radius=0.11, color=RED)
        current_tag = VGroup(
            txt("현재", 19, SLATE, "BOLD"),
            txt(f"{current:.2f}%", 45, BONE, "BOLD"),
        ).arrange(DOWN, buff=0.02).move_to([1.92, 4.96, 0])

        year_labels = VGroup()
        for year in (2010, 2015, 2020, 2025):
            index = next(index for index, (day, _) in enumerate(rows) if day.startswith(str(year)))
            x = x_left + index / (len(rows) - 1) * (x_right - x_left)
            year_labels.add(txt(str(year), 18, SLATE, "BOLD").move_to([x, 1.18, 0]))

        rank_data = [
            ("2020년 이후", "2 / 80", RED),
            ("2023년 이후", "1 / 44", ELECTRIC),
            ("2010년 이후", "상위 37%", GOLD),
        ]
        cards = VGroup()
        for x, (label, value, color) in zip((-2.62, -0.55, 1.52), rank_data, strict=True):
            box = RoundedRectangle(
                width=1.9,
                height=1.0,
                corner_radius=0.09,
                stroke_color=color,
                stroke_width=2,
                fill_color=color,
                fill_opacity=0.045,
            ).move_to([x, 0.48, 0])
            content = VGroup(
                txt(label, 18, SLATE, "BOLD"),
                txt(value, 31, color, "BOLD"),
            ).arrange(DOWN, buff=0.08).move_to(box)
            cards.add(VGroup(box, content))

        conclusion = txt("최근 구간은 매력적  ·  장기 극단값은 아님", 25, BONE, "BOLD")
        left_align(conclusion, -0.48)
        source = source_chip_safe("Yahoo daily raw close + cash dividends · 월말 200개")
        group = VGroup(
            safe_band, grid, header, title, area, line_glow, chart, guides, guide_labels,
            median_line, median_label, peak_dot, peak_label, current_dot, current_tag,
            year_labels, cards, conclusion, source,
        )

        self.add(grid, safe_band)
        self.play(FadeIn(VGroup(header, title)), run_time=0.5)
        self.play(FadeIn(area), Create(guides), Create(median_line), FadeIn(VGroup(guide_labels, year_labels, median_label)), run_time=0.9)
        self.play(Create(line_glow), Create(chart), FadeIn(VGroup(peak_dot, peak_label, current_dot, current_tag)), run_time=0.8)
        self.play(FadeIn(cards, shift=UP * 0.12), FadeIn(conclusion), FadeIn(source), run_time=0.7)
        self.wait(11.2)
        self.play(FadeOut(group), run_time=0.5)

    def scene_market_rhythm(
        self,
        metrics: dict[str, object],
        mcd_returns: list[float],
        qqq_returns: list[float],
    ) -> None:
        risk = metrics["risk_metrics"]
        grid = ambient_grid(ELECTRIC, 0.09)
        safe_band = caption_safe_band()
        header = section_label("05", "market sensitivity")
        title = left_align(txt("같은 시장, 다른 속도", 53, BONE, "BOLD"), 5.55)

        base_y, top_y = 1.22, 4.62
        max_beta = 1.4
        beta_values = [
            ("MCD", float(risk["mcd_beta_vs_spy"]), -2.85, BRASS),
            ("SPY", 1.0, -0.55, FOG),
            ("QQQ", float(risk["qqq_beta_vs_spy"]), 1.75, ELECTRIC),
        ]
        rails = VGroup()
        bars = VGroup()
        labels = VGroup()
        for ticker, value, x, color in beta_values:
            rail = Line([x, base_y, 0], [x, top_y, 0], color=SLATE, stroke_width=18, stroke_opacity=0.18)
            value_y = base_y + value / max_beta * (top_y - base_y)
            bar = glow_line([x, base_y, 0], [x, value_y, 0], color, 10)
            ticker_label = txt(ticker, 25, color, "BOLD").move_to([x, base_y - 0.37, 0])
            value_label = txt(f"{value:.2f}", 37, BONE, "BOLD").move_to([x, value_y + 0.34, 0])
            rails.add(rail)
            bars.add(bar)
            labels.add(ticker_label, value_label)
        spy_y = base_y + 1.0 / max_beta * (top_y - base_y)
        benchmark = DashedLine([SAFE_LEFT, spy_y, 0], [SAFE_RIGHT - 0.1, spy_y, 0], color=FOG, dash_length=0.1, stroke_opacity=0.4)
        benchmark_label = txt("S&P 500 = 1.00", 20, FOG, "BOLD").move_to([SAFE_LEFT + 0.85, spy_y + 0.23, 0])

        mcd_wave = return_wave(mcd_returns, 0.3, BRASS)
        qqq_wave = return_wave(qqq_returns, -0.05, ELECTRIC)
        mcd_dot = Dot(mcd_wave.get_start(), radius=0.06, color=BRASS)
        qqq_dot = Dot(qqq_wave.get_start(), radius=0.06, color=ELECTRIC)
        corr_box = RoundedRectangle(width=4.05, height=0.62, corner_radius=0.08, stroke_color=ELECTRIC, stroke_width=2, fill_color=ELECTRIC, fill_opacity=0.045)
        corr_box.move_to([SAFE_CENTER_X, -0.62, 0])
        corr = txt("MCD ↔ QQQ  상관 0.33", 28, BONE, "BOLD").move_to(corr_box)
        source = source_chip_safe("Yahoo · 5Y weekly adj close · 261 returns · SPY benchmark")
        group = VGroup(
            safe_band, grid, header, title, rails, bars, labels, benchmark, benchmark_label,
            mcd_wave, qqq_wave, mcd_dot, qqq_dot, corr_box, corr, source,
        )

        self.add(grid, safe_band)
        self.play(FadeIn(VGroup(header, title)), run_time=0.45)
        self.play(Create(rails), Create(benchmark), FadeIn(benchmark_label), run_time=0.45)
        self.play(*[Create(bar) for bar in bars], FadeIn(labels), run_time=1.3)
        self.play(Create(mcd_wave), Create(qqq_wave), MoveAlongPath(mcd_dot, mcd_wave), MoveAlongPath(qqq_dot, qqq_wave), FadeIn(VGroup(corr_box, corr, source)), run_time=1.0)
        self.wait(4.75)
        self.play(FadeOut(group), run_time=0.45)

    def scene_risk(self, metrics: dict[str, object]) -> None:
        risk = metrics["risk_metrics"]
        grid = ambient_grid(RED, 0.09)
        safe_band = caption_safe_band()
        header = section_label("06", "risk check")
        title_one = left_align(txt("LOW BETA", 62, FOG, "BOLD"), 5.25)
        title_two = left_align(txt("≠  LOW RISK", 72, RED, "BOLD"), 4.3)
        divider = Line([SAFE_LEFT, 3.55, 0], [SAFE_RIGHT - 0.1, 3.55, 0], color=RED, stroke_width=3, stroke_opacity=0.6)

        debt_box = RoundedRectangle(width=2.92, height=1.55, corner_radius=0.1, stroke_color=RED, fill_color=RED, fill_opacity=0.055)
        debt_box.move_to([-2.08, 2.35, 0])
        debt = VGroup(txt("장기부채", 22, SLATE, "BOLD"), txt("$39.9B", 51, RED, "BOLD")).arrange(DOWN, buff=0.08).move_to(debt_box)
        traffic_box = RoundedRectangle(width=2.92, height=1.55, corner_radius=0.1, stroke_color=GOLD, fill_color=GOLD, fill_opacity=0.04)
        traffic_box.move_to([1.0, 2.35, 0])
        traffic = VGroup(txt("미국 객수", 22, SLATE, "BOLD"), txt("감소", 51, GOLD, "BOLD")).arrange(DOWN, buff=0.08).move_to(traffic_box)

        vol_title = left_align(txt("5년 주간 연환산 변동성", 26, SLATE, "BOLD"), 0.95)
        mcd_vol = float(risk["mcd_annualized_volatility"]) * 100
        spy_vol = float(risk["spy_annualized_volatility"]) * 100
        mcd_bar = glow_line([SAFE_LEFT, 0.38, 0], [SAFE_LEFT + 4.6 * mcd_vol / 22, 0.38, 0], BRASS, 6)
        spy_bar = glow_line([SAFE_LEFT, -0.08, 0], [SAFE_LEFT + 4.6 * spy_vol / 22, -0.08, 0], FOG, 6)
        vol_labels = VGroup(
            txt(f"MCD  {mcd_vol:.1f}%", 27, BRASS, "BOLD").move_to([1.75, 0.38, 0]),
            txt(f"SPY  {spy_vol:.1f}%", 27, FOG, "BOLD").move_to([1.75, -0.08, 0]),
        )
        qualifier = txt("베타는 시장 민감도 · 총위험이나 손실 보장치가 아님", 23, SLATE, "BOLD")
        left_align(qualifier, -0.72)
        source = source_chip_safe("SEC 10-Q · 2026 H1 · Yahoo 5Y weekly")
        group = VGroup(
            safe_band, grid, header, title_one, title_two, divider, debt_box, debt, traffic_box,
            traffic, vol_title, mcd_bar, spy_bar, vol_labels, qualifier, source,
        )

        self.add(grid, safe_band)
        self.play(FadeIn(VGroup(header, title_one, title_two)), run_time=0.45)
        self.play(Create(divider), FadeIn(VGroup(debt_box, debt, traffic_box, traffic), shift=UP * 0.12), run_time=0.7)
        self.play(FadeIn(vol_title), Create(mcd_bar), Create(spy_bar), FadeIn(vol_labels), FadeIn(qualifier), FadeIn(source), run_time=0.8)
        self.wait(4.2)
        self.play(FadeOut(group), run_time=0.45)

    def scene_close(self, photo: Path) -> None:
        image = cover_image(photo, 0.43)
        shade = Rectangle(width=9, height=16, fill_color="#000000", fill_opacity=0.43, stroke_opacity=0)
        grid = ambient_grid(BRASS, 0.13)
        safe_band = caption_safe_band()
        eyebrow = txt("MCD // INCOME + DEFENSE", 24, GOLD, "BOLD")
        left_align(eyebrow, 5.25)
        rows = VGroup()
        for index, (number, label, color) in enumerate(
            [
                ("01", "임대료 + 로열티", BRASS),
                ("02", "현금환원 약 4%", ELECTRIC),
                ("03", "배당수익률 2.83%", GOLD),
            ]
        ):
            n = txt(number, 24, color, "BOLD")
            rule = Line(ORIGIN, RIGHT * 1.0, color=color, stroke_width=4)
            value = txt(label, 38, BONE, "BOLD")
            row = VGroup(n, rule, value).arrange(RIGHT, buff=0.22)
            left_align(row, 3.9 - index * 0.95)
            rows.add(row)
        finale = left_align(txt("기술주와 다른 리듬", 62, BONE, "BOLD"), 0.25)
        finale_rule = glow_line([SAFE_LEFT, -0.55, 0], [SAFE_RIGHT - 0.1, -0.55, 0], BRASS, 4)
        footer = txt("2026.08.27 US CLOSE · 역사값 기반 · 교육용 연구 · 투자 조언 아님", 21, FOG, "BOLD")
        left_align(footer, -0.92)
        credit = source_chip_safe(asset_credit(photo))

        self.add(image, shade, grid, safe_band)
        self.play(FadeIn(VGroup(eyebrow, rows, finale, finale_rule, footer, credit), shift=UP * 0.12), image.animate.scale(1.014), run_time=0.7)
        self.play(image.animate.scale(1.025), run_time=5.4, rate_func=linear)
        self.wait(0.6)
