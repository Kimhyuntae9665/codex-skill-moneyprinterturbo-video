from __future__ import annotations

import csv
from datetime import date, datetime, timezone
import json
from pathlib import Path
import statistics
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
HISTORY = ROOT / "dividend_yield_history_v6.csv"
OUTPUT = ROOT / "v6_metrics.json"
START = datetime(2008, 1, 1, tzinfo=timezone.utc)
END_EXCLUSIVE = datetime(2026, 9, 1, tzinfo=timezone.utc)
DISPLAY_START = date(2010, 1, 1)
EXPECTED_AS_OF = date(2026, 8, 31)
SHARES_OUTSTANDING = 707_641_531
TTM_DIVIDENDS_M = 5_225.0
TTM_NET_BUYBACKS_M = 2_086.0


def fetch(symbol: str, interval: str = "1d") -> dict:
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        f"?period1={int(START.timestamp())}&period2={int(END_EXCLUSIVE.timestamp())}"
        f"&interval={interval}&events=div%2Csplits&includeAdjustedClose=true"
    )
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=45) as response:
        payload = json.load(response)
    return payload["chart"]["result"][0]


def daily_rows(result: dict) -> list[dict[str, object]]:
    timestamps = result["timestamp"]
    quotes = result["indicators"]["quote"][0]["close"]
    adjusted = result["indicators"]["adjclose"][0]["adjclose"]
    return [
        {
            "day": datetime.fromtimestamp(timestamp, tz=timezone.utc).date(),
            "close": float(close),
            "adjusted": float(adj),
        }
        for timestamp, close, adj in zip(timestamps, quotes, adjusted, strict=True)
        if close is not None and adj is not None
    ]


def monthly_dividend_history(result: dict) -> list[dict[str, object]]:
    rows = daily_rows(result)
    month_ends: dict[tuple[int, int], dict[str, object]] = {}
    for row in rows:
        trading_day = row["day"]
        if trading_day < DISPLAY_START:
            continue
        month_ends[(trading_day.year, trading_day.month)] = row
    dividend_events = result.get("events", {}).get("dividends", {})
    dividends = sorted(
        (
            datetime.fromtimestamp(int(event["date"]), tz=timezone.utc).date(),
            float(event["amount"]),
        )
        for event in dividend_events.values()
    )
    output: list[dict[str, object]] = []
    for row in sorted(month_ends.values(), key=lambda item: item["day"]):
        paid = [(day, amount) for day, amount in dividends if day <= row["day"]]
        if len(paid) < 4:
            continue
        trailing = paid[-4:]
        ttm = sum(amount for _, amount in trailing)
        output.append(
            {
                "month_end": row["day"].isoformat(),
                "raw_close_usd": row["close"],
                "ttm_dividend_usd": ttm,
                "ttm_yield_pct": ttm / row["close"] * 100,
                "latest_dividend_usd": trailing[-1][1],
            }
        )
    if not output or date.fromisoformat(output[-1]["month_end"]) != EXPECTED_AS_OF:
        raise RuntimeError(f"history does not end at {EXPECTED_AS_OF}")
    return output


def window_summary(rows: list[dict[str, object]], start_year: int) -> dict[str, object]:
    window = [row for row in rows if int(row["month_end"][:4]) >= start_year]
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
        "peak_month_end": peak["month_end"],
        "peak_yield_pct": peak["ttm_yield_pct"],
    }


def returns_map(result: dict, cutoff: date) -> dict[date, float]:
    rows = [row for row in daily_rows(result) if row["day"] >= cutoff]
    return {
        rows[index]["day"]: rows[index]["adjusted"] / rows[index - 1]["adjusted"] - 1
        for index in range(1, len(rows))
    }


def covariance(left: list[float], right: list[float]) -> float:
    ml, mr = statistics.mean(left), statistics.mean(right)
    return sum((a - ml) * (b - mr) for a, b in zip(left, right, strict=True)) / (len(left) - 1)


def risk_metrics(results: dict[str, dict]) -> dict[str, float | int | str]:
    cutoff = date(2021, 9, 1)
    maps = {symbol: returns_map(result, cutoff) for symbol, result in results.items()}
    common = sorted(set.intersection(*(set(value) for value in maps.values())))
    series = {symbol: [maps[symbol][day] for day in common] for symbol in maps}
    spy_var = statistics.variance(series["SPY"])
    mcd_beta = covariance(series["MCD"], series["SPY"]) / spy_var
    qqq_beta = covariance(series["QQQ"], series["SPY"]) / spy_var
    mcd_qqq = covariance(series["MCD"], series["QQQ"]) / (
        statistics.stdev(series["MCD"]) * statistics.stdev(series["QQQ"])
    )
    return {
        "basis": "Yahoo adjusted weekly close, aligned simple returns, 2021-09-01 through 2026-08-31",
        "observations": len(common),
        "mcd_beta_vs_spy": mcd_beta,
        "spy_beta_vs_spy": 1.0,
        "qqq_beta_vs_spy": qqq_beta,
        "mcd_qqq_correlation": mcd_qqq,
    }


def return_for_window(rows: list[dict[str, object]], start: date) -> float:
    selected = [row for row in rows if row["day"] >= start]
    return selected[-1]["adjusted"] / selected[0]["adjusted"] - 1


def main() -> int:
    results = {symbol: fetch(symbol) for symbol in ("MCD", "SPY", "QQQ")}
    weekly_results = {symbol: fetch(symbol, "1wk") for symbol in ("MCD", "SPY", "QQQ")}
    histories = {symbol: daily_rows(result) for symbol, result in results.items()}
    dividend_rows = monthly_dividend_history(results["MCD"])
    current = dividend_rows[-1]
    price = float(current["raw_close_usd"])
    market_cap_m = SHARES_OUTSTANDING * price / 1_000_000
    metrics = {
        "as_of": "2026-08-31 US close",
        "current": current,
        "price_performance": {
            "six_month_adjusted_return": {
                symbol: return_for_window(rows, date(2026, 3, 1))
                for symbol, rows in histories.items()
            }
        },
        "dividend_yield_history": {
            "method": "latest four cash dividends divided by raw calendar month-end close",
            "since_2010": window_summary(dividend_rows, 2010),
            "since_2020": window_summary(dividend_rows, 2020),
            "since_2023": window_summary(dividend_rows, 2023),
        },
        "risk": risk_metrics(weekly_results),
        "shareholder_return": {
            "ttm_dividends_usd_millions": TTM_DIVIDENDS_M,
            "ttm_net_cash_buybacks_usd_millions": TTM_NET_BUYBACKS_M,
            "market_cap_usd_millions": market_cap_m,
            "cash_shareholder_yield": (TTM_DIVIDENDS_M + TTM_NET_BUYBACKS_M) / market_cap_m,
            "method": "FY2025 + H1 2026 - H1 2025; net buybacks subtract option proceeds",
        },
        "recommendation_frame": {
            "current_price_zone": "260s",
            "second_zone": "245-250",
            "second_zone_reason": "TTM dividend yield approaches 3.0% at $245-$250",
            "final_add_condition": "U.S. comparable guest counts turn positive or operating trend confirms",
            "invalidation": "guest counts, free cash flow, or dividend coverage materially weakens",
        },
    }
    with HISTORY.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=dividend_rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(dividend_rows)
    OUTPUT.write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
