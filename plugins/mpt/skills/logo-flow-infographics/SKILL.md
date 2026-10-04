---
name: logo-flow-infographics
description: Create or revise compact logo-first flow diagrams with a dark dotted canvas, rounded logo cards, curved arrows, and only short technology names beneath each logo. Use for minimal-text architecture or workflow infographics in this style, including source SVG and PNG output.
---

# Logo Flow Infographics

## Visual contract
- Use a restrained dark dotted canvas, white rounded cards, clear spacing, thin gray curved directed connectors, and a short accurate name directly below each logo
- Keep technology names only: no function paragraphs, feature lists, decorative dashboards or oversized headings. Put a necessary test/proposal disclaimer outside the graph
- Preserve logo proportions, artwork and brand colors. Fit rather than stretch. Label an Ollama mark Ollama, not Llama
- Preserve the user's existing topology and approved composition during label-only edits

## Build from a verified graph
1. Derive nodes, edges and branch meaning from the user's flow or inspected project sources. Logos alone are not integration evidence. Mark synthetic/proposed graphs explicitly; do not imply deployment
2. Use provided or approved local logo assets. Record source, revision/hash and license/trademark notes. Do not silently fetch assets, install software, authenticate or publish. Bundled example glyphs are original synthetic shapes
3. Keep editable source. For a compact left-to-right static graph, use the Python helper and [input contract](references/input-contract.md). For complex routing or an interactive canvas, use the selected editor/engine while preserving the style and semantics
4. Produce SVG, then PNG with an already available renderer. The helper uses installed Inkscape and performs no network access or installation. If PNG tooling is missing, report that specific limit and preserve SVG
5. Inspect actual pixels: correct marks/names, no broken images or clipping, readable labels, visible arrowheads, connected branches and no edge through a card. File existence or renderer exit 0 is insufficient
6. Deliver the image with an accurate brief caption and retain SVG plus manifest for edits. Approval to edit a diagram does not authorize unrelated publication or account changes

## Local helper
Use Python 3.9+ (standard library). Run from the skill directory, writing artifacts outside the installed skill:
~~~bash
python3 scripts/render_logo_flow.py assets/example-graph.json --svg /absolute/output/flow.svg --png /absolute/output/flow.png
~~~
The example uses fictional names and original glyphs only. Replace its graph and manifest with requested content; its branches are not a real architecture.

Read [export checks](references/export-checks.md) for portable SVG or another renderer. External-image SVGs with 1em intrinsic dimensions can work in a browser yet fail in a rasterizer. The helper embeds local assets and sets explicit intrinsic dimensions while retaining viewBox ratio and geometry.

Retain a short SVG title and an adjacent text description of relationships for accessibility. Hover labels and brand recognition alone do not communicate branch meaning. Keep that description outside the minimal visual composition.
