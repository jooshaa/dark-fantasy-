---
name: roblox-blender-asset
description: Build, revise, inspect, validate, render, and export Blender meshes for the Pink House dark-fantasy Roblox project. Use for Blender modeling, MeshPart or GLB/FBX preparation, cliff/house/prop creation, PBR and UV work, LOD decisions, Roblox scale conversion, triangle audits, reference matching, and Blender-to-Roblox import preparation.
---

# Roblox Blender Asset

Create production assets through a measured, reversible Blender workflow. Treat
the supplied video and fixed comparison views as the visual authority.

## Required context

1. Read the repository `GRAPHICS.md` completely before editing visuals.
2. Read [references/production-spec.md](references/production-spec.md).
3. Inspect the live Blender scene before changing it.
4. Preserve unrelated objects and user work.

## Workflow

1. Write a short asset specification: purpose, visible views, target dimensions,
   named parts, collision owner, material plan, and expected export path.
2. Create a full-scene checkpoint before material changes.
3. Work non-destructively. Save new major versions beside the source instead of
   overwriting an approved asset.
4. Build reusable modules. Use authored geometry for hero silhouettes and keep
   primitives only for collision, hidden blockers, or greybox.
5. Capture front, rear, and both three-quarter views. Compare proportion,
   silhouette, depth, seams, repetition, and readability against the reference.
6. Iterate when the result reads as flat, procedural, noisy, tiled, detached, or
   toy-like. Do not call the first successful script final.
7. Validate every exported mesh for non-finite vertices, zero-area faces,
   zero-length edges, dimensions, transforms, materials, and triangle count.
   Explain intentional open boundaries.
8. Apply or export modifiers, preserve meaningful unique names, embed supported
   textures, and export GLB unless another format is required.
9. Verify the exported file exists and record size plus checksum. Do not upload a
   permanent Roblox asset without explicit consent for that upload.
10. After importing, verify mesh count, orientation, scale, anchoring, material,
    collision, placement, and visuals in Studio. Profile before optimization
    claims.
11. Update `GRAPHICS.md`: Current State, Implementation Notes, Audit Log, and
    Next Priorities.

## Blender MCP rules

- Start with scene inspection and a checkpoint.
- Use stable operation IDs and wait for long jobs instead of duplicate calls.
- Prefer typed tools for inspection, capture, and validation. Use Blender Python
  for custom deterministic geometry.
- Save a checkpoint before each major iteration and retain the last visually
  acceptable version.
- Never restore a checkpoint unless the current scene is genuinely worse or
  broken.

## Completion gate

Finish only when the asset has a saved editable `.blend`, a validated export,
multi-view captures, measured geometry, documented limitations, and a clear
Roblox integration plan. A technically successful export is not sufficient if
the visual comparison still fails.
