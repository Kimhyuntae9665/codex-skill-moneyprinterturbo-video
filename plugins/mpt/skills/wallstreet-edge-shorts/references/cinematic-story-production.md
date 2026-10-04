# Cinematic Company-Story Production

Use this reference for company-story Shorts whose main value is a surprising mechanism or narrative rather than a valuation dashboard.

## Directional target

The target is a moving explanatory world. The viewer should see the hidden process occur inside a recognizable company, product, facility, contract, supply chain, or platform ecosystem. Captions support the action; they do not replace it.

The 2026-09-05 follow-up research expanded the reference sample to 16 recent/popular Shorts, with chronological frame sampling, ASR transcript analysis and detailed sequence checks. See the installed `cinematic-mechanism-shorts/README.md` for the self-contained report, evidence limits, production tutorials and actual implementation test. Use that skill for realistic reference matching. Earlier six-video observations are a preliminary study, not the current evidence ceiling.

## Build an animation state machine before a storyboard

For each story, define a physical or visual subject and these states:

1. `familiar`: the object appears in its ordinary real-world context;
2. `impossible`: the surprising result is already happening in the first two seconds;
3. `wrong_model`: the obvious explanation is shown and visually rejected or exposed as incomplete;
4. `internal_reveal`: the camera enters, cuts through, explodes, peels, or isolates the hidden layer;
5. `causal_action`: capacity fills, money moves, ownership connects, supply is reserved, software spreads, or a constraint activates;
6. `consequence`: the world visibly changes because of that action;
7. `callback`: the first image returns with a new meaning.

Each state must record its claim ID, start and end appearance, moving object, motion driver, camera purpose, duration, and transition into the next state. Camera movement by itself does not satisfy `causal_action`.

For a connected dossier, create a separate state machine for each of two to four mechanisms. Reuse an umbrella company world—campus, data-center map, product stack, supply-chain globe, or platform ecosystem—between them.

## Motion grammar extracted from the reference

- Put the physical subject in frame immediately. Do not open with a logo slate, chapter card, P/E chart, or generic stock footage.
- Start with visible action: a cable being assembled, a rack going dark, a data route changing, a factory lane locking, or a cash stream returning.
- Preserve the protagonist across shots. Change scale and access: wide exterior → tracking approach → macro component → cutaway or x-ray → top-down flow → consequence wide.
- Use section cuts, exploded views, transparent shells, underground or underwater transitions, and matched camera moves to reveal inaccessible layers.
- Anchor arrows, dimensions, quantities, and labels to the object. Floating arrows over a generic background are insufficient.
- Give color one job. Use the accent only for the active force, flow, stress, constraint, or disputed claim.
- Show the common misconception as an actual model, then break, remove, reroute, or replace it. A red X alone is not the explanation.
- Keep one spoken idea per visible action. Short captions stay in a stable phone-safe band while the object remains dominant.
- Let the environment transform. Filling racks, extending cables, multiplying factories, opening network lanes, changing ownership edges, or collapsing capacity should change the silhouette or topology of the scene.

## Motion-density contract

For company-story mode, the percentages below are our editorial starting targets, not measurements of the reference channel:

- target at least 70% of narrated runtime as genuine subject or environment animation;
- keep traditional cards, tables, and charts to roughly 20% or less unless the chart is itself the mystery;
- change the view at semantic/action boundaries; a roughly 2–4-second cut is a useful starting hypothesis, while 5–6-second continuous explanations can be appropriate;
- avoid an unchanged hold longer than three seconds unless it is needed to recognize or understand the mechanism; a continuous causal action is not an unchanged hold;
- include at least one macro reveal, one cutaway or topology reveal, one causal transformation, and one payoff wide shot;
- use a camera move to carry the viewer to new information, not as decoration over a still image.

Count an action only when the subject, material, topology, flow, lighting state, or environment changes in a way that teaches a causal step. A pan, zoom, parallax drift, text fade, particle loop, or animated background does not count by itself.

## Renderer routing

Choose per shot rather than forcing one tool across the whole video. For realistic cinematic briefs, prefer generated footage or sufficiently detailed tested 3D. Deterministic 2D/2.5D remains useful for abstract flows and explicit previews, but does not satisfy realistic reference similarity by itself.

### Blender

Use for facilities, products, machines, construction, infrastructure, physical supply chains, believable depth, cross-sections, exploded assemblies, fluids, particles, destruction, or long camera moves through a system. Prefer procedural geometry and reusable scene rigs for racks, factories, cables, pipelines, warehouses, campuses, chips, and network equipment.

Build low-detail geometry first and prove the camera, silhouette, causal action and timing before adding materials. Inspect the opening, midpoint, peak action and exit frames, then render a short low-resolution motion proof. Bound retries and change the shot plan when the same failure persists. A 2D/2.5D fallback must be labeled as lower fidelity when the brief requires realistic imagery. A clear blockout verifies mechanism, not final visual similarity.

Prefer a prevalidated parameterized rig or subject-specific pre-rendered motion plate when it can express the frozen claim. Reject generic 3D B-roll that merely decorates the narration.

### Remotion with Three.js

When a 2.5D scene fits the visual brief, use CSS, SVG, and layered transforms. Add Three.js only for bounded geometry whose camera and object envelope can be tested deterministically. Good candidates include server racks, chip stacks, network graphs, product ecosystems, supply routes, ownership structures, and capital flows. Drive every animated property from the video frame so previews and final renders match. This route is not an automatic substitute for requested realistic footage.

### Motion Canvas or vector animation

Use for contracts, ownership, platform distribution, customer flows, regulatory gates, and money movement when dimensional depth does not add meaning. Its scene hierarchy, tweening, and time events are useful for voice-over-synchronized explanatory motion.

### Real imagery and footage

Use licensed or appropriately reusable images and clips to establish place, scale, product identity, executives, facilities, or documentary proof. Transition from the real establishing image into a matched animated model when possible. Do not hold one photo under a long narration.

### MoneyPrinterTurbo

Use selected components for Korean narration, silence editing, subtitle timing, BGM/SFX mixing, encoding, thumbnail export, and delivery QA. Do not use its ordinary infographic or stock-footage composition as the company-story motion master. In investment-story mode, reuse its valuation and verdict modules only after the animated mechanism is understood.

## Asset and environment collection

After freezing the story, extract all physical nouns and relationships from the script. Create `world-assets.json` with:

- subject, environment, component, counterparty, and state;
- required wide, macro, cutaway, and consequence appearances;
- source URL, creator, license, attribution, file hash, and allowed transformation;
- whether the asset is factual reference, direct media, generated stand-in, or conceptual model;
- scale, orientation, material, and geometry facts that must remain accurate;
- the shot and claim IDs that use it.

Search official product pages, issuer media kits, regulatory exhibits, Wikimedia Commons, public-domain archives, and reputable 3D repositories with clear item-level licenses. Search GitHub for reusable procedural rigs or render workflows, but inspect code, dependencies, license, asset provenance, and the exact commit before executing or importing anything. When no safe model exists, build a simple original model from verified dimensions or mark it as conceptual.

Do not treat an attractive model as evidence. The filing, technical documentation, or official product reference controls what the model may imply.

## Open-source production candidates

Evaluate these as implementation options; do not install or execute them without the normal dependency, license, and security review:

- Blender Geometry Nodes for procedural geometry, repeated structures, and parameterized transformations;
- `@remotion/three` with React Three Fiber for frame-accurate Three.js scenes inside Remotion;
- Motion Canvas for open-source vector animation synchronized with voice-over;
- the official Remotion Three starter for a minimal deterministic 3D composition;
- relevant Blender-to-glTF workflows for authoring in Blender and rendering repeatably in Three.js;
- `vsim` only as an experimental candidate after verifying its license, current maintenance, renderer claims, and dependency safety.

Record accepted and rejected candidates in `open-source-review.json`. Reusing code or assets requires a compatible license and preserved attribution where required.

## Story-first data presentation

Do not interrupt company-story mode with a finance dashboard unless the number changes the mechanism. Convert data into the world:

- capacity becomes lit versus dark racks;
- a purchase commitment becomes reserved factory, memory, packaging, power, or data-center lanes;
- platform distribution becomes people or devices entering a network;
- ownership becomes a persistent proportional link, separate from revenue;
- recurring revenue becomes a second cash path that activates only under the documented condition;
- concentration risk becomes the same world losing one customer or route;
- a market rumor appears as a temporary disputed layer that is peeled away to expose the public record.

Use a source excerpt as a macro proof object for one short beat, then return to the animated world. Avoid unreadable full-page filings.

## Sound and pacing

Lock narration before final animation timing. Use semantic phrases to trigger actions: object entry on the noun, motion start on the causal verb, impact or state change on the result. Add restrained mechanical, electrical, fluid, impact, or cash-flow sound cues only when they reinforce a visible action. Use BGM to sustain tension and resolution without flattening narration.

## Review gate

Before final render, show representative frames or a short low-resolution motion proof covering:

- the first impossible state;
- the hardest cutaway or topology reveal;
- the peak causal action;
- the final consequence and callback.

Review the full motion at phone size. Reject the sequence when the story still works equally well as static slides, when captions explain actions that never occur, when spatial continuity is lost, or when visual metaphors make a rumor look like a disclosed fact.
