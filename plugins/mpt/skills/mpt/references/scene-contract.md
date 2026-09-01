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

Use `parent_id` when a label or asset is intentionally contained by a card,
building, chart, or other element. The parent rectangle must fully contain the
child. Use `allow_overlap_with` only for intentional sibling intersections.

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

## Claims and assets

`claims` is the canonical display-value ledger. A claim should include
`display`, `value`, `unit`, `as_of`, `source_url`, and `definition`. Every claim
ID attached to a scene or element must exist in the ledger.

`assets` records an ID, type, origin or generation method, and rights note.
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
