---
name: moneyprinterturbo-video
description: Create and verify a finished short-form MP4 with MoneyPrinterTurbo. Use for YouTube Shorts, Reels, TikTok, Korean narration, evidence-led finance and US-equity shareholder-return explainers, deterministic data motion, or requests that expect the final video rather than instructions alone.
---

# MoneyPrinterTurbo Video

Produce the finished video, verify it, and return its absolute path. Do not stop at setup, a storyboard, or render commands.

## Route the request

- Use `prepared-local` when the script and rights-cleared local visuals already exist.
- Use `topic-online` when MoneyPrinterTurbo must draft the script or find online footage. Request only credentials named by `MPT_NEEDS_INPUT`.
- Use `evidence-motion` as the strict `prepared-local` submode for financial claims, charts, maps, brand architecture, institutional ownership, or tightly directed motion. Freeze evidence and geometry before rendering, then pass one continuous master MP4 to MoneyPrinterTurbo.

Read only the references required by the selected route:

- On Windows: [references/local-windows.md](references/local-windows.md) for the installed Python runtime and PATH refresh.

- All runs: [references/modes.md](references/modes.md).
- Directed or evidence-led work: [references/evidence-motion-workflow.md](references/evidence-motion-workflow.md), [references/scene-contract.md](references/scene-contract.md), and [references/professional-motion.md](references/professional-motion.md).
- Every portrait video: [references/visual-quality-gate.md](references/visual-quality-gate.md).
- Every narrated Short: [references/editorial-tempo.md](references/editorial-tempo.md) for reference breakdown, TTS silence editing, and semantic cut alignment.
- External AI-video references or a specific material, camera, editing, or sound defect: [references/reference-to-production.md](references/reference-to-production.md) for purpose-based source selection, disclosed-setting limits, and translation into a tested production decision.
- Considering an external image, I2V, TTS, or music generator: [references/generative-component-selection.md](references/generative-component-selection.md) for component-level trials, Korean voice comparison, music briefs, and actual plan/output eligibility.
- Every YouTube Shorts growth or publishing-package request: [references/channel-growth-loop.md](references/channel-growth-loop.md) for audience promise, topic selection, hook experiments, and post-publication learning.
- Every evidence-motion production: [references/production-source.md](references/production-source.md) for the single-source build and truthful delivery-status gate.
- US-listed securities: [references/us-equity-research-gate.md](references/us-equity-research-gate.md).
- Every company or stock Short: [references/company-signature-thesis.md](references/company-signature-thesis.md) for the mandatory X thesis scan and one company-specific, evidence-backed story that viewers can remember.
- Historical valuation, platform scale, active-user, ARPU/ARPP, or network-effect theses: [references/historical-valuation-user-economics.md](references/historical-valuation-user-economics.md).
- S&P 500 membership, dividends, repurchases, dilution, shareholder yield, payout sustainability, or total shareholder return: [references/shareholder-return.md](references/shareholder-return.md), after the US-equity research gate.
- Company relationships, service architecture, partner roles, and workflows: [references/infographic-motion-bridge.md](references/infographic-motion-bridge.md) and the installed `logo-flow-infographics` Skill. Use its logo-first, minimal-text graph style; keep quantitative trends, comparisons, compositions, and 13F figures in scale-accurate deterministic charts.
- Every company Short, before choosing official demo footage, live interface/ranking captures, photographs, marks, or substitutes: [references/brand-assets.md](references/brand-assets.md). Apply its actual-media and service-identity reviews even when the company sells no physical product.
- Every video: [references/official-footage-production.md](references/official-footage-production.md) for the minimum 60% official-video runtime share and the user-approved Muse V2 production method: action-matched excerpts, large authentic identities, measured speech cuts, and phone-size review.
- On a fresh or shared installation, if present: `references/portable-install.md`; run `python scripts/check_environment.py --json` before the first render.

The MCD v8 evidence-motion package is the visual and QA reference. Use its principles - frozen claims, subject-relevant physical metaphors, continuous motion, large Korean text, and boundary-frame inspection - without copying its company-specific content.

## Narrative and retention contract

### Choose a familiar format and a coherent viewer frame

Before drafting, record `format_family` (how the story is presented), `topic_frame` (the interest shared by the intended viewers), and `viewer_continuity` (why someone who watched the preceding relevant episode would watch this one). A repeated company logo or the broad label “US stocks” does not establish that continuity. Expand a series through an adjacent viewer question, with a complete answer in this episode; avoid unrelated trend chasing or withholding the answer to force a follow-up.

Apply the evaluated creator-learning notes in [references/creator-learning-20261003.md](references/creator-learning-20261003.md): measure meaningful visual information, remove redundant headings and text layers, and compare the opening and densest number sentence at normal speed. Creator explanations of recommendation thresholds are hypotheses, not platform rules. Keep the official-video runtime minimum at **60%**, and preserve measured analytics and financial evidence gates.

### Connect the technology to real events — minimum 30% of runtime

For company, stock, AI, and technology Shorts, at least **30% of the final narrated runtime** must explain subject-relevant nontechnical news, current issues, user adoption, market reactions, partnerships, competition, customer behavior, or business consequences. Technical mechanisms and repeated equipment imagery must not dominate by default. This applies to news/story explainers as well as valuation videos; it does not require adding a buy/sell verdict to a user-requested news explainer.

- In the single-source timeline, mark intervals `news_context`, `technical`, or `other`, and write the spoken point, directly matching visual, source, and date. Compute `NEWS_CONTEXT_SHARE = union of news_context intervals / final narrated runtime`; require at least `0.30`. Exclude silent covers/end padding, and do not double-count mixed scenes: split at the actual semantic transition. Do not inflate the share by inserting unrelated headlines, stretching stills, or relabeling technical narration.
- Examples of qualifying content: a dated US App Store ranking and what it shows about adoption; a dated stock move and the reported catalysts; a verified partnership or access restriction and who gains or loses. A company logo, generic city/server image, or news screenshot behind technical narration alone does not count.
- Use direct visual evidence when the sentence reports an observable event: real ranking capture for ranking, actual app UI/demo for product use, sourced news excerpt for an announcement, and a dated measured chart for price changes. Preserve ranking country/category/date and financial period. Never generate a fake screenshot or stock-price path. Use an explicitly labeled sourced editorial chart when a historical screenshot cannot be obtained; disclose the difference.
- Before rendering, reject each shot whose subject/action cannot explain the concurrent spoken sentence. Change visual form with the information: source capture, product demo, financial chart, relationship scene, then a mechanism diagram only where the mechanism is being explained. A new camera angle or changed heading on the same generic chip/server set does not resolve monotony.
- At final review record the measured share and inspect the actual news intervals for legibility and story relevance. If the verified news is insufficient, research more relevant context or shorten the technical section; do not invent news to satisfy the quota.

Record the editorial route before applying the valuation sections below. In a user-requested `news-explainer` (for example, why a stock moved after an app launch), the payoff is the supported explanation of that event. The P/E and price-aware verdict requirements below apply when making a valuation or investment-recommendation case; they must not displace the requested news explanation. State this route explicitly in `production.json`. Fact, source, period, thumbnail, and review requirements still apply.

For valuation and finance Shorts, default to the **Disconnect** story: show a visible mismatch, explain what causes it, test the counterargument, and finish with an explicit investment verdict. The verdict must be `추천`, `관망`, or `비추천`; do not dissolve the conclusion into a question or a list of things to watch. Treat the company's own ten-year P/E history as the required valuation first impression for every listed-company Short; read [references/historical-valuation-user-economics.md](references/historical-valuation-user-economics.md) before drafting or rendering it.

Choose the story from the evidence rather than forcing every company into dividend yield or undervaluation:

- **Company signature thesis:** every company Short must contain one spoken, visually demonstrated sentence that explains what makes this business structurally distinctive. Discover candidate angles through a targeted X scan, then verify every factual premise with SEC, issuer IR, contracts, or another appropriate primary source. The signature thesis must be specific enough that swapping in another ticker would make it false. Place it in the first half of the Short and connect it directly to the valuation, operating metric, risk, or verdict; do not leave it as an isolated slogan.
- **Valuation disconnect:** price or multiple versus an aligned operating denominator and the strongest reason the discount may persist.
- **Self-history and user economics:** when peers have different business models, compare the company with its own consistently defined historical valuation first, then connect the rerating case to active people, engagement, ARPU/ARPP, ad load or price, and operating profit per user where officially supportable.
- **Income durability:** dividend amount or growth versus free-cash-flow coverage, leverage, cyclicality, and the next declaration or operating condition.
- **Shareholder-return engine:** cash generated -> dividends and actual repurchases -> dilution or share-count result -> sustainability. A large authorization or gross buyback headline is not the payoff unless execution and dilution support it.
- **Capital-allocation tradeoff:** compare shareholder distributions with reinvestment, debt reduction, or acquisition needs using one period and a clearly defined cash-flow base.

For an S&P 500 shareholder-return request, do not rank candidates from dividend yield alone. Verify current index membership as of a stated date, use a dated broad screen only to generate a shortlist, then lock shortlisted companies to SEC/IR and compare actual cash returned, the resulting share-count change, and coverage on a consistent basis. Keep banks, insurers, REITs, and ordinary operating companies on defensible sector-appropriate payout-capacity measures rather than forcing one free-cash-flow denominator across the index. Read `references/shareholder-return.md` before drafting the hook or screen.

0. **Mandatory standalone thumbnail; optional embedded cover:** Every video created with this skill must produce a separate thumbnail image at the same time as the MP4. For a company or stock Short, the thumbnail must contain the verified company logo or mark, the company/ticker identifier, and one short Korean sentence that represents the video's central thesis or verdict. Make the line concrete and conversational, such as `자사주 매입에 진심인 병원주`; keep it to one thought and no more than two short lines. Use a clean hierarchy with generous empty space, one dominant focal point, and no decorative clutter, source text, footnotes, progress bars, captions, or duplicate headlines. The logo must remain proportional and immediately recognizable. Export a native 1080x1920 PNG or JPEG; do not rely on a contact-sheet crop, screenshot of the player, or low-resolution preview. Embed the cover in the video only when it is also the strongest first visual for the spoken hook. If embedded, start the spoken hook at 0.0 seconds or as close to it as the voice permits and keep the complete hook within three seconds; do not add a silent cover hold merely to expose the thumbnail.
1. **Hook, 0-3 seconds including the thumbnail cold open:** Open in short, conversational Korean with one concrete surprise, contradiction, or consequence. The first semantic beat should register in about one second and the complete unanswered question should be clear within three seconds. Pair it with a visual that proves the tension. Reading the company name, ticker, dividend yield, or video title alone does not pass. Avoid greetings, company history, academic phrasing, and claims of guaranteed returns.
2. **Mandatory ten-year P/E first impression, normally 3-12 seconds:** Every listed-company Short must show a readable line chart covering ten completed fiscal or calendar years plus the dated current trailing GAAP P/E. State the exact window and sampling rule on screen, show every plotted observation, and mark the current level against at least the ten-year median and range or percentile. Speak one plain conclusion such as `10년 중앙값 아래`, `하단 20%`, or `과거보다 비쌈`. Do not replace the chart with one current multiple or an unlabeled sparkline. If the issuer has less than ten years of public history, plot all available years and state the shorter window. If P/E is negative, not meaningful, structurally weak for the sector, or distorted by a material one-time item, keep that fact visible in the P/E scene and add the aligned sector metric or separately labeled adjusted current marker; never silently omit P/E or splice an adjusted point into a reported historical series.
3. **Primary evidence, roughly 10-24 seconds:** Use one or two decisive SEC/IR metrics. Explain why they matter rather than reading a list.
4. **Bull-versus-bear conflict, roughly 24-47 seconds:** Put the attractive evidence and its strongest risk into the same story. Treat the company as a question to resolve, not a collection of cards.
5. **Verdict and price case, roughly 47-60 seconds:** Put the conclusion first and say it plainly: `현재 $X에서는 매수 매력이 있어 추천합니다`, `매력은 있지만 $X 이하까지 관망합니다`, or `현재 가격에서는 비추천합니다`. A `추천` verdict requires a dated current price, a reproducible valuation basis, and one decisive reason the expected return compensates for the main risk. Follow with one compact invalidation condition; do not replace the verdict with that condition. End on the verdict visually as well as verbally.

Before applying those timings, choose and record one duration profile. Use `focused` (about 25-35 seconds) for one question with two or three decisive numbers, or `full` (about 45-60 seconds) when the counterargument and price case require the extra time. The timing ranges above describe the full profile. Do not pad a focused script or compress a full thesis until its definitions become unreadable.

### Start from the viewer's question

- In `brief.md`, state the intended viewer, their immediate question, why it matters now, the one answer delivered by this Short, and the channel promise it reinforces.
- Before writing hooks, record `SIGNATURE_THESIS` as one conversational Korean sentence, the X posts that inspired the angle, the primary-source claim IDs that verify it, the decisive visual proof, and one condition that would weaken it. Also record `X_THESIS_SCAN=USED|UNAVAILABLE|CONFLICTED`. X is a discovery surface for investor language and overlooked relationships, not evidence for company facts.
- Search X for at least three recent, relevant posts from at least two independent authors when accessible. Search beyond the ticker using combinations such as `moat`, `misunderstood`, `not just`, `full stack`, `distribution`, `pricing power`, `network`, `supply`, `contract`, and the company's key product or segment. Extract the recurring causal idea; never copy a creator's wording, chart, or image without permission.
- Reject generic signature lines such as `AI 수혜주`, `좋은 브랜드`, `시장 1위`, or `주주환원을 잘한다`. A usable line identifies the distinctive system and its economic consequence, such as `제품 A와 유통망 B가 지표 C를 끌어올리는 회사`.
- The signature thesis must be spoken and shown, normally within the first 20 seconds. It may supply the hook, the answer to the hook, or the bridge into the hero metric. It cannot exist only in the title, description, thumbnail, or research notes.
- Build one Short around one investment question. Two or three hero numbers are the normal starting point; split additional independent claims into another complete Short or move supporting detail to the description.
- Write three hook candidates before narration. Select by immediate comprehension, viewer relevance, specificity, evidence strength, and connection to the final payoff. A stronger adjective cannot rescue a weak or unrelated answer.
- Give every production a `strategy_id`, `series`, `topic_hypothesis`, `hook_variant`, and `duration_profile`. These fields describe an experiment; they are not predictions of reach.
- Produce an upload package with three title candidates, one selected title, the thumbnail sentence, the first two description lines, dated source links, and one meaningful viewer question. For company Shorts, default to a provocative identity, territorial-expansion, hidden-control, or broken-intuition title such as `엔비디아는 ETF다`, `엔비디아의 미친 영토 확장`, or `아마존은 쇼핑몰이 아니다`. Keep routine price, P/E, growth, and target figures inside the video and description; do not turn the title into a row of metrics. Use one number only when it is the irreducible mystery. Aggressive metaphors are allowed when the video resolves their real meaning early and does not create a false legal or factual classification. Do not use fabricated urgency, a ticker-swapped template, or repetitive engagement bait.

### Make the verdict decisive

- The channel's editorial purpose is to identify attractive or unattractive stocks. Every completed stock Short therefore chooses one of `추천`, `관망`, or `비추천` and displays it in large, high-contrast type during the final beat.
- When the frozen evidence supports a buy case, use direct language such as `현재 $X, 저는 매수 매력이 있다고 봅니다. 추천합니다.` State the price timestamp and whether the case rests on earnings, free cash flow, assets, peer multiples, or shareholder yield.
- When price is above the supported entry range, state the actionable level: `좋은 기업이지만 현재 $X에서는 관망, $Y 이하에서 매수 후보입니다.`
- When the thesis fails, say `비추천합니다` and name the failed premise. Do not use vague endings such as `다음 실적을 지켜보세요`, `확인이 필요합니다`, `어떻게 될까요?`, or `투자 판단은 각자` as the final conclusion.
- A disclaimer, risk, or monitoring condition may follow in one short clause, but it may not weaken or obscure the selected verdict. Put the verdict before the caveat and repeat the verdict on the end card.
- Strong color and impact are encouraged: use a consistent verdict color, decisive scale-down typography, a short impact sound, and a stable reading hold. Color communicates the decision; it does not substitute for valuation evidence.
- If the research cannot support any price-aware verdict, stop before rendering and complete the missing valuation work. Do not manufacture a `추천` merely because the subject was requested or because the company pays a dividend.

Use `setup -> conflict -> resolution` even when the exact timing differs. A financial script should feel like a strategic mystery: "Why is this cash-generating company still priced this way?" is stronger than a sequence of unrelated ratios.

### Review the opening before full production

Record in `brief.md` the exact opening line, the first visual, the question the viewer should want answered, and the later beat that answers it. Name the company when it helps understanding; withholding its name alone is not a mystery. If the standalone thumbnail is not embedded, record `THUMBNAIL_FRAME_INTERVAL=STANDALONE_ONLY`.

- Record the thumbnail sentence, logo/mark asset ID and rights note, composition description, exact stable-frame interval when embedded in the video, and absolute exported PNG/JPEG path. The thumbnail sentence is a claim subject to the same ledger and fact-strength ceiling as narration. Words such as `소각`, `말소`, `매년`, `최고`, or `미친 기업` require evidence for their literal premise and period. Gross repurchases or a lower period-end share count alone do not prove retirement or cancellation; use wording such as `자사주 매입에 진심인 기업` or a verified share-count result when that is the supported claim.
- Judge the thumbnail at phone size and as a standalone still. The logo must be recognizable and proportional, the identifier and representative sentence must remain legible, and the image must not resemble an official company endorsement. The core sentence and logo must be understandable without the video title, narration, captions, or description. Use a logo only after the source, reuse terms, and trademark context have been recorded under `brand-assets.md`.

- Reject an opening such as `배당 7%, 카지노 건물주 VICI`: it labels a topic without creating a reason to continue. An illustrative question such as `카지노의 진짜 건물주는 누구일까요?` can work when the following evidence answers it; adapt wording and timing to the actual subject. Examples are not verified current claims.
- Write the spoken hook as a person would say it: short clauses, familiar words, one vivid verb, and one unresolved contrast. Prefer patterns such as `[검증된 큰 금액]을 썼는데, 주식 수는 왜 그대로죠?`, `배당은 [검증된 낮은 수치]뿐인데, 주주환원은 왜 더 클까요?`, or `돈은 잘 버는데, 왜 주식 수는 늘었을까요?` only when the frozen evidence supports every premise.
- Enforce a **fact-strength ceiling**: a stronger tone may compress or dramatize a verified contrast, but may not strengthen the underlying claim. Do not turn `authorized` into `spent`, `repurchased` into `retired`, a one-period amount into `every year`, gross buybacks into account cash, or historical return into promised income. Replace unverified specifics with a ledger-backed value or reject the hook.
- The impact must come from specificity, contrast, rhythm, and the first visual rather than unsupported superlatives, fear, certainty, or a withheld answer. The video must explicitly pay off the opening question with linked claim IDs.
- Generate a short opening TTS preview at the selected voice and rate. Review only its first three seconds with the opening visual. The tension must already be clear; a question mark at the end of a long sentence does not satisfy this gate.
- Revise the line, emphasis, or first visual before generating the full narration and master. Do not repair a weak hook merely by adding a louder sound or larger title.

### Make numbers understandable

Keep two language layers aligned:

- On-screen metrics use the exact filing or market-data vocabulary and frozen value, such as `AFFO/share $2.46`, `FCF $4.2B`, or `YoY +18%`. Preserve English abbreviations when they are the precise financial identifier; add a short Korean label when it improves comprehension.
- Korean narration translates the meaning into plain language without changing the definition, period, or unit. Do not replace a precise metric with a looser synonym that overstates cash, profit, ownership, or return.

Every number in narration, subtitles, graphics, and source lines must resolve to the same claim ID and display value.

- A point-to-point change is incomplete without its interval. Place the start date, end date, and elapsed period adjacent to the change metric in the primary visual, large enough to read on a phone. For example, show `2026.01.31 → 2026.07.31 · 6개월` beside `전체 공시 주식 수 −3.52%`; a tiny source line or narration-only date does not satisfy this rule. Distinguish elapsed time from the number of named calendar months: January 31 to July 31 is six elapsed months even though seven month names appear on a calendar.
- Keep the denominator and population visible when a percentage could be ambiguous. Say `전체 공시 주식 수`, `Class B 주식 수`, `희석주식 수`, or the applicable basis instead of showing an unexplained percentage.

For each decisive monetary claim, give the viewer a usable scale: per share, per quarter, per 100 hypothetical shares, or another relevant basis. Speak the consequence as well as the decimal; do not narrate a chain of dollar amounts and ratios without interpretation.

- For a Korean general audience, prefer a rounded KRW equivalent for one key dollar amount when it improves intuition. Verify the exchange-rate source and date, show the assumed rate, retain the original USD value, and record the conversion and rounding in the ledger before freezing it. Omit the conversion and record why if reliable FX is unavailable; never invent a current rate.
- Label hypothetical holdings, tax basis, and period. A hypothetical share-count calculation is not the user's actual portfolio or a guaranteed future payment. Do not describe a quarterly dividend as monthly income.
- Use a concrete comparison only if its denominator is supported. Preserve distinctions such as AFFO versus accounting earnings and contractual rent versus guaranteed income. When a derived explanation is added after freezing, revise and re-freeze the ledger before regenerating dependent audio and visuals.

## US equity research gate

For every US-equity Short, enforce this dependency chain before production:

```text
us-stock-research -> SEC and issuer-IR primary-source lock -> Unusual Whales secondary check -> claim-ledger freeze -> video production
```

This is a gate, not a suggestion:

1. Invoke `us-stock-research` and define ticker, legal issuer, CIK, as-of date, price basis, valuation denominator, comparison method, thesis, counterpoint, and unresolved questions.
2. Freeze the mandatory ten-year reported P/E series and current point before narration. Record provider, exact window, annual or periodic sampling rule, adjusted-price convention, denominator definition, every plotted value, median, mean, minimum, maximum, current rank or percentile, and any N/M or one-time-item treatment. A current market-data timestamp must be visible in the ledger and scene.
3. Run the company-signature X scan, freeze one company-specific thesis, and map every factual premise to primary-source claim IDs. If X is inaccessible or yields only unsupported repetition, record that result and derive the angle from SEC/IR without pretending an X review occurred.
4. Lock fundamentals, guidance, dividends, repurchases, share counts, and 13F rows to SEC EDGAR or issuer IR. Record period end, filed date, document URL, raw value, calculation path, rounding, and limitation.
5. Record the Unusual Whales decision as `used`, `not_relevant`, `unavailable`, or `conflicted`. It is a dated market-context check, not primary evidence for fundamentals, valuation denominators, dividends, buybacks, or institutional ownership.
6. Align timestamp, timezone, adjusted-price basis, unit, fiscal period, and definition before resolving conflicts. SEC or issuer IR controls reported company facts. Never average conflicting values; omit unresolved claims.
7. Freeze the ledger before narration or layout. Production may simplify density but may not mutate claim meaning.

## Shareholder-return gate

When the thesis includes shareholder friendliness, buybacks, shareholder yield, payout quality, or S&P 500 screening, apply [references/shareholder-return.md](references/shareholder-return.md) before freezing the ledger.

- Treat cash dividends paid and shares actually repurchased as distributions. Keep declared dividends, repurchase authorizations, and management intentions separate from completed cash outflows.
- Show repurchase effectiveness as a second layer: gross repurchase dollars do not prove per-share benefit when stock issuance, equity compensation, acquisitions, or other dilution keep the share count flat or rising.
- Test sustainability with a reproducible cash-flow base and period. Label issuer-defined free cash flow as non-GAAP; otherwise show the calculation from operating cash flow and capital expenditures. Do not call a payout safe from one favorable quarter.
- Keep shareholder yield, payout ratio, and total shareholder return distinct. Any yield needs a dated price or market-cap basis; total shareholder return includes market-price movement and is an outcome rather than cash distributed by the company.
- For comparisons, align fiscal or trailing periods, currencies, share-count definitions, and market-data timestamps. Omit or qualify a ranking when companies cannot be compared on the same basis.

For 13F, show manager, issuer/security, quarter end, filing date, and shares or reported value. State that 13F is delayed, long-only disclosure - not a current trade, cost basis, or proof of present ownership.

## Visual and motion contract

### Mandatory official-video use — minimum 60% of the final video

Every video must use **official source videos for at least 60% of its entire final MP4 runtime**. The user clarified that this measures official-video use time, including natural reading/waiting moments inside a playing source excerpt; it does not measure seconds of continuous visible movement. This replaces the earlier 50% moving-visual rule.

- Count relevant, attributable official product demonstrations, shopping/checkout recordings, event footage, and issuer/institution footage while the original video excerpt plays as a main readable subject. Retain provenance, source in/out times, actual output intervals, and the use basis. A historical or general-service demonstration may qualify with clear on-screen and spoken context; do not imply it is footage of a different product or current transaction.
- Do not count photographs, screenshots, extracted still frames, photo pan/zoom, self-made logo flows/charts, generative video, unofficial stock footage, decorative effects, or a tiny official insert under a dominant static slide. These may supplement the story but do not satisfy this quota. Exclude editor-added frozen tails, loop-padding used merely to inflate the share, and intervals where the source is hidden.
- Calculate `OFFICIAL_VIDEO_SHARE = union duration of eligible official-video output intervals / entire final MP4 duration`; require `>= 0.60`. Include covers, reading holds, and silent/end padding in the denominator; never double-count overlapping clips. A 60-second video requires at least 36 seconds of official video. Native pauses within a playing official source remain eligible.
- Plan the share before rendering and verify it on the final timeline/playback in `official-video-report.json`. Report `OFFICIAL_VIDEO_SHARE`, `OFFICIAL_VIDEO_QA=PASS|HOLD`, and the report path in verification and delivery records. Missing measurement or a share below 60% is HOLD: source better matching official excerpts or shorten static explanation, then remeasure. Do not pad irrelevant footage or silently substitute animation for the quota.
- Preserve the separate 30% news-context requirement, source/use review, legibility, and technical checks. A footage-share PASS does not assert constant movement or a freeze-detector PASS.

### Reuse the approved Muse V2 production method

Follow [references/official-footage-production.md](references/official-footage-production.md): open with one concrete question over real action; show a concise role map early when needed; pair each spoken action with a matching official excerpt; explain each company's strategy in one sentence; state conditions/counterevidence; answer the opening question. Use large original identities, a consistent top identity / central footage / lower Korean explanation layout, measured narration cuts, and actual phone-size playback review. Replace weak source cuts with clearer source actions and repair unreadable overlays before delivery. Adapt the method to the subject rather than copying Muse facts, dates, or a fixed scene count.

### Actively use official footage, real screens, and authentic photographs

User-approved direction from the Muse/AMD/Intel revision: **make relevant official product-demo excerpts, real service screens, live ranking screenshots, and authentic company/product photographs primary visuals throughout the story.** Source these before designing replacement graphics. The approved examples are the actual Meta product demonstration during the product-use sentence and the actual US free-app chart during the ranking sentence; reuse that method, not their old facts or assets for unrelated subjects.

- Show the thing being discussed: product action -> a matching official demo excerpt; app ranking -> the actual dated ranking screen; launch/partnership -> the announcement or relevant official footage; product/facility -> its authentic photograph. Use multiple relevant moments across the Short, not one token screenshot followed by generic machinery.
- For a feature/action scene, usable footage or UI takes priority over a logo, generic 3D chip, stock server room, or text card. Use diagrams/Blender when they explain an unseen mechanism or relationship that the source material cannot show. Record a concrete sourcing or editorial reason when a planned actual-media scene needs a substitute.
- Make the selected footage/capture the main readable subject. Crop or reframe for 9:16 around the action, app identity, rank, or announcement; preserve context. Add concise Korean explanation, a deliberate highlight, and a source/date label. Do not hide the useful material behind large opaque panels or constant subtitles.
- Synchronize the spoken action with the excerpt: a form submission supports `신청`, not automatically `결제` or `예약`. Preserve the action's setup and result. Label company-supplied material `공식 제품 시연 · 발췌` when needed; do not present a promotional demonstration as independent testing or actual user adoption.
- For rankings, retain the country, category, free/paid distinction, observation date, app name, and visible rank. Keep screenshot contents authentic; commentary/highlights belong in separate overlays. A recreated graphic is not a screenshot. Prefer original media assets over enlarging a tiny icon cropped from a screen.
- Apply the sourcing, excerpt, audio, and review details in `brand-assets.md`. Record `ACTUAL_MEDIA_QA` with scene IDs and inspected playback intervals. Relevant media use does not by itself satisfy the separate 30% news requirement: the narration must also explain nontechnical news/context.

### Default to recognizable real-world photo backgrounds

- For scenes explaining a physical place or business, retain the MCD real-store preference: use authentic, subject-relevant location photographs across the portrait canvas. Official-demo and real-screen scenes above instead let that material own the canvas; they do not need an unrelated location photograph underneath. The desired quality is the visible reality of the subject. Choose colors for the subject and photograph; navy and gold are not required. A later explicit visual-style request overrides this preference.
- Show the relevant physical business: restaurant/store exteriors and interiors for a franchise, the identified properties for a REIT, or verified factories, shelves, and distribution sites for a manufacturer. Source and inspect photographs before locking the layout, using the provenance and use-terms checks in `brand-assets.md`. Do not imply that an unidentified building belongs to the issuer or that an older reference photo depicts current conditions.
- Let the photograph fill the background behind titles, numbers, charts, and captions. Keep enough of the building, storefront, or environment recognizable at phone size. A small photo inside a card, a solid-color slide, or an image hidden by an opaque panel does not fulfill this default. Use gentle local shading, gradients, restrained shadows, or compact translucent panels to make text readable without obscuring the scene. Preserve photographic color and detail where possible.
- Reframe proportionally and use subtle purposeful camera movement. Follow the explanatory-beat rules below: introduce another relevant view, a real product image, or a relationship/flow/comparison as the narration advances. A repeating photo with only new text or pan/zoom is insufficient. Keep foreground text steady during reading holds.
- In `brief.md`, link each background asset to its scene and record the crop, focal subject, contrast treatment, and any justified exception. A chart may briefly need a clean field; restore the photographic setting when appropriate. If suitable real photos cannot be used after sourcing, document the fallback instead of silently returning to generic slide backgrounds. Generated scenery is not an authentic location photograph.

### Pace with meaning

- Plan an explanatory visual beat about every two to four seconds: a relevant new shot, a relationship revealed, a scale-accurate comparison, or a causal flow advancing with the narration. Keep exact values still long enough to read; record a justified longer reading hold in the shot plan when necessary.
- In `brief.md`, list each shot's time range, primary visual or asset, narration beat, and what new information the visual change reveals. In a typical 45-60 second company Short, vary the views with purpose, such as property -> operator/landlord relationship -> rent flow -> shareholder payment -> risk comparison. Choose views that fit the subject, not a fixed asset quota.
- Reusing one full-screen photograph under changing text for most of the Short fails this editorial gate. Pan/zoom, color changes, caption entrances, and counting the same number do not by themselves count as a new explanatory beat. A neutral recurring background is acceptable when the foreground genuinely changes the explanation; a continuous diagram is acceptable when its structure progressively explains the story.
- A state change must explain the argument. Do not use unrelated wipes, glows, coins, machinery, or random 3D objects merely to keep pixels moving.
- Freeze detection measures technical frame change, not storytelling. Do not add arbitrary drift solely to clear it, or cite a freeze-detector pass as proof of dynamic pacing.
- Let exact text and values settle before the reading hold. Keep text stationary while the viewer must read it.
- Use kinetic typography only for the active verb and core metric, such as `SOLD $4.2B` or `DIVIDEND 70Y`. Do not animate an entire paragraph as one block.
- Use subject-relevant physical metaphors: property and rent flow for a REIT, stores and royalties for a franchise, products and repeat purchase for staples. Generated plates contain scenery only; exact text, numbers, maps, charts, and logos remain deterministic layers.

### Use actual products for product recognition

- When a scene introduces what a company sells or which brands it owns, prioritize authentic product photographs or official packshots with verified use terms. Real packaging is part of the explanation. A generic can or bag with a brand name underneath does not meet this default; a logo alone is a secondary choice when the product itself is the subject. Respect an explicit user request for an illustrated treatment.
- Before locking the layout, inspect official media/brand asset libraries and relevant product pages, then suitable licensed photo sources if needed. Record the candidates, source and terms URLs, intended use, and selection or rejection reasons in `sources.md` using `brand-assets.md`. An unperformed search is not evidence that photos are unavailable or prohibited by copyright.
- Use a substitute only after documenting why suitable real images could not be used and what the substitute loses. Do not silently downgrade to generic shapes or fabricate branded packaging. General category diagrams remain appropriate for explaining mechanisms where identifying an actual product is not the point.
- Review a representative product scene before full rendering and the actual final frames at phone size: packaging must be recognizable, sufficiently large, proportionally scaled, and matched to the correct brand. Record `PRODUCT_ASSET_QA`; missing sourcing work or an unexplained substitution is a HOLD even if geometry and encoding pass.

### Direct the deciding moments

- Choose a few emphasis moments, typically two or three in a 45-60 second Short, based on the argument. Give those moments a brief, deliberate entrance such as a scale-down stamp or a contrasting highlight that settles; a fade alone does not fulfill a planned impact cue. Ordinary labels and supporting numbers can enter quietly.
- Fit the motion to the word or number. Do not require 150%-to-100% scaling for every metric. Check the largest animated extent, especially for long KRW labels, and let the complete value and unit remain still long enough to read. Emphasize the callout without distorting quantitative chart geometry.
- In `brief.md`, plan each cue with its scene/element and claim ID where applicable, spoken phrase, intended emphasis word, visual action, and sound choice. After narration is approved, record the actual audio timestamp and align the visual landing and any short sound accent to that emphasis. Respect no-effects preferences and use the same rights checks as music.
- Keep the accent subordinate to the spoken number. Avoid repeated flashes, identical stamps on every statistic, or louder BGM as a substitute for timing. Follow `scene-contract.md` to carry the cues into the renderer and inspect their peak, landing, and reading hold.

### Map data to the right visual

- Valuation or peer rank: horizontal ranked bar or a scale-accurate custom chart.
- Historical valuation: for every listed-company Short, a mandatory ten-completed-year line plus the dated current trailing GAAP P/E from one consistent methodology, with real scale, every observation, a clearly labeled current point, the ten-year median, and an explicit statement of the current rank or percentile. Show mean when it materially changes the impression. Reserve N/M gaps and separately styled adjusted markers for negative or distorted earnings; never join them as ordinary reported observations. Never call a value `역사적 최저` from a chart that contains lower observations.
- Platform or marketplace economics: show unique active people first, then ARPU/ARPP or profit per person on the same definition and period. Use separate product tiles only as scale context; do not add overlapping app user counts into a fake total.
- Revenue, cash flow, or shareholder return: waterfall, Sankey, or causal flow.
- Target or decision price: valuation target ladder with current, watch, and invalidation states.
- Historical trend: line chart with a single direct endpoint callout.
- Two-sided thesis: binary comparison with one deciding metric.
- Compact 13F view: disclosure date first, then two or three readable manager rows.

For a company with multiple named businesses, map each spoken business or segment to a recognizable visual identity before rendering. A text label inside a generic number card is insufficient when a sourced service logo, official icon, product image, app mark, interface crop, storefront, facility, or editorial composite can identify it. In the signature-thesis and primary-evidence section, show at least two distinct business-identity assets when two or more businesses drive the thesis. Keep metrics dominant, but reserve roughly 15-30% of the card or scene for the identifying asset and show it for at least one full spoken clause. Do not reuse the parent-company logo as the only identity for every segment.

Use at most two ratios per scene. Use `logo-flow-infographics` for verified company/service relationships, with authentic identities, short names, and clear curved connectors. Put interpretation, conditions, and source labels outside the graph. Use deterministic charts for numerical comparisons; a logo flow must not replace a quantitative scale or imply an unverified integration.

### Fill the portrait frame deliberately

- Start from the large type scale in `visual-quality-gate.md`. Shorten or split copy before shrinking it.
- When revising a small-text draft, enlarge ordinary visible copy by about 20% and the smallest chart or card labels by about 40%, then reflow the layout.
- Make meaningful content occupy roughly 60-85% of the central content zone. A large white card containing a tiny diagram is a failed composition even if the card fills the canvas.
- Crop intrinsic white or transparent margins from imported SVG/PNG assets before scaling. Use available space to enlarge the chart, property, product, map, or comparison - not to add decoration.
- Keep title, qualifier, metric, source, and caption in separate readable regions. Fail on clipping, collisions, weak contrast, caption intrusion, logo deformation, blank flashes, diagonal transition bars, or leftover underlines.
- Give arrows, connector lines, and their arrowheads a dedicated lane between labels or values. They may not pass behind text, terminate under a number, touch glyph bounds, or make direction ambiguous. Declare connector geometry in the scene contract and inspect its maximum animated extent; shortening or rerouting the connector is preferable to hiding it behind a foreground value.
- In product scenes, give authentic product images and readable product/category labels the space they need; reduce the item count before making packaging tiny. Apply the sourcing and documented-fallback rules above rather than treating generic icons as the default.

### Direct online footage precisely

In `topic-online`, specify the subject, emotional tone, shot scale, and camera movement for each clip - for example, `investigative slow push-in on a casino exterior at blue hour` or `fast hyper-lapse of city traffic`. Reject generic business meetings, handshake footage, and unrelated skyscrapers unless they directly support the narration.

## Audio and narration contract

- Choose a voice that matches the topic. For Korean finance, prefer a calm, engaged delivery with a questioning hook, clear emphasis on the deciding metric, and a deliberate pause before the counterpoint. Calm does not mean identical cadence throughout. Verify the selected voice name before rendering.
- Preserve the user's preferred voice character, including a calm, weighty male voice when requested. Plan different delivery for the question, explanation, deciding number, and counterpoint. Move uncomplicated explanation along while leaving numbers, units, and conditions intelligible; do not make constant speed or breathless delivery a goal.
- Current user preference: Korean finance narration should be about **30% faster than the original PEP baseline** (2026-09-03, ko-KR-HyunsuMultilingualNeural, segment rates 0.94-1.02). Use a relative 1.30 times speed as the starting point while retaining that voice character and clear numbers. A later explicit speed request overrides this preference. Do not apply another 1.30 multiplier to an already accelerated revision.
- Record the baseline and applied speed factor in `brief.md`. For new TTS, translate the relative factor into the verified provider's rate controls and audition a representative passage; a provider rate number is not a measured duration ratio. For an existing narration, a pitch-preserving tempo adjustment before mixing can implement the relative speed precisely. Do not speed up BGM or the entire mixed soundtrack merely to accelerate speech.
- Write short spoken sentences and place a pause only where anticipation or comprehension benefits. A half-second pause is an option for a major turn, not a requirement before every number. Audition the hook, a dense numeric sentence, and the risk turn; punctuation suggests delivery but does not guarantee a pause duration or rising question pitch.
- Verify the active MoneyPrinterTurbo wrapper and provider support before using SSML, pitch, or other expressive controls. Do not pass unsupported raw SSML such as `<break>` into Edge TTS. If precise pauses or different sentence rates are needed and direct controls are unavailable, synthesize phrase segments through the verified MPT voice path, insert measured silence where intended, and listen for unnatural joins. Do not switch to a paid voice provider without charge authorization.
- Finalize speech timing before locking visual and sound cues. After changing rate, pauses, or phrasing, update subtitle timestamps, scene boundaries, and cue timing against the resulting audio; a plan or SSML tag is not proof of audible expression.
- Treat narration timing as an editorial audio pass, not only a playback-rate setting. Generate or obtain the dry TTS, measure silent runs, distinguish intentional dramatic or comprehension pauses from synthesis slack, and shorten only the unplanned gaps before locking scene timing. Complete this pass before adding effects or music so silence processing cannot damage accents or desynchronize cuts. Keep the measured before/after report beside the brief.
- Align visual cuts to completed semantic units in the approved narration. Do not remove the relevant visual while a company name, number and unit, comparison, or qualifying clause is still being spoken. Introduce the next primary visual at the next clause or sentence onset, with only a justified lead. Record the actual audio boundary and cut offset in frames; a proportional retime of an older timeline is insufficient evidence.
- A requested speed increase may shorten the video below the default 45-60 seconds. Set and record the resulting duration target before validation; do not pad with silence or slow the narration again simply to meet an example's minimum duration. Recheck the shortened reading holds and product-identification beats.
- For narrative Shorts, default to planning a quiet instrumental bed that supports the tension and resolution, subject to the user's audio preferences. Use a user-provided, owned, or verified license-compatible no-cost track; record source, license, attribution, and file hash. Respect explicit no-BGM requests. If no suitable track is available, use deliberate silence and report that choice instead of silently treating missing BGM as complete sound design. Paid music still requires explicit charge authorization.
- Keep speech dominant. Start the bed roughly 18-24 dB below the narration's measured average level, then adjust by listening; this is a starting point, not a loudness guarantee. Duck it further during dense numbers, fade the ends, and use only restrained effects at meaningful turns. Do not select random unverified music or bury speech under a dramatic track.
- Pronunciation-check ticker symbols, acronyms, decimals, currencies, dates, and large numbers. Rewrite phonetic narration when needed while preserving the on-screen metric.
- Listen to the actual final mix for cadence, intelligibility, pauses, pronunciation, and clipping. ASR, stream presence, volume measurements, and frame inspection cannot establish that the voice sounds natural. Record who or what actually reviewed audio; if listening is unavailable, record `AUDIO_LISTENING=NOT_PERFORMED` and do not claim a listening pass.

## Safety contract

- Do not publish to YouTube, TikTok, Instagram, or another service unless the user separately requests publishing. The helper must keep Upload-Post disabled.
- Do not use Seedance, WaveSpeed, LoomLoom, Sonilo, or another paid provider without explicit confirmation of the charge.
- Do not expose credentials, `config.toml`, environment values, or full credential-bearing logs.
- Use only owned, generated, public-domain, or license-compatible assets. The upstream MIT license does not cover third-party fonts, music, photos, stock media, or trademarks.
- Run one video job at a time. Do not start the WebUI, API server, Docker service, or cross-posting service for an ordinary request.

## Prepared-local execution

Resolve the Skill directory, set the working directory to `scripts`, and call the helper by relative filename. Keep the command in the foreground and allow at least 20 minutes:

```text
uv run --no-project --python 3.11 python mpt_agent.py --subject "<topic>" --script-file "<utf8-script>" --material "<rights-cleared-master-video>" --font-file "../assets/fonts/NotoSansKR-Bold.ttf" -- --video-source local --video-aspect 9:16 --video-count 1 --video-concat-mode sequential --video-clip-duration 60 --video-transition-mode none --voice-name <verified-voice> --voice-rate <verified-rate> --video-language ko-KR --bgm-type none --subtitle-enabled --subtitle-position custom --custom-position 70
```

The helper pins MoneyPrinterTurbo commit `eb8c23757e098a07bbcd93b3b50e252fc8d1869a`, uses an isolated runtime and frozen dependencies, forces the final-video stage, disables social upload, and prints `MPT_RESULT` only for non-empty MP4 files.

The command above produces narration without a music bed. When the audio plan includes BGM, use the pinned runtime's verified local-track options or mix that cleared track into the narrated output afterward. Avoid double-mixing existing audio, preserve synchronization, and run final QA on the actual mixed deliverable.

## Evidence-motion production

Do not begin the renderer with unfrozen claims.

1. Create one canonical `production.json` following `references/production-source.md`. It owns the frozen claims, script segments, asset records, voice settings, strategy metadata, duration profile, emphasis events, and thumbnail package. Generate or verify `brief.md`, `sources.md`, a dated claim ledger, `narration.ko.txt`, and `reference-breakdown.md` from that source. Analyze at least one recent, genuinely comparable external Short or a user-supplied editorial reference without copying its script, assets, or claims. Record observable timing and screen grammar, then state which findings will and will not be applied. Review the full-resolution standalone thumbnail, the complete opening preview, and a representative synchronized metric cue before the full render.
2. Classify each data scene as `logo_flow`, `custom_chart`, or `non_chart`. Give `logo-flow-infographics` only the frozen nodes, directed edges, branch meaning, claim IDs, and approved local identity assets. Save editable graph JSON, asset/source manifest with hashes, SVG, and a full-resolution PNG preview. Follow its dark dotted canvas, white rounded logo cards, short names, proportional marks, and curved-arrow style. Preserve exact scales and values in a separate deterministic chart when the scene is quantitative. Real shopping and checkout footage remains the primary visual for observable actions.
3. Copy `assets/templates/shorts-scene-contract-v1.json`. Declare scene boundaries, safe zones, element boxes, containment, claim IDs, assets, text roles, logical font sizes, and purposeful state changes. For product scenes, finish the source/terms review and representative product preview before locking the layout; link the selected asset or documented fallback to its scene.
4. Validate geometry before render:

```text
python validate_scene_manifest.py "<scene-manifest.json>" --report "<layout-report.json>"
```

5. Generate the dry narration first, audit and edit its silence according to `editorial-tempo.md`, then derive final word or phrase timestamps. Lock subtitle cues, semantic scene cuts, and emphasis events to that edited audio in that order. Never retain a parallel hand-edited scene file that can silently override stale timed data. Render one continuous 1080x1920, 30 fps master against those locked boundaries. Render and export the mandatory 1080x1920 thumbnail during the same production run. When the cover is embedded because it strengthens the hook, export its exact stable frame; otherwise render it from the same frozen logo, sentence, and visual system and record `STANDALONE_ONLY`. Keep the platform-caption band quiet. Disable MoneyPrinterTurbo transitions and set clip duration at least as long as the narration.
6. Generate narration and final assembly through MoneyPrinterTurbo. Preserve the task log and output paths.
7. If Edge subtitle aggregation fails, preserve the MoneyPrinterTurbo audio, use an already available Whisper model only for timestamps, replace its text with the human-reviewed SRT, and burn it with `burn_subtitles.py`. Do not use unreviewed speech recognition as final financial copy.

## Verification gate

Run the automated gates after final audio and reviewed subtitles exist:

```text
python validate_video.py --video "<final.mp4>" --log-file "<MPT.log>" --frames-dir "<qa/representative>" --min-duration 45 --max-duration 60
python probe_scene_frames.py "<final.mp4>" "<scene-manifest.json>" --out-dir "<qa/scene-probe>" --require-audio
python validate_delivery.py "<delivery-status.json>"
```

Require the requested aspect ratio, decodable video and audio, audible narration, H.264/AAC for the default YouTube target, and a full FFmpeg decode. The scene probe must match the declared duration, resolution, frame rate, boundaries, and midpoints and report no freeze of at least one second.

Automated checks do not replace visual review. Inspect at original resolution and at a phone-scale preview:

- 0.0 and 0.2 seconds;
- every scene boundary and both sides of each transition;
- first stable entry, 25%, 50%, 75%, and last stable exit for animated or dense scenes;
- the maximum extent, landing, and reading hold of each selected emphasis cue;
- the smallest chart label, densest caption, brand-heavy scene, and final decodable frame.

Also review the opening and full sequence in motion against the brief: is the tension clear by three seconds, do the shots advance the explanation, does a key number have a comprehensible scale, and is the promised question answered? Contact sheets alone cannot verify rhythm. Review the final mixed audio separately as described above. Record inspected timestamps and concrete evidence for each editorial result; a declared storyboard is not proof that the rendered video follows it.

Replay each selected emphasis cue with sound: the visual landing and any sound accent should reinforce the intended spoken word, preserve its intelligibility, and leave a readable hold. Record this evidence under the existing visual-pacing and audio review results. Treat direction choices as editorial hypotheses; do not claim improved retention without audience data.

For an evidence-motion US-equity Short, `verification.md` must record:

```text
US_STOCK_RESEARCH=PASS|FALLBACK|HOLD
PRIMARY_SOURCE_LOCK=PASS|HOLD
UNUSUAL_WHALES=used|not_relevant|unavailable|conflicted
SP500_MEMBERSHIP=PASS|NOT_APPLICABLE|HOLD
SHAREHOLDER_RETURN_GATE=PASS|NOT_APPLICABLE|HOLD
REPURCHASE_BASIS=actual_gross|actual_plus_dilution_check|authorization_only|NOT_APPLICABLE
DILUTION_CHECK=PASS|NOT_APPLICABLE|HOLD
PAYOUT_COVERAGE_CHECK=PASS|NOT_APPLICABLE|HOLD
INVESTMENT_VERDICT=RECOMMEND|WATCH|AVOID
PRICE_AS_OF=<price, currency, timestamp, timezone>
VALUATION_CASE=<method, denominator, comparison or target>
ENTRY_OR_FAIR_VALUE=<price or range>
VERDICT_INVALIDATION=<one measurable condition>
VERDICT_QA=PASS|HOLD
CLAIM_LEDGER_FREEZE=<ISO-8601 timestamp>
CLAIM_LEDGER_SHA256=<hash>
HOOK_QA=PASS|HOLD
THUMBNAIL_FRAME_QA=PASS|HOLD
THUMBNAIL_FRAME_INTERVAL=<start-end seconds or STANDALONE_ONLY>
THUMBNAIL_EXPORT=<absolute PNG/JPEG path>
THUMBNAIL_RESOLUTION=1080x1920
THUMBNAIL_LOGO_ASSET=<asset ID and rights note>
THUMBNAIL_SENTENCE=<one representative Korean sentence>
THUMBNAIL_CLEAN_LAYOUT_QA=PASS|HOLD
VISUAL_PACING_QA=PASS|HOLD
NUMBER_COMPREHENSION_QA=PASS|HOLD
PERIOD_CONTEXT_QA=PASS|HOLD|NOT_APPLICABLE
CONNECTOR_CLEARANCE_QA=PASS|HOLD|NOT_APPLICABLE
REFERENCE_BREAKDOWN_QA=PASS|HOLD|NOT_APPLICABLE
SILENCE_DENSITY_QA=PASS|HOLD|NOT_APPLICABLE
SEMANTIC_CUT_QA=PASS|HOLD|NOT_APPLICABLE
PRODUCT_ASSET_QA=PASS|FALLBACK|HOLD|NOT_APPLICABLE
SERVICE_IDENTITY_QA=PASS|FALLBACK|HOLD|NOT_APPLICABLE
ACTUAL_MEDIA_QA=PASS|FALLBACK|HOLD|NOT_APPLICABLE
OFFICIAL_VIDEO_SHARE=<official-video union seconds / entire final MP4 seconds; minimum 0.60>
OFFICIAL_VIDEO_QA=PASS|HOLD
OFFICIAL_VIDEO_REPORT=<absolute official-video-report.json path>
SOUND_PLAN=<track and mix choice, or reason for silence>
AUDIO_LISTENING=PASS|HOLD|NOT_PERFORMED
STRATEGY_ID=<stable experiment identifier>
SERIES=<channel topic series>
TOPIC_HYPOTHESIS=<viewer question and expected value>
HOOK_VARIANT=<candidate identifier>
DURATION_PROFILE=focused|full|custom
UPLOAD_PACKAGE=<absolute JSON/Markdown path>
VIDEO_QA=PASS|HOLD
```

Apply the `PRODUCT_ASSET_QA` meanings in `brand-assets.md`. A documented, visually reviewed fallback may satisfy the asset review, but must remain labeled `FALLBACK` and be disclosed at delivery. Missing investigation is `HOLD`, never `FALLBACK` or `NOT_APPLICABLE`.

Apply `SERVICE_IDENTITY_QA` to every company Short that names a product, platform, segment, or service. `PASS` requires a sourced and recognizable identity asset for each thesis-critical business, visual review at phone size, and at least two distinct identities in a multi-business thesis. A text-only metric card or repeated parent logo is `HOLD` when a usable identity asset was available. A documented editorial pictogram or composite is `FALLBACK`, not `PASS`.

Apply `ACTUAL_MEDIA_QA` from `brand-assets.md` to observable product actions, rankings, events, and real-world subjects. Check the actual rendered excerpt against its concurrent narration, not just the asset filename. Skipped sourcing, mismatched actions, fabricated screenshots, or unreadable proof are `HOLD`; repair them before finished delivery.

Set overall `VIDEO_QA=PASS` only after the technical, visual, editorial, and actual listening checks pass and `validate_delivery.py` accepts the corresponding status artifact. Do not deliver as finished on `HOLD`, `NOT_PERFORMED`, unresolved claim conflict, failed layout, missing audio, empty planned emphasis cues, missing standalone thumbnail, clipped or overlapping text, blank transition frames, unreadable phone-scale labels, deformed logos, a vague non-verdict ending, or an investment verdict unsupported by a dated price and reproducible evidence. Repair recoverable defects and rerun only the affected gates. If a check cannot be completed, report the failed or unavailable stage and artifact paths as a review draft, without calling it finished or fully verified.

## Delivery

Return the absolute MP4 path and the mandatory absolute thumbnail PNG/JPEG path together, plus duration, video and thumbnail resolution, codecs, narration language and voice, source mode, validation result, data as-of date, primary-source-lock status, Unusual Whales decision, selected title and description package, strategy ID, and material limitations. A video-only delivery is incomplete. State explicitly whether social publishing occurred. Publishing itself remains separately authorized. When the user later supplies Studio data, append same-age 24-hour, 72-hour, and 7-day observations under `references/channel-growth-loop.md`; do not call a single result causal proof.
