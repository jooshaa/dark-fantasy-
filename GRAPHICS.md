# Graphics and Environment Context

Last updated: 2026-11-20

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

- An eight-piece Blender-authored irregular front-cliff facade imported as a
  permanent Roblox Model asset, aligned around the central chasm and layered in
  front of the retained collision cores.
- A roughly 1,000-stud-tall plateau composed so that the narrow fissure ends
  near the house instead of cutting through the entire world.
- Separate left/right front cliff cores and a continuous rear plateau.
- Generated PBR MaterialVariants for overgrown rock and meadow grass.
- Hundreds of varied hanging-growth strips on the front, sides, and chasm walls.
- A long functional ladder and small top landing.
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
- Two non-spherical vapor cloud layers now supplement Terrain Clouds: 24 upper
  mist banks around Y=1050-1080 and 38 broad lower banks around Y=520-650.
  Together they distribute 62 irregular vapor anchors across the horizon.
- `HouseTestSpawn` is active on the safe side of the cottage at approximately
  `(145, 1015, 185)`; both the older map spawn and the default Workspace spawn
  are disabled.
- The complete upper meadow now has a thin real Terrain Grass layer across the
  left, right, and rear plateau sections while preserving the open fissure.
- Nine tiled hanging-grass texture faces cover the front, outer sides, rear, and
  inner fissure walls over a continuous dark-green collision core.
- A first modular 3D hanging-grass layer now breaks the flat wall treatment:
  374 non-colliding MeshPart instances use eight reusable Blender-authored edge
  and long-drop variants across the upper lips, outer walls, and fissure walls.
- The camera-critical front face and both inner fissure walls additionally use
  130 dense 3D wall-grass panels. Each panel contains 650 crossed grass blades
  projecting outward over the tiled texture, so close oblique views show real
  depth while the texture fills distant gaps.
- A second-generation local Blender cliff-shell candidate now covers the front,
  both outer sides, and both inner chasm walls. It is validated and exported,
  but has not been uploaded or inserted into Roblox pending visual review.
- The active Studio composition has been corrected to one continuous upper
  meadow with one narrow fissure ending before the house. The false horizontal
  canyon and perforated front facade are archived rather than deleted.
- The cottage is scaled to approximately 167 x 105 x 227 studs and surrounded
  by a denser 123-instance garden pass of shrubs, flowers, and stones.
- The replacement ladder is approximately 24.5 studs wide and 1,052 studs long,
  slopes into the fissure, and uses 12 overlapping invisible TrussPart sections
  for continuous climbing coverage.

This is the first production pass, not final 1:1 art. Composition and playable
scale are established; authored cliff meshes, foliage cards, final house meshes,
audio, and reference-matched cinematography remain.

## Known Limitations

- The front face now has an authored irregular mesh shell, but the side and rear
  silhouettes still expose large Part-based cores. Hanging-growth strips improve
  the read; authored side modules and foliage cards are still needed.
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
- The v1 geometric grass is intentionally a restrained silhouette/detail layer
  over the tiled wall texture, not a full blade-for-blade wall simulation. It
  still needs runtime draw-call profiling and a second organic-shape pass;
  close views can reveal repeated ribbon clusters.
- Dense wall-grass coverage currently targets the front face and inner fissure.
  Outer side and rear walls still rely mainly on the tiled texture and lip
  fringe until the 507k-triangle hero-wall pass is profiled.
- The new cottage matches the low single-storey cross-gabled read much more
  closely. Its materials are currently Roblox material/color assignments rather
  than final baked PBR texture sets, and the roof intersections need one more
  polish pass.
- The house/garden group now sits immediately beside the fissure entrance. Its
  center is approximately `(45, 168)` in XZ and the door-to-ladder-top horizontal
  distance is about 37 studs, reduced from the original roughly 87 studs.

## Next Priorities

1. Replace the smooth continuous wall with a non-perforating authored grass and
   soil shell; keep exactly one readable fissure and the existing collision cores.
2. Profile and consolidate the new 3D grass modules, then add more organic
   silhouette variants only where fixed reference cameras expose repetition.
3. Add unique PBR breakup and tune grass/cliff response against fixed matched
   video cameras.
4. Polish the Blender cottage roof intersections and create final plaster, tile,
   glass, stone, and garden PBR treatment.
4. Refine the inclined ladder entrance and verify a complete manual climb with
   a normal R15 character.
5. Replace the ladder with an optimized authored model.
6. Add roots, erosion, decals, soft low clouds, a distant meadow horizon, and
   moving cloud-shadow treatment.
7. Add layered wind, house, chasm, and ladder ambience.
8. Validate representative desktop and mobile camera paths, not only the current
   spawn view.
9. Finish this vertical slice before producing additional maps.

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
  `ServerStorage.ImportedAssetSources.DenseWallGrassPanelsV1`; 130 active
  non-colliding clones are under `Workspace.PinkHouseMap.DenseWallGrass3D_v1`.
- The cliff GLB was uploaded once as permanent Model asset `124672594627247`
  and inserted as the package copy `Workspace.PinkHouseMap.AuthoredFrontCliff`.
  The imported 280-stud height was corrected by a 3.571429 scale factor to the
  intended 1,000 studs. The eight modules were separated around a roughly
  25-stud central opening, anchored, made non-collidable, and assigned the
  existing `pinkhouse_overgrown_cliff` MaterialVariant. Existing cliff cores
  remain responsible for collision.

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
