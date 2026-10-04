# Source Harvest

Use this guide to find differentiated stories without treating social media as evidence.

## Discovery order

1. **Authorized personal X surfaces:** the user's likes, reposts, bookmarks, lists, or following feed when they explicitly asked for them and the logged-in session is available. Read only.
2. **Targeted X search:** company, executives, suppliers, customers, contracts, facilities, products, and operating indicators.
3. **Targeted Reddit search:** company and ticker plus product, contract, customer, supplier, industry jargon, `DD`, `bear case`, and disputed claims; inspect substantive replies, not only post titles.
4. **Adjacent-company filings:** customers, suppliers, landlords, lenders, and competitors often disclose the relationship more clearly than the target company.
5. **Primary proof:** SEC filings, issuer IR, earnings transcripts, contract exhibits, regulator releases, court records, patent or procurement records, and official product documentation.
6. **Independent context:** reputable reporting, technical analysis, and industry data used to challenge or contextualize the primary evidence.

## X failure fallback

Do not block the run when X is unavailable. Record the failure mode and continue in this order:

1. search-engine results for the same mechanism terms and named counterparties;
2. specialist newsletters and Substack posts;
3. Seeking Alpha and other investor commentary when accessible;
4. Reddit through search-engine indexing, alternative front ends, or accessible thread pages;
5. major financial-news headlines and earnings-call Q&A for disputed or overlooked relationships;
6. the target company's customers, suppliers, landlords, lenders, and competitors in SEC or IR search.

Items 1–5 generate leads only. They do not raise a claim above C grade. Use item 6 and the primary-proof sources in the discovery order to establish A-grade facts. If no primary spine is found, reject the topic or recast it as an explicitly unresolved question without an investment verdict based on that claim.

Use `X_SCAN=USED|PARTIAL|UNAVAILABLE` and `DISCOVERY_FALLBACK=NONE|SEARCH|NEWSLETTER|COMMENTARY|REDDIT|NEWS|COUNTERPARTY_FILINGS` in the scout record. List every fallback source actually consulted.

The per-run scout should examine enough material to detect repetition rather than mistake one viral claim for consensus. When both surfaces are accessible, the default target is at least 20 relevant X posts from at least eight authors and at least eight substantive Reddit posts or comment threads from at least three communities. Search bull, bear, technical, customer, supplier, and industry-specialist views. Record raw items examined, unique authors, communities, duplicate claims, unique story clusters, and promoted finalists. Reduce the target only when access or topic sparsity makes it impractical, and state why.

Search freshness and historical depth separately: recent posts explain why the topic matters now, while older high-signal threads may reveal contracts or operating mechanics that current headlines omit. Do not equate likes, upvotes, reposts, or repeated wording with truth.

## Search families

Search by the mechanism, not only the ticker.

| Story family | Useful terms |
| --- | --- |
| Hidden contract | `take-or-pay`, `minimum revenue guarantee`, `offtake`, `residual capacity`, `revenue share`, `warrant`, `exclusivity` |
| Supply fortress | `capacity commitment`, `advanced packaging`, `HBM`, `substrate`, `lead time`, `power`, `land`, `shell`, `prepayment` |
| Capital allocation | `repurchase execution`, `share count`, `Form 4`, `strategic investment`, `authorization`, `dilution`, `convertible` |
| Demand clue | secondary-market price, used-equipment price, product lead time, backlog, utilization, app ranking, channel inventory |
| Moat change | regulator, standard change, open access, interoperability, court ruling, procurement rule, customer concentration |
| Platform economics | active users, engagement, ARPU, price per workload, inference cost, attach rate, distribution |

Add the target company's customer, supplier, landlord, and financing partner to the query. A good story often appears first in the other party's filing.

## What to record for each X post

```json
{
  "url": "https://x.com/.../status/...",
  "author": "display name or handle",
  "published_at": "ISO date when visible",
  "claim_verbatim_short": "brief quote or faithful summary",
  "mechanism_proposed": "what the author says causes what",
  "primary_source_target": "the filing, exhibit, regulator or metric needed",
  "status": "lead|corroborated|conflicted|rejected",
  "rights_note": "discovery only; do not reuse chart/image"
}
```

Keep quoted text short. Preserve URLs so the user can revisit the idea, but write the final script in original Korean.

## Pattern learned from the user's authorized likes

The useful recurring style is not generic bullishness. It tends to emphasize:

- a regulatory change that may weaken a moat;
- an indirect demand indicator that must be checked against company results;
- buyback discipline measured against price and share-count outcome;
- insider alignment verified through Form 4;
- a concrete downside model instead of a vague risk warning;
- the business process that creates value, not a macro prediction.

Use these as search patterns. Do not assume every liked post is endorsed by the user or factually correct.

Examples surfaced during the 2026-09-05 authorized scan, to be rechecked before use:

- FICO/VantageScore regulatory-moat discussion: https://x.com/VJNCapital/status/2095935101909570003
- MSCI repurchases and insider purchase lead: https://x.com/BourbonCap/status/2095985387814465747
- NVIDIA Hopper-price demand lead: https://x.com/02jason88/status/2095869112950157730
- Buyback execution versus valuation: https://x.com/DimitryNakhla/status/2095527148370923717

These links are story leads only. Verify FHFA actions, Form 4 transactions, issuer repurchases, share counts, and operating demand independently.

## Reference-video study

Before writing a new series format, inspect several recent Shorts in the same language and subject plus one high-retention adjacent explainer. Record only observable production grammar:

- first object visible in the first second;
- exact moment the unresolved question appears;
- average cut interval and longest static hold;
- ratio of real footage, screenshots, diagrams, charts, and text-only frames;
- number of spoken ideas per scene;
- when the source or proof appears;
- how the final payoff changes the opening assumption.

Do not copy a script, thumbnail, chart, footage, or creator-specific visual identity. Reuse general principles such as full-frame archival footage, one dominant sentence, frequent semantic cuts, and a reveal before explanation.

The first reference reviewed for this skill used full-frame historical trading-floor footage with one concise top statement and one bottom consequence. The useful lesson is the immediate physical context and single-message hierarchy; the weak point is that captions alone do not explain a current company mechanism. Pair that immediacy with claim-linked motion diagrams.

## Economy scout output

Use a cheap, fast model at minimal or low reasoning for the wide collection pass when the runtime permits model selection. Its output is a lead inventory, not analysis approval. It should:

1. expand five or more query families;
2. collect and normalize X and Reddit URLs and metadata;
3. summarize each lead in one or two sentences;
4. cluster duplicates and name the unresolved proof target;
5. score novelty, company specificity, visual potential, and source traceability;
6. return the best three to six candidates for full verification.

Use a stronger reasoning pass only for finalists that require contract interpretation, reconciliation across filings, numerical calculation, or a defensible investment conclusion. The research audit must name the model tier and reasoning effort used for discovery and verification when that information is available.

## Multi-story harvesting

Do not assume one video must contain one story. Build clusters around a single company identity or strategic pattern. For example, an NVIDIA dossier might separately examine networking economics, supply reservations, neocloud financing, strategic equity stakes, and software or model distribution. Select two to four only when each has a distinct mechanism and the combined thesis is stronger than any random list. Keep rejected and overflow candidates in the audit for later Shorts.
