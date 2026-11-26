-- ServerScriptService/Core/RoundManager
-- Этап 1 (Lead Dev): Главный цикл раунда Lobby -> Prep -> Invasion -> End

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local GameConfig = require(ReplicatedStorage.Shared.GameConfig)
local Remotes = ReplicatedStorage.Remotes
local RoundStateChanged = Remotes.RoundStateChanged

local currentPhase = GameConfig.Phases.Lobby
local currentDefender: Player? = nil
local roundEndedReason: string? = nil

-- Инициализация игрока: leaderstats + шанс роли (MM2-система)
local function setupPlayer(player: Player)
	local ls = Instance.new("Folder")
	ls.Name = "leaderstats"
	ls.Parent = player

	local coins = Instance.new("IntValue")
	coins.Name = "Coins"
	coins.Value = 100
	coins.Parent = ls

	local streak = Instance.new("IntValue")
	streak.Name = "WinStreak"
	streak.Value = 0
	streak.Parent = ls

	player:SetAttribute("Role", "Lobby")
	player:SetAttribute("DefenderWeight", 1)
	player:SetAttribute("TrapBudget", 0)
end

Players.PlayerAdded:Connect(setupPlayer)
for _, p in ipairs(Players:GetPlayers()) do
	if not p:FindFirstChild("leaderstats") then
		setupPlayer(p)
	end
end

local function broadcastState(phase: string, timeLeft: number, message: string)
	currentPhase = phase
	workspace:SetAttribute("RoundPhase", phase)
	workspace:SetAttribute("RoundTimeLeft", timeLeft)
	workspace:SetAttribute("DefenderName", currentDefender and currentDefender.Name or "")

	for _, player in ipairs(Players:GetPlayers()) do
		RoundStateChanged:FireClient(player, {
			phase = phase,
			timeLeft = timeLeft,
			role = player:GetAttribute("Role") or "Lobby",
			defenderName = currentDefender and currentDefender.Name or "",
			message = message,
		})
	end
end

local function teleportPlayer(player: Player, targetPart: BasePart?)
	if not targetPart then return end
	local char = player.Character
	if not char then return end
	local hrp = char:FindFirstChild("HumanoidRootPart")
	if hrp and hrp:IsA("BasePart") then
		hrp.CFrame = targetPart.CFrame + Vector3.new(math.random(-3, 3), 3.5, math.random(-3, 3))
	end
end

local function getSpawns()
	local map = workspace:FindFirstChild("Map")
	if not map then return nil end
	return map:FindFirstChild("Spawns")
end

-- Взвешенный выбор Защитника (как в Murder Mystery 2)
local function pickDefender(playerList: { Player }): Player
	local totalWeight = 0
	for _, p in ipairs(playerList) do
		totalWeight += (p:GetAttribute("DefenderWeight") or 1)
	end
	local roll = math.random() * totalWeight
	local acc = 0
	for _, p in ipairs(playerList) do
		acc += (p:GetAttribute("DefenderWeight") or 1)
		if roll <= acc then
			return p
		end
	end
	return playerList[1]
end

local function addCoins(player: Player, amount: number)
	local ls = player:FindFirstChild("leaderstats")
	local coins = ls and ls:FindFirstChild("Coins")
	if coins and coins:IsA("IntValue") then
		coins.Value += amount
	end
end

local function setWinStreak(player: Player, won: boolean)
	local ls = player:FindFirstChild("leaderstats")
	local streak = ls and ls:FindFirstChild("WinStreak")
	if streak and streak:IsA("IntValue") then
		streak.Value = won and (streak.Value + 1) or 0
	end
end

-- Подключаем триггер Тарзанки (победа Защитника при касании)
local function hookZiplineGoal()
	local map = workspace:FindFirstChild("Map")
	local zones = map and map:FindFirstChild("Zones")
	local attic = zones and zones:FindFirstChild("Zone4_AtticAndTreehouse")
	local goal = attic and attic:FindFirstChild("ZiplineGoal")
	if goal and goal:IsA("BasePart") then
		goal.Touched:Connect(function(hit)
			if currentPhase ~= GameConfig.Phases.Invasion or roundEndedReason ~= nil then return end
			local char = hit.Parent
			local player = char and Players:GetPlayerFromCharacter(char)
			if player and player == currentDefender then
				roundEndedReason = "DefenderEscaped"
			end
		end)
	end
end

local function runCountdown(phase: string, seconds: number, message: string, shouldStopFn: (() -> boolean)?): boolean
	for t = seconds, 1, -1 do
		if shouldStopFn and shouldStopFn() then
			return true
		end
		broadcastState(phase, t, message)
		task.wait(1)
	end
	return false
end

-- Главный бесконечный цикл игры
task.spawn(function()
	task.wait(1)
	hookZiplineGoal()

	while true do
		-- 1. LOBBY
		currentDefender = nil
		roundEndedReason = nil
		local spawns = getSpawns()
		local lobbySpawn = spawns and spawns:FindFirstChild("LobbySpawn")

		for _, p in ipairs(Players:GetPlayers()) do
			p:SetAttribute("Role", "Lobby")
			p:SetAttribute("TrapBudget", 0)
			if lobbySpawn and lobbySpawn:IsA("BasePart") then
				teleportPlayer(p, lobbySpawn)
			end
		end

		local minRequired = (RunService:IsStudio() and GameConfig.StudioSoloTest) and 1 or GameConfig.MinPlayers
		while #Players:GetPlayers() < minRequired do
			broadcastState(
				GameConfig.Phases.Lobby,
				0,
				string.format("Ждём игроков (%d/%d)...", #Players:GetPlayers(), minRequired)
			)
			task.wait(1)
		end

		runCountdown(GameConfig.Phases.Lobby, GameConfig.Durations.LobbyWait, "Раунд скоро начнётся!")

		-- 2. ROLE SELECTION & PREP PHASE (25 сек)
		local participants = Players:GetPlayers()
		if #participants < minRequired then
			continue
		end

		currentDefender = pickDefender(participants)
		local thiefCount = math.max(1, #participants - 1)
		local scaling = GameConfig.GetScaling(thiefCount)

		local defSpawn = spawns and spawns:FindFirstChild("DefenderSpawn")
		local vanSpawn = spawns and spawns:FindFirstChild("VanSpawn")

		for _, p in ipairs(participants) do
			if p == currentDefender then
				p:SetAttribute("Role", "Defender")
				p:SetAttribute("DefenderWeight", 1) -- сброс веса
				p:SetAttribute("TrapBudget", scaling.DefenderTrapBudget)
				if defSpawn and defSpawn:IsA("BasePart") then
					teleportPlayer(p, defSpawn)
				end
			else
				p:SetAttribute("Role", "Thief")
				p:SetAttribute("DefenderWeight", (p:GetAttribute("DefenderWeight") or 1) + 1)
				if vanSpawn and vanSpawn:IsA("BasePart") then
					teleportPlayer(p, vanSpawn)
				end
			end
		end

		runCountdown(
			GameConfig.Phases.Prep,
			GameConfig.Durations.PrepDuration,
			"Подготовка: Защитник ставит ловушки, Воры едут в фургоне!"
		)

		-- 3. INVASION PHASE (180 сек)
		local entrySpawns = spawns and spawns:FindFirstChild("EntrySpawns")
		local defaultEntry = entrySpawns and entrySpawns:FindFirstChild("FrontDoor")

		for _, p in ipairs(participants) do
			if p.Parent and p:GetAttribute("Role") == "Thief" and defaultEntry and defaultEntry:IsA("BasePart") then
				teleportPlayer(p, defaultEntry)
			end
		end

		-- Следим за поимкой / смертью Защитника
		local defenderDeathConn: RBXScriptConnection? = nil
		if currentDefender and currentDefender.Character then
			local hum = currentDefender.Character:FindFirstChildOfClass("Humanoid")
			if hum then
				defenderDeathConn = hum.Died:Connect(function()
					if currentPhase == GameConfig.Phases.Invasion and roundEndedReason == nil then
						roundEndedReason = "DefenderCaught"
					end
				end)
			end
		end

		runCountdown(
			GameConfig.Phases.Invasion,
			GameConfig.Durations.InvasionDuration,
			"ШТУРМ! Защитник бежит к тарзанке на чердаке, Воры ловят его!",
			function()
				if roundEndedReason ~= nil then return true end
				if not currentDefender or not currentDefender.Parent then
					roundEndedReason = "DefenderLeft"
					return true
				end
				return false
			end
		)

		if defenderDeathConn then
			defenderDeathConn:Disconnect()
		end

		-- 4. END PHASE (Итоги и награды)
		local endMsg = "Время вышло! Защитник победил!"
		local defenderWon = true

		if roundEndedReason == "DefenderEscaped" then
			endMsg = "Защитник сбежал по тарзанке! Победа Защитника!"
			defenderWon = true
		elseif roundEndedReason == "DefenderCaught" then
			endMsg = "Воры поймали Защитника! Победа Воров!"
			defenderWon = false
		elseif roundEndedReason == "DefenderLeft" then
			endMsg = "Защитник вышел из игры. Победа Воров!"
			defenderWon = false
		end

		for _, p in ipairs(participants) do
			if p.Parent then
				local isDef = (p == currentDefender)
				if (isDef and defenderWon) or ((not isDef) and (not defenderWon)) then
					addCoins(p, isDef and GameConfig.Rewards.DefenderWinCoins or GameConfig.Rewards.ThiefWinCoins)
					setWinStreak(p, true)
				else
					addCoins(p, GameConfig.Rewards.ParticipationCoins)
					setWinStreak(p, false)
				end
			end
		end

		runCountdown(GameConfig.Phases.End, GameConfig.Durations.EndDuration, endMsg)
	end
end)
