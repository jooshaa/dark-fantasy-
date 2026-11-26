-- ServerScriptService/Gameplay/README_FOR_BEKZOD
-- Привет, Бекзод! Все геймплейные скрипты (RagdollController, TrapService, Gadgets, Zipline) клади сюда в Gameplay/.
--
-- Готовые хуки от Lead Dev (Этап 1):
-- 1) Роль игрока: player:GetAttribute("Role") -> "Lobby" | "Defender" | "Thief"
-- 2) Текущая фаза раунда: workspace:GetAttribute("RoundPhase") -> "Lobby" | "Prep" | "Invasion" | "End"
-- 3) Бюджет ловушек Защитника: player:GetAttribute("TrapBudget")
-- 4) Слоты ловушек лежат в Workspace.Map.TrapSlots (у каждого Part есть атрибуты SlotType и Occupied)
-- 5) RemoteEvent для 1-tap установки ловушки уже создан: ReplicatedStorage.Remotes.PlaceTrap
-- 6) Конфиг ловушек: require(ReplicatedStorage.Shared.GameConfig).Traps

return {}
