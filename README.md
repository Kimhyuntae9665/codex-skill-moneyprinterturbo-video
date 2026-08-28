# MoneyPrinterTurbo Video Codex Skill

[MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo)를 이용해 세로형 숏폼 영상을 실제 MP4로 만들고 검증하는 개인용 Codex Skill입니다. 단순 설치 안내가 아니라 대본, 영상 소재, 한국어 음성, 자막, 최종 파일과 검증 결과까지 완성하는 흐름을 제공합니다.

## 설계 원칙

- 검토한 upstream 커밋 `eb8c23757e098a07bbcd93b3b50e252fc8d1869a`만 별도 런타임에 체크아웃합니다.
- 준비된 대본과 권리 문제가 없는 로컬 소재를 쓰면 LLM 및 스톡 영상 API 키 없이 실행합니다.
- 자동 소셜 업로드를 강제로 끄며, 유료 영상 공급자는 사용자가 비용을 명시적으로 승인해야 합니다.
- 최종 MP4는 해상도, 길이, 코덱, 전체 디코딩, 음성 볼륨, 대표 프레임까지 검사합니다.
- upstream 전체를 복제하지 않는 얇은 래퍼입니다. MoneyPrinterTurbo 자체 라이선스와 업데이트는 upstream을 따릅니다.

## 설치

Codex에서 다음처럼 요청합니다.

```text
$skill-installer https://github.com/Kimhyuntae9665/codex-skill-moneyprinterturbo-video/tree/main/moneyprinterturbo-video 를 설치해줘
```

설치 후 새 Codex 세션을 열고 다음처럼 사용합니다.

```text
$moneyprinterturbo-video 준비한 한국어 대본과 이미지로 55초짜리 YouTube Shorts 영상을 만들어줘.
```

필수 로컬 도구는 Git, uv, FFmpeg입니다. 첫 실행에는 upstream 체크아웃과 Python 의존성 설치, Edge TTS 접속을 위한 네트워크가 필요합니다.

## MCD 전문 모션그래픽 예제

`moneyprinterturbo-video/examples/mcd-valuation-2026/`에는 현재 MCD 밸류에이션과 가맹 수익 구조를 함께 설명하는 59초대 한국어 Shorts 제작 패키지가 있습니다.

- 비조정 종가끼리 계산한 고점 대비 하락률과 5년·20년 P/E 비교
- SEC/IR 공시에 맞춘 매장 수, 가맹 매출, 임대료, 로열티, 배당, 부채 근거
- 재사용 권리를 기록한 실제 매장 외관 사진과 원자료 기반 차트
- 오픈소스 Manim Community 0.21.0으로 렌더링하는 1080×1920/30fps master 영상
- SunHi 한국어 TTS 1.17배속 측정값에 맞춘 장면 타이밍과 MoneyPrinterTurbo 단일-master 합성

전문 모션그래픽 렌더 예시:

```powershell
.\moneyprinterturbo-video\examples\mcd-valuation-2026\motion\render.ps1
```

이 예제의 결론은 `최근 5년 P/E 범위에서는 매우 낮지만 20년 전체의 극단적 바닥은 아니다`입니다. 가맹 매출은 이익이나 FCF로 표시하지 않으며, 배당 기록도 미래 지급 보장으로 표현하지 않습니다.

## 이전 MCD 정적 예제

`moneyprinterturbo-video/examples/mcd-2025/`에는 맥도날드의 가맹·부동산 연계 수익 구조를 설명하는 한국어 Shorts 예제가 있습니다.

- `narration.ko.txt`: 2025 Form 10-K에 맞춘 한국어 내레이션
- `brief.md`, `storyboard.md`, `sources.md`: 표현 범위, 장면 구성, 1차 출처
- `make_materials.py`: 로고와 상업 사진 없이 1080x1920 인포그래픽 8장을 재현
- `verification.md`: 실제 생성 결과와 기술·시각 검증 기록

화면 생성 예시:

```powershell
uv run --project . python .\moneyprinterturbo-video\examples\mcd-2025\make_materials.py
```

생성된 소재, MP4, 런타임 설정과 로그는 의도적으로 Git에 포함하지 않습니다. 예제는 교육용 설명이며 투자 조언이 아닙니다.

## 검증

```powershell
uv run --project . python -m unittest discover -s tests -v
python C:\Users\<USER>\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\moneyprinterturbo-video
```

## 라이선스

이 저장소의 자체 작성 코드는 [MIT License](LICENSE)입니다. 수정한 upstream helper와 Noto Sans KR 글꼴의 별도 조건은 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) 및 글꼴 폴더의 `OFL.txt`를 확인하세요.
