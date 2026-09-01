# Web-sourced brand assets

Use a real company logo only when it materially improves identification in an informational Short. A logo is not generic decoration, and an official download does not automatically grant an open license.

## Source gate

Use this source order:

1. official newsroom or media-kit download;
2. asset served by the official company website;
3. a third-party repository only when its license and trademark warning are explicit.

Download the original file from its source page. Do not copy a search-result thumbnail, screenshot a logo, trace it, or ask a generative model to redraw it.

For every downloaded mark, record:

- asset ID and intended on-screen purpose;
- official source-page URL and direct asset URL;
- publisher, retrieval date, file type, dimensions, and SHA-256;
- stated license or terms, including when no open license is stated;
- the bounded use rationale and every modification performed.

If the terms or intended use remain unclear, use the company name or ticker in plain text instead.

## Rendering contract

- Use the mark only as a contextual identifier for reporting, analysis, criticism, or explanation; do not imply sponsorship or endorsement.
- Preserve the supplied aspect ratio, colors, lettering, and internal geometry. Cropping transparent padding and proportional scaling are allowed; recoloring, warping, tracing, and generative animation are not.
- Composite the original asset in a deterministic layer after generated imagery. Keep exact marks out of generative-video prompts.
- Give the logo a quiet container or enough contrast and clear space. Keep it outside charts, source lines, and the platform-caption lane.
- Avoid dominant full-screen logo treatment unless the company identity itself is the subject. Never use the mark for merchandise, impersonation, or a fake official channel.
- Inspect the opening, densest frame, scene boundaries, and final frame at full resolution for clipping, deformation, halo artifacts, or unintended overlap.

Add the logo to the scene manifest asset ledger with its provenance and rights note. A final report should state that the mark is a contextual identifier and that social publishing was not performed unless separately authorized.

## Consumer-product portfolio scenes

When the company's brands or repeated-use products are part of the investment thesis, do not default to generic icons such as an unlabeled razor, diaper, detergent bottle, or toothbrush.

- Choose three to six representative brands that are explicitly connected to the company by an official portfolio, annual-report, or brand page.
- Show the unmodified official mark together with a large plain-language category label, such as `Gillette · 면도기`, `Pampers · 기저귀`, or `Tide · 세탁세제`. The logo identifies the brand; the adjacent text explains the product.
- Use a consistent grid or sequence with equal visual weight, generous internal padding, and enough contrast for every mark. Do not let packaging, decorative shapes, or a transition layer cover the mark or category.
- Prefer the actual official mark when it materially improves recognition and the bounded contextual use is supportable. When provenance or terms are insufficient, keep the product and brand names as deterministic text and omit the logo.
- Inspect entry, settled, and exit frames. A missing, cropped, stretched, low-contrast, or partially covered mark fails the scene even when the midpoint looks correct.
