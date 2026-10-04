"""Audit this skill's conceptual Blender rig, not a fluid or product simulation.
Run Blender -b cooling-proof.blend --python audit_cooling_geometry.py -- --out report.json
"""
import argparse, json, pathlib, sys
import bpy
from mathutils import Vector

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--out', type=pathlib.Path, required=True)
a = p.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
dividers = sorted((o for o in bpy.data.objects if o.name.startswith('channel divider')), key=lambda o: o.name)
tracers = [o for o in bpy.data.objects if o.name.startswith('conceptual coolant tracer')]
errors = []
if len(dividers) != 5:
    errors.append('Expected five alternating dividers')
if len(tracers) != 15:
    errors.append('Expected fifteen symbolic tracers')

def bounds(o):
    points = [o.matrix_world @ Vector(v) for v in o.bound_box]
    return [min(v[i] for v in points) for i in range(3)], [max(v[i] for v in points) for i in range(3)]

walls = []
for j, o in enumerate(dividers):
    lo, hi = bounds(o)
    # Inner face of the side walls is at +/- 1.2375 model units.
    attached = lo[0] <= -1.2375 if j % 2 == 0 else hi[0] >= 1.2375
    turn_gap = 1.2375 - hi[0] if j % 2 == 0 else lo[0] + 1.2375
    if not attached:
        errors.append(o.name + ': unintended bypass at attached side')
    if turn_gap < .09:
        errors.append(o.name + ': insufficient clearance for tracer diameter')
    walls.append({'name': o.name, 'bounds': [lo, hi], 'attached': attached, 'turn_gap': turn_gap})

visible_samples = 0
min_divider_clearance = 1e9
for frame in range(155, 353):
    bpy.context.scene.frame_set(frame)
    for o in tracers:
        if max(o.scale) < .5:
            continue
        visible_samples += 1
        v = o.location
        radius = .045
        if not (-1.2375 + radius <= v.x <= 1.2375 - radius and -.9075 + radius <= v.y <= .9075 - radius):
            errors.append(f'frame {frame}: {o.name} outside inner perimeter')
        for w in walls:
            lo, hi = w['bounds']
            distance = sum(max(lo[i] - v[i], 0, v[i] - hi[i]) ** 2 for i in range(3)) ** .5
            min_divider_clearance = min(min_divider_clearance, distance - radius)
            if distance < radius - 1e-5:
                errors.append(f'frame {frame}: {o.name} intersects {w["name"]}')

result = {
    'geometry_status': 'fail' if errors else 'pass',
    'blender_version': bpy.app.version_string,
    'divider_count': len(dividers), 'tracer_count': len(tracers),
    'tested_frames': [155, 352], 'visible_tracer_samples': visible_samples,
    'minimum_tracer_to_divider_clearance': min_divider_clearance,
    'walls': walls, 'errors': errors[:30], 'error_count': len(errors),
    'scope': 'nominal model-space bounds and integer-frame symbolic tracer positions',
    'not_verified': [
        'fluid dynamics, pressure, temperature or performance',
        'vendor-specific CAD or manufacturing dimensions',
        'bored hose connectors: connectors are schematic exterior geometry',
        'subframe interpolation or camera/text occlusion',
        'photorealism, narration or full-video perceptual quality'
    ]
}
a.out.parent.mkdir(parents=True, exist_ok=True)
a.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
if errors:
    raise RuntimeError('Cooling geometry audit failed')
