#!/usr/bin/env python3
"""
Quick US stock research helper for the us-stock-research Codex skill.

No API keys or third-party packages are required. The script fetches public
SEC company facts, Yahoo chart data, Stooq fallback prices, and a current
S&P 500 ticker list from Wikipedia.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import html
import json
import math
import os
import re
import statistics
import sys
import time
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


DEFAULT_USER_AGENT = os.environ.get(
    "SEC_USER_AGENT",
    "us-stock-research skill contact@example.com",
)

SEC_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SEC_FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
YAHOO_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
STOOQ_DAILY_URL = "https://stooq.com/q/d/l/"
SP500_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"


def fetch_text(url: str, headers: dict[str, str] | None = None, timeout: int = 30) -> str:
    req_headers = {
        "User-Agent": DEFAULT_USER_AGENT,
        "Accept": "application/json,text/csv,text/html;q=0.9,*/*;q=0.8",
    }
    if headers:
        req_headers.update(headers)
    request = Request(url, headers=req_headers)
    with urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def fetch_json(url: str, timeout: int = 30) -> Any:
    return json.loads(fetch_text(url, timeout=timeout))


def parse_date(value: str | None) -> dt.date | None:
    if not value:
        return None
    return dt.date.fromisoformat(value[:10])


def date_to_epoch(date_value: dt.date) -> int:
    return int(dt.datetime.combine(date_value, dt.time()).replace(tzinfo=dt.timezone.utc).timestamp())


def safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(number) or math.isinf(number):
        return None
    return number


def pct(value: float | None) -> str:
    return "N/A" if value is None else f"{value * 100:.2f}%"


def money(value: float | None) -> str:
    if value is None:
        return "N/A"
    abs_value = abs(value)
    if abs_value >= 1_000_000_000_000:
        return f"{value / 1_000_000_000_000:.2f}T"
    if abs_value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    if abs_value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    return f"{value:.2f}"


def ratio(value: float | None) -> str:
    return "N/A" if value is None else f"{value:.2f}"


def normalize_ticker(ticker: str) -> str:
    return ticker.strip().upper().replace(".", "-")


def stooq_symbol(ticker: str) -> str:
    return ticker.strip().lower().replace("-", ".") + ".us"


class Sp500Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.cell_text: list[str] = []
        self.current_row: list[str] = []
        self.rows: list[list[str]] = []
        self.table_class = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag == "table" and "wikitable" in attrs_dict.get("class", ""):
            self.in_table = True
            self.table_class = attrs_dict.get("class", "")
        elif self.in_table and tag == "tr":
            self.in_row = True
            self.current_row = []
        elif self.in_row and tag in {"td", "th"}:
            self.in_cell = True
            self.cell_text = []

    def handle_endtag(self, tag: str) -> None:
        if self.in_cell and tag in {"td", "th"}:
            text = html.unescape("".join(self.cell_text)).strip()
            text = re.sub(r"\s+", " ", text)
            self.current_row.append(text)
            self.in_cell = False
        elif self.in_row and tag == "tr":
            if self.current_row:
                self.rows.append(self.current_row)
            self.in_row = False
        elif self.in_table and tag == "table":
            self.in_table = False

    def handle_data(self, data: str) -> None:
        if self.in_cell:
            self.cell_text.append(data)


def get_sp500_tickers(limit: int | None = None) -> list[str]:
    page = fetch_text(SP500_URL, headers={"Accept": "text/html"})
    parser = Sp500Parser()
    parser.feed(page)
    tickers: list[str] = []
    for row in parser.rows:
        if row and row[0].strip().upper() == "SYMBOL":
            continue
        if len(row) >= 2 and re.fullmatch(r"[A-Z. -]{1,8}", row[0].strip().upper()):
            symbol = normalize_ticker(row[0])
            if symbol not in tickers:
                tickers.append(symbol)
    if not tickers:
        raise RuntimeError("Could not parse S&P 500 ticker list from Wikipedia")
    return tickers[:limit] if limit else tickers


def load_sec_ticker_map() -> dict[str, dict[str, Any]]:
    data = fetch_json(SEC_TICKERS_URL)
    result: dict[str, dict[str, Any]] = {}
    rows = data.values() if isinstance(data, dict) else data
    for item in rows:
        ticker = normalize_ticker(str(item.get("ticker", "")))
        if ticker:
            cik = str(item.get("cik_str", "")).zfill(10)
            result[ticker] = {
                "ticker": ticker,
                "cik": cik,
                "title": item.get("title"),
            }
    return result


def fetch_sec_facts(cik: str) -> dict[str, Any]:
    return fetch_json(SEC_FACTS_URL.format(cik=str(cik).zfill(10)))


def concept_units(facts: dict[str, Any], concept: str) -> dict[str, list[dict[str, Any]]]:
    for taxonomy in ("us-gaap", "dei", "ifrs-full", "srt"):
        data = facts.get("facts", {}).get(taxonomy, {}).get(concept)
        if data and isinstance(data.get("units"), dict):
            return data["units"]
    return {}


def unit_facts(facts: dict[str, Any], concept: str, preferred_units: tuple[str, ...]) -> list[dict[str, Any]]:
    units = concept_units(facts, concept)
    for unit in preferred_units:
        if unit in units:
            return [x for x in units[unit] if safe_float(x.get("val")) is not None]
    for values in units.values():
        valid = [x for x in values if safe_float(x.get("val")) is not None]
        if valid:
            return valid
    return []


def pick_concept(facts: dict[str, Any], concepts: list[str], units: tuple[str, ...]) -> tuple[str | None, list[dict[str, Any]]]:
    for concept in concepts:
        values = unit_facts(facts, concept, units)
        if values:
            return concept, values
    return None, []


def sort_fact_key(fact: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(fact.get("end", "")),
        str(fact.get("filed", "")),
        str(fact.get("accn", "")),
    )


def latest_instant(facts: dict[str, Any], concepts: list[str], units: tuple[str, ...] = ("USD",)) -> tuple[float | None, dict[str, Any] | None, str | None]:
    concept, values = pick_concept(facts, concepts, units)
    if not values:
        return None, None, None
    filtered = [
        x for x in values
        if x.get("form") in {"10-K", "10-Q", "20-F", "40-F", "8-K"} and x.get("end")
    ]
    if not filtered:
        filtered = [x for x in values if x.get("end")]
    if not filtered:
        return None, None, concept
    fact = sorted(filtered, key=sort_fact_key)[-1]
    return safe_float(fact.get("val")), fact, concept


def duration_days(fact: dict[str, Any]) -> int | None:
    start = parse_date(fact.get("start"))
    end = parse_date(fact.get("end"))
    if not start or not end:
        return None
    return (end - start).days + 1


def latest_annual(facts: dict[str, Any], concepts: list[str], units: tuple[str, ...] = ("USD",)) -> tuple[float | None, dict[str, Any] | None, str | None]:
    concept, values = pick_concept(facts, concepts, units)
    candidates = []
    for item in values:
        days = duration_days(item)
        if days is None:
            continue
        if item.get("form") in {"10-K", "20-F", "40-F"} and 300 <= days <= 430:
            candidates.append(item)
    if not candidates:
        return None, None, concept
    fact = sorted(candidates, key=sort_fact_key)[-1]
    return safe_float(fact.get("val")), fact, concept


def annual_series(facts: dict[str, Any], concepts: list[str], units: tuple[str, ...] = ("USD",)) -> tuple[str | None, list[dict[str, Any]]]:
    concept, values = pick_concept(facts, concepts, units)
    candidates = []
    seen: set[tuple[str, str]] = set()
    for item in sorted(values, key=sort_fact_key):
        days = duration_days(item)
        fy = str(item.get("fy", ""))
        if days is None or not fy:
            continue
        if item.get("form") in {"10-K", "20-F", "40-F"} and 300 <= days <= 430:
            key = (fy, str(item.get("fp", "")))
            if key in seen:
                candidates = [x for x in candidates if (str(x.get("fy", "")), str(x.get("fp", ""))) != key]
            seen.add(key)
            candidates.append(item)
    return concept, candidates


def latest_ttm(facts: dict[str, Any], concepts: list[str], units: tuple[str, ...] = ("USD",)) -> tuple[float | None, list[dict[str, Any]], str | None]:
    concept, values = pick_concept(facts, concepts, units)
    quarter_re = re.compile(r"^CY\d{4}Q[1-4]$")
    quarter_facts: dict[str, dict[str, Any]] = {}
    for item in values:
        frame = str(item.get("frame", ""))
        days = duration_days(item)
        if not quarter_re.match(frame) or days is None:
            continue
        if 60 <= days <= 130 and item.get("form") in {"10-Q", "10-K", "20-F", "40-F", "8-K"}:
            prior = quarter_facts.get(frame)
            if prior is None or sort_fact_key(item) > sort_fact_key(prior):
                quarter_facts[frame] = item
    quarters = sorted(quarter_facts.values(), key=sort_fact_key)
    if len(quarters) >= 4:
        last_four = quarters[-4:]
        values_sum = sum(safe_float(x.get("val")) or 0.0 for x in last_four)
        return values_sum, last_four, concept
    annual_value, annual_fact, annual_concept = latest_annual(facts, concepts, units)
    return annual_value, ([annual_fact] if annual_fact else []), annual_concept or concept


def yoy_growth(facts: dict[str, Any], concepts: list[str], units: tuple[str, ...] = ("USD",)) -> tuple[float | None, str | None]:
    concept, series = annual_series(facts, concepts, units)
    if len(series) < 2:
        return None, concept
    latest = safe_float(series[-1].get("val"))
    prior = safe_float(series[-2].get("val"))
    if latest is None or prior in (None, 0):
        return None, concept
    return latest / prior - 1.0, concept


def fetch_yahoo_history(ticker: str, start: dt.date, end: dt.date) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    params = {
        "period1": date_to_epoch(start),
        "period2": date_to_epoch(end + dt.timedelta(days=1)),
        "interval": "1d",
        "events": "div,splits",
        "includeAdjustedClose": "true",
    }
    url = YAHOO_CHART_URL.format(ticker=quote(ticker)) + "?" + urlencode(params)
    data = fetch_json(url)
    chart = data.get("chart", {})
    if chart.get("error"):
        raise RuntimeError(str(chart["error"]))
    result = chart.get("result", [])
    if not result:
        raise RuntimeError("No Yahoo chart result")
    payload = result[0]
    timestamps = payload.get("timestamp") or []
    quote_data = (payload.get("indicators", {}).get("quote") or [{}])[0]
    adj_data = (payload.get("indicators", {}).get("adjclose") or [{}])[0].get("adjclose") or []
    rows: list[dict[str, Any]] = []
    for i, ts in enumerate(timestamps):
        close = safe_float((quote_data.get("close") or [None] * len(timestamps))[i])
        if close is None:
            continue
        date_value = dt.datetime.fromtimestamp(ts, tz=dt.timezone.utc).date()
        rows.append({
            "date": date_value.isoformat(),
            "open": safe_float((quote_data.get("open") or [None] * len(timestamps))[i]),
            "high": safe_float((quote_data.get("high") or [None] * len(timestamps))[i]),
            "low": safe_float((quote_data.get("low") or [None] * len(timestamps))[i]),
            "close": close,
            "adj_close": safe_float(adj_data[i]) if i < len(adj_data) else close,
            "volume": safe_float((quote_data.get("volume") or [None] * len(timestamps))[i]),
            "source": "Yahoo chart",
        })
    events = payload.get("events", {}) or {}
    return rows, events


def fetch_stooq_history(ticker: str, start: dt.date, end: dt.date) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    params = {
        "s": stooq_symbol(ticker),
        "d1": start.strftime("%Y%m%d"),
        "d2": end.strftime("%Y%m%d"),
        "i": "d",
    }
    text = fetch_text(STOOQ_DAILY_URL + "?" + urlencode(params), headers={"Accept": "text/csv"})
    reader = csv.DictReader(text.splitlines())
    rows: list[dict[str, Any]] = []
    for row in reader:
        if row.get("Close") in {None, "No data"}:
            continue
        close = safe_float(row.get("Close"))
        if close is None:
            continue
        rows.append({
            "date": row.get("Date"),
            "open": safe_float(row.get("Open")),
            "high": safe_float(row.get("High")),
            "low": safe_float(row.get("Low")),
            "close": close,
            "adj_close": close,
            "volume": safe_float(row.get("Volume")),
            "source": "Stooq",
        })
    if not rows:
        raise RuntimeError("No Stooq price rows")
    return rows, {}


def fetch_history(ticker: str, start: dt.date, end: dt.date) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    try:
        return fetch_yahoo_history(ticker, start, end)
    except Exception as first_error:
        try:
            rows, events = fetch_stooq_history(ticker, start, end)
            events["fallback_note"] = f"Yahoo failed: {first_error}"
            return rows, events
        except Exception as second_error:
            raise RuntimeError(f"Yahoo failed: {first_error}; Stooq failed: {second_error}") from second_error


def period_return(rows: list[dict[str, Any]], days: int) -> float | None:
    if len(rows) < 2:
        return None
    latest_date = parse_date(rows[-1]["date"])
    if latest_date is None:
        return None
    threshold = latest_date - dt.timedelta(days=days)
    start_row = None
    for row in rows:
        row_date = parse_date(row["date"])
        if row_date and row_date >= threshold:
            start_row = row
            break
    if not start_row:
        return None
    start_price = safe_float(start_row.get("adj_close") or start_row.get("close"))
    latest_price = safe_float(rows[-1].get("adj_close") or rows[-1].get("close"))
    if start_price in (None, 0) or latest_price is None:
        return None
    return latest_price / start_price - 1.0


def ytd_return(rows: list[dict[str, Any]]) -> float | None:
    if len(rows) < 2:
        return None
    latest_date = parse_date(rows[-1]["date"])
    if latest_date is None:
        return None
    start_of_year = dt.date(latest_date.year, 1, 1)
    start_row = None
    for row in rows:
        row_date = parse_date(row["date"])
        if row_date and row_date >= start_of_year:
            start_row = row
            break
    if not start_row:
        return None
    start_price = safe_float(start_row.get("adj_close") or start_row.get("close"))
    latest_price = safe_float(rows[-1].get("adj_close") or rows[-1].get("close"))
    if start_price in (None, 0) or latest_price is None:
        return None
    return latest_price / start_price - 1.0


def annualized_volatility(rows: list[dict[str, Any]]) -> float | None:
    prices = [safe_float(r.get("adj_close") or r.get("close")) for r in rows]
    prices = [p for p in prices if p and p > 0]
    if len(prices) < 30:
        return None
    returns = [math.log(prices[i] / prices[i - 1]) for i in range(1, len(prices)) if prices[i - 1] > 0]
    if len(returns) < 30:
        return None
    return statistics.stdev(returns) * math.sqrt(252)


def max_drawdown(rows: list[dict[str, Any]]) -> float | None:
    peak = None
    worst = 0.0
    for row in rows:
        price = safe_float(row.get("adj_close") or row.get("close"))
        if price is None:
            continue
        if peak is None or price > peak:
            peak = price
        if peak and peak > 0:
            drawdown = price / peak - 1.0
            worst = min(worst, drawdown)
    return worst if peak else None


def dividends_ttm(events: dict[str, Any], latest_date: dt.date, latest_price: float | None) -> tuple[float | None, float | None]:
    dividends = events.get("dividends") or {}
    if not isinstance(dividends, dict):
        return None, None
    cutoff = latest_date - dt.timedelta(days=365)
    total = 0.0
    found = False
    for item in dividends.values():
        ts = item.get("date")
        amount = safe_float(item.get("amount"))
        if ts is None or amount is None:
            continue
        pay_date = dt.datetime.fromtimestamp(ts, tz=dt.timezone.utc).date()
        if cutoff <= pay_date <= latest_date:
            total += amount
            found = True
    if not found:
        return None, None
    dividend_yield = total / latest_price if latest_price else None
    return total, dividend_yield


REVENUE_TAGS = [
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "Revenues",
    "SalesRevenueNet",
]
NET_INCOME_TAGS = ["NetIncomeLoss", "ProfitLoss"]
OPERATING_INCOME_TAGS = ["OperatingIncomeLoss"]
PRETAX_INCOME_TAGS = ["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest"]
TAX_TAGS = ["IncomeTaxExpenseBenefit"]
OCF_TAGS = ["NetCashProvidedByUsedInOperatingActivities"]
CAPEX_TAGS = ["PaymentsToAcquirePropertyPlantAndEquipment"]
ASSETS_TAGS = ["Assets"]
LIABILITIES_TAGS = ["Liabilities"]
EQUITY_TAGS = [
    "StockholdersEquity",
    "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
]
CASH_TAGS = ["CashAndCashEquivalentsAtCarryingValue", "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"]
DEBT_CURRENT_TAGS = [
    "LongTermDebtAndFinanceLeaseObligationsCurrent",
    "LongTermDebtCurrent",
    "ShortTermBorrowings",
]
DEBT_NONCURRENT_TAGS = [
    "LongTermDebtAndFinanceLeaseObligationsNoncurrent",
    "LongTermDebtNoncurrent",
    "LongTermDebt",
]
SHARES_TAGS = [
    "EntityCommonStockSharesOutstanding",
    "CommonStocksIncludingAdditionalPaidInCapitalSharesOutstanding",
    "WeightedAverageNumberOfDilutedSharesOutstanding",
]
EPS_TAGS = ["EarningsPerShareDiluted", "EarningsPerShareBasic"]


def add_nullable(a: float | None, b: float | None) -> float | None:
    values = [x for x in (a, b) if x is not None]
    return sum(values) if values else None


def safe_div(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    return numerator / denominator


def sec_fundamentals(ticker: str, ticker_map: dict[str, dict[str, Any]]) -> dict[str, Any]:
    ticker = normalize_ticker(ticker)
    mapping = ticker_map.get(ticker)
    if not mapping:
        return {"ticker": ticker, "sec_error": "No SEC CIK mapping found"}
    cik = mapping["cik"]
    facts = fetch_sec_facts(cik)

    revenue_ttm, revenue_facts, revenue_tag = latest_ttm(facts, REVENUE_TAGS)
    net_income_ttm, net_income_facts, net_income_tag = latest_ttm(facts, NET_INCOME_TAGS)
    operating_income_ttm, _, operating_income_tag = latest_ttm(facts, OPERATING_INCOME_TAGS)
    pretax_ttm, _, _ = latest_ttm(facts, PRETAX_INCOME_TAGS)
    tax_ttm, _, _ = latest_ttm(facts, TAX_TAGS)
    ocf_ttm, _, ocf_tag = latest_ttm(facts, OCF_TAGS)
    capex_ttm, _, capex_tag = latest_ttm(facts, CAPEX_TAGS)

    assets, assets_fact, assets_tag = latest_instant(facts, ASSETS_TAGS)
    liabilities, _, liabilities_tag = latest_instant(facts, LIABILITIES_TAGS)
    equity, equity_fact, equity_tag = latest_instant(facts, EQUITY_TAGS)
    cash, _, cash_tag = latest_instant(facts, CASH_TAGS)
    debt_current, _, debt_current_tag = latest_instant(facts, DEBT_CURRENT_TAGS)
    debt_noncurrent, _, debt_noncurrent_tag = latest_instant(facts, DEBT_NONCURRENT_TAGS)
    shares, shares_fact, shares_tag = latest_instant(facts, SHARES_TAGS, ("shares",))
    eps_ttm, _, eps_tag = latest_ttm(facts, EPS_TAGS, ("USD/shares", "USD/shares"))

    total_debt = add_nullable(debt_current, debt_noncurrent)
    fcf_ttm = None
    if ocf_ttm is not None:
        fcf_ttm = ocf_ttm - abs(capex_ttm or 0.0)

    tax_rate = safe_div(tax_ttm, pretax_ttm)
    if tax_rate is None or tax_rate < 0 or tax_rate > 0.5:
        tax_rate = 0.21
    nopat = operating_income_ttm * (1 - tax_rate) if operating_income_ttm is not None else None
    invested_capital = None
    if equity is not None:
        invested_capital = equity + (total_debt or 0.0) - (cash or 0.0)

    revenue_growth_yoy, revenue_growth_tag = yoy_growth(facts, REVENUE_TAGS)
    net_income_growth_yoy, net_income_growth_tag = yoy_growth(facts, NET_INCOME_TAGS)

    return {
        "ticker": ticker,
        "company": mapping.get("title"),
        "cik": cik,
        "period_end": (
            (revenue_facts[-1].get("end") if revenue_facts else None)
            or (net_income_facts[-1].get("end") if net_income_facts else None)
            or (assets_fact.get("end") if assets_fact else None)
        ),
        "filed": (
            (revenue_facts[-1].get("filed") if revenue_facts else None)
            or (net_income_facts[-1].get("filed") if net_income_facts else None)
            or (assets_fact.get("filed") if assets_fact else None)
        ),
        "revenue_ttm": revenue_ttm,
        "net_income_ttm": net_income_ttm,
        "operating_income_ttm": operating_income_ttm,
        "ocf_ttm": ocf_ttm,
        "capex_ttm": capex_ttm,
        "fcf_ttm": fcf_ttm,
        "assets": assets,
        "liabilities": liabilities,
        "equity": equity,
        "cash": cash,
        "total_debt": total_debt,
        "shares": shares,
        "eps_ttm": eps_ttm,
        "revenue_growth_yoy": revenue_growth_yoy,
        "net_income_growth_yoy": net_income_growth_yoy,
        "net_margin": safe_div(net_income_ttm, revenue_ttm),
        "roe": safe_div(net_income_ttm, equity),
        "roa": safe_div(net_income_ttm, assets),
        "roic": safe_div(nopat, invested_capital),
        "debt_to_equity": safe_div(total_debt, equity),
        "xbrl_tags": {
            "revenue": revenue_tag or revenue_growth_tag,
            "net_income": net_income_tag or net_income_growth_tag,
            "operating_income": operating_income_tag,
            "ocf": ocf_tag,
            "capex": capex_tag,
            "assets": assets_tag,
            "liabilities": liabilities_tag,
            "equity": equity_tag,
            "cash": cash_tag,
            "debt_current": debt_current_tag,
            "debt_noncurrent": debt_noncurrent_tag,
            "shares": shares_tag,
            "eps": eps_tag,
        },
        "source": "SEC EDGAR companyfacts",
    }


def ticker_snapshot(ticker: str, years: int, ticker_map: dict[str, dict[str, Any]] | None = None) -> dict[str, Any]:
    ticker = normalize_ticker(ticker)
    end = dt.date.today()
    start = end - dt.timedelta(days=max(years, 1) * 366)
    history, events = fetch_history(ticker, start, end)
    if not history:
        raise RuntimeError(f"No history for {ticker}")
    latest = history[-1]
    latest_date = parse_date(latest["date"]) or end
    latest_price = safe_float(latest.get("adj_close") or latest.get("close"))
    raw_close = safe_float(latest.get("close"))

    fundamentals: dict[str, Any] = {}
    if ticker_map is not None:
        try:
            fundamentals = sec_fundamentals(ticker, ticker_map)
        except Exception as exc:
            fundamentals = {"ticker": ticker, "sec_error": str(exc)}

    dividend_ttm, dividend_yield = dividends_ttm(events, latest_date, latest_price)
    shares = safe_float(fundamentals.get("shares"))
    market_cap = latest_price * shares if latest_price is not None and shares is not None else None
    net_income_ttm = safe_float(fundamentals.get("net_income_ttm"))
    revenue_ttm = safe_float(fundamentals.get("revenue_ttm"))
    equity = safe_float(fundamentals.get("equity"))
    fcf_ttm = safe_float(fundamentals.get("fcf_ttm"))
    eps_ttm = safe_float(fundamentals.get("eps_ttm"))
    eps_growth = safe_float(fundamentals.get("net_income_growth_yoy"))

    pe = safe_div(market_cap, net_income_ttm) if net_income_ttm and net_income_ttm > 0 else None
    if pe is None and latest_price is not None and eps_ttm and eps_ttm > 0:
        pe = latest_price / eps_ttm
    ps = safe_div(market_cap, revenue_ttm)
    pb = safe_div(market_cap, equity)
    fcf_yield = safe_div(fcf_ttm, market_cap)
    peg = None
    if pe is not None and eps_growth is not None and eps_growth > 0.01:
        peg = pe / (eps_growth * 100.0)

    return {
        "ticker": ticker,
        "company": fundamentals.get("company"),
        "cik": fundamentals.get("cik"),
        "latest_date": latest.get("date"),
        "price": latest_price,
        "raw_close": raw_close,
        "price_source": latest.get("source"),
        "history_rows": len(history),
        "return_1m": period_return(history, 31),
        "return_3m": period_return(history, 92),
        "return_6m": period_return(history, 183),
        "return_ytd": ytd_return(history),
        "return_1y": period_return(history, 366),
        "volatility": annualized_volatility(history[-252:]),
        "max_drawdown": max_drawdown(history),
        "dividend_ttm": dividend_ttm,
        "dividend_yield": dividend_yield,
        "market_cap": market_cap,
        "pe": pe,
        "pb": pb,
        "ps": ps,
        "peg": peg,
        "fcf_yield": fcf_yield,
        **{k: v for k, v in fundamentals.items() if k not in {"ticker", "company", "cik"}},
    }


def percentile_scores(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    metrics = {
        "quality": [("roe", True), ("roic", True), ("net_margin", True), ("debt_to_equity", False)],
        "value": [("pe", False), ("pb", False), ("ps", False), ("peg", False), ("fcf_yield", True)],
        "growth": [("revenue_growth_yoy", True), ("net_income_growth_yoy", True)],
        "momentum": [("return_6m", True), ("return_1y", True), ("volatility", False), ("max_drawdown", True)],
        "dividend": [("dividend_yield", True), ("fcf_yield", True)],
    }
    weights = {
        "quality": 0.30,
        "value": 0.25,
        "growth": 0.20,
        "momentum": 0.15,
        "dividend": 0.10,
    }

    def metric_percentile(metric: str, high_good: bool) -> dict[int, float]:
        values = [(i, safe_float(row.get(metric))) for i, row in enumerate(rows)]
        values = [(i, v) for i, v in values if v is not None]
        if len(values) < 2:
            return {}
        values.sort(key=lambda x: x[1])
        scores: dict[int, float] = {}
        n = len(values) - 1
        for rank_idx, (row_idx, _) in enumerate(values):
            score = rank_idx / n
            if not high_good:
                score = 1.0 - score
            scores[row_idx] = score
        return scores

    bucket_metric_scores: dict[str, list[dict[int, float]]] = {
        bucket: [metric_percentile(metric, high_good) for metric, high_good in metric_list]
        for bucket, metric_list in metrics.items()
    }

    for i, row in enumerate(rows):
        composite = 0.0
        valid_weight = 0.0
        for bucket, score_maps in bucket_metric_scores.items():
            scores = [score_map[i] for score_map in score_maps if i in score_map]
            bucket_score = sum(scores) / len(scores) if scores else None
            row[f"{bucket}_score"] = bucket_score
            if bucket_score is not None:
                composite += bucket_score * weights[bucket]
                valid_weight += weights[bucket]
        row["composite_score"] = composite / valid_weight if valid_weight >= 0.50 else None
    return rows


CSV_FIELDS = [
    "ticker", "company", "cik", "latest_date", "price", "market_cap",
    "composite_score", "quality_score", "value_score", "growth_score", "momentum_score", "dividend_score",
    "revenue_ttm", "revenue_growth_yoy", "net_income_ttm", "net_income_growth_yoy",
    "fcf_ttm", "roe", "roic", "roa", "net_margin", "debt_to_equity",
    "pe", "pb", "ps", "peg", "fcf_yield", "dividend_yield",
    "return_1m", "return_3m", "return_6m", "return_ytd", "return_1y", "volatility", "max_drawdown",
    "period_end", "filed", "price_source", "sec_error",
]


def write_outputs(rows: list[dict[str, Any]], out: str | None, title: str) -> None:
    rows = percentile_scores(rows)
    rows.sort(key=lambda r: (safe_float(r.get("composite_score")) is not None, safe_float(r.get("composite_score")) or -1), reverse=True)

    if out:
        out_path = Path(out)
        if out_path.suffix:
            base = out_path.with_suffix("")
        else:
            base = out_path
        base.parent.mkdir(parents=True, exist_ok=True)
        json_path = base.with_suffix(".json")
        csv_path = base.with_suffix(".csv")
        md_path = base.with_suffix(".md")
        json_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        md_path.write_text(markdown_table(rows, title), encoding="utf-8")
        print(f"Wrote {json_path}")
        print(f"Wrote {csv_path}")
        print(f"Wrote {md_path}")
    print(markdown_table(rows[:20], title))


def markdown_table(rows: list[dict[str, Any]], title: str) -> str:
    lines = [f"# {title}", ""]
    lines.append(f"Generated: {dt.datetime.now().isoformat(timespec='seconds')}")
    lines.append("")
    lines.append("| Rank | Ticker | Company | Price | Mkt Cap | Score | ROE | ROIC | P/E | PEG | Div Yld | 1Y Ret | Max DD | Data Gap |")
    lines.append("|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for idx, row in enumerate(rows, 1):
        gap = row.get("sec_error") or ""
        lines.append(
            "| {rank} | {ticker} | {company} | {price} | {mcap} | {score} | {roe} | {roic} | {pe} | {peg} | {div} | {ret} | {dd} | {gap} |".format(
                rank=idx,
                ticker=row.get("ticker") or "",
                company=(row.get("company") or "")[:34],
                price=ratio(safe_float(row.get("price"))),
                mcap=money(safe_float(row.get("market_cap"))),
                score=ratio(safe_float(row.get("composite_score"))),
                roe=pct(safe_float(row.get("roe"))),
                roic=pct(safe_float(row.get("roic"))),
                pe=ratio(safe_float(row.get("pe"))),
                peg=ratio(safe_float(row.get("peg"))),
                div=pct(safe_float(row.get("dividend_yield"))),
                ret=pct(safe_float(row.get("return_1y"))),
                dd=pct(safe_float(row.get("max_drawdown"))),
                gap=str(gap).replace("|", "/")[:50],
            )
        )
    lines.append("")
    lines.append("Sources: SEC EDGAR companyfacts for fundamentals when available; Yahoo chart or Stooq for prices; Wikipedia for current S&P 500 constituents when universe=sp500.")
    lines.append("Limitations: first-pass screen only; verify filings, corporate actions, fiscal periods, and provider adjustments before investment decisions.")
    return "\n".join(lines)


def command_install_check(_: argparse.Namespace) -> int:
    print("Python:", sys.version.split()[0])
    print("No third-party packages required.")
    print("SEC_USER_AGENT:", DEFAULT_USER_AGENT)
    checks = [
        ("SEC ticker map", SEC_TICKERS_URL),
        ("Yahoo chart AAPL", YAHOO_CHART_URL.format(ticker="AAPL") + "?range=5d&interval=1d"),
        ("Stooq AAPL", STOOQ_DAILY_URL + "?s=aapl.us&i=d"),
    ]
    for name, url in checks:
        try:
            text = fetch_text(url, timeout=15)
            print(f"[OK] {name}: {len(text)} bytes")
        except Exception as exc:
            print(f"[WARN] {name}: {exc}")
    return 0


def command_history(args: argparse.Namespace) -> int:
    ticker = normalize_ticker(args.ticker)
    start = parse_date(args.start) or (dt.date.today() - dt.timedelta(days=366 * args.years))
    end = parse_date(args.end) or dt.date.today()
    rows, events = fetch_history(ticker, start, end)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["date", "open", "high", "low", "close", "adj_close", "volume", "source"])
            writer.writeheader()
            writer.writerows(rows)
        print(f"Wrote {out_path}")
    latest = rows[-1]
    print(json.dumps({
        "ticker": ticker,
        "start": rows[0]["date"],
        "end": latest["date"],
        "rows": len(rows),
        "latest_close": latest["close"],
        "latest_adj_close": latest["adj_close"],
        "return_1y": period_return(rows, 366),
        "max_drawdown": max_drawdown(rows),
        "source": latest["source"],
        "events_available": sorted(events.keys()),
    }, indent=2))
    return 0


def command_snapshot(args: argparse.Namespace) -> int:
    tickers = [normalize_ticker(x) for x in args.tickers]
    ticker_map = load_sec_ticker_map()
    rows = []
    for idx, ticker in enumerate(tickers, 1):
        try:
            print(f"[{idx}/{len(tickers)}] {ticker}", file=sys.stderr)
            rows.append(ticker_snapshot(ticker, args.years, ticker_map))
            time.sleep(args.sleep)
        except Exception as exc:
            rows.append({"ticker": ticker, "sec_error": str(exc)})
    write_outputs(rows, args.out, "US Stock Snapshot")
    return 0


def command_screen(args: argparse.Namespace) -> int:
    if args.universe == "sp500":
        tickers = get_sp500_tickers(limit=args.limit)
    elif args.tickers:
        tickers = [normalize_ticker(x) for x in args.tickers]
    else:
        raise SystemExit("Provide --tickers or --universe sp500")

    ticker_map = load_sec_ticker_map()
    rows = []
    for idx, ticker in enumerate(tickers, 1):
        try:
            print(f"[{idx}/{len(tickers)}] {ticker}", file=sys.stderr)
            rows.append(ticker_snapshot(ticker, args.years, ticker_map))
            time.sleep(args.sleep)
        except (HTTPError, URLError, RuntimeError, ValueError) as exc:
            rows.append({"ticker": ticker, "sec_error": str(exc)})
    write_outputs(rows, args.out, f"US Stock Screen ({args.universe or 'custom'})")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="US stock research helper")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("install-check", help="Check Python and public endpoints")
    p.set_defaults(func=command_install_check)

    p = sub.add_parser("history", help="Download daily historical OHLCV")
    p.add_argument("--ticker", required=True)
    p.add_argument("--start")
    p.add_argument("--end")
    p.add_argument("--years", type=int, default=5)
    p.add_argument("--out", help="CSV output path")
    p.set_defaults(func=command_history)

    p = sub.add_parser("snapshot", help="Create a first-pass snapshot for explicit tickers")
    p.add_argument("--tickers", nargs="+", required=True)
    p.add_argument("--years", type=int, default=5)
    p.add_argument("--sleep", type=float, default=0.15, help="Delay between tickers")
    p.add_argument("--out", help="Output base path; writes .json/.csv/.md")
    p.set_defaults(func=command_snapshot)

    p = sub.add_parser("screen", help="Screen a universe")
    p.add_argument("--universe", choices=["sp500"], default=None)
    p.add_argument("--tickers", nargs="+")
    p.add_argument("--limit", type=int, default=None, help="Limit universe size for quick runs")
    p.add_argument("--years", type=int, default=5)
    p.add_argument("--sleep", type=float, default=0.15, help="Delay between tickers")
    p.add_argument("--out", help="Output base path; writes .json/.csv/.md")
    p.set_defaults(func=command_screen)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args) or 0)


if __name__ == "__main__":
    raise SystemExit(main())
