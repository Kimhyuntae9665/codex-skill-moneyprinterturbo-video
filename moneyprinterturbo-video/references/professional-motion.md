# Professional motion workflow

Use this workflow when a Short needs premium data graphics, real photography,
or tightly directed motion instead of a sequence of generic cards.

## 1. Freeze evidence before design

- Lock one market-data timestamp and one price basis. Never mix raw and
  dividend-adjusted closes in a drawdown calculation.
- Label every statement as fact, calculation, or interpretation. Prefer SEC or
  issuer filings for company claims, and name the vendor for market history.
- Keep a counterpoint when a visual hook could overstate the conclusion. A
  price decline is not, by itself, proof of undervaluation.

## 2. Clear visual rights

- Use owned work, public-domain material, or assets with a recorded license
  that permits the intended reuse and adaptation.
- Record the source page, author, license, license URL, dimensions, SHA-256,
  and intended crop for every third-party image.
- A renderer's open-source license does not grant rights to photos, logos,
  music, fonts, or trademarks. Keep brand marks incidental and unmodified in
  an informational context, and do not imply endorsement.

## 3. Render one directed master video

- Use an actually executed open-source motion renderer such as Manim Community
  or Motion Canvas. Record the version and reproducible render command.
- Default to 1080x1920 at 30 fps. Keep essential content away from the top,
  right-side controls, and bottom caption/description areas.
- Use one visual idea per scene, restrained easing, tabular numerals, and no
  bouncing icons, emojis, decorative coins, or classroom-style card grids.
- Prefer a real building image, original chart, direct-label comparison, or
  architectural diagram over generic stock footage.
- Render a single master MP4 long enough for the locked narration and hold the
  last frame briefly. Leave the caption band visually quiet.

## 4. Assemble with MoneyPrinterTurbo

Pass the single master MP4 with `--material`, `--video-count 1`, sequential
concatenation, a clip duration at least as long as the Short, and transitions
disabled. This prevents the upstream local-material splitter from truncating,
reordering, or repeating a directed timeline.

Use the bundled Korean font and no background music unless the user supplies a
rights-cleared track. Keep social upload disabled.

## 5. Verify the finished artifact

- Run `validate_video.py` and require 1080x1920, 45-60 seconds, H.264/AAC, full
  decode, and audible narration.
- Inspect the opening, every scene boundary, the densest chart, the lowest
  subtitle, and the end card at full portrait resolution.
- Confirm Korean TTS pronunciation of dates, decimals, currency, acronyms, and
  large numbers. Shorten or rewrite text instead of shrinking it below mobile
  readability.
- Recheck that the final log shows no LLM, stock-provider, paid-generation, or
  social-post activity in prepared-local mode.
