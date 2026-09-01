# Portrait-video visual quality gate

Use this gate for every 9:16 Short. It addresses four recurring delivery
failures: tiny text, generic product tiles, unexplained blank panels, and
animation states that are clipped even though a midpoint frame looks clean.

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

If products, brand breadth, or recurring household demand are part of the
argument, a generic category icon is only a fallback.

1. Verify the parent-company relationship on an official portfolio, annual
   report, investor-relations page, or official brand page.
2. Apply `brand-assets.md` and obtain the official-served mark when its bounded
   contextual use is supportable.
3. Pair each mark with a large product or brand name and a plain-language
   category. Use three to six items; more usually forces the labels too small.
4. Preserve aspect ratio and clear space. Put the exact logo in a deterministic
   layer, never in a generative image or video prompt.
5. If rights or provenance are unclear, show the verified name as text and omit
   the logo. Never invent a logo or fake product packaging.

## 4. Review progressive animation states

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

- text, chart, logo, card, map, or building cut by the canvas or its parent;
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
