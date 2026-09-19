# Nikon ZR modular cage — revised design plan

Revision 2 · 19 September 2026 · Current stage: design plan

## Agreed direction

The user selected **the modular cage in reference images 5–11**. Build a finished-looking assembly with two round uprights, rounded machined top and base plates, recessed fasteners, an articulated cable clamp, and a clear camera installation route. Images 1–4 remain secondary references for edge treatment and the silicone grip.

This supersedes the earlier half-cage architecture. The next CAD revision must reflect the proportions, mechanical detail, and finish of the selected references, with camera-specific dimensions and a complete assembly design.

Primary cage-only target — supplied reference, not our current CAD:

![User-supplied modular cage reference 11](C:/nikon_cage_cad/reference/visuals/reference-11.png)

Reference with camera:

![User-supplied modular cage reference 06](C:/nikon_cage_cad/reference/visuals/reference-06.png)

All eleven originals are retained. The [image-by-image review](C:/nikon_cage_cad/reference/VISUAL_REVIEW.md) identifies what each contributes.

## 1. Visual design

- Two cylindrical uprights in an offset arrangement. Proposed placement is camera-left/front near the connector side and camera-right/rear, interpreting the reference perspectives. Final offsets must clear the screen and operator's hand.
- A rounded U-shaped top plate: broad crossbar, side returns, large open center, blended post bosses and an underside relief. It should read as one deliberately machined part.
- An asymmetrical sculpted base supporting the actual tripod-socket region, with a large opening for the combined battery/card compartment.
- Circular post-clamp bosses, narrow split-clamp slits, recessed socket-head screws, and visible assembly seams.
- Ordered groups of mounting holes with chamfered entrances and sufficient surrounding material, including hole patterns on selected side faces.
- Satin/matte black metal, subtle edge highlights, black elastomer inserts, and restrained stainless hardware accents. No vendor branding on our cage.
- Removable front lens-adapter support, corresponding to the silver stud in the references. It is an accessory, not a camera anti-twist pin.
- A detachable silicone grip configuration preserves the original grip requirement while keeping the primary modular silhouette.

## 2. Mechanical assembly

| Component | Geometry and connection | Reference |
| --- | --- | --- |
| Top plate | Single machined U-shaped part; rounded ends, post bosses, underside relief, accessory holes and integrated top NATO profile | 06, 07, 09, 11 |
| Baseplate | Single connected machined part with camera support lands, pad recesses, door opening, tie-down slot, tool pocket and integrated Arca profile | 05, 10, 11 |
| Two uprights | Separate round parts seated in top/base bosses; positive axial location/retention and split-clamp tightening | 06–11 |
| Left NATO carrier | Short machined carrier with integral NATO profile, positively attached beside the round post, clear of ports and screen | Original requirement, 08 |
| Cable clamp | Carrier attached through the specified two M4 mounts, swing-away body, adjustable jaws, captive screws, travel limits and replaceable contact pads | 03, 04, 08, 11 |
| Camera retention | Captive bottom screw, removable locating pin and adjustable side-lug bracket, each with a defined mating interface | Original requirement, 10, 11 |
| Cold shoe | Actual lips and undercut, insertion opening, stop and safety-pin provision on left shoulder | Original requirement, 02 |
| QD interface | Retained socket/insert in a reinforced lower-right boss, with access to release the selected swivel | Original requirement |
| Grip | Detachable metal carrier with contoured silicone insert and defined insert retention | 02, 03 |
| Lens support | Removable front slider and adjustable support stud with a lock; sized for the intended lens adapter | 05, 09–11 |
| Hardware | Separate screws, pins, magnet, multitool, pads and any required washers, listed in a BOM | 05, 10, 11 |

Named multiple solids are correct for an assembly. Each machined component must itself be valid and connected, and every structural joint must have a physical attachment. The uprights transfer top-plate loads into the base. The camera lug bracket stabilizes the camera; it is not the structural connection between top and base. Uprights need axial retention as well as rotational clamping.

Check assembly order: assemble lower frame, fit pads, insert camera along a verified path, secure camera, install/secure top, then close cable clamp and fit accessories. Top removal must not require removing the lens. Allow tool access to every fastening operation.

## 3. Provisional design parameters

These are starting values for our cage, not measurements extracted from the images or released manufacturing dimensions.

| Parameter | Proposed starting point | Final dependency |
| --- | --- | --- |
| Core cage envelope | Approximately 178–185 W × 110–125 H × 70–85 D mm, excluding optional accessories | Posts, screen movement, controls and hand access |
| Upright diameter | 15 mm candidate; reference diameter not verified | Stiffness, clamp design and stock |
| Top plate thickness | 8–10 mm with locally reinforced bosses | Thread engagement, clamps and accessory loads |
| Base thickness | 8–10 mm plus local Arca projection | Screw recess, compartment opening, tool pocket and stiffness |
| Principal outside corners | R6–R10 | Reference proportions and material around clamps |
| Exposed edge treatment | Typically R0.8–R1.5 or a small specified chamfer | Handling, cutter access and individual feature geometry |
| Ordinary body clearance | Start near 2.5 mm nominal; retain the requested 1.5 mm minimum after tolerances and finish | Measured camera body; larger clearances around moving parts |
| Pad recess | Set from selected elastomer thickness and compressed stand-off | Defined support contacts without unwanted metal contact |
| Arca profile | Nominal 38 mm class; complete section must be verified | Selected clamp and its engagement/retention geometry |

The 1.5 mm gap is the user's requirement, not a Nikon thermal guarantee. Record intentional pad/hardware contacts separately from non-contact clearances. Overall mass is to be calculated from modeled parts and assigned materials, not inferred from appearance.

## 4. Camera geometry and access

Build a separate reference assembly: camera body, lens-mount surround, screen/hinge, door, connectors, controls, accessory shoe and strap lugs. Refine visible shape using the references while keeping the source and certainty of every interface dimension identifiable.

Coordinates: X toward the operator's right, Y toward the lens/front, Z upward. Origin at bottom center of the provisional body envelope. Locate the tripod screw independently; do not assume it is at the body center.

Nikon's current reference guide lists approximately **134 × 80.5 × 49 mm**. The original brief and earlier regional specifications used **133 × 80.5 × 48.7 mm**. Preserve both entries, use the larger envelope for preliminary packaging, and resolve local dimensions by measurement before machining. Neither bounding envelope supplies exact contours. [Nikon specifications](https://onlinemanual.nikonimglib.com/zr/en/15-08.html)

Battery and memory cards share the bottom compartment. The base must clear the door, latch, fingers, battery and both card extraction paths. The earlier separate right-side card-door assumption is superseded. [Nikon battery/card access](https://onlinemanual.nikonimglib.com/zr/en/03-03.html)

Model the spaces needed for:

1. Screen closed, opening, rotated and front-facing, including the entire travel between positions.
2. Bottom door and battery/card extraction, including access with the target Arca clamp installed.
3. Port-cover motion, HDMI/USB-C/audio plugs, cable bends, and cable clamp open/closed positions.
4. Top controls, built-in microphones, speaker, digital-shoe insertion and the chosen audio adapter.
5. Lens installation, lens release, front REC button, grip, rear controls, camera insertion and fastener access.

Approximate clearance bodies support concept development. Track measurement-dependent checks separately; an approximate-envelope check does not certify the physical fit.

## 5. Complete functional interfaces

| Interface | Required detail and evidence |
| --- | --- |
| 1/4-20 and 3/8-16 holes | Chosen thread class, appropriate pilot geometry, usable depth, entry chamfer, screw intrusion limit and hole schedule; verify mating fastener |
| ARRI groups | Selected accessory's pin diameters, centers and depths; perpendicular pin pairs for four orientations where required; verify a mating drawing/part |
| NATO rails | Complete dovetail section, clamp engagement, insertion path and end retention; verify selected clamp |
| Cold shoe | Lips, undercut, opening, stop, safety pin and actual accessory-foot clearance |
| Arca base | Complete male profile, sliding direction and safety provisions; test every intended DJI clamp, since nominal width alone does not establish compatibility |
| M4 attachment | Two correctly located threaded bores, adequate depth/edge distance and clamp/tool access |
| QD socket | Defined latch seat, retention geometry and insert attachment, verified with chosen socket/swivel pair |
| Bottom screw | Captive head/shoulder, slot and controlled projection above pads; measure camera socket depth |
| Anti-twist pin | Replaceable pin, constrained projection; first confirm a compatible camera hole, then measure position, diameter and depth |
| M2.5 side restraint | Adjustable bracket, defined bearing faces and thread location; do not assume the camera lug itself is threaded M2.5 |
| Tool pocket | Selected tool seat, magnet retention, finger access and adequate remaining wall thickness |

Model explicit screw heads and seats. Selected visible thread detail for rendering must derive from the same thread specifications. Manufacturing exports may use simplified holes accompanied by complete thread callouts. A block or ordinary round hole does not count as a finished rail, shoe or QD mechanism.

The silver front stud is a lens-adapter support. The manufacturer's description also confirms the swing-away HDMI clamp and bottom-compartment access. These clarify function without providing our mating dimensions. [MID49 Upper Cage for Nikon ZR](https://www.mid49.com/products/upper-cage-for-nikon-zr)

## 6. Materials, finish and machining

Start with 6061-T6 aluminum. Retain 7075-T6 as a later option requiring its own process review. Preserve the stainless 304 hardware preference, but specify fastener strength class and pin properties before assigning loads. Alloy alone does not establish a fastener rating.

Design plates for billet machining with reachable pockets, finite internal radii and feature-level fillets. Establish clamp/fastener/thread locations before adding weight-reduction pockets. Prevent hole arrays from intersecting clamp bores or leaving thin unsupported walls.

Use the requested matte black hard anodize over an agreed blast texture. Define coating thickness, allowance and masking with the finisher. Evaluate finished post/clamp and dovetail fits; install pads, magnets and grip inserts after finishing.

Proposed machining sequence: establish datums and rough stock; finish primary face/pockets; refixture for opposite face; index for side holes, dovetails and clamps; finish accessible 3D contours; deburr; inspect; anodize; inspect fits; assemble. Use simultaneous five-axis motion where access or surface requirements justify it.

Allocate tolerances by function. Preserve ±0.01 mm as the user's target to review for specific locating/fit dimensions. Define general tolerances, datum relationships, position tolerances, thread classes and post-finish acceptance explicitly; do not assign a blanket precision tolerance merely to imply quality.

Before manufacturing release, establish camera/lens/accessory masses, lever arms and handling loads. Check plate stiffness, post retention, thread engagement and camera restraint for those conditions. Verify thermal performance on a physical assembly; nominal gap is not a thermal test.

## 7. Work stages and review evidence

### A. Reference and skeleton

Create shared datums/parameters and camera access bodies. Lay out posts, top contour and sculpted base in front, rear, side and perspective views. Match the silhouette to images 06, 10 and 11 before adding hole patterns. Resolve camera insertion here.

Review output: frame proportions and reference images shown together, with provisional clearances identified.

### B. Connected assembly

Model named top, base, uprights, post seats, split clamps, axial retention, screws and camera support. Locate mating parts from shared parameters. Check connectivity and camera interference.

Review output: assembled and exploded views with actual joints, seating and tightening routes.

### C. Functional detail and finish

Add mounting patterns, NATO/Arca profiles, cold shoe, cable clamp, QD, bottom screw, pads, tool pocket and side restraint. Add grip and lens support as separate accessory configurations. Apply consistent radii and chamfers per component.

Review output: working interface sections and close-ups of joints, hardware and access. No missing edge treatment caused by dropping a failed global fillet.

### D. Product presentation

Render the actual CAD assembly with matte black metal, subtle highlights and controlled studio lighting on a neutral background. A white/gray camera reference should reveal the clearances as in the supplied images. Identify uncertain camera geometry as reference-only.

Required views:

- Cage-only three-quarter views matching images 11 and 10.
- Camera installed, front and rear three-quarter views.
- Front, rear, left, right, top and bottom orthographic views.
- Underside with door open and extraction route visible.
- Screen open/rotated with nearby post and clamp visible.
- Exploded assembly with component/hardware names.
- Close-ups of hole patterns, post joints, NATO rail, cable clamp, Arca base and detachable grip.

The first review package should already look assembled and finished. Still images and an orbitable viewer, if local tools support one, must use the same CAD geometry as the exports. No cosmetic substitution for missing mechanical parts.

### E. Physical fit and manufacturing release

Replace provisional camera-interface data with measurements/scan; verify motions and accessory mating; produce fit prototypes or interface coupons; test the camera and intended clamps; complete drawings; prepare CAM with the actual machine information.

Machine/controller, rotary configuration, CAM software/postprocessor, stock, fixtures, cutters and holders remain inputs for executable toolpaths. CadQuery/OCP is the verified CAD backend. A verified five-axis CAM backend has not yet been established.

## 8. Acceptance and deliverables

Visual acceptance: recognizably the selected two-post cage, with rounded plates, organized hole groups, recessed hardware, credible joints and finish. Compare CAD and supplied references at matched angles.

CAD acceptance: one valid solid per intended machined part, expected assembly part count, defined joints, no unintended intersections or disconnected material, and STEP round-trip checks. File readability alone is insufficient.

Fit acceptance: measured minimum clearances, moving-part and installation access, correct accessory fit and a physical camera check. Intended support is through specified pads/hardware.

Deliverables:

1. Parametric CadQuery source, versioned parameters and measurement-status record.
2. Named component STEP files and structured assembly STEP.
3. Requested IGES after implementing a supported OCP/export route and validating re-import; local IGES capability has not yet been checked.
4. STL for review and fit prototypes.
5. CAD-derived renders, orthographic views and exploded assembly.
6. BOM with selected hardware, drawings/hole schedules, finish and inspection notes, material-based mass and center-of-mass estimates.
7. CAM setup sheets, simulation and machine-specific toolpaths after fit and manufacturing inputs are established.

## 9. Existing model audit

Preserve revision 1 source and exports as history. They require substantial rebuilding to meet the revised brief.

A read-only STEP check on 19 September 2026 found four individually valid solids but no connected frame. The upright spans Z=11.5–89.5 mm while the top begins at Z=93 mm. The base outer rail ends at Z=10 mm and does not join the upright; only the central support rises higher. The right tab is separate. The cage also overlaps its own camera envelope by approximately 1,466.5 mm³.

The source identifies rails/shoe as blanks; global filleting was removed after failure. Re-import established readability, not mechanical completeness. Revision 2 must pass assembly/clearance checks and show finished geometry before it is presented as a completed design.

## 10. Decision status

- User-selected: modular architecture from images 5–11 and finished-product appearance.
- Preserved user requirements: specified interfaces, silicone grip, three-point camera retention intent, alloy/finish preferences, exports and eventual CNC deliverables.
- Proposed: initial envelope, post diameter, thickness/radius ranges, detachable grip, removable lens support and exact post arrangement.
- Unresolved for machining: camera mating geometry, selected accessory hardware, design loads and machine/CAM inputs.
- Current task: remake and save the plan. Revision 2 CAD, renders and CAM have not been generated during this planning turn.
