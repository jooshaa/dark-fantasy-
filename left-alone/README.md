# Left Alone! (1 vs 9 House Traps) — Luau Source (Rojo)

Отдельный Rojo-проект для игры **Left Alone!** внутри общего репозитория (не затрагивает `Pink House` в корневом `src/`).

## Структура кода
- `src/shared/GameConfig.luau` → `ReplicatedStorage.Shared.GameConfig` (единый конфиг фаз, ловушек, баланса)
- `src/server/Core/RoundManager.server.luau` → `ServerScriptService.Core.RoundManager` (Lead Dev)
- `src/server/Gameplay/` → `ServerScriptService.Gameplay` (Бекзод: `RagdollController`, `TrapService`, `GadgetService`, `ZiplineService`)
- `src/client/HUDController.client.luau` → `StarterPlayer.StarterPlayerScripts.HUDController`

## Как синхронизировать с Roblox Studio (Rojo)
```bash
rojo serve left-alone/default.project.json
```
В Roblox Studio открой плагин **Rojo** и нажми **Connect**. Все сервисы настроены с `"$ignoreUnknownInstances": true`, поэтому карта (`Workspace.Map`), звуки и UI в Studio **не удаляются** при синке.

## Документация команды
- Поэтапный план PDF (3 Dev + 1 Маркетолог): `../output/pdf/Left_Alone_Traps_Roadmap_RU.pdf`
- Полный разбор идеи (87/100): `../research/ideas/12_left_alone_traps.md`
- Стандарты кода, Ragdoll и оптимизации: `../research/ideas/12_left_alone_dev_guide.md`
- AI-скилл для агентов: `../.agents/skills/left-alone-dev-standards/SKILL.md`
