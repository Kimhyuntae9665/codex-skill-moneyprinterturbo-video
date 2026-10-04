# Evidence Ladder

Grade each atomic claim before it enters narration, on-screen text, thumbnail, title, or verdict.

## Grades

### A — Disclosed

The claim is directly supported by a current primary source: filed financial statement, contract exhibit, official transcript, regulator decision, court record, patent, procurement notice, or issuer product documentation.

Record the exact period, unit, source URL, document date, page or section, and a short source excerpt or table cell. Preserve conditional wording.

### B — Corroborated inference

The premises are supported, but the economic conclusion is an inference. Require at least one A-grade premise and an independent source or calculation. Write the conclusion as analysis: `이는 … 가능성을 높입니다`, `이 구조라면 …로 이어질 수 있습니다`.

Examples: a capacity commitment may secure supply but can also increase inventory or cancellation risk; a revenue-share arrangement may create recurring upside but its size is unknown.

### C — Chatter

The claim exists on X, Reddit, in commentary, a user-provided lead, or an unattributed report but lacks sufficient primary support. It may appear as a clearly identified rumor, question, or disputed extension when that gap is the story. It cannot be spoken with factual certainty or supply the investment verdict.

Use a C-grade claim only when all of these are present in the same beat:

- visible `시장설`, `미확인`, or `연결 추정` label;
- origin URL, named commentary source, or `user_reported` provenance in the scout;
- the strongest A-grade fact that overlaps with it;
- a plain statement of what remains undisclosed or unconnected;
- a visual style distinct from confirmed facts.

A C-grade number may serve as a curiosity hook or large visual, but the uncertainty label must appear at the same time and with phone-size readability. Keep the rumor lane brief and pivot to evidence.

### D — Reject

Exclude from the finished video:

- anonymous or circular sourcing;
- a precise number with no discoverable calculation or document;
- private, hacked, or improperly obtained information;
- defamatory personal allegations;
- a combined segment relabeled as an undisclosed sub-business;
- a scenario presented as a signed contract;
- a causal connection created by merging unrelated disclosures.

## Claim decomposition test

For every sentence, ask:

1. What exact subject, verb, object, period, and unit does it assert?
2. Does the source prove the whole sentence or only one clause?
3. Is the verb too strong? Distinguish `committed`, `authorized`, `purchased`, `recognized`, `guaranteed`, `may use`, and `expects`.
4. Is the number disclosed, calculated, estimated, or hypothetical?
5. Does the graphic imply more than the words?

If any answer is unclear, split the sentence again.

## Numeric rules

- Every historical or current number gets an as-of date and a consistent unit.
- A calculated number stores its input claim IDs and formula.
- A scenario stores its assumptions and displays `가정` on screen.
- A market price stores timestamp, currency, and source.
- A point-to-point change stores start, end, and elapsed interval.
- A percentage share is not inferred from a dollar amount unless both numerator and denominator share the same definition and period.

## Fact-versus-inference display

Use visible labels when the distinction matters:

- `공시 확인` for A-grade facts;
- `계산` for reproducible arithmetic;
- `가능성` or `시나리오` for B-grade analysis;
- `X에서 도는 주장` or `Reddit에서 나온 주장` for a C-grade lead being tested;
- `확인 안 됨` for a popular extension the evidence does not support.

The source strip must remain legible but does not replace the narration's wording boundary.

## Common AI-infrastructure traps

- **Revenue-share percentage:** the existence of revenue sharing does not disclose its percentage. A number such as 50% remains C-grade market chatter unless the exact contract supports it; if shown, pair it with `비율 미공개`.
- **Idle capacity use:** a residual-capacity obligation and a separate open-model R&D cloud agreement do not prove that the same idle GPUs run a named model. The connection can be explored as a labeled hypothesis, followed by the evidence needed to confirm it.
- **Networking revenue:** NVIDIA's `Compute & Networking` reportable segment is combined. Do not call the entire segment networking revenue.
- **Chip adoption:** distinguish testing, availability, planned consumption, and contractual commitment.
- **Supply commitment:** purchasing or capacity commitments are not current revenue and can create downside if demand or deployment timing changes.
- **Equity ecosystem:** an investment may improve alignment or access, but it can also concentrate counterparty and valuation risk.

## Promotion rule

A C-grade lead can become A only after the primary document directly proves it. Repetition by multiple X accounts does not upgrade evidence. A B-grade conclusion remains B even when all of its premises are A; do not erase the inference boundary. Including C-grade chatter is an editorial device, not an evidence upgrade.
