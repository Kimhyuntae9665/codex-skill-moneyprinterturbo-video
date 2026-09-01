# MCD v8 research-applied Shorts verification

검증일: 2026-09-01 KST
데이터 기준일: 2026-08-31 미국 종가

## 최종 산출물

- final: `<local-output>/MCD_v8_research_applied.mp4`
- duration: 58.500000s
- video: H.264 High, yuv420p, 1080×1920, 30fps
- audio: AAC LC, 44.1kHz, stereo
- mean/max volume: -20.4 / -5.9 dB
- bytes: 14,503,625
- SHA-256: `FFDC736E9F861ECA2331C17A21B295C90E44B5435B6F135860A0ACDE4B94B511`
- common validator: `MPT_VIDEO_VALID`
- full video decode: PASS with FFmpeg `-xerror`
- full audio decode: PASS with FFmpeg `-xerror`
- freeze gate: no freeze event of at least 1 second at `n=0.003`

## 적용한 조사 결과

- 원클릭 생성 영상 대신 `claim ledger → 14-shot contract → deterministic renderer → reviewed SRT → full media QA`의 hybrid pipeline을 사용했다.
- HF·Reddit·GitHub 조사에서 반복된 규칙대로 AI가 약한 숫자·한국어·지도·차트·브랜드 geometry는 Pillow/FFmpeg 후합성으로 고정했다.
- 유료 provider, hosted generation, 대형 모델 다운로드, Blender/CUDA 의존성을 사용하지 않았다.
- 16개의 slide-like beat를 내레이션에 맞춘 14개 scene으로 합쳐 장면과 자막의 의미 경계를 맞췄다.
- 모든 scene에 primary object action, delayed secondary action, bounded continuous camera를 두어 1~3초마다 의미 있는 변화가 발생하도록 했다.
- header/title, evidence stage, source rail, caption lane, bottom dead zone을 분리했다.

## 핵심 시각 개선

- 지구본을 실제 Natural Earth 기반 평면 vector world map으로 교체하고 노드·연결선·46,028·약 95% 카드를 서로 다른 lane에 배치했다.
- 부동산 장면은 LAND, BUILDING, EQUIPMENT를 수직 폭발도로 분리하고 RENT와 ROYALTY를 오른쪽 고정 lane에 뒀다.
- 배당·순현금 자사주매입은 FCF hub에서 갈라지는 실제 흐름으로, 현금 주주환원률과 50년 인상은 ring과 year stack으로 표현했다.
- beta와 MCD–QQQ 상관을 별도 장면으로 분리해 기술주와 다른 리듬을 직접 비교했다.
- 위험 장면에서 화면 밖으로 잘린 차량을 제거하고 큐에서 완전히 사라지는 상태 변화로 수정했다.
- 마지막에는 큰 golden-arches geometry와 회복/취소 gate를 분리했다. 취소선·밑줄·플랫폼 UI와 혼동되는 장식은 사용하지 않았다.
- 12pt ASS subtitle을 고정 dark caption lane에 배치해 content card와 겹치지 않게 했다.

## 자동·수동 QA

- `validate_video.py`: duration, stream count, H.264/AAC, 1080×1920, volume, three review frames 검증.
- FFmpeg: video/audio full decode, 30fps probe, `freezedetect=n=0.003:d=1`, `volumedetect` 검증.
- manual review: 2-second full-duration contact sheet, fourteen scene midpoints, 3.0s hook, 13.2s property, 27.2s yield, 44.3s risk, 57.5s final frame 확인.
- final 3-line caption도 reserved caption lane 안에 들어가며, title·source·decision card를 침범하지 않는 것을 확인했다.
- `layout_qa_v8.py`: 14개 scene, error 0, warning 0, PASS.
- `frame_probe_v8.py`: 최종 MP4 metadata, 29/29 boundary·midpoint frames, contact sheet, freeze gate PASS.

## MPT와 Luna 경계

- 한국어 내레이션은 prepared-local MPT task `93cab07a-d9d4-43cc-83de-4dbe41365032`에서 생성·검증된 음성을 재사용했다. v8 내레이션은 v6 텍스트와 동일하다.
- `run-luna-team.ps1` planning manifest는 validation을 통과했지만 Windows session의 전역 live-worker ceiling 때문에 3개 task가 모두 pending에서 시작하지 못했다. 이 실패를 완료 작업으로 세지 않았다.
- fallback Luna collaboration에서 editorial, executable layout QA, independent visual review 세 작업을 완료했다.
- 독립 비평이 찾은 `46,028 / RESTAURANTS`, `$7.35 / divider`, entry price rail 충돌을 수정하고 최신 subtitle-burn MP4를 다시 검증했다.

## 게시 경계

이 영상은 교육 목적의 조건부 기업 분석이며 개인 맞춤 투자자문이 아니다. YouTube, Instagram, X 업로드나 자동 게시를 수행하지 않았다.
