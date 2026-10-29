# Scene contract

The scene contract is a JSON file that makes layout and timeline assumptions
machine-checkable. Copy `assets/templates/shorts-scene-contract-v1.json` and
replace the example values.

## Coordinate model

`canvas.logical` defines the coordinate system used by every rectangle.
`canvas.output` defines the encoded MP4 dimensions. A rectangle is
`[x, y, width, height]`.

`reserved_bboxes` are mutually exclusive presentation regions.
`safe_bboxes` are the smaller regions in which content may be placed. A zone
may be nested in another through `zone_parents`, for example a source strip
inside the lower edge of content.

Recommended 720x1280 logical zones:

```json
{
  "header": [0, 0, 720, 236],
  "content": [48, 250, 624, 750],
  "source": [48, 930, 624, 50],
  "caption_platform": [0, 1000, 720, 240]
}
```

Keep the remaining bottom area visually quiet for platform chrome. Adapt the
boxes only when the platform target changes, then review them at the actual
export resolution.

## Elements

Every fixed or scene element requires:

- `id`: unique within the evaluated scene;
- `zone`: a declared zone;
- `kind`: `text`, `caption`, `source`, `card`, `chart`, `asset`, `brand_asset`,
  `shape`, or another descriptive kind;
- `bbox`: logical rectangle.

Text-like elements also need `text`, `lines`, `max_lines`, `text_role`, and
`font_px` when the template's mobile-readability checks are enabled. Keep
`require_font_px`, `require_text_role`, and `min_font_px_by_role` enabled for
new portrait-video manifests. `font_px` is measured in the logical canvas, not
the encoded output. The validator checks declared role minima, geometry, and
line counts; final rendered glyph fit still needs original-resolution visual
review.

For every point-to-point percentage or amount change, include a visible text
element for the start date, end date, and elapsed period in the primary visual.
Attach the same claim ID used by the change metric and record the exact basis or
population, such as `전체 공시 주식 수`. A source-strip date alone is
insufficient.

Use `parent_id` when a label or asset is intentionally contained by a card,
building, chart, or other element. The parent rectangle must fully contain the
child. Use `allow_overlap_with` only for intentional sibling intersections.

Represent arrows and connector lines as `shape` elements with a bounding box
covering the full line, animated path, stroke, and arrowhead. Their boxes must
not overlap text or numeric-value boxes unless the overlap is semantically
necessary and explicitly reviewed. Do not use `allow_overlap_with` to excuse a
connector hidden behind a label. Inspect the peak and settled rendered frames,
because the static contract box cannot prove that an animated arrowhead remains
clear throughout its path.

## Timeline and motion

`timeline.boundaries_s` must begin at zero, increase strictly, and end at
`canvas.duration_s`. The number of scenes must be one fewer than the number of
boundaries. Each scene's start and end must match the corresponding boundaries.

For new portrait-video manifests, declare `primary_visual_bbox` on every scene.
It represents the union of the meaningful chart, illustration, cards, and
direct labels after intrinsic asset whitespace is removed. Keep
`require_primary_visual_bbox` enabled and use the template's minimum width and
height ratios. This checks the scale of the actual composition rather than the
outer background panel.

Each state change declares an element or state ID, absolute `at_s`, `from`,
`to`, and a descriptive motion name. The timestamp must fall inside its scene.
The contract does not prescribe a renderer; it preserves intent across Pillow,
Manim, Motion Canvas, Three.js, Blender, or another deterministic tool.

### Thumbnail cold-open scene

Embedding is optional. For a standalone-only thumbnail, record `STANDALONE_ONLY` and do not add a cover scene or silent hold. When an embedded cover is selected because it strengthens the spoken hook, represent it as an ordinary
first scene or the first stable state of the hook scene; do not invent schema
fields that the validator cannot check. Its stable interval begins at 0.0
seconds and lasts at least 0.5 seconds. Declare the logo or mark as a
`brand_asset`, the company/ticker identifier and short positioning line as text
elements, and their actual displayed boxes in the normal scene contract.

The very first encoded frame must already be fully composed. Do not rely on a
fade-in, pre-roll, or blank frame to reach the thumbnail state. The spoken hook
should begin at 0.0 seconds or immediately afterward, and the unanswered hook
must still be complete by 3.0 seconds measured from the start of the file.

Record the exact stable-frame interval and separately exported full-resolution
PNG/JPEG path in `brief.md` and `verification.md`. Probe the first frame, a frame
near 0.2 seconds, the last stable cover frame, and both sides of the transition.
Review the exported still at full resolution and phone size for legibility,
proportional logo rendering, clipping, and misleading endorsement cues. The
positioning line remains subject to the frozen claim ledger and fact-strength
ceiling; asset geometry validation does not establish factual accuracy or logo
rights.

### Selected emphasis cues

For each emphasis cue chosen under the Skill's direction contract, keep a row
in `brief.md` with the scene/element ID, claim ID when applicable, spoken
phrase and emphasis word, actual audio timestamp, visual entrance and landing
times, reading hold, and optional sound accent. The approved audio determines
the timing; revise cues after any narration edit.

Represent the element's entrance and settled state with the existing state
change fields. Describe the scale or highlight behavior, duration, and pivot
clearly enough for the renderer to implement it. A manifest entry alone does
not animate pixels or mix sound: implement and preview the corresponding
renderer and audio actions. Keep these production notes in the brief rather
than inventing JSON fields and assuming the validator checks them.

Allow a brief scale-down stamp or a contrasting highlight on selected core
metrics; there is no mandatory 150% scale. Leave supporting text, sources,
and chart axes stable, and preserve proportional data marks. Calculate the
maximum transformed text bounds around the chosen pivot and check safe zones,
card containment, captions, and adjacent labels at that extent. Split long
KRW labels or reduce the entrance scale before shrinking readable type.

Review the rendered peak, landing, and full reading hold at phone size, then
replay with audio to check the spoken emphasis and any sound accent together.
Record actual timestamps and findings in `verification.md`. Static declared
boxes do not establish transformed glyph fit, and geometry validation does
not establish audiovisual timing or expressive delivery.

## Claims and assets

`claims` is the canonical display-value ledger. A claim should include
`display`, `value`, `unit`, `as_of`, `source_url`, and `definition`. Every claim
ID attached to a scene or element must exist in the ledger.

`assets` records an ID, type, origin or generation method, and rights note.
Include real location backgrounds in this asset record and link their source,
use terms, depicted place, and known date in `sources.md`. Keep the scene-to-asset
mapping, focal crop, camera movement, and shading plan in `brief.md`; these are
rendering instructions and visual-review items, not new automatic validator
checks. A full-canvas background does not enlarge `primary_visual_bbox` unless
the depicted subject itself is the meaningful primary visual.
For a product photo, packshot, or mark, link its asset ID to the source/terms
record in `sources.md` and the scene where it appears. Keep any fallback reason
and candidate-search record there as well, following `brand-assets.md`. Use
the existing geometry fields for its displayed bounds; inspect the actual
packaging and product/brand match in rendered frames. Do not invent schema
fields and assume they implement the editorial `PRODUCT_ASSET_QA` gate.

Brand marks are contextual identifiers, not decorative endorsements. The
contract cannot grant trademark, photo, music, model-output, or dataset rights.

## Commands

From this Skill's `scripts` directory:

```text
python validate_scene_manifest.py "<manifest.json>" --report "<layout-report.json>"
python probe_scene_frames.py "<final.mp4>" "<manifest.json>" --out-dir "<frame-probe>" --require-audio
```

Both commands print JSON and exit nonzero on required-check failure. Keep the
reports beside the verification note. Do not edit a report to force a pass;
edit the source manifest or renderer and rerun it.
