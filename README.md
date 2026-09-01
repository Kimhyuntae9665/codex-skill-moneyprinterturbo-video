# MoneyPrinterTurbo Video v1.0.0

MoneyPrinterTurbo를 이용해 한국어 YouTube Shorts·Reels용 9:16 MP4를 만들고, 자막·오디오·프레임·데이터 근거까지 검증하는 Codex Plugin/Skill입니다.

이 저장소는 두 가지 설치 방식을 동시에 제공합니다.

- Plugin: ZIP 전체 또는 GitHub Marketplace로 설치
- Standalone Skill: `$skill-installer`로 Skill 폴더만 설치

## ZIP으로 설치

Release의 `MoneyPrinterTurbo-Video-Plugin-v1.0.0.zip`을 원하는 폴더에 압축 해제합니다. 압축을 푼 최상위 폴더를 Marketplace로 등록한 다음 Plugin을 설치합니다.

```powershell
codex plugin marketplace add "C:\path\to\MoneyPrinterTurbo-Video-Plugin-v1.0.0"
codex plugin add mpt-video@mpt-video
```

설치 후 새 Codex 작업을 열고 다음처럼 사용합니다.

```text
$moneyprinterturbo-video 준비한 한국어 대본과 이미지로 55초짜리 YouTube Shorts 영상을 만들어줘.
```

## GitHub에서 Plugin 설치

```powershell
codex plugin marketplace add Kimhyuntae9665/codex-skill-moneyprinterturbo-video --ref v1.0.0
codex plugin add mpt-video@mpt-video
```

## Standalone Skill 설치

Codex에서 다음처럼 요청합니다.

```text
$skill-installer Install the skill from https://github.com/Kimhyuntae9665/codex-skill-moneyprinterturbo-video/tree/v1.0.0/plugins/mpt-video/skills/moneyprinterturbo-video
```

## 실행 전 검사

필수 도구는 Git, Python 3.11+, uv, FFmpeg/FFprobe입니다. 최초 실행에는 pinned MoneyPrinterTurbo checkout, Python 의존성, Edge TTS를 위한 네트워크가 필요합니다.

```powershell
python .\plugins\mpt-video\skills\moneyprinterturbo-video\scripts\check_environment.py --json
```

미국주식 영상은 다음처럼 companion Skill까지 확인합니다.

```powershell
python .\plugins\mpt-video\skills\moneyprinterturbo-video\scripts\check_environment.py --mode us-equity --json
```

`us-stock-research`는 미국주식 근거 확정에 필요합니다. `infographic-creator`는 인포그래픽 장면에 사용합니다. Unusual Whales는 선택적 보조 확인 수단이며, 설치되지 않은 경우 `unavailable`로 기록하도록 설계했습니다.

## 포함 기능

- 준비된 로컬 영상·이미지와 대본을 사용하는 API-key-free 모드
- MoneyPrinterTurbo upstream commit `eb8c23757e098a07bbcd93b3b50e252fc8d1869a` 고정
- 한국어 Edge TTS와 검수된 SRT 복구 경로
- SEC·issuer IR 중심 claim ledger와 13F 표현 규칙
- AntV 인포그래픽 또는 deterministic chart 모션
- 큰 모바일 글자, 빈 공간·겹침·잘림·전환 잔상 검수
- MP4 해상도·코덱·오디오·전체 디코딩·장면 경계 검사
- MCD v8 골든 예제와 재현 가능한 계산·레이아웃 자료

## 검증

```powershell
uv sync --frozen
uv run --frozen python -m unittest discover -s tests -v
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .\plugins\mpt-video\skills\moneyprinterturbo-video
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" .\plugins\mpt-video
```

## 배포 제외 항목

가상환경, API 키, `.env`, 생성된 MP4, QA 프레임 묶음, 브라우저 캐시, 로컬 로그와 절대경로는 Release/ZIP에 포함하지 않습니다.

## 라이선스

자체 작성 코드는 MIT License입니다. MoneyPrinterTurbo, Noto Sans KR, 예제 사진과 수정 helper의 별도 조건은 `THIRD_PARTY_NOTICES.md`, Skill 내부 `THIRD_PARTY_NOTICES.md`, 폰트 `OFL.txt`, 예제 asset manifest를 확인하세요.
