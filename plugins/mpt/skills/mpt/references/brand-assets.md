# Official footage, real screens, product photographs, and brand assets

Actively seek authentic media that shows the concurrent spoken claim: official product demonstrations and real interfaces for actions, dated screen captures for rankings/events, and authentic photographs or packshots for physical products/places. Use a company logo when it materially improves identification. An official download does not automatically grant an open license, but uncertainty alone is not a reason to skip sourcing and draw generic substitutes.

## Official footage and actual-screen workflow

Before locking the storyboard, look for the relevant company newsroom/media kit, product page, official channel, service interface, ranking page, or announcement. Choose useful material throughout the story rather than satisfying the preference with one decorative insert. Watch the candidate excerpt or inspect the actual page; a thumbnail or page title does not establish what a clip demonstrates.

| Narration purpose | Preferred evidence on screen | Context to retain |
| --- | --- | --- |
| What the product actually does | Official demonstration or authorized real-use recording | Exact visible action, relevant UI, demonstration status |
| App adoption or ranking | Real chart-page/app screenshot | Country, category, free/paid filter, rank, app name, capture date |
| Partnership, release, restriction | Official announcement crop or relevant event footage | Parties, announcement date, announced versus already available |
| Physical business/product | Official or otherwise usable photograph/packshot/footage | Correct location/product, period, recognizable details |
| Hidden causal mechanism | Explanatory animation alongside relevant real evidence | Explicit conceptual status; no invented benchmark |

For each selected item, add to the existing asset/scene ledger: `asset_id`, `media_type`, source-page and original-media URLs, publisher, publication/capture date, use basis, claim IDs, exact narration beat, source in/out times for clips, output interval, crop, overlays, audio choice, and necessary on-screen context. Add dimensions and hash after acquisition. Do not read or expose unrelated private account details in an otherwise useful screenshot.

Apply the mandatory **60% official-video runtime gate** in `../SKILL.md` and `official-footage-production.md` while selecting assets and again on final playback. Count relevant official source excerpts as main readable visuals, including natural reading/waiting moments inside the playing original. Photos, screenshots, self-made animations, generative video, unofficial clips, and editor-added frozen/loop padding do not qualify. Record eligible source/output intervals and the union share in `official-video-report.json`; source authenticity and source-use time require provenance and review, not just video-file metadata.

### Cut and composite for comprehension

- Use a short, purposeful excerpt long enough to show the stated action and result. A roughly 3-6 second demonstration is a useful starting point, not a quota or a copyright safe harbor. Split a multi-step claim when its actions cannot be understood in one excerpt.
- Preserve temporal meaning. Do not splice an input from one feature to a result from another, imply a sped-up demonstration is measured real-time performance, or use a queue animation as evidence of an observed outage. Label acceleration or reconstruction when material to the claim.
- Prefer original downloads from official media resources or authorized source access. Follow the existing source gate; retain source marks/notices and keep required attribution. An official upload or a short excerpt alone does not establish unrestricted reuse. Record the actual terms/use basis and resolve concrete restrictions with usable alternatives.
- Reframe landscape footage for portrait around the demonstrated action. If a crop loses a necessary button, result, or participant, use a readable inset or stacked composition instead. Do not let an unrelated background occupy most of the frame while the real demonstration is tiny.
- Show the authentic capture first; highlight the decisive row, rank, button, or headline without changing the underlying content. Place translations and explanations outside the source pixels. Keep the important context readable on screen, not only in the source ledger.
- For exact numbers and ranking changes, use the real dated capture. If unavailable after relevant attempts, label a source-backed replacement `자료 기반 재구성`; do not imitate a live official UI or call a generated graphic a screenshot.
- Default to muting source music/narration under our Korean narration. Preserve original sound only when it serves the explanation, has a documented use basis, and is deliberately mixed. Keep the existing 1.30 voice-rate setting applied once; do not accidentally accelerate source footage with the narration.
- Inspect the actual entry, action, result, reading hold, and exit in the final MP4. Check that the action is visible when named, the screen is legible at phone size, captions do not cover the proof, and the source label does not imply independent verification.

Record `ACTUAL_MEDIA_QA` in `verification.md`:

- `PASS`: relevant source search performed, selected materials have documented provenance/use basis, and rendered clips/captures/photos visibly support the concurrent narration with readable context.
- `FALLBACK`: a concrete access, use, or editorial limitation is recorded and the reviewed alternative still explains the claim; identify affected scenes at delivery.
- `HOLD`: sourcing skipped; a usable demonstration replaced without reason; mismatched action; false/recreated screenshot presented as real; proof hidden, distorted, or unreadable; or unresolved use restrictions on a selected asset.
- `NOT_APPLICABLE`: no claim about observable product actions, rankings, events, or physical subjects requires actual-media proof. Simply omitting the media does not qualify.

This review is separate from `NEWS_CONTEXT_SHARE`: a technical explanation over official footage remains technical. Neither file metadata nor the geometry validator can prove narrative alignment or adequate permissions.

## Source gate

Before committing a product scene to illustration, inspect these sources as relevant:

1. official newsroom, media kit, or product/brand asset library;
2. official company or brand product pages and their asset-specific terms;
3. suitable openly licensed or otherwise permission-compatible photographs, including an available user-owned original, when official assets do not cover the intended use.

Search-result thumbnails, retailer listings, and publicly downloadable files are discovery leads, not reuse permission. Inspect the original source and applicable terms. A menu or foodservice asset license may not cover a stock-analysis Short. Attribution, brief screen time, and an informational purpose alone do not establish permission. Distinguish the photograph's reuse terms from identifying a brand; do not assert that all real product images are prohibited by copyright.

Keep a compact sourcing record in `sources.md`: scene and intended product, candidate source URL, terms URL or permission evidence, intended distribution/use, and the selection or rejection reason. Distinguish `not_investigated`, `unavailable`, `restricted_for_intended_use`, `terms_unresolved`, and `usable_for_intended_use`. Do not mark a failed lookup as a legal prohibition. If the first source is unsuitable, examine a relevant alternative before falling back; record access limitations when further research cannot be completed.

Download a selected original from its source page. Do not screenshot, trace, or generatively redraw a logo or branded package to evade the source gate. For every selected photograph, packshot, or mark, record:

- asset ID and intended on-screen purpose;
- source-page URL and direct asset URL;
- publisher, retrieval date, file type, dimensions, and SHA-256;
- stated license, applicable terms, or permission evidence and required attribution;
- the basis supporting the intended use, depicted product/brand and market or packaging date when relevant, and every modification performed.

An unsupported use rationale does not resolve restrictive or missing terms. Continue with usable alternatives; do not acquire a paid license or contact a rights holder without the relevant user authorization. If suitable real images remain unavailable after investigation, use an appropriately sourced mark with text, or verified names and category text. A generic category diagram is acceptable only if it still explains the scene and is clearly illustrative. Record the affected scene, attempts, concrete reason, and loss of recognition; disclose the fallback at delivery. Do not stop routine production merely to reconfirm a reversible fallback that existing instructions allow.

## Rendering contract

- Make the real product the main visual in a product-identification scene. Preserve the packaging, label, color, proportions, and correct brand/product pairing. Do not replace a bottle with a generic can or invent a variant. Check the depicted region and date when they could mislead the claim.
- Use enough resolution for the final display size. Reduce the number of products or split the scene before shrinking them beyond recognition. Apply only transformations compatible with the source terms, preserving required notices; do not remove watermarks. Check any crop or compositing operation for damaged packaging edges.
- Use the mark only as a contextual identifier for reporting, analysis, criticism, or explanation; do not imply sponsorship or endorsement.
- Preserve the supplied aspect ratio, colors, lettering, and internal geometry. Cropping transparent padding and proportional scaling are allowed; recoloring, warping, tracing, and generative animation are not.
- Composite the original asset in a deterministic layer after generated imagery. Keep exact marks out of generative-video prompts.
- Give the logo a quiet container or enough contrast and clear space. Keep it outside charts, source lines, and the platform-caption lane.
- Avoid dominant full-screen logo treatment unless the company identity itself is the subject. Never use the mark for merchandise, impersonation, or a fake official channel.
- Inspect the opening, densest frame, scene boundaries, and final frame at full resolution for clipping, deformation, halo artifacts, or unintended overlap.

Add each selected product image or mark to the scene manifest asset ledger with its provenance and rights note. Keep the detailed sourcing record in `sources.md` and link it by asset/scene ID. Do not imply sponsorship; keep the normal no-upload statement in the final report unless publishing was separately authorized.

## Consumer-product portfolio scenes

When the company's brands or repeated-use products are part of the investment thesis, do not default to generic icons such as an unlabeled razor, diaper, detergent bottle, or toothbrush. A PepsiCo portfolio scene made of blue/green generic cans and colored snack bags underneath `Pepsi`, `Lay's`, `Doritos`, and `Gatorade` repeats the known failure: labels alone do not restore recognizable packaging.

- Choose a readable set of representative products explicitly connected to the company by an official portfolio, annual report, or brand page. Three to six can work, but fewer large recognizable products are better than many tiny ones.
- Show the actual product photo or packshot with a large brand name and plain-language category. A separate official logo is optional when the package already identifies the brand. Do not treat a logo-only grid as equivalent to a product-photo scene.
- Use a consistent grid or sequence with balanced visual weight, generous spacing, and enough contrast. Keep product fronts and labels visible through the intended reading hold. Animate entry or a purposeful comparison while preserving package geometry.
- Inspect a representative product scene before the full render, then entry, settled, and exit frames in the final MP4 at original resolution and phone size. A missing, cropped, stretched, low-contrast, or partially covered product fails even when a different sampled frame looks correct.

## Product asset review result

Record `PRODUCT_ASSET_QA` in `verification.md`, with scene IDs, source-record references, inspected timestamps, and findings:

- `PASS`: authentic product assets have a documented use basis and the rendered products are correctly matched, recognizable, and legible at phone size.
- `FALLBACK`: the source search and concrete reason for substitution are recorded, or the user explicitly requested illustration; the alternative has been visually reviewed and still fulfills the scene's explanation. State the substitution and limitation at delivery.
- `HOLD`: sourcing was skipped or incomplete, rights for a used asset remain unresolved, generic substitutes are unexplained, or the rendered products are unrecognizable or incorrect. Repair recoverable issues before calling the video finished.
- `NOT_APPLICABLE`: the video has no scene whose purpose is identifying actual products or brand portfolios. Removing product photos does not make an existing product-identification scene inapplicable.

This is an editorial review. The current geometry validator cannot establish licensing, product identity, source-search completeness, or visual recognition; do not claim it enforces this gate automatically.

## Service and segment identity scenes

Apply this section to cloud, advertising, marketplaces, subscriptions, payments, software, insurance, media, logistics, and other businesses whose product is not a package on a shelf. A photo background plus text-only number cards does not make the service visually recognizable.

- Build a `SERVICE_IDENTITY_MAP` before layout. For every thesis-critical named business, record the spoken phrase, claim IDs, preferred identity asset, source and use basis, on-screen interval, and fallback.
- Choose by what the sentence needs to show. For function, behavior, adoption, or an event, prefer a usable official demonstration, actual interface/ranking capture, or relevant photograph. For identity alone, prefer the official service/product mark, then an appropriate architecture/product icon or other sourced identifier. Use an editorial composite from sourced marks, plain text, and owned or openly licensed pictograms when the direct material cannot explain the scene. A logo alone cannot demonstrate a product action or ranking.
- When two or more businesses form the thesis, show at least two distinct identity assets in the signature or proof sequence. For example, a cloud mark and server image can identify cloud, while a seller portal crop or storefront pictogram and an advertising mark or sponsored-result visual can identify marketplace services and ads.
- Keep the financial number largest, but allocate about 15-30% of the card or scene to the service identity. The asset must remain recognizable for at least one complete spoken clause and may not be hidden behind a number, connector, source strip, or caption.
- Do not paste the same parent-company logo into every card and call the segments differentiated. Pair the parent mark with a service name, official sub-brand mark, interface, or distinct explanatory image.
- An editorial composite must not imitate an official badge. Label it through ordinary scene text, preserve the original mark, and record the composite construction in `sources.md` and the manifest.
- Review entry, settled, and exit states at full resolution and phone size. Confirm that each asset matches the spoken business at that moment and that the sequence is more than changing text over one background.

Record `SERVICE_IDENTITY_QA` in `verification.md`:

- `PASS`: every thesis-critical service has a sourced recognizable asset, multi-business scenes use distinct identities, and final frames pass phone-size review.
- `FALLBACK`: the search and concrete source limitation are documented, and an editorial pictogram or composite has been reviewed and clearly functions as explanation rather than an official mark.
- `HOLD`: a named thesis-critical service is represented only by text or a repeated parent logo despite a usable identity asset, sourcing was skipped, or the asset is too small, obscured, or mismatched.
- `NOT_APPLICABLE`: no named product, platform, service, or business segment is part of the thesis. A text-only treatment does not make the gate inapplicable.
