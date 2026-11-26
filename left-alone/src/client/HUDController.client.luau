-- StarterPlayerScripts/HUDController
-- Базовый верхний HUD (фаза раунда, таймер, роль игрока) — готов для ПК и мобильных

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local player = Players.LocalPlayer
local playerGui = player:WaitForChild("PlayerGui")
local RoundStateChanged = ReplicatedStorage:WaitForChild("Remotes"):WaitForChild("RoundStateChanged")

-- Создаём аккуратный ScreenGui
local screenGui = Instance.new("ScreenGui")
screenGui.Name = "LeftAloneHUD"
screenGui.ResetOnSpawn = false
screenGui.IgnoreGuiInset = true
screenGui.Parent = playerGui

local topBar = Instance.new("Frame")
topBar.Name = "TopBar"
topBar.AnchorPoint = Vector2.new(0.5, 0)
topBar.Position = UDim2.new(0.5, 0, 0, 12)
topBar.Size = UDim2.new(0, 420, 0, 68)
topBar.BackgroundColor3 = Color3.fromRGB(17, 24, 39)
topBar.BackgroundTransparency = 0.15
topBar.Parent = screenGui

local corner = Instance.new("UICorner")
corner.CornerRadius = UDim.new(0, 14)
corner.Parent = topBar

local stroke = Instance.new("UIStroke")
stroke.Color = Color3.fromRGB(59, 130, 246)
stroke.Thickness = 2
stroke.Parent = topBar

local phaseLabel = Instance.new("TextLabel")
phaseLabel.Name = "PhaseLabel"
phaseLabel.BackgroundTransparency = 1
phaseLabel.Position = UDim2.new(0, 14, 0, 6)
phaseLabel.Size = UDim2.new(0.65, -14, 0, 26)
phaseLabel.Font = Enum.Font.GothamBold
phaseLabel.TextSize = 18
phaseLabel.TextXAlignment = Enum.TextXAlignment.Left
phaseLabel.TextColor3 = Color3.fromRGB(255, 255, 255)
phaseLabel.Text = "ЛОББИ"
phaseLabel.Parent = topBar

local timerLabel = Instance.new("TextLabel")
timerLabel.Name = "TimerLabel"
timerLabel.BackgroundTransparency = 1
timerLabel.Position = UDim2.new(0.65, 0, 0, 6)
timerLabel.Size = UDim2.new(0.35, -14, 0, 26)
timerLabel.Font = Enum.Font.GothamBlack
timerLabel.TextSize = 20
timerLabel.TextXAlignment = Enum.TextXAlignment.Right
timerLabel.TextColor3 = Color3.fromRGB(250, 204, 21)
timerLabel.Text = "00:00"
timerLabel.Parent = topBar

local msgLabel = Instance.new("TextLabel")
msgLabel.Name = "MessageLabel"
msgLabel.BackgroundTransparency = 1
msgLabel.Position = UDim2.new(0, 14, 0, 34)
msgLabel.Size = UDim2.new(1, -28, 0, 26)
msgLabel.Font = Enum.Font.Gotham
msgLabel.TextSize = 13
msgLabel.TextScaled = false
msgLabel.TextWrapped = true
msgLabel.TextXAlignment = Enum.TextXAlignment.Left
msgLabel.TextColor3 = Color3.fromRGB(203, 213, 225)
msgLabel.Text = "Подключение к раунду..."
msgLabel.Parent = topBar

local ROLE_NAMES = {
	Defender = "ЗАЩИТНИК",
	Thief = "ВОР",
	Lobby = "ЛОББИ",
}

local PHASE_COLORS = {
	Lobby = Color3.fromRGB(59, 130, 246),
	Prep = Color3.fromRGB(245, 158, 11),
	Invasion = Color3.fromRGB(239, 68, 68),
	End = Color3.fromRGB(34, 197, 94),
}

local function formatTime(sec: number)
	local m = math.floor(sec / 60)
	local s = sec % 60
	return string.format("%02d:%02d", m, s)
end

RoundStateChanged.OnClientEvent:Connect(function(data)
	local roleRu = ROLE_NAMES[data.role] or "ЛОББИ"
	phaseLabel.Text = string.format("%s  |  %s", string.upper(data.phase), roleRu)
	timerLabel.Text = formatTime(data.timeLeft or 0)
	msgLabel.Text = data.message or ""
	stroke.Color = PHASE_COLORS[data.phase] or Color3.fromRGB(59, 130, 246)
end)
