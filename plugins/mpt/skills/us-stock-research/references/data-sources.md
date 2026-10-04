# Data Sources

Use primary/official sources first. Use vendor and scraped sources as convenience layers only after labeling limitations.

Source links were checked on 2026-06-08. Re-check when a provider endpoint, plan, or rate limit matters.

## Verified Links

- SEC EDGAR API documentation: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- SEC ticker to CIK JSON: https://www.sec.gov/files/company_tickers.json
- SEC company facts bulk archive: https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip
- FRED API documentation: https://fred.stlouisfed.org/docs/api/fred/
- Alpha Vantage documentation: https://www.alphavantage.co/documentation/
- FMP developer documentation: https://site.financialmodelingprep.com/developer/docs
- OpenBB Platform documentation: https://docs.openbb.co/platform/
- Nasdaq Trader Symbol Directory definitions: https://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs
- Fama-French Data Library: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
- Stooq historical data page: https://stooq.com/db/h/

## Source Priority

| Priority | Source | Best use | Access | Caveats |
|---|---|---|---|---|
| 1 | SEC EDGAR APIs | 10-K/10-Q/8-K filing history, XBRL facts, CIK mapping | No auth for public JSON APIs | Requires respectful rate limits and descriptive User-Agent; XBRL tags differ by company; not all metrics are directly reported |
| 1 | Company IR / press releases | Guidance, presentations, dividends, buybacks, earnings releases | Web pages/PDFs/RSS | Narrative can be promotional; verify against SEC filings |
| 1 | FRED / Treasury / BLS / BEA | Rates, inflation, GDP, employment, yield curve, macro context | Public APIs, some require API key | Release schedules and revisions matter; use vintage data when backtesting macro decisions |
| 2 | Nasdaq Trader Symbol Directory | Current listed symbols and exchange metadata | Public web/FTP | Current-day list; not a historical constituent database |
| 2 | Fama-French Data Library | Factor returns and portfolio factors | Public downloads | Factor definitions and frequency must match the return window |
| 2 | Stooq | Free historical OHLCV CSV for many US stocks and ETFs | No key | Vendor-adjustment details and coverage vary; verify unusual dates/prices |
| 2 | yfinance / Yahoo Finance | Historical prices, dividends, splits, snapshots, analyst/news fields | Python package, no official Yahoo API contract | Unofficial; rate limits and schema changes can break workflows |
| 3 | Financial Modeling Prep (FMP) | Screener, ratios, statements, TTM metrics, bulk fundamentals, analyst data | API key/subscription | Plan limits; vendor-calculated fields require formula checks; useful endpoints include `company-screener`, `ratios`, `ratios-ttm`, `key-metrics-ttm`, and bulk ratios/key metrics |
| 3 | Alpha Vantage | Time series, company overview, fundamentals, technical indicators, macro | Free API key and paid tiers | Rate limits; endpoint coverage varies; official docs include `TIME_SERIES_DAILY`, adjusted daily data, `OVERVIEW`, statements, earnings, and economic indicators |
| 3 | OpenBB Platform | Aggregated equity/fundamental/screener/news workflows | Open-source package plus provider credentials | Output quality depends on configured providers |
| 3 | Polygon / Twelve Data / Benzinga / Tiingo / Finnhub | Market data, news, fundamentals, estimates, corporate actions | API keys, free/paid tiers | Licensing and rate limits differ by plan |
| 3 | GDELT / broad web news | Broad media/news discovery | Public APIs/web | Finance relevance and duplicate removal require filtering |

## SEC EDGAR Notes

- Map ticker to CIK with `https://www.sec.gov/files/company_tickers.json`.
- Pull filing history with `https://data.sec.gov/submissions/CIK##########.json`.
- Pull all company XBRL facts with `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json`.
- Pull one concept with `https://data.sec.gov/api/xbrl/companyconcept/CIK##########/us-gaap/<Tag>.json`.
- Use nightly bulk archives for large-scale jobs instead of hammering per-company endpoints.
- Prefer `10-K`, `10-Q`, `20-F`, `40-F`, and material `8-K` filings for investment research.

## Universe Selection

- `sp500`: acceptable for current screens when pulled from a current public constituent page, but label the retrieval date and warn about survivorship bias for historical analysis.
- `nasdaq-listed` / `nyse-listed`: use Nasdaq Trader current symbol files or vendor symbol directories.
- `sec-reporters`: use SEC CIK mapping; this includes entities that may not be actively traded common stocks.
- Historical constituent analysis requires a historical membership source; do not infer past S&P 500 membership from today's list.

## News Source Rules

- Use direct company releases and SEC 8-K filings as primary event evidence.
- Use at least two reputable news sources for disputed or market-moving stories.
- When Helium MCP is available, use bias scores and balanced-news synthesis for controversial topics.
- Always report article publication date, event date, source, and whether the content is confirmed by filings or company statements.

## Data Quality Warnings

- Ticker symbols can be reused; historical work should use CIK, CUSIP/ISIN, or issuer identity when possible.
- Free price sources may revise adjusted prices or have missing dividends/splits.
- Vendor ratios may differ because of leases, non-controlling interest, preferred equity, fiscal calendars, and normalized earnings adjustments.
- Banks, insurers, REITs, BDCs, MLPs, and ADRs need sector-specific metrics.
