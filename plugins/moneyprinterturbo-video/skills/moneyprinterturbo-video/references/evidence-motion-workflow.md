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

1. `brief.md` — audience, hook, thesis, counterpoint, target duration, and
   dated data scope.
2. `sources.md` — primary-source links, market-data vendor links, asset rights,
   retrieval dates, and calculation scripts or formulas.
3. `narration.ko.txt` — final spoken Korean. Use the same display values as the
   graphics.
4. `subtitle.srt` — reviewed timing and copy. Do not use raw speech recognition
   as final financial copy.
5. infographic DSL, exported SVG, and full-resolution preview for each scene
   routed through `infographic-creator`.
6. `scene-manifest.json` — executable geometry, timeline, state-change, claim,
   and asset contract.
7. one deterministic renderer and its exact render command.
8. one directed visual master, one MoneyPrinterTurbo narrated output, and one
   final reviewed-subtitle derivative.
9. `verification.md` plus JSON reports from layout, stream, frame, freeze, and
   visual review gates.

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

## Design data scenes with infographic-creator

After the ledger is frozen and before the scene contract is finalized, read
[`infographic-motion-bridge.md`](infographic-motion-bridge.md). Invoke the
installed `infographic-creator` Skill for editorial trend, comparison,
composition, sequence, relation, and compact ownership scenes. Save its DSL,
render a pinned AntV SVG, and inspect a full-resolution preview. Use custom
deterministic charts for dense multi-series plots or finance-specific geometry
that the available infographic templates cannot represent faithfully.

The infographic receives frozen values; it never researches or updates them.
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
- Keep the main object moving gently even during narration holds. A one-second
  static frame can feel broken in a fast Short.
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
the narration. Keep BGM off unless a rights-cleared track is explicitly chosen.
Use MoneyPrinterTurbo for the pinned execution, narration, and final assembly;
do not let its generic material splitter restructure the directed timeline.

If Edge TTS does not return reliable Korean subtitle boundaries, preserve the
MoneyPrinterTurbo narration audio, recover timestamps with an already-approved
speech model, replace the text with the reviewed SRT, and burn it with the
bundled Noto Sans KR font.

## Final QA order

Run gates in this order so later checks never hide an earlier failure:

1. claim-ledger review;
2. infographic DSL, SVG export, claim match, and full-resolution preview review;
3. `validate_scene_manifest.py`;
4. renderer execution and full visual-master decode;
5. MoneyPrinterTurbo prepared-local log check;
6. reviewed subtitle burn;
7. `validate_video.py`;
8. `probe_scene_frames.py` with audio required;
9. original-resolution contact-sheet and individual-frame review;
10. Korean narration pronunciation review;
11. SHA-256, byte size, exact output path, and no-upload statement.

The MCD v8 reference demonstrates the intended standard: it uses a dated claim
ledger, contextual Golden Arches geometry, a deterministic world map, separate
building/land/equipment layers, historical dividend-yield context, beta and
correlation comparisons, a risk scene, and a conditional end rule.
