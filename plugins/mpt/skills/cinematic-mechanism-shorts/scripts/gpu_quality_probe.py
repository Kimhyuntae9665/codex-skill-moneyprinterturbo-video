"""Bounded GPU quality comparison for cooling-proof.blend; no external assets.
Run: blender -b cooling-proof.blend --python gpu_quality_probe.py -- --out-dir quality
Add --clip after reviewing stills to render a 48-frame material/framing trial.
"""
import argparse, json, pathlib, sys, time
import bpy
from mathutils import Vector

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--out-dir',type=pathlib.Path,required=True)
p.add_argument('--clip',action='store_true')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
out=a.out_dir.resolve();out.mkdir(parents=True,exist_ok=True)
prefs=bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type='OPTIX';prefs.get_devices()
if not any(d.type=='OPTIX' for d in prefs.devices):raise RuntimeError('OptiX GPU required')
for d in prefs.devices:d.use=d.type=='OPTIX'
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='GPU'
s.cycles.use_denoising=True;s.cycles.denoiser='OPTIX'
s.render.use_persistent_data=True;s.render.resolution_x=1080;s.render.resolution_y=1920;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.image_settings.compression=15
s.render.threads_mode='FIXED';s.render.threads=8
log={'same_scene_comparison':['base12','base64'],'art64_changes':['machining_shader','smooth_cylinders','exposure','camera_target','lens34'],'frames':[]}
def render(name,frame,samples):
    s.cycles.samples=samples;s.render.filepath=str(out/(name+'.png'))
    start=time.perf_counter();bpy.ops.render.render(write_still=True)
    log['frames'].append({'name':name,'frame':frame,'samples':samples,'seconds':round(time.perf_counter()-start,3)})
    (out/'quality-report.json').write_text(json.dumps(log,indent=2),'utf-8')
s.frame_set(271)
if not a.clip:
    render('base12',271,12);render('base64',271,64)
mat=bpy.data.materials.get('machined copper')
if mat is None:raise RuntimeError('This probe requires the original cooling proof')
nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF')
bs.inputs['Base Color'].default_value=(.38,.145,.047,1)
bs.inputs['Roughness'].default_value=.25
for n in nt.nodes:
    if n.type=='BUMP':n.inputs['Strength'].default_value=.025;n.inputs['Distance'].default_value=.002
# Fine directional machining, preserving mesh and every channel connection.
wave=nt.nodes.new('ShaderNodeTexWave');wave.wave_type='BANDS';wave.bands_direction='X';wave.inputs['Scale'].default_value=180
bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.035;bump.inputs['Distance'].default_value=.0008
nt.links.new(wave.outputs['Color'],bump.inputs['Height']);nt.links.new(bump.outputs['Normal'],bs.inputs['Normal'])
for o in bpy.data.objects:
    if o.type=='MESH' and ('coupling' in o.name or 'tracer' in o.name or 'fastener' in o.name):
        for poly in o.data.polygons:poly.use_smooth=True
s.view_settings.exposure=-.6
def frame_art(f):
    s.frame_set(f);cam=s.camera
    cam.rotation_euler=(Vector((0,0,.19))-cam.location).to_track_quat('-Z','Y').to_euler()
    cam.keyframe_insert('rotation_euler',frame=f)
    cam.data.lens=34
    cam.data.dof.use_dof=False
frame_art(271)
if a.clip:
    for i,f in enumerate(range(271,319),1):
        frame_art(f);render('art_%04d'%i,f,64)
else:render('art64',271,64)
print('QUALITY_PROBE_COMPLETE',flush=True)
