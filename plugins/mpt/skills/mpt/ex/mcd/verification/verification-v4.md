# MCD v4 검증 기록

검증일은 2026-08-29 KST, 시장 데이터 기준은 2026-08-27 미국 종가다.

## 재현 구성

- MoneyPrinterTurbo upstream: `eb8c23757e098a07bbcd93b3b50e252fc8d1869a`
- 최종 MoneyPrinterTurbo task: `885c3175-7420-4af6-9838-43229c50eb65`
- source mode: prepared-local, 단일 master, sequential, transition 없음
- renderer: Manim Community `0.21.0`, 1080×1920, 30fps
- voice: `ko-KR-SunHiNeural-Female`, rate `1.17`
- BGM·LLM·온라인 stock search·유료 생성·소셜 업로드: 사용하지 않음

무음 master:

- duration: `59.630729s`
- codec: H.264, `yuv420p`, 30fps
- bytes: `3,350,567`
- SHA-256: `31C83A699DA4F1E54EF4E2CB4368051CFE7680929A5B9EF490341D48C858CBA9`

## 자막과 겹침 복구

Edge 자막 집계는 `sub_items len: 15, script_lines len: 24`로 실패했다. 자동
자막이 없는 MPT 결과를 완성본으로 사용하지 않고, 로컬
`faster-whisper-small`의 단어 타임스탬프만 사용해 숫자·고유명사를 확정 대본과
대조한 `subtitle.v4.srt` 24개 구간을 만들었다.

v3에서 겹쳤던 약 9초 전환 문장 패널을 제거했다. 모든 장면에
`CAPTION_BAND_TOP=-2.28`의 자막 전용 영역을 만들고, 본문·출처를 그 위에
제한했다. 검수 자막은 Noto Sans KR, ASS 11 units, `MarginV=48`로 번인했다.
최종본에서 12개 대표·전환 프레임과 배당 장면 원본 크기 프레임을 다시 검토해
본문, 출처, 제목, 현재값, 자막 사이의 겹침이 없음을 확인했다.

## 최종 MP4

- path: `<local-output>/MCD_v4_final.mp4`
- duration: `59.400000s`
- resolution: `1080×1920`
- video: H.264, `yuv420p`, 30fps
- audio: AAC, 44.1kHz, stereo
- bytes: `5,288,512`
- mean volume: `-20.6dB`
- max volume: `-6.0dB`
- SHA-256: `34C8458F90DA4D03215B0172AC30D759ED4E6868E921E7305FFC68BD67507003`

`validate_video.py`는 `MPT_VIDEO_VALID`을 반환했다. FFmpeg `-xerror`로 영상과
음성을 각각 끝까지 디코드했으며 오류가 없었다. 기존 v2·v3 및 중간 v4 파일은
삭제하거나 덮어쓰지 않았다.

## 배당수익률 회귀 검증

`research/recompute_v4.py --offline`과 단위 테스트가 다음 값을 저장 CSV에서
다시 계산한다.

- 월말 관측치 200개, 현재 TTM 배당 7.35달러, 수익률 2.8263%
- 2020년 이후 2 / 80, 2023년 이후 1 / 44
- 2010년 이후 74 / 200, 상위 37.0%, 중앙값 2.5070%
- 2015-08-31 최고 3.5782%

이 순위는 비조정 월말 종가와 당시 최근 4회 현금배당을 사용한 역사적 계산이며,
향후 배당이나 총수익률을 보장하지 않는다.
