# 오픈소스 모션 렌더러 smoke 결정

기준일: 2026-08-29 KST
대상: Windows PowerShell, 1080×1920 세로형 한국어 금융 Short master
결정: **Manim Community 0.21.0을 전체 제작용 기본 렌더러로 채택**

## 결론

Manim은 이 Windows 환경에서 `python -m manim render` 한 번으로 비대화식 씬 렌더가 재현됐다. 한글 `Text`와 수치·선 그래프만 사용하면 LaTeX 없이도 동작했고, 최종 smoke는 1080×1920 H.264 MP4로 검증됐다.

Motion Canvas는 TypeScript와 실시간 편집 경험은 좋지만, 공식 렌더 문서의 주 경로가 Vite 에디터의 Video Settings 탭에서 `RENDER` 버튼을 누르는 방식이다. 따라서 Windows 무인 작업에는 브라우저 자동화나 별도 exporter 제어가 필요하다. 이 평가의 목적에는 파일·씬을 직접 받는 Manim CLI가 더 단순하고 재현성이 높다.

## 공식 프로젝트·라이선스·버전

### Motion Canvas

- 공식 저장소: <https://github.com/motion-canvas/motion-canvas>
- 안정 릴리스: `v3.17.2` — <https://github.com/motion-canvas/motion-canvas/releases/tag/v3.17.2>
- 공식 라이선스 파일: <https://github.com/motion-canvas/motion-canvas/blob/v3.17.2/LICENSE>
- 라이선스: MIT. `v3.18.0-alpha.0`은 prerelease이므로 제작 pin에서 제외했다.
- 공식 시작 문서: <https://motioncanvas.io/docs/quickstart/>
- 공식 렌더 문서: <https://motioncanvas.io/docs/rendering/>
- 공식 FFmpeg exporter 문서: <https://motioncanvas.io/docs/rendering/video/>

2026-08-29에 실행한 `npm view`에서 `@motion-canvas/core`, `@motion-canvas/2d`, `@motion-canvas/vite-plugin`, `@motion-canvas/ffmpeg`, `@motion-canvas/create`의 안정 버전은 모두 `3.17.2`였다. npm 메타데이터의 각 패키지 license도 MIT였다. 직접 패키지의 unpacked size는 각각 865,449 / 1,732,849 / 75,324 / 29,988 bytes이며, 이는 transitive `node_modules` 전체 크기가 아니다.

공식 Windows/Node 경로는 다음과 같다.

```powershell
npm init @motion-canvas@latest
npm install
npm install --save @motion-canvas/ffmpeg
npm run serve
```

그 후 `vite.config.ts`에 `@motion-canvas/ffmpeg`의 `ffmpeg()` plugin을 넣고 에디터의 Video Settings 탭에서 `RENDER`를 실행한다. 공식 렌더 문서는 프레임을 프로젝트 `output`에 저장하고, FFmpeg exporter가 완성 영상을 만든다고 설명한다. 이 페이지들에는 `motion-canvas render scene.ts --headless`와 같은 공식 무인 CLI가 제시되지 않는다. 따라서 자동화 시에는 `npm run serve`를 띄운 뒤 브라우저 자동화로 에디터를 조작하고, output/MP4 생성 완료를 별도로 감시해야 한다. Node 22.22.2는 공식 quickstart의 Node 16 이상 조건을 만족하지만, plugin peer 범위가 Vite 4.x 또는 5.x인 점은 pin 시 확인해야 한다.

평가 경계: 불필요한 `node_modules`를 선택 프로젝트에 남기지 않기 위해 Motion Canvas의 설치·브라우저 렌더 자체는 수행하지 않고, 공식 문서·GitHub 릴리스·npm package metadata와 로컬 Node/npm 경로를 확인했다. 따라서 Motion Canvas의 Windows browser automation은 별도 POC가 필요한 미검증 영역이다.

### Manim Community

- 공식 저장소: <https://github.com/ManimCommunity/manim>
- 공식 릴리스: `v0.21.0` — <https://github.com/ManimCommunity/manim/releases/tag/v0.21.0>
- 원본 MIT 라이선스: <https://github.com/ManimCommunity/manim/blob/v0.21.0/LICENSE>
- 커뮤니티 저작권 고지: <https://github.com/ManimCommunity/manim/blob/v0.21.0/LICENSE.community>
- 공식 설치 문서: <https://docs.manim.community/en/stable/installation.html>
- 공식 Windows/local 설치 안내: <https://docs.manim.community/en/stable/installation/linux.html>
- 공식 CLI/config 문서: <https://docs.manim.community/en/stable/guides/configuration.html>
- 공식 render 명령 문서: <https://docs.manim.community/en/stable/reference/manim.cli.render.html>
- 라이선스: MIT. 원본과 커뮤니티 에디션의 저작권 고지가 각각 존재한다. 코드의 MIT 허용 범위와 별개로 사진·상표·폰트·3Blue1Brown의 Pi 캐릭터 같은 콘텐츠 권리는 따로 확인해야 하며, 이 smoke에는 외부 이미지·캐릭터·로고를 사용하지 않았다.

## 로컬 버전·의존성 footprint

측정 환경:

| 항목 | 측정값 |
|---|---|
| OS shell | Windows PowerShell |
| Python | 3.13.7 |
| Node / npm | v22.22.2 / 10.9.7 |
| uv | 0.10.10 |
| Manim | 0.21.0, `pyproject.toml` 및 `uv.lock` pin |
| FFmpeg / ffprobe | `2025-07-12-git-35a6de137a-full_build-www.gyan.dev` |
| uv lock graph | 38 packages resolved |
| 실제 local `.venv` | 34 distributions, 297,595,734 bytes = 283.81 MiB |
| LaTeX | 미설치. 이 씬은 `Text`만 사용하므로 필요 없음 |

Setup은 project directory에서 실행한다.

```powershell
uv venv --python 3.13 .venv
uv lock
uv sync --frozen
```

실제 렌더에 사용한 외부 runtime은 PATH의 FFmpeg/ffprobe와 local `.venv`뿐이다. global pip/npm 설치와 root `pyproject.toml`/`package.json` 수정은 하지 않았다. Manim 공식 `checkhealth`는 direct module 호출이라 `manim` executable이 PATH에 없다고 경고했고, LaTeX도 없다고 경고했지만, 아래 direct-module render는 성공했다. Python 3.13 import 때 dependency `pydub`의 SyntaxWarning이 출력되었으나 렌더 결과에는 오류가 없었다.

## 정확한 비대화식 렌더 경로

재현용 wrapper는 [render_smoke.ps1](./render_smoke.ps1)이고, 내부에서 다음 명령을 실행한다.

```powershell
& .\.venv\Scripts\python.exe -m manim render `
  --renderer=cairo `
  --media_dir .\render-cache `
  --disable_caching `
  --flush_cache `
  --resolution 1080,1920 `
  --frame_rate 30 `
  --format mp4 `
  --output_file mcd-valuation-smoke `
  .\manim_smoke.py `
  MCDValuationSmoke
```

실제 실행은 다음과 같다. 이 명령이 만드는 `output/mcd-valuation-smoke.mp4`는
검증용 런타임 산출물이므로 저장소에는 커밋하지 않는다. 아래 해시와 측정값은
2026-08-29에 실제 생성한 파일을 기준으로 기록했다.

```powershell
.\render_smoke.ps1
```

`--disable_caching`으로 stale partial frame을 사용하지 않게 했고, `render-cache`는 local intermediate만 담는다. Manim이 만든 nested MP4를 wrapper가 `output/mcd-valuation-smoke.mp4`로 복사한다. 최종 cold/no-cache 측정 render time은 wrapper Stopwatch 기준 **6.50 s**였다. smoke source는 부모 brief의 `341.06 → 260.06`, `−23.8%` raw-close 값을 사용하지만 `교육용 편집 프레임`으로 표시하며 live quote로 주장하지 않는다.

## 산출물 ffprobe / 전체 decode

검증 명령:

```powershell
ffprobe -v error -print_format json -show_format -show_streams `
  .\output\mcd-valuation-smoke.mp4

ffmpeg -hide_banner -loglevel error -xerror `
  -i .\output\mcd-valuation-smoke.mp4 `
  -map 0:v:0 -f null NUL
```

최종 파일 SHA-256은 `93FB83F6181D5EA5F1B13190A0C76BAEC0F7E2D79B01BC7AF824AFE3346F082A`이다. `ffprobe` 핵심 결과는 다음과 같다.

```json
{
  "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
  "format_size": 199573,
  "format_duration": "5.898698",
  "format_probe_score": 100,
  "stream_count": 1,
  "codec_name": "h264",
  "profile": "High",
  "width": 1080,
  "height": 1920,
  "pix_fmt": "yuv420p",
  "field_order": "progressive",
  "r_frame_rate": "30/1",
  "nb_frames": "177",
  "stream_duration": "5.898698",
  "audio_streams": 0,
  "stream_bit_rate": 266548
}
```

전체 decode는 **exit code 0**, stderr empty, 측정 wall time 약 **0.97 s**였다. 5.898698초는 요구 범위 3~6초 안이며, 세로 1080×1920·30fps·무음 MP4 조건을 만족한다.

## 대표 프레임·안전영역 육안 검사

다음으로 temporary `qa/` PNG를 추출해 직접 확인했다. `qa/`는 최종 전달 전에 제거하며 local `.gitignore`로도 제외한다.

```powershell
ffmpeg -hide_banner -loglevel error -y -ss 0.80 `
  -i .\output\mcd-valuation-smoke.mp4 -frames:v 1 .\qa\frame-start.png
ffmpeg -hide_banner -loglevel error -y -ss 3.00 `
  -i .\output\mcd-valuation-smoke.mp4 -frames:v 1 .\qa\frame-middle.png
ffmpeg -hide_banner -loglevel error -y -ss 5.50 `
  -i .\output\mcd-valuation-smoke.mp4 -frames:v 1 .\qa\frame-end.png
```

픽셀 배경 대비 threshold 18로 산출한 representative-frame bounding box는 다음과 같다.

| 프레임 | bbox `(left, top, right, bottom)` | 육안 결과 |
|---|---:|---|
| 0.80 s 시작 | `(100, 562, 843, 863)` | 제목/메타데이터가 나타나며 상단 잘림 없음 |
| 3.00 s 중간 | `(100, 562, 843, 1218)` | 하강 선이 부분 진행되고 가격행·차트 겹침 없음 |
| 5.50 s 끝 | `(100, 562, 842, 1510)` | 전체 선·양 끝점·footer가 안정적으로 정지 |

최종 프레임 기준으로 확인한 보수적 안전영역은 `x=96..849`, `y=150..1619`이다. 시작/중간/끝 모두 다음 문제가 없었다.

- 상단 `y=0..149`: 비어 있어 Shorts 상단 UI/자막과 충돌하지 않는다.
- 좌우: content bbox가 `x=100..843` 이내여서 우측 컨트롤 영역 `x>=850`과 겹치지 않는다.
- 중간: `341.06 → 260.06`과 `−23.8%`가 분리되고, 제목 아래에 차트가 시작한다.
- 하단 `y=1620..1919`: 비어 있다. footer는 `y=1510` 안에서 끝나므로 후속 자막 합성 여지가 있다.
- 스타일: carbon/bone/slate/brass/brick/mint 계열, 단일 하강 가격선, 절제된 숫자·타이포그래피다. 카드 그리드·이모지·바운스는 사용하지 않았다.

초기 렌더에서 가격행 충돌과 제목/차트 충돌을 발견해 위치·크기를 수정했고, 수정 후 대표 프레임을 다시 추출해 위 수치를 확인했다. 빈 상·하단은 Shorts overlay와 후속 자막을 위한 의도적 여백으로 유지한다.

## 전체 제작 추천과 남은 제한

1. 전체 master는 Manim Community 0.21.0 + `uv.lock`을 사용한다. 원자료 숫자를 Python data contract로 분리하고, scene은 chart/typography primitives만 렌더링한 뒤 silent MP4로 내보낸다.
2. MoneyPrinterTurbo prepared-local 단계에서는 검증된 master MP4에 SunHi 한국어 음성·자막을 후합성한다. live web query, 유료 API, 업로드는 renderer 단계에 넣지 않는다.
3. 모든 릴리스에서 `render_smoke.ps1` 재실행, `ffprobe`, `ffmpeg -xerror`, 0.8/3.0/5.5초 frame QA를 gate로 둔다. `manim` PATH 대신 wrapper의 `python -m manim` 호출을 유지한다.
4. Motion Canvas는 향후 브라우저 자동화 POC가 필요하고, Vite peer 범위·에디터 UI selector·output completion 감시를 먼저 고정해야 한다. 무인 CI의 단일 master 경로로 승격하기 전까지는 추천하지 않는다.

### 파일/캐시 정책

저장소에는 소스·설정·lock·재현 명령·검증 기록만 전달한다. `.venv/`, `render-cache/`, `qa/`, `output/`, `node_modules/`, `__pycache__/`는 local `.gitignore`로 제외한다. smoke MP4와 대표 프레임은 검증 시마다 wrapper와 FFmpeg 명령으로 재생성한다.
