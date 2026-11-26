---
name: left-alone-dev-standards
description: Engineering standards, anti-exploit rules, ragdoll physics guidelines, 1-tap mobile UX, optimization limits, and Roblox MCP skill routing for the Left Alone! (1 vs 9 House Traps) Roblox project. Read before writing any Luau code, UI, traps, or map props for Left Alone!.
---

# Left Alone! (1 vs 9 House Traps) — Engineering & Quality Skill

Use this skill whenever building, reviewing, or debugging any script, trap, gadget, UI, or map asset for **Left Alone!**.

## 1. Architecture & Team Boundaries (3 Devs)

- **Single Source of Truth:** All phase durations, trap stats, costs, cooldowns, rewards, and player-count scaling MUST live in `ReplicatedStorage.Shared.GameConfig`. Never hardcode trap prices or timers inside individual scripts.
- **Folder Ownership:**
  - `ServerScriptService/Core/` — Lead Dev (`RoundManager`, `DataService`, `ShopService`, `MonetizationService`).
  - `ServerScriptService/Gameplay/` — Gameplay Dev / Bekzod (`RagdollController`, `TrapService`, `GadgetService`, `ZiplineService`).
  - `Workspace/Map/` & `StarterGui/` — Junior Dev / Saidabbos (map props, `TrapSlots` markers, UI layouts, SFX).
- **No Per-Instance Script Spam:** Never duplicate a `Script` inside every trap, door, or coin. Use ONE central server module (`TrapService`) with `CollectionService` tags or folder listeners (`Workspace.Map.TrapSlots`).

## 2. Modern Luau & Zero-Leak Standards

- Always use `task.wait()`, `task.spawn()`, `task.delay()`. NEVER use deprecated `wait()`, `spawn()`, or `delay()`.
- Always use `AssemblyLinearVelocity` or `BasePart:ApplyImpulse()` for physics knockback. NEVER use deprecated `BodyVelocity`, `BodyPosition`, or `BodyGyro`.
- Every round-scoped connection (`Touched`, `Died`, `Heartbeat`) MUST be stored in a cleanup table (or `Trove`/`Janitor`) and disconnected at the end of every round (`End` → `Lobby`) so memory never leaks across 20+ rounds.
- Always guard `Touched` events with per-player cooldowns/debounces (`os.clock()`).

## 3. Client–Server Security (Anti-Exploit)

- **Never trust the client** for coins, trap costs, damage, ragdoll triggers, or win conditions.
- When handling `ReplicatedStorage.Remotes.PlaceTrap:OnServerEvent(player, slotPart, trapId)`, the server MUST validate ALL of:
  1. `player:GetAttribute("Role") == "Defender"`
  2. `workspace:GetAttribute("RoundPhase")` is `"Prep"` or `"Invasion"`
  3. `typeof(slotPart) == "Instance" and slotPart:IsA("BasePart") and slotPart:IsDescendantOf(workspace.Map.TrapSlots)`
  4. `slotPart:GetAttribute("Occupied") == false`
  5. `GameConfig.Traps[trapId]` exists and `trapConfig.SlotType == slotPart:GetAttribute("SlotType")`
  6. `(player:GetAttribute("TrapBudget") or 0) >= trapConfig.Cost`
  7. Rate limit (at least `0.25s` between placement requests per player).

## 4. Ragdoll & Comedy "Juice" Standards

- **Stable Ragdoll (No Floor Clipping / No Stuck Players):**
  - Replace `Motor6D` joints with `BallSocketConstraint` (`LimitsEnabled = true`, `TwistLimitsEnabled = true`) rather than deleting joints permanently.
  - Set `Humanoid.PlatformStand = true` and disable `Enum.HumanoidStateType.GettingUp` during ragdoll.
  - Enforce a hard max duration (`2.0–3.5s`), then restore `Motor6D`, re-enable `GettingUp`, and safely lift `HumanoidRootPart` by `+1.5 studs` if needed.
- **3-Part Comedy Feedback on Every Trap Hit:**
  1. **Audio:** Cartoon SFX (bonk, slip, splash, boing, sizzle).
  2. **Visual:** Short burst `ParticleEmitter:Emit(15)` (paint splatter, ice shards, stars, hat flame) — never infinite high-rate emitters.
  3. **Reward:** Instant `+Coins` feedback to Defender and clear visual state on Thief.

## 5. Mobile-First UI & Performance Budget (Target: 45–60 FPS on Budget Phones)

- **1-Tap Placement:** Trap placement MUST work with a single tap on highlighted `TrapSlots` (no mandatory keyboard-only hotkeys). All action buttons must be at least `56×56 px` for thumbs.
- **Responsive UI:** Use `Scale` (`UDim2.fromScale`) + `UIAspectRatioConstraint` / `UISizeConstraint` so nothing clips on small phones.
- **Map Optimization:**
  - Set `CastShadow = false` on all small props, Christmas lights, snow decor, and particles.
  - Set `CanCollide = false` and `CanQuery = false` on purely decorative props (ornaments, garlands, rugs).
  - **Toolbox Safety Rule:** Inspect EVERY Creator Store / Toolbox model and delete any unexpected `Script` / `LocalScript` before inserting into `Workspace.Map`.

## 6. Mandatory Roblox Studio MCP Skills to Use Before Launch

When connected to Roblox Studio MCP, invoke these built-in Roblox skills at the right stage:
- **`rbx-docs-search`**: Verify current Engine APIs (Constraints, `ApplyImpulse`, `AnalyticsService`, `DataStoreService`) instead of guessing.
- **`rbx-device-simulator-lua`**: Test HUD, Van Voting UI, and Trap Shop on phone & tablet resolutions (Stage 3–4).
- **`rbx-perf-profiling`**: Run MicroProfiler during a multi-player trap/ragdoll test to catch frame spikes (Stage 4).
- **`rbx-scene-analysis`**: Audit instance counts, memory, and leaks in `Workspace.Map` (Stage 4).
- **`rbx-network-simulator`**: Test 3G/4G latency & packet loss so ragdoll and trap hits don't desync (Stage 4).
- **`rbx-instrument-analytics`**: Wire up `AnalyticsService` funnels (`bounce <60s`, first trap placed, rounds per session) before release.
- **`rbx-debug` / `rbx-unit-test`**: Debug runtime issues and unit-test `GameConfig` scaling and economy logic.
