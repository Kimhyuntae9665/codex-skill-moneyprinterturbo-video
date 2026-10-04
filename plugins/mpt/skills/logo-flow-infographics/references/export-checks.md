# Export checks

A controlled 2026-09-30 test used four Lobe SVG assets at 329f378cbd1a88f45b60cd096b9111ce16f3ea39 with 1em dimensions and 24×24 viewBoxes. Embedded as SVG data-URI images, Inkscape 1.4 exited 0 yet produced broken-image placeholders. Explicit 24px dimensions recovered the marks but blurred at 64px display size; explicit 256px dimensions rendered sharply with unchanged viewBox, paths and colors. This is one renderer/test result, not a universal guarantee. Those brand assets are not bundled.

- Set adequate intrinsic dimensions without changing viewBox proportions; inspect final export size. Native vector children can avoid intrinsic rasterization, but prefix IDs per instance when inlining gradients or clips
- Treat imported SVG as untrusted. Inspect external hrefs, scripts/events, foreignObject and unwanted metadata. Keep assets pinned/local and embed approved resources
- Preserve gradients, clipping, colors and needed descriptions. Do not rely on OS adaptive light/dark export colors
- Verify Korean glyphs and fonts. SVG text depends on recipient fonts unless separately addressed; PNG does not
- Inspect real output pixels. Renderer exit 0 alone is insufficient
- Keep source and asset manifest. Claim an editing round-trip only after actually reopening and editing the export
- Embedded source/all-pages export may include hidden information; inspect before sharing

The helper is a local static SVG authoring aid, not a workflow runtime, browser controller, installer, draw.io authoring tool or deployment system.

A later non-square fixture showed that this Inkscape path did not preserve a 2:1 mark inside a square image box from preserveAspectRatio alone. The helper therefore computes both fitted width and height from the viewBox and centers the actual image rectangle. Test wide and tall marks as well as square ones.
