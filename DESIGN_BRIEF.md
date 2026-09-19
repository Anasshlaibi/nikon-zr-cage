# Nikon ZR CNC Camera Cage — Design Brief

## Current direction — revision 2, 19 September 2026

The user selected images 5–11: a modular cage with two round uprights, rounded top/base plates, split-clamp joints, recessed fasteners and a detailed cable clamp. [DESIGN_PLAN_V2.md](C:/nikon_cage_cad/DESIGN_PLAN_V2.md) is the current rebuild plan; the [visual review](C:/nikon_cage_cad/reference/VISUAL_REVIEW.md) records every supplied image. The earlier half-cage architecture is superseded. Existing revision 1 CAD is historical and is not ready for manufacture.

## Intent

Create a premium CNC-milled modular aluminum cage for the Nikon ZR, matching the finished appearance of images 5–11. Use matte-black metal, rounded machined plates, two cylindrical uprights, defined joints and generous accessory mounting. Preserve access to camera functions.

## Confirmed camera data

- Original brief envelope: 133.0 W x 80.5 H x 48.7 D mm. Nikon's current guide lists approximately 134 x 80.5 x 49 mm; use the larger value for preliminary packaging and resolve actual mating geometry by measurement. [Nikon specifications](https://onlinemanual.nikonimglib.com/zr/en/15-08.html)
- Body-only mass: approximately 540 g.
- Tripod socket: 1/4 in. ISO 1222.
- Media: CFexpress Type B/XQD and microSD behind the battery/card access cover.
- Monitor: 4-inch vari-angle LCD.
- Connectors: mic/line input, headphone/remote, Type-D HDMI, USB-C, and digital accessory shoe.

## Design requirements

- 6061-T6 aluminum primary material; 7075-T6 may be substituted after manufacturing review.
- Matte-black, bead-blasted hard anodize; stainless 304 hardware preference with fastener strength class to be specified; recessed pad channels; silicone grip in a detachable configuration.
- Maintain at least 1.5 mm non-contact air gap around the camera body.
- Keep the monitor hinge and full articulation envelope unobstructed.
- Provide unobstructed battery/card-cover swing and battery removal route.
- Preserve access to all port covers, controls, digital accessory shoe, and cable plug envelopes.
- Integrated top NATO rail, left NATO rail, left-shoulder cold shoe with safety retention, 1/4-20 and 3/8-16 ARRI locating interfaces, two M4 cable-clamp holes, and a lower-right QD socket.
- Bottom: integrated 38 mm Arca-Swiss-style dovetail, central 1/4-20 tie-down slot, and recessed magnetic multitool pocket.
- Three-point retention: bottom 1/4-20 screw, replaceable anti-twist pin, and adjustable M2.5 strap-lug lock tab.

## Concept architecture

Use a modular assembly with a sculpted base, two round uprights, rounded U-shaped top plate, defined split-clamp/axial-retention joints and a camera-specific side restraint. Incorporate accessory profiles on the appropriate machined parts/carriers. Preserve bottom battery/card access, display articulation and connectors. Grip and lens support are separately removable configurations. See revision 2 for detailed dimensions and verification stages.

## Reference visuals

Images are retained under `reference/visuals/`. Images 5–11 define the selected architecture and visual finish. Their visible details must inform our CAD; hidden geometry and precision mating dimensions still need engineering definition.

- `reference-01.png`: compact wraparound cage silhouette.
- `reference-02.png` to `reference-04.png`: close-fitting cage styling, grip and cable-clamp concepts.
- `reference-05.png`: underside/battery-access and baseplate reference.
- `reference-06.png` to `reference-11.png`: selected modular two-post cage, mounting density, rounded plates, split clamps, camera insertion and separate locking/support hardware.

## Required measurements before production release

1. Tripod socket center, anti-twist-hole center/diameter/depth, and base contour.
2. Battery/card-cover perimeter and full opening/ejection envelope.
3. Screen hinge position and swept volume in every articulation position.
4. Port cover locations, door swing angles, and plug/cable clearance volumes.
5. Digital accessory-shoe envelope, top controls, grip, strap lug, lens mount, and all body curvature/contact zones.
6. Actual Arca clamp target and selected QD, magnet, anti-twist pin, and fastener components.

## Tolerance policy

Use +/-0.01 mm only for suitably controlled local locating features. Use realistic general machining tolerances and explicit protective clearances for all camera-facing regions; account for hard-anodize build-up.

## Deliverables after approval

- Parametric CadQuery source and configurable dimensions.
- Assembly and component STEP files; STL review exports; requested IGES after implementing and validating a supported export route.
- Production drawings, BOM, inspection plan, and finish notes.
- Machine-specific CAM operations/toolpaths only after receiving machine, controller, tool, stock, and fixture data.
