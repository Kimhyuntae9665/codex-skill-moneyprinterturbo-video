# Editorial tempo for narrated Shorts

Use this reference for every narrated Short after the script and claims are
stable. It governs three linked decisions: what recent external work teaches,
which TTS gaps belong in the performance, and where visual cuts occur.

## Break down a comparable reference

Before locking the shot plan, inspect at least one recent Short that matches the
topic, language, format, or intended viewing behavior, or use an editorial
reference supplied by the user. Record the URL, retrieval date, visible
duration, first semantic beat, completed hook time, observable cut intervals,
camera or subject changes, caption role, and audio treatment in
`reference-breakdown.md`. Separate direct observations from interpretations.

When selecting AI-film galleries or transferring a specific material, camera,
editing, or sound technique, use [reference-to-production.md](reference-to-production.md).
Record what was actually watched or heard separately from creator-reported
settings and our rendered tests. A gallery listing alone is not a shot or audio analysis.

Use the reference to set an editorial hypothesis, not to copy a script, visual,
asset, claim, or unverified performance formula. Do not infer platform ranking
rules from a view-count curve or one creator's explanation. State which
observations will be applied and which are unsuitable for the current evidence,
audience, accessibility, or rights constraints.

## Edit dry TTS before pictures and effects

Use this order:

```text
dry TTS -> silence report -> deliberate gap edits -> approved narration
-> semantic cut map and subtitles -> visual render -> effects and music mix
```

Measure silent runs on the dry narration with a documented threshold and
minimum duration. Thresholds such as -60 dBFS and minimum runs around 0.1-0.3
seconds are starting observations, not universal settings. Audition the actual
voice and preserve short breaths, comprehension space around dense figures, and
an intentional pause before a major reversal. Remove synthesis slack, repeated
dead air, and accidental joins that make ordinary clauses feel slow.

Keep a before/after JSON or table containing each changed range, original and
new duration, reason, and resulting total duration. Do not run blanket silence
reduction after effects or music have been mixed. Listen to the hook, densest
number sentence, every edited join, and final risk turn.

## Cut on semantic completion

Build the timeline from the approved narration rather than scaling an older
timeline by a global speed factor. Mark the onset and completion of each clause,
number-unit pair, comparison, qualifier, and decision rule. Keep the supporting
visual through completion, then cut at the next meaningful onset or within a
small justified lead.

A cut fails when it splits a company name, number from its unit, subject from
its predicate, comparison from its second term, or claim from a necessary
qualifier. Captions may change inside a longer scene, but they must not create a
different meaning from the spoken clause.

Record `audio_boundary_s`, `cut_s`, `offset_frames`, and `reason` for every
primary cut. Review the real-time first three seconds and the whole phone-scale
sequence. A contact sheet or correctly declared manifest cannot establish
rhythm.

## Make every shot earn its time

For each shot, record the primary subject, camera or crop path, new information,
and exit reason. A new caption, a slow zoom over the same photograph, or a
decorative transition does not by itself earn another beat. Prefer a subject
change, a causal reveal, a measured comparison, or a detail that answers the
current spoken clause. Remove frames that add neither comprehension nor
anticipation.

Record these results in `verification.md`:

```text
REFERENCE_BREAKDOWN_QA=PASS|HOLD|NOT_APPLICABLE
SILENCE_DENSITY_QA=PASS|HOLD|NOT_APPLICABLE
SEMANTIC_CUT_QA=PASS|HOLD|NOT_APPLICABLE
```

`PASS` requires the saved reference breakdown, measured silence report with
reviewed edits or a documented finding that no edits were needed, and a cut map
derived from the approved audio. These gates do not claim higher retention or
platform distribution without audience data.
