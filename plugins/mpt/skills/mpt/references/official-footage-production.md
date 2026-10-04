# Official-video production method

Use for every video. The user approved the Muse V2 method and clarified the quota
on 2026-10-01: **official-video use time / entire final MP4 runtime >= 60%**.
This replaces the earlier continuous-moving-visual minimum of 50%.

## Count source use, not pixel motion

Qualifying assets are attributable official source videos from the relevant
issuer, product maker, institution, newsroom, media resource, or official channel.
Use excerpts that support the concurrent sentence and keep a documented use basis.
The source must remain a main readable visual, with necessary action/context intact.

Count its full actual playback interval, including natural UI reading, approval
waiting, or quiet moments already present in the source. Do not restrict the
numerator to moving pixels. Exclude editor-added freezes, screenshot extractions,
source-end padding, hidden/tiny inserts, and loops inserted solely to fill time.
Photos, ranking captures, self-made logo flows/charts, generated video, and
unofficial footage may be useful supplements but contribute zero to this quota.
Preserve technical freeze reports separately; this source-use measure does not
convert a failed motion/technical check into PASS.

Merge overlapping qualifying output intervals, sum their union length, and divide
by the entire final MP4 duration, including cover, reading holds, and silent padding.
Require at least 0.60. For 48 seconds this means 28.8 seconds; for 60 seconds, 36.
Do not count clips twice when two play concurrently. Missing footage requires
more relevant sourcing or shorter static sections, not artificial padding.

## Build the story around the source actions

1. Choose one viewer question and one supported answer. Start the spoken hook
   immediately over real action; make the complete question clear within three
   seconds. A company name/title or silent thumbnail alone is not an opening.
2. Find official action clips before locking the script. Keep a candidate table
   with narration beat, publisher, URL, source in/out, visible setup/action/result,
   context, crop, and use basis. Watch the candidate rather than choosing by title.
   Plan at least 60% source use before committing to a full render.
3. Give viewers a short role map early when the topic involves multiple companies.
   Use `logo-flow-infographics` for verified relationships and branching choices;
   original service identities and short names explain who does what. Preserve
   independent alternatives rather than inventing a serial partnership chain.
4. Pair each action sentence with the matching clip: selection with product
   selection, approval with approval, checkout with the actual checkout step.
   Explain a company's strategy in one plain sentence tied to that action.
   Use source-backed charts instead when the narration's proof is quantitative.
5. After the evidence, state material support conditions and the strongest
   counterpoint. Distinguish announcements, actual availability, and measured
   revenue. End by answering the opening question, following the selected
   editorial route; do not insert an investment verdict into a news explainer.

The useful sequence is question/action -> role map -> company action and strategy
-> conditions/counterevidence -> answer. Adapt it to the subject. Muse's exact
eleven scenes, companies, 48.43 seconds, dates, and facts are not a universal template.

## Compose and time the footage

- Use a consistent top identity/short heading, central official excerpt, and lower
  two-line Korean explanation/source arrangement. Keep footage the main subject.
  For native 1080x1920, use the existing readable type contract (normally 54px
  captions/headlines). Keep essential text steady while reading; avoid paragraphs.
- Use large proportional original logos/marks when the identity matters. Respect
  supplied geometry/use terms, retain whole artwork when extraction is restricted,
  and document a text-identifier fallback. A large identity supports recognition;
  it does not itself show product behavior or count toward official-video time.
- Crop around the action while preserving the relevant brand, approval button,
  payment choice, result, and supporting context. Contain/stack the crop if filling
  the portrait would lose a crucial detail. Keep translations and commentary
  outside the original source content where possible.
- Generate approved narration, measure the edited audio, then derive scene cuts,
  captions, and emphasis timestamps. Around 3–6 seconds per explanatory beat is
  useful when the action fits, not a fixed cut schedule. Preserve setup and result.
  Keep source playback at 1x unless a justified speed change is clearly disclosed;
  apply the existing 1.30 narration rate once, independently of source-video speed.
- Mute source narration/music under the Korean voice by default. A narration-only
  mix is an appropriate deliberate choice for dense product evidence; background
  music is optional under the sound plan, not a requirement for perceived quality.

## Review and replace weak cuts

Watch a representative synchronized clip and opening before full render. Review
the final at native resolution and phone size: actual action, setup/result,
caption obstruction, source context, brand readability, and entry/exit joins.
If a selected source passage is weak or static despite the action being available
elsewhere, choose the clearer source interval. Do not merely pan the source image.
The Muse V2 Shopify revision used a real recommendation-to-payment scroll for this
reason; retain the selection principle rather than those exact in/out times.

When condition text falls over a bright UI, add a compact dark/translucent backing
in a quiet region, then inspect the actual output. Preserve approval and payment
buttons. Label general-service or historical comparison clips in narration and
on screen so they cannot imply a current transaction or unrelated product demo.
Run technical checks and separately perform real audio listening when available;
record unavailable/failed gates truthfully. GPU encoding supports export speed
and output quality; it does not replace sourcing, editorial decisions, or review.

## Report the measured share

Create `official-video-report.json` from the final measured timeline. Include
`duration_s`, `official_video_s`, `official_video_share`, `minimum_share: 0.60`,
`pass`, and `intervals`. Each interval records `scene_id`, `asset_id`,
`official_publisher`, `source_page_url`, `source_media_url`, `source_in_s`,
`source_out_s`, `output_start_s`, `output_end_s`, `narration_match`, and
`review_evidence`. Preserve source hashes and use basis in the asset ledger.
Set `pass: true` only when the measured share is >=0.60 and eligibility was reviewed.
Recalculate after edits; metadata or a plan alone cannot establish eligibility.

Mirror the fraction as `official_video_share` and the review as
`official_video_qa: PASS|HOLD` in delivery status, and link the absolute report
under `artifacts.official_video_report`. Record `OFFICIAL_VIDEO_SHARE`,
`OFFICIAL_VIDEO_QA`, and `OFFICIAL_VIDEO_REPORT` in verification. The independent
news-context requirement remains at least 30% of narrated runtime.
