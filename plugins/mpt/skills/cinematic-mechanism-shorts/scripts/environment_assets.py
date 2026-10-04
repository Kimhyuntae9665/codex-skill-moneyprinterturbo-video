"""Reusable grounded studio supports for the conceptual cooling example.
Not engineering CAD. Call with the scene's box factory and material.
"""
def floor_stand(box, name, xy, top_z, floor_z, footprint, material):
    if top_z <= floor_z:raise ValueError('Stand top must be above floor')
    o=box(name,(*xy,(top_z+floor_z)/2),(*footprint,top_z-floor_z),material,.015)
    o['visual_role']='physical_support';o['support_surface']='floor'
    return o

def complete_studio_supports(box, material, floor_z=-1.19):
    parts=[]
    for x in [-2.9,2.9]:
        for y in [-1.55,1.55]:
            parts.append(floor_stand(box,'table leg', (x,y),-.47,floor_z,(.18,.18),material))
    parts.append(floor_stand(box,'CDU floor pedestal',(-2.15,3.1),-.26,floor_z,(1.05,.65),material))
    # The PCB sits 0.04 units above the table: explicit insulated mounting pads.
    for x in [-1.7,1.7]:
        for y in [-1.2,1.2]:
            o=box('PCB mounting pad',(x,y,-.23),(.16,.16,.04),material,.004)
            o['visual_role']='physical_support';o['support_surface']='lab table';parts.append(o)
    return parts
