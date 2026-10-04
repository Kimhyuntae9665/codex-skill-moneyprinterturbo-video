# Portrait-video visual quality gate

Use this gate for every 9:16 Short. It addresses four recurring delivery
failures: tiny text, generic product tiles, unexplained blank panels, and
animation states that are clipped even though a midpoint frame looks clean.

For every portrait video, also apply the mandatory official-video gate in
`../SKILL.md`: official source excerpts must occupy at least 60% of the entire
final MP4 runtime. Require `official-video-report.json` and
`OFFICIAL_VIDEO_QA=PASS`. Natural reading/waiting inside the playing original
counts; photos/screenshots, self-made animation, generative or unofficial video,
and editor-added freeze/loop padding do not. Review main-subject prominence,
action/narration match, and readable context using `official-footage-production.md`.
This share is independent of text size, news context, and technical freeze detection.

## 1. Start from a large mobile type scale

The values below are minimum starting points, not targets to shrink toward.
They assume a 720x1280 logical canvas rendered to 1080x1920.

| Text role | Logical px | Output px | Typical use |
|---|---:|---:|---|
| `headline` | 36 | 54 | scene title or main claim |
| `key_metric` | 46 | 69 | price, yield, ranking, decision value |
| `body` | 26 | 39 | short explanatory sentence |
| `product_name` | 28 | 42 | Tide, Pampers, Gillette, Oral-B |
| `product_category` | 20 | 30 | 세탁세제, 기저귀, 면도기, 전동칫솔 |
| `caption` | 36 | 54 | burned Korean narration caption |
| `eyebrow` | 18 | 27 | short section label |
| `utility` | 16 | 24 | date or compact header metadata |
| `source` | 14 | 21 | provenance line only; never a core claim |

Keep essential text to one or two lines. Shorten the sentence, split the scene,
or simplify the chart before reducing the type. Sources may be smaller because
they are provenance, but every number or qualifier needed to understand the
claim belongs in a larger role.

When revising a draft that the user rejected for small text, use the rejected
render as the baseline: enlarge ordinary visible copy by about 20% and the
smallest chart, axis, legend, or card labels by about 40%. Reflow cards and
labels after scaling. Do not simply enlarge text until it clips.

## 2. Use the content area purposefully

Whitespace is useful only when it improves hierarchy. An oversized white card
with tiny content floating in its center is not intentional whitespace.

- At the settled frame, aim for meaningful visuals and labels to occupy roughly
  60-85% of the central content zone. Treat this as a composition diagnostic,
  not a reason to crowd the frame.
- When one large panel owns the scene, the meaningful visual group inside that
  panel should normally span at least 75% of its usable width and 55% of its
  usable height after the panel title, source, and metric chip are excluded. A
  panel that fills the canvas does not pass when its actual diagram occupies a
  small island in the middle.
- If a large central region remains empty, first enlarge the primary chart,
  product, building, map, or comparison. Then add direct labels, a sourced
  product-brand grid, or a concise explanatory callout if it adds information.
- Remove a large white container when it contributes no grouping or contrast.
- Keep at least 24 logical pixels of internal padding around large text and
  brand marks. Preserve the platform-caption lane and outer safe zones.
- Crop transparent padding and uniform white margins from imported SVG, PNG,
  chart, or infographic assets before scaling. Record the crop in the asset
  manifest. Do not center an uncropped export inside another large white card.
- Use at least 18 logical pixels between separate text bounding boxes and at
  least 24 logical pixels between a label block and a key metric. Give cards
  more width or height when the frame has room; never compress multiple labels,
  numbers, and icons into one narrow row merely to keep a preset grid.
- In two-column comparisons, let each side use roughly 44-47% of the available
  width with a clear center gap. Put the label, value, and qualifier on separate
  rows when one line feels crowded. The reader should perceive two spacious
  arguments, not several text fragments colliding inside two boxes.
- Never fill empty space with unrelated glows, generic machinery, decorative
  coins, random 3D objects, or motion that does not explain the narration.

## 3. Prefer recognizable product and brand evidence

For product actions, rankings, announcements, and service use, apply the
official-footage/actual-screen workflow in `brand-assets.md`. The real clip or
capture should own the relevant scene: inspect the stated action, app identity,
rank, country/category/date, and visible result at phone size. A large logo or
generic machine does not substitute for an available demonstration. Record
`ACTUAL_MEDIA_QA` from the rendered video, including any justified fallback.

If products, brand breadth, or recurring household demand are part of the
argument, authentic product photos or official packshots are the default. A
generic category icon is a documented fallback, not a shortcut around sourcing.

1. Verify the parent-company relationship on an official portfolio, annual
   report, investor-relations page, or official brand page.
2. Apply the source search and use-terms review in `brand-assets.md` before
   choosing substitutes. Save selected and rejected candidates in `sources.md`.
   An unchecked assumption about copyright does not justify generic shapes.
3. Pair a recognizable real product image with a large brand/product name and
   plain-language category. A logo alone is secondary when physical products
   are the subject. Reduce item count before making packages too small.
4. Preserve package appearance, aspect ratio, clear space, and source-required
   notices. Composite authentic assets as deterministic layers; never invent
   logos, packaging, or product variants through drawing or generation.
5. Review a representative product scene before full rendering and actual final
   entry, reading-hold, and exit frames at phone size. Check product identity,
   brand/category match, package visibility, edge quality, and label contrast.
6. Record `PRODUCT_ASSET_QA` using `brand-assets.md`. Unexplained generic cans,
   bags, or bottles beneath real brand names fail this gate. A researched or
   explicitly requested fallback must still be reviewed and disclosed.

## 4. Review progressive animation states

For place-oriented scenes, review the real-photo background preference in `../SKILL.md`
before full rendering and again in the final frames. Official-demo and actual-screen
scenes instead prioritize the source material itself and its readable action/context.
For photographic scenes, at phone size, confirm that
the location remains recognizable behind the information, shading preserves
useful photographic detail, and text stays legible as the crop moves. Inspect
the brightest and busiest background positions as well as the midpoint. Record
the inspected timestamps and any justified clean-chart or sourcing exception
under the existing visual review. A nominal photo layer hidden by panels or
darkening does not satisfy the preference. Camera movement alone does not pass
the sequence review in section 5.

For every animated, chart-heavy, brand-heavy, or previously failed scene,
extract and inspect at original resolution:

- the exact scene boundary;
- the first stable frame after the entrance begins;
- approximately 25%, 50%, and 75% through the scene;
- the last stable frame before exit;
- the next scene boundary.

Use a contact sheet for scanning, then open suspicious frames individually.
Check the full portrait edges, safe zones, header, source strip, and caption
lane. Confirm that every product mark, chart label, large number, and Korean
line is readable at every intended settled state.

Also inspect a phone-scale preview near 360x640. If the main illustration looks
small or the hierarchy collapses at that size, enlarge and reflow it even when
the original-resolution pixels are technically legible.

The scene fails if any sampled frame contains:

- text, chart, logo, card, map, or a required identifying subject unintentionally
  cut by the canvas or its parent; deliberate background-photo crops are allowed
  when the planned focal subject remains recognizable;
- overlapping labels, cards, captions, or product marks;
- text swallowed by the background or rendered too small for a phone;
- a blank white flash, off-canvas wipe, diagonal transition bar, debug guide,
  placeholder, accidental underline, or other transition remnant;
- a missing, stretched, recolored, partially covered, or duplicated logo;
- a large unexplained central blank panel that makes the composition look
  unfinished.

Record the inspected timestamps, contact-sheet path, defects found, repairs,
and final pass/fail result in the verification note. Automated OCR, saliency,
blank-frame, or object-detection checks may assist, but they do not replace the
original-resolution visual review.

## 5. Review the sequence, not only sampled frames

Apply the hook and explanatory-beat rules in `../SKILL.md` to a real-time
phone-scale preview. Check the actual first three seconds, then the whole
sequence against the shot plan. Record when the viewer sees a new relationship,
comparison, or consequence. Background pan/zoom and changing text alone do not
demonstrate dynamic pacing, even if freeze detection passes. Confirm that the
opening's promised question receives a supported answer. If playback is
unavailable, record the limitation; still frames cannot establish rhythm.
