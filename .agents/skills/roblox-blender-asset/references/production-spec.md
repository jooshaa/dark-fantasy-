# Pink House Roblox asset specification

## Scale and coordinates

- Treat `1 Roblox stud = 0.28 metres` in Blender source files.
- Record expected dimensions in both metres and studs before export.
- Expect GLB imports to arrive near `1 metre = 1 stud`; measure and compute the
  correction instead of assuming it.
- Include an asymmetric temporary marker for orientation checks, then remove it
  from the placed production copy.

## Geometry

- Keep each mesh comfortably below Roblox's current per-mesh import limit.
- Prefer multiple reusable modules over one monolithic environment mesh.
- Retain simple invisible collision cores for very large cliffs unless authored
  collision is proven stable and performant.
- Avoid perfect planes, repeated sine-wave displacement, obvious grid patterns,
  detached decorative rocks, and identical module silhouettes.
- Apply transforms before final export or verify the exporter applies them.

## Materials

- Use metalness/roughness PBR conventions.
- Use reusable Roblox `MaterialVariant` surfaces for large tileable cliff, grass,
  soil, plaster, and wood areas.
- Use `SurfaceAppearance` for unique UV-mapped hero assets.
- Prefer OpenGL tangent-space normal maps (Y+).
- Avoid flat-color texture uploads when a material tint is sufficient.

## Pink House cliff targets

- Approximate shell envelope: `1400 x 620 x 1000` studs.
- Preserve a central chasm opening near `25` studs at the front.
- Preserve the iconic long ladder and the fissure terminating near the house.
- Front, side, and inner-chasm walls need authored silhouettes; hidden cores own
  collision.
- Large-scale reads matter first: plateau outline, chasm, house scale, ladder,
  horizon, clouds. Micro-detail cannot repair incorrect composition.

## Verification record

Record:

- Source and export paths.
- Object and MeshPart counts.
- Total triangles and maximum triangles per mesh.
- Overall dimensions and per-axis orientation.
- Material and texture coverage.
- Multi-view captures and known visual limitations.
- Export size and checksum.
- Roblox asset IDs only after explicit permanent-upload consent.
