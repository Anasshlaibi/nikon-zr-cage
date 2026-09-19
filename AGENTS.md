# CAD workspace instructions

- Working CAD folder: `C:\nikon_cage_cad`.
- Run CAD Python with `conda run --no-capture-output -n cad-ai python ...` (Python 3.10, CadQuery/OCP).
- Read `DESIGN_PLAN_V2.md`, `reference/VISUAL_REVIEW.md` and the latest export README before editing this cage.
- The user selected the modular two-round-upright cage from reference images 05–11. Images 01–04 are secondary grip/finish references. Do not revert to the earlier half cage.
- Preserve R1 files as history. Current R2 source is `models/zr_modular_v2.py`; exports are in `exports/r2`; actual-CAD Blender renderer is `models/render_zr_v2.py`; previews are in `renders/r2`.
- Preserve measured versus provisional dimension status. Camera proxy geometry is not a scan or a fit certification.
- Recheck individual solids, structural joints, camera clearance, export round-trip and moving-part reference geometry after relevant changes. File export success alone does not prove a complete assembly.
- Do not describe provisional CAD or its render as CNC-ready. Executable CAM needs the actual machine, fixtures, tools, postprocessor and an approved fit.
- Keep the design state and output README current. Render the same geometry that is exported.
