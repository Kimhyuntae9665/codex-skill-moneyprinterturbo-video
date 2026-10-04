# Metrics and Scoring

Use reported values when available; otherwise calculate from cited source data. Show `N/A` for unstable or unavailable values.

## Core Formulas

| Metric | Formula | Notes |
|---|---|---|
| Market cap | Price x shares outstanding | Prefer latest diluted or actual shares; note if estimated from SEC tags |
| Revenue growth | Latest annual revenue / prior annual revenue - 1 | Use comparable fiscal periods |
| Net margin | Net income / revenue | Use TTM or annual consistently |
| ROE | Net income / average common equity | If average equity unavailable, use latest equity and label approximation |
| ROA | Net income / average assets | Financial firms require sector-specific interpretation |
| ROIC | NOPAT / invested capital | NOPAT = operating income x (1 - tax rate); invested capital = equity + debt - cash |
| Debt/equity | Total debt / shareholders' equity | Negative equity makes the ratio unusable |
| P/E | Market cap / net income or price / EPS | Do not use when earnings are negative or one-time distorted |
| PEG | P/E / EPS growth percentage | Use forward growth if cited; avoid when growth <= 0 or low confidence |
| P/B | Market cap / book equity | Most useful for banks, insurers, asset-heavy businesses |
| P/S | Market cap / revenue | Useful for unprofitable growth companies, but margin quality matters |
| FCF | Operating cash flow - capex | Check sign conventions; some APIs report capex negative |
| FCF yield | FCF / market cap | Prefer normalized or multi-year average for cyclical firms |
| Dividend yield | TTM dividend per share / price | Forward yield requires declared dividend policy |
| Payout ratio | Dividends / net income or dividends / FCF | Use FCF payout for capital-intensive firms |
| Total return | Price return plus dividends | Use adjusted close when available |
| Max drawdown | Trough / prior peak - 1 | Use adjusted close for long horizons |
| Volatility | Std dev of daily returns x sqrt(252) | State window length |

## Sector Caveats

- Banks: emphasize P/B, ROE, ROTCE, CET1, net interest margin, credit losses, deposit beta, and tangible book value.
- Insurers: emphasize combined ratio, investment portfolio yield, reserves, book value, and catastrophe exposure.
- REITs: emphasize AFFO/FFO, NAV, occupancy, debt maturity, cap rates, and dividend coverage.
- Utilities: emphasize regulated rate base, allowed ROE, debt, payout sustainability, and interest-rate sensitivity.
- Energy/materials: normalize through commodity cycles; use balance sheet and reserve/replacement data.
- Software/high-growth: use revenue retention, gross margin, rule of 40, SBC dilution, FCF margin, and EV/revenue.
- ADRs/foreign issuers: SEC XBRL coverage and fiscal-period comparability may be weaker.

## Screening Score

Default composite score:

| Bucket | Weight | Inputs |
|---|---:|---|
| Quality | 30% | ROE, ROIC, net margin, FCF margin, low leverage |
| Value | 25% | P/E, P/B, P/S, FCF yield, PEG where valid |
| Growth | 20% | Revenue, EPS/net income, operating income, FCF growth |
| Momentum/Risk | 15% | 6M and 1Y return, volatility, max drawdown |
| Dividend/Return | 10% | Dividend yield, payout coverage, dividend growth, buybacks |

Implementation rules:

- Rank metrics by percentile within the selected universe and, when possible, within sector.
- Invert valuation and risk metrics where lower is better.
- Cap extreme outliers at the 5th/95th percentile for scoring but show raw values in tables.
- Penalize missing critical data instead of assuming neutral quality.
- Do not let one metric dominate; require at least three valid buckets for a composite rank.

## Interpretation Rules

- Cheap + low quality is a value trap candidate, not automatically attractive.
- High dividend yield with weak FCF coverage is a risk signal.
- High ROE with high leverage or negative equity is not necessarily high quality.
- PEG below 1 is not sufficient if growth is cyclical, acquisition-driven, or margin-dilutive.
- A screen is a triage tool; always follow with issuer-level filing/news review.
