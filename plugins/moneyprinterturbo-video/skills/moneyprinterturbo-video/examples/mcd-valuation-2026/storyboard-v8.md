# MCD 조건부 분할매수 Shorts v8 스토리보드

기준일: 2026-08-31 미국 종가 · 최종 1080×1920 · 30fps · 약 58.5초

이 문서는 `narration.v8.ko.txt`와 `subtitle.v8.srt`를 1:1로 연결하는
14-scene manifest 초안이다. 장면은 0초에서 시작하며, 표의 `end`가 다음
장면의 `start`와 정확히 일치한다. 각 장면은 하나의 주동작, 제한된 카메라
움직임, 지연된 보조동작을 가진다.

## Boundary lock

`0, 4.0, 7.45, 10.95, 15.15, 19.75, 23.95, 29.05, 33.3, 38.35, 41.55, 45.75, 50.0, 54.0, 58.5`

| # | scene_id | 구간 | 주동작 | 카메라·지연 보조동작 | 결정론적 화면·claim_id | arrange lane |
|---:|---|---:|---|---|---|---|
| 1 | `divergence` | 0.00–4.00 | QQQ 선은 상승하고 MCD 선은 하락 | 9% push-in; 마지막 0.8초에 QQQ/MCD 수치 카드가 좌우로 settle | 두 선과 `QQQ +18.1%`, `MCD -20.3%`; `c01_divergence` | `chart_main`과 `metric_left/right`를 분리. 제목·출처·자막 lane 침범 금지 |
| 2 | `conditional_candidate` | 4.00–7.45 | 매장 건물이 부지 위로 조립 | 낮은 orbit; 1차·2차·확인 배지가 순차적으로 내려옴 | `몰빵 아닌 조건부 분할매수 후보`; `c02_candidate` | `store_hero` 중앙, `stage_badges` 하단. 배지가 건물과 겹치지 않음 |
| 3 | `global_franchise` | 7.45–10.95 | 하나의 매장이 세계지도 노드로 복제 | 좌우 track; 노드·연결선이 순차 등장하고 마지막 노드에서 focus | 지도·노드, `46,028`, `약 95% FRANCHISED`; `c03_global` | `map_main`, `count_left`, `franchise_card_right`를 독립 rect로 고정 |
| 4 | `real_estate_engine` | 10.95–15.15 | `LAND → BUILDING → EQUIPMENT` 폭발도 전개 | 12도 orbit; 각 층 그림자가 늦게 settle, 오른쪽 임대료·로열티 카드 진입 | `RENT $5.26B`, `ROYALTY $3.10B`; `c04_property` | `property_stack_left`, `cash_cards_right`; 땅·건물·장비 같은 좌표 중첩 금지 |
| 5 | `cash_to_owners` | 15.15–19.75 | FCF가 배당과 순현금 자사주매입으로 분기 | 짧은 top-down; 배당 봉투/막대가 먼저, share grid가 늦게 감소 | `배당 52억달러`, `순현금 자사주매입 21억달러`; `c05_return` | `fcf_hub`, `dividend_card_left`, `buyback_card_right` 세 칸 분리 |
| 6 | `shareholder_return` | 19.75–23.95 | 현금환원 링과 연속 인상 연수 카운트업 | 수직 tilt; 링이 채워진 뒤 50년 카드와 요약 카드 등장 | `3.92%`, `50 YEARS`; `c06_return_rate` | `yield_ring_left`, `years_right`, `summary_bottom`; 자막 lane은 비움 |
| 7 | `yield_signal` | 23.95–29.05 | 배당÷가격 계산과 월말 순위 막대가 채워짐 | macro push; 좌측 TTM 카드 후 우측 rank bar, 끝에 `2/80` hold | `TTM $7.35`, `$263.54`, `2.79%`, `2/80`; `c07_yield` | `yield_card_left`, `rank_card_right`; `2/80`은 카드 안에만 배치 |
| 8 | `history_check` | 29.05–33.30 | 역사적 배당률 **schematic** 선이 2015 기준점과 현재를 연결 | 좌→우 track; 2015 `3.58%` callout 후 현재 `2.79%` marker | `2015 3.58%`, `현재 2.79%`, `2010년 이후 상위 약 38%`; `c08_history` | `history_chart` 하나, `peak_callout`와 `current_callout` 서로 반대 구역. 중간 선은 원자료 시계열로 오인 금지 |
| 9 | `different_rhythm` | 33.30–38.35 | 동일 충격에 세 beta rail이 서로 다른 폭으로 반응 | lateral track; MCD rail 먼저, SPY·QQQ rail과 수치 pill이 지연 등장 | `MCD 0.42 · SPY 1.00 · QQQ 1.25`; `c09_beta` | 세 rail의 y-band 고정. 라벨·beta pill이 선 위로 겹치지 않음 |
| 10 | `lower_co_movement` | 38.35–41.55 | MCD와 QQQ 선이 잠시 함께 움직인 뒤 갈라짐 | baseline lock; split이 끝난 뒤 상관 카드가 pop-in | `상관계수 0.28`, `역상관은 아님`; `c10_correlation` | `correlation_plot` 상단, `corr_card` 하단. 자막은 별도 |
| 11 | `debt_guest_risk` | 41.55–45.75 | 부채 블록은 쌓이고 미국 객수 차량은 감소 | 10% pull-back; 차량이 하나씩 사라진 뒤 위험 카드가 늦게 표시 | `$40.6B`, `US GUEST COUNTS`, `낮은 beta ≠ 낮은 기업 위험`; `c11_risk` | `debt_stack_left`, `guest_queue_right`, `risk_card_bottom` 분리 |
| 12 | `entry_260s` | 45.75–50.00 | 매장 모델이 260달러대 가격 바닥으로 내려옴 | top-down settle; 수평 가격선 뒤 `1차` 카드가 나타남 | `1차 260달러대`, `작게`; `c12_entry_one` | `price_shaft`, `store_on_rail`, `entry_card`; 개인 주문 UI처럼 만들지 않음 |
| 13 | `entry_245_250` | 50.00–54.00 | 245~250달러 밴드와 3% 근접 yield bar가 채워짐 | band가 좌→우 fill; yield marker가 `≈ 3.0%`에서 멈춤 | `$245 — $250`, `2.79% → ≈3.0%`; `c13_entry_two` | `price_band_top`, `yield_rail_bottom`; 숫자는 밴드 안에서만 표시 |
| 14 | `guest_recovery_cancel` | 54.00–58.50 | 금색 아치가 먼저 복원되고 회복·취소 두 gate가 분리 | 첫 1.2초 arch reveal; 회복 카드 후 취소 카드 등장, 끝 1초에 opening line loop | `객수 회복 확인 → 비중 확대`와 `객수·FCF·배당 커버리지 훼손 → 투자 아이디어 취소`; `c14_close` | `arch_hero`, `confirm_card`, `cancel_card`; 취소선·밑줄·플랫폼 UI와 혼동되는 장식 금지 |

## 공통 화면 배치

내부 renderer 좌표(720×1280)를 1.5배 확대해 최종 1080×1920을 만든다.

- `header`: `(0,0)-(720,74)` — `MCD · INVESTMENT CASE`, 기준일.
- `title`: `(46,100)-(680,230)` — eyebrow와 최대 2줄 제목.
- `content`: `(54,272)-(666,944)` — 표의 primary visual과 data card만 둔다.
- `source`: `(48,948)-(672,990)` — 장면별 한 줄 출처.
- `caption`: `(38,1002)-(682,1182)` — 검토된 SRT만 둔다.
- `bottom_dead_zone`: `(0,1183)-(720,1280)` — Shorts UI가 덮을 수 있어 핵심 정보 금지.

각 장면의 lane은 `title → content → source → caption` 순으로 독립한다.
`map`, `building`, `equipment`, `data_card`, `source`, `caption`의 실제 bbox가
겹치면 render를 통과시키지 않는다. 생성형 plate를 삽입할 경우에도 같은
`content` rect 안에서만 무문자·무숫자 장면으로 사용한다.

## Motion grammar

- 첫 장면은 0~2초 안에 선 그래프 상태가 바뀐다.
- 모든 장면은 `primary action 1개 + camera 1개 + delayed secondary 1개`만
  허용한다. easing은 과장하지 않고, 상태가 바뀌는 순간에만 강조색을 쓴다.
- 그래프의 선·지도 노드·배당 막대·share grid·차량은 frame clock으로
  계산한다. wall-clock timer나 랜덤 위치를 쓰지 않는다.
- 마지막은 녹색 확인 카드와 빨간 취소 카드를 나란히 두며, 취소선을 화면
  전체에 긋거나 하단 자막을 가리는 효과를 쓰지 않는다.
- 금융 숫자·한글·축·범례·M 아치 geometry는 결정론적 레이어다. AI 모델에는
  건물·매장·도로·지도 질감 같은 텍스트 없는 plate만 맡긴다.

## Scene-to-subtitle contract

`subtitle.v8.srt`의 cue 1~14가 scene 1~14에 대응한다. 자막은 모든 cue가
최대 2줄이며, cue 14만 세 개의 짧은 줄을 허용한다. 시작·끝은 장면 안쪽에
0.1초 여유를 두되, 다음 cue와 겹치지 않는다. 자막 캡슐 아래에는 출처나
데이터 카드를 배치하지 않는다.
