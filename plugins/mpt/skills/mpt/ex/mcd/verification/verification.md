# Verification record

Verified on 2026-08-29 KST. The finished video is a local deliverable and is
not committed to this repository.

## Delivered video

- Path: `<local-output>/MCD_initial.mp4`
- SHA-256: `F0A9C162D189646B3198D1783F020E5C5FE9E443EA56728A438004A75F5FFDA5`
- Size: 4,208,868 bytes
- Duration: 58.420 seconds
- Video: H.264, 1080x1920, 30 fps, yuv420p
- Audio: AAC, 44.1 kHz, stereo; measured mean volume -20.6 dB
- MoneyPrinterTurbo task: `21d67ff2-447e-46c1-909f-0ea0af3819bc`
- Upstream pin: `eb8c23757e098a07bbcd93b3b50e252fc8d1869a`
- Voice: `ko-KR-SunHiNeural`, requested rate `+17%`
- Inputs: one prepared local master, local Korean script, local font
- Disabled: stock-footage search, paid generation APIs, BGM, and social upload

`validate_video.py` returned `MPT_VIDEO_VALID`. FFprobe found one H.264 video
stream and one AAC audio stream. A full FFmpeg A/V decode with `-xerror`
completed successfully.

An independent faster-whisper `small` transcription recovered the key spoken
figures and terms, including 21x P/E, 2026, franchise, 5.3 billion dollars of
rent, royalties, annualized dividend, and 39.9 billion dollars of long-term
debt. This automated intelligibility check does not replace a human final
listening pass before publication.

## Motion master

- Renderer: Manim Community 0.21.0, pinned by `motion/uv.lock`
- SHA-256: `76137AB911EADBBE38672CF1CC0A044A8445BA30A248E7862DE82539B5FB9FFC`
- Duration: 59.200 seconds
- Video: H.264, 1080x1920, 30 fps, yuv420p, silent
- Price chart window: 126 raw-close observations from 2026-02-27 through
  2026-08-27; endpoints are checked in code as 341.06 and 260.06 dollars
- Full FFmpeg video decode: pass

Eight motion-master scene frames and ten finished-video frames, including seven
dense-subtitle checkpoints, were visually reviewed at native resolution. The
review covered the opening title and photo credit, raw-close chart, both
valuation comparisons, franchise share, rent/royalty split, dividend timeline,
risk screen, and closing photo. No text clipping, Korean line collision,
chart-callout mismatch, subtitle/source overlap, or first-frame loop remained
after repair.

The two building photographs were checked against `assets/asset-manifest.json`.
The CC BY 4.0 author, license, and vertical-crop notice are visible in the
opening; the CC0 courtesy credit is visible in the closing.

## Evidence and orchestration

- Research packet: 14 sources, 56 facts, 251 daily price rows, and 30
  calculation rows; JSON/CSV parsing and stored calculation checks passed.
- Five independent Council advisors completed and the synthesis gate passed
  5/5. The resulting claim boundary is "low versus the recent five-year
  history," not "an extreme 20-year historical bottom."
- Luna Team Build run `c032b7605e41459a9f4b9e6d0eaad463` completed all three
  tracks successfully. Actual wall time was 1,185.062 seconds and measured
  worker parallelism ratio was 2.12.

## Known runtime note

MoneyPrinterTurbo logged a Windows CP949 decode warning in a background reader
thread while FFmpeg output was being collected. The combine step subsequently
reported completion, the task exited successfully, and the delivered file
passed independent FFprobe, hash, and full A/V decode checks.

The older file `MCD_부동산_수익구조_Shorts_20260828.mp4` was preserved.
