"""Use an available NVIDIA GPU for the original cooling proof; never silently fall back."""
import bpy, pathlib, json, time, argparse, sys
p=argparse.ArgumentParser();p.add_argument('--full',action='store_true');p.add_argument('--frames',default='270,271');p.add_argument('--samples',type=int,default=12);a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
if a.samples<1:raise ValueError('samples must be positive')
root=pathlib.Path(bpy.data.filepath).resolve().parent
prefs=bpy.context.preferences.addons['cycles'].preferences
chosen=None
for backend in ['OPTIX','CUDA']:
    try:
        prefs.compute_device_type=backend;prefs.get_devices()
        gpu=[d for d in prefs.devices if d.type==backend]
        if gpu:
            chosen=backend
            for d in prefs.devices:d.use=d.type==backend
            break
    except Exception:continue
if chosen is None:raise RuntimeError('No usable NVIDIA Cycles device; stop rather than silently use CPU')
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='GPU';s.cycles.samples=a.samples;s.cycles.use_denoising=True;s.cycles.denoiser='OPTIX'
s.render.use_persistent_data=True;s.render.resolution_x=1080;s.render.resolution_y=1920;s.render.resolution_percentage=100
s.render.threads_mode='FIXED';s.render.threads=8;s.render.image_settings.file_format='PNG';s.render.image_settings.compression=0
record={'backend':chosen,'devices':[{'name':d.name,'type':d.type,'used':bool(d.use)} for d in prefs.devices],'resolution':[1080,1920],'samples':a.samples,'denoiser':'OPTIX','frames':[]}
(root/'gpu-frames').mkdir(exist_ok=True)
for f in ([int(f) for f in a.frames.split(',')] if not a.full else range(1,577)):
    s.frame_set(f);s.render.filepath=str(root/'gpu-frames'/f'f_{f:04}.png')
    t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t
    record['frames'].append({'frame':f,'seconds':round(elapsed,3)})
    (root/('gpu-render.json' if a.full else 'gpu-benchmark.json')).write_text(json.dumps(record,indent=2),'utf-8')
    print('GPU_FRAME',f,round(elapsed,3),flush=True)
print('GPU_RENDER_COMPLETE',chosen,flush=True)
