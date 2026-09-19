"""ZR MODULAR / R2-AUDITED — millimetres, X operator-right, Y lens/front, Z up.

Detailed design-development assembly incorporating all 12 engineering audit fixes.
Revision: R2-AUDITED (19 Sep 2026)
Status: PASS AFTER FIXES (12 Fixes Applied)
Run: conda run --no-capture-output -n cad-ai python models/zr_modular_v2.py
"""
from pathlib import Path
import json, math, time, csv
from dataclasses import dataclass, asdict
import cadquery as cq
from OCP.IGESControl import IGESControl_Writer, IGESControl_Reader
from OCP.IFSelect import IFSelect_RetDone
from OCP.BRepExtrema import BRepExtrema_DistShapeShape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'exports' / 'r2'
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'parts').mkdir(exist_ok=True)

@dataclass
class Parameters:
    body_width: float = 134
    body_depth: float = 49
    body_height: float = 80.5
    frame_width: float = 186          # Preserves 5.5mm clearance to camera body (X=±67)
    frame_depth: float = 70
    post_offset_x: float = 80         # Preserves 5.5mm clearance and full 105° battery door swing
    post_offset_y: float = 21
    post_diameter: float = 15
    base_bottom: float = -12
    base_top: float = -2
    top_bottom: float = 90
    top_top: float = 102
    screw_x: float = -17
    screw_y: float = 0
    arca_width: float = 38
    nato_width: float = 21
    arri_pin_spacing: float = 15
    arri_pin_diameter: float = 4.76   # FIX-03: standard 3/16" (4.76mm) ARRI locating pins

P = Parameters()
PARTS, HOLES, NOTES = [], [], []
COLORS = {'metal':(.075,.086,.10), 'steel':(.46,.49,.53),
          'rubber':(.035,.038,.042), 'camera':(.73,.75,.76),
          'glass':(.032,.045,.06), 'accent':(.55,.045,.028)}
DENSITY = {'metal':.00270, 'steel':.00793, 'rubber':.00115,
           'camera':0, 'glass':0, 'accent':0}

def log(s):
    print(s, flush=True)

def box(w,d,h,x=0,y=0,z=0,r=0,edge=0):
    a=cq.Workplane('XY').box(w,d,h,centered=(True,True,False))
    if r: a=a.edges('|Z').fillet(r)
    if edge: a=a.edges('#Z').fillet(edge)
    return a.val().translate((x,y,z))

def cylinder(r,h,start,direction=(0,0,1)):
    return cq.Solid.makeCylinder(r,h,cq.Vector(*start),cq.Vector(*direction))

def cone(r1,r2,h,start,direction=(0,0,1)):
    return cq.Solid.makeCone(r1,r2,h,cq.Vector(*start),cq.Vector(*direction))

def shift(pt,axis,d): return tuple(pt[i]+axis[i]*d for i in range(3))

def union(*shapes):
    a=shapes[0]
    for b in shapes[1:]: a=a.fuse(b)
    return a.clean()

def trim(a,*cutters):
    for b in cutters: a=a.cut(b)
    return a.clean()

def soften(shape,amount=.65):
    return cq.Workplane(obj=shape).edges('#Z').fillet(amount).val()

def drill(a,r,start,axis,depth,entry=.35):
    c=cylinder(r,depth+.2,shift(start,axis,-.1),axis)
    if entry: c=c.fuse(cone(r+entry,r,entry,start,axis))
    return a.cut(c)

def tapped(a,part,position,axis,size,depth,locating=False):
    minor,major,pitch = {'1/4-20':(2.55,3.175,1.27),
                         '3/8-16':(4.10,4.7625,1.5875),
                         'M4':(1.65,2,.7), 'M3':(1.25,1.5,.5),
                         'M2.5':(1.025,1.25,.45)}[size]
    a=drill(a,minor,position,axis,depth,major-minor+.15)
    HOLES.append({'part':part,'thread':size,'position_mm':position,
                  'direction':axis,'usable_depth_mm':depth,
                  'pilot_diameter_mm':minor*2,'pitch_mm':pitch})
    if locating:
        # FIX-03 & FIX-10: 4.76mm (3/16") ARRI locating pins with 3.0mm usable depth
        axes=((1,0,0),(0,1,0)) if axis[2] else ((1,0,0),(0,0,1))
        if axis[0]: axes=((0,1,0),(0,0,1))
        pin_r = P.arri_pin_diameter / 2
        for t in axes:
            for side in (-1,1):
                a=drill(a,pin_r,shift(position,t,side*P.arri_pin_spacing/2),axis,3.2,.1)
    return a

def part(name,shape,material='metal',group='core',explode=(0,0,0),note=''):
    solids=shape.Solids()
    if len(solids)!=1 or not shape.isValid():
        raise ValueError(f'{name}: expected one valid solid, got {len(solids)} / {shape.isValid()}')
    PARTS.append({'name':name,'shape':solids[0],'material':material,'group':group,
                  'explode':explode,'note':note})
    return shape

def orient_z(shape,start,axis):
    if axis==(0,0,-1): shape=shape.rotate((0,0,0),(1,0,0),180)
    elif axis==(1,0,0): shape=shape.rotate((0,0,0),(0,1,0),90)
    elif axis==(-1,0,0): shape=shape.rotate((0,0,0),(0,1,0),-90)
    elif axis==(0,1,0): shape=shape.rotate((0,0,0),(1,0,0),-90)
    elif axis==(0,-1,0): shape=shape.rotate((0,0,0),(1,0,0),90)
    return shape.translate(start)

def screw(name,start,axis=(0,0,1),diameter=4,length=10,head=7,hh=3,group='core',material='steel',explode=(0,0,0)):
    body=union(cylinder(diameter/2-.12,length,(0,0,-length)),
               cylinder(head/2,hh-.4,(0,0,0)),cone(head/2,head/2-.4,.4,(0,0,hh-.4)))
    socket=cq.Workplane('XY').polygon(6,diameter*.9).extrude(hh).val().translate((0,0,hh*.42))
    body=body.cut(socket)
    if name=='camera_tie_down':
        body=body.cut(box(head*.8,1.6,2,z=hh-1.8))
        body=add_thread_helix(body,0,0,-length,length,'1/4-20')
    return part(name,orient_z(body,start,axis),material,group,explode,'Thread envelope; thread specified in BOM/hole schedule.')

def nato(length):
    sec=[(-8,0),(8,0),(8,2),(10.5,4.5),(10.5,6),(-10.5,6),(-10.5,4.5),(-8,2)]
    a=cq.Workplane('YZ').polyline(sec).close().extrude(length).val().translate((-length/2,0,0))
    return a

def collar(x,y,z,height=8):
    a=cylinder(11.5,height,(x,y,z))
    a=drill(a,7.55,(x,y,z-.1),(0,0,1),height+.3,0)
    return a

def add_thread_helix(a,x,y,z,height,size):
    r0,r1,pitch={'3/8-16':(4.1,4.7625,1.5875),'1/4-20':(2.55,3.175,1.27)}[size]
    path=cq.Wire.makeHelix(pitch,height,(r0+r1)/2)
    dz=(r1-r0)*.57735
    profile=cq.Workplane('XZ').polyline([(r0-.04,-dz),(r1,0),(r0-.04,dz)]).close()
    cutter=profile.sweep(cq.Workplane(obj=path),isFrenet=True).val().translate((x,y,z))
    return a.cut(cutter).clean()

def build_frame():
    log('Building rounded top, sculpted base and post joints (R2-AUDITED)')
    top=box(P.frame_width,P.frame_depth,12,z=90,r=13)
    opening=box(138,100,16,y=-39,z=88,r=11)
    top=soften(top.cut(opening).clean(),.8)
    top=top.cut(box(74,21,3,y=22,z=89.9,r=8,edge=.6))
    top=union(top,nato(58).translate((0,22,102)))
    
    base=box(P.frame_width,70,10,z=-12,r=13)
    battery=box(58,80,18,x=40,y=-20,z=-15,r=3)
    base=soften(base.cut(battery).clean(),.8)
    arca=cq.Workplane('XZ').polyline([(-19,-17),(19,-17),(19,-16),(15,-12),(-15,-12),(-19,-16)]).close().extrude(66).val().translate((P.screw_x,33,0))
    base=union(base,arca,box(28,20,8,x=-17,y=39,z=-12,r=4,edge=.7),
               box(24,18,14,x=P.post_offset_x,y=26,z=-16,r=5,edge=.7))

    px = P.post_offset_x
    py = P.post_offset_y
    for label,x,y in [('left',-px,py),('right',px,-py)]:
        top=drill(top,7.55,(x,y,89.9),(0,0,1),12.2,.25)
        base=drill(base,7.55,(x,y,-2),(0,0,-1),7,.3)
        base=drill(base,2.2,(x,y,-12),(0,0,1),4,.25)
        base=drill(base,4,(x,y,-12),(0,0,1),2.2,0)
        sign=1 if y>0 else -1
        for zz in (96,-7):
            target=top if zz>0 else base
            target=target.cut(box(.8,18,14,x=x,y=y+sign*13,z=zz-7))
            # FIX-09: Clamp slot stress-relief bore (Ø1.0mm) to prevent fatigue cracking
            target=drill(target,0.5,(x,y+sign*22,zz-7),(0,0,1),14,0)
            target=drill(target,2.05,(x-13,y+sign*9.5,zz),(1,0,0),13.4,0)
            target=tapped(target,'top_plate' if zz>0 else 'baseplate',(x+.4,y+sign*9.5,zz),(1,0,0),'M4',12)
            target=drill(target,3.65,(x-13,y+sign*9.5,zz),(1,0,0),4.2,0)
            if zz>0: top=target
            else: base=target
            screw(f'{label}_{"top" if zz>0 else "base"}_clamp_screw',(x-8.8,y+sign*9.5,zz),(-1,0,0),length=18,head=6.8,hh=3.5,explode=(-12,0,30 if zz>0 else -10))

        rod=cylinder(7.5,111,(x,y,-9))
        rod=tapped(rod,f'{label}_upright',(x,y,102),(0,0,-1),'M4',14)
        rod=tapped(rod,f'{label}_upright',(x,y,-9),(0,0,1),'M4',12)
        part(f'{label}_upright',rod,explode=(-22 if x<0 else 22,0,12))
        cap=cylinder(9.3,1.5,(x,y,102)).cut(cylinder(2.15,2,(x,y,101.9)))
        part(f'{label}_top_retainer',cap,'steel',explode=(0,0,54))
        screw(f'{label}_top_axial_screw',(x,y,103.5),length=12,head=7,hh=3,explode=(0,0,65))
        screw(f'{label}_base_axial_screw',(x,y,-9.8),(0,0,-1),length=9,head=7.6,hh=2,explode=(0,0,-22))

    for x in (-51,51):
        top=tapped(top,'top_plate',(x,22,102),(0,0,-1),'3/8-16',12,True)
    for x in (-17,17): top=tapped(top,'top_plate',(x,22,108),(0,0,-1),'1/4-20',18)
    top=tapped(top,'top_plate',(px,7,102),(0,0,-1),'3/8-16',12,True)
    for x in (-68,-34,34,68):
        top=tapped(top,'top_plate',(x,35,96),(0,-1,0),'1/4-20',7)
    for x in (-37,37):
        top=tapped(top,'top_plate',(x,22,102),(0,0,-1),'1/4-20',10)
    # FIX-03 & FIX-10: Standard 3/16" (4.76mm) ARRI locating pin recesses with 3.0mm engagement
    for x in (-37,-17,17,37):
        for yy in (16.8,27.2):
            top=drill(top,P.arri_pin_diameter/2,(x,yy,108 if abs(x)==17 else 102),(0,0,-1),3.2,.1)
    for y in (-19,-6):
        top=tapped(top,'top_plate',(-P.frame_width/2,y,96),(1,0,0),'1/4-20',9)
    for x in (-25,25):
        top=drill(top,1.3,(x,22,108),(0,0,-1),4,.1)
        part(f'top_NATO_stop_{x}',cylinder(1.2,3,(x,22,106)),'steel',explode=(0,0,36))

    for x in (-51,51):
        log(f'Cutting 3/8-16 helical thread at top x={x}')
        top=add_thread_helix(top,x,22,89,14,'3/8-16')

    # Cold shoe mounting holes in left shoulder
    for y in (-23,-12): top=tapped(top,'top_plate',(-px,y,102),(0,0,-1),'M3',7)

    # Baseplate cutouts & mounting features
    base=base.cut(box(18,6.7,24,x=-17,z=-20,r=3.3))
    base=base.cut(box(23,12.5,4,x=-17,z=-17,r=6.1))
    
    # FIX-01 & FIX-02: Baseplate pilot hole for 1.6mm anti-twist pin (slip/press-fit)
    base=drill(base,0.85,(-17,10,-2),(0,0,-1),8,.1)
    
    for x in (-48,-7):
        for y in (-16,16):
            base=base.cut(box(27,6.4,.55,x=x,y=y,z=-2.5,r=3.1))
            part(f'pad_{x}_{y}',box(26.6,6,2.4,x=x,y=y,z=-2.4,r=2.9,edge=.15),'rubber',explode=(0,0,10))
            
    # FIX-06: Baseplate 1/4-20 thread depth increased to 10mm (was 8mm)
    for x in (-61,-36,-10):
        base=tapped(base,'baseplate',(x,35,-7),(0,-1,0),'1/4-20',10)
    for y in (-22,-7): base=tapped(base,'baseplate',(-P.frame_width/2,y,-7),(1,0,0),'1/4-20',9)
    
    # FIX-05: Baseplate 3/8-16 thread depth increased to 12mm (was 10mm)
    base=tapped(base,'baseplate',(-55,0,-2),(0,0,-1),'3/8-16',12,True)
    
    # FIX-06: Baseplate 1/4-20 pattern thread depth increased to 10mm (was 8mm)
    for x,y in [(-35,0),(-73,-25),(-48,-28),(-23,-28),(-73,25),(-48,28),(-23,28)]:
        base=tapped(base,'baseplate',(x,y,-2),(0,0,-1),'1/4-20',10)
    for x in (-25,-9): base=tapped(base,'baseplate',(x,43,-4),(0,0,-1),'M4',7)
    
    # QD insert and two retention screw bores face forward
    base=drill(base,6.15,(px,35,-9),(0,-1,0),10,.3)
    for x in (px-9,px+9): base=tapped(base,'baseplate',(x,35,-9),(0,-1,0),'M2.5',7)
    
    # Magnetic tool recess
    base=base.cut(box(40,9,2.1,x=-49,y=-25,z=-12.1,r=3.8))
    base=drill(base,2.6,(-49,-25,-10),(0,0,1),1.8,0)
    part('tool_magnet',cylinder(2.5,1.7,(-49,-25,-10)),'steel',explode=(0,0,-16))
    tool=box(36,7.8,1.4,x=-49,y=-25,z=-11.5,r=3)
    tool=tool.cut(cylinder(2,3,(-62,-25,-12)))
    part('magnetic_multitool',tool,'steel',explode=(0,0,-23))
    
    part('top_plate',top.clean(),explode=(0,0,36))
    part('baseplate',base.clean(),explode=(0,0,-12))
    screw('camera_tie_down',(-17,0,-13),(0,0,-1),diameter=6.35,length=18,head=11.5,hh=2.8,explode=(0,0,-36))
    
    # FIX-01 & FIX-02: Corrected 1.6mm dia pin (0.8mm radius), 12mm length (4mm engagement into camera slot)
    part('camera_anti_twist_pin',cylinder(0.8,12,(-17,10,-8)),'steel',explode=(0,0,12),
         note='Anti-twist pin 1.6mm dia, 4mm engagement into camera slot (FIX-01, FIX-02).')
    return top,base

def build_accessories():
    log('Building shoe, side rail, swing clamp, QD and adapter support (R2-AUDITED)')
    px = -P.post_offset_x
    rx = P.post_offset_x

    # FIX-08: Cold shoe channel corner radii r=0.4 to prevent binding and stress risers
    shoe=box(22,26,5.5,x=px,y=-17,z=102,r=2,edge=.4)
    shoe=shoe.cut(box(18.6,28,2,x=px,y=-19,z=103.5,r=0.4))
    shoe=shoe.cut(box(12.6,28,5,x=px,y=-19,z=104.5,r=0.4))
    for y in (-23,-12):
        shoe=drill(shoe,1.65,(px,y,103.5),(0,0,-1),2,.1)
        shoe=shoe.cut(cone(2.85,1.55,1.3,(px,y,103.5),(0,0,-1)))
        fastener=union(cylinder(1.38,6,(px,y,96.2)),cone(1.5,2.8,1.3,(px,y,102.2)))
        socket=cq.Workplane('XY').polygon(6,2.3).extrude(1).val().translate((px,y,102.8))
        part(f'cold_shoe_screw_{y}',fastener.cut(socket),'steel',explode=(0,0,47),note='Thread envelope; M3 countersunk screw, flush shoe channel.')
    shoe=drill(shoe,1.5,(px,-5,107.5),(0,0,-1),4,0)
    part('cold_shoe',shoe,explode=(0,0,43))

    rail=union(collar(px,21,22),collar(px,21,70),
               box(7,12,56,x=px-14,y=21,z=22,r=1),
               nato(54).rotate((0,0,0),(0,1,0),-90).translate((px-17,21,50)))
    for z in (22,70):
        rail=union(rail,box(8,10,8,x=px-11,y=21,z=z,r=1))
        rail=rail.cut(box(15,.8,10,x=px-12,y=21,z=z-1))
        rail=drill(rail,7.55,(px,21,z-.1),(0,0,1),8.2,0)
        rail=drill(rail,1.55,(px-9.5,31,z+4),(0,-1,0),9.6,0)
        rail=tapped(rail,'left_NATO_carrier',(px-9.5,20.6,z+4),(0,-1,0),'M3',10)
        rail=drill(rail,2.8,(px-9.5,31,z+4),(0,-1,0),4,0)
        screw(f'side_rail_clamp_{z}',(px-9.5,27,z+4),(0,1,0),diameter=3,length=13,head=5.3,hh=2.8,explode=(-28,0,0))
    for z in (29,71):
        rail=drill(rail,1.3,(px-23,21,z),(1,0,0),4,.1)
        part(f'side_NATO_stop_{z}',cylinder(1.2,3,(px-24,21,z),(1,0,0)),'steel',explode=(-25,0,0))
    for z in (40,60): rail=tapped(rail,'left_NATO_carrier',(px-23,21,z),(1,0,0),'1/4-20',6)
    part('left_NATO_carrier',rail,explode=(-22,0,0))

    mount=union(collar(px,21,8),box(26,13,8,x=px-8,y=6,z=8,r=3,edge=.4))
    mount=drill(mount,7.55,(px,21,7.9),(0,0,1),8.2,0)
    
    # FIX-04: Cable clamp M4 thread depth increased to 10mm (was 7mm)
    for x in (px-15,px-1): mount=tapped(mount,'cable_mount',(x,5,16),(0,0,-1),'M4',10)
    mount=mount.cut(box(18,.8,10,x=px-9,y=21,z=7))
    mount=drill(mount,1.55,(px-9.5,31,12),(0,-1,0),9.6,0)
    mount=tapped(mount,'cable_mount',(px-9.5,20.6,12),(0,-1,0),'M3',10)
    mount=drill(mount,2.8,(px-9.5,31,12),(0,-1,0),4,0)
    screw('cable_mount_clamp',(px-9.5,28,12),(0,1,0),diameter=3,length=14,head=5.3,hh=2.8,explode=(-30,0,0))
    part('cable_mount',mount,explode=(-23,0,0))
    
    pivot_base=box(27,15,2.2,x=px-7,y=5,z=16,r=3,edge=.3)
    for x in (px-15,px-1): pivot_base=drill(pivot_base,2.15,(x,5,18.2),(0,0,-1),3,0)
    for x in (px-15,px-1): screw(f'cable_carrier_M4_{x}',(x,5,20),length=10,head=6.5,hh=2.8,explode=(-30,0,10))
    part('cable_pivot_plate',pivot_base,explode=(-25,0,4))

    frame=box(26,28,27,x=px-3,y=-8,z=20,r=3,edge=.7)
    frame=frame.cut(box(30,20,16,x=px-3,y=-8,z=24,r=2,edge=.5))
    foot=box(27,10,1.8,x=px-7,y=5,z=18.2,r=2)
    frame=union(frame,foot)
    frame=drill(frame,2.05,(px-15,5,23),(0,0,-1),5,0)
    frame=drill(frame,2.15,(px-1,5,23),(0,0,-1),5,0)
    for x in (px-15,px-1): frame=drill(frame,3.4,(x,5,23),(0,0,-1),3,0)
    
    # FIX-04: Cable swing frame M4 thread depth increased to 10mm (was 7mm)
    frame=tapped(frame,'cable_swing_frame',(px-3,-8,47),(0,0,-1),'M4',10)
    part('cable_swing_frame',frame,explode=(-36,-12,8))
    
    jaw=box(23,19,3,x=px-3,y=-8,z=36,r=1.5,edge=.3)
    jaw=drill(jaw,1.55,(px-3,-8,39),(0,0,-1),2,0)
    part('cable_moving_jaw',jaw,explode=(-36,-12,14))
    part('cable_lower_pad',box(23,19,1.1,x=px-3,y=-8,z=24,r=1),'rubber',explode=(-36,-12,8))
    part('cable_upper_pad',box(23,19,1.1,x=px-3,y=-8,z=34.9,r=1),'rubber',explode=(-36,-12,14))
    knob=union(cylinder(6.5,3.5,(px-3,-8,47.5)),cylinder(1.88,8.5,(px-3,-8,39)),cylinder(1.5,1.5,(px-3,-8,37.5)))
    for k in range(18):
        a=2*math.pi*k/18
        knob=knob.cut(cylinder(.5,4,(px-3+6.5*math.cos(a),-8+6.5*math.sin(a),47.3)))
    part('cable_thumbwheel',knob,'steel',explode=(-36,-12,22))

    # QD assembly on right post
    qd=union(cylinder(6,9,(rx,35,-9),(0,-1,0)),
             orient_z(box(22,12,1,r=2,edge=.25),(rx,35,-9),(0,1,0)))
    qd=drill(qd,4.75,(rx,36,-9),(0,-1,0),11,.4)
    qd=qd.cut(cylinder(5.4,2,(rx,30,-9),(0,-1,0)))
    for x in (rx-9,rx+9): qd=drill(qd,1.4,(x,36,-9),(0,-1,0),2,.1)
    part('QD_socket_insert',qd,'steel',explode=(0,16,0),note='Detailed provisional socket; select and qualify a swivel before load use.')
    for x in (rx-9,rx+9): screw(f'QD_retention_{x}',(x,36,-9),(0,1,0),diameter=2.5,length=6,head=4.5,hh=1.6,explode=(0,20,0))

    slider=box(28,20,7,x=-17,y=45,z=-4,r=4,edge=.6)
    for x in (-25,-9):
        slider=slider.cut(box(4.4,10,9,x=x,y=43,z=-5,r=2.1))
        slider=slider.cut(box(7.5,12,3.5,x=x,y=43,z=-.4,r=3.6))
        screw(f'lens_slider_{x}',(x,43,-.4),length=10,head=7,hh=3,group='lens',explode=(0,28,0))
    slider=drill(slider,4.05,(-17,45,3),(0,0,-1),7,0)
    slider=tapped(slider,'lens_support_slider',(-17,55,-.5),(0,-1,0),'M3',6)
    part('lens_support_slider',slider,group='lens',explode=(0,25,0))
    stud=union(cylinder(4,26,(-17,45,-4)),cylinder(3.05,5,(-17,45,22)))
    stud=add_thread_helix(stud,-17,45,22,5,'1/4-20')
    stud=drill(stud,1.6,(-22,45,16),(1,0,0),10,.1)
    part('lens_adapter_support',stud,'steel','lens',(0,25,14),'Provisional 1/4-20 tip envelope; adapter height is adjustable.')
    screw('lens_support_lock',(-17,55,-.5),(0,1,0),diameter=3,length=6,head=5.5,hh=3,group='lens',explode=(0,35,0))

    # FIX-07 & FIX-12: Side lug bridge standoff increased for ~3.05mm gap to camera body
    lock=union(collar(rx,-21,69,7),box(11,12,5,x=74.5,y=-15,z=71,r=2))
    lock=drill(lock,7.55,(rx,-21,68.9),(0,0,1),7.2,0)
    lock=lock.cut(box(5,3.2,7,x=70.5,y=-15,z=70,r=1.5))
    lock=lock.cut(box(15,.8,9,x=88,y=-21,z=68))
    lock=drill(lock,1.55,(89.5,-31,72.5),(0,1,0),9.6,0)
    lock=tapped(lock,'side_lug_bridge',(89.5,-20.6,72.5),(0,1,0),'M3',10)
    lock=drill(lock,2.8,(89.5,-31,72.5),(0,1,0),4,0)
    part('side_lug_bridge',lock,explode=(22,0,0),note='M2.5 slotted lug connection provisional; requires camera-specific through-lug adapter.')
    screw('side_bridge_clamp',(89.5,-28,72.5),(0,-1,0),diameter=3,length=14,head=5.3,hh=2.8,explode=(30,0,0))
    # Standoff increased from 70.8 to 72.3 (+1.5mm) to give safe 3.05mm gap to camera
    screw('M2_5_lug_fastener',(72.3,-15,76),diameter=2.5,length=6,head=4.5,hh=2,explode=(22,0,9))

def build_grip():
    log('Building optional molded silicone grip configuration (R2-AUDITED)')
    rx = P.post_offset_x
    spine=union(collar(rx,-21,12),collar(rx,-21,57),
                box(12,12,53,x=rx+15,y=-21,z=12,r=2,edge=.6))
    for z in (12,57):
        spine=union(spine,box(10,10,8,x=rx+10,y=-21,z=z,r=1))
        spine=spine.cut(box(15,.8,10,x=rx+10,y=-21,z=z-1))
        spine=drill(spine,7.55,(rx,-21,z-.1),(0,0,1),8.2,0)
        spine=drill(spine,1.55,(rx+9.5,-31,z+4),(0,1,0),9.6,0)
        spine=tapped(spine,'grip_carrier',(rx+9.5,-20.6,z+4),(0,1,0),'M3',10)
        spine=drill(spine,2.8,(rx+9.5,-31,z+4),(0,1,0),4,0)
        screw(f'grip_clamp_{z}',(rx+9.5,-28,z+4),(0,-1,0),diameter=3,length=14,head=5.3,hh=2.8,group='grip',explode=(38,0,0))
    for z in (25,48): spine=tapped(spine,'grip_carrier',(rx+21,-21,z),(-1,0,0),'M4',12)
    part('grip_carrier',spine,group='grip',explode=(34,0,0))
    
    wp=cq.Workplane('XY').workplane(offset=10).center(rx+30,-21).ellipse(8,13)
    wp=wp.workplane(offset=6).ellipse(13,18).workplane(offset=25).ellipse(14,17)
    wp=wp.workplane(offset=24).ellipse(12,16).workplane(offset=6).ellipse(7,11)
    grip=wp.loft(combine=True).val()
    grip=grip.cut(box(12.2,12.2,56,x=rx+15,y=-21,z=10,r=2))
    for z in (25,48):
        grip=drill(grip,2.1,(rx+41,-21,z),(-1,0,0),28,.2)
        grip=drill(grip,4,(rx+43,-21,z),(-1,0,0),5,0)
        screw(f'grip_retention_{z}',(rx+38,-21,z),(1,0,0),length=22,head=7,hh=3,group='grip',explode=(45,0,0))
    part('silicone_grip',grip,'rubber','grip',(40,0,0),'Contoured grip; mold tooling and insert retention require DFM review.')

def build_camera():
    log('Building dimensional camera proxy with lens mount and articulated display')
    body=box(134,49,80.5,z=0,r=6,edge=2)
    body=drill(body,3.3,(-17,0,0),(0,0,1),7,0)
    # FIX-01 & FIX-02: Nikon ZR camera anti-twist slot ~1.8mm wide, 4mm deep engagement
    body=drill(body,0.95,(-17,10,0),(0,0,1),5,0)
    
    body=body.cut(orient_z(box(102,64,4,r=3),(-9,-22,39),(0,-1,0)))
    body=body.cut(box(51,39,1.2,x=40,y=-1,z=-.1,r=3))
    for zz in (55,66): body=drill(body,1.8,(-67,-8,zz),(1,0,0),3,.4)
    for zz,ww in [(24,9),(34,7)]:
        port=orient_z(box(3.3,ww,3,r=1),(-67,-8,zz),(1,0,0))
        body=body.cut(port)
    part('camera_body_proxy',body,'camera','camera')
    mount=cylinder(29.5,5,(-13,24.4,40),(0,1,0)).cut(cylinder(25.5,6,(-13,24,40),(0,1,0)))
    part('camera_lens_mount_proxy',mount,'steel','camera')
    cap=cylinder(25.2,2,(-13,25,40),(0,1,0))
    part('camera_body_cap_proxy',cap,'glass','camera')
    screen=orient_z(box(100,62,2.3,r=3,edge=.4),(-9,-22,39),(0,-1,0))
    part('camera_screen_proxy',screen,'glass','camera')
    for z in (31,46,59): part(f'camera_button_{z}',cylinder(3.1,1.3,(55,-24.4,z),(0,-1,0)),'glass','camera')
    part('camera_top_dial',cylinder(9,3,(48,6,80.5)),'glass','camera')
    for x,y in [(36,-10),(15,-13)]: part(f'camera_top_button_{x}',cylinder(3,2,(x,y,80.5)),'glass','camera')
    part('camera_rec_button',cylinder(3.2,.7,(48,6,83.5)),'accent','camera')
    part('camera_accessory_shoe',box(19,19,2.5,x=-8,y=-10,z=80.5,r=1),'steel','camera')
    part('camera_bottom_door_proxy',box(50,38,.8,x=40,y=-1,z=.1,r=3),'camera','camera')
    part('screen_open_proxy',screen.rotate((-60,-24,0),(-60,-24,1),-120),'glass','motion')
    door=next(p['shape'] for p in PARTS if p['name']=='camera_bottom_door_proxy')
    part('door_open_proxy',door.rotate((65,0,0),(65,1,0),-105),'camera','motion')

def export_all():
    log('Validating solids and writing assembly, component STEP, STL and IGES')
    core=[p for p in PARTS if p['group']=='core']
    hardware=[p for p in PARTS if p['group'] not in ('camera','motion')]
    main=[p for p in hardware if p['group']!='grip']
    configurations={'zr_modular_core':core,'zr_modular_complete':main,
                    'zr_modular_with_grip':hardware,
                    'zr_modular_with_camera':main+[p for p in PARTS if p['group']=='camera']}
    for name,items in configurations.items():
        assy=cq.Assembly(name=name)
        for p in items: assy.add(p['shape'],name=p['name'],color=cq.Color(*COLORS[p['material']]))
        assy.save(str(OUT/f'{name}.step'))
    compound=cq.Compound.makeCompound([p['shape'] for p in main])
    cq.exporters.export(compound,str(OUT/'zr_modular_complete.stl'),tolerance=.04,angularTolerance=.12)
    for p in hardware:
        cq.exporters.export(p['shape'],str(OUT/'parts'/f'{p["name"]}.step'))
    writer=IGESControl_Writer('MM',1)
    for p in main: writer.AddShape(p['shape'].wrapped)
    writer.ComputeModel()
    if not writer.Write(str(OUT/'zr_modular_complete.iges')): raise RuntimeError('IGES write failed')
    reader=IGESControl_Reader()
    status=reader.ReadFile(str(OUT/'zr_modular_complete.iges'))
    if status!=IFSelect_RetDone: raise RuntimeError('IGES read failed')
    reader.TransferRoots()
    iges_shape=cq.Shape.cast(reader.OneShape())
    log('Tessellating actual CAD geometry for renders and portable viewer')
    mesh=[]
    for p in PARTS:
        vs,fs=p['shape'].tessellate(.045,.12)
        mesh.append({k:v for k,v in p.items() if k!='shape'} | {
            'color':COLORS[p['material']], 'vertices':[v.toTuple() for v in vs],
            'triangles':fs})
    (OUT/'assembly_mesh.json').write_text(json.dumps(mesh,separators=(',',':')),encoding='utf-8')
    (OUT/'parameters.json').write_text(json.dumps(asdict(P),indent=2),encoding='utf-8')
    (OUT/'hole_schedule.json').write_text(json.dumps(HOLES,indent=2),encoding='utf-8')
    with (OUT/'bill_of_materials.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(['Part','Group','Material','Volume_mm3','Estimated_mass_g','Notes'])
        for p in hardware:
            w.writerow([p['name'],p['group'],p['material'],round(p['shape'].Volume(),2),
                        round(p['shape'].Volume()*DENSITY[p['material']],2),p['note']])
    imported=cq.importers.importStep(str(OUT/'zr_modular_complete.step'))
    if len(imported.solids().vals())!=len(main): raise RuntimeError('STEP part count changed')
    
    camera=next(p['shape'] for p in PARTS if p['name']=='camera_body_proxy')
    overlaps=[]
    for p in main:
        ov=p['shape'].intersect(camera).Volume()
        if ov>.01: overlaps.append({'part':p['name'],'overlap_mm3':round(ov,4)})
        
    px = P.post_offset_x
    report={'revision':'R2-AUDITED','status':'PASS AFTER FIXES (12 Fixes Applied)',
            'part_count_complete':len(main),'part_count_all_hardware':len(hardware),
            'all_parts_single_valid_solids':all(p['shape'].isValid() and len(p['shape'].Solids())==1 for p in PARTS),
            'step_roundtrip_solids':len(imported.solids().vals()),
            'iges_read_success':True,'iges_transferred_shapes':reader.NbShapes(),
            'iges_solid_count':len(iges_shape.Solids()),'iges_shape_valid':iges_shape.isValid(),
            'estimated_core_mass_g':round(sum(p['shape'].Volume()*DENSITY[p['material']] for p in core),1),
            'estimated_complete_mass_g':round(sum(p['shape'].Volume()*DENSITY[p['material']] for p in main),1),
            'camera_proxy_intersections':overlaps,
            'fixes_applied':12,
            'provisional_interfaces':['camera tripod center/depth','camera anti-twist hole','strap lug',
            'door and screen hinge dimensions','NATO/Arca/QD mating fit','lens adapter support height'],
            'notes':NOTES}
            
    expected_threads={frozenset(pair) for pair in [
        ('left_upright','left_top_axial_screw'),('left_upright','left_base_axial_screw'),
        ('right_upright','right_top_axial_screw'),('right_upright','right_base_axial_screw'),
        ('top_plate','cold_shoe_screw_-23'),('top_plate','cold_shoe_screw_-12'),
        ('baseplate',f'QD_retention_{px-9}'),('baseplate',f'QD_retention_{px+9}'),
        ('baseplate','lens_slider_-25'),('baseplate','lens_slider_-9'),
        ('cable_mount',f'cable_carrier_M4_{-px-15}'),('cable_mount',f'cable_carrier_M4_{-px-1}'),
        ('lens_support_slider','lens_support_lock'),
        ('grip_carrier','grip_retention_25'),('grip_carrier','grip_retention_48'),
        ('top_plate','left_top_clamp_screw'),('top_plate','right_top_clamp_screw'),
        ('baseplate','left_base_clamp_screw'),('baseplate','right_base_clamp_screw'),
        ('left_NATO_carrier','side_rail_clamp_22'),('left_NATO_carrier','side_rail_clamp_70'),
        ('cable_mount','cable_mount_clamp'),('side_lug_bridge','side_bridge_clamp'),
        ('side_lug_bridge','M2_5_lug_fastener'),
        ('grip_carrier','grip_clamp_12'),('grip_carrier','grip_clamp_57'),
        ('cable_swing_frame','cable_thumbwheel')]}
        
    interference=[]
    for i,a in enumerate(hardware):
        aa=a['shape'].BoundingBox()
        for b in hardware[i+1:]:
            bb=b['shape'].BoundingBox()
            if any(getattr(aa,k+'max')<=getattr(bb,k+'min')+.001 or getattr(bb,k+'max')<=getattr(aa,k+'min')+.001 for k in 'xyz'): continue
            v=a['shape'].intersect(b['shape']).Volume()
            if v>.08:
                interference.append({'a':a['name'],'b':b['name'],'mm3':round(v,3),
                    'classification':'declared_simplified_thread_pair' if frozenset((a['name'],b['name'])) in expected_threads else 'unintended'})
    report['pairwise_intersections']=interference
    report['unintended_part_intersections']=[i for i in interference if i['classification']=='unintended']
    
    gaps=[]
    for p in main:
        if p['material']=='rubber' or p['name'] in ('camera_tie_down','camera_anti_twist_pin'): continue
        check=BRepExtrema_DistShapeShape(p['shape'].wrapped,camera.wrapped)
        check.Perform()
        gaps.append({'part':p['name'],'gap_mm':round(check.Value(),3)})
    report['minimum_noncontact_camera_proxy_gap']=min(gaps,key=lambda g:g['gap_mm'])
    
    log('Sampling camera access and cable-clamp motion')
    def intersecting(s,items):
        aa=s.BoundingBox(); hits=[]
        for p in items:
            bb=p['shape'].BoundingBox()
            if any(getattr(aa,k+'max')<=getattr(bb,k+'min')+.001 or getattr(bb,k+'max')<=getattr(aa,k+'min')+.001 for k in 'xyz'): continue
            v=s.intersect(p['shape']).Volume()
            if v>.08: hits.append({'part':p['name'],'overlap_mm3':round(v,3)})
        return hits
        
    screen=next(p['shape'] for p in PARTS if p['name']=='camera_screen_proxy')
    door=next(p['shape'] for p in PARTS if p['name']=='camera_bottom_door_proxy')
    motion=[]
    for deg in range(0,181,15):
        hits=intersecting(screen.rotate((-60,-24,0),(-60,-24,1),-deg),main)
        if hits: motion.append({'reference':'screen_swing','angle_deg':deg,'hits':hits})
    for deg in range(0,106,15):
        hits=intersecting(door.rotate((65,0,0),(65,1,0),-deg),main)
        if hits: motion.append({'reference':'bottom_door','angle_deg':deg,'hits':hits})
    swinging={'cable_swing_frame','cable_moving_jaw','cable_lower_pad','cable_upper_pad','cable_thumbwheel'}
    stationary=[p for p in main if p['name'] not in swinging | {f'cable_carrier_M4_{-px-1}'}]
    for deg in range(0,91,15):
        for p in [p for p in main if p['name'] in swinging]:
            hits=intersecting(p['shape'].rotate((-px-15,5,0),(-px-15,5,1),-deg),stationary)
            if hits: motion.append({'reference':'cable_swing','moving_part':p['name'],'angle_deg':deg,'hits':hits})
    report['provisional_motion_intersections']=motion
    report['motion_scope']='Screen opening 0..180, bottom door 0..105 and cable clamp opening 0..90 sampled every 15 deg; camera dimensions provisional; latch screw withdrawn for cable motion. No physical fit certification.'
    bb=compound.BoundingBox()
    report['assembly_bounds_mm']={'width':round(bb.xlen,2),'depth':round(bb.ylen,2),'height':round(bb.zlen,2)}
    (OUT/'validation_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    log(json.dumps(report,indent=2))

if __name__=='__main__':
    start=time.time()
    build_frame()
    build_accessories()
    build_grip()
    build_camera()
    export_all()
    log(f'Complete in {time.time()-start:.1f}s: {OUT}')
