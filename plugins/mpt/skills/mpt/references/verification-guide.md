# Detailed verification and delivery

Apply the editorial-route table in `../SKILL.md`; investment-only fields do not block a news explanation. Use delivery schema v2 and report formats in `production-source.md`.

## Verification gate

Run the automated gates after final audio and reviewed subtitles exist:

```text
python validate_video.py --video "<final.mp4>" --log-file "<MPT.log>" --frames-dir "<qa/representative>" --duration-profile <focused|full> --report "<video-report.json>"
python probe_scene_frames.py "<final.mp4>" "<scene-manifest.json>" --out-dir "<qa/scene-probe>" --require-audio
python validate_delivery.py "<delivery-status.json>"
```

Require the requested aspect ratio, decodable video and audio, audible narration, H.264/AAC for the default YouTube target, and a full FFmpeg decode. The scene probe must match the declared duration, resolution, frame rate, boundaries, and midpoints and retain every freeze-detection event of at least one second. Unexpected freezes are HOLD. An individually reviewed native source wait or purposeful reading hold can be accepted only through a matching, final-MP4-hash-bound `--freeze-review` record; never add drift to evade detection. See `production-source.md`.

Automated checks do not replace visual review. Inspect at original resolution and at a phone-scale preview:

- 0.0 and 0.2 seconds;
- every scene boundary and both sides of each transition;
- first stable entry, 25%, 50%, 75%, and last stable exit for animated or dense scenes;
- the maximum extent, landing, and reading hold of each selected emphasis cue;
- the smallest chart label, densest caption, brand-heavy scene, and final decodable frame.

Also review the opening and full sequence in motion against the brief: is the tension clear by three seconds, do the shots advance the explanation, does a key number have a comprehensible scale, and is the promised question answered? Contact sheets alone cannot verify rhythm. Review the final mixed audio separately as described above. Record inspected timestamps and concrete evidence for each editorial result; a declared storyboard is not proof that the rendered video follows it.

Replay each selected emphasis cue with sound: the visual landing and any sound accent should reinforce the intended spoken word, preserve its intelligibility, and leave a readable hold. Record this evidence under the existing visual-pacing and audio review results. Treat direction choices as editorial hypotheses; do not claim improved retention without audience data.

For an evidence-motion US-equity Short, `verification.md` must record the following fields. For a news/company explanation with no investment case, verdict/entry/valuation-case fields are `NOT_APPLICABLE` with the route reason. Do not force an investment conclusion. News context uses a separate measured `news-context-report.json` and final-MP4 hash. Investment-analysis keeps the valuation and verdict requirements:

```text
US_STOCK_RESEARCH=PASS|FALLBACK|HOLD
PRIMARY_SOURCE_LOCK=PASS|HOLD
UNUSUAL_WHALES=used|not_relevant|unavailable|conflicted
SP500_MEMBERSHIP=PASS|NOT_APPLICABLE|HOLD
SHAREHOLDER_RETURN_GATE=PASS|NOT_APPLICABLE|HOLD
REPURCHASE_BASIS=actual_gross|actual_plus_dilution_check|authorization_only|NOT_APPLICABLE
DILUTION_CHECK=PASS|NOT_APPLICABLE|HOLD
PAYOUT_COVERAGE_CHECK=PASS|NOT_APPLICABLE|HOLD
INVESTMENT_VERDICT=RECOMMEND|WATCH|AVOID|NOT_APPLICABLE
PRICE_AS_OF=<price, currency, timestamp, timezone>
VALUATION_CASE=<method, denominator, comparison or target>
ENTRY_OR_FAIR_VALUE=<price or range>
VERDICT_INVALIDATION=<one measurable condition>
VERDICT_QA=PASS|HOLD|NOT_APPLICABLE
CLAIM_LEDGER_FREEZE=<ISO-8601 timestamp>
CLAIM_LEDGER_SHA256=<hash>
HOOK_QA=PASS|HOLD
THUMBNAIL_FRAME_QA=PASS|HOLD
THUMBNAIL_FRAME_INTERVAL=<start-end seconds or STANDALONE_ONLY>
THUMBNAIL_EXPORT=<absolute PNG/JPEG path>
THUMBNAIL_RESOLUTION=1080x1920
THUMBNAIL_LOGO_ASSET=<asset ID and rights note>
THUMBNAIL_SENTENCE=<one representative Korean sentence>
THUMBNAIL_CLEAN_LAYOUT_QA=PASS|HOLD
VISUAL_PACING_QA=PASS|HOLD
NUMBER_COMPREHENSION_QA=PASS|HOLD
PERIOD_CONTEXT_QA=PASS|HOLD|NOT_APPLICABLE
CONNECTOR_CLEARANCE_QA=PASS|HOLD|NOT_APPLICABLE
REFERENCE_BREAKDOWN_QA=PASS|HOLD|NOT_APPLICABLE
SILENCE_DENSITY_QA=PASS|HOLD|NOT_APPLICABLE
SEMANTIC_CUT_QA=PASS|HOLD|NOT_APPLICABLE
PRODUCT_ASSET_QA=PASS|FALLBACK|HOLD|NOT_APPLICABLE
SERVICE_IDENTITY_QA=PASS|FALLBACK|HOLD|NOT_APPLICABLE
ACTUAL_MEDIA_QA=PASS|FALLBACK|HOLD|NOT_APPLICABLE
OFFICIAL_VIDEO_SHARE=<official-video union seconds / entire final MP4 seconds; minimum 0.60>
OFFICIAL_VIDEO_QA=PASS|HOLD
OFFICIAL_VIDEO_REPORT=<absolute official-video-report.json path>
NEWS_CONTEXT_SHARE=<news-context union seconds / narrated union seconds; minimum 0.30 when applicable>
NEWS_CONTEXT_QA=PASS|HOLD|NOT_APPLICABLE
NEWS_CONTEXT_REPORT=<absolute news-context-report.json path or NOT_APPLICABLE>
SOUND_PLAN=<track and mix choice, or reason for silence>
AUDIO_LISTENING=PASS|HOLD|NOT_PERFORMED
STRATEGY_ID=<stable experiment identifier>
SERIES=<channel topic series>
TOPIC_HYPOTHESIS=<viewer question and expected value>
HOOK_VARIANT=<candidate identifier>
DURATION_PROFILE=focused|full|custom
UPLOAD_PACKAGE=<absolute JSON/Markdown path>
VIDEO_QA=PASS|HOLD
```

Apply the `PRODUCT_ASSET_QA` meanings in `brand-assets.md`. A documented, visually reviewed fallback may satisfy the asset review, but must remain labeled `FALLBACK` and be disclosed at delivery. Missing investigation is `HOLD`, never `FALLBACK` or `NOT_APPLICABLE`.

Apply `SERVICE_IDENTITY_QA` to every company Short that names a product, platform, segment, or service. `PASS` requires a sourced and recognizable identity asset for each thesis-critical business, visual review at phone size, and at least two distinct identities in a multi-business thesis. A text-only metric card or repeated parent logo is `HOLD` when a usable identity asset was available. A documented editorial pictogram or composite is `FALLBACK`, not `PASS`.

Apply `ACTUAL_MEDIA_QA` from `brand-assets.md` to observable product actions, rankings, events, and real-world subjects. Check the actual rendered excerpt against its concurrent narration, not just the asset filename. Skipped sourcing, mismatched actions, fabricated screenshots, or unreadable proof are `HOLD`; repair them before finished delivery.

Set overall `VIDEO_QA=PASS` only after the technical, visual, editorial, and actual listening checks pass and `validate_delivery.py` accepts the corresponding status artifact. Do not deliver as finished on `HOLD`, `NOT_PERFORMED`, unresolved claim conflict, failed layout, missing audio, empty planned emphasis cues, missing standalone thumbnail, clipped or overlapping text, blank transition frames, unreadable phone-scale labels, deformed logos, an investment-analysis ending without a verdict, or an investment verdict unsupported by a dated price and reproducible evidence. Repair recoverable defects and rerun only the affected gates. If a check cannot be completed, report the failed or unavailable stage and artifact paths as a review draft, without calling it finished or fully verified.

## Delivery

Return the absolute MP4 path and the mandatory absolute thumbnail PNG/JPEG path together, plus duration, video and thumbnail resolution, codecs, narration language and voice, source mode, validation result, data as-of date, primary-source-lock status, Unusual Whales decision, selected title and description package, strategy ID, and material limitations. A video-only delivery is incomplete. State explicitly whether social publishing occurred. Publishing itself remains separately authorized. When the user later supplies Studio data, append same-age 24-hour, 72-hour, and 7-day observations under `references/channel-growth-loop.md`; do not call a single result causal proof.
