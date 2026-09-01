# Execution modes

## Prepared-local

Use this mode when the content is already fact-checked and the visuals are local files with clear rights. It is the preferred path for company explainers, portfolio samples, and any task where exact narration matters.

Required inputs:

- a non-empty UTF-8 script file;
- at least one supported local image or video;
- an explicit voice or custom audio choice;
- an explicit aspect ratio and output target.

The helper converts `--script-file`, repeated `--material`, or `--materials-dir` into MoneyPrinterTurbo CLI arguments. A run counts as prepared-local only when the effective CLI contains a non-empty script, `video_source=local`, and non-empty local materials. Only then may the helper skip LLM and stock-provider credential checks.

For Korean subtitles, use the bundled Noto Sans KR font. The font file is staged into the isolated runtime and is not installed system-wide.

### Evidence-motion submode

Use the evidence-motion submode when the local material is a directed data or
brand explainer rather than a set of interchangeable clips. Freeze the claim
ledger, narration, SRT, scene manifest, and renderer before calling the helper.
Pass one master MP4, use sequential concat, disable transitions, and set the
clip duration at least as long as the Short. Run the scene-manifest and
boundary-frame gates described in `evidence-motion-workflow.md` in addition to
the normal prepared-local validation.

## Topic-online

Use this mode only when the user wants automated script generation or online material search. The helper may request:

- `MPT_LLM_PROVIDER`
- `MPT_LLM_API_KEY`
- `MPT_LLM_BASE_URL`
- `MPT_LLM_MODEL_NAME`
- `MPT_PEXELS_API_KEY`
- `MPT_VOLCENGINE_ARK_API_KEY`

Ask only for fields named by `MPT_NEEDS_INPUT`. Never echo values or put them in commands that will be copied into public artifacts. Existing credentials are stored only in the isolated runtime configuration.

`MPT_LLM_PROVIDER`, API key, base URL, and model are all required for a generic OpenAI-compatible endpoint. Pexels keys are validated against an authenticated endpoint before use.

## Paid providers

The helper treats `volcengine_seedance`, `wavespeed`, and `loomloom` as paid video sources. A paid source requires the top-level `--confirm-paid-provider` flag after the user explicitly confirms the charge. Volcengine Seedance additionally requires the upstream `--confirm-seedance-charge` flag. Do not infer consent from a topic, an existing key, or a prior unrelated task.

Sonilo and other paid music providers are not selected by this Skill. Use `--bgm-type none` unless the user supplies a rights-cleared local track or explicitly authorizes a supported paid music provider.

## Isolated runtime and upstream pin

Default runtime:

```text
~/.codex/runtimes/moneyprinterturbo/eb8c23757e098a07bbcd93b3b50e252fc8d1869a
```

The helper fetches the exact full commit with Git, checks out detached HEAD, and verifies `rev-parse HEAD`. It does not fall back to `main`. An existing non-Git directory or mismatched commit fails closed.

The runtime configuration always forces:

```text
upload_post_enabled = false
upload_post_auto_upload = false
upload_post_platforms = []
```

This Skill does not reuse `~/MoneyPrinterTurbo`, because saved settings there could enable cross-posting, paid music, or other behavior outside the current request.

## Exit contract

- `0`: `MPT_RESULT` lists verified non-empty MP4 files and artifact paths.
- `10`: `MPT_NEEDS_INPUT` lists only missing or rejected credentials.
- `1`: `MPT_ERROR` reports an actionable failure; inspect only the named log tail.

Dependency installation and generation can take several minutes. Keep one foreground terminal session and resume that session rather than starting duplicate jobs or polling with new processes.

## Verification contract

`validate_video.py` checks:

- file existence and non-zero size;
- FFprobe-readable video and audio streams;
- expected width, height, duration, and codecs;
- full FFmpeg decode without errors;
- narration mean volume above the configured silence floor;
- absence of prepared-local log evidence for stock, paid-video, or cross-post execution;
- extracted representative frames for human visual review.

Automated checks cannot prove factual accuracy, asset licensing, mobile readability, or whether a frame is visually persuasive. Review the script sources and representative frames before delivery.
