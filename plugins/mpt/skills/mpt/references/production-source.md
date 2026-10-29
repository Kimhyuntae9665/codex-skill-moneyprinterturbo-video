# Single-source production and delivery status

Use one canonical `production.json` for every evidence-motion run. Claims, spoken segments, assets, voice settings, duration profile, emphasis events, thumbnail text, and strategy metadata originate there. Derived files may add measured timing and render geometry, but they may not silently replace the canonical text, value, unit, source, or settings.

## Required source sections

```json
{
  "schema_version": "mpt-production-v1",
  "project_id": "ticker-date-topic",
  "editorial_route": "investment-analysis",
  "content_kind": "stock",
  "source_mode": "evidence-motion",
  "strategy": {
    "strategy_id": "series-episode-hypothesis",
    "series": "series name",
    "viewer_question": "one question",
    "topic_hypothesis": "why this is useful now",
    "hook_variant": "H1",
    "duration_profile": "focused"
  },
  "research": {"as_of": "ISO-8601", "ledger_sha256": "sha256"},
  "historical_pe": {
    "basis": "trailing GAAP P/E",
    "window": "ten completed years plus current",
    "sampling_rule": "year-end plus dated current",
    "price_convention": "split-adjusted",
    "observations": [],
    "median": 0,
    "mean": 0,
    "minimum": 0,
    "maximum": 0,
    "current": 0,
    "current_rank_or_percentile": "ledger-backed position",
    "distortion_treatment": "none, N/M gaps, or separately labeled adjusted marker"
  },
  "voice": {"provider": "provider", "name": "voice", "rate": 1.30, "pronunciation_version": "v1"},
  "segments": [],
  "assets": {},
  "emphasis_events": [],
  "thumbnail": {},
  "upload_package": {}
}
```

Each segment carries a stable ID, final spoken text, caption text, claim IDs, intended visual, and optional emphasis-event IDs. The final edited narration supplies measured starts and ends. Scene boundaries, SRT cues, effect landings, and renderer inputs are regenerated from those measurements. A change to text, voice, rate, pronunciation rules, or silence policy invalidates all dependent timings.

Plan official-video use in the canonical segments, then derive `official-video-report.json` from the final output timeline and actual playback review. Each eligible interval records scene/asset ID, official publisher, source page/media URL, source in/out, output start/end, narration/action match, and review evidence. Follow `official-footage-production.md`: calculate union duration divided by the entire final MP4 duration and require at least `0.60`. Natural reading/waiting inside the playing official original counts; self-made animation and editor-added frozen tails do not. Recalculate after any cut, hold, padding, or timing revision.

For a listed-company investment-analysis Short, `historical_pe` is required. For news-explainer/general-explainer without a valuation case, omit that object and record the route reason; do not force a chart or recommendation. Every observation, statistic, current-position statement, N/M gap, and adjusted-current marker must resolve to frozen claim IDs. The renderer must consume this same object for the chart; do not maintain a second hand-entered P/E array in the drawing code.

Cache signatures include the segment text, provider, voice, rate, pitch or style controls, pronunciation dictionary/version, audio format, and synthesis implementation version. Never key an audio cache only by text and rate.

Record the actual skill-file hashes/version, pinned MPT commit and renderer version or hash in the build record beside `production.json`. Link the final video ID and strategy ID when the user later provides publication data. Do not invent the build version of an older channel upload.

## Emphasis events

An emphasis event records ID, segment ID, claim ID when factual, spoken phrase, measured landing time, visual action, sound action, peak extent, and reading-hold end. A planned visual or sound accent with no measured landing time is incomplete. If the brief plans emphasis but the produced cue list is empty, delivery is HOLD.

## Delivery status

Create `delivery-status.json` after rendering. It is the machine-readable aggregate of the actual run, not a restatement of the plan. Use absolute artifact paths and link the generated reports.

Include `official_video_share` (numeric fraction), `official_video_qa` (`PASS|HOLD`), and `artifacts.official_video_report` (absolute path). Missing measurement, unreviewed eligibility, or a measured share below `0.60` blocks finished delivery even when technical validation passes. `validate_delivery.py` checks the recorded threshold and the referenced report's PASS flag; actual source provenance and visual eligibility remain performed reviews.

```json
{
  "schema_version": "mpt-delivery-status-v2",
  "editorial_route": "investment-analysis",
  "content_kind": "stock",
  "news_context_qa": "PASS",
  "verdict_qa": "PASS",
  "video_qa": "PASS",
  "audio_listening": "PASS",
  "visual_review": "PASS",
  "claim_lock": "PASS",
  "layout_qa": "PASS",
  "semantic_cut_qa": "PASS",
  "thumbnail_qa": "PASS",
  "official_video_share": 0.60,
  "official_video_qa": "PASS",
  "emphasis_plan_count": 2,
  "emphasis_cue_count": 2,
  "artifacts": {
    "video": "absolute path",
    "thumbnail": "absolute path",
    "production": "absolute path",
    "scene_manifest": "absolute path",
    "layout_report": "absolute path",
    "video_report": "absolute path",
    "upload_package": "absolute path",
    "official_video_report": "absolute path",
    "news_context_report": "absolute path",
    "scene_probe_report": "absolute path"
  },
  "reviews": {
    "audio": {"reviewer": "human or assistant playback", "observations": ["concrete observation"]},
    "visual": {"reviewer": "actual reviewer", "timestamps_s": [0, 1.0], "observations": ["concrete observation"]}
  }
}
```

`PASS` is allowed only for performed checks. `NOT_PERFORMED`, missing fields, empty observations, failed referenced JSON reports, nonexistent artifacts, or fewer actual cues than planned block finished delivery. Technical media validation never substitutes for audio listening, visual motion review, or claim review.

## Measured reports for delivery v2

V2 rejects old V1 status files until their evidence is migrated; do not relabel a V1 report as V2. It requires the actual scene-probe report, identifies the reviewer, rejects boolean cue counts and out-of-range review timestamps, and binds technical/editorial reports to the **final MP4 SHA-256**. Any later video edit invalidates these reports. Hash agreement associates reports with bytes; it does not prove a review was performed.

`video-report.json` is produced with `validate_video.py --report`; it contains measured `duration`, `duration_profile` and `video_sha256`. Use the canonical `strategy.duration_profile`; `custom` also records `strategy.duration_bounds_s: [minimum, maximum]`. `scene-probe-report.json` is generated by `probe_scene_frames.py` and includes the same final hash. Include its absolute path even if no unexpected freeze is found.

`official-video-report.json` retains its existing fields and intervals from `official-footage-production.md`. Add `video_sha256`. The delivery validator recomputes union seconds from `output_start_s`/`output_end_s`, compares `duration_s` with the measured video report, and checks `official_video_s` and `official_video_share`. Empty intervals, double-counted overlap, out-of-bounds or nonfinite times, missing source in/out or performed eligibility evidence, and <0.60 are HOLD. Natural waits count only while the eligible original plays. Do not count a reading-hold exception as official playback unless it is genuinely in the source.

For `content_kind` company/stock/ai/technology, create `news-context-report.json` separately:

```json
{
  "pass": true,
  "video_sha256": "actual final MP4 hash",
  "duration_s": 50.0,
  "narrated_intervals": [{"start_s": 0.0, "end_s": 48.0}],
  "narrated_s": 48.0,
  "intervals": [{
    "start_s": 0.0, "end_s": 15.0,
    "spoken_point": "the actual nontechnical news/business point",
    "source_url": "primary-source URL", "source_date": "YYYY-MM-DD",
    "review_evidence": "who inspected which final passage and what qualified"
  }],
  "news_context_s": 15.0,
  "news_context_share": 0.3125
}
```

The example illustrates arithmetic, not a real production. Narrated intervals come from final edited speech timing and exclude silent covers/end padding. Classify the corresponding canonical segments as news_context/technical/other; split mixed narration at the semantic boundary. The validator independently merges overlaps, requires news intervals to stay inside narrated intervals, recomputes both seconds and fraction, and requires >=0.30. A general subject may omit the report; a company subject cannot claim that exemption by changing only the delivery status, since route/content_kind must agree with production.json. Numbers cannot verify that the narration really explains news; review the actual passages and preserve observations.

`investment-analysis` additionally needs performed `verdict_qa: PASS`, with the price/valuation evidence under the detailed production contract. Other routes set verdict fields NOT_APPLICABLE in verification and answer their requested question. All routes retain source, footage, thumbnail and actual listening/visual requirements.

## Review individual freeze events

Run the probe once and inspect its raw events. Unexpected or unreviewed >=1s freezes remain HOLD. If an observed event is a purposeful reading hold or a wait present in the original source, record the **exact detected interval** and a real observation in a separate file:

```json
{
  "video_sha256": "actual final MP4 hash",
  "intervals": [{
    "start_s": 10.0, "end_s": 12.0,
    "kind": "source_native_wait", "asset_id": "official-demo-1",
    "reviewer": "actual reviewer",
    "reason": "source UI waits for approval while the narration explains it",
    "evidence": "source 42-44s and final 10-12s replayed; no editor-added freeze"
  }]
}
```

Use `--freeze-review <file>` for the affected probe rerun. `reading_hold` is the other allowed kind. Each row must match one detector event within 0.05s at both ends; a whole-video waiver, stale hash, absent reviewer/evidence, unmatched row, decoder failure or unclosed event cannot pass. Raw detector results remain in the report alongside adjudicated observations. The script checks association/structure, not the truth of a human or assistant observation. Do not fabricate a review when playback is unavailable.

## Revise an existing video

Start from the actual prior `production.json`, approved audio/SRT, scene manifest, renderer and MP4. Preserve their hashes and the requested edit in a change record. Keep old reports as evidence and mark them stale; do not delete failures or rerender from an unrelated draft. An existing MP4 alone does not supply editable scenes or word timing: inspect what is available and disclose missing sources before claiming an exact revision.

Change the intended canonical segment first. Reuse unchanged source claims, assets and audio segments when their provenance, date scope and settings still apply. A text-only graphic correction does not require a new TTS call. If spoken text changes, synthesize/edit the affected passage using the same verified voice/settings, review its joins, assemble the approved narration and measure it again. Changed durations invalidate that passage and downstream cuts, subtitle cues, emphasis landings and interval counts; keep an unchanged prefix only after checking its join/boundary. Update all affected derived files from the canonical content.

Reassemble with the exact approved audio, then regenerate reports bound to the new final-MP4 hash: decode/metadata, scene probe, official/news interval unions and any individual freeze reviews. Recheck edited passages, joins and shifted boundaries; final playback/listening and delivery status must describe the actual new output. Old file-bound reports cannot pass a new file even when much of its content is reused. Re-run unchanged financial calculations only if their inputs, definitions or required as-of date changed; do not invent a fresh research check.
