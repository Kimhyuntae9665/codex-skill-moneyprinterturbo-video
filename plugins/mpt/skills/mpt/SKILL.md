---
name: moneyprinterturbo-video
description: Create and verify a finished short-form MP4 with MoneyPrinterTurbo. Use for YouTube Shorts, Reels, TikTok, Korean narration, evidence-led finance and US-equity shareholder-return explainers, deterministic data motion, or requests that expect the final video rather than instructions alone.
---

# MoneyPrinterTurbo Video

Make a finished, understandable Korean Short whose visuals show the narrated subject, whose factual claims can be traced to sources, and whose review status is honest. Deliver the MP4 and a separate full-resolution thumbnail. A setup, storyboard or render command alone does not complete a video request. A request to review this skill itself calls for inspection and improvement, not a video render.

## Select purpose before tools

Record two independent choices in `production.json` before sourcing and drafting:

| Field | Choice | Required payoff |
| --- | --- | --- |
| `editorial_route` | `news-explainer` | Explain the requested event, evidence and limits. |
| | `investment-analysis` | Resolve a valuation/investment question with dated price, reproducible valuation, risk, and 추천/관망/비추천. |
| | `general-explainer` | Answer the requested business, product or mechanism question. |
| `source_mode` | `prepared-local` | Reviewed script and rights-cleared local media. |
| | `topic-online` | MPT drafts a script or finds online material; request only `MPT_NEEDS_INPUT` credentials. |
| | `evidence-motion` | Strict prepared-local submode: frozen claims, deterministic charts/layout, one continuous master. Use for financial/data claims and tightly directed motion. |

Also record `content_kind` as `company`, `stock`, `ai`, `technology`, or `general`. Ten-year P/E and an investment verdict are required for listed-company **investment-analysis**. Mentioning a ticker in news or explaining a business does not activate those requirements. Any valuation claim actually made still needs aligned evidence. A mixed episode that argues whether to buy uses investment-analysis. This table governs route scope in all supporting references.

Choose `strategy.duration_profile` before narration: `focused` 25–35 seconds, `full` 45–60, or `custom` with explicit bounds justified by the request and measured speech. Do not pad the story or change bounds afterward merely to pass QA.

## Preserve the user's production choices

- Official source videos must occupy at least **60% of the entire final MP4** by union of eligible output intervals. Natural waits inside a playing original count; editor-added freezes, padding, hidden inserts and irrelevant footage do not. Official publication is not permission to reuse: record the separate source/use basis.
- For company, stock, AI and technology Shorts, nontechnical news/adoption/competition/business context must occupy at least **30% of narrated runtime**. Measure its own interval union, excluding silent covers/end padding. Technical narration over a news image does not qualify. Anchor qualifying spans to the spoken clause onset/end in the approved final narration, split mixed content at the semantic transition, and record each span's point/source/date under `production-source.md`.
- Use actual relevant demonstrations, screens, products and identities. Show the action being spoken, with readable Korean explanation and dated proof. Charts keep true numerical scales; generated visuals do not replace exact text, logos or authentic screenshots.
- Keep the preferred weighty Korean male narration brisk: start at **1.30x the original baseline once**, audition dense numbers, edit unplanned silence, then lock cuts/subtitles/cues to measured speech. Follow later explicit voice/speed instructions.
- Export a native **1080x1920 thumbnail** alongside portrait video. Embed a cover only if it strengthens the spoken hook; no silent cover hold. Preserve proportional sourced marks and one concise Korean thesis.
- Facts, financial definitions, rights, intelligibility and truthful QA are hard requirements. Example scene counts, 2–4-second visual beats, impact effects and title metaphors are editorial tools; adapt them to the story. Do not claim better retention without audience data.

## Load only the needed detail

Read [production-guide.md](references/production-guide.md) for the relevant narrative, visual and audio sections, and [verification-guide.md](references/verification-guide.md) for detailed performed-review evidence and delivery fields. The scope table above applies throughout both guides.

Read only the references required by the selected route:

- On this migrated PC: [references/editorial-production.md](references/editorial-production.md) for source provenance and retained user preferences; apply the detailed production references below.

- On Windows: [references/local-windows.md](references/local-windows.md) for the installed Python runtime and PATH refresh.

- All runs: [references/modes.md](references/modes.md).
- Directed or evidence-led work: [references/evidence-motion-workflow.md](references/evidence-motion-workflow.md), [references/scene-contract.md](references/scene-contract.md), and [references/professional-motion.md](references/professional-motion.md).
- Every portrait video: [references/visual-quality-gate.md](references/visual-quality-gate.md).
- Every narrated Short: [references/editorial-tempo.md](references/editorial-tempo.md) for reference breakdown, TTS silence editing, and semantic cut alignment.
- External AI-video references or a specific material, camera, editing, or sound defect: [references/reference-to-production.md](references/reference-to-production.md) for purpose-based source selection, disclosed-setting limits, and translation into a tested production decision.
- Considering an external image, I2V, TTS, or music generator: [references/generative-component-selection.md](references/generative-component-selection.md) for component-level trials, Korean voice comparison, music briefs, and actual plan/output eligibility.
- Every YouTube Shorts growth or publishing-package request: [references/channel-growth-loop.md](references/channel-growth-loop.md) for audience promise, topic selection, hook experiments, and post-publication learning.
- Every evidence-motion production: [references/production-source.md](references/production-source.md) for the single-source build and truthful delivery-status gate.
- US-listed securities: [references/us-equity-research-gate.md](references/us-equity-research-gate.md).
- Every company or stock Short: [references/company-signature-thesis.md](references/company-signature-thesis.md) for the mandatory X thesis scan and one company-specific, evidence-backed story that viewers can remember.
- Historical valuation, platform scale, active-user, ARPU/ARPP, or network-effect theses: [references/historical-valuation-user-economics.md](references/historical-valuation-user-economics.md).
- S&P 500 membership, dividends, repurchases, dilution, shareholder yield, payout sustainability, or total shareholder return: [references/shareholder-return.md](references/shareholder-return.md), after the US-equity research gate.
- Company relationships, service architecture, partner roles, and workflows: [references/infographic-motion-bridge.md](references/infographic-motion-bridge.md) and the installed `logo-flow-infographics` Skill. Use its logo-first, minimal-text graph style; keep quantitative trends, comparisons, compositions, and 13F figures in scale-accurate deterministic charts.
- Every company Short, before choosing official demo footage, live interface/ranking captures, photographs, marks, or substitutes: [references/brand-assets.md](references/brand-assets.md). Apply its actual-media and service-identity reviews even when the company sells no physical product.
- Every video: [references/official-footage-production.md](references/official-footage-production.md) for the minimum 60% official-video runtime share and the user-approved Muse V2 production method: action-matched excerpts, large authentic identities, measured speech cuts, and phone-size review.
- On a fresh or shared installation, if present: `references/portable-install.md`; run `python scripts/check_environment.py --json` before the first render.

The MCD v8 evidence-motion package is the visual and QA reference. Use its principles - frozen claims, subject-relevant physical metaphors, continuous motion, large Korean text, and boundary-frame inspection - without copying its company-specific content.

## Production sequence

1. Define the intended viewer, immediate question, supported answer and route. Find relevant usable source actions before locking a story that cannot meet the footage quota. Write three hook candidates and preview the chosen first three seconds with the real visual and selected voice.
   For a cold viewer, make the visible subject and concrete consequence understandable before relying on an unfamiliar product name or abbreviation. Inspect the silent first frame as well as the synchronized preview. Keep one dominant proposition: remove a duplicate top/central headline when captions already repeat the hook, and enlarge the actual evidence rather than filling the space with another label. These are comprehension checks, not claims of improved retention.
2. Lock claims and asset/use records before narration/layout. For US-equity claims follow the primary-source research gate; for investment-analysis include historical valuation and the price case. Keep dates, units, calculations and counterevidence. Use X for discovering angles, with a documented fallback when inaccessible.
3. Use one canonical `production.json` under [production-source.md](references/production-source.md). Derive brief, source ledger, narration, scene contract, reviewed captions, emphasis cues and upload package from it. Changing facts or speech invalidates dependent timing and reports. For an existing MP4 edit, follow the revision section in `production-source.md`: preserve the prior version, identify affected passages, reuse valid unchanged inputs, and regenerate reports for the new final file.
4. Generate dry narration, audit silence, measure semantic boundaries, then derive cuts and cues. Validate layout before rendering. Preview the opening, a dense number passage, a representative action excerpt and thumbnail before full production.
5. Render a continuous master, assemble through MPT, and run final QA on the actual last MP4 after all mixing/subtitle edits. Keep source in/out and final output intervals for independent footage/news reports.
6. Perform native-resolution and phone-size visual playback, and actual final-mix listening. Repair recoverable defects and rerun affected checks. If playback/listening is unavailable, preserve useful artifacts as a **review draft** with the missing check; never invent a PASS or claim finished delivery.

## Safety and execution

Keep Upload-Post disabled. Publishing and paid providers require separate explicit authorization. Never expose keys/configuration or credential-bearing logs. Run one MPT job at a time in the foreground, resuming its existing session; do not start a WebUI/API/Docker/posting service for an ordinary request. Use owned/generated/public-domain/license-compatible material; MPT's software license does not cover third-party media.

## Prepared-local execution

Resolve the Skill directory, set the working directory to `scripts`, and call the helper by relative filename. Keep the command in the foreground and allow at least 20 minutes:

```text
uv run --no-project --python 3.11 python mpt_agent.py --subject "<topic>" --script-file "<utf8-script>" --material "<rights-cleared-master-video>" --font-file "../assets/fonts/NotoSansKR-Bold.ttf" -- --video-source local --video-aspect 9:16 --video-count 1 --video-concat-mode sequential --video-clip-duration <clip-budget-seconds> --video-transition-mode none --voice-name <verified-voice> --voice-rate <verified-rate> --video-language ko-KR --bgm-type none --subtitle-enabled --subtitle-position custom --custom-position 70
```

The helper pins MoneyPrinterTurbo commit `eb8c23757e098a07bbcd93b3b50e252fc8d1869a`, uses an isolated runtime and frozen dependencies, forces the final-video stage, disables social upload, and prints `MPT_RESULT` only for non-empty MP4 files.


Choose `clip-budget-seconds` from measured media, not the duration-profile name. For a continuous directed master, use the integer ceiling of the larger of master duration and approved-audio duration plus the pinned backend's 0.1s coverage margin. The master itself must cover that audio margin; increasing a flag cannot create missing source footage. In sequential mode a 60s limit on a 68s master selects only the first 60s. Recheck actual final duration and scene boundaries after assembly.

For **evidence-motion**, preserve the approved dry narration used to time the master. In the command above, pass `--custom-audio-file "<approved-dry-narration.wav>"` and replace `--subtitle-enabled` with `--no-subtitle-enabled`; then burn the reviewed, audio-aligned SRT once with `burn_subtitles.py`. The pinned CLI supports these options and custom audio skips TTS. Do not regenerate speech or apply another 1.30x speed change during final assembly. An ordinary prepared-local job without approved audio may let MPT synthesize narration; its actual resulting audio then controls all final timing. Record the approved-audio hash in the build record and compare the assembled speech timing before final mixing/QA.

The command above produces narration without a music bed. When the audio plan includes BGM, use the pinned runtime's verified local-track options or mix that cleared track into the narrated output afterward. Avoid double-mixing existing audio, preserve synchronization, and run final QA on the actual mixed deliverable.

## Verification commands

Run from this skill's `scripts` directory, after final narration/subtitles/mix exist:

```text
python validate_scene_manifest.py "<scene-manifest.json>" --report "<layout-report.json>"
python validate_video.py --video "<final.mp4>" --log-file "<MPT.log>" --duration-profile <focused|full> --frames-dir "<qa/representative>" --report "<video-report.json>"
python probe_scene_frames.py "<final.mp4>" "<scene-manifest.json>" --out-dir "<qa/scene-probe>" --require-audio
python validate_delivery.py "<delivery-status.json>"
```

For `custom`, pass `--duration-profile custom --min-duration <min> --max-duration <max>` from the recorded bounds. Pass the expected `--width`/`--height` for a nonportrait request. `topic-online` validation requires `--allow-online-log-activity` for its authorized script/search activity; this does not authorize paid usage or publishing.

Use **delivery schema v2** in [production-source.md](references/production-source.md). The validator recomputes union time from official/news intervals, verifies thresholds and final-MP4 hashes, and requires the scene-probe report. A numeric/structural PASS cannot establish licensing, semantic eligibility, visual rhythm or actual listening; those require performed reviews.

Unexpected >=1s freeze events remain HOLD. Inspect each event; a genuine source wait or purposeful reading hold can use `--freeze-review <performed-review.json>` bound to the final MP4 hash and exact detected interval. Retain the raw detection and concrete observation. Do not waive a whole video, hide decoder errors, or add arbitrary motion to evade detection.

Follow [verification-guide.md](references/verification-guide.md) for boundary/emphasis/dense-scene sampling and route-specific fields. `MPT_RESULT` proves a nonempty render exists; only completed technical, factual, visual, listening and delivery gates support finished status.

## Delivery

Return MP4 and thumbnail absolute paths together, duration/resolution/codecs/voice, source mode, data date, relevant research/review results, selected title/upload package, and material limits. Say whether publishing occurred. A missing required check means review draft. For later channel analytics use [channel-growth-loop.md](references/channel-growth-loop.md); compare same-age observations without claiming causality from one result.
