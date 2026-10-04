# Codex Skill: 미국 주식 리서치 (`us-stock-research`)

이 저장소는 **Codex Skills**용 미국 주식 리서치 스킬입니다.  
미국 개별주, S&P 500 스크리닝, 밸류에이션, 배당 분석, SEC/EDGAR/XBRL 기반 재무제표 분석, 과거 주가 분석을 할 때 Codex가 일관된 절차와 데이터 출처 기준을 따르도록 만든 패키지입니다.

투자 판단을 대신하는 도구가 아니라, 공개 데이터 기반 리서치와 계산을 보조하는 Codex 스킬입니다.

## 이 스킬이 하는 일

- 미국 주식 티커 분석 및 기업 식별
- SEC EDGAR / XBRL 재무 데이터 우선 사용
- Yahoo, Stooq 등 비공식 가격 데이터 사용 시 출처 구분
- P/E, P/B, ROE, ROIC, ROA, EV/EBITDA, 배당수익률, payout ratio 등 핵심 지표 정리
- S&P 500 또는 사용자 지정 티커 목록 스크리닝
- 뉴스, 공시, 매크로 컨텍스트를 구분해서 리서치 답변 작성
- 한국어로 미국 주식 리서치 결과를 구조화해서 출력

## Codex Skill 구성

- `SKILL.md`: Codex가 이 스킬을 언제 어떻게 사용할지 정의한 핵심 지침
- `agents/openai.yaml`: Codex UI 표시용 메타데이터
- `scripts/us_stock_research.py`: API 키 없이 실행 가능한 1차 데이터 수집/스크리닝 스크립트
- `references/data-sources.md`: 데이터 소스 우선순위와 주의사항
- `references/metrics-and-scoring.md`: 지표 계산식과 스코어링 기준
- `references/report-templates.md`: 리서치 보고서 출력 템플릿
- `references/prompts.md`: 한국어 프롬프트 예시

## 빠른 실행

미국 스킬의 기본 스크립트는 Python 표준 라이브러리만 사용합니다.

```powershell
python .\scripts\us_stock_research.py install-check
python .\scripts\us_stock_research.py snapshot --tickers AAPL MSFT NVDA --years 5 --out "$env:TEMP\us-stock-snapshot"
python .\scripts\us_stock_research.py history --ticker AAPL --start 2010-01-01 --out "$env:TEMP\aapl-history.csv"
python .\scripts\us_stock_research.py screen --universe sp500 --limit 50 --years 5 --out "$env:TEMP\sp500-screen"
```

SEC EDGAR를 반복 호출할 때는 사용자 식별용 User-Agent를 설정하는 것이 좋습니다.

```powershell
$env:SEC_USER_AGENT="your-name your-email@example.com"
```

## 사용 예시

- `AAPL, MSFT, NVDA의 최근 5년 매출 성장률, ROE, 밸류에이션을 비교해줘`
- `S&P 500에서 배당수익률과 ROIC가 높은 종목을 스크리닝해줘`
- `미국 금융주 중 P/B와 ROE 기준으로 저평가된 종목을 찾아줘`
- `최근 실적 발표와 10-Q를 반영해서 테슬라 투자 포인트와 리스크를 정리해줘`

## 출력 원칙

- 출처 사실, 계산 지표, 추론을 분리합니다.
- 공식 데이터와 편의 데이터의 신뢰도를 구분합니다.
- 누락 데이터는 임의 보정하지 않고 `N/A`로 표시합니다.
- 단일 결론만 제시하지 않고 bull/base/bear 시나리오와 리스크를 함께 둡니다.

## 주의

이 스킬은 투자 자문이 아닙니다. 결과는 공개 데이터 기반 리서치 보조 자료이며, 실제 투자 판단은 사용자가 별도로 검토해야 합니다.

