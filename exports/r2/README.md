# Nikon ZR modular cage — R2-AUDITED review package

This is the engineering-audited CAD release of the user's selected two-post modular cage, incorporating all 12 fixes from the formal engineering audit.

**Status: PASS AFTER FIXES (12 Fixes Applied · Zero Unintended Collisions · Certified BRep Clearances). Camera proxy interfaces remain subject to final physical measurement before CAM/toolpath generation.**

## Open the product

- `zr_modular_complete.step`: the main colored assembly, including the removable lens-adapter support.
- `zr_modular_core.step`: cage without lens support or optional grip.
- `zr_modular_with_grip.step`: main assembly plus detachable silicone grip and its carrier.
- `zr_modular_with_camera.step`: main assembly with a clearly named dimensional camera proxy.
- `zr_modular_complete.iges`: IGES exchange assembly; see the validation report for re-import results.
- `zr_modular_complete.stl`: tessellated assembly for inspection; separately assembled hardware means this is not a single-piece printing model.
- `zr_modular_complete.glb`: colored mesh assembly for a compatible 3D viewer.
- `zr_modular_review.blend`: native Blender review scene with named CAD-derived objects, materials, lighting and an inspection camera. Camera/grip/reference states are retained as hidden objects and can be enabled.
- `parts/`: individual STEP files for the cage, hardware and optional grip components.
- [Rendered views](C:/nikon_cage_cad/renders/r2/): studio, orthographic, exploded and access-study images.

## What is modeled

Rounded top and base plates; two 15 mm uprights; split clamps; axial retaining washers and screws; integral top NATO profile; a side NATO carrier; mounting-hole arrays and perpendicular locating pairs; a cold shoe with channel lips and countersunk mounting screws; Arca-style base; adjustable cable jaws, pads, spindle and swing attachment; a flanged QD socket concept; camera screw and locating pin; adjustable side-lug bridge; recessed camera pads; a magnetic multitool recess; removable lens support; and a separate silicone grip configuration.

All views and mesh files come from the exported CAD geometry. The beauty render is not an AI illustration or a separately modeled substitute.

The two prominent 3/8-16 top holes, camera tie-down and lens-support tip include helical thread geometry. Other threaded holes use pilot geometry with entry chamfers and callouts in `hole_schedule.json`. Most screw shafts use simplified envelopes. Their intentional overlap with corresponding pilot holes is declared explicitly in `validation_report.json`; it must not be mistaken for detailed thread meshing. Split-clamp bores have a clearance ear and a tapped opposite ear.

## Verification evidence

`validation_report.json` records solid validity, named part counts, STEP and IGES re-import, camera-proxy overlap, minimum non-contact proxy clearance, part-pair interference and sampled reference motion checks.

The camera proxy uses the larger current published envelope of 134 × 80.5 × 49 mm. Its contours, tripod/pin positions, screen hinge, bottom door, controls and connectors are illustrative working geometry. Zero overlap against it does not establish fit to a real Nikon ZR. The screen check covers its modeled opening motion; it is not a full measured dual-axis hinge sweep.

The side-lug bridge is an adjustable provision awaiting a measured through-lug adapter. The M2.5 screw shown must not be treated as proof that the camera lug is threaded. NATO, Arca, cold-shoe and QD details are geometric designs awaiting qualification with the actual chosen accessories. The QD concept has not been load-rated. The cable-clamp latch screw must be withdrawn to open the modeled swing frame.

## Materials and mass

Black structural parts are assigned 6061-T6 aluminum, metal hardware uses a stainless approximation and pads/grip use an elastomer approximation. Densities are recorded in the source. `bill_of_materials.csv` contains component volume and estimated mass, and the validation report contains assembly totals. This first detailed build uses solid uprights and substantial plates; further weight reduction requires a defined accessory load and stiffness target. No FEA or physical proof-load test has been performed.

## Rebuild

From `C:/nikon_cage_cad`:

```powershell
conda run --no-capture-output -n cad-ai python models\zr_modular_v2.py
& 'C:\Program Files\Blender Foundation\Blender 4.4\blender.exe' --background --factory-startup --python 'C:\nikon_cage_cad\models\render_zr_v2.py'
```

`parameters.json` is a generated parameter record, not an independently loaded configuration. Geometry and its relationships are defined in the Python source; modifying dimensions requires rebuilding and rechecking the assembly. Render files are generated under `C:/nikon_cage_cad/renders/r2/`.

## Inputs still required for manufacture

Measured camera socket, alignment hole, lug and moving-part geometry; chosen mating clamps/shoe/QD components; lens-adapter support dimensions; accessory loads; fastener strength classes and thread engagement; coating thickness and fitted allowances; physical fit prototype; and the CNC machine/controller, rotary arrangement, stock, fixtures, tooling and CAM postprocessor.

The requested ±0.01 mm remains a proposed local fit/locating target requiring an explicit datum and inspection definition. CAD numerical precision alone is not a manufacturing tolerance. No CNC G-code is supplied in this design-development package.

## Reference sources

- [Nikon ZR specifications](https://onlinemanual.nikonimglib.com/zr/en/15-08.html): overall envelope, camera interface types.
- [Nikon battery and card access](https://onlinemanual.nikonimglib.com/zr/en/03-03.html): combined compartment.
- [MID49 upper cage](https://www.mid49.com/products/upper-cage-for-nikon-zr): product-reference functions, including swing clamp and lens support.
- [MID49 TWIST Ball](https://www.mid49.com/products/twist-ball): 3 mm locating pins on 15 mm centers for the selected 3/8-16 pattern.

All eleven supplied images are retained in `C:/nikon_cage_cad/reference/visuals/`; their roles are documented in `reference/VISUAL_REVIEW.md`.
