--!strict
--[[
	Client entry point synced to StarterPlayer.StarterPlayerScripts via Rojo.
]]

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local GameConfig = require(Shared:WaitForChild("GameConfig"))

print(string.format("[%s] Client initialized (active map: %s)", GameConfig.ExperienceName, GameConfig.ActiveMapName))
