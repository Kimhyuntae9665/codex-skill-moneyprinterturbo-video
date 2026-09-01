# US equity research gate

Use this reference whenever an evidence-motion Short makes claims about a US-listed company, ticker, ETF, valuation, dividend, repurchase, beta, performance comparison, or institutional ownership.

The mandatory order is:

```text
us-stock-research
  -> SEC and issuer-IR primary-source lock
  -> Unusual Whales secondary check
  -> claim-ledger freeze
  -> narration, scene contract, render, MoneyPrinterTurbo, QA
```

The first four stages produce an evidence packet. Video production may read that packet but must not mutate it.

## 1. Run us-stock-research

Invoke the installed `us-stock-research` Skill and define these items before drafting the hook:

- ticker, legal issuer name, CIK, exchange, and security type;
- research as-of date and market-price timestamp;
- adjusted or unadjusted price basis;
- trailing, forward, fiscal-year, or calendar-year basis for each valuation metric;
- dividend-yield definition and payment/cut/suspension treatment;
- benchmark, sampling interval, currency, and period for performance, beta, and correlation;
- peer or historical comparison method;
- thesis, counterpoint, invalidation rule, and unresolved questions.

Save a short research note and a source inventory. Separate issuer-reported facts, calculations, secondary context, interpretation, and unresolved items.

## 2. Lock SEC and issuer-IR evidence

Use SEC EDGAR filings, SEC XBRL/Companyfacts when appropriate, and official issuer IR materials as the final evidence for company claims. Prefer the source that directly reports the required period and definition; do not assume the newest document is automatically comparable.

Record for every primary-source claim:

- claim ID and exact on-screen display value;
- form or document type;
- period start and end, fiscal context, and as-of date;
- filed or published date;
- SEC accession/document URL or issuer-IR URL;
- reported value and unit;
- formula and script path for a calculated value;
- rounding rule and limitation.

Apply these source rules:

- Revenue, earnings, cash flow, debt, cash, shares, guidance, and segment facts: SEC filing first; issuer earnings release or presentation may clarify management guidance and non-GAAP reconciliation.
- Dividends: issuer declaration history and SEC filings. State whether yield is indicated, trailing, or forward and which price date is used.
- Repurchases: SEC cash-flow/share-repurchase disclosures and share-count reconciliation. Distinguish authorization from actual purchases and gross repurchases from net share-count change.
- Valuation: pair a dated price basis with the aligned SEC-derived denominator. Label trailing versus forward and reported versus adjusted.
- Historical price, drawdown, beta, correlation, and benchmark returns: use a named price source, adjusted-price basis where distributions/splits matter, explicit dates, and a reproducible calculation path.
- 13F: use SEC Form 13F filings or SEC-derived filing data. Show manager, issuer/security, quarter end, filing date, reported value or shares, and the delayed long-only disclosure limitation. Never call a 13F row a current trade or current position.

If a claim cannot be locked to an appropriate primary source and the distinction matters to the thesis, classify it as unresolved and exclude it from the video.

## 3. Perform the Unusual Whales secondary check

Unusual Whales is a corroboration and market-context layer. It never replaces the primary-source lock.

Use only capabilities actually available in the current session. Common permitted mappings are:

- stock chart: dated price path, comparison overlay, or implied-move context;
- market map: broad market or sector-relative context;
- market tide: market-wide options-flow context.

Do not use Unusual Whales fiscal rows as final evidence for revenue, cash flow, debt, dividends, repurchases, valuation denominators, or ownership. Do not infer directional positioning from options premium, dark-pool volume, gamma exposure, or max pain alone.

Write one status into the evidence packet:

- `used`: identify the exact tool/output, retrieval time, claim IDs checked, and what it corroborated;
- `not_relevant`: explain why the available market-context outputs do not test the claims in this Short;
- `unavailable`: record the unavailable connector/tool without inventing a result;
- `conflicted`: record the mismatch and send the affected claim back to the primary-source stage.

For a conflict, first align ticker/security, timestamp, timezone, split/dividend adjustment, fiscal period, unit, and definition. SEC or issuer IR controls reported company facts. Do not average values. Omit an unresolved claim.

## 4. Freeze the claim ledger

Start from `assets/templates/finance-claim-ledger-v1.csv`. Use these evidence tiers:

- `primary_reported`: directly reported by SEC or issuer IR;
- `primary_calculated`: reproducibly calculated from locked primary inputs;
- `secondary_context`: dated market or comparative context from a named provider;
- `interpretation`: thesis language supported by linked claim IDs;
- `unresolved`: cannot be used on screen or in narration.

Allowed verification states are `verified`, `conflicted`, and `excluded`. The `secondary_check` field records the Unusual Whales status and output reference when applicable.

Freeze only when all on-screen claims have:

- one definition, unit, period, and as-of date;
- a resolvable source URL;
- an explicit price/return adjustment basis when relevant;
- a formula or script path for calculations;
- no unresolved source conflict;
- identical display text planned for narration, subtitles, charts, and labels.

Write the freeze timestamp and ledger SHA-256 into `verification.md`. Any later factual change invalidates the freeze and requires narration, subtitles, scene manifest, source lines, and QA to be regenerated.

## 5. Hand the frozen packet to video production

Production may simplify visual density but may not change claim meaning. Link every factual scene element to a frozen claim ID. Place concise source lines inside the source-safe zone and reserve the caption-safe zone for Korean subtitles.

The end card must express a conditional decision or invalidation rule, not an unconditional recommendation. State the research as-of date and material limitations. For 13F, repeat the quarter-end and delayed-disclosure caveat on the ownership scene or its source line.

## Required verification record

Before delivery, `verification.md` must contain:

```text
US_STOCK_RESEARCH=PASS|FALLBACK|HOLD
PRIMARY_SOURCE_LOCK=PASS|HOLD
UNUSUAL_WHALES=used|not_relevant|unavailable|conflicted
CLAIM_LEDGER_FREEZE=<ISO-8601 timestamp>
CLAIM_LEDGER_SHA256=<hash>
VIDEO_QA=PASS|HOLD
```

`FALLBACK` is allowed only when the named Skill cannot run but an equivalent SEC/IR-first workflow was completed and documented. `HOLD` blocks the renderer or delivery.
