"""Check the declared support contacts of cooling-proof.blend, not full physics."""
import bpy,json,pathlib
from mathutils import Vector
s=bpy.context.scene;s.frame_set(1);bpy.context.view_layer.update()
def bounds(o):
    pts=[o.matrix_world@Vector(v) for v in o.bound_box]
    return [[min(p[i] for p in pts),max(p[i] for p in pts)] for i in range(3)]
floor_top=bounds(bpy.data.objects['floor'])[2][1]
checks=[]
for o in bpy.data.objects:
    if o.name.startswith(('table leg','CDU floor pedestal')):
        lo,hi=bounds(o)[2];target=-.47 if o.name.startswith('table leg') else -.26
        checks.append({'object':o.name,'floor_gap':lo-floor_top,'top_gap':hi-target,'pass':abs(lo-floor_top)<1e-4 and abs(hi-target)<1e-4})
    if o.name.startswith('PCB mounting pad'):
        lo,hi=bounds(o)[2]
        checks.append({'object':o.name,'table_gap':lo-(-.25),'board_gap':hi-(-.21),'pass':abs(lo+.25)<1e-4 and abs(hi+.21)<1e-4})
floating_lights=[o.name for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('ceiling light')]
result={'scope':'Named static support bounding contacts only. Not global collision, stability, CFD or perceptual QA.','unsupported_visible_light_meshes':floating_lights,'contacts':checks,'pass':not floating_lights and len(checks)==9 and all(c['pass'] for c in checks)}
path=pathlib.Path(bpy.data.filepath).parent/'environment-audit.json';path.write_text(json.dumps(result,indent=2),'utf-8')
print(json.dumps(result),flush=True)
if not result['pass']:raise RuntimeError('Environment support audit failed')
