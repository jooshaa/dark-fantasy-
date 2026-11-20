--!strict
--[[
	Shared configuration for the dark-fantasy Roblox experience.
	Synced to ReplicatedStorage.Shared.GameConfig via Rojo.
]]

local GameConfig = {
	ExperienceName = "dark fantasy",
	ActiveMapName = "PinkHouseMap",
	Maps = {
		{ Id = "PinkHouse", Name = "Pink House", UnlockMinutes = 0 },
		{ Id = "AshForest", Name = "Ash Forest", UnlockMinutes = 30 },
		{ Id = "SunkenCathedral", Name = "Sunken Cathedral", UnlockMinutes = 120 },
		{ Id = "DeadVillage", Name = "Dead Village", UnlockMinutes = 300 },
		{ Id = "CrimsonCastle", Name = "Crimson Castle", UnlockMinutes = 600 },
		{ Id = "FinalAbyss", Name = "Final Abyss", UnlockMinutes = 1200 },
	},
}

return GameConfig
