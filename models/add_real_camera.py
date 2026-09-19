import bpy
from pathlib import Path

STL_IN    = r'C:\nikon_cage_cad\exports\r2\camera_aligned.stl'
OUT_BLEND = r'C:\nikon_cage_cad\exports\r2\zr_with_real_camera.blend'

bpy.ops.wm.stl_import(filepath=STL_IN, global_scale=1.0)
cam_obj = bpy.context.selected_objects[0]
cam_obj.name = 'NikonZR_body'

mat = bpy.data.materials.new(name='NikonZR_body')
mat.use_nodes = True
mat.blend_method = 'BLEND'
bsdf = mat.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (0.72, 0.76, 0.80, 1.0)
bsdf.inputs['Roughness'].default_value  = 0.30
bsdf.inputs['Metallic'].default_value   = 0.10
bsdf.inputs['Alpha'].default_value      = 0.75
if cam_obj.data.materials:
    cam_obj.data.materials[0] = mat
else:
    cam_obj.data.materials.append(mat)

col_name = 'Real Camera'
if col_name not in bpy.data.collections:
    col = bpy.data.collections.new(col_name)
    bpy.context.scene.collection.children.link(col)
else:
    col = bpy.data.collections[col_name]
for c in list(cam_obj.users_collection):
    c.objects.unlink(cam_obj)
col.objects.link(cam_obj)

bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
print(f'Saved: {OUT_BLEND}')
