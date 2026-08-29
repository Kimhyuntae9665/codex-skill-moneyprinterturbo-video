# v4 출처와 계산 경계

시장 데이터 기준은 2026-08-27 미국 종가다. 회사 공시는 사실, Yahoo 시장
데이터는 벤더 원자료, 배당수익률 순위는 저장 CSV에서 만든 계산값이다.

## 회사 공시

- [McDonald's 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/63908/000006390826000035/mcd-20251231.htm): 50년 연속 배당 인상, 2025년 연간 주당 배당 7.17달러, 분기 배당 1.86달러와 향후 배당의 이사회 결정 조건.
- [McDonald's Q1 2026 dividend release](https://corporate.mcdonalds.com/content/dam/sites/corp/nfl/pdf/2026%20Q1%20Dividend%20Release%20.pdf): 2026년 3월 지급 분기 배당 1.86달러.
- [McDonald's Q2 2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/63908/000006390826000073/mcd-20260630.htm): H1 2026 현금흐름, 장기부채, 미국 객수 감소와 가맹 관련 공시.

## 시장 데이터와 재현

- [Yahoo Finance chart endpoint](https://query1.finance.yahoo.com/v8/finance/chart/MCD?period1=1199145600&period2=1787875200&interval=1d&events=div%2Csplits&includeAdjustedClose=true): 2008-01-01부터 2026-08-27까지의 일별 raw close와 현금배당 이벤트를 한 요청으로 수집했다. 2008~2009 값은 2010년 초 최근 4회 배당 계산의 lookback이다.
- `research/dividend_yield_history_v4.csv`: 2010-01부터 2026-08까지 달력 월별 마지막 거래일 200개를 저장한다.
- `research/recompute_v4.py`: 온라인 갱신과 `--offline` 재계산, JSON·PNG 차트 생성을 담당한다.

재현 명령:

```powershell
python .\research\recompute_v4.py
python .\research\recompute_v4.py --offline
```

## 계산값

| 계산값 | 결과 | 정의 |
|---|---:|---|
| 2026-08-27 raw close | 260.06달러 | Yahoo 일별 비조정 종가 |
| 최근 4회 주당 현금배당 | 7.35달러 | 1.77 + 1.86 + 1.86 + 1.86 |
| TTM 배당수익률 | 2.8263% | 7.35 / 260.06 |
| 2010년 이후 중앙값 | 2.5070% | 월말 200개 중앙값 |
| 2010년 이후 순위 | 74 / 200 | 높은 값부터, 상위 37.0% |
| 2020년 이후 순위 | 2 / 80 | 2020-03-31의 2.9150%만 현재보다 높음 |
| 2023년 이후 순위 | 1 / 44 | 현재가 해당 구간 최고 |
| 2010년 이후 최고 | 3.5782% | 2015-08-31 |

## 해석 한계

- `최근 구간에서 매력적`은 2020년·2023년 이후 상대 순위를 뜻한다. 2010년
  이후 상위 37%이므로 장기 역사 전체의 극단값이나 확정 매수 신호는 아니다.
- 분모는 현금 배당수익률 관행에 맞춘 raw close다. 배당을 반영하는 adjusted close를 분모로 쓰지 않는다.
- TTM 배당수익률은 과거 4회 배당 기준이다. 현재 분기 배당 1.86달러를 4배한
  forward 값은 7.44달러, 같은 종가 기준 약 2.86%지만 역사 순위에는 섞지 않는다.
- 세금, 환율, 재투자, 총수익률, 향후 배당 삭감 가능성을 포함하지 않는다.
