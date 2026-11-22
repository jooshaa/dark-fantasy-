# Graphics and Environment Context

Last updated: 2026-11-22

## Project Direction

Create a polished Roblox dark-fantasy horror experience with multiple unlockable
maps. The game is primarily a personal artistic project, but it should also be
attractive, replayable, performant, and capable of ethical monetization.

Target visual style: **cinematic realistic dark fantasy**, not generic Roblox
realism and not realism at the expense of playability. Surreal compositions are
welcome when materials, lighting, scale, sound, and environmental detail remain
physically convincing.

The first vertical slice is the **Pink House / Endless Chasm** map, based on a
reference video supplied by the user. Its key composition is:

- A small pink house on top of an enormous grass-covered monolith.
- A narrow central chasm or cut in the monolith.
- A very long ladder descending along the exposed face.
- A lower grass field, distant landscape, clouds, and extreme vertical scale.
- A calm, dreamlike surface contrasted with dark-fantasy horror below.

## Experience Structure

The planned experience contains multiple dark-fantasy maps connected through a
hub. Maps unlock primarily through active playtime, with optional progression
milestones to discourage AFK farming.

Possible progression:

1. Pink House — available immediately.
2. Ash Forest — approximately 30 minutes active playtime.
3. Sunken Cathedral — approximately 2 hours.
4. Dead Village — approximately 5 hours.
5. Crimson Castle — approximately 10 hours.
6. Final Abyss — approximately 20 hours plus prior progression.

Large worlds should normally be separate Places within one Roblox Experience so
each can have independent lighting, terrain, ambience, and asset loading.

## Visual Standard

### Lighting

- Use `LightingStyle = Realistic` for production visuals.
- Use physically motivated key, fill, and practical lights.
- Interiors need solid light-blocking walls at least 1 stud thick; 2–2.5 studs
  is safer for important structures.
- Keep bloom, sun rays, depth of field, color correction, and camera effects
  subtle. Depth of field should normally be reserved for cinematics.
- Each map may have its own lighting profile, but exposure and gameplay
  readability must remain consistent.
- Use warm practical lights against cool exterior ambience for dark-fantasy
  interiors.

### Materials and textures

- Roblox uses a metalness/roughness PBR workflow.
- PBR sets may include albedo/color, OpenGL tangent-space normal (Y+), roughness,
  metalness, and selective emissive masks.
- Use `MaterialVariant` for reusable tileable surfaces such as earth, rock,
  plaster, wood, and grass.
- Use `SurfaceAppearance` for UV-mapped hero meshes and unique props.
- Reserve 2K/4K textures for camera-critical unique assets. Prefer 256, 512, or
  1024 textures according to object size and screen importance.
- Reuse texture sets with tinting and variation instead of importing duplicates.

### Modeling

- Primitive Parts are acceptable for greybox, collision, hidden light blockers,
  and distant low-detail forms.
- Final houses, cliffs, ruins, weapons, creatures, and hero props should use
  authored or carefully generated meshes with clean scale, UVs, normals, and
  suitable topology.
- Preferred pipeline: Roblox greybox -> Blender model -> UV/retopo -> PBR bake
  and texture -> GLB/FBX -> Roblox import -> scale/material/LOD verification.
- Use modular kits, trim sheets, decals, and reusable props.
- Break perfect silhouettes and flat surfaces with secondary forms, vegetation,
  roots, erosion, damage, dirt, moss, and controlled asymmetry.

### Environment and atmosphere

- Use Terrain for natural ground where appropriate.
- Use custom terrain materials and MaterialVariants for hero environments.
- Use `Atmosphere`, `Sky`, dynamic `Clouds` under Terrain, and global wind.
- Use particles and mesh cards selectively for low clouds, fog pockets, dust,
  ash, rain, insects, leaves, and embers.
- Avoid excessive transparency overdraw.
- Use decals and vertex/texture variation to prevent obvious tiling.

### Audio

Sound is part of the visual-quality target. Each map should have layered ambience,
positional/volumetric sources, material-specific footsteps, occlusion-like
muffling, and appropriate reverb for interiors, caves, and large halls.

### Camera and animation

- Camera movement should feel weighted and cinematic without causing nausea.
- Camera shake, head bob, motion effects, and depth of field must be subtle and
  user-configurable where practical.
- Use authored interaction, locomotion, weapon, injury, and creature animations.

## Performance Standard

- Design for a selected low-end mobile baseline as well as high-end graphics.
- Enable and validate `Workspace.StreamingEnabled` for large maps.
- Reuse meshes, textures, materials, and packages.
- Use LOD or simplified distant silhouettes where appropriate.
- Disable unnecessary shadows on tiny, distant, transparent, or rapidly moving
  decorative objects.
- Limit overlapping transparent particles and lights.
- Keep `ReplicatedStorage` lean; do not load every map's heavy assets at join.
- Test with Studio performance stats, Scene Analysis, MicroProfiler, Device
  Simulator, and Network Simulator.
- Do not claim a scene is optimized until a representative gameplay path has
  been measured. Record device, graphics quality, FPS/frame time, memory,
  visible triangles, and draw/scene counts where available.

Roblox documentation gives roughly 1,000 draw calls and 1,000,000 visible
triangles as an example ceiling for a chosen low-end baseline scene, not a
universal guarantee. Real measurements decide the final budget.

## Available Production Tools

The connected Roblox Studio MCP has provided these relevant capabilities:

- Material, texture, mesh, procedural-model, scene, avatar, and animation
  generation.
- Direct Luau execution and multi-editing.
- Instance inspection, game-tree search, script search/read, console output.
- Screen capture for visual verification.
- Asset search, insertion, image storage/upload, and external asset import.
- Roblox skills: `rbx-docs-search`, `rbx-import-asset`, `rbx-scene-analysis`,
  `rbx-perf-profiling`, `rbx-device-simulator-lua`, `rbx-network-simulator`,
  `rbx-debug`, `rbx-instrument-analytics`, and experimentation/configuration
  guidance.

Rojo and Git are recommended for durable source code and history. MCP is useful
for live Studio editing and inspection. Their roles are complementary.

## Current State

The active Pink House production pass is in `Workspace.PinkHouseMap`. The
original 166-descendant greybox is preserved under
`ServerStorage.MapArchives.ReferenceMap_Greybox_2026_11_19`.

Current production elements:

- An eight-piece Blender-authored irregular front-cliff facade is retained as a
  permanent Roblox Model asset and in the recovery history, but is not active
  in the current live map; the retained collision cores carry the visible wall
  treatment for this composition pass.
- A roughly 501-stud vertical separation between the upper and lower meadows,
  composed so that the narrow fissure ends near the house instead of cutting
  through the entire world.
- Separate left/right front cliff cores and a continuous rear plateau.
- Generated PBR MaterialVariants for overgrown rock and meadow grass.
- Hundreds of varied hanging-growth strips on the front, sides, and chasm walls.
- A full-height functional inclined ladder connects the lower meadow to the
  upper meadow at the house-end of the fissure.
- Terrain lower meadow and enabled Workspace streaming.
- A Blender-authored low pink cross-gabled cottage with framed windows, porch,
  tiled roof, chimney, stone foundation, and an 86-object garden kit has replaced
  the previous tall modular house in the active map.
- The active cottage now uses saturated pink plaster, a rose clay-tile roof, a
  warm-white wooden door, translucent pale-blue glass, dark interior backing,
  and paired warm fabric curtains behind all four windows.
- Realistic LightingStyle, dynamic Terrain clouds, global wind, Atmosphere,
  subtle bloom/color correction/sun rays, and disabled
  gameplay depth of field.
- The rejected 62-emitter vapor layer is archived rather than active. Terrain
  Clouds now provide the sky layer without washing out the house and meadow.
- `HouseTestSpawn` is active on the safe side of the cottage at approximately
  `(145, 503.5, -85)` above the invisible collidable
  `HouseSpawnSafetyPlatform`; both the older map spawn and the default Workspace
  spawn are disabled.
- The complete upper meadow now has a real Terrain Grass surface at the correct
  plateau elevation across the left, right, and rear sections while preserving
  the single open fissure. Former opaque GrassCap parts are hidden and no longer
  cover the rendered Terrain blades.
- Nine tiled hanging-grass texture faces cover the front, outer sides, rear, and
  inner fissure walls over a continuous dark-green collision core.
- The earlier sparse 374-instance hanging-grass experiment remains preserved in
  the failed-wall-grass archive and is not active; it is not mixed into the
  restored dense layer.
- The rejected 130-panel v2 lattice is archived under
  `ServerStorage.MapArchives.BeforeCliffGrassV3_2026_11_21`. The subsequently
  rejected 24-MeshPart v3 shell is archived under
  `ServerStorage.MapArchives.RejectedCliffGrassV3_2026_11_21`; no procedural
  3D wall-grass shell is active in the live map.
- Unrelated `AscentGame` obby content, its `AscentServer`, `AscentHUD`, and
  `AscentRemotes`, plus the default `Baseplate` and disabled default spawn,
  are archived under
  `ServerStorage.MapArchives.ArchivedOtherContributor_AscentGame_2026_11_21`.
- A second-generation local Blender cliff-shell candidate is validated and
  exported, but is not active in Roblox pending visual review.
- The active Studio composition has been corrected to one continuous upper
  meadow with one narrow fissure ending before the house. The false horizontal
  canyon and perforated front facade are archived rather than deleted.
- The cottage is scaled to approximately 167 x 105 x 227 studs and surrounded
  by a denser 123-instance garden pass of shrubs, flowers, and stones.
- The cottage is now axis-aligned with the fissure instead of yawed 31.477
  degrees. Its stone foundation is embedded 0.5 stud into the Terrain surface,
  eliminating the visible floating gap.
- `InclinedLadder_v4` is approximately 21 studs wide and 551.87 studs long. It
  runs from the lower meadow at `(16.97, 3.2, -509)` to the upper meadow at
  `(16.97, 503, -275)` at 64.91 degrees above horizontal. It has two rails, 91
  rungs, and three overlapping invisible TrussPart climb surfaces spanning the
  full route. The previous `InclinedLadder_v3` and its associated composition
  are archived under `BeforeCompactFissure_2026_11_22`.
- The visible fissure is approximately 208 studs long and has a compact tapered
  plan shape instead of a constant-width rectangular slot.
  `Geometry.TaperedFissure_v2` widens from approximately 22 studs beside the
  house/ladder landing to 55 studs at the exposed front edge. The entire front
  cliff edge now begins at Z `-487`, so the shorter opening remains exposed to
  the lower meadow without creating a roof above the ladder. The house/garden
  group remains near Z `-170`, roughly 25 studs behind the fissure end.
- The upper meadow surface is now approximately Y `503` while the lower meadow
  remains approximately Y `2`. The active cliff cores are 500 studs tall with
  tops at approximately Y `493`; the house, ladder, spawn, and upper Terrain
  were lowered together by 682 studs. The complete pre-change map is preserved
  under `ServerStorage.MapArchives.BeforeHalfHeightCliff_2026_11_21`.
- The obsolete Grass Terrain slab left at approximately Y `1004`–`1012` after
  the height reduction has been removed from the live sky. Its original voxel
  region is recoverable from
  `ServerStorage.MapArchives.BeforeOverheadTerrainCleanup_2026_11_22`.
- An isolated 80 x 80 stud true-3D vertical wall-grass proof now exists in
  Blender and GLB form. It is deliberately not imported or active in Roblox
  until its density, projection, and top-lip silhouette receive visual approval.

This is the first production pass, not final 1:1 art. Composition and playable
scale are established; authored cliff meshes, foliage cards, final house meshes,
audio, and reference-matched cinematography remain.

## Known Limitations

- The front, side, and rear silhouettes currently expose large Part-based cores
  with tiled wall treatment. The authored cliff candidates are retained for
  recovery but are not active; approved authored geometry and foliage cards are
  still needed.
- Generated PBR grass is darker than the bright reference in some camera angles;
  lighting, tint, and material selection need another matching pass.
- The house is a detailed modular Part build, not yet a final Blender-authored
  mesh with unique PBR textures and a furnished interior.
- The ladder still uses repeated Parts and should eventually become an optimized
  modular mesh or package.
- The unacceptable sphere-based cloud clusters have been removed from the active
  map. Terrain Clouds now provide the sky layer, but ground-projected moving
  cloud shadows and distant volumetric layers still need a dedicated solution.
- The distant landscape is intentionally sparse and does not yet reproduce the
  reference's continuous meadow horizon and cloud shadows.
- A background procedural generation job temporarily removed a concurrently
  built house. The generated result was archived and the house was rebuilt after
  the job completed; avoid editing the same scene while generation jobs run.
- The prototype had not been saved to Roblox Cloud when last checked.
- The v2 cliff shell is a technically valid procedural candidate, not final
  photoreal art: it still needs reference-camera matching, unique PBR breakup,
  vegetation/erosion dressing, and an in-Studio silhouette review.
- The corrected active cliff face is intentionally continuous but visually too
  smooth at distance. It needs a non-perforating authored grass/soil surface
  and foliage breakup; the archived v2 shell must not be reinserted unchanged.
- The hanging-grass albedo backing image is still awaiting Roblox moderation;
  walls intentionally fall back to solid dark green until asset
  `81298258373496` becomes available.
- Both attempted procedural 3D wall-grass systems failed visual review. V3 also
  created an unacceptable giant overhead surface in gameplay and is archived;
  it must not be reinserted unchanged.
- Dense wall-grass coverage currently targets the front face and inner fissure.
  Outer side and rear walls still rely mainly on the tiled texture and lip
  fringe until the 507k-triangle hero-wall pass is profiled.
- The new cottage matches the low single-storey cross-gabled read much more
  closely. Its materials are currently Roblox material/color assignments rather
  than final baked PBR texture sets, and the roof intersections need one more
  polish pass.
- The house/garden group now sits immediately beside the shortened fissure end.
  Its pivot is approximately `(34, -170)` in XZ; the nearest house/garden edge
  is about 25 studs behind the fissure end at Z `-275`.
- Terrain grass height is engine-controlled and is taller/coarser than the
  short photographic grass in the reference at close gameplay distance.

## Next Priorities

1. Review the isolated 80 x 80 stud Blender wall-grass proof from its front,
   oblique, side, and upper-lip captures; import it only after visual approval.
2. Add rear-wall coverage only after the approved proof exists; keep the
   PBR wall as the distant backing surface.
3. Add unique PBR breakup and tune grass/cliff response against fixed matched
   video cameras.
4. Polish the Blender cottage roof intersections and create final plaster, tile,
   glass, stone, and garden PBR treatment.
5. Polish the full-height ladder's visible landings and the new 55-to-22-stud
   tapered fissure edges while preserving the verified R15 traversal.
6. Replace the 96-Part ladder prototype with an optimized authored model once
   its final composition is approved.
7. Add roots, erosion, decals, soft low clouds, a distant meadow horizon, and
   moving cloud-shadow treatment.
8. Add layered wind, house, chasm, and ladder ambience.
9. Validate representative desktop and mobile camera paths, not only the current
   spawn view.
10. Finish this vertical slice before producing additional maps.
11. Keep the approved approximately 501-stud upper/lower meadow separation fixed
    unless a new reference-matched composition pass explicitly replaces it.
12. After any future vertical Terrain move, ray-test the full former elevation
    range so no detached voxel layer remains above the playable meadow.

## Implementation Notes

- The first scene was generated through Roblox Studio MCP using Luau.
- Existing user content outside `ReferenceMap` was intentionally preserved.
- A visual overview was captured after generation.
- Lighting effects were created in a second pass after the initial operation
  stopped on a restricted lighting-property write.
- The modern `LightingStyle = Realistic` property was successfully set through
  MCP during the production pass.
- Custom materials were generated as four variants each under MaterialService's
  `AssistantMaterials` folders. Selected variants are applied to cliff cores and
  grass caps.
- Workspace streaming is enabled with a 128-stud minimum and 512-stud target
  radius for the current prototype.
- Blender 5.3.0 for Apple Silicon is installed and verified at
  `/Applications/Blender.app`.
- The first authored cliff kit is saved as
  `blender/pink_house_cliff_modules.blend` and exported to
  `exports/pink_house_cliff_modules.glb`.
- The expanded candidate is reproducibly generated by
  `blender/build_cliff_shell_v2.py`, saved as
  `blender/pink_house_cliff_shell_v2.blend`, and exported as
  `exports/pink_house_cliff_shell_v2.glb`. The editable file retains two red
  verification markers; the production GLB excludes them.
- Independent clean-scene reimport through `blender/validate_glb.py` reported
  36 production meshes, 192,520 total triangles, 9,450 maximum triangles on a
  single mesh, and bounds of approximately 1,502 x 694 x 1,007 studs at the
  project's 0.28 m/stud conversion. Final GLB SHA-256 is
  `a057207758137d0545c919f9ec900581e1489144f545b10bb1ceb8a67c2bb992`.
- A project-local `roblox-blender-asset` skill now records the measured Blender
  to Roblox workflow, validation gates, scale convention, and upload consent
  boundary under `.agents/skills/roblox-blender-asset/`.
- The reference cottage is generated by
  `blender/build_reference_pink_house.py`, saved as
  `blender/pink_house_reference_v1.blend`, previewed at
  `exports/pink_house_reference_v1_preview.png`, and exported as
  `exports/pink_house_reference_v1.glb`. Clean reimport reported 124 meshes,
  7,752 triangles total, 108 maximum triangles per mesh, and an envelope of
  approximately 216 x 87 x 160 studs at 0.28 m/stud. Final named-mesh GLB
  SHA-256 is `f39b4164366cc0c8fdc583bb5d8ad29060c9d31ea6cc875a5625a483034fb285`.
- Roblox Model asset `102586129289574` is the active named-mesh cottage import.
  It is scaled by 3.571429, anchored, placed at the corrected meadow height,
  rotated so the entrance faces the fissure, and uses Roblox material/color
  assignments. Asset `72217119043698` was the first white-material import and
  is archived from the active map.
- The hanging-grass source is reproducibly generated by
  `blender/build_hanging_grass_kit.py`, saved as
  `blender/pink_house_hanging_grass_v1.blend`, previewed at
  `exports/pink_house_hanging_grass_v1_preview.png`, and exported as
  `exports/pink_house_hanging_grass_v1.glb`. Clean reimport reported eight
  meshes, 1,712 triangles total, 244 maximum triangles per mesh, and an envelope
  of approximately 26.93 x 7.47 x 64 studs. GLB SHA-256 is
  `6c6c682e6ee7b18c5624629c41bb4b3b7d4d62ef29017f56aece962ac44fef55`.
- Roblox Model asset `140006443989412` contains the eight source grass modules.
  Its inserted package source is preserved under
  `ServerStorage.ImportedAssetSources.HangingGrassKitV1`; active clones are in
  `Workspace.PinkHouseMap.HangingGrass3D_v1`, scaled by 3.571429, anchored,
  double-sided, non-colliding, and tinted as LeafyGrass.
- Dense wall panels are generated by
  `blender/build_wall_grass_panels_v1.py`, saved as
  `blender/pink_house_wall_grass_panels_v1.blend`, previewed at
  `exports/pink_house_wall_grass_panels_v1_preview.png`, and exported as
  `exports/pink_house_wall_grass_panels_v1.glb`. Clean reimport reported four
  meshes, 15,600 triangles total, 3,900 maximum per mesh, and an envelope of
  approximately 102.14 x 5.4 x 213.78 studs. GLB SHA-256 is
  `e7f8fb9b1a76554c72bd678b51548e2a1004971a7db33efdac45a587bf911893`.
- Roblox Model asset `88989842398880` stores the four dense panel variants.
  The source package is preserved under
  `ServerStorage.ImportedAssetSources.DenseWallGrassPanelsV1`; its 130 rejected
  clones are archived under
  `ServerStorage.MapArchives.BeforeCliffGrassV3_2026_11_21`.
- The replacement v3 shell is generated by
  `blender/build_cliff_grass_shell_v3.py`, saved as
  `blender/pink_house_cliff_grass_shell_v3.blend`, and exported as
  `exports/pink_house_cliff_grass_shell_v3.glb`. Clean reimport reports 24
  meshes, 165,600 triangles total, 7,500 maximum triangles per mesh, and bounds
  of approximately 1,414 x 940 x 1,017 studs before in-Studio orientation.
  GLB SHA-256 is
  `2f77ad6c57a98ad42bce571ba54861a406f4c3206a7fd8f32df55d3cd792c01a`.
  Approved Model asset `100772135265591` was tested as
  `Workspace.PinkHouseMap.CliffGrassShellV3`, then rejected and moved to
  `ServerStorage.MapArchives.RejectedCliffGrassV3_2026_11_21`. It is retained
  only for audit/recovery and is not active gameplay geometry.
- The cliff GLB was uploaded once as permanent Model asset `124672594627247`.
  Its prior package copy used a 3.571429 scale factor and was separated around a
  roughly 25-stud central opening. It is no longer active in
  `Workspace.PinkHouseMap`; the current 500-stud cliff cores remain responsible
  for collision and wall presentation.
- The half-height composition keeps the lower meadow at approximately Y `2`,
  places the upper Terrain Grass surface at approximately Y `503`, and uses
  500-stud cores centered at Y `243.239` with tops at Y `493.239`. The cottage
  bounding-box bottom is Y `499.232`, so its foundation is embedded rather than
  floating. The then-active `InclinedLadder_v2` and the house spawn were
  translated with the upper composition rather than rebuilt independently.
- The active `InclinedLadder_v4` uses exact endpoints `(16.9704, 3.2, -509)`
  and `(16.9704, 503, -275)`, a 551.87-stud route at 64.91 degrees. Its climb
  collision is split into three overlapping centered TrussParts; a single
  full-length TrussPart would exceed Roblox's 512-stud size limit.
- `Geometry.TaperedFissure_v2` uses two vertical WedgeParts to create a
  symmetric plan-view taper from 55 studs at Z `-487` to 22 studs at Z `-279`.
  `LeftCliffCore` and `RightCliffCore` retain their outer X and rear Z bounds,
  but their front edge moved 80 studs back and their depth is now 540 studs.
  The upper Terrain strip over the former front extension was removed, then the
  narrower taper was rebuilt at 4-stud voxel resolution with its surrounding
  Grass surface matched to Y `503.016`.
- The detached old Terrain layer occupied approximately X `-720..740`,
  Y `1004..1012`, and Z `-580..2120`. The cleanup archived cell region
  `(-180,248,-145)` through `(185,256,530)` as
  `OldOverheadGrassTerrain_Y992_1024`, then cleared only Y `968..1048`; the live
  upper and lower meadow elevations were outside that operation.
- The isolated wall-grass proof is reproducibly generated by
  `blender/build_wall_grass_proof_v1.py` from the acceptance specification in
  `blender/pink_house_wall_grass_proof_v1_spec.md`. Its editable source is
  `blender/pink_house_wall_grass_proof_v1.blend`; its five selected production
  meshes export to `exports/pink_house_wall_grass_proof_v1.glb`. The 80 x 80
  stud module is divided into four independently importable quadrants plus a
  short upper-lip strip. Clean reimport reported 68,196 triangles total, 16,224
  maximum triangles per mesh, bounds of approximately 81.00 x 5.59 x 81.36
  studs at 0.28 m/stud, and SHA-256
  `1272104348495e3eb5513a72001e666731e82785fd2a9b4fc5265dee0311d42f`.

## Audit Log

Use this compact format for every material graphics change:

```text
YYYY-MM-DD — Short title
Scope: map/assets/settings changed
Implementation: concise description of how it was made
Verification: capture/playtest/profile performed and result
Performance: measurements or "not measured"
Limitations: remaining issues
Next: immediate follow-up
```

### 2026-11-20 — Rojo & Git team collaboration setup

Scope: Repository root (`rokit.toml`, `default.project.json`, `README.md`, `AGENTS.md`, `.gitignore`) and `src/` Luau structure.

Implementation: Initialized Rokit with `rojo 7.7.1`, created `default.project.json` mapping `src/server` (`ServerScriptService`), `src/client` (`StarterPlayer.StarterPlayerScripts`), and `src/shared` (`ReplicatedStorage.Shared`) with `"$ignoreUnknownInstances": true` so syncing preserves all Studio-authored map geometry, Terrain, Lighting, and archives. Exported active `ServerScriptService.WallGrassLODController` to `src/server/WallGrassLODController.server.luau` and added starter `src/shared/GameConfig.luau` and `src/client/ClientInit.client.luau`.

Verification: Ran `rojo build default.project.json -o /tmp/dark-fantasy-test.rbxlx` and confirmed clean build with exit code 0.

Performance: Not measured (no runtime scene changes).

Limitations: Map geometry (`Workspace.PinkHouseMap`), Terrain, and Lighting remain hosted in the Roblox Cloud place (`placeId: 96826195026003`); collaborators need Team Create access (or a `.rbxl` snapshot) alongside `rojo serve` to run the full map.

Next: Enable Team Create for collaborators if needed and continue vertical-slice development with all new Luau scripts authored in `src/`.

### 2026-11-19 — Initial Pink House greybox

Scope: `Place1` / `Workspace.ReferenceMap` and Lighting effects.

Implementation: Created the monolith, chasm, ladder, primitive house, small
garden, lower meadow, spawn, and first cinematic atmosphere through MCP Luau.

Verification: Confirmed `ReferenceMap` existed with approximately 166
descendants and captured an overview from Studio.

Performance: Not measured.

### 2026-11-20 — Blender cliff shell v2 candidate

Scope: Local Pink House cliff, side silhouettes, and inner chasm asset set.

Implementation: Rebuilt the shell as 24 modular cliff surfaces plus 12 embedded
hero rock masses using deterministic layered noise. Preserved verification
markers in the editable Blender source and excluded them from the production
GLB. No Roblox asset was created and the live place was not modified.

Verification: Inspected the source from multiple viewpoints through BlendRelay,
saved checkpoints during iteration, exported GLB, and reimported it into a clean
Blender 5.3 scene successfully. The clean import contains 36 meshes and no
verification markers.

Performance: Geometry audit only: 192,520 triangles total and 9,450 maximum per
mesh. Runtime frame time, memory, draw calls, streaming, and mobile performance
were not measured because the candidate has not been inserted into Studio.

Limitations: Procedural rock breakup remains visible and the asset has no final
unique PBR textures, vegetation cards, collision, LOD evaluation, or matched
reference-camera approval. This is not yet a complete 1:1 recreation.

Next: Morning visual review, then either revise the candidate or explicitly
approve permanent Roblox upload and an in-Studio integration/performance pass.

### 2026-11-20 — Reference composition correction

Scope: `Workspace.PinkHouseMap` upper meadow, fissure, cottage, garden, cliff
surface, lighting, and ladder gameplay surface.

Implementation: Archived the previous active facade, 390-piece repeated cliff
detail layer, ladder, and cottage under
`ServerStorage.MapArchives.ReferenceCorrection_Before_2026_11_20_0750`.
Closed the unintended transverse canyon by moving the rear plateau to meet the
fissure termination, retained one 26-stud central fissure, converted visible
cliff cores to continuous LeafyGrass surfaces, scaled and lifted the cottage,
added 123 garden details, and replaced the vertical ladder with a broad inclined
ladder. Tuned sunlight for stronger natural form shadows.

Verification: Captured top/reference and front-wall views. The upper view now
shows one continuous field and one fissure; the front wall no longer contains
false black openings. Play mode confirmed 12 climbable TrussPart sections at
runtime, spanning nominal Y coverage from approximately -4 to 1,022 studs.

Performance: No frame-time or memory profile taken. Active scene descendant
count after the first correction was 362 before adding the 123-piece garden.

Limitations: A full player-controlled bottom-to-top climb has not yet been
performed. The house silhouette remains unlike the final reference, the wall
surface is too smooth, and garden primitives are an interim dressing pass.

Next: Author the reference-matched cottage and a continuous non-perforating
grass/soil cliff shell, then conduct manual R15 climb and representative device
performance tests.

### 2026-11-20 — Blender cottage and cloud correction

Scope: Active Pink House cottage, garden, clouds, and sunlight response.

Implementation: Removed the sphere-based LowClouds folder from the active map
and retained it only in the existing archive. Enabled and tuned Terrain Clouds.
Built a reproducible Blender cottage with a low cross-gabled silhouette, front
wing, chimney, windows, porch, stairs, foundation, 34 shrubs, 22 flower accents,
and 30 border stones. Uploaded and inserted the named-mesh v2 asset, archived
the previous cottage/garden and first white import, scaled and oriented the new
model, and assigned Roblox materials and colors by semantic mesh name.

Verification: Rendered a Blender preview, clean-reimported the exported GLB,
verified 124 meshes / 7,752 triangles, and captured the active Studio model from
the fissure-facing side. The front now reads as a low pink cottage with visible
windows, entrance, roof, chimney, shadows, and a surrounding garden.

Performance: Geometry only: 7,752 triangles total; runtime frame time, memory,
draw calls, and mobile performance not measured.

Limitations: Terrain Clouds do not yet reproduce the reference's low volumetric
cloud banks and moving ground shadows. Cottage roof intersections and final PBR
maps remain to be polished. The cliff wall remains too smooth.

Next: Author the continuous grass-covered cliff wall and cloud-shadow treatment,
then polish cottage PBR and profile the representative camera path.

### 2026-11-20 — Cottage color, windows, and placement pass

Scope: `Workspace.PinkHouseMap.PinkHouse_Blender_v2` materials, windows,
interior dressing, and placement relative to the fissure ladder.

Implementation: Preserved a pre-change clone in the existing map archive.
Changed walls to saturated pink plaster, roof to rose clay tile, and door to
warm white wood. Increased glass transparency, added dark interior shadow cards,
and placed paired fabric curtain panels behind each of four windows. Shifted the
complete cottage/garden group from approximately `(78, 205)` to `(48, 190)` in
XZ so the entrance sits closer to the ladder without covering the chasm.

Verification: Studio capture confirms visible pink walls, white entrance, window
frames/curtains, garden shadows, and safe fissure clearance. Door position is
approximately `(29.5, 1034.9, 125.8)`; ladder top is near `(0, 1008, 78)`.

Performance: Added 12 non-colliding window-detail Parts. Runtime performance not
measured.

Limitations: Curtains are simple interim geometry and there is no furnished
walkable interior yet. Final glass/PBR response requires a close gameplay test.

Next: Build the non-perforating grass cliff shell, then polish cottage roof/PBR
and test windows and ladder from a normal R15 gameplay camera.

### 2026-11-20 — Cottage moved to fissure edge

Scope: Active Blender cottage and garden placement.

Implementation: Shifted the complete group to approximately `(45, 168)` in XZ,
placing the front garden and entrance directly beside the chasm termination.

Verification: Studio capture confirms the garden edge meets the fissure approach;
door position is approximately `(26.5, 103.8)` in XZ and its horizontal distance
to the ladder top is approximately 37 studs.

Performance: Unchanged.

Limitations: Final porch/ladder transition still needs a normal R15 walk test.

Next: Test the short approach and adjust only if the character catches on the
garden border or fissure lip.

### 2026-11-20 — House test spawn

Scope: Pink House playtest spawn.

Implementation: Disabled the old spawn and created `HouseTestSpawn` beside the
cottage on stable upper meadow ground.

Verification: Play mode placed the player near `(142.8, 1017.5, 182.1)`, beside
the intended spawn at `(145, 1014, 185)`.

Performance: Negligible.

Limitations: Test spawn is intentionally visible at 65% transparency in Edit
mode and should be hidden for release.

Next: Use this spawn for rapid house, fissure, and ladder iteration.

### 2026-11-20 — Upper meadow and hanging-grass coverage

Scope: Upper plateau Terrain and every visible vertical monolith wall.

Implementation: Added 4-stud Terrain Grass overlays to all three upper meadow
sections with `Terrain.Decoration` enabled and kept the central fissure empty.
Rejected a 418-Part rectangular strip experiment after capture showed obvious
banding. Generated a seamless dense hanging-grass/ivy albedo, saved it as
`textures/cliff_hanging_grass_albedo_v1.png`, uploaded Decal asset
`117131796857966`, and assigned its backing image `81298258373496` through nine
tiled Texture faces on the front, sides, rear, and chasm walls.

Verification: Play capture confirmed the upper meadow now renders with the same
Terrain grass surface family as the lower field. Front capture rejected the
temporary block-strip treatment and confirmed it was removed. Texture image is
not yet visible because Roblox reports its backing image moderation as pending.

Performance: Removed the 418 temporary strip Parts. Final wall treatment uses
nine Texture instances plus three Terrain fill regions; runtime profile pending.

Limitations: Roblox moderation must complete before final wall visual matching
can be captured. Texture is albedo-only; normal/roughness maps are still needed.

Next: Re-check backing image moderation, capture all wall faces once available,
then add restrained geometric fringe only along camera-critical top edges.

### 2026-11-20 — Modular 3D hanging-grass pass

Scope: Pink House upper cliff lips, front/outer walls, and inner fissure walls.

Implementation: Built eight Blender ribbon-grass modules, exported and clean-
reimported the GLB, uploaded approved Model asset `140006443989412`, and placed
374 non-colliding instances over the tiled wall treatment. Corrected the GLB
metre-to-stud scale, reduced the first overly dense layout, narrowed cluster
widths, varied colour/tilt, and shifted lip modules below the plateau edge.

Verification: Blender preview and clean import confirmed eight meshes and 1,712
triangles. Studio front and oblique captures confirmed the modules project from
the wall, cast depth shadows, and no longer stand above the meadow like a fence.

Performance: Active geometric layer is approximately 80,000 source triangles
before visibility/streaming culling. Runtime frame time, draw calls, and mobile
performance have not yet been measured.

Limitations: Repeated ribbon silhouettes remain visible at close range and the
active layer uses many MeshPart instances. It is a first geometric breakup pass,
not final photoreal vegetation.

Next: Profile representative cameras, consolidate distant repetitions, and
author a smaller number of more organic hero clumps for close fissure views.

### 2026-11-20 — House spawn priority correction

Scope: Pink House player spawn locations.

Implementation: Found the default `Workspace.SpawnLocation` still enabled at
ground level. Disabled it and the retained old map spawn, then made
`HouseTestSpawn` at `(145, 1015, 185)` the only enabled SpawnLocation.

Verification: A fresh Play session placed the local HumanoidRootPart at
approximately `(140.8, 1018.5, 183.9)`, safely beside the cottage.

Performance: Negligible.

Limitations: None known for the current single-spawn prototype.

Next: Re-test after adding teams, checkpoints, or map-selection spawning.

### 2026-11-20 — Dense 3D grass wall conversion

Scope: Pink House front cliff and both inner fissure walls.

Implementation: Authored four reusable 100 x 200-stud Blender panels, each with
650 crossed low-poly grass blades projecting from the wall. Uploaded approved
Model asset `88989842398880`, corrected metre-to-stud scale, tiled 70 panels
across the front and 60 inside the fissure, and removed 95 obsolete sparse
mid-wall grass clusters while preserving the upper-lip fringe.

Verification: Clean GLB reimport confirmed four meshes and 15,600 triangles.
Studio face-on and oblique captures confirmed continuous visual coverage and
visible geometric depth away from the wall plane.

Performance: Approximately 507,000 source triangles across 130 MeshParts before
visibility and streaming culling. Runtime frame time and mobile performance are
not yet measured.

Limitations: The tiled albedo remains as a necessary distant/gap-fill layer.
Outer sides and rear wall have not received the dense geometry pass pending
  profiling of the hero walls.
- All previous painted-wall textures, sparse wall-grass modules, dense-panel
  attempt, and the oversized LOD0 orientation test are now removed from the
  active map and preserved under
  `ServerStorage.MapArchives.FailedWallGrass_2026_11_20`. Active cliff walls use
  a dark Slate fallback until the replacement production module is approved.
- The rejected distance-streamed wall-grass corridor is no longer active. Its
  468 sectors and controller are preserved only in
  `ServerStorage.MapArchives.FailedWallGrass_2026_11_20`; real Terrain grass
  remains enabled on the upper and lower horizontal meadows.

Next: Profile the front and fissure gameplay path, then create a cheaper distant
LOD panel before extending geometric coverage to outer and rear walls.

### 2026-11-20 — Wall-grass prototype rejection and cleanup

Scope: Active cliff wall vegetation experiments.

Implementation: Removed the stretched grass image and both earlier sparse/dense
panel systems from the active map. Built a 900-blade 25 x 50-stud LOD0 module,
identified and corrected Blender-to-Roblox outward-normal orientation, then
rejected the integration because doubling panel scale made the blades visibly
oversized. Archived every rejected system rather than deleting it.

Verification: Close Studio captures exposed both the original inward-facing
orientation and the later oversized blade silhouette. Active map was returned
to a clean dark Slate fallback with no rejected grass system left visible.

Performance: Rejected LOD0 test would have used about 1.17 million triangles;
it was archived before being accepted. Runtime performance was not claimed.

Limitations: Production 3D wall grass is not yet installed.

Next: Author a roughly 50 x 100-stud module containing about 3,000 correctly
sized blades under the per-mesh triangle limit, plus lower-density LOD1/LOD2,
then profile one ladder-sector slice before expanding coverage.

### 2026-11-20 — Working ladder-corridor grass streaming

Scope: Both fissure walls along the full inclined ladder trajectory.

Implementation: Reused the validated 900-blade LOD0 modules at their correct
physical blade scale, split the ladder corridor into 468 small sectors, disabled
collision/touch/query/shadows, and added `ServerScriptService.WallGrassLODController`.
The controller updates every 0.25 seconds and shows a sector only when at least
one player is within 135 studs; only sectors within 55 studs cast dynamic
shadows, and the dark Slate cliff remains the far LOD.

Verification: Fresh Play test near `(0, 900, 20)` reported 60 visible sectors
and 356 hidden among the 416 sectors currently streamed to that client. The
remaining 52 sectors were outside the client's Workspace streaming radius.

Performance: Approximately 324,000 source triangles visible in the measured
ladder position, versus roughly 2.5 million if every sector were rendered.
Frame time, draw calls, and mobile GPU time still require formal profiling.

Limitations: This is the ladder corridor only. LOD1 is currently represented by
the plain dark-green cliff rather than a separate medium-detail foliage mesh.

Next: Capture close gameplay views, tune the 135-stud radius, run desktop/mobile
profiling, then extend the same sector system to other camera-visible walls.

### 2026-11-20 — Rejected wall-grass streaming rollback

Scope: `Workspace.PinkHouseMap.WallGrassStreamingSectors`,
`ServerScriptService.WallGrassLODController`, and the Rojo server source.

Implementation: Removed the complete 468-sector streaming mesh layer from the
active map and moved it, together with its disabled controller, to
`ServerStorage.MapArchives.FailedWallGrass_2026_11_20`. Deleted
`src/server/WallGrassLODController.server.luau` so Rojo cannot restore the
rejected system. Kept `Terrain.Decoration` enabled and did not alter the real
upper/lower meadow grass, house, ladder, or clouds.

Verification: Studio inspection reports no active `WallGrassStreamingSectors`
folder and no active wall-grass controller; the rejected folder is present in
the archive and Terrain decoration remains enabled. Captured post-rollback
upper and side views showing clean cliff cores without the streamed plants.

Performance: Removed 468 active MeshParts and the 0.25-second server distance
update loop. Frame time and GPU cost were not re-measured.

Limitations: Vertical cliff walls are intentionally plain while a better
authored solution is designed; only horizontal Terrain surfaces currently have
true grass decoration.

Next: Fix the floating cottage placement, then design one optimized authored
cliff-surface solution and approve it from a small visual test before scaling.

### 2026-11-21 — House grounding and real upper grass correction

Scope: `Workspace.PinkHouseMap.PinkHouse_Blender_v2`, upper plateau Terrain,
cliff materials, test spawn, clouds, and rejected atmosphere archive.

Implementation: Archived the pre-change cottage and the complete 62-emitter
`VolumetricCloudLayers_v1` under
`ServerStorage.MapArchives.BeforeGroundingAndGrass_2026_11_21`. Straightened the
cottage from 31.477 degrees to world-axis alignment, shifted it toward the
fissure centerline, and lowered it until `StoneFoundation_mesh` sits 0.5 stud
below the measured Terrain surface at Y=1185.25. Rebuilt Grass Terrain at the
actual plateau height, hid the three flat GrassCap cover parts, enabled Terrain
decoration, and set a darker reference-oriented Grass material color. Corrected
the cliff cores to use the Rock base required by their existing overgrown PBR
MaterialVariants, brightened their tint, removed shadows from invisible ladder
climb surfaces, softened Terrain Clouds, and aimed `HouseTestSpawn` toward the
house.

Verification: Fixed-view captures confirm a level grounded cottage, visible
Terrain blades across the upper meadow, no white particle washout, and textured
grass/rock cliff walls. Fresh Play placed the HumanoidRootPart at approximately
`(142.8, 1189.25, 184.6)` beside the house. Foundation bottom measured
Y=1184.75 against Terrain Y=1185.25.

Performance: Spawn-view SceneAnalysis measured 270,470 creator-controlled
triangles and 162 draw calls excluding shadow passes (Grass 227,304/33,
Terrain 33,720/76, Opaque 9,440/47, Transparent 1/1, Clouds 5/5). Runtime scene
contained 957 instances. Shadow passes were 1,346,856 triangles/771 draws and
are engine-driven.

Limitations: The large cliff silhouette remains mostly core-based and the
overgrown PBR pattern reads horizontally at close range; it is an optimized
surface treatment, not final authored hanging vegetation. Terrain grass blade
height cannot match the short reference lawn exactly. House materials still
need unique final PBR maps.

Next: Build and approve one camera-matched authored cliff-wall module with
vertical hanging growth, then apply it only after side-by-side reference review.

### 2026-11-20 — Near and lower vapor cloud layers

Scope: Pink House sky, plateau mist, and lower chasm atmosphere.

Implementation: Added eight upper and fourteen lower invisible box-volume
emitters using Roblox's soft smoke texture, long lifetimes, low velocity, mild
wind acceleration, high transparency, and flattened particle squash. Upper mist
sits near Y=1062; the lower bank sits around Y=560 with vertical variation.

Verification: Elevated Studio capture confirmed soft irregular vapor patches
without the rejected sphere-cluster silhouette or opaque rectangular cards.

Performance: 62 low-rate emitters; runtime overdraw and mobile GPU cost not yet
profiled.

Limitations: Particle clouds do not create physically accurate volumetric light
scattering or projected cloud shadows.

Next: Playtest from plateau and ladder cameras, tune density, and profile
transparent overdraw before adding more emitters.

Limitations: Greybox geometry, primitive house, flat cliffs, excessive haze,
unverified streaming, no mobile or profiler test.

Next: Save the place, enable Realistic Lighting manually, then begin the
production cliff/material pass.

### 2026-11-20 — Pink House production pass 1

Scope: `Workspace.PinkHouseMap`, Lighting, Terrain, MaterialService, and the
archived original greybox.

Implementation: Archived the original greybox, rebuilt the plateau so the
fissure terminates beside the house, layered hanging cliff vegetation, rebuilt
the ladder, generated and applied PBR cliff/grass MaterialVariants, created a
detailed modular cottage and garden, enabled streaming, and added realistic
lighting, dynamic clouds, wind, atmosphere, low cloud clusters, and a test spawn.

Verification: Inspected the map and house hierarchy, captured overview and close
Studio views, started a play session, ran SceneAnalysisService instance and
triangle composition queries, and returned Studio to Edit mode.

Performance: In the sampled spawn view, Opaque rendered about 7,284 triangles
and 11 draw calls; Transparent 1 triangle/1 draw; Clouds 5 triangles/5 draws.
Terrain rendered about 17,176 triangles/28 draws and Terrain grass about 292,480
triangles/44 draws. Shadow passes are engine-driven and excluded from the
creator-controlled comparison. Runtime instance composition reported 842 total
instances, including player/core runtime objects.

Limitations: Current cliff vegetation uses many simple Parts, house is not yet
an authored Blender/PBR asset, clouds are partly stylized spheres, distant world
and audio are unfinished, and performance has only been sampled from one view.

Next: Save the place, then replace the visible cliff shell and house with final
authored assets while matching fixed reference cameras.

### 2026-11-20 — Blender cliff kit prepared

Scope: Local Blender source and GLB export for the Pink House front cliff.

Implementation: Created eight deterministic irregular cliff facade modules in
real-world metre scale. Combined target size is approximately 1,360 x 14 x 1,000
Roblox studs after conversion. Added one asymmetric top-left verification marker
for orientation checks and exported meshes/materials as a single GLB.

Verification: Blender 5.3 completed the background build and GLB export. The
source `.blend` is approximately 143 KB and the GLB approximately 254 KB. The
planned geometry is about 9,420 triangles total, comfortably below the Roblox
per-mesh import limit.

Performance: Not measured in Roblox because the permanent asset has not yet
been uploaded or inserted.

Limitations: Source material is a plain rough green preview material; Roblox
will receive the existing generated overgrown-cliff MaterialVariant after
import. Upload and in-Studio scale/orientation verification are pending explicit
asset-creation consent and MCP upload-folder approval.

Next: Upload the GLB once approved, insert it, scale to 1,360 x 14 x 1,000
studs, orient the marked edge correctly, anchor it, and replace the visible
front cliff shell while retaining the core for collision.

### 2026-11-20 — Authored front cliff imported

Scope: `Workspace.PinkHouseMap.AuthoredFrontCliff` and permanent Roblox Model
asset `124672594627247`.

Implementation: Uploaded the approved GLB once through Open Cloud, inserted its
package copy, corrected GLB metre-to-stud scale by 3.571429, used the asymmetric
marker to correct orientation, split the four left and four right modules around
the chasm, anchored all mesh parts, disabled mesh collision, and applied the
existing overgrown-cliff MaterialVariant. Retained the original cores for stable
collision and removed the temporary orientation marker from the placed copy.

Verification: Roblox reported the asset Approved and Active. Verified nine
imported mesh parts before removing the marker, eight final cliff modules, final
bounding size approximately 1,387 x 1,000 x 28 studs, a roughly 25-stud central
opening, top/bottom alignment, material assignment, anchoring, and front and
angled Studio captures.

Performance: Imported facade geometry is approximately 9,420 source triangles;
runtime frame time and full scene composition were not re-profiled in this pass.

Limitations: The package asset itself contains the raw unscaled import; scale,
orientation, material, collision, and placement repairs currently exist on this
inserted package copy. Side and rear Part silhouettes remain visible, and the
existing hanging-growth strips still dominate the facade at distance.

Next: Extend authored geometry around the sides, replace repeated growth strips
with optimized foliage cards, then re-run scene analysis from matched reference
cameras.

### 2026-11-21 — Static true-3D cliff grass restored

Scope: `Workspace.PinkHouseMap.DenseWallGrass3D_v2_Static`, the front monolith
face, and both inner fissure walls.

Implementation: Restored 130 dense Blender-authored MeshPart panels from
`ServerStorage.MapArchives.FailedWallGrass_2026_11_20.DenseWallGrass3D_v1` and
translated them by `(16.9704, 175.2394, -64)` into the current map coordinates.
Each panel contains 650 crossed blades. All panels are anchored, double-sided,
non-colliding, non-queryable, shadowless, and use Performance render fidelity.
No distance controller or custom streaming script was restored.

Verification: Edit-mode face-on and close oblique captures confirmed continuous
front/fissure coverage, visible blade depth, correct alignment below the upper
meadow, and no plants standing above the lip. A fresh Play session confirmed
the layer streams normally with Workspace streaming.

Performance: At a close fissure camera, SceneAnalysis measured 94,127 total
triangles and 187 draw calls: Opaque 86,340/8, Terrain 4,892/147, Terrain Grass
2,888/25, Transparent 1/1, and Clouds 6/6. Thirty of the 130 wall panels were
streamed to that client view. The spawn view remained 268,330 creator-controlled
triangles and 157 draws excluding engine shadow passes.

Limitations: Four repeating panel variants create a visible crossed-blade grid
at very close range. Dense geometry currently covers the front and inner
fissure, not the outer sides or rear wall.

Next: Create an irregular v3 Blender panel set with clumped hanging blades,
length variation and broken seams, then compare it against the supplied video
from the same fixed oblique camera before replacing this accepted functional
3D baseline.

### 2026-11-21 — Reference-frame cliff grass shell v3

Scope: Blender v3 cliff vegetation asset, `Workspace.PinkHouseMap`, front and
outer monolith walls, inner fissure walls, and obsolete edge bars.

Implementation: Extracted the 14.418-second reference into 29 half-second
frames and used its aerial, frontal, ground and house-close views as the shape
authority. Built 24 unique Blender meshes containing 55,200 varied downward
blades, exported GLB `pink_house_cliff_grass_shell_v3.glb`, uploaded approved
Model asset `100772135265591`, repaired import scale/orientation, and aligned it
to world bounds `(-677.94, 185.25, -563.81)` through
`(711.88, 1185.25, 49.81)`. Archived the rejected 130-panel v2 layer and four
blocky `ReferenceGrassEdges`; collision remains on the original cliff cores.

Verification: Blender front/oblique previews and Studio fixed-camera captures
confirmed continuous fine vertical coverage on the front, both outer sides and
both fissure walls, with the single narrow opening retained. Clean GLB reimport
confirmed 24 meshes, 165,600 triangles total and 7,500 maximum per mesh.

Performance: Reference aerial Play camera measured 81,321 visible triangles and
303 draw calls total: Opaque 54,932/143, Terrain 26,382/153, Transparent 1/1,
and Clouds 6/6. Wall MeshParts have collision, touch, query and shadows disabled.

Limitations: The backing cliff core is still geometrically straight and a thin
upper material transition can remain visible from extreme editor-only aerial
angles. The result is a materially better reference-directed baseline, not a
claim of pixel-identical final art.

Next: Tune the upper transition and wall colour from the supplied fixed frames,
then continue with cloud scale/shadows and house proportion matching.

### 2026-11-21 — Emergency rollback of rejected v3 shell

Scope: `Workspace.PinkHouseMap.CliffGrassShellV3`, cliff-wall presentation, and
all active `SpawnLocation` instances.

Implementation: Removed the rejected v3 shell from the active map without
deleting it by moving it to
`ServerStorage.MapArchives.RejectedCliffGrassV3_2026_11_21`. Left the rejected
v2 panels archived. Disabled every active spawn and then enabled only
`Workspace.PinkHouseMap.HouseTestSpawn` at `(145, 1185.75, 185)`.

Verification: A fresh Play session reported no active `CliffGrassShellV3` and
placed the HumanoidRootPart at `(146.68, 1189.25, 189.41)`, 5.87 studs from the
house test spawn. A gameplay capture confirmed the character beside the pink
house with no giant overhead mesh.

Performance: Not measured; this rollback removes 165,600 source triangles from
the active scene.

Limitations: The cliff walls currently have no approved true-3D vegetation
shell. The retained backing/collision cliff art is not a 1:1 visual match.

Next: Produce and render a small isolated Blender wall-grass proof from the
fixed reference camera. Do not alter the live map until that proof passes visual
review.

### 2026-11-21 — Stable upper spawn beside house

Scope: `Workspace.PinkHouseMap.HouseTestSpawn` and new
`Workspace.PinkHouseMap.HouseSpawnSafetyPlatform`.

Implementation: Kept only `HouseTestSpawn` enabled, placed it at
`(145, 1185.5, 185)`, and added an invisible anchored 40 x 2 x 40 stud collision
platform beneath it at `(145, 1184, 185)` so streaming cannot drop a newly
spawned character through the upper meadow.

Verification: A fresh four-second Play test placed the HumanoidRootPart at
`(140.75, 1189.00, 182.66)` and confirmed `Y > 1100`; the character remained on
the upper plateau beside the house instead of falling to the lower meadow.

Performance: Not measured; one static invisible Part was added.

Limitations: The safety platform is intentionally invisible and only protects
the immediate spawn area.

Next: Keep the spawn unchanged while the next visual prototype is developed
outside the live map.

### 2026-11-21 — Remove unrelated contributor content

Scope: Workspace clutter outside `Workspace.PinkHouseMap`.

Implementation: Moved the separate `Workspace.AscentGame` obby (StartZone,
Routes, Checkpoints, Coins, Summit, and scenery), `ServerScriptService.AscentServer`,
`StarterPlayer.StarterPlayerScripts.AscentHUD`, `ReplicatedStorage.AscentRemotes`,
and the default `Workspace.Baseplate`/disabled `Workspace.SpawnLocation` into
`ServerStorage.MapArchives.ArchivedOtherContributor_AscentGame_2026_11_21`.

Verification: Edit-mode Workspace now contains only `Terrain`, `PinkHouseMap`,
and the Studio camera; the unrelated obby and default baseplate are no longer
active. The place was saved to Roblox as version 47.

Performance: Not measured; removed 421 obby descendants and the 2048-stud
default baseplate from active Workspace.

Limitations: Archived content remains recoverable in ServerStorage and is not
published as active gameplay.

Next: Continue only with the Pink House vertical slice.

### 2026-11-21 — Short fissure and inclined ladder composition pass

Scope: `Workspace.PinkHouseMap` house/garden placement, upper fissure,
`Geometry.ChasmEndWall`, ladder, Terrain grass closure, and house spawn.

Implementation: Archived the previous house pose, 1,052-stud ladder, and end
wall under `ServerStorage.MapArchives.BeforeShortChasmComposition_2026_11_21`.
Moved the house pivot from Z `100` to `-170`, moved the fissure end from Z `49`
to `-275`, added `ChasmClosureCore_v1` plus a Terrain Grass surface over the
closed rear section, and replaced the old ladder with `InclinedLadder_v1`: two
wood rails, 25 rungs, and one invisible climb surface between `(16.97, 1055,
-360)` and `(16.97, 1185, -275)`. Moved `HouseTestSpawn` and its invisible
40 x 2 x 40 safety platform beside the relocated house.

Verification: Edit-mode aerial/front/close captures confirmed the house beside
the shortened fissure and the ladder visibly inclined inside it. A fresh
four-second Play test kept the HumanoidRootPart on the upper plateau at
`(149.10, 1189.00, -84.39)` instead of dropping to the lower meadow.

Performance: Not measured; active ladder geometry dropped from 165 descendants
over 1,052 studs to 28 parts over 155 studs.

Limitations: The new ladder is a composition-quality Roblox build rather than a
final Blender hero asset. Cliff-wall vegetation remains deliberately unchanged
for a separate approved prototype.

Next: Manually test the ladder climb with a normal R15 character, then address
only the cliff-wall vegetation after approving a small Blender proof.

### 2026-11-21 — Level meadow seam over closed fissure

Scope: Terrain Grass strip above `Geometry.ChasmClosureCore_v1`.

Implementation: Removed the raised Terrain voxels over the newly closed rear
fissure section and rebuilt the 26 x 328 stud Grass strip at a lower voxel
height matching the surrounding meadow. House, ladder, fissure end, and wall
vegetation were not moved.

Verification: Before correction the closure strip raycast at X `17`, Z `-230`
hit Terrain at Y `1189.5` while adjacent meadow hit Y `1185.25`. After rebuilding,
the same strip hits Y `1185.0`; a fresh Play test kept the player beside the
house at Y `1189.0` and an overhead capture confirmed the raised ridge is gone.

Performance: Not measured; no new instances were added.

Limitations: Natural directional shadows from the house and garden remain
visible across the grass and can still read as darker grass from a vertical
camera.

Next: Keep the meadow level fixed and evaluate composition from the supplied
reference camera rather than an editor-only vertical view.

### 2026-11-21 — Lower ladder to reference-like slope

Scope: `Workspace.PinkHouseMap.InclinedLadder_v1` only.

Implementation: Archived the 57-degree ladder under
`ServerStorage.MapArchives.BeforeLadderSlope30_2026_11_21` and replaced it with
`InclinedLadder_v2`. The new ladder runs from `(16.97, 1105, -420)` to
`(16.97, 1185, -275)`, with two wood rails, 27 rungs, and one invisible aligned
TrussPart climb surface.

Verification: Calculated length is 165.60 studs and slope is 28.89 degrees above
horizontal. A close side capture confirmed the ladder now lies along the chasm
instead of reading as nearly vertical.

Performance: Not measured; active ladder contains 30 parts.

Limitations: This remains a composition-quality Roblox ladder rather than a
final Blender hero asset.

Next: Keep the approved slope fixed and manually test full R15 traversal before
any art replacement.

### 2026-11-21 — Half-height cliff composition

Scope: `Workspace.PinkHouseMap` cliff cores, upper Terrain meadow, cottage,
`InclinedLadder_v2`, house spawn, and lower chasm floor.

Implementation: Preserved the complete pre-change map at
`ServerStorage.MapArchives.BeforeHalfHeightCliff_2026_11_21.PinkHouseMap_PreHalfHeight`.
Reduced `LeftCliffCore`, `RightCliffCore`, `RearPlateauCore`, `ChasmEndWall`, and
`ChasmClosureCore_v1` from 1,000 to 500 studs tall, keeping their new tops at
Y `493.239`. Lowered the upper Terrain, cottage, ladder, spawn, and safety
platform by 682 studs while retaining the lower meadow near Y `2`; moved the
chasm floor to Y `5`.

Verification: Edit raycasts measured upper Terrain at Y `503.016` and lower
Terrain at Y `2`, a 501.016-stud vertical separation. The cottage bounding-box
bottom is Y `499.232`, embedded below the meadow surface rather than floating.
An aerial capture confirmed the reduced silhouette. A fresh three-second Play
test placed the HumanoidRootPart at `(144.69, 507.00, -84.95)` beside the house
with full health. The place was saved to Roblox as version 51.

Performance: Not measured; no new active rendering geometry was added, and the
five active cliff cores contain half their previous vertical area. One complete
recovery clone remains in ServerStorage and does not render during gameplay.

Limitations: Wall materials and vegetation remain a separate unresolved art
pass. The current cliff silhouette is still core-based and deliberately keeps
the approved upper meadow, house, fissure, and ladder layout unchanged.

Next: Keep this approximately 501-stud height fixed while developing one small
approved wall-surface proof before any further live-map vegetation replacement.

### 2026-11-22 — Remove obsolete overhead Terrain slab

Scope: `Workspace.Terrain` above the Pink House playable meadow.

Implementation: Copied the obsolete Grass voxel layer into
`ServerStorage.MapArchives.BeforeOverheadTerrainCleanup_2026_11_22.OldOverheadGrassTerrain_Y992_1024`
for recovery, then cleared Terrain only across X `-740..760`, Y `968..1048`,
and Z `-600..2200`. The cottage, cliff cores, ladder, current upper meadow, and
lower meadow were not modified.

Verification: Before cleanup, upward raycasts hit the detached Grass slab from
Y `1003.984` to `1012.016`. After cleanup, a 35-point overhead ray grid found
zero Terrain hits. The current upper surface still raycasts at Y `503.016` and
the lower meadow at Y `2`. A fresh three-second Play test spawned the
HumanoidRootPart at `(143.05, 507.00, -82.46)` and found no overhead hit within
900 studs; gameplay and sky captures confirmed the slab is gone. Saved to
Roblox as version 58.

Performance: Not measured; one large detached rendered Terrain layer was
removed. The recovery TerrainRegion remains in ServerStorage and does not
render during gameplay.

Limitations: This fixes only the accidental overhead voxel layer. Cliff-wall
art, grass scale, clouds, and reference matching remain separate work.

Next: Preserve the current clean vertical stack and continue only with an
approved small wall-surface prototype.

### 2026-11-22 — Full-height steeper ladder to lower meadow

Scope: `Workspace.PinkHouseMap.InclinedLadder_v2`, its replacement
`InclinedLadder_v3`, and the ladder recovery archive only.

Implementation: Archived the former 165.60-stud, 28.89-degree ladder under
`ServerStorage.MapArchives.BeforeFullHeightLadder_2026_11_22`. Built
`InclinedLadder_v3` from `(16.9704, 3.2, -589)` on the lower meadow to
`(16.9704, 503, -275)` on the upper meadow: 590.25 studs long at 57.86 degrees,
with two rails and 97 rungs. Replaced the single clamped climb surface with
three overlapping, invisible, 16.5-stud-wide TrussParts covering the complete
route.

Verification: Edit raycast measured the lower Terrain at Y `2`. A Play test
started the R15 HumanoidRootPart at Y `5`; holding forward entered `Climbing`,
crossed both TrussPart overlaps at measured Y `193.21` and `365.75`, and exited
onto upper Terrain at `(17.03, 506.01, -220.56)` in `Running` state. Captures
`FullHeightLadder_BasePlay` and `FullHeightSteepLadder_FinalPlaytest` verified
the lower contact and upper exit. Saved to Roblox as version 60.

Performance: Not measured; the active prototype contains 102 BaseParts.

Limitations: The ladder is still a repeated-Part composition prototype rather
than an optimized authored mesh, and the visible landings need a final
reference-matching art pass.

Next: Keep the verified route functional while polishing the visible landings,
then consolidate the repeated geometry after composition approval.

### 2026-11-22 — Reference-like tapered fissure

Scope: `Workspace.PinkHouseMap.Geometry` cliff cores, chasm closure/end/floor,
upper fissure Terrain, and new `TaperedFissure_v1` wall geometry.

Implementation: Preserved the five modified geometry Parts plus the affected
Terrain region under
`ServerStorage.MapArchives.BeforeTaperedFissure_2026_11_22`. Narrowed the left
and right cliff cores while retaining their outer bounds, widened the closure,
end wall, and lower floor to 80 studs, and added two 500-stud-high WedgeParts.
The opening now tapers symmetrically from 80 studs at Z `-567` to 24 studs at
Z `-279`; only the corresponding plan-view wedge was cleared from upper
Terrain. `InclinedLadder_v3` was not moved or rebuilt.

Verification: Horizontal Edit raycasts measured opening widths of `78.64`,
`66.97`, `51.42`, `35.86`, and `25.17` studs while approaching the house.
Vertical Terrain-only raycasts at the same samples hit the lower meadow at Y
`2` through the opening and upper meadow at Y `503.02` immediately outside it.
A Play test entered `Climbing` from the lower meadow at Y `5`, and a second
upper-section test exited onto upper Grass at `(16.93, 506.01, -220.56)`.
Captured `TaperedFissure_TopDown` and saved to Roblox as version 61.

Performance: Not measured; two active WedgeParts were added and no runtime
scripts or update loops were introduced.

Limitations: The taper is a collision-stable Part/WedgePart composition pass;
its cliff-edge materials and vegetation still need final authored art.

Next: Keep the approved taper and verified climb fixed while replacing only the
visible core surfaces with the approved grass/cliff art treatment.

### 2026-11-22 — Compact fissure and steeper ladder

Scope: `Workspace.PinkHouseMap.Geometry` front cliff cores, upper front-edge
Terrain, `TaperedFissure_v2`, `InclinedLadder_v4`, and their recovery archive.

Implementation: Archived the prior geometry, ladder, and affected Terrain under
`ServerStorage.MapArchives.BeforeCompactFissure_2026_11_22`. Moved the complete
front cliff edge from Z `-567` to `-487` while retaining its outer X and rear Z
bounds, reducing core depth from 620 to 540 studs. Rebuilt the opening as a
208-stud taper from 55 studs at the exposed front to 22 studs at Z `-279` and
removed only the obsolete upper Terrain strip in front. Replaced the ladder
with `InclinedLadder_v4`, running from `(16.9704, 3.2, -509)` to
`(16.9704, 503, -275)` over 551.87 studs at 64.91 degrees, with two rails, 91
rungs, and three overlapping invisible climb surfaces.

Verification: Horizontal Edit raycasts measured opening widths of `53.89`,
`47.54`, `38.02`, `28.50`, and `22.95` studs while approaching the house.
Terrain-only rays hit the lower meadow at Y `2` through every sample and the
surrounding upper Grass at Y `503.016`. The former front extension at Z `-530`
and `-500` now raycasts directly to the lower meadow. In Play, the R15 character
entered `Climbing` at the base and reached `(16.97, 48.92, -491.53)` after five
seconds; the upper-section test exited onto Grass at
`(16.94, 506.01, -263.29)` in `Running` state with full health. Captured
`CompactFissure_TopOblique` and `CompactFissure_Overview`; saved to Roblox as
version 63.

Performance: Not measured; the active ladder decreased from 102 to 96
BaseParts, the taper still uses two WedgeParts, and no runtime scripts or update
loops were added.

Limitations: The composition and traversal are stable, but the cliff edges are
still Part/WedgePart cores and need final authored grass, soil, erosion, and
landing art.

Next: Preserve the approved 55-to-22-stud taper and verified ladder route while
polishing only the visible surfaces and landings.

### 2026-11-22 — Isolated true-3D wall-grass proof

Scope: Local Blender wall-grass proof assets only; no Roblox Studio map,
scripts, live cliff geometry, or cloud settings changed.

Implementation: Added `blender/build_wall_grass_proof_v1.py` and
`blender/pink_house_wall_grass_proof_v1_spec.md`. Built an 80 x 80 stud module
as four 52 x 52 jittered blade grids plus one short upper-lip strip. Each blade
is a curved six-triangle ribbon rooted in the vertical wall and projecting
outward before bending slightly downward. Saved the editable source at
`blender/pink_house_wall_grass_proof_v1.blend` and exported five selected meshes
to `exports/pink_house_wall_grass_proof_v1.glb`.

Verification: Blender mesh audits found zero non-finite vertices, zero
zero-length edges, and zero zero-area faces. A clean-scene GLB reimport found
five meshes, 68,196 total triangles, 16,224 maximum triangles per mesh, and
approximately 81.00 x 5.59 x 81.36 stud bounds. Front, oblique, side, and
upper-lip renders confirmed dense coverage, visible outward depth, and a short
top transition. GLB SHA-256 is
`1272104348495e3eb5513a72001e666731e82785fd2a9b4fc5265dee0311d42f`.

Performance: Not measured in Roblox; the local proof is 4,159,260 bytes and
68,196 triangles before any LOD or distance substitution.

Limitations: Geometry and a single rough green material are proof quality only.
The module has not been uploaded, imported, tiled across the cliff, profiled on
desktop/mobile, or approved as final art. Distant LOD/backing and final PBR
variation remain intentionally deferred.

Next: Obtain visual approval for the four proof renders, then test one imported
module in an isolated Studio area before changing the active cliff.
