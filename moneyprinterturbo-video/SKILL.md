---
name: moneyprinterturbo-video
description: Create and verify a finished short-form MP4 with MoneyPrinterTurbo from a topic or prepared script. Use for YouTube Shorts, Reels, TikTok, Korean narration, local visual materials, stock-footage generation, MoneyPrinterTurbo setup or repair, and requests that expect the final video file rather than instructions alone.
---

# MoneyPrinterTurbo Video

Produce the finished video, verify it, and return its path. Do not stop at setup or commands.

## Choose the mode

- Use `prepared-local` when a complete script and rights-cleared local images or videos are available. This mode avoids LLM and stock-provider credentials. It still needs network access for the pinned upstream checkout, dependencies, and Edge TTS.
- Use `topic-online` when MoneyPrinterTurbo must write the script or find online footage. Request only credentials reported by `MPT_NEEDS_INPUT`.
- If factual or time-sensitive claims appear in the video, verify them with primary sources before freezing the script. Keep facts, interpretation, and unresolved limits distinct.

Read [references/modes.md](references/modes.md) for exact input, credential, and recovery rules. When the request calls for premium charts, real photography, or motion design, also read [references/professional-motion.md](references/professional-motion.md). For the current MCD valuation example, read the files under [examples/mcd-valuation-2026](examples/mcd-valuation-2026/). The older static-card example remains under [examples/mcd-2025](examples/mcd-2025/).

## Safety contract

- Never post to YouTube, TikTok, Instagram, or another service unless the user separately asks for publishing. The helper disables Upload-Post in its isolated runtime.
- Never select Seedance, WaveSpeed, LoomLoom, Sonilo, or another paid generation provider without explicit user confirmation of the charge. Do not add confirmation flags silently.
- Never print credentials, `config.toml`, environment values, or full credential-bearing logs.
- Use only owned, generated, public-domain, or license-compatible materials. Do not infer that the upstream MIT license covers fonts, music, stock media, logos, or third-party photos.
- Run one video job at a time. Do not start the WebUI, API server, Docker service, or cross-posting service for an ordinary Skill request.

## Prepared-local execution

Resolve this Skill directory, set the terminal working directory to its `scripts` folder, and invoke the helper by relative filename. Use a foreground command and allow at least 20 minutes:

```text
uv run --no-project --python 3.11 python mpt_agent.py --subject "<topic>" --script-file "<utf8-script>" --material "<rights-cleared-master-video>" --font-file "../assets/fonts/NotoSansKR-Bold.ttf" -- --video-source local --video-aspect 9:16 --video-count 1 --video-concat-mode sequential --video-clip-duration 60 --video-transition-mode none --voice-name ko-KR-SunHiNeural-Female --video-language ko-KR --bgm-type none --subtitle-enabled --subtitle-position custom --custom-position 70
```

The helper checks out upstream commit `eb8c23757e098a07bbcd93b3b50e252fc8d1869a` into an isolated Codex runtime, verifies the commit, uses `uv sync --frozen`, forces a final video stage, and prints `MPT_RESULT` only for non-empty MP4 files.

## Korean subtitle recovery

Do not deliver a video when the log says that Edge subtitle aggregation did not
produce a subtitle file. The current pinned upstream can lose Korean boundary
characters around some decimals or acronyms even when the narration audio is
correct.

Use this bounded recovery path:

1. Preserve the original MoneyPrinterTurbo task and audio.
2. Use an explicitly selected, already available Whisper model only to recover
   speech timestamps. Do not silently download a large model.
3. Replace recognition errors with a human-reviewed SRT whose numbers and
   claims match the locked narration and evidence.
4. Burn that SRT into the MoneyPrinterTurbo MP4 with the bundled font:

```text
python burn_subtitles.py --video "<MPT_VIDEO>" --subtitle "<REVIEWED_SRT>" --output "<REPAIRED_MP4>"
```

5. Run `validate_video.py`, full audio/video decode, pronunciation review, and
   representative-frame review again. Record that the final artifact is a
   subtitle-repaired derivative of the same MoneyPrinterTurbo task.

Do not use the upstream Whisper text correction output without review. A
one-to-many sentence mismatch can shift later captions or create zero-length
timestamps.

## Topic-online execution

Run the same helper with `--subject` and the requested video options but without `--script-file` or local materials. If it exits with code 10, ask once for only the fields listed under `MISSING`. Pass supplied values through the documented `MPT_*` environment variables and retry once. Do not store secrets in this Skill repository.

## Verify before delivery

After `MPT_RESULT`, run `validate_video.py` from the same `scripts` working directory:

```text
python validate_video.py --video "<VIDEO_FILE>" --log-file "<LOG_FILE>" --frames-dir "<qa-directory>" --min-duration 45 --max-duration 60
```

Require the requested aspect, a decodable video stream, an audio stream, non-silent narration, readable subtitles, and representative-frame review. For a YouTube Short, default to 1080x1920, H.264, AAC, and 45-60 seconds unless the user specifies another target.

On failure, read only the reported error and relevant log tail. Repair one recoverable issue and retry once. If the final video still fails, return the failed stage, concise error, log path, and any completed script/storyboard; do not call it finished or Shorts-ready.

## Delivery

Return the absolute MP4 path, duration, resolution, codecs, narration language, source mode, verification result, and important content/data limits. State explicitly that social publishing was not performed.
