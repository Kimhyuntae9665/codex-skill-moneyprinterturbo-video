# Scene integrity, reuse and audience testing

## Incident: floating white strips, 2026-09-05

The first cooling proof placed three visible emissive boxes named `ceiling light` at z=4.3, with no ceiling, suspension or housing. They were authored geometry, not SDXL/LTX hallucinations. Prior checks focused on channels, captions and decode validity; the whole-scene support review missed this obvious background defect. The earlier broad sampled-visual pass was insufficient and must not be reused as a release approval.

Fix the current open studio example by removing unnecessary visible emissive strips while keeping off-camera area lighting. `environment_assets.py` adds reusable grounded table legs, a CDU pedestal and PCB mounting pads. These address other missing support cues found in the same sweep. The example is a conceptual teaching studio, not an actual data-center reconstruction. The deliberately exploded lid and colored flow markers have separate explanatory roles; do not classify them as ordinary unsupported furniture.

`audit_environment.py` checks nine named support contacts and absence of the obsolete visible light meshes. Its bounding-box contact tolerance is not proof of physical stability, whole-scene collision freedom or a comprehensible image. Always inspect all five camera views and the opening at full portrait size after this test.

## Priority 1 — reliable scene and asset library

Each reusable module should record origin, dimensions/unit convention, floor plane, support/anchor points, connection ports and orientation, permitted material variants, source/license and tested camera views. A pipe module must expose its ports; a rack must include its floor relationship; a visible suspended light must include a mount or support route. The current support factories are a first small tested module, not a completed photoreal asset library.

Reuse normally reduces authoring/rework first. Material replacement does not inherently reduce rendering time: translucent materials, glossy surfaces and complex geometry can increase it. Track authoring, simulation/generation, render, transfer, assembly and QA separately. Estimate a render from warm representative frames × frame count plus initialization/transfer, and record failed attempts. Compare **cost per accepted shot/second**, not only the fastest generated candidate. Give elapsed seconds unless actual electricity/cloud pricing is known; do not invent monetary savings.

## Priority 2 — controlled generation as a bounded experiment

ComfyUI is a workflow host, not a physical correctness guarantee. [ControlNet](https://huggingface.co/docs/diffusers/en/using-diffusers/controlnet) conditions on depth/edges/pose; this helps guide geometry but is not a rigid-body/contact solver. Use Depth/Canny from a corrected original 3D scene for a mechanism. OpenPose is relevant to a person/task, not a pipe connection. Do not preserve the faulty floating layout through a control map.

Prepare a fixed 2-second shot with known anchors, beginning/end state and motion. Export matching RGB/depth/edge/ID masks with the same camera, resolution and frame numbers. Compare unconditioned versus conditioned output using a small fixed seed/setting set. Inspect attachment points, part count, flow direction and frame-to-frame continuity. A good still is not a validated video pipeline. After two bounded failed revisions, change the shot or keep deterministic geometry instead of scaling the whole episode.

[SVD's official guide](https://huggingface.co/docs/diffusers/main/en/using-diffusers/svd) describes short image-conditioned video and memory-saving options. This does not make SVD a physics-engine integration or prove it follows a multi-step mechanical action. An actual integration would need a tested data/control interface and frame-level evidence. These ControlNet/ComfyUI/SVD experiments are **planned, not implemented or validated** by adding this document. Verify current model compatibility, license, disk/VRAM and usable resolution before installing anything; do not replace the working environment just to run the experiment.

## Priority 3 — perceptual QA and audience evidence

Before publishing, perform a normal-speed start-to-end review and actual listening, using a phone-size frame and normal speaker/headphone level. Check first three seconds for a clear subject/question, captions against action, TTS consonants after trimming, music masking and fatigue. Record reviewer, date, specific observed defects and outcome. If playback or listening is unavailable, mark it pending and deliver a review version; never translate codec/loudness checks into a perceptual pass.

Make A/B variants by changing one variable: the opening line **or** visual reveal timing, holding the factual story, duration, voice/mix and remaining edit stable. Comparing both a new hook and faster cuts at once prevents attribution. Offline review with a few viewers is qualitative feedback, not measured platform retention.

For authorized publishing or user-supplied analytics, record the observation window, exposure, traffic source, video length and [YouTube's available metrics](https://support.google.com/youtube/answer/12220281?hl=en): stayed-to-watch, engaged views, average view duration/percentage and retention curve when available. Read the 3-second point only if actual data supports it; do not invent a native “3-second drop-off” field. Sequential uploads are not randomized A/B tests because audience, topic and timing vary. Report uncertainty rather than promising virality or declaring a winner from a few views. Skill editing alone does not authorize upload, viewer recruitment/messages or analytics access.
