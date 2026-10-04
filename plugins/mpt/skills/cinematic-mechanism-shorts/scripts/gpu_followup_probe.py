"""Bounded ControlNet and SVD trials, reusing the existing SDXL cache."""
import argparse, json, os, time, shutil
from pathlib import Path
os.environ['HF_HUB_DISABLE_PROGRESS_BARS'] = '1'
import torch
from huggingface_hub import HfApi, snapshot_download

def fetch(repo, target):
    info = HfApi().model_info(repo, files_metadata=True)
    names = [x.rfilename for x in info.siblings]
    selected = []
    for f in names:
        if f.endswith(('.json', '.txt')) or f == 'README.md' or f.startswith('LICENSE'):
            selected.append(f)
        elif f.endswith('.fp16.safetensors'):
            selected.append(f)
        elif f.endswith('.safetensors') and f.replace('.safetensors', '.fp16.safetensors') not in names:
            if '/' in f or f == 'diffusion_pytorch_model.safetensors':
                selected.append(f)
    size = sum(x.size or 0 for x in info.siblings if x.rfilename in selected)
    print(json.dumps({'repo':repo,'revision':info.sha,'selected_bytes':size,'files':selected}), flush=True)
    if shutil.disk_usage(target.parent).free < size + 8*1024**3:
        raise RuntimeError('Insufficient disk reserve')
    snapshot_download(repo, revision=info.sha, local_dir=str(target), allow_patterns=selected, max_workers=3)
    return info.sha, 'fp16' if any('.fp16.' in f for f in selected) else None

def main():
    p=argparse.ArgumentParser(); p.add_argument('--mode',choices=['canny','svd'],required=True);p.add_argument('--root',type=Path,required=True);p.add_argument('--input',type=Path,required=True);p.add_argument('--base-cache',type=Path);p.add_argument('--decode-chunk',type=int,default=2);p.add_argument('--suffix',default='')
    a=p.parse_args(); out=a.root/(a.mode+a.suffix);out.mkdir(parents=True,exist_ok=True)
    if a.mode=='canny' and a.base_cache is None: p.error('--base-cache is required for canny')
    if not torch.cuda.is_available(): raise RuntimeError('CUDA required')
    from PIL import Image
    image=Image.open(a.input).convert('RGB')
    metrics={'mode':a.mode,'gpu':torch.cuda.get_device_name(0),'input':str(a.input),'trials':[],'visual_review':'pending'}
    t=time.monotonic()
    if a.mode=='canny':
        import cv2,numpy as np
        from diffusers import ControlNetModel,StableDiffusionXLControlNetPipeline
        revision,variant=fetch('diffusers/controlnet-canny-sdxl-1.0',out/'model')
        cn=ControlNetModel.from_pretrained(out/'model',torch_dtype=torch.float16,variant=variant,local_files_only=True)
        pipe=StableDiffusionXLControlNetPipeline.from_pretrained('stabilityai/stable-diffusion-xl-base-1.0',cache_dir=str(a.base_cache),controlnet=cn,torch_dtype=torch.float16,variant='fp16',local_files_only=True)
        pipe.enable_sequential_cpu_offload();pipe.vae.enable_tiling()
        image=image.resize((576,1024));image.save(out/'input.png')
        edges=Image.fromarray(np.repeat(cv2.Canny(np.array(image),100,200)[:,:,None],3,axis=2));edges.save(out/'control.png')
        for scale in (0.5,1.0):
            torch.cuda.reset_peak_memory_stats(); start=time.monotonic()
            result=pipe(prompt='Photorealistic macro photograph of a machined copper liquid cooling plate, open serpentine copper channels, green circuit board on industrial test bench, copper lid raised above the plate, polished metal, precise manufacturing, realistic soft lighting',negative_prompt='text, watermark, illustration, melted metal, extra components',image=edges,controlnet_conditioning_scale=scale,num_inference_steps=25,guidance_scale=5,width=576,height=1024,generator=torch.Generator('cpu').manual_seed(20260905)).images[0]
            name=f'canny_{scale:.1f}.png';result.save(out/name)
            row={'scale':scale,'seconds':time.monotonic()-start,'peak_allocated_GiB':torch.cuda.max_memory_allocated()/1024**3,'file':name};metrics['trials'].append(row);print(json.dumps(row),flush=True)
    else:
        from diffusers import StableVideoDiffusionPipeline
        from diffusers.utils import export_to_video
        model_dir=a.root/'svd/model';model_dir.parent.mkdir(parents=True,exist_ok=True)
        revision,variant=fetch('stabilityai/stable-video-diffusion-img2vid-xt',model_dir)
        pipe=StableVideoDiffusionPipeline.from_pretrained(model_dir,torch_dtype=torch.float16,variant=variant,local_files_only=True)
        pipe.enable_model_cpu_offload();pipe.unet.enable_forward_chunking()
        image=image.resize((320,576));image.save(out/'input.png')
        torch.cuda.reset_peak_memory_stats();start=time.monotonic()
        frames=pipe(image,num_frames=25,num_inference_steps=25,decode_chunk_size=a.decode_chunk,motion_bucket_id=80,noise_aug_strength=0.02,height=576,width=320,generator=torch.Generator('cpu').manual_seed(20260905)).frames[0]
        export_to_video(frames,str(out/'svd.mp4'),fps=7)
        for i in (0,6,12,18,24): frames[i].save(out/f'frame_{i:03d}.png')
        row={'seconds':time.monotonic()-start,'peak_allocated_GiB':torch.cuda.max_memory_allocated()/1024**3,'frames':25,'decode_chunk_size':a.decode_chunk,'file':'svd.mp4'};metrics['trials'].append(row);print(json.dumps(row),flush=True)
    metrics.update(revision=revision,total_seconds=time.monotonic()-t)
    (out/'metrics.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8')
    print('PROBE_COMPLETE',flush=True)

if __name__=='__main__': main()
