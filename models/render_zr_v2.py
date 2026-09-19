"""Render the actual R2 CAD meshes in Blender 4.4 (background invocation)."""
from pathlib import Path
import bpy, json, math, sys
from mathutils import Vector, Matrix

ROOT=Path(r'C:\nikon_cage_cad')
OUT=ROOT/'exports'/'r2'
RENDERS=ROOT/'renders'/'r2'
RENDERS.mkdir(parents=True,exist_ok=True)
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
quick='--quick' in args
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.unit_settings.system='METRIC'
scene.unit_settings.length_unit='MILLIMETERS'
scene.render.engine='CYCLES'
scene.cycles.samples=20 if quick else 40
scene.cycles.use_denoising=True
scene.cycles.max_bounces=6
scene.render.resolution_x=1200 if quick else 1800
scene.render.resolution_y=950 if quick else 1400
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.film_transparent=False
scene.view_settings.view_transform='AgX'
scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.8,.84,.9,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.35

def mat(name,color,metallic,roughness):
    m=bpy.data.materials.new(name);m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Metallic'].default_value=metallic
    bs.inputs['Roughness'].default_value=roughness
    return m

materials={
 'metal':mat('6061 / satin black hard anodize',(.018,.023,.03),.38,.38),
 'steel':mat('Brushed stainless hardware',(.42,.46,.52),.85,.28),
 'rubber':mat('Black silicone / rubber',(.013,.016,.019),0,.73),
 'camera':mat('UNMEASURED / camera reference',(.65,.68,.71),.1,.43),
 'glass':mat('Camera glass and polymer reference',(.028,.037,.05),.15,.25),
 'accent':mat('Record button indicator',(.42,.018,.011),.05,.4)}

data=json.loads((OUT/'assembly_mesh.json').read_text(encoding='utf-8'))
objs={}
for p in data:
    mesh=bpy.data.meshes.new(p['name'])
    mesh.from_pydata([tuple(v*.001 for v in pt) for pt in p['vertices']],[],p['triangles'])
    mesh.update()
    obj=bpy.data.objects.new(p['name'],mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(materials[p['material']])
    # OCP duplicates vertices along CAD face boundaries; smoothing stays inside a face.
    for face in mesh.polygons: face.use_smooth=True
    obj['part_group']=p['group'];obj['engineering_note']=p.get('note','')
    objs[p['name']]=(obj,p)

floor_mat=mat('Warm neutral studio',(.70,.72,.75),0,.8)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0185))
floor=bpy.context.object;floor.name='STUDIO / floor';floor.data.materials.append(floor_mat)

def aim(obj,pt): obj.rotation_euler=(Vector(pt)-obj.location).to_track_quat('-Z','Y').to_euler()
def area(name,loc,power,size,target=(0,0,.04)):
    d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size
    o=bpy.data.objects.new(name,d);bpy.context.collection.objects.link(o);o.location=loc;aim(o,target)

area('Large softbox / key',(.08,.16,.38),2.6,.28)
area('Large softbox / fill',(-.30,.08,.17),1.8,.24)
area('Strip / rear edge',(.1,-.22,.30),3.6,.22)
area('Soft front lift',(.32,.22,.1),.88,.2)
camdata=bpy.data.cameras.new('Review camera');camdata.type='ORTHO';camdata.clip_start=.001;camdata.clip_end=1000
cam=bpy.data.objects.new('Review camera',camdata);bpy.context.collection.objects.link(cam);scene.camera=cam

def configure(groups,explode=False,motion=False):
    for name,(obj,p) in objs.items():
        show=p['group'] in groups
        if motion and name in ('camera_screen_proxy','camera_bottom_door_proxy'): show=False
        obj.hide_render=not show;obj.hide_viewport=not show
        obj.rotation_euler=(0,0,0)
        obj.location=tuple(v*.001 for v in p['explode']) if explode and p['group'] not in ('camera','motion') else (0,0,0)
    floor.hide_render=explode or motion

def view(name,loc,target=(0,0,.042),scale=.255,groups=('core','lens'),explode=False,motion=False,ground=True):
    print('RENDER',name,flush=True)
    configure(groups,explode,motion)
    floor.hide_render=not ground or explode or motion
    cam.location=loc;aim(cam,target);camdata.ortho_scale=scale
    scene.render.filepath=str(RENDERS/f'{name}.png')
    bpy.ops.render.render(write_still=True)

view('01_hero_cage',(.25,.32,.23))
if not quick:
    view('02_rear_cage',(-.24,-.32,.22))
    view('03_with_camera',(.25,.32,.23),groups=('core','lens','camera'))
    view('04_camera_rear',(-.25,-.32,.2),groups=('core','lens','camera'))
    view('05_exploded',(.3,.36,.28),target=(0,0,.06),scale=.34,explode=True)
    view('06_with_grip',(.30,.31,.23),target=(.01,0,.04),scale=.285,groups=('core','lens','grip'))
    view('07_bottom',(-.24,.3,-.26),target=(0,0,.024),scale=.25,ground=False)
    view('08_access_study',(-.28,-.35,.2),target=(-.022,0,.036),scale=.3,groups=('core','lens','camera','motion'),motion=True)
    view('09_front',(0,.45,.045),scale=.24,ground=False)
    view('10_rear',(0,-.45,.045),scale=.24,ground=False)
    view('11_left',(-.45,0,.045),scale=.2,ground=False)
    view('12_right',(.45,0,.045),scale=.2,ground=False)
    view('13_top',(0,.001,.5),target=(0,0,0),scale=.24,ground=False)
    view('14_bottom_ortho',(0,.001,-.5),target=(0,0,0),scale=.24,ground=False)
    view('15_top_detail',(-.19,.23,.25),target=(-.035,.019,.096),scale=.145,ground=False)
    view('16_clamp_detail',(-.29,-.23,.14),target=(-.082,.007,.030),scale=.12,ground=False)
    configure(('core','lens'))
    pivot=Vector((-.095,.005,0))
    transform=Matrix.Translation(pivot) @ Matrix.Rotation(-math.pi/2,4,'Z') @ Matrix.Translation(-pivot)
    for n in ('cable_swing_frame','cable_moving_jaw','cable_lower_pad','cable_upper_pad','cable_thumbwheel'):
        objs[n][0].matrix_world=transform
    objs['cable_carrier_M4_-81'][0].location.z=.015
    cam.location=(-.29,-.23,.14);aim(cam,(-.093,-.002,.03));camdata.ortho_scale=.14
    floor.hide_render=True;scene.render.filepath=str(RENDERS/'17_clamp_open.png')
    bpy.ops.render.render(write_still=True)

configure(('core','lens'))
floor.hide_render=False
cam.location=(.25,.32,.23);aim(cam,(0,0,.042));camdata.ortho_scale=.255
# Native editable scene and portable GLB use the same mesh geometry.
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'zr_modular_review.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj,p in objs.values():
    if p['group'] in ('core','lens'): obj.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(OUT/'zr_modular_complete.glb'),use_selection=True,export_format='GLB')
for obj,p in objs.values():
    if p['group']=='grip':
        obj.hide_viewport=False;obj.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(OUT/'zr_modular_with_grip.glb'),use_selection=True,export_format='GLB')
print('Render package complete:',RENDERS,flush=True)
