---
name: moneyprinterturbo-video
description: Create and verify a finished short-form MP4 with MoneyPrinterTurbo from a topic or prepared script. Use for YouTube Shorts, Reels, TikTok, Korean narration, evidence-led US-stock and finance explainers, SEC and issuer-IR sourced claims, AntV infographic chart scenes, deterministic data motion, local visual materials, stock-footage generation, MoneyPrinterTurbo setup or repair, and requests that expect the final video file rather than instructions alone.
---

# MoneyPrinterTurbo Video

Produce the finished video, verify it, and return its path. Do not stop at setup or commands.

## Choose the mode

- Use `prepared-local` when a complete script and rights-cleared local images or videos are available. This mode avoids LLM and stock-provider credentials. It still needs network access for the pinned upstream checkout, dependencies, and Edge TTS.
- Use `topic-online` when MoneyPrinterTurbo must write the script or find online footage. Request only credentials reported by `MPT_NEEDS_INPUT`.
- Use `evidence-motion` as a stricter `prepared-local` submode when the Short contains financial claims, charts, maps, brand architecture, or tightly arranged motion. Freeze a claim ledger and executable scene contract before rendering, then use one directed master MP4 as the local material.
- If factual or time-sensitive claims appear in the video, verify them with primary sources before freezing the script. Keep facts, interpretation, and unresolved limits distinct.

Read [references/modes.md](references/modes.md) for exact input, credential, and recovery rules. For premium charts, finance explainers, or directed motion, read [references/evidence-motion-workflow.md](references/evidence-motion-workflow.md) and [references/scene-contract.md](references/scene-contract.md); then use [references/professional-motion.md](references/professional-motion.md) as the visual-direction checklist. For a US-listed company, ticker, ETF, valuation claim, dividend claim, buyback claim, or institutional-holdings claim, also read and follow [references/us-equity-research-gate.md](references/us-equity-research-gate.md) before writing narration. When the frozen storyboard contains a trend, composition, ranked comparison, binary comparison, process, or institutional-holdings scene, invoke the installed `infographic-creator` Skill and follow [references/infographic-motion-bridge.md](references/infographic-motion-bridge.md). The MCD v8 package under [examples/mcd-valuation-2026](examples/mcd-valuation-2026/) is the golden reference for claim-ledger discipline, contextual brand geometry, continuous motion, reviewed Korean captions, and boundary-frame QA. The older static-card example remains under [examples/mcd-2025](examples/mcd-2025/).

When a real company logo or other web-sourced brand mark would materially improve identification, read [references/brand-assets.md](references/brand-assets.md) before downloading or rendering it. For every portrait video, also read and enforce [references/visual-quality-gate.md](references/visual-quality-gate.md). It defines the mobile type scale, meaningful content-fill rules, product/brand portfolio treatment, and progressive-frame review required to prevent tiny text, unexplained white voids, clipped motion, and transition remnants.

For a fresh machine, shared ZIP, or GitHub installation, read [references/portable-install.md](references/portable-install.md) and run `python scripts/check_environment.py --json` before the first render. For a US-equity request, rerun it with `--mode us-equity` and record unavailable companion Skills or connectors instead of silently assuming they exist.

## US equity research gate

For any US-equity Short, enforce this dependency chain before production:

```text
us-stock-research -> SEC and issuer-IR primary-source lock -> Unusual Whales secondary check -> claim-ledger freeze -> video production
```

This is a gate, not a suggested order:

1. Invoke and follow the installed `us-stock-research` Skill to define the ticker, CIK, as-of date, valuation basis, price basis, comparison set, and unresolved questions.
2. Lock every fundamental, guidance, dividend, repurchase, share-count, and 13F claim to SEC EDGAR or the issuer's investor-relations material. Save the filing form, period end, filed date, accession or document URL, and calculation path. Use the latest source only when it measures the same period and definition needed by the claim.
3. Perform an explicit Unusual Whales decision: `used`, `not_relevant`, `unavailable`, or `conflicted`. Use it only for dated market-price, stock-chart, implied-move, market-map, or market-tide context supported by the available tool. It is not final evidence for company fundamentals, valuation denominators, dividend history, buybacks, or 13F ownership.
4. Resolve conflicts before freezing. SEC or issuer IR controls reported company facts. Never average conflicting values. If differences remain after aligning period, timestamp, adjusted-price basis, and definition, mark the claim unresolved and omit it from narration and graphics.
5. Freeze the claim ledger only after steps 1-4 pass. Narration, subtitles, chart labels, map labels, source lines, and end-card language must consume the frozen display values and claim IDs.

Do not skip this gate merely because a market-data number looks plausible. If a required Skill or connector is unavailable, record the fallback and limitation in `verification.md`; complete the SEC/IR primary-source lock independently or place the production on HOLD.

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

## Evidence-motion execution

Do not begin the renderer with an unfrozen script. Complete these gates in order:

For a US-equity Short, complete the entire US equity research gate first. Its locked evidence packet becomes the input to step 1 below; the renderer must never trigger fresh research or silently substitute newer numbers.

1. Create a dated claim ledger with display value, raw value, unit, as-of date, source URL, calculation definition, caveat, evidence tier, verification status, and secondary-check status for every on-screen fact.
2. Freeze narration and reviewed SRT from the same claim IDs.
3. Mark each data scene as `infographic`, `custom_chart`, or `non_chart`. Use `infographic` by default for editorial trends, comparisons, compositions, sequences, and ownership summaries. Invoke `infographic-creator` only with frozen claim-ledger rows, save its DSL, render a pinned AntV SVG, and inspect the SVG or a full-resolution raster preview before motion work.
4. Copy `assets/templates/shorts-scene-contract-v1.json`, replace its example content, and declare every scene boundary, safe zone, element box, parent-child relation, claim ID, infographic asset ID, intended state change, visible text role, and logical font size. New manifests must keep the template's role-based minimum type checks enabled.
5. Run the manifest gate before rendering:

```text
python validate_scene_manifest.py "<scene-manifest.json>" --report "<layout-report.json>"
```

6. Render one continuous 1080x1920, 30 fps master. Animate approved infographic SVGs with deterministic masks, line reveals, bar growth, number counters, or restrained camera movement. Never ask a generative image or video model to render exact numbers, Korean copy, charts, logos, or maps. Put those in deterministic SVG/vector/Pillow/Canvas/Manim/Motion Canvas layers.
7. Pass only that master to MoneyPrinterTurbo in `prepared-local` mode. Keep transitions off and make the clip duration at least as long as the narration.
8. After final audio and reviewed subtitles are present, run both the ordinary video validator and the scene probe:

```text
python validate_video.py --video "<final.mp4>" --log-file "<MPT.log>" --frames-dir "<qa/representative>" --min-duration 45 --max-duration 60
python probe_scene_frames.py "<final.mp4>" "<scene-manifest.json>" --out-dir "<qa/scene-probe>" --require-audio
```

The scene probe must extract every boundary and midpoint, build a contact sheet, match the declared resolution, frame rate, and duration, and report no freeze of at least one second. Automated success does not replace original-resolution review of the generated contact sheet.

For every animated, brand-heavy, chart-heavy, or previously rejected scene, also extract the first stable frame after entry, quarter points, and the last stable frame before exit. Review those frames at original resolution. A clean midpoint does not excuse a clipped entry state, off-canvas wipe, white flash, diagonal transition bar, or late caption collision.

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

When dense financial graphics and burned captions coexist, reserve a visibly
quiet caption band in the master itself. Keep all essential chart labels,
sources, and transition remnants above that boundary, then inspect every scene
boundary and each dense two-line caption at original resolution.

Apply the mobile visual quality gate before delivery:

- Start new 1080x1920 scenes from the large type scale in `visual-quality-gate.md`; never shrink essential copy to preserve an oversized card or unused whitespace. If a user has already rejected a draft for small text, enlarge ordinary visible copy by about 20% and the smallest chart/card labels by about 40%, then shorten and reflow the layout.
- Use meaningful content to occupy the central safe area. A large empty white panel is a layout defect unless it clearly serves the argument. Enlarge the primary chart, product, building, map, or comparison; add direct labels or a sourced brand/product grid; or remove the empty container. Do not fill space with unrelated glow, machinery, coins, or decorative clutter.
- Judge space inside the panel separately from space around it. A large card containing a tiny centered diagram fails even when the card itself fills the frame. Crop intrinsic white or transparent margins from imported SVG or PNG assets, then scale the meaningful chart or illustration to use most of the panel width and height. Keep generous padding between text blocks, but do not achieve that padding by shrinking the entire composition.
- Do not pack a title, qualifier, number, and icon into one narrow rectangle when the scene has unused space. Widen or heighten the card, separate the label and metric into distinct rows, and use the empty area before reducing font size. Text bounding boxes must not touch, visually merge, or compete for the same baseline.
- When a consumer-company portfolio is part of the thesis, prefer three to six recognizable, officially sourced product-brand marks plus plain-language product categories over generic category icons. If rights or provenance are unclear, use product and brand names as text instead of fabricating a logo.
- Fail the visual review for clipped or off-canvas elements, overlapping text/cards, unreadable contrast, deformed or missing logos, unexplained central blank space, or any transition remnant visible at entry, settled, or exit frames.

For `evidence-motion`, do not deliver unless all of the following are true:

- for a US-equity Short, the research packet records the `us-stock-research` pass, SEC/IR lock, and explicit Unusual Whales decision before the claim-ledger freeze timestamp;
- every company fundamental, dividend, buyback, valuation denominator, and 13F claim is anchored to SEC or issuer IR rather than a secondary market-data screen;
- every infographic DSL value and visible SVG label matches its frozen claim ID, and the exported asset contains no clipped Korean text, template placeholder, or unplanned legend;
- the claim ledger and narration agree character-for-character on all displayed numbers;
- `validate_scene_manifest.py` reports zero errors;
- the final MP4 passes `validate_video.py` and a full audio/video decode;
- `probe_scene_frames.py` extracts every planned boundary and midpoint and reports no prohibited freeze;
- a human review confirms no clipped Korean text, card collision, chart/label overlap, caption intrusion, accidental logo deformation, or transition remnant;
- a human review confirms essential text meets the large mobile type scale, the settled composition uses its central content area purposefully, and relevant consumer-product scenes use verified names or official marks rather than generic placeholders;
- the end card states the decision rule or limitation instead of an unqualified recommendation.

On failure, read only the reported error and relevant log tail. Repair one recoverable issue and retry once. If the final video still fails, return the failed stage, concise error, log path, and any completed script/storyboard; do not call it finished or Shorts-ready.

## Delivery

Return the absolute MP4 path, duration, resolution, codecs, narration language, source mode, verification result, data as-of date, primary-source lock status, Unusual Whales decision, and important content/data limits. State explicitly that social publishing was not performed.
