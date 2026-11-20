# dark-fantasy-

Cinematic realistic dark-fantasy horror experience in Roblox (`dark fantasy`, `placeId: 96826195026003`, `universeId: 10777885251`).

## Repository Structure

- `default.project.json` & `rokit.toml` — Rojo project configuration (`Rojo 7.7.1`) for syncing Luau code into Roblox Studio without overwriting the Studio-authored map.
- `src/server/` → `ServerScriptService` (server scripts, e.g. `WallGrassLODController.server.luau`)
- `src/client/` → `StarterPlayer.StarterPlayerScripts` (client scripts)
- `src/shared/` → `ReplicatedStorage.Shared` (shared modules, configs, remotes)
- `blender/`, `exports/`, `textures/`, `references/` — Blender 3D assets, GLB exports, textures, and visual references.
- `AGENTS.md` — mandatory workflow, collaboration, and logging rules for all contributors and AI agents.
- `GRAPHICS.md` — live source of truth for visual direction, current state, implementation notes, audit log, and next priorities.

## Quick Start for Collaborators

1. Clone the repository and pull the latest `main`:
   ```bash
   git clone https://github.com/jooshaa/dark-fantasy-.git
   cd dark-fantasy-
   ```
2. Install [Rokit](https://github.com/rojo-rbx/rokit) (or Rojo directly) and run:
   ```bash
   rokit install
   rojo serve
   ```
3. Open the `dark fantasy` place in **Roblox Studio** (ask the project owner for **Team Create** collaborator access to `placeId: 96826195026003` so you have the live `PinkHouseMap`, Terrain, and Lighting).
4. In Roblox Studio, open the **Rojo** plugin and click **Connect** (`localhost:34872`).
   - `default.project.json` uses `"$ignoreUnknownInstances": true` on services, so syncing code will **not** delete map models, Terrain, Lighting, or archives in Studio.

## Mandatory Collaboration Rule

Whoever works on this project, **their AI agent MUST always record what was changed, how it was implemented, what was verified, and any known limitations** in `GRAPHICS.md` (and commit/push with a clear message) before finishing the task. See `AGENTS.md` for full details.
