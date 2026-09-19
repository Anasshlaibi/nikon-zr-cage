"""Nikon ZR camera cage: preliminary parametric architecture.

This is a non-production fit-check concept.  Camera contact surfaces, the
anti-twist pin, right strap-lug lock, and all door/screen keep-outs require
physical measurement or a scan before machining release.
Coordinates: X=width, Y=front/back, Z=vertical; mm.
"""

from pathlib import Path
import cadquery as cq


# Nikon-published overall envelope (not an exact surface model).
CAM_W, CAM_D, CAM_H = 133.0, 48.7, 80.5
CLEARANCE = 1.5

# Cage architecture parameters.
BASE_W, BASE_D, BASE_H = 145.0, 58.0, 10.0
BODY_Z = BASE_H + CLEARANCE
OUT = Path(__file__).resolve().parents[1] / "exports"


def capsule_cut(length, width, height):
    """Centered capsule solid, long axis X, used for a central screw slot."""
    radius = width / 2
    straight = length - width
    return (
        cq.Workplane("XY")
        .box(straight, width, height)
        .union(cq.Workplane("XY").cylinder(height, radius).translate((straight / 2, 0, 0)))
        .union(cq.Workplane("XY").cylinder(height, radius).translate((-straight / 2, 0, 0)))
    )


def arca_dovetail():
    """Approximate 38 mm Arca-style male rail; verify against target clamp."""
    profile = [(-19, -5), (19, -5), (17, 0), (-17, 0)]
    return cq.Workplane("YZ").polyline(profile).close().extrude(112)


# Base plate: peripheral rails preserve the battery/card door's underside area.
base = cq.Workplane("XY").box(BASE_W, BASE_D, BASE_H).translate((0, 0, BASE_H / 2))
battery_window = cq.Workplane("XY").box(84, 34, BASE_H + 4).translate((0, 0, BASE_H / 2))
base = base.cut(battery_window)

# Central camera support island carries the screw and the future locating-pin bore.
support = cq.Workplane("XY").box(38, 42, 2.5).translate((0, 0, BASE_H + 1.25))
slot = capsule_cut(20, 7.0, 16).translate((0, 0, BASE_H + 2))
support = support.cut(slot)
base = base.union(support)

# Underside tool/magnet recess (magnet specification to be selected).
tool_pocket = cq.Workplane("XY").box(42, 10, 3.2).translate((0, -22, 1.6))
base = base.cut(tool_pocket)

# Approximate Arca rail, intentionally marked for clamp verification.
base = base.union(arca_dovetail().translate((-56, 0, 0)))

# Left upright: deliberately slim and offset from the body for display clearance.
left_pillar = (
    cq.Workplane("XY")
    .box(8, 16, 78)
    .translate((-(CAM_W / 2 + CLEARANCE + 4), 0, BODY_Z + 39))
)
base = base.union(left_pillar)

# Left integrated NATO-inspired rail blank (final profile to standard drawing).
left_rail = (
    cq.Workplane("XY")
    .box(5.5, 23, 58)
    .translate((-(CAM_W / 2 + CLEARANCE + 10.75), 0, BODY_Z + 42))
)
base = base.union(left_rail)

# Top bridge: front bar plus short end wings leaves the rear/screen region open.
top_z = BODY_Z + CAM_H + 5
front_bar = cq.Workplane("XY").box(145, 12, 8).translate((0, -(CAM_D / 2 + 7), top_z))
left_wing = cq.Workplane("XY").box(16, 45, 8).translate((-64.5, -6, top_z))
right_wing = cq.Workplane("XY").box(16, 45, 8).translate((64.5, -6, top_z))
base = base.union(front_bar).union(left_wing).union(right_wing)

# Low-profile top NATO-inspired rail blank, centered above the front bar.
top_rail = cq.Workplane("XY").box(64, 23, 4).translate((0, -(CAM_D / 2 + 7), top_z + 6))
base = base.union(top_rail)

# Right-side minimal lock-tab blank: mount provision only, no lug engagement yet.
right_tab = cq.Workplane("XY").box(8, 18, 20).translate((CAM_W / 2 + CLEARANCE + 4, 12, BODY_Z + 63))
right_tab = right_tab.cut(cq.Workplane("XZ").circle(1.3).extrude(12).translate((CAM_W / 2 + CLEARANCE - 2, 12, BODY_Z + 63)))
base = base.union(right_tab)

# Top mounting holes: nominal drill representations only; tapping is specified in drawings.
for x in (-48, -24, 24, 48):
    base = base.cut(cq.Workplane("XY").cylinder(20, 3.3).translate((x, -(CAM_D / 2 + 7), top_z)))
for x in (-36, 36):
    base = base.cut(cq.Workplane("XY").cylinder(20, 4.8).translate((x, -(CAM_D / 2 + 7), top_z)))

# Cold shoe blank at left shoulder; exact standardized profile is a later feature.
cold_shoe = cq.Workplane("XY").box(20, 18, 5).translate((-57, 14, top_z + 5))
cold_shoe = cold_shoe.cut(cq.Workplane("XY").cylinder(10, 1.5).translate((-57, 14, top_z + 5)))
base = base.union(cold_shoe)

# M4 cable-clamp provisions in the front-left upright region.
for z in (BODY_Z + 18, BODY_Z + 32):
    base = base.cut(cq.Workplane("YZ").cylinder(14, 1.65).translate((-(CAM_W / 2 + CLEARANCE + 12), -10, z)))

# QD socket placeholder at the bottom-right corner (verify selected insert geometry).
qd = cq.Workplane("XZ").cylinder(10, 6.0).translate((CAM_W / 2 + 4, 19, BASE_H / 2))
base = base.cut(qd)

# Final edge breaks are intentionally deferred to component-level machining
# drawings. A global fillet is invalid across the intersecting rail features.

# Reference-only camera envelope is exported separately to support later interference checks.
camera_envelope = (
    cq.Workplane("XY")
    .box(CAM_W, CAM_D, CAM_H)
    .translate((0, 0, BODY_Z + CAM_H / 2))
)

OUT.mkdir(parents=True, exist_ok=True)
cq.exporters.export(base, str(OUT / "nikon_zr_cage_concept.step"))
cq.exporters.export(base, str(OUT / "nikon_zr_cage_concept.stl"), tolerance=0.08, angularTolerance=0.2)
cq.exporters.export(camera_envelope, str(OUT / "nikon_zr_reference_envelope.step"))

print("Exported:")
for path in sorted(OUT.glob("nikon_zr_*")):
    print(f"  {path.name} ({path.stat().st_size:,} bytes)")
