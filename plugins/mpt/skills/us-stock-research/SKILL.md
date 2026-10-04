---
name: us-stock-research
description: Use this skill for US stock research, stock screening, valuation, dividend analysis, SEC/EDGAR/XBRL fundamentals, S&P 500 or US-listed universe analysis, historical prices, ratios such as ROE, ROIC, ROI, ROA, P/E, P/B, PEG, EV/EBITDA, dividend yield, payout ratio, revenue and EPS growth, filings, news, macro context, and Korean-language requests about US equities, fundamentals, valuation, dividends, and news-driven analysis.
---

# US Stock Research

Use this skill to build objective US equity research from public data. Treat outputs as research support, not investment advice. Always separate source facts, calculated metrics, and inference.

## Core Workflow

1. Define the task.
   - Ticker research: normalize symbols and identify the company/CIK.
   - Screening: define universe (`sp500`, explicit tickers, or all US-listed names), minimum market cap/liquidity, sector constraints, and ranking objective.
   - Historical question: define date range, adjusted/unadjusted price basis, and corporate-action handling.

2. Gather data by source priority.
   - Financial statements and filings: prefer SEC EDGAR APIs and company filings.
   - Prices, dividends, splits: use exchange/vendor data when available; otherwise use `yfinance`, Yahoo chart data, or Stooq as convenience sources and label them as non-official.
   - Ratios and bulk fundamentals: use FMP, Alpha Vantage, OpenBB, Polygon, Twelve Data, Benzinga, or other configured providers when API keys/tools are available.
   - News and events: use Helium MCP/news search, company IR, SEC 8-K/10-Q/10-K filings, earnings call transcripts, and GDELT-style broad news only as evidence with dates.
   - Macro/factors: use FRED, Treasury Fiscal Data, BLS, BEA, and Fama-French factor data when relevant.

3. Preserve provenance.
   - Record source name, URL/API endpoint, retrieval date, fiscal period, reported currency, and whether a number is reported or calculated.
   - For SEC facts, keep CIK, taxonomy tag, unit, form type, filed date, fiscal year/period, and period end date when available.

4. Calculate defensively.
   - Align income/cash-flow items to TTM or annual periods; align balance-sheet items to period-end values.
   - Use adjusted close for total-return-like price comparisons unless the user asks for raw historical prices.
   - Do not compute PEG when earnings or growth is negative, near zero, or sourced from an inconsistent period.
   - Show `N/A` rather than filling missing data with estimates.

5. Score within the relevant universe.
   - Quality: ROE, ROIC, margins, balance-sheet strength, accrual/FCF quality.
   - Growth: revenue, EPS, operating income, FCF, and forward estimates when available.
   - Value: P/E, PEG, P/B, P/S, EV/EBITDA, FCF yield, sector-relative valuation.
   - Dividend: yield, payout ratio, FCF coverage, dividend growth/stability, buybacks.
   - Momentum/risk: 3M/6M/1Y returns, volatility, max drawdown, beta when available.
   - Event/news: earnings surprises, guidance, lawsuits, regulation, M&A, insider/13F signals, and filing red flags.

6. Write the answer.
   - Lead with a concise conclusion and the strongest evidence.
   - Include a compact table of key metrics and a short source note.
   - Separate bull/base/bear scenarios, key risks, and what data would change the view.
   - State data limitations plainly, especially for free vendor data, index constituents, historical ticker changes, and survivorship bias.

## Scripts

Use the bundled script for quick data pulls and first-pass screens. It uses Python standard library only and works without API keys, but richer provider data should be added when available.

```powershell
python "$env:USERPROFILE\.codex\skills\us-stock-research\scripts\us_stock_research.py" install-check
python "$env:USERPROFILE\.codex\skills\us-stock-research\scripts\us_stock_research.py" snapshot --tickers AAPL MSFT NVDA --years 5 --out "$env:TEMP\us-stock-snapshot"
python "$env:USERPROFILE\.codex\skills\us-stock-research\scripts\us_stock_research.py" history --ticker AAPL --start 2010-01-01 --out "$env:TEMP\aapl-history.csv"
python "$env:USERPROFILE\.codex\skills\us-stock-research\scripts\us_stock_research.py" screen --universe sp500 --limit 50 --years 5 --out "$env:TEMP\sp500-screen"
```

Set a descriptive SEC user agent when doing repeated EDGAR calls:

```powershell
$env:SEC_USER_AGENT="your-name your-email@example.com"
```

## References

Read only the file needed for the current task:

- `references/data-sources.md`: source catalog, access rules, API-key notes, and reliability hierarchy.
- `references/metrics-and-scoring.md`: formulas, edge cases, sector caveats, and scoring rules.
- `references/report-templates.md`: Korean/English output formats for single-stock research, screens, and news-driven updates.
- `references/prompts.md`: ready-to-use Korean prompts for screening, valuation, dividends, historical prices, and news synthesis.

## Output Standard

For single-stock analysis, include: price, market cap, business summary, revenue/net income/FCF trend, ROE/ROIC/ROA, leverage, margins, valuation, dividend/buyback profile, recent news/filings, peer comparison, bull/base/bear scenario, and data quality notes.

For screens, include: universe, filters, ranking logic, top table, excluded names/data gaps, sector distribution, and a short "why these ranked high" explanation.

For historical price requests, specify adjusted versus raw close, date/time zone, data source, split/dividend handling, and nearest available trading day when the exact date was not a market day.

## Local Windows runtime (2026-09-03)

Run bundled Python scripts with your Python 3.11+ virtual environment. Resolve script paths relative to this installed skill; install requirements.txt when your selected route needs them.
