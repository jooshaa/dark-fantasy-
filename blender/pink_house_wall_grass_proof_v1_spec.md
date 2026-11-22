# Pink House wall-grass proof v1

## Purpose

Validate a dense true-3D vertical grass treatment against the supplied Pink
House video before any live Roblox cliff is changed.

## Visual target

- Short grass rooted directly into a vertical cliff face.
- Blades initially grow outward from the wall, then bend slightly downward.
- Dense hedge-like coverage with irregular clumps and no visible square grid.
- A soft overhanging transition at the upper cliff lip.
- Readable depth from front, side, and three-quarter gameplay views.

## Dimensions and scale

- Module envelope: 80 x 80 Roblox studs.
- Blender source envelope: 22.4 x 22.4 metres.
- Conversion: 1 Roblox stud = 0.28 metres.

## Named parts

- `WallGrass_Q1` through `WallGrass_Q4`: four reusable quadrants forming one
  80 x 80 stud module.
- `WallGrass_Lip`: optional upper-edge transition strip.
- `PREVIEW_*`: backing wall, top meadow, cameras, and lights; excluded from GLB.

## Collision and materials

- Existing Roblox cliff cores remain the sole collision owner.
- Grass meshes are decorative, anchored, non-colliding, non-queryable, and
  double-sided after import.
- One rough non-metal grass material is used for the geometry proof. Final PBR
  colour/normal/roughness work is deferred until the silhouette is approved.

## Outputs

- Editable source: `blender/pink_house_wall_grass_proof_v1.blend`
- Empty-scene checkpoint:
  `blender/checkpoints/pink_house_wall_grass_proof_v1_empty.blend`
- Roblox-ready proof export: `exports/pink_house_wall_grass_proof_v1.glb`
- Comparison renders:
  `exports/pink_house_wall_grass_proof_v1_front.png`,
  `exports/pink_house_wall_grass_proof_v1_oblique.png`,
  `exports/pink_house_wall_grass_proof_v1_side.png`, and
  `exports/pink_house_wall_grass_proof_v1_lip.png`.

## Acceptance gate

Do not cover or modify the live Roblox cliff until the proof has been reviewed
for density, projection, blade scale, top-lip transition, seams, repetition,
triangle count, and fixed-camera similarity to the supplied video.
