# Historical valuation and user-economics Shorts

Use this reference for every listed-company Short. The ten-year reported P/E chart is the viewer's required valuation first impression even when the main thesis is dividends, buybacks, real estate, insurance, user economics, or another operating story. It is especially important when a popular label such as `M7`, `tech`, or `consumer internet` groups companies with different revenue models and capital intensity.

## Comparator hierarchy

1. Start with the company against its own history when one consistent multiple and denominator are available.
2. Add a sector or business-model peer only when revenue model, growth stage, capital intensity, cyclicality, and valuation denominator are sufficiently aligned.
3. Use broad baskets such as M7 only as market context. Do not use their rank as the primary proof of undervaluation when the members are not economic substitutes.

Record why the comparison is valid in `brief.md`. A familiar peer label does not establish comparability.

## Historical valuation contract

- Plot ten completed fiscal or calendar years plus the dated current trailing GAAP P/E. The default is `2016-2025 year-end observations + current` for a 2026 production; update the window with the production year. Use all available completed years and label the shorter history when the issuer has not traded for ten years.
- Choose one basis: trailing GAAP P/E, forward consensus P/E, EV/EBITDA, price/free-cash-flow, or a sector-appropriate measure. Do not splice bases.
- The mandatory first-impression line uses trailing GAAP P/E. A forward P/E or sector measure may appear as a second layer, but it cannot replace or be joined into the reported trailing series.
- Use one named provider or one reproducible price-and-denominator calculation across the full series.
- State the exact window, sampling rule, and price convention. `2016-2025 year-end snapshots plus current` is different from a daily 10-year series.
- Plot every value used. Record mean, median, minimum, maximum, current value, and current rank or percentile from the ten completed-year observations. Describe the current level against that distribution in narration and large on-screen text.
- A mean can be distorted by early high-growth years or earnings shocks. Prefer the median for a normalized valuation case and show both mean and median when they lead to different impressions.
- Negative, near-zero, restructuring-distorted, or litigation-distorted earnings require an explicit treatment. Exclude only with a documented rule; never silently delete an inconvenient year.
- Render a negative or meaningless P/E as an `N/M` gap at its true year, not as zero and not as a connected point. For REITs, financials, cyclicals, or other cases where P/E is structurally weak, still show the reported P/E first impression and immediately label why AFFO, tangible book, normalized earnings, or another sector denominator carries more decision weight.
- When a material one-time gain or loss distorts the current reported P/E, plot the reported current point on the historical line and add a visually distinct adjusted-current marker beside it. State the adjustment, tax treatment, share denominator, and formula in the claim ledger. Never replace the reported point with the adjusted value or connect the adjusted marker as if it were a historical observation.
- Use precise language: `10년 평균보다 14% 낮음`, `표본 하단 3번째`, or `중앙값 아래`. Reserve `역사적 최저` for an actually verified minimum on the declared series.
- A historical multiple is not automatically fair value. Connect it to the current operating engine and risk, then show a reproducible normalized-multiple range rather than one magical target when reasonable assumptions differ.

## Required P/E scene

- Give the chart a dedicated primary visual for roughly five to nine seconds. It may share a subtle real-photo background, but the graph must dominate the content zone.
- Show a true vertical scale or directly label every annual point. Label the start year, end year, `현재`, and the exact sampling note such as `2016~2025 연말 + 2026.09.05 현재`.
- Draw a median reference line. Add the mean only when it clarifies rather than crowds the phone-size chart.
- Use one high-contrast current marker and a short conclusion badge: `10년 중앙값 아래`, `하단 2번째`, `상단 20%`, `N/M`, or another ledger-backed position.
- Keep the chart, conclusion badge, and sampling note readable together for at least one complete spoken sentence. Do not cover a point or line with an arrow, logo, source strip, caption, or pop animation at its largest extent.
- Add `HISTORICAL_PE_QA=PASS|HOLD` to verification. `PASS` requires the full series, sampling note, current marker, median, position statement, distortion treatment where applicable, and phone-size visual inspection.

## Platform user-economics contract

- Use the issuer's current unique-person metric as the primary scale number when available. Preserve `daily`, `monthly`, `account`, `person`, product scope, geography, and deduplication language.
- Never add Facebook, Instagram, WhatsApp, Messenger, Threads, or other app counts into a total when one person can use several apps.
- Product-level MAU or user milestones are supporting scale tiles. Put the original disclosure date beside every app count; a stale last disclosure must look stale on screen.
- Prefer a monetization bridge such as `unique active people growth -> ARPU/ARPP growth -> revenue growth`. This answers whether growth came from more users, more revenue per user, or both.
- ARPU and ARPP are not profit. Call them revenue per user/person. Calculate profit per person only when the numerator and denominator cover the same business, period, and population; otherwise omit it.
- When ARPP is quarterly, show the quarter. Do not annualize without labeling the calculation and seasonality limitation.
- If the company no longer reports an app-specific count, say so. Do not fill the gap with an unlabeled third-party estimate.

## Recommended 45-60 second composition

This is a structure example, not reusable factual copy:

1. **0-3s — self-history hook:** `주가는 올랐는데, 메타 P/E는 10년 평균 아래입니다.` Pair the current point with the historical reference line immediately.
2. **3-12s — historical chart:** show the complete 5-10 year series, current value, median, average, and current rank. Name the sampling rule on screen.
3. **12-21s — product scale:** show two or three dated app milestones and one deduplicated current family metric. Visually warn that app counts overlap.
4. **21-31s — monetization bridge:** compare active-person growth with ARPU/ARPP growth over the same quarter. Use an arrow only when it has a dedicated lane and no label collision.
5. **31-40s — operating payoff:** connect user economics to revenue, ad price, margin, or cash generation with one decisive metric.
6. **40-49s — strongest counterpoint:** show capital spending, margin compression, free cash flow, regulation, or another risk on the same period.
7. **49-60s — normalized value and verdict:** use the historical median and an alternative mean or conservative range, give the dated current price, then state `추천`, `관망`, or `비추천` before one invalidation condition.

For a focused 25-35 second version, keep only the historical chart, one deduplicated user metric, one ARPP bridge, and the verdict. Do not compress four app counts into unreadable tiles.

## Visual QA

- Historical charts need real axes or directly labeled points, a visible sampling note, and enough contrast between current, median, and average.
- Do not draw an evenly spaced annual chart and describe it as daily history.
- Product logos remain proportional and are identifiers, not proof of ownership or endorsement. Source each mark under `brand-assets.md`.
- Show `중복 포함, 합산 금지` near product tiles when counts overlap.
- Inspect the current point, median line, app-count dates, user-economics arrow, and verdict range at original resolution and phone scale.
