# 설치 / Installation

## 가장 간단한 설치

Git, Python 3.11 이상을 설치한 뒤 저장소를 받습니다. 경로가 긴 Windows
환경에서는 짧은 폴더에 내려받으세요.

```text
git clone --branch v1.2.1 https://github.com/Kimhyuntae9665/codex-skill-moneyprinterturbo-video.git mpt-video
cd mpt-video
python scripts/install_bundle.py --profile core --dry-run
python scripts/install_bundle.py --profile core
```

`core`는 `moneyprinterturbo-video`, `us-stock-research`,
`logo-flow-infographics` 3개를 설치합니다. 기본 대상은 `$CODEX_HOME/skills`,
환경 변수가 없으면 `~/.codex/skills`입니다. Codex 설정, 계정, 모델 설정을
수정하지 않습니다. 설치 후 새 대화를 열어 스킬을 불러오세요.

모든 동봉 워크플로 53개를 설치하려면:

```text
python scripts/install_bundle.py --profile all --dry-run
python scripts/install_bundle.py --profile all
```

Remotion 공식 스킬 12개까지 사용하려면 다음을 실행합니다. 이 명령은 Git과
네트워크를 사용해 공식 저장소의 고정 커밋을 가져옵니다. 공식 스킬 원문은 이
배포에 복제하지 않았습니다. 설치 전에 [외부 의존성](EXTERNAL_DEPENDENCIES.md)을
읽으세요.

```text
python scripts/install_bundle.py --profile all --with-external --dry-run
python scripts/install_bundle.py --profile all --with-external
```

기존 폴더가 있으면 설치는 파일을 쓰기 전에 중단합니다. 교체하려면 결과를
검토하고 `--overwrite`를 명시하세요. 기존 폴더는 설치 대상의 상위 폴더 안
`mpt-skill-backups/<UTC timestamp>/`에 보존됩니다. 되돌릴 때는 Codex를 종료하고
해당 백업을 원래 이름으로 복원하세요. `--target /your/skills/path`로 사용자
환경을 건드리지 않는 별도 설치도 가능합니다.

## Codex 플러그인

이 저장소의 marketplace는 동봉한 53개 스킬을 하나의 플러그인으로 제공합니다.
해당 명령을 지원하는 Codex 버전에서:

```text
codex plugin marketplace add Kimhyuntae9665/codex-skill-moneyprinterturbo-video --ref v1.2.1
codex plugin add mpt-video@mpt-video
```

Codex 버전에 따라 플러그인 UI/명령 지원이 다를 수 있습니다. 지원하지 않으면
위 Python 설치기를 사용하세요. 개별 스킬 설치용 경로도 유지했습니다:

```text
$skill-installer Install https://github.com/Kimhyuntae9665/codex-skill-moneyprinterturbo-video/tree/v1.2.1/plugins/mpt/skills/mpt
```

개별 설치는 관련 스킬을 자동으로 설치하지 않습니다. 미국 주식 영상에는
`core` 설치를 권장합니다. 플러그인과 standalone을 중복 설치하면 같은 이름이
두 번 검색될 수 있으니 한 방식을 선택하세요.

## 실행 도구와 첫 점검

기본 제작에는 Git, Python 3.11+, uv, FFmpeg/FFprobe 및 최초 다운로드·Edge TTS에
접속할 네트워크가 필요합니다. 이 설치기는 운영체제 도구나 API 키를 설치하지
않습니다. 공식 설치 문서: [Python](https://www.python.org/downloads/),
[Git](https://git-scm.com/downloads), [uv](https://docs.astral.sh/uv/getting-started/installation/),
[FFmpeg](https://ffmpeg.org/download.html).

설치 전 저장소에서도 검사할 수 있습니다:

```powershell
python .\plugins\mpt\skills\mpt\scripts\check_environment.py --mode us-equity --json
```

실제 설치 후에는 설치된 `moneyprinterturbo-video/scripts/check_environment.py`를
실행하세요. PATH에 도구가 없으면 실패로 보고합니다. 설치 성공과 제작 환경
점검 성공은 서로 다른 결과입니다.

`prepared-local`은 준비된 대본·사용 권한이 확인된 로컬 미디어를 사용합니다.
`topic-online`은 선택한 LLM/미디어 제공자의 자격 증명이 필요할 수 있습니다.
`mpt_agent.py --help`와 본체의 [모드 안내](../plugins/mpt/skills/mpt/references/modes.md)를
먼저 읽으세요. MoneyPrinterTurbo는 본체 스크립트에 명시된 커밋을 별도 런타임에
설치하며, 저장소에 엔진 전체를 포함하지 않습니다.

Blender, Manim, Remotion, HyperFrames, Inkscape, Hugging Face 모델은 선택한
제작 방식에만 필요합니다. 서비스 비용·라이선스·GPU 요구량은 해당 제공자의
현재 조건을 확인하세요. 원격 GPU는 본인의 승인된 서버를 설정해야 합니다.

## English quick start

Clone the tagged release and run `python scripts/install_bundle.py --profile core`.
It verifies SHA-256 hashes and installs three core skills into `$CODEX_HOME/skills`
or `~/.codex/skills`. Use `--profile all` for 53 bundled workflows, and explicitly
add `--with-external` to fetch 12 official Remotion skills at the locked commit.
Use `--dry-run` to inspect the plan. Existing folders are refused unless you use
`--overwrite`, which backs them up. Start a new Codex task after installation.

Install external executables separately and run the environment check. A passing
package check does not establish that a production video, GPU inference, rights
clearance, listening review, or YouTube upload was completed.
