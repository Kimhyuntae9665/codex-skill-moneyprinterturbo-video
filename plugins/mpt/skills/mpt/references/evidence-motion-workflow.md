# Evidence-led motion workflow

Use this workflow for investment explainers, company-business-model Shorts,
historical valuation comparisons, or any production where exact numbers and
high-density motion must coexist.

For a US-listed security, complete
[`us-equity-research-gate.md`](us-equity-research-gate.md) first. Its required
order is `us-stock-research -> SEC/issuer IR lock -> Unusual Whales secondary
check -> claim-ledger freeze -> production`. The stages below consume that
frozen evidence packet and do not replace it.

## Required artifact set

Create these artifacts before calling a video finished:

1. `brief.md` — audience, exact opening line and visual, question and payoff,
   thesis, counterpoint, target duration, dated data scope, shot plan with
   explanatory changes, numeric explanation, and sound plan. Apply the
   pre-render opening review in `../SKILL.md` before full production.
2. `sources.md` — primary-source links, market-data vendor links, asset rights,
   retrieval dates, and calculation scripts or formulas.
3. `narration.ko.txt` — final spoken Korean. Use the same display values as the
   graphics.
4. `subtitle.srt` — reviewed timing and copy. Do not use raw speech recognition
   as final financial copy.
5. editable graph JSON, asset/source manifest with hashes, exported SVG, and
   full-resolution PNG preview for each scene routed through `logo-flow-infographics`.
6. `scene-manifest.json` — executable geometry, timeline, state-change, claim,
   and asset contract.
7. one deterministic renderer and its exact render command.
8. one directed visual master, one MoneyPrinterTurbo narrated output, and one
   final reviewed-subtitle derivative.
9. `verification.md` with the editorial and listening statuses in `../SKILL.md`,
   plus automated JSON reports from layout, stream, frame, and freeze checks.
   Record visual and audio observations, timestamps, and reviewer separately.
10. `official-video-report.json` — attributable official assets, source in/out
    and reviewed final output intervals, union duration, full MP4 duration,
    share, and PASS/HOLD against the minimum 60% gate in `../SKILL.md`.
    Plan the share in `brief.md`; natural source reading/waiting moments count,
    while stills, self-made animation, and editor-added freeze/loop padding do not.

Missing evidence or a failed gate is a HOLD, not a stylistic suggestion.

## Freeze facts before layout

Give every factual or calculated statement a stable claim ID. Each claim must
store:

- display text and unrounded value;
- unit and precise definition;
- as-of date;
- primary source or named market-data vendor;
- formula or calculation-script path when derived;
- the limitation needed to prevent overstatement.
- evidence tier, verification status, and the recorded secondary-check result.

Do not mix adjusted and unadjusted prices, forward and trailing yields, gross
and net buybacks, reported and constant-currency values, or differently sampled
betas. Put the definition on screen when the distinction changes the meaning.
Use language such as `조건부 후보`, `역사적 비교`, and `개인화된 조언 아님`
when appropriate. A drawdown or high yield is not proof of undervaluation.

## Design relationship scenes with logo-flow-infographics

After the ledger is frozen and before the scene contract is finalized, read
[`infographic-motion-bridge.md`](infographic-motion-bridge.md). Invoke the
installed `logo-flow-infographics` Skill for verified company relationships,
service architecture, partner roles, and workflows. Use authentic approved
local identities in white rounded cards on a dark dotted canvas, short names
beneath them, and thin curved directed connectors. Keep interpretation and
conditions outside the graph. Save graph JSON, an asset/source manifest with
hashes, SVG, and a full-resolution PNG preview. Use custom deterministic charts
for trends, numeric comparisons, compositions, ownership figures, and other
finance-specific geometry that needs an accurate quantitative scale.

The graph receives frozen relationships and claims; it never researches or updates them.
The renderer may animate masks, paths, bars, nodes, and callouts, but it must not
change labels, values, order, scale meaning, or source association.

## Build a scene contract

Start from `assets/templates/shorts-scene-contract-v1.json`. A scene normally
lasts 2.5–5 seconds and carries one main idea. Every scene must declare:

- start and end timestamps;
- all visible element rectangles;
- parent-child containment for labels inside cards or marks inside buildings;
- intentional overlap exceptions by element ID;
- claim IDs used by graphics and captions;
- at least one purposeful state change, preferably two for a dense scene;
- a source line whenever factual claims appear.

Use logical coordinates so layout remains readable. The default contract uses
720x1280 logical pixels and renders to 1080x1920 at 30 fps. Keep the header,
content, source, and platform-caption areas separate. The content zone should
not extend into the lower caption area merely because a specific preview app
hides its controls.

Run `scripts/validate_scene_manifest.py` after every geometry change. If an
element is meant to sit inside another, declare `parent_id`; if two siblings
must overlap, declare `allow_overlap_with`. Never silence a real collision by
adding a broad exception.

## Direct the visual language

Use one visual grammar for the whole Short:

- editorial finance palette with one signal color and one comparison color;
- tabular numbers and a Korean font with verified glyph coverage;
- simple physical metaphors tied to the subject, such as stores, land parcels,
  pipes for rent/royalty flow, or a measured world map for global footprint;
- continuous camera or object motion with restrained easing;
- direct labels next to the thing they describe;
- negative space around captions and source lines.

Avoid decorative objects that do not explain the topic. Coins, glowing orbs,
generic skyscrapers, unrelated machinery, confetti, and classroom card grids
are not substitutes for evidence.

For generated plates, ask only for scenery, materials, lighting, and camera
perspective. Add all text, numbers, charts, map data, brand marks, and decision
rules afterward with deterministic code. Record the model, prompt, seed when
available, output hash, and rights terms. Inspect generated architecture for
impossible geometry before use.

## Motion rules

- Make motion reveal causality: lines draw, locations activate, rent flows from
  land to company, cash separates into dividends and net buybacks, and risk
  counters interrupt the positive thesis.
- Follow the explanatory beat and shot-plan rules in `../SKILL.md`. A pan over
  the same photo or a caption entrance alone is not a new explanatory beat.
  Keep reading holds intentional; never add arbitrary motion just to defeat
  freeze detection. Review technical continuity and editorial pacing separately.
- Restrict flashes and wipes to the content zone. Do not wash out the header,
  source, or caption.
- Do not use transition presets that leave a line, underline, or ghost card in
  the next scene.
- Reserve 6–10 frames for a settle after each entry motion. Do not move text
  while the viewer must read an exact number.
- Check the opening at 0.0 and 0.2 seconds, both sides of every boundary, the
  midpoint of every scene, and the final decodable frame.

## MoneyPrinterTurbo assembly

Use the directed master as a single local material. Set sequential concat,
`video-count 1`, transition mode `none`, and a clip duration not shorter than
the narration. Apply the sound plan in `../SKILL.md`: use a quiet, cleared
instrumental bed when suitable, or record the reason for silence. A narration-only
assembly is intermediate when the plan calls for BGM; verify the final mix.
Use MoneyPrinterTurbo for the pinned execution, narration, and final assembly;
do not let its generic material splitter restructure the directed timeline.

If Edge TTS does not return reliable Korean subtitle boundaries, preserve the
MoneyPrinterTurbo narration audio, recover timestamps with an already-approved
speech model, replace the text with the reviewed SRT, and burn it with the
bundled Noto Sans KR font.

## Final QA order

Run gates in this order so later checks never hide an earlier failure:

1. claim-ledger and numeric-explanation review, then opening TTS/visual preview
   and shot/sound-plan review before the full render;
2. logo-flow graph/asset manifests, SVG export, claim match, and full-resolution preview review (or scale-accurate custom-chart review);
3. `validate_scene_manifest.py`;
4. renderer execution and full visual-master decode;
5. MoneyPrinterTurbo prepared-local log check;
6. reviewed subtitle burn;
7. `validate_video.py`;
8. `probe_scene_frames.py` with audio required;
9. original-resolution contact-sheet and individual-frame review;
10. playback review of the first three seconds, full explanatory sequence,
    and actual final audio mix, including Korean pronunciation and cadence;
    verify official-video interval union is at least 60% of full MP4 duration
    and record `OFFICIAL_VIDEO_QA`; missing measurement or a lower share is HOLD;
11. SHA-256, byte size, exact output path, and no-upload statement.

ASR and loudness checks do not replace listening. If playback or listening is
unavailable, mark the affected gate incomplete and report a review draft, not
a finished or fully verified video, following `../SKILL.md`.

The MCD v8 reference demonstrates the intended standard: it uses a dated claim
ledger, contextual Golden Arches geometry, a deterministic world map, separate
building/land/equipment layers, historical dividend-yield context, beta and
correlation comparisons, a risk scene, and a conditional end rule.
