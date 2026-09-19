import bpy, struct, numpy as np, math
from mathutils import Vector
from pathlib import Path

ROOT    = Path(r'C:\nikon_cage_cad')
STL_IN  = ROOT / 'nikon zr' / 'obj_1_NikonZR.stl'
RENDERS = ROOT / 'renders' / 'r2'
OUT     = ROOT / 'exports' / 'r2'

SCALE    = 0.001
DECIMATE = 2   # 1-in-2 -> ~1M triangles, much smoother

print("Reading STL...", flush=True)
raw    = STL_IN.read_bytes()
n_tris = (len(raw) - 84) // 50
print(f"  {n_tris:,} total triangles -> keeping {n_tris//DECIMATE:,}", flush=True)

dt   = np.dtype([('n','<f4',3),('v0','<f4',3),('v1','<f4',3),('v2','<f4',3),('a','<u2')])
tris = np.frombuffer(raw, dtype=dt, count=n_tris, offset=84)
tris = tris[np.arange(n_tris) % DECIMATE == 0]
n    = len(tris)

v = np.concatenate([tris['v0'], tris['v1'], tris['v2']], axis=0)

# Camera is UPRIGHT in STL: X=width, Y=height(bottom at 89.7), Z=depth(0=back,93.8=front)
# Cage: X=width, Y=depth(front=+Y), Z=height(up)
# Permutation: cage[X,Y,Z] = stl[X, Z, Y]  (Z->depth, Y->height)
TX = -((v[:,0].min() + v[:,0].max()) / 2.0)
TZ =  -v[:,1].min()          # bottom of stl-Y (camera bottom) -> cage Z=0
TY = -((v[:,2].min() + v[:,2].max()) / 2.0)   # centre stl-Z -> cage Y=0

# Apply permutation + flip Y (so stl-Z-max = lens = cage +Y front)
cx = (v[:,0] + TX) * SCALE
cy = (v[:,2] + TY) * SCALE    # NOT negated this time -- try stl-Z-max = front
cz = (v[:,1] + TZ) * SCALE

# Re-interleave (v0,v1,v2 are concatenated blocks)
cx = np.stack([cx[:n], cx[n:2*n], cx[2*n:]], axis=1).ravel()
cy = np.stack([cy[:n], cy[n:2*n], cy[2*n:]], axis=1).ravel()
cz = np.stack([cz[:n], cz[n:2*n], cz[2*n:]], axis=1).ravel()

print(f"  X {cx.min()*1e3:.0f}-{cx.max()*1e3:.0f}  Y {cy.min()*1e3:.0f}-{cy.max()*1e3:.0f}  Z {cz.min()*1e3:.0f}-{cz.max()*1e3:.0f} mm", flush=True)

verts_list = list(zip(cx.tolist(), cy.tolist(), cz.tolist()))
faces_list = [(i*3, i*3+1, i*3+2) for i in range(n)]

# Remove old
for obj in list(bpy.data.objects):
    if 'nikon' in obj.name.lower():
        bpy.data.objects.remove(obj, do_unlink=True)

print("Building mesh...", flush=True)
mesh = bpy.data.meshes.new('NikonZR_body')
mesh.from_pydata(verts_list, [], faces_list)
mesh.update()
for p in mesh.polygons: p.use_smooth = True

obj = bpy.data.objects.new('NikonZR_body', mesh)
bpy.context.collection.objects.link(obj)

# Solid dark-silver material (like real ZR body colour)
mat = bpy.data.materials.new('NikonZR_mat')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (0.15, 0.155, 0.165, 1.0)   # dark grey
bsdf.inputs['Roughness'].default_value  = 0.35
bsdf.inputs['Metallic'].default_value   = 0.4
bsdf.inputs['Alpha'].default_value      = 1.0
obj.data.materials.append(mat)

bpy.ops.wm.save_as_mainfile(filepath=str(OUT / 'zr_with_real_camera.blend'))
print("Blend saved.", flush=True)

scene = bpy.context.scene
scene.render.engine        = 'CYCLES'
scene.cycles.samples       = 80
scene.cycles.use_denoising = True
scene.render.resolution_x  = 1800
scene.render.resolution_y  = 1400

rc = None
for o in bpy.data.objects:
    if o.type == 'CAMERA' and 'Review' in o.name: rc = o; break
if not rc:
    for o in bpy.data.objects:
        if o.type == 'CAMERA': rc = o; break
scene.camera = rc
cd = rc.data
cd.type = 'ORTHO'; cd.clip_start = 0.001; cd.clip_end = 1000

def aim(o, pt):
    o.rotation_euler = (Vector(pt) - o.location).to_track_quat('-Z','Y').to_euler()

# Hero view
rc.location = (0.25, 0.32, 0.23); aim(rc, (0, 0, 0.042)); cd.ortho_scale = 0.27
scene.render.filepath = str(RENDERS / 'real_camera_hero.png')
print("Rendering hero...", flush=True)
bpy.ops.render.render(write_still=True)

# Front view (looking from +Y = lens side if correct)
rc.location = (0, 0.45, 0.04); aim(rc, (0, 0, 0.04)); cd.ortho_scale = 0.24
scene.render.filepath = str(RENDERS / 'real_camera_front.png')
print("Rendering front...", flush=True)
bpy.ops.render.render(write_still=True)

# Right side view
rc.location = (0.45, 0, 0.04); aim(rc, (0, 0, 0.04)); cd.ortho_scale = 0.22
scene.render.filepath = str(RENDERS / 'real_camera_right.png')
print("Rendering right...", flush=True)
bpy.ops.render.render(write_still=True)
print("ALL DONE.", flush=True)
