---
name: moneyprinterturbo-video
description: Create and verify a finished short-form MP4 with MoneyPrinterTurbo. Use for YouTube Shorts, Reels, TikTok, Korean narration, evidence-led finance explainers, deterministic data motion, or requests that expect the final video rather than instructions alone.
---

# MoneyPrinterTurbo Video

Produce the finished video, verify it, and return its absolute path. Do not stop at setup, a storyboard, or render commands.

## Route the request

- Use `prepared-local` when the script and rights-cleared local visuals already exist.
- Use `topic-online` when MoneyPrinterTurbo must draft the script or find online footage. Request only credentials named by `MPT_NEEDS_INPUT`.
- Use `evidence-motion` as the strict `prepared-local` submode for financial claims, charts, maps, brand architecture, institutional ownership, or tightly directed motion. Freeze evidence and geometry before rendering, then pass one continuous master MP4 to MoneyPrinterTurbo.

Read only the references required by the selected route:

- All runs: [references/modes.md](references/modes.md).
- Directed or evidence-led work: [references/evidence-motion-workflow.md](references/evidence-motion-workflow.md), [references/scene-contract.md](references/scene-contract.md), and [references/professional-motion.md](references/professional-motion.md).
- Every portrait video: [references/visual-quality-gate.md](references/visual-quality-gate.md).
- US-listed securities: [references/us-equity-research-gate.md](references/us-equity-research-gate.md).
- Trends, comparisons, compositions, processes, or 13F summaries: [references/infographic-motion-bridge.md](references/infographic-motion-bridge.md) and the installed `infographic-creator` Skill.
- Web-sourced company or product marks: [references/brand-assets.md](references/brand-assets.md).
- On a fresh or shared installation, if present: `references/portable-install.md`; run `python scripts/check_environment.py --json` before the first render.

The MCD v8 evidence-motion package is the visual and QA reference. Use its principles - frozen claims, subject-relevant physical metaphors, continuous motion, large Korean text, and boundary-frame inspection - without copying its company-specific content.

## Narrative and retention contract

For valuation and finance Shorts, default to the **Disconnect** story: show a visible mismatch, explain what causes it, test the counterargument, and finish with a conditional decision rule.

1. **Hook, 0-3 seconds:** Begin with a counter-intuitive dated fact, a high-stakes question, or a valuation disconnect. Pair it with an immediate visual change. Never open with a greeting, company history, or boilerplate.
2. **Primary evidence, roughly 4-20 seconds:** Use one or two decisive SEC/IR metrics. Explain why they matter rather than reading a list.
3. **Bull-versus-bear conflict, roughly 21-45 seconds:** Put the attractive evidence and its strongest risk into the same story. Treat the company as a question to resolve, not a collection of cards.
4. **Decision and risk gate, roughly 46-60 seconds:** State the price, metric, or operating condition that would strengthen or invalidate the thesis. Never finish with an unconditional recommendation.

Use `setup -> conflict -> resolution` even when the exact timing differs. A financial script should feel like a strategic mystery: "Why is this cash-generating company still priced this way?" is stronger than a sequence of unrelated ratios.

Keep two language layers aligned:

- On-screen metrics use the exact filing or market-data vocabulary and frozen value, such as `AFFO/share $2.46`, `FCF $4.2B`, or `YoY +18%`. Preserve English abbreviations when they are the precise financial identifier; add a short Korean label when it improves comprehension.
- Korean narration translates the meaning into plain language without changing the definition, period, or unit. Do not replace a precise metric with a looser synonym that overstates cash, profit, ownership, or return.

Every number in narration, subtitles, graphics, and source lines must resolve to the same claim ID and display value.

## US equity research gate

For every US-equity Short, enforce this dependency chain before production:

```text
us-stock-research -> SEC and issuer-IR primary-source lock -> Unusual Whales secondary check -> claim-ledger freeze -> video production
```

This is a gate, not a suggestion:

1. Invoke `us-stock-research` and define ticker, legal issuer, CIK, as-of date, price basis, valuation denominator, comparison method, thesis, counterpoint, and unresolved questions.
2. Lock fundamentals, guidance, dividends, repurchases, share counts, and 13F rows to SEC EDGAR or issuer IR. Record period end, filed date, document URL, raw value, calculation path, rounding, and limitation.
3. Record the Unusual Whales decision as `used`, `not_relevant`, `unavailable`, or `conflicted`. It is a dated market-context check, not primary evidence for fundamentals, valuation denominators, dividends, buybacks, or institutional ownership.
4. Align timestamp, timezone, adjusted-price basis, unit, fiscal period, and definition before resolving conflicts. SEC or issuer IR controls reported company facts. Never average conflicting values; omit unresolved claims.
5. Freeze the ledger before narration or layout. Production may simplify density but may not mutate claim meaning.

For 13F, show manager, issuer/security, quarter end, filing date, and shares or reported value. State that 13F is delayed, long-only disclosure - not a current trade, cost basis, or proof of present ownership.

## Visual and motion contract

### Pace with meaning

- No scene or static infographic may remain visually unchanged for more than four seconds. Add a distinct state change - line reveal, bar growth, number count, label entrance, relevant cut, or restrained camera move - tied to the narration's emphasis word.
- A state change must explain the argument. Do not use unrelated wipes, glows, coins, machinery, or random 3D objects merely to keep pixels moving.
- Let exact text and values settle before the reading hold. Keep text stationary while the viewer must read it.
- Use kinetic typography only for the active verb and core metric, such as `SOLD $4.2B` or `DIVIDEND 70Y`. Do not animate an entire paragraph as one block.
- Use subject-relevant physical metaphors: property and rent flow for a REIT, stores and royalties for a franchise, products and repeat purchase for staples. Generated plates contain scenery only; exact text, numbers, maps, charts, and logos remain deterministic layers.

### Map data to the right visual

- Valuation or peer rank: horizontal ranked bar or a scale-accurate custom chart.
- Revenue, cash flow, or shareholder return: waterfall, Sankey, or causal flow.
- Target or decision price: valuation target ladder with current, watch, and invalidation states.
- Historical trend: line chart with a single direct endpoint callout.
- Two-sided thesis: binary comparison with one deciding metric.
- Compact 13F view: disclosure date first, then two or three readable manager rows.

Use at most two ratios per scene. If an AntV template cannot preserve scale, labels, or readability after one simplification pass, switch to a deterministic custom chart and record why.

### Fill the portrait frame deliberately

- Start from the large type scale in `visual-quality-gate.md`. Shorten or split copy before shrinking it.
- When revising a small-text draft, enlarge ordinary visible copy by about 20% and the smallest chart or card labels by about 40%, then reflow the layout.
- Make meaningful content occupy roughly 60-85% of the central content zone. A large white card containing a tiny diagram is a failed composition even if the card fills the canvas.
- Crop intrinsic white or transparent margins from imported SVG/PNG assets before scaling. Use available space to enlarge the chart, property, product, map, or comparison - not to add decoration.
- Keep title, qualifier, metric, source, and caption in separate readable regions. Fail on clipping, collisions, weak contrast, caption intrusion, logo deformation, blank flashes, diagonal transition bars, or leftover underlines.
- Prefer three to six officially sourced brand marks plus large product/category labels over generic icons when brand recognition is part of the thesis. If provenance or rights are unclear, use verified names as text and omit the mark.

### Direct online footage precisely

In `topic-online`, specify the subject, emotional tone, shot scale, and camera movement for each clip - for example, `investigative slow push-in on a casino exterior at blue hour` or `fast hyper-lapse of city traffic`. Reject generic business meetings, handshake footage, and unrelated skyscrapers unless they directly support the narration.

## Audio and narration contract

- Choose a voice that matches the topic. For Korean finance, prefer a calm, weighty delivery over an excited sales tone. Verify the selected voice name before rendering.
- Use `--voice-rate` deliberately. A normal explainer is usually near `0.9-1.0`; a requested slow, weighty delivery can use `0.7-0.8`, followed by an actual listening check. Do not assume the numeric rate alone produces the intended tone.
- Insert short spoken pauses before decisive frozen metrics using punctuation or the selected TTS engine's verified pause mechanism. Do not pass unsupported raw SSML such as `<break>` into Edge TTS.
- Keep BGM off by default. If the user explicitly chooses a rights-cleared track, define its mood and lower it by at least 30% during dense numerical narration. Recheck speech intelligibility after the mix.
- Pronunciation-check ticker symbols, acronyms, decimals, currencies, dates, and large numbers. Rewrite phonetic narration when needed while preserving the on-screen metric.

## Safety contract

- Do not publish to YouTube, TikTok, Instagram, or another service unless the user separately requests publishing. The helper must keep Upload-Post disabled.
- Do not use Seedance, WaveSpeed, LoomLoom, Sonilo, or another paid provider without explicit confirmation of the charge.
- Do not expose credentials, `config.toml`, environment values, or full credential-bearing logs.
- Use only owned, generated, public-domain, or license-compatible assets. The upstream MIT license does not cover third-party fonts, music, photos, stock media, or trademarks.
- Run one video job at a time. Do not start the WebUI, API server, Docker service, or cross-posting service for an ordinary request.

## Prepared-local execution

Resolve the Skill directory, set the working directory to `scripts`, and call the helper by relative filename. Keep the command in the foreground and allow at least 20 minutes:

```text
uv run --no-project --python 3.11 python mpt_agent.py --subject "<topic>" --script-file "<utf8-script>" --material "<rights-cleared-master-video>" --font-file "../assets/fonts/NotoSansKR-Bold.ttf" -- --video-source local --video-aspect 9:16 --video-count 1 --video-concat-mode sequential --video-clip-duration 60 --video-transition-mode none --voice-name <verified-voice> --voice-rate <verified-rate> --video-language ko-KR --bgm-type none --subtitle-enabled --subtitle-position custom --custom-position 70
```

The helper pins MoneyPrinterTurbo commit `eb8c23757e098a07bbcd93b3b50e252fc8d1869a`, uses an isolated runtime and frozen dependencies, forces the final-video stage, disables social upload, and prints `MPT_RESULT` only for non-empty MP4 files.

## Evidence-motion production

Do not begin the renderer with unfrozen claims.

1. Create `brief.md`, `sources.md`, a dated claim ledger, `narration.ko.txt`, and a reviewed `subtitle.srt`.
2. Classify each data scene as `infographic`, `custom_chart`, or `non_chart`. Give `infographic-creator` only frozen claim rows; save its DSL, pinned AntV SVG, preview, version, and hashes.
3. Copy `assets/templates/shorts-scene-contract-v1.json`. Declare scene boundaries, safe zones, element boxes, containment, claim IDs, assets, text roles, logical font sizes, and purposeful state changes.
4. Validate geometry before render:

```text
python validate_scene_manifest.py "<scene-manifest.json>" --report "<layout-report.json>"
```

5. Render one continuous 1080x1920, 30 fps master. Keep the platform-caption band quiet. Disable MoneyPrinterTurbo transitions and set clip duration at least as long as the narration.
6. Generate narration and final assembly through MoneyPrinterTurbo. Preserve the task log and output paths.
7. If Edge subtitle aggregation fails, preserve the MoneyPrinterTurbo audio, use an already available Whisper model only for timestamps, replace its text with the human-reviewed SRT, and burn it with `burn_subtitles.py`. Do not use unreviewed speech recognition as final financial copy.

## Verification gate

Run the automated gates after final audio and reviewed subtitles exist:

```text
python validate_video.py --video "<final.mp4>" --log-file "<MPT.log>" --frames-dir "<qa/representative>" --min-duration 45 --max-duration 60
python probe_scene_frames.py "<final.mp4>" "<scene-manifest.json>" --out-dir "<qa/scene-probe>" --require-audio
```

Require the requested aspect ratio, decodable video and audio, audible narration, H.264/AAC for the default YouTube target, and a full FFmpeg decode. The scene probe must match the declared duration, resolution, frame rate, boundaries, and midpoints and report no freeze of at least one second.

Automated checks do not replace visual review. Inspect at original resolution and at a phone-scale preview:

- 0.0 and 0.2 seconds;
- every scene boundary and both sides of each transition;
- first stable entry, 25%, 50%, 75%, and last stable exit for animated or dense scenes;
- the smallest chart label, densest caption, brand-heavy scene, and final decodable frame.

For an evidence-motion US-equity Short, `verification.md` must record:

```text
US_STOCK_RESEARCH=PASS|FALLBACK|HOLD
PRIMARY_SOURCE_LOCK=PASS|HOLD
UNUSUAL_WHALES=used|not_relevant|unavailable|conflicted
CLAIM_LEDGER_FREEZE=<ISO-8601 timestamp>
CLAIM_LEDGER_SHA256=<hash>
VIDEO_QA=PASS|HOLD
```

Do not deliver on `HOLD`, unresolved claim conflict, failed layout, missing audio, clipped or overlapping text, blank transition frames, unreadable phone-scale labels, deformed logos, or an unconditional investment end card. Repair one recoverable issue and rerun the affected gates. If it still fails, report the failed stage and artifact paths without calling it finished.

## Delivery

Return the absolute MP4 path, duration, resolution, codecs, narration language and voice, source mode, validation result, data as-of date, primary-source-lock status, Unusual Whales decision, and material limitations. State explicitly whether social publishing occurred.
