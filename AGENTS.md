# Project Agent Instructions

## Required context & mandatory logging (all contributors and agents)

Before making **any** change to the project (map, lighting, environment art,
material, texture, mesh, script, gameplay, camera, VFX, audio ambience, or
graphics/performance setting), read `GRAPHICS.md` completely and pull the latest
Git history.

**Universal handoff rule:** Regardless of who is working on the repository,
their agent MUST always record what was done and how before finishing the task.
Update `GRAPHICS.md` in the same task and keep these sections current:

- `Current State`
- `Implementation Notes`
- `Audit Log`
- `Next Priorities`

Every `Audit Log` entry must clearly state:
- **Scope:** what map, scripts, assets, or settings changed
- **Implementation:** how it was built or modified (including exact file paths,
  asset IDs, object names, or parameters)
- **Verification:** what capture, playtest, validation, or profiling was run and
  the result
- **Performance:** measured numbers or `"Not measured"`
- **Limitations:** remaining issues or caveats
- **Next:** immediate follow-up

Keep entries short, factual, and self-contained so any other collaborator or AI
agent can pick up the work without reconstructing context from chat history.
Commit and push changes with clear, descriptive commit messages.

## Visual workflow

1. Preserve the intended cinematic realistic dark-fantasy direction.
2. Treat primitive geometry as greybox unless explicitly approved as final art.
3. Build and validate one polished vertical slice before expanding to more maps.
4. Prefer reusable PBR materials, modular assets, streaming, and measured
   performance over uncontrolled visual complexity.
5. Do not delete or replace user work outside the named task scope.
6. Capture or inspect the result after material visual changes.
7. Profile before making performance claims.

## Roblox Studio & Rojo

- Luau game code lives in Git under `src/server/` (`ServerScriptService`),
  `src/client/` (`StarterPlayer.StarterPlayerScripts`), and `src/shared/`
  (`ReplicatedStorage.Shared`), synced via `default.project.json` (`Rojo 7.7.1`,
  managed by `rokit.toml`). Keep `"$ignoreUnknownInstances": true` on mapped
  services so Rojo never removes Studio-authored map/archive objects.
- Keep Luau edits in `src/` committed to Git so all collaborators can run the
  same code via `rojo serve`.
- The active map and environment are edited through Roblox Studio (and
  `Roblox_Studio` MCP).
- Confirm the intended Studio instance before modifying a place.
- As of 2026-11-20, the active cloud-persisted place is
  `dark fantasy` (`placeId: 96826195026003`, `universeId: 10777885251`). Always
  re-check via `list_roblox_studios`; do not assume it remains unchanged.
- `LightingStyle = Realistic` may require a manual Studio Properties change if
  MCP lacks the necessary capability.

