# Skill integration verification

Date: 2026-09-01 (Asia/Seoul)

Scope: update the reusable `moneyprinterturbo-video` Skill with the MCD v8
evidence-motion workflow. This note verifies the Skill and its generic QA tools;
it does not refresh the dated financial claims in the MCD example.

## Skill package

- Canonical source:
  `plugins/mpt-video/skills/moneyprinterturbo-video`
- Installed Skill:
  `$CODEX_HOME/skills/moneyprinterturbo-video`
- `quick_validate.py`: PASS for both source and installed directories.
- Source/install SHA-256 comparison: PASS for all synchronized files.
- Python AST parsing: PASS for `validate_scene_manifest.py` and
  `probe_scene_frames.py`.
- PowerShell parsing: PASS for `motion/render_v8.ps1`.

## Contract tests

- Generic template: PASS, 3 scenes, 0 errors, 0 warnings.
- Frozen MCD v8 manifest: PASS, 14 scenes, 0 errors, 0 warnings.
- MCD v8 manifest illegal overlap count: 0 in every scene.
- All scenes declare at least two state changes; the final scene declares three.

## Finished-video smoke test

Input:
`<local-output>/MCD_v8_research_applied.mp4`

- `validate_video.py`: `MPT_VIDEO_VALID`.
- Duration: 58.5 seconds.
- Resolution and rate: 1080x1920, 30 fps.
- Streams: H.264 video, yuv420p; AAC audio; mean volume -20.4 dB.
- Generic scene probe: PASS.
- Boundary and midpoint extraction: 29/29 frames.
- Contact sheet: generated and manually inspected.
- FFmpeg freeze detection at the 1.0-second gate: 0 events.
- File size: 14,503,625 bytes.
- SHA-256:
  `FFDC736E9F861ECA2331C17A21B295C90E44B5435B6F135860A0ACDE4B94B511`.

The boundary contact sheet intentionally includes frames captured during the
yellow content-zone wipe. This confirms that transition frames are evaluated,
not skipped. No new card collision, clipped Korean copy, caption intrusion, or
transition remnant was observed in the smoke-test sheet.

Social publishing was not performed.
