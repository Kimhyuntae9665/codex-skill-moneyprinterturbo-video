"""Original parameterized mechanism proof. Blender 5.2.1, no external assets.
The geometry is a teaching model of single-phase cold-plate cooling, not a vendor CAD model.
Blue/orange beads are disclosed flow tracers, not literal solids in coolant.
"""
import bpy, math, random, pathlib, sys, json
from mathutils import Vector
import argparse
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from environment_assets import complete_studio_supports
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('mode',nargs='?',choices=['build','stills','render'],default='build')
parser.add_argument('--out',type=pathlib.Path,default=pathlib.Path.cwd()/'cooling-proof')
options=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=options.out.resolve();OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
S=bpy.context.scene;S.render.engine='CYCLES';S.cycles.samples=6;S.cycles.use_denoising=True;S.render.use_persistent_data=True
S.render.resolution_x=720;S.render.resolution_y=1280;S.render.resolution_percentage=100
S.render.fps=24;S.frame_start=1;S.frame_end=576
S.world.color=(.16,.18,.22)
S.view_settings.view_transform='AgX'
def mat(name,color,metal=0,rough=.4,emission=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 if emission:p.inputs['Emission Color'].default_value=(*color,1);p.inputs['Emission Strength'].default_value=emission
 return m
COPPER=mat('machined copper',(.52,.21,.075),.84,.3)
noise=COPPER.node_tree.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=160
bump=COPPER.node_tree.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.12;bump.inputs['Distance'].default_value=.008
COPPER.node_tree.links.new(noise.outputs['Fac'],bump.inputs['Height']);COPPER.node_tree.links.new(bump.outputs['Normal'],COPPER.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
METAL=mat('brushed nickel',(.45,.5,.55),.85,.27)
BLACK=mat('black anodized chassis',(.027,.037,.044),.7,.3)
PCB=mat('dark green circuit board',(.018,.08,.055),.25,.42)
CHIP=mat('chip package',(.016,.02,.025),.35,.25)
GOLD=mat('gold contacts',(.52,.34,.075),.8,.25)
BLUE=mat('cool tracer',(.025,.4,.8),.3,.24,.35)
ORANGE=mat('warm tracer',(.85,.2,.025),.3,.24,.35)
HOSE=mat('rubber hoses',(.018,.027,.033),.12,.42)
FLOOR=mat('concrete floor',(.18,.21,.24),.1,.55)
def box(name,loc,size,material,bevel=.02):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material)
 if bevel:md=o.modifiers.new('machined edge','BEVEL');md.width=bevel;md.segments=3;o.modifiers.new('weighted normals','WEIGHTED_NORMAL')
 return o
def cyl(name,a,b,r,material,verts=20):
 a,b=Vector(a),Vector(b);v=b-a;bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=r,depth=v.length,location=(a+b)/2);o=bpy.context.object;o.name=name;o.rotation_euler=v.to_track_quat('Z','Y').to_euler();o.data.materials.append(material);return o
def tube(name,pts,r,material):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=16;cu.bevel_depth=r;cu.bevel_resolution=3;sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,v in zip(sp.points,pts):p.co=(*v,1)
 o=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(o);o.data.materials.append(material);return o
def key(o,frame,loc):o.location=loc;o.keyframe_insert('location',frame=frame)
def camera(name,loc,target,lens):
 bpy.ops.object.camera_add(location=loc);o=bpy.context.object;o.name=name;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();o.data.lens=lens;return o
def camkey(o,frame,loc,target):
 o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();o.keyframe_insert('location',frame=frame);o.keyframe_insert('rotation_euler',frame=frame)
box('lab table',(0,0,-.36),(7,4,.22),BLACK)
box('PCB',(0,0,-.16),(3.9,2.8,.1),PCB)
box('GPU package',(0,0,-.045),(1.1,.9,.12),CHIP)
box('cold plate base',(0,0,.075),(2.6,1.94,.14),COPPER)
# Five alternating separator walls produce six connected lanes.
for j in range(5):
 y=-.64+j*.32
 x=-.13 if j%2==0 else .13
 box('channel divider %d'%j,(x,y,.22),(2.30,.055,.16),COPPER,.016)
for y in [-.94,.94]:box('perimeter long',(0,y,.22),(2.6,.065,.16),COPPER,.015)
for x in [-1.27,1.27]:box('perimeter short',(x,0,.22),(.065,1.94,.16),COPPER,.015)
lid=box('lifted copper lid',(0,0,.365),(2.6,1.94,.12),COPPER)
key(lid,1,(0,0,.365));key(lid,85,(0,0,.365));key(lid,135,(0,2.7,1.35));key(lid,360,(0,2.7,1.35));key(lid,410,(0,0,.365))
for x in [-1.17,1.17]:
 for y in [-.83,.83]:
  screw=cyl('retained fastener',(x,y,.42),(x,y,.48),.065,METAL)
  screw.parent=lid;screw.matrix_parent_inverse=lid.matrix_world.inverted()
  box('mount lug',(x,y,.015),(.25,.25,.1),METAL)
random.seed(19)
for side in [-1,1]:
 for j in range(12):
  x=-1.6+j*.29
  box('memory package',(x,side*1.17,-.075),(.21,.21,.11),CHIP,.007)
  for k in range(4):box('solder',(x-.075+k*.05,side*1.315,-.094),(.025,.045,.018),METAL,.002)
for j in range(45):box('edge contact',(-1.72+j*.078,-1.37,-.097),(.045,.16,.01),GOLD,.001)
for j in range(60):
 x=random.uniform(-1.88,1.88);y=random.uniform(-1.28,1.28)
 if abs(x)<1.4 and abs(y)<1:continue
 box('SMD',(x,y,-.075),(.055,.032,.037),METAL,.003)
# Inlet to first lane, outlet from final lane. Both hoses remain connected.
tube('supply hose',[(-1.26,-.8,.22),(-1.8,-.8,.22),(-2.05,-.6,.1),(-2.35,0,.1),(-2.35,2,.25),(-2.5,2.7,.6)],.085,HOSE)
tube('return hose',[(-1.26,.8,.22),(-1.7,.8,.22),(-1.9,1.05,.2),(-1.9,2,.3),(-1.85,2.7,.6)],.085,HOSE)
for y in [-.8,.8]:
 cyl('hose coupling',(-1.25,y,.22),(-1.63,y,.22),.125,METAL)
 cyl('blue inlet / orange outlet band',(-1.65,y,.22),(-1.73,y,.22),.108,BLUE if y<0 else ORANGE)
box('CDU teaching model',(-2.15,3.1,.64),(1.2,.75,1.8),METAL,.055)
for i in range(16):box('CDU vent',(-2.15,2.706,.15+i*.06),(.9,.025,.019),BLACK,.003)
box('CDU panel',(-2.15,2.71,1.21),(.68,.026,.28),CHIP)
# Full environment, keeping the mechanism readable.
box('floor',(0,4,-1.24),(18,20,.1),FLOOR)
for x in [-4.8,4.8]:
 for y in [1,3,5,7]:
  box('rack frame',(x,y,.68),(1.15,1.45,3.75),BLACK,.045)
  for j in range(12):
   box('server tray',(x,y-.745,-.95+j*.27),(1.04,.12,.2),METAL,.005)
   box('status led',(x+.4,y-.818,-.95+j*.27),(.03,.008,.015),BLUE,.002)
# Open studio teaching scene: off-camera area lighting, no unsupported visible
# emissive strips pretending to be mounted ceiling fixtures.
complete_studio_supports(box,BLACK)
for loc,power,size in [((1,-4,7),1500,6),((-5,0,4),1200,5),((0,4,5),1600,4)]:
 bpy.ops.object.light_add(type='AREA',location=loc);l=bpy.context.object;l.data.energy=power;l.data.shape='DISK';l.data.size=size;l.rotation_euler=(Vector((0,0,.1))-l.location).to_track_quat('-Z','Y').to_euler()
# Tracers travel continuously through each connected lane; no flow through walls.
pts=[]
for j in range(6):
 y=-.8+j*.32;xs=[-1.13,1.13] if j%2==0 else [1.13,-1.13]
 if j==0:pts.append((xs[0],y,.23))
 pts.append((xs[1],y,.23))
 if j<5:pts.append((xs[1],y+.32,.23))
lengths=[(Vector(b)-Vector(a)).length for a,b in zip(pts,pts[1:])];total=sum(lengths)
def pos(t):
 dist=t*total
 for i,L in enumerate(lengths):
  if dist<=L:return Vector(pts[i]).lerp(Vector(pts[i+1]),dist/L)
  dist-=L
 return Vector(pts[-1])
for j in range(15):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=6,radius=.045);o=bpy.context.object;o.name='conceptual coolant tracer';o.data.materials.append(BLUE)
 for f in range(1,577):
  t=((f-160)/130+j/15)%1;visible=155<=f<=352 and .025<t<.975
  o.location=pos(t);o.scale=(1,1,1) if visible else (0,0,0);o.keyframe_insert('location',frame=f);o.keyframe_insert('scale',frame=f)
  o.active_material=BLUE if t<.5 else ORANGE
 # Material switch cannot be keyed safely per object shared material. Use separate material per tracer.
 mm=mat('tracer gradient '+str(j),(.025,.4,.8),0,.8,1);o.data.materials.clear();o.data.materials.append(mm);node=mm.node_tree.nodes.new('ShaderNodeEmission');node.inputs['Strength'].default_value=1
 mm.node_tree.links.new(node.outputs[0],mm.node_tree.nodes.get('Material Output').inputs['Surface'])
 for f in range(1,577,3):
  t=((f-160)/130+j/15)%1;c=(.025*(1-t)+.85*t,.4*(1-t)+.2*t,.8*(1-t)+.025*t,1)
  node.inputs['Color'].default_value=c;node.inputs['Color'].keyframe_insert('default_value',frame=f)
wide=camera('wide',(5,-8,5.5),(0,.3,.4),42)
camkey(wide,1,(5,-8,5.5),(0,.2,.45));camkey(wide,96,(3.8,-6.8,4.6),(0,.15,.4))
macro=camera('reveal',(3.2,-4.7,4.2),(0,0,.5),50)
camkey(macro,97,(3.2,-4.7,4.2),(0,0,.5));camkey(macro,216,(2.6,-4.1,4.3),(0,0,.3))
top=camera('flow',(0,-2.1,5.3),(0,0,.15),40)
camkey(top,217,(0,-2.1,5.3),(0,0,.15));camkey(top,336,(.6,-1.9,5.2),(0,0,.15))
back=camera('closed loop',(4,-7,5.2),(-.8,1,.5),37)
camkey(back,337,(4,-7,5.2),(-.8,1,.5));camkey(back,456,(4.5,-8,5.5),(-.8,1,.5))
pay=camera('payoff',(5,-8,5.5),(0,.2,.45),42)
camkey(pay,457,(3.8,-6.8,4.6),(0,.15,.4));camkey(pay,576,(5,-8,5.5),(0,.2,.45))
for f,cam in [(1,wide),(97,macro),(217,top),(337,back),(457,pay)]:mk=S.timeline_markers.new(cam.name,frame=f);mk.camera=cam
S.camera=wide
for o in bpy.data.objects:
 if o.animation_data and o.animation_data.action:
  try:
   for fc in o.animation_data.action.fcurves:
    for kp in fc.keyframe_points:kp.interpolation='LINEAR'
  except AttributeError:pass
S.render.image_settings.file_format='PNG';S.render.filepath=str(OUT/'frames'/'f_')
(OUT/'frames').mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'cooling-proof.blend'))
if options.mode=='stills':
 for f in [48,160,270,400,520]:S.frame_set(f);S.render.filepath=str(OUT/f'frame_{f}.png');bpy.ops.render.render(write_still=True)
elif options.mode=='render':bpy.ops.render.render(animation=True)
print('PROOF_READY',flush=True)
