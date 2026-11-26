-- ReplicatedStorage/Shared/GameConfig
-- Единый конфиг проекта Left Alone! (1 vs 9 House Traps)

local GameConfig = {}

GameConfig.Phases = {
	Lobby = "Lobby",
	Prep = "Prep",
	Invasion = "Invasion",
	End = "End",
}

GameConfig.Durations = {
	LobbyWait = 6,        -- секунд ожидания перед стартом раунда
	PrepDuration = 25,    -- фаза расстановки ловушек / поездки воров в фургоне
	InvasionDuration = 180, -- 3 минуты на штурм дома
	EndDuration = 7,      -- показ итогов раунда
}

-- Старт уже от 2 игроков (решает ловушку "ждём 10 человек")
GameConfig.MinPlayers = 2
-- В Studio позволяет тестировать цикл в одиночку (1 игрок = Защитник)
GameConfig.StudioSoloTest = true

GameConfig.EntryPoints = {
	"FrontDoor",
	"Garage",
	"Basement",
	"Chimney",
}

-- Автобаланс бюджета и жизней под количество воров (1..9)
function GameConfig.GetScaling(thiefCount: number)
	local clamped = math.clamp(thiefCount, 1, 9)
	return {
		DefenderTrapBudget = 150 + clamped * 40, -- больше воров -> больше монет на ловушки
		MaxTrapsPlaced = 4 + math.ceil(clamped * 0.6),
		ThiefWalkSpeed = 16,
		DefenderWalkSpeed = 17,
	}
end

-- Базовый реестр ловушек (Этап 1-2 для Бекзода)
GameConfig.Traps = {
	PaintCan = { Name = "Банка краски", SlotType = "Stairs", Cost = 50, Cooldown = 10 },
	IcePatch = { Name = "Лёд", SlotType = "Floor", Cost = 35, Cooldown = 6 },
	ToyCars = { Name = "Машинки", SlotType = "Floor", Cost = 30, Cooldown = 5 },
	SuperGlue = { Name = "Суперклей", SlotType = "Floor", Cost = 40, Cooldown = 8 },
	DoorTorch = { Name = "Горелка на двери", SlotType = "Door", Cost = 45, Cooldown = 9 },
}

GameConfig.Rewards = {
	DefenderWinCoins = 100,
	ThiefWinCoins = 60,
	ParticipationCoins = 20,
}

return GameConfig
