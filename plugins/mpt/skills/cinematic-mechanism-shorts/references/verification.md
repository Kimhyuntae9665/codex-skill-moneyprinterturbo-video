# Verification and honest delivery

## Gates

**Story alignment is a separate blocking editorial gate.** For each core narrated claim, compare `story-visual-map.md` with actual final frames and motion: identify the actor, role, target, event and outcome. First mute narration/long captions while retaining short identity/role labels; then compare the same interval with narration. A logo watermark, physical motion or a valid shot JSON does not prove the relationship. Apply `story-aligned-miniatures.md` for the current miniature baseline, character contact/rig checks and intentional cutaways.


**Company-story editorial gate (2026-09-06):** inspect `topic-selection.md` and its actual social-response records. The chosen topic must pass casual-listening comprehension, have a plain-language hook/payoff and require little background. Verify missing engagement was not changed into zero, popularity was not promoted into truth, and the video has not drifted back into engineering instruction. This is a separate gate from technical and visual validity. See `easy-company-stories.md`.

Before production, review the visual treatment alternatives and event-based storyboard from `shot-production.md`. Confirm that a route was chosen for a stated reason and that repetitive beats were redesigned. Treat missing visual ideas as a preproduction gap; higher render quality, more camera angles and a longer script cannot close it. This is an editorial inspection, not an automated creativity certification.

Apply the 12-film transfer checks from `causal-staging-library.md` within story alignment: inspect the actor and receiving target at the decisive contact/change; verify the result is readable before the next cut; follow actor/object identity between whole-system and close views; and check that the final state answers the opening question. For a character handoff, inspect support before pickup, hand contact during motion and stable placement after release. If a counterfactual or remaining limitation is shown, its status must survive without a tiny footnote. Record actual reviewed intervals; do not mark these passed from populated storyboard fields.

1. **Evidence:** the pictures imply no stronger claim than the sourced script. A visual metaphor, reconstruction or teaching model is identified where confusion is plausible.
2. **Topology:** inlet/outlet, supports, ownership and direction remain consistent. Particle loops do not interpolate through a wall when resetting. Geometry-critical facts are checked against a reference or labeled conceptual.
3. **Camera:** inspect opening, reveal start, peak action, camera switch and end; check both sides of each cut. A lid, worker, title or background structure must not occlude the explanation.
4. **Motion:** view representative continuous clips, not just attractive frames. The action must visibly cause the consequence. A camera orbit or floating labels alone cannot pass.
5. **Timing:** phrase-end cuts and visible action agree with the edited voice. If audio is changed, revalidate cuts and captions. Technical tolerance in a validator is not a substitute for meaning.
6. **Sound:** listen to pronunciation, clipped consonants, pace, effects and BGM balance. If the environment cannot actually listen, record `listening: not_performed` and call the result a review/proof version.
7. **Technical:** decode the whole MP4; check stream duration, frame count, dimensions, codec, audio presence and peak. Inspect phone-size frames for text clipping and overlap. In procedural renderers, quantize font-cache keys and bound the cache; skip text fitting when its animated container has zero/negative available width, and bound fit loops. Test entry/exit frames as well as settled layouts. The 2026-09-06 Amazon run exposed an unbounded fit loop during a tiny entering label; a valid settled preview did not cover that failure.
8. **Similarity:** separately assess material realism, spatial access, causal transformations, pace, voice and payoff. Do not average away a failed main requirement with good codec scores.
9. **Visual progression:** compare the full storyboard strip and selected motion clips. Record distinct explanatory compositions and actual subject/state changes; camera-angle count is not scene variety. Reject a sequence dominated by an unchanged layout unless continuous causal evolution is demonstrated. When explaining a bottleneck, the muted clip must make the constraint, upstream queue and downstream waiting understandable.
10. **Company identification:** at a material partner's introduction, check its sourced logo/name, role and timing. Check that component labels are meaningful and category-correct; `CUSTOM` is not sufficient for an ASIC explanation. A readable protagonist watermark does not cover missing partner identification.

11. **Visible explanatory paths:** inspect the actual rendered route, not only object coordinates. In the photon/Rainier preflight, a route placed below a workbench and an optical tracer enclosed by an opaque cable were invisible despite existing in the scene. Move symbolic routes into a visible layer; show a clearly identified cutaway when the hidden path itself is the lesson. Recheck that a pulse changes role/color at the actual conversion point, not on an unrelated timer. Fit physical labels to their actual support surfaces, and place room cameras inside the intended walls so foreground architecture does not hide the subject.

12. **Visible system boundaries:** a claim such as “inside the same package” needs a visible common substrate/boundary, rather than unrelated parts scattered on a generic board. Keep component, package, board, rack and site levels distinct. Add real supports to physical insertion motions; sliding a module toward a receptacle does not explain why it stays suspended before contact. Inspect the boundary and support in the rendered frame, then rerender the affected shots instead of treating an overlay label as proof of physical correctness.

## Known failures from the 2026-09-05 implementation test

2026-09-06 paired Amazon failures: the early miniature had crude wooden figures and unfinished-looking spaces; its photoreal replacement then failed story alignment by substituting generic office/server/lobby footage. The user now selects NVIDIA v2 as the baseline and explicitly accepts polished miniature people. Improve miniature craft and narrative correspondence together. Do not revive a blanket miniature ban from the earlier incident.

- A generated copper cold-plate keyframe looked convincingly detailed but showed disconnected concentric channels. It could not demonstrate the proposed continuous path. Rebuild/verify the topology before using it as causal evidence.
- A Blender lid lifted correctly in an oblique shot, then blocked the mechanism in a top view. Moving the lid outside the next camera's sightline repaired it. Inspect every camera against animated occluders.
- A looped tracer could cross walls when its path position reset from 1 to 0 with interpolation. Key each frame and hide the tracer around reset, or animate a genuinely closed loop.
- Alternating divider walls must actually meet the appropriate perimeter wall. A tiny gap leaves an unintended bypass even if a scripted tracer follows the desired path. The local model's divider length was increased to overlap the side wall; this remains a conceptual model, not a fluid simulation.
- A reference-conditioned image improved materials but still changed divider/perimeter connections. Classify it as art direction only until topology is verified; image conditioning does not guarantee mechanism preservation.
- Existing 2.5D racks with moving graphics were technically animated but did not match realistic generated architecture footage. Mark the fidelity gap; do not call any motion a successful style match.
- The NVIDIA Fusion 45-second review used many angles of one board, weakly differentiated queue colors, a `CUSTOM` label and no Marvell logo at the partnership beat. The user found it visually repetitive and the bottleneck unclear. A prior sampled-frame pass only covered visible defects/readability; it did not establish explanatory variety or mechanism comprehension. Future productions must pass the added progression and identification gates. These instructions do not constitute a rerender or correction of the existing MP4.

## Suggested report

After the 2026-09-05 user-found floating-light defect, inspect background attachment and floor contact explicitly. A pass from hero-object samples alone is not a full-scene visual pass. See `scene-integrity-and-next-steps.md` for the incident, correction and staged QA. If the user identifies a valid miss, preserve the original review scope and mark the affected release pending/failed until corrected views are checked.

```json
{
  "artifact": "proof.mp4",
  "story_alignment": "pass|fail|not_performed",
  "miniature_craft": "pass|fail|not_applicable|not_performed",
  "character_action": "pass|fail|not_applicable|not_performed",
  "technical": "pass|fail|not_run",
  "sampled_visual": "pass|fail|partial",
  "full_playback": "pass|fail|not_performed",
  "listening": "pass|fail|not_performed",
  "reference_similarity": "matched|partial|not_matched|not_assessed",
  "remaining_gaps": [],
  "reviewed_timestamps": [],
  "tools_actually_used": [],
  "tools_only_researched": []
}
```

A structural script may reject missing fields and inconsistent timestamps. It cannot know whether a generated hand has six fingers or a visual explanation is understandable. Keep those review categories separate.
