"""
Correct render: import camera STL at 0.001 scale (mm->m) to match the scene,
then render using the same ortho camera setup as render_zr_v2.py view 03.
"""
import bpy, math, json
from mathutils import Vector
from pathlib import Path

ROOT   = Path(r'C:\nikon_cage_cad')
STL_IN = str(ROOT / 'exports' / 'r2' / 'camera_aligned.stl')
OUT    = ROOT / 'exports' / 'r2'
RENDERS= ROOT / 'renders' / 'r2'

# ── Remove old wrong-scale NikonZR if present ─────────────────────────────
for obj in list(bpy.data.objects):
    if 'nikonzr' in obj.name.lower() or 'nikon' in obj.name.lower():
        bpy.data.objects.remove(obj, do_unlink=True)

# ── Import STL at correct scale (mm -> m) ─────────────────────────────────
bpy.ops.wm.stl_import(filepath=STL_IN, global_scale=0.001)
cam_obj = bpy.context.selected_objects[0]
cam_obj.name = 'NikonZR_body'

import mathutils
bb_world = [cam_obj.matrix_world @ mathutils.Vector(c) for c in cam_obj.bound_box]
xs = [v.x for v in bb_world]; ys = [v.y for v in bb_world]; zs = [v.z for v in bb_world]
print(f"Camera body in scene (m): X {min(xs):.3f}-{max(xs):.3f}  Y {min(ys):.3f}-{max(ys):.3f}  Z {min(zs):.3f}-{max(zs):.3f}")

# ── Material: translucent silver ──────────────────────────────────────────
mat = bpy.data.materials.new('NikonZR_mat')
mat.use_nodes = True
mat.blend_method = 'BLEND'
bsdf = mat.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (0.78, 0.81, 0.84, 1.0)
bsdf.inputs['Roughness'].default_value  = 0.28
bsdf.inputs['Metallic'].default_value   = 0.08
bsdf.inputs['Alpha'].default_value      = 0.82
cam_obj.data.materials.clear()
cam_obj.data.materials.append(mat)

# ── Save updated blend ────────────────────────────────────────────────────
blend_out = str(OUT / 'zr_with_real_camera.blend')
bpy.ops.wm.save_as_mainfile(filepath=blend_out)
print(f"Saved: {blend_out}")

# ── Render: hero view (same angle as existing 01_hero_cage.png) ───────────
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 48
scene.cycles.use_denoising = True
scene.render.resolution_x = 1800
scene.render.resolution_y = 1400

# Find or fix render camera
render_cam = bpy.data.objects.get('Review camera')
if render_cam is None:
    for obj in bpy.data.objects:
        if obj.type == 'CAMERA':
            render_cam = obj
            break
if render_cam is None:
    cd = bpy.data.cameras.new('Review camera')
    cd.type = 'ORTHO'
    cd.clip_start = 0.001
    cd.clip_end = 1000
    render_cam = bpy.data.objects.new('Review camera', cd)
    bpy.context.collection.objects.link(render_cam)

scene.camera = render_cam
camdata = render_cam.data
camdata.type = 'ORTHO'
camdata.clip_start = 0.001
camdata.clip_end = 1000
camdata.ortho_scale = 0.27

def aim(obj, pt):
    obj.rotation_euler = (Vector(pt) - obj.location).to_track_quat('-Z','Y').to_euler()

# Hero 3/4 view
render_cam.location = (0.25, 0.32, 0.23)
aim(render_cam, (0, 0, 0.042))

scene.render.filepath = str(RENDERS / 'camera_in_cage_hero.png')
print("Rendering hero view...")
bpy.ops.render.render(write_still=True)
print("Done: camera_in_cage_hero.png")

# Front view (lens-facing)
render_cam.location = (0, 0.45, 0.045)
aim(render_cam, (0, 0, 0.045))
camdata.ortho_scale = 0.24
scene.render.filepath = str(RENDERS / 'camera_in_cage_front.png')
print("Rendering front view...")
bpy.ops.render.render(write_still=True)
print("Done: camera_in_cage_front.png")
