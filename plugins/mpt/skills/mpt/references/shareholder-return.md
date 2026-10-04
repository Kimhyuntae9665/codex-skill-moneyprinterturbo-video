# S&P 500 shareholder-return research and video gate

Use this reference after `us-equity-research-gate.md` whenever a Short screens or explains S&P 500 companies using dividends, repurchases, shareholder yield, payout quality, capital allocation, or total shareholder return.

The goal is to explain how cash reaches shareholders, whether per-share ownership actually improves, and whether the return can continue. Do not reduce “shareholder friendly” to a high dividend yield or a large repurchase announcement.

## 1. Define the universe and question

Record the research as-of date and the exact question before collecting metrics.

- If the request says “S&P 500,” verify index membership as of that date. Index membership changes; ticker recognition, company size, or past membership is insufficient. Prefer S&P Dow Jones Indices material. If the official constituent list is not accessible, use a dated, named secondary constituent source, label it `secondary_context`, and disclose the limitation.
- State whether the task is a single-company explainer, a screen, or a peer comparison.
- State the measurement window: latest fiscal year, trailing twelve months, or a multi-year history. Do not silently compare one company’s fiscal year with another company’s calendar year.
- Define “well returns capital” using the evidence the video will test. At minimum, a positive conclusion needs actual distributions, a dilution or share-count check when repurchases matter, and a sustainability check. Valuation may be omitted for a descriptive explainer, but it is mandatory before the video gives `추천`, `관망`, `비추천`, an entry price, or a claim of current buying appeal.

Use one of these evidence-led questions:

- How much cash did shareholders actually receive?
- Did buybacks reduce the ownership denominator after dilution?
- Can the company fund the payout through a weaker part of its cycle?
- Is management returning excess cash while preserving necessary reinvestment and balance-sheet capacity?

### Use a two-pass screen for the full index

Do not attempt to make final SEC-locked claims for all 500 constituents before knowing which companies matter.

1. **Candidate generation:** use a dated constituent list and a named standardized dataset to identify a manageable shortlist from transparent preliminary fields such as dividends paid, actual repurchases, share-count change, and cash-flow coverage. Save the retrieval time, field definitions, missing rows, and preliminary formula. These rows are discovery evidence and cannot appear as final company claims merely because the provider normalized them.
2. **Primary-source confirmation:** for the shortlist, rebuild every thesis-critical value from each company’s SEC filings and issuer IR on aligned periods. Resolve fiscal calendars, units, restatements, acquisitions, and continuing-operations differences before selecting the final subject or showing a rank.

Keep sector economics visible. Operating-cash-flow-minus-capex is often useful for ordinary operating companies, but it is not a universal payout-capacity denominator for banks and insurers; REIT analysis may require issuer-reconciled FFO or AFFO with its non-GAAP limitations. Either compare companies within a compatible group or show different sector-appropriate coverage measures without pretending they form one precise cross-sector rank. Negative or near-zero denominators make payout ratios unstable; show the cash amounts and limitation instead of producing a misleading percentage.

## 2. Lock the distribution facts

Use SEC filings and issuer IR as primary evidence. Record the source URL, form, filing date, period, raw value, unit, calculation, rounding, and limitation for every claim.

### Dividends

Keep these concepts separate:

- **cash dividends paid:** cash-flow statement outflow during the period;
- **dividends declared:** board-approved amount, which may not equal cash paid in the same period;
- **dividend per share:** per-share declaration or payment basis;
- **dividend yield:** annualized or trailing dividend divided by a dated share price;
- **dividend growth streak:** historical record through a specified declaration, not a guarantee.

State whether special dividends are included. Do not call a quarterly amount monthly income or apply a company-total dividend payment to a hypothetical holder.

### Repurchases

Keep these concepts separate:

- **authorization:** permission to buy; it is not cash returned;
- **actual gross repurchases:** shares purchased and cash paid during the period;
- **retirement or treasury treatment:** how purchased shares are accounted for;
- **issuance and dilution:** employee plans, option exercises, vesting, acquisitions, conversions, or other share creation;
- **share-count outcome:** change in period-end common shares outstanding and, separately, diluted weighted-average shares.

Do not describe gross buybacks as “net buybacks” without a declared formula. Do not subtract stock-based compensation expense from repurchase dollars as though the two were the same unit. Stock-based compensation is an expense measure; dilution is tested through issuance disclosures and share counts.

When a video says buybacks benefited continuing shareholders, show either a verified reduction in the relevant share count or a precise limitation explaining why the outcome is unclear. A falling diluted weighted-average share count may reflect timing and weighting, so preserve the definition and also inspect period-end shares when available.

## 3. Calculate only named, reproducible metrics

Choose the smallest set that answers the question. Use the same period and currency across numerator and denominator.

- **gross cash returned** = cash dividends paid + cash used for actual share repurchases.
- **gross payout ratio** = gross cash returned / defined free cash flow.
- **dividend coverage** = defined free cash flow / cash dividends paid, or show its inverse and name it consistently.
- **gross buyback yield** = actual repurchase cash / dated average or point-in-time market capitalization. State which market-cap basis is used.
- **dividend yield** = stated trailing or indicated annual dividend / share price at a stated timestamp.
- **share-count change** = ending comparable shares / beginning comparable shares − 1. Prefer like-for-like period-end common shares; keep diluted weighted-average changes separately labeled.
- **shareholder yield:** define the exact formula. If it combines dividend yield with buyback yield, say whether buybacks are gross cash outflow or a share-count-based estimate. Never mix the two approaches without disclosure.
- **total shareholder return:** calculate from an adjusted-price or price-plus-reinvested-dividend series with exact dates and benchmark. Keep it separate from company cash distributions and never present past TSR as management’s promised return.

Free cash flow is not a single GAAP line item. If using an issuer-defined version, label it non-GAAP and preserve its reconciliation. If calculating operating cash flow minus capital expenditures, name that formula and retain the SEC inputs. Record how acquisitions, asset sales, working-capital swings, and one-time tax or legal payments affect the interpretation.

Do not create a composite “shareholder-return quality score” unless the formula, weights, missing-data treatment, and ranking universe are frozen and visible. Prefer a transparent comparison of two or three deciding measures.

## 4. Test sustainability and effectiveness

A favorable shareholder-return conclusion should survive these checks where material:

1. **Coverage:** compare distributions with the defined free-cash-flow base. Use multiple years or a full cycle for cyclical or working-capital-sensitive businesses when available; one quarter is normally context, not proof of durability.
2. **Dilution:** compare actual repurchases with issuance disclosures and share-count movement. State when buybacks mainly offset dilution.
3. **Balance sheet:** inspect net debt or liquidity, near-term maturities, leverage covenants or targets, pension needs, and credit-rating commentary when the payout relies on borrowing or shrinking cash.
4. **Reinvestment:** distinguish genuine excess cash from underinvestment. Record capital expenditure, research, capacity, regulatory, or maintenance needs that compete for cash when they are central to the thesis.
5. **Cyclicality and one-offs:** identify commodity cycles, asset sales, tax benefits, litigation, unusually favorable working capital, or acquisition timing that makes the measured period unrepresentative.
6. **Management flexibility:** dividends, ordinary repurchases, special dividends, and authorizations have different commitment levels. Describe management policy accurately; do not call discretionary buybacks guaranteed.

For a screen, apply the same checks to every candidate. A missing disclosure is not zero. Do not rank incomparable or stale rows; mark them unresolved or narrow the universe.

## 5. Build the Short around the cash path

Prefer a causal story over a card sequence:

```text
cash generated
  -> reinvestment and obligations
  -> dividends + actual repurchases
  -> issuance/dilution check
  -> per-share outcome
  -> coverage and next-period decision rule
```

Useful hooks expose a verified mismatch in short, conversational Korean. Make the first clause understandable in about one second and finish the unanswered contrast within three seconds:

- **Amount shock:** “[검증된 기간]에 [검증된 금액]을 썼는데, 주식 수는 얼마나 줄었을까요?”
- **Low-yield reversal:** “배당률은 [검증된 수치]뿐인데, 주주환원은 왜 더 클까요?”
- **Dilution warning:** “돈은 잘 버는데, 왜 주식 수는 계속 늘었을까요?”
- **Execution gap:** “자사주 [승인액]을 약속했는데, 실제로 산 건 얼마일까요?”
- **Funding mystery:** “[검증된 금액]을 돌려줬습니다. 그런데 이 돈, 어디서 났을까요?”

These are narrative templates, not factual claims. Replace every bracket and premise with frozen company evidence. The tone may be punchier than the filing language, but the fact strength may not increase:

- do not turn an authorization into cash spent;
- do not turn repurchased shares into retired shares without accounting evidence;
- do not turn one period into “every year”;
- do not describe buybacks or TSR as cash deposited into every shareholder's account;
- do not present past return, a dividend streak, or a large amount as guaranteed future income.

Use vivid verbs only when technically accurate. For example, “불태웠다” requires verified retirement or cancellation rather than a gross repurchase alone. Prefer specificity and contrast over unsupported superlatives such as “S&P 500 최고의 주주환원 기업.” The body must answer the exact hook with linked claim IDs.

Match visuals to the definition:

- cash allocation: scale-accurate waterfall, Sankey, or staged flow;
- dividends versus repurchases: common-denominator stacked bars across three to five periods;
- authorization versus execution: two-step progress display, never one merged number;
- gross buybacks versus dilution: repurchase outflow beside period-end share-count movement;
- payout coverage: distributions over the same-period free-cash-flow base, with one-off qualifiers;
- TSR: indexed line chart with stated dates, benchmark, and adjusted-return basis.

Do not use a donut when dividends and repurchases are being divided by different denominators. Keep actual cash, per-share effects, and market returns visually distinct. Use a verified product, store, facility, or service environment as the photographic setting when it explains how the company generates cash; financial arrows and exact numbers remain deterministic layers.

## 6. End with an explicit verdict and measurable condition

Every stock Short must select one editorial verdict: `추천`, `관망`, or `비추천`. State it in the narration and end card. For a recommendation, show the dated current price and a reproducible valuation case before saying `추천합니다`. For `관망`, name the supported entry level or the specific missing confirmation. For `비추천`, name the failed premise or excessive price.

Use a direct final form:

- `현재 $X에서는 예상수익이 위험을 보상합니다. 추천합니다. 다만 [핵심 지표]가 [기준]을 이탈하면 판단을 바꾸겠습니다.`
- `사업은 좋지만 현재 $X는 비쌉니다. 관망하고 $Y 이하에서 매수 후보로 보겠습니다.`
- `[핵심 전제]가 깨졌고 현재 $X는 이를 반영하지 못했습니다. 비추천합니다.`

Do not finish on an unanswered question or monitoring instruction. `다음 실적에서 확인하세요` may be the invalidation clause, but it cannot be the verdict. The final measurable condition should identify what would strengthen or weaken the chosen conclusion, such as:

- free-cash-flow coverage remains above the frozen threshold through the next full period;
- actual repurchases continue while comparable period-end share count declines;
- management preserves distributions without leverage moving beyond its stated range;
- revenue or margin recovery funds the payout rather than debt, asset sales, or temporary working-capital release.

Do not infer `추천` from shareholder return alone. Index membership, a dividend streak, and past buybacks do not establish valuation or future return. Once the valuation and risk evidence are locked, state the resulting recommendation without hedging it back into ambiguity.

## Required evidence and verification fields

Add these fields to `verification.md` for applicable work:

```text
SP500_MEMBERSHIP=PASS|NOT_APPLICABLE|HOLD
SHAREHOLDER_RETURN_GATE=PASS|NOT_APPLICABLE|HOLD
RETURN_PERIOD=<fiscal year|TTM|multi-year dates>
DIVIDEND_BASIS=cash_paid|declared|per_share|yield|NOT_APPLICABLE
REPURCHASE_BASIS=actual_gross|actual_plus_dilution_check|authorization_only|NOT_APPLICABLE
DILUTION_CHECK=PASS|NOT_APPLICABLE|HOLD
PAYOUT_COVERAGE_CHECK=PASS|NOT_APPLICABLE|HOLD
SHAREHOLDER_YIELD_FORMULA=<formula|NOT_APPLICABLE>
TSR_BASIS=<dates, adjustment, benchmark|NOT_APPLICABLE>
INVESTMENT_VERDICT=RECOMMEND|WATCH|AVOID
PRICE_AS_OF=<price, currency, timestamp, timezone>
VALUATION_CASE=<method, denominator, comparison or target>
ENTRY_OR_FAIR_VALUE=<price or range>
VERDICT_INVALIDATION=<one measurable condition>
VERDICT_QA=PASS|HOLD
```

`SHAREHOLDER_RETURN_GATE=PASS` requires aligned periods, actual-versus-authorized labeling, and all thesis-critical coverage and dilution checks. `VERDICT_QA=PASS` additionally requires a dated price and a reproducible price-aware case. `authorization_only` cannot support a claim that cash was returned. `HOLD` blocks production when the unresolved distinction would change the story or verdict.
