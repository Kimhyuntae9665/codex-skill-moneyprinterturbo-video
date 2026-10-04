# MoneyPrinterTurbo Video v1.2.1

**근거를 확인하고 공식 시연 영상을 적극 활용하는 한국어 Shorts 제작 스킬 묶음입니다.**
조사 → 대본 → 자료 선정 → 움직이는 화면 → 한국어 음성·자막 → 검수까지 연결합니다.
영상 제작 요청에는 최종 MP4를 목표로 하며, 검수하지 않은 결과를 완성본으로
표시하지 않습니다.

## 포함한 것

- 최신 본체, 참고문서 20개, 실행·검수 Python 스크립트 8개.
- **공식 동영상 사용 시간 최소 60%**. 실제 시연 동작과 나레이션을 맞추고,
  화면을 크게 보여 주며 출처·시점을 기록합니다. 사진 확대·텍스트 모션은
  공식 동영상으로 계산하지 않습니다. 확보하지 못하면 기준 미달을 보고합니다.
- SEC·IR 근거와 주주환원·희석·역사적 밸류에이션 검증 지침.
- 실제 로고와 편집 가능한 JSON/SVG를 사용하는 `logo-flow-infographics`.
- 음성 침묵·자막·화면·장면 원장·완료 상태 검사, 폰트, 템플릿,
  재계산 가능한 MCD 예제 데이터와 렌더링 소스.
- 참조 관계를 따라 정리한 **65개 스킬**: **53개 전체 파일 동봉**, **12개 공식
  Remotion 스킬은 고정 upstream 설치**.
- 설치기, 파일별 SHA-256, 원본 대비 변경 기록, 참고 URL 목록, 개별 라이선스.

관련 회사/주식 영상에서 뉴스·사업·사용자 반응 설명은 최소 30%를 유지합니다.
공식 영상 60%와 별도로 계산합니다. 조회수·수익률·저작권 허가를 보장하지 않으며,
게시에는 사용자의 명시적 요청과 필요한 권리 검토가 필요합니다.

## 설치

Git과 Python 3.11+가 필요합니다. Windows에서는 짧은 경로에 복제하세요.

```text
git clone --branch v1.2.1 https://github.com/Kimhyuntae9665/codex-skill-moneyprinterturbo-video.git mpt-video
cd mpt-video
python scripts/install_bundle.py --profile core --dry-run
python scripts/install_bundle.py --profile core
```

| 선택 | 내용 |
| --- | --- |
| `--profile core` | 영상 제작 + 미국 주식 조사 + 로고 흐름도, 3개 |
| `--profile all` | 전체 동봉 워크플로, 53개 |
| `--profile all --with-external` | 53개 + 공식 Remotion 스킬 12개, 총 65개; Git/네트워크 사용 |

기본 대상은 `$CODEX_HOME/skills` 또는 `~/.codex/skills`입니다. 기존 폴더는
자동으로 덮어쓰지 않습니다. 계획을 검토한 후 `--overwrite`를 명시하면 백업을
남기고 교체합니다. 설치 후 새 Codex 대화를 여세요.

```text
python scripts/install_bundle.py --profile all --with-external
```

지원하는 Codex 버전에서는 플러그인으로 동봉한 53개를 설치할 수 있습니다:

```text
codex plugin marketplace add Kimhyuntae9665/codex-skill-moneyprinterturbo-video --ref v1.2.1
codex plugin add mpt-video@mpt-video
```

개별 스킬 경로는
[plugins/mpt/skills/mpt](https://github.com/Kimhyuntae9665/codex-skill-moneyprinterturbo-video/tree/v1.2.1/plugins/mpt/skills/mpt)입니다.
[설치·교체·환경 준비](docs/INSTALL.md)를 읽고 한 가지 설치 방식을 선택하세요.
개별 스킬 설치는 관련 스킬을 자동으로 설치하지 않습니다.

## 실행

Git, uv, FFmpeg/FFprobe, 네트워크를 준비한 뒤 점검합니다:

```powershell
python .\plugins\mpt\skills\mpt\scripts\check_environment.py --mode us-equity --json
```

Codex 요청 예시:

```text
$moneyprinterturbo-video 공식 제품 시연 영상을 중심으로 한국어 9:16 Short를 만들어줘.
각 장면의 주장을 1차 자료로 확인하고 실제 로고와 동작을 크게 보여줘.
자료 사용 권한, 공식 동영상 시간 비율, 음성·자막·화면 검수 결과도 전달해줘.
```

[실행 모드](plugins/mpt/skills/mpt/references/modes.md),
[공식 영상 제작 방법](plugins/mpt/skills/mpt/references/official-footage-production.md),
[완료 판정](plugins/mpt/skills/mpt/references/production-source.md)을 먼저 읽으세요.
`prepared-local`은 준비된 대본과 권리 확인된 로컬 자료, `topic-online`은 선택한
제공자의 키가 필요한 온라인 제작, `evidence-motion`은 주장·데이터가 고정된
정밀 연출 방식입니다.

## 전체 자료

```text
plugins/mpt/skills/mpt/        본체·참고문서·8개 helper·폰트·예제
plugins/mpt/skills/<name>/     52개 관련 스킬의 지원 파일과 LICENSE
scripts/install_bundle.py     core/all 설치, 외부 upstream 선택 fetch
scripts/audit_bundle.py       배포 무결성·경로·참조 검사
distribution/                 원본 원장·공개 파일 해시·참고 URL 목록
docs/                         설치·외부 의존성·전체 스킬 안내
tests/                        제작 helper 검사 + 배포/설치 회귀 검사
```

- [전체 스킬과 의존성](docs/SKILLS.md)
- [원본·변경 이력](distribution/source-inventory.json)
- [공개 파일 해시](distribution/file-manifest.json)
- [참고문헌·공식 문서 URL 목록](distribution/reference-catalog.json)
- [외부 엔진·재배포 범위](docs/EXTERNAL_DEPENDENCIES.md)
- [라이선스와 에셋 고지](THIRD_PARTY_NOTICES.md)
- [변경 기록](CHANGELOG.md)

실행 파일, GPU 드라이버, 모델 가중치, API 키·계정, 개인 영상 원본은 포함하지
않습니다. MCD 예제는 역사적 샘플이며 최신 투자 판단 자료가 아닙니다. 선택한
제작 방식의 실행 엔진과 자료 사용 권한을 별도로 준비하세요.

## English

A portable Korean short-video skill bundle: evidence research, official-demo
footage, authentic logos, motion direction, narration, subtitles and delivery QA.
The main workflow requires at least 60% official-video runtime; animated stills
do not count as footage.

Run `python scripts/install_bundle.py --profile core` for three core skills,
`--profile all` for 53 bundled skills, or add `--with-external` for 12 official
Remotion skills fetched at the recorded upstream commit. The installer verifies
hashes and refuses existing folders unless replacement with backup is explicit.
See [installation](docs/INSTALL.md) and [external requirements](docs/EXTERNAL_DEPENDENCIES.md).

Original work is MIT. Third-party skills keep their individual licenses; fonts
and photos keep their own notices. Official product footage is not redistributed
or automatically licensed. Package checks do not prove GPU inference, listening
review, rights clearance or uploads. Verify with `python scripts/audit_bundle.py`
and `uv run --frozen python -m unittest discover -s tests -v`.
