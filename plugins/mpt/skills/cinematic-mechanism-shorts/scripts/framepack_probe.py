"""Headless bounded upstream FramePack worker; no public UI or login."""
import argparse, json, os, shutil, sys, time
from pathlib import Path
os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'

def write_rgb_frames(frames,path,fps=30,crf=18):
    import av
    with av.open(str(path),'w') as container:
        stream=container.add_stream('libx264',rate=fps)
        stream.width=frames.shape[2];stream.height=frames.shape[1]
        stream.pix_fmt='yuv420p';stream.options={'crf':str(crf)}
        for rgb in frames:
            for packet in stream.encode(av.VideoFrame.from_ndarray(rgb,format='rgb24')):container.mux(packet)
        for packet in stream.encode():container.mux(packet)

def encoder_preflight(out):
    import numpy as np,av
    path=out/'encoder-preflight.mp4'
    frames=np.zeros((2,16,16,3),dtype=np.uint8);frames[0,:,:,0]=255;frames[1,:,:,2]=255
    write_rgb_frames(frames,path)
    with av.open(str(path)) as container:decoded=list(container.decode(video=0))
    if len(decoded)!=2 or decoded[0].width!=16:raise RuntimeError('Encoder preflight failed')
    print('ENCODER_PREFLIGHT_PASS',flush=True)

def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--mode',choices=['download','infer','encode-test'],required=True);p.add_argument('--input',type=Path)
    a=p.parse_args();root=a.root.resolve();out=root/'probe';out.mkdir(exist_ok=True)
    manifest=out/'download-manifest.json'
    if a.mode=='download':
        from huggingface_hub import HfApi,snapshot_download,try_to_load_from_cache
        specs=[('hunyuanvideo-community/HunyuanVideo',('text_encoder/','text_encoder_2/','tokenizer/','tokenizer_2/','vae/')),('lllyasviel/flux_redux_bfl',('feature_extractor/','image_encoder/')),('lllyasviel/FramePackI2V_HY',('',))]
        jobs=[]
        for repo,prefixes in specs:
            info=HfApi().model_info(repo,files_metadata=True)
            files=[f for f in info.siblings if f.rfilename.startswith(prefixes) and f.rfilename.endswith(('.json','.safetensors','.txt','.model'))]
            missing=0
            for f in files:
                cached=try_to_load_from_cache(repo,f.rfilename,revision=info.sha,cache_dir=root/'hf_download/hub')
                if not isinstance(cached,str) or not Path(cached).is_file():missing+=f.size or 0
            jobs.append({'repo':repo,'revision':info.sha,'bytes':sum(f.size or 0 for f in files),'missing_bytes':missing,'files':[f.rfilename for f in files]})
        total=sum(j['bytes'] for j in jobs)
        print(json.dumps({'selected_bytes':total,'free_bytes':shutil.disk_usage(root).free,'jobs':jobs}),flush=True)
        if sum(j['missing_bytes'] for j in jobs)+8*1024**3>shutil.disk_usage(root).free: raise RuntimeError('Disk reserve would be consumed')
        for job in jobs:
            print('DOWNLOAD_BEGIN',job['repo'],flush=True)
            job['path']=snapshot_download(job['repo'],revision=job['revision'],allow_patterns=job['files'],cache_dir=root/'hf_download/hub',max_workers=2)
            manifest.write_text(json.dumps(jobs,indent=2),encoding='utf-8')
            print('DOWNLOAD_DONE',job['repo'],flush=True)
        return
    encoder_preflight(out)
    if a.mode=='encode-test':return
    if a.input is None:p.error('--input required')
    jobs=json.loads(manifest.read_text());os.environ['HF_HUB_OFFLINE']='1';os.environ['TRANSFORMERS_OFFLINE']='1'
    source=(root/'demo_gradio.py').read_text().split('\ndef process(')[0]
    source=source.replace('from diffusers_helper.hf_login import login','')
    for j in jobs:
        if not j.get('path'):raise RuntimeError('Download incomplete')
        source=source.replace(repr(j['repo']),repr(j['path'])).replace('"'+j['repo']+'"',repr(j['path']))
    os.chdir(root);sys.path.insert(0,str(root));sys.argv=['demo_gradio.py']
    ns={'__file__':str(root/'demo_gradio.py'),'__name__':'framepack_probe_runtime'}
    start=time.monotonic();exec(compile(source,str(root/'demo_gradio.py'),'exec'),ns)
    ns['outputs_folder']=str(out)
    import torch,numpy as np
    from PIL import Image
    def save_probe_pixels(x,output_filename,fps=30,crf=18):
        if x.shape[0]!=1:raise ValueError('This bounded probe supports one video')
        frames=((x[0].float().clamp(-1,1)*127.5+127.5).permute(1,2,3,0).detach().cpu().to(torch.uint8).numpy())
        np.save(Path(output_filename).with_suffix('.frames.npy'),frames)
        write_rgb_frames(frames,output_filename,fps,crf)
        return frames
    ns['save_bcthw_as_mp4']=save_probe_pixels
    prompt='The raised copper lid above the open cold plate moves down and settles onto the plate, covering the serpentine channels. The copper plate, circuit board and hoses remain rigid and connected. Only the lid moves. Locked camera, realistic industrial lighting.'
    existing=set(out.glob('*.mp4'))
    torch.cuda.reset_peak_memory_stats();sample_start=time.monotonic()
    ns['worker'](np.array(Image.open(a.input).convert('RGB')),prompt,'',20260905,1.2,9,25,1.0,10.0,0.0,6.0,False,18)
    files=sorted((f for f in out.glob('*.mp4') if f not in existing and f.name[:6].isdigit()),key=lambda f:f.stat().st_mtime)
    metrics={'total_seconds':time.monotonic()-start,'worker_seconds':time.monotonic()-sample_start,'peak_allocated_GiB':torch.cuda.max_memory_allocated()/1024**3,'outputs':[str(f) for f in files],'prompt':prompt,'seed':20260905,'steps':25,'requested_seconds':1.2,'teacache':False,'preserved_gpu_GiB':6,'status':'returned_video' if files else 'failed','visual_review':'pending'}
    (out/'metrics.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8');print(json.dumps(metrics),flush=True)
    if not files:raise RuntimeError('Worker produced no video; inspect traceback')

if __name__=='__main__':main()
