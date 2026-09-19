import bpy, math
from pathlib import Path

ROOT   = Path(r'C:\nikon_cage_cad')
RENDER = ROOT / 'renders' / 'r2' / 'camera_in_cage_preview.png'

# ── Check what we have ────────────────────────────────────────────────────
for obj in bpy.data.objects:
    print(f"  OBJ: {obj.name}  type={obj.type}  loc={[round(v,1) for v in obj.location]}")

# ── Find the camera body ──────────────────────────────────────────────────
cam_body = bpy.data.objects.get('NikonZR_body')
if cam_body is None:
    # Try to find by name pattern
    for obj in bpy.data.objects:
        if 'nikon' in obj.name.lower() or 'zr' in obj.name.lower() or 'camera' in obj.name.lower():
            cam_body = obj
            break

if cam_body:
    bb = cam_body.bound_box  # 8 corners in local space
    import mathutils
    world_corners = [cam_body.matrix_world @ mathutils.Vector(c) for c in bb]
    xs = [v.x for v in world_corners]
    ys = [v.y for v in world_corners]
    zs = [v.z for v in world_corners]
    print(f"\nNikonZR_body world bounds:")
    print(f"  X: {min(xs):.1f} to {max(xs):.1f}  ({max(xs)-min(xs):.1f})")
    print(f"  Y: {min(ys):.1f} to {max(ys):.1f}  ({max(ys)-min(ys):.1f})")
    print(f"  Z: {min(zs):.1f} to {max(zs):.1f}  ({max(zs)-min(zs):.1f})")
else:
    print("WARNING: NikonZR_body not found!")

# ── Set up render ─────────────────────────────────────────────────────────
scn = bpy.context.scene
scn.render.engine           = 'CYCLES'
scn.cycles.samples          = 64
scn.render.resolution_x     = 1280
scn.render.resolution_y     = 960
scn.render.resolution_percentage = 100
scn.render.image_settings.file_format = 'PNG'
scn.render.filepath         = str(RENDER)

# ── Find or create render camera ──────────────────────────────────────────
render_cam = bpy.data.objects.get('Camera')
if render_cam is None:
    bpy.ops.object.camera_add()
    render_cam = bpy.context.active_object
    render_cam.name = 'RenderCam'
scn.camera = render_cam

# Position: front-right-above view like reference image
render_cam.location = (240, -280, 200)
render_cam.rotation_euler = (
    math.radians(57),   # tilt down
    0,
    math.radians(40),   # rotate right
)
render_cam.data.lens = 65

# ── Render ────────────────────────────────────────────────────────────────
print(f"\nRendering → {RENDER}")
bpy.ops.render.render(write_still=True)
print("Done.")
