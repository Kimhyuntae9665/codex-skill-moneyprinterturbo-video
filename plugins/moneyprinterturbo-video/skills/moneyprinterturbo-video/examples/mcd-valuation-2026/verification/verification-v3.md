# MCD v3 검증 기록

검증 기준일은 2026-08-29 KST, 시장 데이터 기준은 2026-08-27 미국 종가다.
이 문서는 저장소에 MP4나 런타임 로그를 넣지 않고도 최종 산출물의 근거와 제작
상태를 추적하기 위한 기록이다.

## 재현 구성

- MoneyPrinterTurbo upstream: `eb8c23757e098a07bbcd93b3b50e252fc8d1869a`
- MoneyPrinterTurbo task: `31d45c2d-2bd5-4a86-8643-f62907b8578b`
- source mode: prepared-local, 단일 master, sequential, transition 없음
- renderer: Manim Community `0.21.0`, 1080×1920, 30fps
- voice: `ko-KR-SunHiNeural-Female`, rate `1.17`
- BGM·LLM·온라인 stock search·유료 생성·소셜 업로드: 사용하지 않음

무음 master:

- duration: `59.066016s`
- codec: H.264, `yuv420p`, 30fps
- bytes: `3,314,227`
- SHA-256: `9C45EC197684677FEA5FB5A4C138C5EB7A605C4DC85FF3688647802D654E42CA`

## 자막 복구

첫 MoneyPrinterTurbo 결과는 내레이션과 영상은 정상이었지만 Edge 자막 집계가
`sub_items len: 11, script_lines len: 21`로 실패했다. 로그는 자막 파일이 없어
자막을 생략했다고 명시했으며, 따라서 그 파일을 완성본으로 사용하지 않았다.

복구 절차:

1. 원래 task와 SunHi 오디오를 보존했다.
2. 로컬에 이미 있던 `faster-whisper-small`은 텍스트 채택이 아니라 음성 구간
   타임스탬프 복구에만 사용했다.
3. 숫자·고유명사 오인식을 잠근 내레이션과 근거 자료로 사람이 교정해
   `subtitle.v3.srt` 21개 구간을 만들었다.
4. `scripts/burn_subtitles.py`와 번들 Noto Sans KR로 같은 MPT MP4에 자막을
   번인했다.
5. 자동 Whisper 교정 함수가 만든 뒤틀린 1:N 매핑과 0초 자막은 사용하지 않았다.

## 최종 MP4

- path: `<local-output>/MCD_v3.mp4`
- duration: `58.366016s`
- resolution: `1080×1920`
- video: H.264, `yuv420p`, 30fps
- audio: AAC, 44.1kHz, stereo
- bytes: `5,354,692`
- mean volume: `-20.4dB`
- max volume: `-6.2dB`
- SHA-256: `7A602F16D032FC2E46ADFCD2DA068CC903908A5B23CD97C699A6C448717C4C26`

`validate_video.py`는 `MPT_VIDEO_VALID`을 반환했다. FFmpeg `-xerror`로 전체
비디오·오디오 스트림을 끝까지 디코드했으며 오류가 없었다. 시작, 모든 장면
경계, 주주환원 원형 그래프, beta rail, 상관 파형, 위험 경고, 엔딩을 포함한
21개 프레임을 세로 원본 비율로 검토했다. 자막은 두 줄 이하이고 본문 숫자와
출처 칩을 가리지 않는다.

기존 v2 파일
`<local-output>/MCD_prior_draft.mp4`
는 삭제하거나 덮어쓰지 않았다.

## 수치 회귀 검증

`research/recompute_v3.py --offline`과 단위 테스트로 다음 값을 저장 CSV에서 다시
계산한다.

- 주간 가격 262개, 단순 주간 수익률 261개
- MCD beta vs SPY `0.4766795`
- QQQ beta vs SPY `1.2516079`
- MCD–QQQ 상관 `0.3273663`
- TTM 배당 `5.225B달러`
- TTM 순현금 자사주매입 `2.086B달러`
- 현금 주주환원 합계 `7.311B달러`
- 시가총액 근사 대비 현금 주주환원률 `3.9727%`

이는 역사적 계산이다. QQQ는 Nasdaq-100 대형 성장주 프록시이고 순수 기술 섹터
지수가 아니다. 낮은 beta와 낮은 상관은 미래 성과·분산효과·낮은 총위험을
보장하지 않는다. 현금 주주환원률도 회사가 공시한 공식 비율이 아니다.
