from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import statistics
from urllib.parse import quote
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
INPUTS = ROOT / "shareholder_return_inputs_v3.csv"
WEEKLY = ROOT / "weekly_adjusted_prices_v3.csv"
OUTPUT = ROOT / "v3_metrics.json"
START = datetime(2021, 8, 27, tzinfo=timezone.utc)
END_EXCLUSIVE = datetime(2026, 8, 28, tzinfo=timezone.utc)
TICKERS = ("MCD", "SPY", "QQQ")


def yahoo_url(ticker: str) -> str:
    return (
        "https://query1.finance.yahoo.com/v8/finance/chart/"
        f"{quote(ticker)}?period1={int(START.timestamp())}"
        f"&period2={int(END_EXCLUSIVE.timestamp())}"
        "&interval=1wk&events=history&includeAdjustedClose=true"
    )


def fetch_weekly(ticker: str) -> dict[str, float]:
    request = Request(yahoo_url(ticker), headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=30) as response:
        payload = json.load(response)
    result = payload["chart"]["result"][0]
    timestamps = result["timestamp"]
    adjusted = result["indicators"]["adjclose"][0]["adjclose"]
    rows: dict[str, float] = {}
    for timestamp, value in zip(timestamps, adjusted, strict=True):
        if value is None:
            continue
        day = datetime.fromtimestamp(timestamp, tz=timezone.utc).date().isoformat()
        rows[day] = float(value)
    if len(rows) < 250:
        raise RuntimeError(f"too few weekly prices for {ticker}: {len(rows)}")
    return rows


def save_weekly(series: dict[str, dict[str, float]]) -> None:
    dates = sorted(set.intersection(*(set(series[ticker]) for ticker in TICKERS)))
    with WEEKLY.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(("week_anchor_utc", *TICKERS))
        for day in dates:
            writer.writerow((day, *(f"{series[ticker][day]:.8f}" for ticker in TICKERS)))


def load_weekly() -> dict[str, list[float]]:
    values = {ticker: [] for ticker in TICKERS}
    with WEEKLY.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        for ticker in TICKERS:
            values[ticker].append(float(row[ticker]))
    if len(rows) < 250:
        raise RuntimeError(f"too few aligned weekly rows: {len(rows)}")
    return values


def returns(prices: list[float]) -> list[float]:
    return [current / prior - 1 for prior, current in zip(prices, prices[1:])]


def beta(asset: list[float], market: list[float]) -> float:
    return statistics.covariance(asset, market) / statistics.variance(market)


def load_inputs() -> dict[str, float]:
    with INPUTS.open("r", encoding="utf-8", newline="") as handle:
        return {row["key"]: float(row["value"]) for row in csv.DictReader(handle)}


def compute() -> dict[str, object]:
    prices = load_weekly()
    weekly_returns = {ticker: returns(prices[ticker]) for ticker in TICKERS}
    inputs = load_inputs()

    dividends = (
        inputs["fy2025_dividends"]
        + inputs["h1_2026_dividends"]
        - inputs["h1_2025_dividends"]
    )
    repurchases = (
        inputs["fy2025_repurchases"]
        + inputs["h1_2026_repurchases"]
        - inputs["h1_2025_repurchases"]
    )
    option_proceeds = (
        inputs["fy2025_option_proceeds"]
        + inputs["h1_2026_option_proceeds"]
        - inputs["h1_2025_option_proceeds"]
    )
    net_buybacks = repurchases - option_proceeds
    cash_return = dividends + net_buybacks
    market_cap_millions = (
        inputs["shares_outstanding_2026_06_30"]
        * inputs["price_2026_08_27"]
        / 1_000_000
    )
    diluted_share_change = (
        inputs["h1_2026_diluted_weighted_shares"]
        / inputs["h1_2025_diluted_weighted_shares"]
        - 1
    )

    mcd = weekly_returns["MCD"]
    spy = weekly_returns["SPY"]
    qqq = weekly_returns["QQQ"]
    return {
        "as_of": "2026-08-27 US close",
        "sources": {
            "sec_inputs": "shareholder_return_inputs_v3.csv",
            "adjusted_close_definition": "https://help.yahoo.com/kb/SLN28256.html",
            "price_requests": {ticker: yahoo_url(ticker) for ticker in TICKERS},
            "spy_benchmark": "https://www.ssga.com/us/en/individual/etfs/state-street-spdr-sp-500-etf-trust-spy",
            "qqq_benchmark": "https://www.invesco.com/qqq-etf/en/home.html",
        },
        "weekly_risk_method": {
            "requested_start": START.date().isoformat(),
            "requested_end_inclusive": "2026-08-27",
            "first_week_anchor_utc": "2021-08-23",
            "last_week_anchor_utc": "2026-08-24",
            "price_rows": len(prices["MCD"]),
            "return_observations": len(mcd),
            "basis": "Yahoo Finance weekly adjusted close; simple returns; sample covariance and variance",
            "beta_formula": "cov(asset_weekly_return, SPY_weekly_return) / var(SPY_weekly_return)",
            "correlation_formula": "Pearson correlation of aligned weekly simple returns",
        },
        "risk_metrics": {
            "mcd_beta_vs_spy": beta(mcd, spy),
            "spy_beta_vs_spy": 1.0,
            "qqq_beta_vs_spy": beta(qqq, spy),
            "mcd_spy_correlation": statistics.correlation(mcd, spy),
            "mcd_qqq_correlation": statistics.correlation(mcd, qqq),
            "qqq_spy_correlation": statistics.correlation(qqq, spy),
            "mcd_annualized_volatility": statistics.stdev(mcd) * (52**0.5),
            "spy_annualized_volatility": statistics.stdev(spy) * (52**0.5),
            "qqq_annualized_volatility": statistics.stdev(qqq) * (52**0.5),
        },
        "shareholder_return": {
            "ttm_formula": "FY2025 + H1 2026 - H1 2025",
            "ttm_dividends_usd_millions": dividends,
            "ttm_treasury_stock_purchases_usd_millions": repurchases,
            "ttm_stock_option_proceeds_usd_millions": option_proceeds,
            "ttm_net_cash_buybacks_usd_millions": net_buybacks,
            "ttm_cash_shareholder_return_usd_millions": cash_return,
            "market_cap_denominator_usd_millions": market_cap_millions,
            "dividend_cash_yield": dividends / market_cap_millions,
            "net_buyback_cash_yield": net_buybacks / market_cap_millions,
            "total_cash_shareholder_yield": cash_return / market_cap_millions,
            "h1_diluted_weighted_share_change_yoy": diluted_share_change,
            "dividend_increase_streak_years": inputs["dividend_increase_streak"],
            "limitations": [
                "The denominator combines June 30 shares outstanding with the August 27 unadjusted close.",
                "Net cash buybacks subtract stock-option cash proceeds but do not capture every noncash dilution effect.",
                "Historical beta and correlation are not forecasts and low beta does not guarantee low total risk.",
            ],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true", help="recompute from the stored weekly CSV")
    args = parser.parse_args()
    if not args.offline:
        save_weekly({ticker: fetch_weekly(ticker) for ticker in TICKERS})
    metrics = compute()
    OUTPUT.write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
