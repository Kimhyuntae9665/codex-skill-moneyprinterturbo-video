# Single-source production and delivery status

Use one canonical `production.json` for every evidence-motion run. Claims, spoken segments, assets, voice settings, duration profile, emphasis events, thumbnail text, and strategy metadata originate there. Derived files may add measured timing and render geometry, but they may not silently replace the canonical text, value, unit, source, or settings.

## Required source sections

```json
{
  "schema_version": "mpt-production-v1",
  "project_id": "ticker-date-topic",
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

For a listed-company Short, `historical_pe` is required. Every observation, statistic, current-position statement, N/M gap, and adjusted-current marker must resolve to frozen claim IDs. The renderer must consume this same object for the chart; do not maintain a second hand-entered P/E array in the drawing code.

Cache signatures include the segment text, provider, voice, rate, pitch or style controls, pronunciation dictionary/version, audio format, and synthesis implementation version. Never key an audio cache only by text and rate.

## Emphasis events

An emphasis event records ID, segment ID, claim ID when factual, spoken phrase, measured landing time, visual action, sound action, peak extent, and reading-hold end. A planned visual or sound accent with no measured landing time is incomplete. If the brief plans emphasis but the produced cue list is empty, delivery is HOLD.

## Delivery status

Create `delivery-status.json` after rendering. It is the machine-readable aggregate of the actual run, not a restatement of the plan. Use absolute artifact paths and link the generated reports.

Include `official_video_share` (numeric fraction), `official_video_qa` (`PASS|HOLD`), and `artifacts.official_video_report` (absolute path). Missing measurement, unreviewed eligibility, or a measured share below `0.60` blocks finished delivery even when technical validation passes. `validate_delivery.py` checks the recorded threshold and the referenced report's PASS flag; actual source provenance and visual eligibility remain performed reviews.

```json
{
  "schema_version": "mpt-delivery-status-v1",
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
    "official_video_report": "absolute path"
  },
  "reviews": {
    "audio": {"reviewer": "human or assistant playback", "observations": ["concrete observation"]},
    "visual": {"timestamps_s": [0, 1.0], "observations": ["concrete observation"]}
  }
}
```

`PASS` is allowed only for performed checks. `NOT_PERFORMED`, missing fields, empty observations, failed referenced JSON reports, nonexistent artifacts, or fewer actual cues than planned block finished delivery. Technical media validation never substitutes for audio listening, visual motion review, or claim review.
