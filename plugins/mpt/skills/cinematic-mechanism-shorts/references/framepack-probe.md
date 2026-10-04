# FramePack: bounded local experiment

This is a reproducible experiment route, not the reference channel's identified tool or an accepted mechanical-animation pipeline. Read the dated result in `gpu-quality.md` before choosing it for a shot.

Use the [official FramePack repository](https://github.com/lllyasviel/FramePack). The tested checkout is `97fe5dbe06ac1f337ece08935b1076a35eefeeb9`. Its repository license and the separate model licenses remain applicable; the skill does not redistribute model weights or the upstream implementation.

The 2026-09-05 isolated Python 3.10 environment installed PyTorch 2.14.0, torchvision 0.29.0 and the checkout's requirements, including Diffusers 0.33.1, Transformers 4.46.2 and Accelerate 1.6.0. Keep it separate from the newer SDXL/SVD environment. Native PyTorch attention was used; optional Xformers/Flash Attention/Sage Attention packages were not required to load and begin the probe.

The helper `scripts/framepack_probe.py` downloads only the components actually used by the upstream worker and records exact model revisions. In this run they totalled 42,866,789,142 bytes:

| Components | Revision | Selected bytes |
|---|---|---:|
| HunyuanVideo text encoders, tokenizers, VAE | `e8c2aaa66fe3742a32c11a6766aecbf07c56e773` | 16,261,365,987 |
| flux_redux_bfl image encoder/processor | `45b801affc54ff2af4e5daf1b282e0921901db87` | 856,507,099 |
| FramePackI2V_HY transformer | `86cef4396041b6002c957852daac4c91aaa47c79` | 25,748,916,056 |

The full base HunyuanVideo transformer is unnecessary for this worker. Do not download it in addition to the FramePack transformer. The helper checks missing cache entries and keeps an 8GiB disk reserve; also budget for the Python environment and temporary installation space. Do not infer low RAM or fast HDD loading from the advertised low VRAM requirement.

```text
python scripts/framepack_probe.py --root /path/to/FramePack --mode download
python scripts/framepack_probe.py --root /path/to/FramePack --mode encode-test
python scripts/framepack_probe.py --root /path/to/FramePack --mode infer --input /path/to/inspected-input.png
```

Run these commands from the prepared environment, using the real authorized checkout path. Inference loads the recorded local snapshot paths in offline mode and calls the upstream worker without launching its web UI. The wrapper depends on that checkout's function structure; inspect compatibility before changing the upstream revision. Reuse the download manifest to run inference without fetching weights again.

The initial 25-step inference reached VAE decoding but failed at export: torchvision 0.29.0 no longer provided the upstream `torchvision.io.write_video` function. That attempt produced no accepted video. The wrapper now uses the installed PyAV/libx264 writer, verifies a two-frame encode/decode before loading the expensive model, and saves decoded uint8 frames as `.frames.npy` before encoding. Preserve this intermediate so an export failure does not require repeating diffusion. The encoder preflight is a technical test only; it cannot certify the generated motion.

The probe asks only for a raised copper lid to descend onto its cold plate, with a fixed camera and rigid plate/board/hoses. It requests 1.2 seconds, 25 steps, seed 20260905, latent window 9, CFG 1, distilled guidance 10, guidance rescale 0, GPU memory preservation 6GiB and TeaCache off. Output dimensions/frame count must be read from the actual file. The input is the wider 34mm Blender composition, different from the 40mm source used for ControlNet and SVD. Do not call this an identical-input quality or speed benchmark.

Review the lid's motion separately from channel topology, hose attachment, camera drift, board identity and unwanted transformations. A short result cannot establish long-video identity retention. Preserve the returned file and measured cost even when the shot is rejected. If the worker catches an error and returns without producing a new MP4, treat it as failed; an MP4 left over from an earlier run is not evidence of success.

Actual repaired result: 37 frames, 480×832, 30fps, 1.233333 seconds. Total wall time 1,223.19 seconds, worker 1,130.57 seconds, peak allocated CUDA 5.116GiB. The lower channel plate moved upward instead of the upper lid closing; the board/support relation broke. Returned MP4: technical success. Requested mechanism: rejected. See `gpu-quality.md` for the resulting production choice.

The headless upstream runtime left background threads alive after writing the successful metrics. In the observed run, the task-owned Python process was terminated only after the MP4, raw-frame checkpoint and metrics existed and the MP4 had been transferred and decoded. A still-open SSH session is not necessarily ongoing diffusion. Inspect the exact process and artifacts; do not terminate unrelated processes or repeat generation merely because the CLI has not exited.
