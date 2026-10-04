"""Compare SDXL denoising strengths against an original, inspected 3D frame.
This is a still-image experiment, not temporally consistent video processing.
"""
import argparse,json,pathlib,time
import torch
from PIL import Image
from diffusers import StableDiffusionXLImg2ImgPipeline
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--input',type=pathlib.Path,required=True)
p.add_argument('--cache-dir',type=pathlib.Path,required=True)
p.add_argument('--out-dir',type=pathlib.Path,required=True)
a=p.parse_args();a.out_dir.mkdir(parents=True,exist_ok=True)
if not torch.cuda.is_available():raise RuntimeError('CUDA required; no CPU fallback')
im=Image.open(a.input).convert('RGB').resize((768,1368),Image.Resampling.LANCZOS)
pipe=StableDiffusionXLImg2ImgPipeline.from_pretrained('stabilityai/stable-diffusion-xl-base-1.0',torch_dtype=torch.float16,variant='fp16',use_safetensors=True,cache_dir=a.cache_dir,token=False)
pipe.enable_model_cpu_offload();pipe.vae.enable_tiling()
prompt='A realistic macro photograph of precisely machined copper cold plate on a dark green server circuit board, five alternating connected copper divider walls, six serpentine channels, identical geometry to the reference, brushed copper machining marks, subtle metal reflections, dark laboratory table, crisp technical product photography, small blue and orange symbolic flow markers remain visible.'
negative='text, letters, logo, extra channels, disconnected walls, melted metal, warped board, illustration, toy, clutter, added parts'
log={'input':a.input.name,'model':'SDXL base 1.0','seed':20260905,'steps':30,'size':[768,1368],'prompt':prompt,'negative_prompt':negative,'trials':[]}
for strength in [.18,.30,.45]:
    torch.cuda.reset_peak_memory_stats();start=time.perf_counter()
    result=pipe(prompt=prompt,negative_prompt=negative,image=im,strength=strength,num_inference_steps=30,guidance_scale=5,generator=torch.Generator('cpu').manual_seed(log['seed'])).images[0]
    torch.cuda.synchronize();name='img2img_%02d.png'%round(strength*100);result.save(a.out_dir/name)
    log['trials'].append({'strength':strength,'filename':name,'seconds':round(time.perf_counter()-start,3),'peak_gib':round(torch.cuda.max_memory_allocated()/1024**3,3),'review':'pending'})
    (a.out_dir/'img2img-report.json').write_text(json.dumps(log,indent=2),'utf-8')
print('IMG2IMG_PROBE_COMPLETE',flush=True)
