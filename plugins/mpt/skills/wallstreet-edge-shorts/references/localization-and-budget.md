# Korean Localization and Information Budget

Use this reference for every Korean narration and scene plan.

## Narration priority

In company-story mode, preserve information in this order:

1. the opening causal question;
2. the familiar but incomplete mental model;
3. the hidden mechanism and the document-backed answer;
4. the measurable or visible economic consequence;
5. the closing payoff that resolves the first frame;
6. the strongest counterpoint and supporting context.

Items 1–5 should normally be spoken. Supporting context moves to the description or another Short. In investment-story mode, add the dated valuation basis, verdict, and invalidation condition after the mechanism; remove supporting context before compressing the mechanism.

When rumor-like material is the hook, reserve a five-to-eight-second chatter lane inside items 1–2. A connected dossier may use up to three short chatter beats when each leads to a different documented mechanism. Speak it as `이런 말이 돕니다`, `X에서는 이렇게 연결합니다`, `Reddit에서는 이런 해석이 나옵니다`, or `여기서부터는 추정입니다`; never spend so long on the rumor that the documented mechanism loses its explanation time.

Do not insert a ten-year P/E chart, current price, or recommendation in company-story mode by default. In investment-story mode, the ten-year P/E view may become a three-to-four-second visual valuation stamp when valuation is not the main story. It still needs the current trailing GAAP P/E, ten-year window, median, current position, sampling note, and phone-size readability.

Do not solve density by accelerating TTS beyond the production skill's established rate, shrinking source text, overlapping clauses, or displaying several independent numbers at once. Split the topic when the mechanism requires more than three to six causal steps.

## Two-layer translation

For specialized finance, infrastructure, or contract language:

- **Narration layer:** conversational Korean that a general investor understands immediately.
- **Precision layer:** the exact English term plus the narrow legal or accounting meaning on screen and in the source map.

Keep the metaphor structurally faithful. Preserve the subject, obligation, covered amount or portion, condition, period, and uncertainty that matter to the thesis.

| Source term | Preferred Korean narration | Precision label |
| --- | --- | --- |
| `take-or-pay` | `안 써도 최소 약정량은 돈을 내는 계약` | `Take-or-pay · 최소 사용량 지급 약정` |
| `capacity backstop` | `빈 서버 자리를 일정 부분 대신 사주는 안전판` | `보장 범위: 계약상 일부 용량` |
| `minimum revenue guarantee` | `최소 매출선을 받쳐 주는 보장` | `Minimum revenue guarantee · 조건 확인` |
| `revenue share above a floor` | `기준 매출을 넘으면 일부를 다시 나누는 구조` | `Revenue share above floor · 비율 비공개` |
| `offtake agreement` | `생산 전에 구매 물량부터 잡아두는 계약` | `Offtake · 사전 구매/인수 약정` |
| `remaining performance obligations` | `아직 매출로 잡히지 않은 계약 잔액` | `RPO · 취소/이행 조건 확인` |
| `supply and capacity commitments` | `앞으로 쓸 공급과 생산 자리를 미리 묶어 둔 약정` | `확정 매출 아님 · 취소/수요 위험` |
| `warrant` | `정해진 가격에 주식을 살 수 있는 권리` | `Warrant · 행사조건/희석 확인` |

Reject a translation when it changes economics. Examples:

- Do not translate a partial capacity backstop as `모든 빈 서버를 책임진다`.
- Do not translate an undisclosed revenue share as `수익의 절반을 받는다`.
- Do not translate a commitment as cash already spent or revenue already earned.
- Do not translate a right or option as ownership already acquired.

## Spoken-density gate

Before TTS, mark every sentence as `HOOK`, `WRONG_MODEL`, `MECHANISM`, `STORY_PAYOFF`, `VALUATION`, `VERDICT`, `COUNTERPOINT`, or `SUPPORT`. Company-story mode should normally contain no `VALUATION` or `VERDICT`. Remove or relocate `SUPPORT` first. The dry narration passes only when:

- one sentence teaches one idea;
- a new specialist term is followed immediately by its plain meaning;
- no scene asks the viewer to understand more than one new causal relation;
- the mechanism remains understandable with captions alone;
- the closing payoff—or the investment verdict when requested—is not rushed into the last second.

If the first pass fails, reduce concepts rather than shortening every pause.
