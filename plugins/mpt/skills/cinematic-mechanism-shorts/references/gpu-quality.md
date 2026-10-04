# GPU quality experiments

Use the remote GPU already authorized for this production when its current capacity permits. Check utilization and disk space first. Use one GPU-heavy job at a time on an 8GB machine; preserve existing environments, artifacts, and unrelated jobs. This permission covers relevant video/image experiments, not unrelated computing or paid cloud resources.

## A bounded comparison before a long render

1. Freeze the source geometry, camera, output size, denoiser and frame. Render a low/high sample pair. This isolates sampling quality; timings include first-frame initialization and are not a clean hardware speed benchmark.
2. If the remaining weakness is artistic, make a separately labeled material/light/framing variant. Never attribute its change to sample count alone.
3. Review the whole portrait image and critical connections at full size. Reject clipped ports, hidden channels, illegible contrasts and material changes that imply a different mechanism.
4. Render 2–4 seconds of the selected variant. Inspect motion, temporal noise and the transition to adjacent shots before paying for a full episode.
5. Keep `executed`, `visually_accepted`, `motion_reviewed`, `listening_reviewed` separate in the report. Store scripts, seed/settings, runtime, output paths and the reason for adoption/rejection.

For the included conceptual cooling rig:

```text
blender -b cooling-proof.blend --python scripts/gpu_quality_probe.py -- --out-dir quality
blender -b cooling-proof.blend --python scripts/gpu_quality_probe.py -- --out-dir quality-motion --clip
```

The first command compares 12/64 samples and a separate art-direction variant. The second produces 48 frames at 24fps. These examples require OptiX and the supplied cooling model; they are not a universal scene upgrader. Encode with the existing FFmpeg workflow, avoiding a silent replacement of the user's previous video.

## Controlled image-to-image trials

`scripts/gpu_img2img_probe.py` uses existing SDXL base weights and an inspected original frame. It tests strengths 0.18/0.30/0.45 with a fixed seed at 768×1368. Use `--input`, `--cache-dir`, `--out-dir` explicitly. It requires the existing CUDA/Diffusers environment.

According to the [official Diffusers guide](https://huggingface.co/docs/diffusers/en/using-diffusers/img2img), higher strength changes more of the input and also changes effective denoising steps. A low value is not a topology guarantee. Reject changed wall attachments, missing markers, invented fasteners or bent connectors. Keep a generated still as mood/reference only when it fails the explanatory structure.

Independent image-to-image processing of every frame does **not** establish temporal consistency. Do not turn a good single-frame result into a claim of a working video pipeline. Depth/edge conditioning, a tested video model or deterministic 3D remain separate routes that require their own short motion tests.

Do not fit a large video model merely because CUDA exists. On 8GB, check model-specific peak memory and available host RAM/disk before downloading; use the existing cache for the first experiment. If the limiting factor is model obedience or asset design, document it rather than pretending more computation fixed it.

## 2026-09-05 measured follow-up

The original cooling scene ran at 1080×1920 on RTX 4060 8GB. The 12/64 sample pair took 2.100/3.234 seconds (initialization not isolated). A separate material variant took 3.338 seconds. The revised 34mm-camera, 64-sample 48-frame trial took 148.38 seconds in summed render calls. Six sampled frames were inspected; full real-time playback was not performed.

SDXL strengths 0.18/0.30/0.45 took 11.859/11.140/12.993 seconds and peaked at 5.367GiB allocated memory. Low strength offered little gain, medium strength invented small components, and high strength turned markers into hole-like details. None was adopted. These results apply to this input and seed, not all SDXL prompts. Material/framing changes were retained as a useful partial improvement, not proof of reference-quality photorealism.

## Additional ControlNet trial, 2026-09-05

The same inspected copper-plate source was tested with `diffusers/controlnet-canny-sdxl-1.0`, revision `eb115a19a10d14909256db740ed109532ab1483c`, using the already cached SDXL base. Downloaded only the ControlNet FP16 weight/config/card (2,502,144,025 bytes). The public [model card](https://huggingface.co/diffusers/controlnet-canny-sdxl-1.0) describes Canny conditioning; it does not promise correct plumbing or temporal consistency.

On RTX 4060 8GB, ordinary model CPU offload failed with CUDA OOM while loading the combined inference components. Sequential CPU offload completed two 576×1024 stills, 25 steps, seed 20260905, Canny thresholds 100/200, guidance 5. Conditioning scales 0.5/1.0 took 59.63/55.91 seconds; both peaked at 2.188 GiB allocated CUDA memory. These times exclude model download and initial loading; reserved/device-wide memory is a different measure.

Both images were inspected. Strong conditioning kept much of the channel outline, but altered the left connection and circuit-board components; symbolic colored tracers lost their intended role. Neither was accepted as mechanical proof. Classify as a material/reference experiment only. Remove composited symbols from the generation input and add them after approved geometry footage; a prompt asking for no extra components is not sufficient validation. Single-frame success would still require a separate motion test.

Route generation by the risk of the shot: an invented generic room can be an establishing-shot candidate after inspection, while a claimed port, valve or flow path needs preserved geometry. For the latter, retain the authored mechanism and consider generating only surroundings/material references. This compositing route is a production proposal, not a tested end-to-end solution. Never label a generated generic facility as the actual company's building. Model installation and a returned file do not authorize a switch in the factual meaning of the image.

## Additional SVD trial, 2026-09-05

`stabilityai/stable-video-diffusion-img2vid-xt`, revision `9e43909513c6714f1bc78bcb44d96e733cd242aa`, downloaded 4,509,208,849 selected bytes, reusing the dedicated CUDA environment. The [official model card](https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt) states that SVD is image-conditioned and cannot be controlled through text. It is therefore a temporal appearance test, not a prompt-following mechanism controller.

The same portrait source generated 25 frames at 320×576, 25 steps, seed 20260905, motion bucket 80, noise augmentation 0.02, model CPU offload, UNet forward chunking, decode chunk size 2. Generation took 71.48 seconds and peaked at 4.458 GiB allocated CUDA memory; download/loading excluded. The MP4 was encoded at 7fps (about 3.57 seconds), not the source video's frame rate.

All 25 frames were inspected as a contact sheet. Severe smoothing and moving bands changed the apparent plate/board geometry. Not accepted for the explanatory shot. This low-resolution portrait smoke test is not a controlled evaluation at the model's native landscape training resolution and does not prove all SVD outputs fail. It does establish that this output cannot be used to explain the channels. Do not use interpolated/upscaled copies to conceal a changed mechanism.

A same-input/seed retry changed only decode chunk size from 2 to 8. All 25 returned frames were inspected; moving bands, changing edge colors and locally blurred geometry remained, so the retry was also rejected. It did not resolve the defect. Peak allocated CUDA memory remained 4.458 GiB. The measured pipeline call took 659.32 seconds while model download/installation competed for a rotational disk; CPU-offloaded weights incurred disk reads inside that call. Do not compare this wall time against 71.48 seconds as a decoder speed benchmark. No full normal-speed playback or listening review was performed for these silent tests.
# Final route decision after FramePack · 2026-09-05

The repaired FramePack export returned a 480×832, 37-frame, 30fps, 1.233333s MP4. Pipeline wall time was 1,223.19s, worker time 1,130.57s, peak CUDA allocation 5.116GiB. The 25-step sampling loop took about 913s; disk loading/offload and decoding are included in broader times. The first attempt had already spent 1,294.81s before failing at the removed torchvision writer. These costs are not a controlled GPU-speed comparison against SVD or Blender.

All 37 decoded frames were inspected in sequence as a contact sheet, with the end state separately available. The upper lid remained raised while the lower channel plate lifted off the board, exposing a dark rectangle. Some initial appearance survived better than the tested SVD, but the commanded actor/action and fixed-body support failed. **Reject this clip for mechanism explanation.** The tiny duration does not establish longer-term identity preservation; silent probe listening is not applicable, and normal-speed playback was not claimed.

For the present 8GB GPU production route, choose authored Blender rigs for geometry-critical cause/effect, sourced real product/identity inserts, and diverse explanatory sets. SDXL/ControlNet may supply inspected art references; generative I2V remains experimental for atmosphere where exact topology is nonessential. Do not silently promote an atmospheric shot into a mechanism proof. A stronger model is a future candidate only after the same actor/action/support test passes.

The immediate quality investment is art direction and visible events across distinct spaces, not another large download. Preserve failures, settings and raw decoded frames so that future model changes can be tested against the same defect. The full motion/image comparison and dated judgments accompany the research package.
