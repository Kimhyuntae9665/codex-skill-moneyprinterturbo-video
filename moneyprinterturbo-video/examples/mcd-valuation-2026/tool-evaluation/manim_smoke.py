from manim import *


CARBON = "#0E1113"
BONE = "#F4F0E8"
SLATE = "#7B848A"
BRASS = "#BA8F73"
BRICK = "#D23A34"
MINT = "#7EC8A2"
GRID = "#334047"


class MCDValuationSmoke(Scene):
    """A 4.8 s vertical editorial chart smoke test.

    The price values are the raw-close figures from the parent brief. They are
    intentionally presented as a visual study, not as a live quote.
    """

    def construct(self):
        self.camera.background_color = CARBON

        eyebrow = Text(
            "MCD / PRICE STUDY",
            font="Consolas",
            font_size=22,
            weight=BOLD,
            color=SLATE,
        )
        eyebrow.to_edge(UP, buff=1.08).to_edge(LEFT, buff=0.72)
        eyebrow.shift(RIGHT * 0.60)

        title = Text(
            "맥도날드 주가",
            font="Malgun Gothic",
            font_size=52,
            weight=BOLD,
            color=BONE,
        )
        title.next_to(eyebrow, DOWN, buff=0.17).align_to(eyebrow, LEFT)
        title.shift(RIGHT * 0.60)

        subtitle = Text(
            "정말 싸졌을까?",
            font="Malgun Gothic",
            font_size=34,
            color=BRASS,
        )
        subtitle.next_to(title, DOWN, buff=0.08).align_to(title, LEFT)
        subtitle.shift(RIGHT * 0.60)

        period = Text(
            "RAW CLOSE · 2026",
            font="Consolas",
            font_size=20,
            weight=BOLD,
            color=SLATE,
        )
        period.to_edge(UP, buff=1.13).to_edge(RIGHT, buff=0.72)
        period.shift(LEFT * 2.40)

        rule = Line(
            start=np.array([-3.65, 5.22, 0]),
            end=np.array([3.65, 5.22, 0]),
            color=GRID,
            stroke_width=2,
        )

        price = Text(
            "341.06  →  260.06",
            font="Consolas",
            font_size=36,
            weight=BOLD,
            color=BONE,
        )
        price.move_to(np.array([-1.55, 4.32, 0]))

        delta = Text(
            "−23.8%",
            font="Consolas",
            font_size=40,
            weight=BOLD,
            color=BRICK,
        )
        delta.move_to(np.array([2.80, 4.32, 0]))

        chart_left = -3.35
        chart_right = 3.35
        chart_bottom = -2.95
        chart_top = 0.85

        horizontal_grid = VGroup(
            *[
                Line(
                    start=np.array([chart_left, y, 0]),
                    end=np.array([chart_right, y, 0]),
                    color=GRID,
                    stroke_width=1.5,
                    stroke_opacity=0.72,
                )
                for y in [-2.95, -2.00, -1.05, -0.10, 0.85]
            ]
        )
        vertical_grid = VGroup(
            *[
                Line(
                    start=np.array([x, chart_bottom, 0]),
                    end=np.array([x, chart_top, 0]),
                    color=GRID,
                    stroke_width=1.5,
                    stroke_opacity=0.44,
                )
                for x in [-3.35, -1.675, 0, 1.675, 3.35]
            ]
        )

        date_left = Text(
            "FEB 27",
            font="Consolas",
            font_size=18,
            color=SLATE,
        )
        date_left.move_to(np.array([-2.85, -3.32, 0]))
        date_right = Text(
            "AUG 27",
            font="Consolas",
            font_size=18,
            color=SLATE,
        )
        date_right.move_to(np.array([2.8, -3.32, 0]))

        points = [
            np.array([-3.35, 0.56, 0]),
            np.array([-2.72, 0.37, 0]),
            np.array([-2.05, 0.02, 0]),
            np.array([-1.30, -0.34, 0]),
            np.array([-0.62, -0.57, 0]),
            np.array([0.12, -1.03, 0]),
            np.array([0.85, -1.32, 0]),
            np.array([1.47, -1.70, 0]),
            np.array([2.18, -2.16, 0]),
            np.array([2.76, -2.60, 0]),
            np.array([3.35, -2.85, 0]),
        ]
        graph = VMobject(color=MINT, stroke_width=7)
        graph.set_points_smoothly(points)
        glow = graph.copy().set_stroke(color=MINT, width=22, opacity=0.12)

        start_dot = Dot(points[0], radius=0.095, color=BONE)
        end_dot = Dot(points[-1], radius=0.12, color=BRICK)
        end_ring = Circle(
            radius=0.22,
            color=BRICK,
            stroke_width=3,
            fill_opacity=0,
        ).move_to(points[-1])

        start_label = Text(
            "341.06",
            font="Consolas",
            font_size=22,
            weight=BOLD,
            color=BONE,
        )
        start_label.next_to(start_dot, UP, buff=0.16).align_to(start_dot, LEFT)

        end_label = Text(
            "260.06",
            font="Consolas",
            font_size=22,
            weight=BOLD,
            color=BRICK,
        )
        end_label.next_to(end_dot, UP, buff=0.16).align_to(end_dot, RIGHT)
        end_label.shift(LEFT * 0.50)

        note = Text(
            "비조정 종가 · 교육용 편집 프레임",
            font="Malgun Gothic",
            font_size=23,
            color=SLATE,
        )
        note.move_to(np.array([0, -3.98, 0]))

        footer = Text(
            "하락률은 가격, 평가는 구간으로 봅니다",
            font="Malgun Gothic",
            font_size=30,
            weight=BOLD,
            color=BONE,
        )
        footer.move_to(np.array([0, -6.38, 0]))
        footer_note = Text(
            "교육용 시각화 · 투자 조언 아님",
            font="Malgun Gothic",
            font_size=20,
            color=SLATE,
        )
        footer_note.move_to(np.array([0, -7.10, 0]))

        self.play(
            FadeIn(eyebrow, shift=0.10 * UP),
            FadeIn(period, shift=0.10 * UP),
            FadeIn(title, shift=0.10 * UP),
            FadeIn(subtitle, shift=0.10 * UP),
            run_time=0.45,
        )
        self.play(Create(rule), run_time=0.30)
        self.play(
            FadeIn(price, shift=0.08 * RIGHT),
            FadeIn(delta, shift=0.08 * LEFT),
            run_time=0.40,
        )
        self.play(
            LaggedStart(
                *[Create(line) for line in horizontal_grid],
                *[Create(line) for line in vertical_grid],
                lag_ratio=0.04,
                run_time=0.48,
            ),
            FadeIn(date_left),
            FadeIn(date_right),
        )
        self.play(
            Create(glow, rate_func=rate_functions.linear),
            Create(graph, rate_func=rate_functions.linear),
            run_time=2.05,
        )
        self.play(
            GrowFromCenter(start_dot),
            GrowFromCenter(end_dot),
            Create(end_ring),
            FadeIn(start_label, shift=0.06 * UP),
            FadeIn(end_label, shift=0.06 * DOWN),
            run_time=0.48,
        )
        self.play(FadeIn(note), run_time=0.25)
        self.play(
            FadeIn(footer, shift=0.08 * UP),
            FadeIn(footer_note, shift=0.08 * UP),
            run_time=0.35,
        )
        self.wait(0.55)
