# MCD v8 golden reference

Use this package as a pattern for future evidence-led company or stock Shorts,
not as a source of current McDonald's facts. Every financial value is frozen to
the dates and definitions in `sources-v8.md` and `scene-manifest-v8.json` and
must be refreshed before reuse.

## What to inspect

- `brief-v8.md`: thesis, counterpoint, dated data scope, and output contract.
- `sources-v8.md`: evidence and calculation provenance.
- `narration.v8.ko.txt` and `subtitle.v8.srt`: locked Korean voice/caption copy.
- `storyboard-v8.md`: scene purpose and motion direction.
- `scene-manifest-v8.json`: complete claim ledger, safe zones, rectangles,
  parent-child nesting, scene boundaries, and state changes.
- `motion/mcd_short_v8.py`: deterministic Pillow renderer. It constructs the
  world map, buildings, land, equipment, cash flows, charts, and contextual
  Golden Arches with code instead of asking an image model to draw exact data.
- `qa/layout_qa_v8.py` and `qa/frame_probe_v8.py`: frozen project-specific gates.
- `verification/verification-v8.md`: final artifact facts and review record.
- `research/hf-reddit-tool-scan-v8/integrated-hf-reddit-tool-report-v8.md`:
  research-to-production decisions and rejected tool uses.

## Reusable decisions

1. The Short is a continuous editorial motion piece, not a slideshow of cards.
2. Each visual is semantically tied to McDonald's: a store, land parcel,
   building/equipment split, map footprint, rent/royalty flow, shareholder cash
   return, yield history, beta/correlation, risks, and conditional entry rules.
3. Brand geometry is contextual and recognizable but does not imply endorsement.
4. All numbers and Korean text are deterministic overlays. Generated assets do
   not carry factual copy.
5. Header, content, source, and platform-caption zones are independent. Labels
   inside cards use declared parent-child containment instead of visual guessing.
6. The opening, every boundary, every midpoint, and final decodable frame are
   extracted. A contact sheet is necessary but individual full-resolution frames
   remain the final layout authority.
7. The end card contains both an expansion condition and a cancellation rule;
   it does not end with an unconditional buy recommendation.

## Generic QA commands

Run these from the installed Skill's `scripts` directory. The generic tools
accept this frozen v8 manifest as well as new `shorts-scene-contract-v1`
projects.

```text
python validate_scene_manifest.py "../examples/mcd-valuation-2026/scene-manifest-v8.json"
python probe_scene_frames.py "<MCD-v8-final.mp4>" "../examples/mcd-valuation-2026/scene-manifest-v8.json" --out-dir "<qa-dir>" --require-audio
```

Do not copy the old values or dated output path into a new production. Copy the
contract structure, regenerate the claim ledger, and rerun every gate.
