# v3 출처와 계산 경계

최종 시장 기준은 2026-08-27 미국 종가다. SEC 값은 공식 공시, 주가·수정주가는
시장 데이터 벤더 값, 주주환원률·베타·상관계수는 저장 데이터에서 만든 계산값이다.

## 회사 공시

- [McDonald's 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/63908/000006390826000035/mcd-20251231.htm): FY2025 배당·자사주 매입·옵션 행사 현금흐름, 50년 연속 배당 인상, 2025년 회사 발표 총 주주환원.
- [McDonald's Q2 2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/63908/000006390826000073/mcd-20260630.htm): H1 2026·H1 2025 비교 현금흐름, 707,641,531주, 희석 가중평균 주식 수, 장기부채, 미국 객수 감소.
- [SEC 가맹 매출 표](https://www.sec.gov/Archives/edgar/data/63908/000006390826000073/R26.htm): H1 2026 임대료 5.264B달러, 로열티 3.096B달러, 초기 수수료 0.039B달러.

## 시장 데이터와 프록시

- [Yahoo Finance 수정주가 정의](https://help.yahoo.com/kb/SLN28256.html): 분할과 배당을 반영한 adjusted close 정의.
- Yahoo Finance chart endpoint: MCD·SPY·QQQ의 `1wk` adjusted close를 2021-08-27부터 2026-08-27까지 같은 요청으로 저장했다. 정확한 URL과 반환 기간은 `research/v3_metrics.json`에 기록했다.
- [State Street SPY](https://www.ssga.com/us/en/individual/etfs/state-street-spdr-sp-500-etf-trust-spy): SPY가 S&P 500의 가격·수익률 성과를 추종하는 ETF라는 근거.
- [Invesco QQQ](https://www.invesco.com/qqq-etf/en/home.html): QQQ가 Nasdaq-100 혁신·대형 성장주 노출을 제공한다는 근거. 순수 기술 섹터 지수로 간주하지 않는다.
- [ChartExchange MCD 가격](https://chartexchange.com/symbol/nyse-mcd/historical/): 2026-08-27 비조정 종가 260.06달러와 v2의 6개월 하락률.

## 저장 계산

재현 명령:

```powershell
python .\research\recompute_v3.py
python .\research\recompute_v3.py --offline
```

온라인 실행은 주간 수정주가 CSV를 갱신하고, 오프라인 실행은 저장 CSV에서 같은
결과를 다시 만든다.

| 계산값 | 결과 | 정의 |
|---|---:|---|
| TTM 배당 현금 | 5.225B달러 | FY2025 + H1 2026 - H1 2025 |
| TTM 순현금 자사주매입 | 2.086B달러 | 매입 현금유출 2.325B - 옵션 행사 현금유입 0.239B |
| TTM 현금 주주환원 | 7.311B달러 | 배당 + 순현금 자사주매입 |
| 시가총액 근사 | 184.029B달러 | 2026-06-30 주식 수 × 2026-08-27 비조정 종가 |
| 현금 주주환원률 | 3.9727% | 7.311 / 184.029 |
| MCD beta vs SPY | 0.4767 | 주간 MCD·SPY 수익률 공분산 / SPY 분산 |
| QQQ beta vs SPY | 1.2516 | 주간 QQQ·SPY 수익률 공분산 / SPY 분산 |
| MCD–QQQ 상관 | 0.3274 | 261개 정렬 주간 단순 수익률의 Pearson 상관 |

## 한계

- 현금 주주환원률은 회사가 공시한 공식 비율이 아니라 시점이 다른 주식 수와 종가를 결합한 단순 근사다.
- 옵션 행사 현금 유입을 차감했지만 RSU 등 비현금 주식보상 희석 전체를 포착하지 않는다. H1 희석 가중평균 주식 수는 전년 동기 대비 약 0.78% 감소했다.
- 베타와 상관은 5년 역사값이며 미래 움직임을 예측하지 않는다. 낮은 베타는 낮은 총변동성·손실 가능성을 보장하지 않는다.
- MCD와 QQQ의 상관 0.33은 `반대로 움직임`이 아니라 `같이 움직인 정도가 낮았음`을 뜻한다.
