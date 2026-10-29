# MoneyPrinterTurbo Video v1.2.2 — 한국어 숏폼 제작 스킬

**근거 조사부터 9:16 영상 제작, 자막·음성 동기화, 최종 영상 검수까지 이어지는 Codex 스킬 묶음입니다.**

이 저장소의 `main`에는 현재 사용 중인 `moneyprinterturbo-video` 스킬 원문과 실행·검수 도구를 담았습니다. 회사·제품 설명, 뉴스, 미국 주식 분석 등 서로 다른 목적을 구분하며, 결과물을 실제로 재생·검토했는지 별도로 기록합니다. **이 스킬이 조회수·투자 수익·저작권 허가·영상 품질을 보장하지는 않습니다.**

> [현재 SKILL.md 전체 보기](https://github.com/Kimhyuntae9665/codex-skill-moneyprinterturbo-video/blob/main/plugins/mpt/skills/mpt/SKILL.md) · [스킬 폴더](https://github.com/Kimhyuntae9665/codex-skill-moneyprinterturbo-video/tree/main/plugins/mpt/skills/mpt) · [설치 안내](docs/INSTALL.md) · [라이선스 및 외부 자료 고지](THIRD_PARTY_NOTICES.md)
>
> 2026-10-30 기준 **v1.2.2는 main 개발 스냅샷이며 별도 태그 릴리스는 아닙니다.** 저장소 `main`의 스킬 본문은 설치된 원본과 바이트까지 동일합니다. 기존 `v1.2.1` 태그는 이전 스냅샷이므로 최신 내용을 설치하려면 아래의 `main` 방법을 사용하세요.

## 어떤 일을 하나요?

| 단계 | 수행 내용 | 확인할 결과 |
| --- | --- | --- |
| 1. 목적과 범위 | 시청자, 전달할 질문, 제작 목적, 길이 선택 | 제작 경로와 `production.json` |
| 2. 근거 조사 | 회사 공식 자료·공시·출처와 반대 근거 확인 | 주장별 출처·날짜·계산 기록 |
| 3. 대본·자료 | 핵심 질문, 한국어 내레이션, 실제 시연 자료 선정 | 검토 가능한 대본과 자료 사용 근거 |
| 4. 화면·음성 | 화면 구성, 음성, 자막, 필요한 차트·로고 연결 | 음성 길이와 맞춘 화면·자막 |
| 5. 제작·검수 | MoneyPrinterTurbo로 조립하고 최종 MP4 검사 | MP4, 썸네일, 검사 및 검토 기록 |

**사람이 직접 최종 영상을 보고 들은 검수와 자동 검사 결과는 별개입니다.** 시청이나 청취를 하지 못한 결과물은 최종 완성으로 표시하지 않고 검토용 초안으로 남깁니다.

## 제작 전에 선택하는 것

### 콘텐츠 목적 `editorial_route`

- `news-explainer`: 뉴스·사건과 그 근거를 설명합니다.
- `investment-analysis`: 투자 판단 질문을 다룹니다. 상장회사 투자 분석에는 기준일이 있는 가격, 재현 가능한 밸류에이션, 위험 및 추천·관망·비추천 판단이 필요합니다.
- `general-explainer`: 사업, 제품 또는 기술의 작동 원리를 설명합니다.

종목 코드가 나온다는 이유만으로 뉴스나 사업 설명에 투자 의견을 강제로 넣지 않습니다. 실제로 투자 주장을 할 때는 그 주장에 맞는 근거를 확인합니다.

### 자료 준비 방식 `source_mode`

- `prepared-local`: 검토된 대본과 사용 권한을 확인한 로컬 영상·이미지를 사용합니다.
- `topic-online`: 주제에서 대본 또는 온라인 자료를 찾습니다. 선택한 제공자가 필요한 경우에만 `MPT_NEEDS_INPUT`에 표시되는 자격 증명을 준비합니다.
- `evidence-motion`: `prepared-local`의 엄격한 하위 방식입니다. 주장과 수치·도표·장면 위치를 고정하고 연속 영상으로 조립합니다. 금융 수치나 정밀한 화면 구성이 필요한 경우에 사용합니다.

`focused`는 25~35초, `full`은 45~60초, `custom`은 명시한 범위입니다. 실제 음성 길이와 요청에 맞춰 선택하며, 검사를 통과시키기 위해 임의로 구간을 늘리지 않습니다.

## 이 스킬이 중요하게 보는 기준

- **공식 출처 영상 60% 이상**: 최종 MP4의 전체 시간 중 사용 조건이 확인된 관련 공식 영상이 차지하는 비율을 계산합니다. 반복 이미지, 편집으로 늘린 정지 화면, 숨겨진 삽입 화면은 공식 영상으로 계산하지 않습니다. 공식 게시 자체가 재사용 허락을 뜻하지 않습니다.
- **사업·뉴스 맥락 30% 이상**: 회사·주식·AI·기술 영상은 실제 내레이션 시간의 30% 이상을 관련 뉴스, 도입, 경쟁, 고객 행동 또는 사업상의 의미를 설명하는 데 사용합니다. 숫자는 실제 발화 구간을 기준으로 계산합니다.
- **읽을 수 있는 실제 근거**: 제품의 실제 화면·시연 동작과 나레이션을 맞추고, 차트는 수치와 단위를 보존합니다. 영상에서 쓰는 로고·사진·영상의 권리와 출처는 각각 따로 확인합니다.
- **한국어 음성·자막**: 기본 선호는 무게감 있는 한국어 남성 내레이션입니다. 기준 음성에 1.30배를 한 번 적용한 후 실제 발화와 침묵을 확인하고, 이후 자막·장면 전환을 맞춥니다. 사용자의 다른 음성 지시는 우선합니다.
- **썸네일**: 기본 세로 영상에는 별도의 1080×1920 썸네일을 만듭니다. 영상 안에 커버를 넣는 것은 선택 사항이며 무음 정지 화면을 강제하지 않습니다.
- **최종 파일 기준 검수**: 인코딩, 음성, 자막, 장면 경계, 자료 비율을 최종 MP4 기준으로 다시 확인합니다. 자동 PASS만으로 실제 청취·화면 검토·자료 사용 권한을 증명할 수 없습니다.

## 다른 컴퓨터에 설치하기

Git과 Python 3.11 이상이 필요합니다. Windows에서 경로 길이 문제가 있다면 `C:\work`처럼 짧은 경로에서 진행하세요. Python이 `python3`으로 실행되는 환경에서는 아래 명령의 `python`을 `python3`으로 바꾸세요.

```bash
git clone https://github.com/Kimhyuntae9665/codex-skill-moneyprinterturbo-video.git mpt-video
cd mpt-video
python scripts/install_bundle.py --profile core --dry-run
python scripts/install_bundle.py --profile core
```

설치기는 파일 해시를 확인한 뒤 기본적으로 `$CODEX_HOME/skills` 또는 `~/.codex/skills`에 설치합니다. `core`는 아래 3개를 함께 설치합니다.

1. `moneyprinterturbo-video`: 영상 제작과 검수 본체
2. `us-stock-research`: 미국 주식·공시 조사에 사용하는 동반 스킬
3. `logo-flow-infographics`: 로고·관계도 시각화에 사용하는 동반 스킬

설치 계획만 살펴보려면 `--dry-run`을 사용하세요. 기존 스킬 폴더가 있으면 기본적으로 덮어쓰지 않습니다. 백업 후 교체할 때만 `--overwrite`를 추가합니다. 설치 경로를 직접 정하려면 `--target <스킬-폴더-경로>`를 사용합니다. 설치 후 **새 Codex 대화**를 열어 스킬을 다시 검색하세요.

```bash
# 전체 동봉 스킬 53개 설치 계획 확인
python scripts/install_bundle.py --profile all --dry-run

# 전체 동봉 스킬 설치
python scripts/install_bundle.py --profile all

# 선택 사항: 고정된 공식 Remotion 스킬 12개도 네트워크로 가져오기
python scripts/install_bundle.py --profile all --with-external
```

Codex 버전에서 플러그인 marketplace를 지원한다면 다음 방법도 사용할 수 있습니다. 플러그인과 standalone 설치를 중복하면 같은 스킬이 두 번 표시될 수 있으므로 한 방식을 고르세요.

```text
codex plugin marketplace add Kimhyuntae9665/codex-skill-moneyprinterturbo-video --ref main
codex plugin add mpt-video@mpt-video
```

### 영상 실행 전 별도 준비물

| 도구 | 필요한 이유 | 확인 방법 |
| --- | --- | --- |
| Git | 고정된 MoneyPrinterTurbo 소스 가져오기 | `git --version` |
| Python 3.11+ | 설치기·검수 도구 실행 | `python --version` |
| uv | 격리된 Python 실행 환경 구성 | `uv --version` |
| FFmpeg / FFprobe | 영상 조립·영상 및 오디오 검사 | `ffmpeg -version`, `ffprobe -version` |
| 네트워크 | 최초 의존성 설치, 온라인 자료, 선택한 TTS | 사용 환경에서 직접 확인 |

Python, FFmpeg, uv, GPU 드라이버, 모델 가중치, API 키, 계정은 이 저장소가 대신 설치하거나 제공하지 않습니다. Blender·Manim·Remotion 등은 사용하는 제작 방식에 따라서만 필요합니다. 제공자별 요금과 사용 조건은 실제 사용 전에 확인하세요.

저장소를 받은 직후 실행 환경을 점검할 수 있습니다.

```bash
python plugins/mpt/skills/mpt/scripts/check_environment.py --json
python plugins/mpt/skills/mpt/scripts/check_environment.py --mode us-equity --json
```

설치된 스킬을 점검할 때는 설치 대상의 `moneyprinterturbo-video/scripts/check_environment.py`를 사용합니다. 명령어 누락, 동반 스킬 미발견 등은 점검 결과에 표시됩니다. 이 점검은 실제 영상 생성이나 영상 검수를 대신하지 않습니다.

## 사용 예시

새 Codex 대화에서 다음처럼 요청할 수 있습니다.

```text
$moneyprinterturbo-video
공식 제품 시연 영상을 중심으로 한국어 9:16 숏폼을 만들어줘.
주장마다 출처를 확인하고, 실제 시연 동작과 설명을 맞춰줘.
최종 MP4와 썸네일, 자료 사용 근거, 실제 영상·음성 검수 결과도 알려줘.
```

```text
$moneyprinterturbo-video
제공한 대본과 사용 권한을 확인한 로컬 영상으로 30초 숏폼을 만들어줘.
```

미국 주식의 투자 판단을 요청한다면 기준일, 공시·IR 근거, 밸류에이션, 위험과 판단을 확인하도록 요청하세요. 영상 제작에 필요한 자료나 외부 제공자 자격 증명이 없다면 해당 부분은 준비가 필요합니다. 사용자 승인 없이 유료 API를 사용하거나 영상을 게시하지 않습니다.

## 결과물과 검수 방법

기본 결과물은 **세로 MP4와 별도 썸네일**입니다. 제작 방식에 따라 주장 원장, 장면 원장, 사용 자료 기록, 오디오·영상 검사 보고서가 함께 만들어집니다. 아래 검수 도구는 스킬의 `scripts` 폴더에 있습니다.

| 파일 | 역할 |
| --- | --- |
| `mpt_agent.py` | 고정된 MoneyPrinterTurbo 실행 및 최종 영상 경로 확인 |
| `check_environment.py` | 도구·필수 파일·동반 스킬 확인 |
| `validate_scene_manifest.py` | 장면 배치와 장면 원장 검사 |
| `validate_video.py` | 최종 영상 형식·길이·디코딩·프레임·일부 음성 상태 검사 |
| `probe_scene_frames.py` | 장면 경계 및 중간 프레임 추출 |
| `audit_audio_silence.py` | 내레이션의 침묵 구간 점검 |
| `burn_subtitles.py` | 검토된 자막을 영상에 적용 |
| `validate_delivery.py` | 최종 파일 해시, 자료 비율, 필수 검수 기록 검사 |

스크립트 옵션과 제작 순서는 [SKILL.md](plugins/mpt/skills/mpt/SKILL.md)와 [상세 검수 안내](plugins/mpt/skills/mpt/references/verification-guide.md)를 기준으로 하세요. `MPT_RESULT`는 비어 있지 않은 MP4가 있다는 신호이며, 사실·권리·화면·청취 검수가 모두 끝났다는 뜻은 아닙니다.

## 자주 묻는 질문

**Q. 이 저장소를 복제하면 MoneyPrinterTurbo 자체가 모두 설치되나요?**

아니요. 스킬과 보조 도구가 포함되어 있으며, 실행 도구와 고정된 MoneyPrinterTurbo 소스는 해당 제작 과정에서 별도로 준비합니다. 본체의 고정 커밋은 `eb8c23757e098a07bbcd93b3b50e252fc8d1869a`입니다.

**Q. API 키가 반드시 필요한가요?**

제작 모드와 사용하는 제공자에 따라 다릅니다. `prepared-local`은 준비된 로컬 자료를 사용합니다. 온라인 대본·자료·음성 기능은 선택한 서비스의 계정이나 키가 필요할 수 있습니다. 키는 GitHub 저장소에 올리지 마세요.

**Q. 공식 영상을 찾기만 하면 60% 기준이 충족되나요?**

아니요. 사용 가능 여부를 따로 확인하고, 최종 영상에서 실제로 사용된 적격 구간의 중복 없는 길이를 계산해야 합니다. 확보하지 못했다면 부족한 상태를 기록합니다.

**Q. 점검에 통과하면 바로 게시하나요?**

아니요. 게시와 유료 사용은 별도의 명시적 요청이 필요합니다. 자동 검사는 실제 전체 영상의 시청·청취와 저작권 검토를 대신하지 않습니다.

**Q. 다른 컴퓨터에서 반드시 똑같이 렌더링되나요?**

그렇게 보장할 수 없습니다. 운영체제, 코덱, 실행 도구, 선택한 음성·모델·외부 서비스에 따라 달라집니다. 먼저 환경 점검을 실행하고 해당 컴퓨터에서 실제 제작 및 최종 검수를 수행하세요.

## 저장소 구조

```text
plugins/mpt/skills/mpt/
├── SKILL.md                 현재 스킬 원문
├── agents/                  스킬 표시 설정
├── scripts/                 실행 및 검수 도구
├── references/              제작·자료·검수 상세 지침
├── assets/                  폰트와 템플릿
├── tests/                   스킬 계약 테스트
└── ex/                      역사적 예시 자료
plugins/mpt/skills/          동봉된 관련 스킬
scripts/install_bundle.py    설치기
scripts/audit_bundle.py      배포 무결성 검사
distribution/                파일 해시와 출처 기록
```

MCD 관련 예제는 **역사적 사례**이며 최신 주가나 현재 투자 판단의 근거로 재사용하면 안 됩니다. 전체 구성과 외부 엔진에 대한 자세한 설명은 [스킬 목록](docs/SKILLS.md), [외부 의존성](docs/EXTERNAL_DEPENDENCIES.md), [출처 원장](distribution/source-inventory.json), [변경 기록](CHANGELOG.md)을 참고하세요.

## English quick start

This repository contains a Korean short-video production skill and its supporting workflows. Clone the default branch, run `python scripts/install_bundle.py --profile core --dry-run`, then run it without `--dry-run`. Start a new Codex conversation and invoke `$moneyprinterturbo-video`. Install Git, Python 3.11+, uv, FFmpeg and FFprobe separately. The skill distinguishes illustrative checks from actual viewing, listening, rights clearance, and completed publication.

The original project is MIT-licensed. Third-party skills, the Noto Sans KR font, photographs, and other assets retain their own license and attribution terms; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
