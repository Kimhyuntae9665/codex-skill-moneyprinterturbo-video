from __future__ import annotations

import argparse
import csv
from datetime import date, datetime, timezone
import json
from pathlib import Path
import statistics
from urllib.request import Request, urlopen

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
HISTORY = ROOT / "dividend_yield_history_v4.csv"
OUTPUT = ROOT / "v4_metrics.json"
CHART = ROOT / "dividend_yield_history_v4.png"
START = datetime(2008, 1, 1, tzinfo=timezone.utc)
END_EXCLUSIVE = datetime(2026, 8, 28, tzinfo=timezone.utc)
DISPLAY_START = date(2010, 1, 1)
EXPECTED_AS_OF = date(2026, 8, 27)


def yahoo_url() -> str:
    return (
        "https://query1.finance.yahoo.com/v8/finance/chart/MCD"
        f"?period1={int(START.timestamp())}"
        f"&period2={int(END_EXCLUSIVE.timestamp())}"
        "&interval=1d&events=div%2Csplits&includeAdjustedClose=true"
    )


def fetch_monthly_history() -> list[dict[str, object]]:
    request = Request(yahoo_url(), headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=45) as response:
        payload = json.load(response)
    result = payload["chart"]["result"][0]
    timestamps = result["timestamp"]
    closes = result["indicators"]["quote"][0]["close"]

    month_ends: dict[tuple[int, int], tuple[date, float]] = {}
    for timestamp, close in zip(timestamps, closes, strict=True):
        if close is None:
            continue
        trading_day = datetime.fromtimestamp(timestamp, tz=timezone.utc).date()
        if trading_day < DISPLAY_START:
            continue
        key = (trading_day.year, trading_day.month)
        previous = month_ends.get(key)
        if previous is None or trading_day > previous[0]:
            month_ends[key] = (trading_day, float(close))

    dividend_events = result.get("events", {}).get("dividends", {})
    dividends = sorted(
        (
            datetime.fromtimestamp(int(event["date"]), tz=timezone.utc).date(),
            float(event["amount"]),
        )
        for event in dividend_events.values()
    )

    rows: list[dict[str, object]] = []
    for month_end, raw_close in sorted(month_ends.values()):
        paid = [(day, amount) for day, amount in dividends if day <= month_end]
        if len(paid) < 4:
            continue
        trailing_four = paid[-4:]
        ttm_dividend = sum(amount for _, amount in trailing_four)
        rows.append(
            {
                "month_end": month_end.isoformat(),
                "raw_close_usd": raw_close,
                "ttm_dividend_usd": ttm_dividend,
                "ttm_yield_pct": ttm_dividend / raw_close * 100,
                "latest_dividend_usd": trailing_four[-1][1],
            }
        )
    if not rows or date.fromisoformat(str(rows[-1]["month_end"])) != EXPECTED_AS_OF:
        raise RuntimeError("Yahoo history does not end at the locked 2026-08-27 close")
    return rows


def save_history(rows: list[dict[str, object]]) -> None:
    with HISTORY.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            (
                "month_end",
                "raw_close_usd",
                "ttm_dividend_usd",
                "ttm_yield_pct",
                "latest_dividend_usd",
            )
        )
        for row in rows:
            writer.writerow(
                (
                    row["month_end"],
                    f'{float(row["raw_close_usd"]):.8f}',
                    f'{float(row["ttm_dividend_usd"]):.8f}',
                    f'{float(row["ttm_yield_pct"]):.8f}',
                    f'{float(row["latest_dividend_usd"]):.8f}',
                )
            )


def load_history() -> list[dict[str, object]]:
    with HISTORY.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return [
        {
            "month_end": row["month_end"],
            "raw_close_usd": float(row["raw_close_usd"]),
            "ttm_dividend_usd": float(row["ttm_dividend_usd"]),
            "ttm_yield_pct": float(row["ttm_yield_pct"]),
            "latest_dividend_usd": float(row["latest_dividend_usd"]),
        }
        for row in rows
    ]


def window_summary(rows: list[dict[str, object]], start_year: int) -> dict[str, object]:
    window = [row for row in rows if int(str(row["month_end"])[:4]) >= start_year]
    current = float(window[-1]["ttm_yield_pct"])
    values = [float(row["ttm_yield_pct"]) for row in window]
    rank = 1 + sum(value > current for value in values)
    peak = max(window, key=lambda row: float(row["ttm_yield_pct"]))
    return {
        "start": f"{start_year}-01-01",
        "observations": len(window),
        "median_yield_pct": statistics.median(values),
        "current_rank_high_to_low": rank,
        "top_share_pct": rank / len(window) * 100,
        "percentile_lower_or_equal_pct": sum(value <= current for value in values) / len(window) * 100,
        "peak_month_end": peak["month_end"],
        "peak_yield_pct": peak["ttm_yield_pct"],
    }


def compute(rows: list[dict[str, object]] | None = None) -> dict[str, object]:
    rows = rows or load_history()
    current = rows[-1]
    metrics = {
        "as_of": "2026-08-27 US close",
        "source_url": yahoo_url(),
        "method": {
            "frequency": "calendar-month final trading day",
            "price_basis": "Yahoo Finance unadjusted/raw close",
            "dividend_basis": "sum of the latest four cash-dividend events on or before each month-end",
            "yield_formula": "latest four cash dividends per share / raw month-end close",
            "interpretation": "historical cash dividend yield, not total return and not a forward guarantee",
        },
        "current": {
            "month_end": current["month_end"],
            "raw_close_usd": current["raw_close_usd"],
            "ttm_dividend_usd": current["ttm_dividend_usd"],
            "ttm_yield_pct": current["ttm_yield_pct"],
            "forward_dividend_usd": float(current["latest_dividend_usd"]) * 4,
            "forward_yield_pct": float(current["latest_dividend_usd"]) * 4 / float(current["raw_close_usd"]) * 100,
        },
        "windows": {
            "since_2010": window_summary(rows, 2010),
            "since_2015": window_summary(rows, 2015),
            "since_2020": window_summary(rows, 2020),
            "since_2023": window_summary(rows, 2023),
        },
        "video_conclusion": (
            "The 2.83% TTM yield is unusually high versus recent years: second-highest among "
            "80 month-ends since 2020 and highest since 2023. It is not an all-time extreme: "
            "it ranks 74th-highest of 200 month-ends since 2010, below the 2015 peak near 3.58%."
        ),
    }

    if round(float(metrics["current"]["ttm_yield_pct"]), 2) != 2.83:
        raise ValueError("unexpected current TTM yield")
    if metrics["windows"]["since_2020"]["current_rank_high_to_low"] != 2:
        raise ValueError("unexpected since-2020 rank")
    if metrics["windows"]["since_2023"]["current_rank_high_to_low"] != 1:
        raise ValueError("unexpected since-2023 rank")
    if metrics["windows"]["since_2010"]["observations"] != 200:
        raise ValueError("unexpected since-2010 observation count")
    return metrics


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    path = ROOT.parents[2] / "assets" / "fonts" / "NotoSansKR-Bold.ttf"
    try:
        return ImageFont.truetype(str(path), size=size)
    except OSError:
        return ImageFont.load_default()


def render_chart(rows: list[dict[str, object]], metrics: dict[str, object]) -> None:
    width, height = 1600, 900
    image = Image.new("RGB", (width, height), "#0E1113")
    draw = ImageDraw.Draw(image)
    left, top, right, bottom = 130, 150, 1510, 730
    values = [float(row["ttm_yield_pct"]) for row in rows]
    y_min, y_max = 1.8, 3.8

    draw.text((left, 42), "MCD 월말 TTM 배당수익률 · 2010–2026", font=font(50), fill="#F4F0E8")
    draw.text((left, 105), "최근 4회 현금배당 ÷ 비조정 월말 종가", font=font(25), fill="#7B848A")
    for tick in (2.0, 2.5, 3.0, 3.5):
        y = bottom - (tick - y_min) / (y_max - y_min) * (bottom - top)
        draw.line((left, y, right, y), fill="#374047", width=2)
        draw.text((35, y - 18), f"{tick:.1f}%", font=font(24), fill="#7B848A")
    points = []
    for index, value in enumerate(values):
        x = left + index / (len(values) - 1) * (right - left)
        y = bottom - (value - y_min) / (y_max - y_min) * (bottom - top)
        points.append((x, y))
    draw.line(points, fill="#D5A66F", width=7, joint="curve")

    median = float(metrics["windows"]["since_2010"]["median_yield_pct"])
    median_y = bottom - (median - y_min) / (y_max - y_min) * (bottom - top)
    draw.line((left, median_y, right, median_y), fill="#46C7F4", width=3)
    draw.text((right - 235, median_y - 38), f"중앙값 {median:.2f}%", font=font(23), fill="#46C7F4")

    current = float(metrics["current"]["ttm_yield_pct"])
    current_x, current_y = points[-1]
    draw.ellipse((current_x - 12, current_y - 12, current_x + 12, current_y + 12), fill="#D23A34")
    draw.text((current_x - 170, current_y - 72), f"현재 {current:.2f}%", font=font(27), fill="#F4F0E8")
    for year in (2010, 2015, 2020, 2025):
        index = next(i for i, row in enumerate(rows) if str(row["month_end"]).startswith(str(year)))
        x = left + index / (len(values) - 1) * (right - left)
        draw.text((x - 34, bottom + 25), str(year), font=font(23), fill="#7B848A")
    draw.text((left, 812), "현재: 2020년 이후 2/80 · 2023년 이후 1/44 · 2010년 이후 상위 약 37%", font=font(29), fill="#F4F0E8")
    image.save(CHART, optimize=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true", help="recompute from the stored monthly CSV")
    args = parser.parse_args()
    if args.offline:
        rows = load_history()
    else:
        rows = fetch_monthly_history()
        save_history(rows)
    metrics = compute(rows)
    OUTPUT.write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    render_chart(rows, metrics)
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
