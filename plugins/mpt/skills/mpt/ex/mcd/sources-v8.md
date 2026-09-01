# MCD 조건부 분할매수 Shorts v8 출처·claim ledger

기준일: 2026-08-31 미국 종가 · 회사 공시 기준: 2026-06-30 · 통화: USD

이 문서는 `storyboard-v8.md`의 `claim_id`를 원자료·계산·해석으로 분리한다.
시장 가격·배당·beta는 기준일과 계산법을 함께 보존하며, 영상 게시 직전에
원자료의 최신 상태를 다시 확인한다. 출처 링크가 있다는 사실만으로 미래 수익,
개인 적합성, 영상 조회수를 보장하지 않는다.

## Claim ledger

| claim_id | 확정 화면 값 | 구분 | 계산·정의 | 1차/재현 출처 |
|---|---|---|---|---|
| `c01_divergence` | MCD 263.54달러; 6개월 -20.31%; SPY +12.35%; QQQ +18.15% | 계산 | Yahoo 조정종가를 같은 기간에 정렬한 단순수익률. 화면은 QQQ +18.1%, MCD -20.3%로 반올림 | `research/v6_metrics.json`, `research/recompute_v6.py`, [Yahoo chart input](https://query1.finance.yahoo.com/v8/finance/chart/MCD?period1=1199145600&period2=1787875200&interval=1d&events=div%2Csplits&includeAdjustedClose=true) |
| `c02_candidate` | 조건부 3단계 분할매수 후보 | 해석 | 몰빵이 아닌 260달러대, 245~250달러, 객수 회복 확인의 교육용 시나리오 | `research/v6_metrics.json`의 `recommendation_frame`; 개인 자문 아님 |
| `c03_global` | 46,028개 매장; 약 95% 가맹 | 공시 사실 | 회사가 쓴 “approximately 95%”와 정확한 count ratio 95.63%를 분리 | [McDonald's Q2 2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/63908/000006390826000073/mcd-20260630.htm) |
| `c04_property` | H1 임대료 52.64억달러; 로열티 30.96억달러 | 공시 사실·해석 | 전통적 가맹 구조에서 토지·건물 소유 또는 장기 임차와 임대료·로열티 흐름을 설명. 모든 점포의 동일한 소유 구조를 뜻하지 않음 | [Q2 2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/63908/000006390826000073/mcd-20260630.htm), [2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/63908/000006390826000035/mcd-20251231.htm) |
| `c05_return` | TTM 현금배당 52.25억달러; 순현금 자사주매입 20.86억달러 | 계산 | FY2025 + H1 2026 - H1 2025 현금흐름. 자사주매입에서 옵션 행사대금을 차감 | `research/v6_metrics.json`, `research/shareholder_return_inputs_v3.csv`, [Q2 2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/63908/000006390826000073/mcd-20260630.htm) |
| `c06_return_rate` | 약 3.92%; 배당 50년 연속 인상 | 계산·공시 사실 | `(5.225B + 2.086B) / 186.491855B = 3.920%`. 이는 근사 현금 주주환원률이며 배당수익률이나 FCF payout ratio가 아님. 50년 문구는 2025 10-K의 배당 이력에서 확인 | `research/v6_metrics.json`, [2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/63908/000006390826000035/mcd-20251231.htm) |
| `c07_yield` | TTM 배당 7.35달러; 2.789% ≈ 2.79%; 2020년 이후 월말 80개 중 2위 | 계산 | 최근 4개 현금배당 ÷ 각 월말 원시 종가; high-to-low rank. 2026-08-31 기준 | `research/v6_metrics.json`, `research/dividend_yield_history_v6.csv`, `research/recompute_v6.py` |
| `c08_history` | 2015년 월말 3.578% ≈ 3.58%; 2010년 이후 상위 약 38% | 계산 | 저장된 2010년 이후 200개 월말 표본에서의 위치. “역대 모든 시점의 최고”로 확대하지 않음 | `research/v6_metrics.json`, `research/dividend_yield_history_v6.csv` |
| `c09_beta` | 5년 주간 beta: MCD 0.42; SPY 1.00; QQQ 1.25 | 계산 | 2021-09-01~2026-08-31 조정주가 주간 단순수익률; SPY 대비 표본 공분산/분산 | `research/v6_metrics.json`, `research/recompute_v6.py` |
| `c10_correlation` | MCD–QQQ 상관 0.28 | 계산·해석 | 같은 주간 관측의 표본 상관. 낮은 동조성이지 역상관이나 미래 분산효과 보장이 아님 | `research/v6_metrics.json`, `research/recompute_v6.py` |
| `c11_risk` | 총부채 약 405.88억달러 ≈ 406억달러; 미국 comparable guest counts 감소 | 공시 사실·위험 해석 | 총부채는 2026-06-30 balance sheet. 10-Q가 언급한 객수 약세를 위험으로 표시 | [Q2 2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/63908/000006390826000073/mcd-20260630.htm) |
| `c12_entry_one` | 260달러대 1차 | 해석 | 현재 가격대에서 작게 시작한다는 교육용 staging scenario. 주문·적정가 지시 아님 | `research/v6_metrics.json`의 `recommendation_frame`, `brief-v6.md` |
| `c13_entry_two` | 245~250달러; 배당수익률 약 3% | 계산·해석 | TTM 7.35달러를 단순 적용하면 245달러 3.00%, 250달러 2.94%로 근접. 배당·가격은 변동 | `research/v6_metrics.json`, `research/recompute_v6.py` |
| `c14_close` | 미국 객수 회복 확인 뒤 확대; 객수·FCF·배당 커버리지 훼손 시 취소 | 해석·invalidation rule | 조건이 충족될 때만 다음 단계 검토. 확정 추천이 아니라 반대 조건을 함께 보여주는 결론 | `research/v6_metrics.json`의 `recommendation_frame`, [Q2 2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/63908/000006390826000073/mcd-20260630.htm) |

## 회사·시장 원자료

- [McDonald's Q2 2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/63908/000006390826000073/mcd-20260630.htm): 매장 수, 약 95% 가맹, 가맹 임대료·로열티, 미국 comparable guest counts, 총부채와 현금흐름.
- [McDonald's Q2 2026 results](https://corporate.mcdonalds.com/corpmcd/our-stories/article/Q2-2026-results.html): Q2 systemwide sales와 comparable-sales 맥락.
- [McDonald's 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/63908/000006390826000035/mcd-20251231.htm): 배당 이력, 2025년 자사주매입, 토지·건물 소유와 부채 맥락.
- [Q3 2026 dividend release](https://corporate.mcdonalds.com/content/dam/sites/corp/nfl/pdf/Q326%20Dividend%20Release.pdf): 분기 현금배당 1.86달러. v6 TTM 계산에는 실제 현금 이벤트와 저장 입력을 사용한다.
- [Q4 2025 dividend release](https://corporate.mcdonalds.com/content/dam/sites/corp/nfl/pdf/Q4_25_Dividend_Release.pdf): 49회 연속 연간 인상과 당시 연환산 배당을 교차 확인.
- [Yahoo Finance chart input](https://query1.finance.yahoo.com/v8/finance/chart/MCD?period1=1199145600&period2=1787875200&interval=1d&events=div%2Csplits&includeAdjustedClose=true): MCD·SPY·QQQ 조정종가와 배당 이벤트 입력. 보조 시장 원자료이며 SEC 공시 사실로 취급하지 않는다.
- [ChartExchange MCD history](https://chartexchange.com/symbol/nyse-mcd/historical/) 및 [Investing historical data](https://ca.investing.com/equities/mcdonalds-historical-data): raw close 교차 확인.

## 계산·재현 파일

- `research/recompute_v6.py`: 저장된 가격·배당·SEC 현금흐름 입력에서 v6 metrics와 월말 yield history를 재계산한다.
- `research/v6_metrics.json`: 영상에 잠근 값과 정의를 보존한다.
- `research/calculations.csv`: drawdown, dividend yield, FCF, rent/royalty share, shareholder return의 계산식과 반올림을 기록한다.
- `research/dividend_yield_history_v6.csv`: 2010년 이후 월말 TTM yield 200개 관측치.
- `research/facts.json`: 회사 사실·계산·추론과 출처 정책을 분리한 원장.

## 제작·조사 참고자료

- [MoneyPrinterTurbo pinned upstream](https://github.com/harry0703/MoneyPrinterTurbo/tree/eb8c23757e098a07bbcd93b3b50e252fc8d1869a): prepared-local 조립 경로. 영상·음성·SRT·MCD 상표 권리는 별도다.
- `research/tool-report.md`: Hugging Face·Reddit·GitHub 도구 조사 통합본. 생성 모델은 2~4초 무문자 plate에만 사용하고 수치·자막·로고를 후합성하라는 제작 원칙을 참고한다. 선택적 외부 GPU 후보는 패키지에서 실행하지 않는다.

## 표시·권리·게시 경계

- 회사 공시 사실, 시장 계산, 편집자의 조건부 해석을 자막·대본에서 섞지 않는다.
- “약 95% 가맹”은 가맹 비율이지 토지 소유율이 아니다. 10-K의 토지·건물 보유 문구도 모든 점포에 일반화하지 않는다.
- beta·상관·배당률·환원률은 과거 관측·근사 계산이다. 기준일·기간·분모를 바꾸면 값이 바뀐다.
- MCD와 황금 아치 geometry는 설명용으로만 합성한다. 외부 로고·사진·음성·지도 타일·모델 생성물의 사용권은 별도로 확인한다.
- MPT, Pillow, FFmpeg와 HF/GitHub Skill 라이선스가 회사 상표나 금융 데이터 재배포권을 부여하지 않는다.
- YouTube·Instagram·X 자동 게시를 하지 않는다. 최종 게시 전 사람이 수치·자막·권리·플랫폼 safe-zone을 확인한다.

## 게시 전 재검증 체크리스트

1. 시장 가격·배당·yield rank·beta·상관을 2026-08-31 기준 원자료와 다시 대조한다.
2. 10-Q/10-K의 기간과 단위를 확인하고, 52억·21억·406억달러의 반올림을 원장과 맞춘다.
3. `claim_id → storyboard scene → subtitle cue → rendered bbox`가 1:1로 연결되는지 확인한다.
4. 모델/Space plate를 새로 쓸 경우 revision, license, quota, 입력 보관, 비용, seed를 기록한다.
5. 금융 수치·한국어·차트·M 아치는 생성 모델 출력이 아니라 결정론적 레이어에서만 만든다.
