# Infographic-to-motion bridge

Use this bridge when a Short contains an information-rich chart, comparison,
composition, process, hierarchy, or ownership summary. It connects the
installed `infographic-creator` Skill to the evidence-motion renderer without
weakening the claim ledger or scene contract.

## Routing rule

After the claim ledger is frozen, classify every data scene:

- `infographic`: editorial trend, ranked comparison, binary comparison,
  composition, sequence, process, hierarchy, or compact 13F summary;
- `custom_chart`: multi-series finance chart, candlestick, drawdown panel,
  confidence band, dense axis work, or any plot whose meaning depends on exact
  scale control not supported by the available AntV Infographic templates;
- `non_chart`: brand architecture, product, store, map, physical metaphor,
  transition, or end card.

Use `infographic-creator` by default for the first class. Do not force a dense
financial plot into a decorative template merely to claim Skill usage.

## Frozen-data handoff

Give `infographic-creator` only the rows needed for one scene:

- claim IDs and exact display labels;
- values, units, period order, and comparison labels;
- one Korean title and, only when necessary, one short description;
- the scene's signal, comparison, neutral, and background colors;
- the intended logical content box.

Do not ask it to research, round, reinterpret, or update values. Preserve the
language of the finished Korean Short. Pure numeric series may omit icons;
semantic comparisons and process items should use restrained, relevant icons.

Save the returned plain DSL as `assets/infographics/<scene-id>.infographic`.
Wrap it in an HTML renderer pinned to `@antv/infographic@0.2.20`, export SVG,
and save a full-resolution PNG preview for visual QA. Record the package
version, DSL path, SVG path, source claim IDs, and file hashes in the asset
manifest. The video renderer consumes the exported SVG or local raster, not a
live CDN page.

## Template mapping

- one ordered time series: `chart-line-plain-text`;
- one ranked numeric comparison: `chart-bar-plain-text` or
  `chart-column-simple`;
- shareholder-return or revenue composition: `chart-pie-donut-plain-text` or
  `chart-pie-donut-pill-badge`;
- two-sided valuation or risk comparison:
  `compare-binary-horizontal-simple-fold` or
  `compare-binary-horizontal-badge-card-arrow`;
- research or decision sequence: `sequence-*`;
- company cash-flow or business-model relationship: `relation-*`;
- compact manager/holding hierarchy: `hierarchy-*` only when the labels remain
  readable in the vertical content zone.

Do not use a pie chart when parts do not share one denominator. Do not use a
line chart for unordered categories. Keep time-series labels in chronological
order.

## Shorts layout rules

- Treat the infographic as one parent asset inside the scene content zone.
- Keep the header, source strip, and platform-caption zone outside its box.
- Target at most one headline, one chart, one direct takeaway, and one source
  line per scene.
- Before sizing the parent asset, crop the exported SVG or raster to its actual
  content bounds. Remove uniform white or transparent export margins and record
  the crop. Scale the meaningful infographic, not its empty export canvas.
- When the infographic is the only main visual, let its meaningful bounds fill
  about 75-90% of the usable panel width and 55-80% of its usable height. Do not
  nest a small full-page infographic screenshot inside another oversized card.
- Prefer 3-6 visible categories or 4-8 time points. If more are necessary,
  reveal them across multiple scenes or use a custom chart.
- Use Korean fonts with verified glyph coverage and tabular numerals.
- Keep small labels at a size that remains readable after 1080x1920 export and
  phone-scale playback; shorten copy before reducing font size.
- Preserve quiet negative space. Remove template decorations, redundant
  legends, duplicate titles, and unrelated icons.

## Motion integration

The static infographic defines composition; the deterministic renderer defines
time. Use motion to explain the comparison:

- line: clip-path draw followed by one endpoint callout;
- bar or column: baseline-to-value growth in comparison order;
- donut: restrained sweep followed by direct labels;
- binary comparison: alternate-side reveal, then highlight the deciding metric;
- sequence or relation: activate nodes and connectors in causal order;
- 13F summary: reveal the disclosure date before manager names and holdings.

Keep exact labels stationary during their reading hold. Add gentle parallax or
camera drift only after the main chart settles. Avoid continuous bouncing,
glows, confetti, generic coins, and decorative motion unrelated to the claim.

## QA and fallback

Before importing an infographic asset, inspect the SVG and the full-resolution
preview for Korean glyphs, clipping, overlap, contrast, axis/order correctness,
and exact agreement with the frozen ledger. Declare the infographic parent box
and every externally animated label/callout in `scene-manifest.json`.

If the chosen template cannot pass the content box or readability gate after
one simplification and content-crop pass, switch that scene to `custom_chart`.
Record the reason in `verification.md`; do not shrink text until it becomes
technically present but visually useless.
