--!strict
--[[
	WallGrassLODController
	Streams visibility and shadow casting for the 3D wall-grass sectors in
	Workspace.PinkHouseMap.WallGrassStreamingSectors based on player distance.
]]

local Players = game:GetService("Players")

local VISIBLE_RADIUS = 135
local SHADOW_RADIUS = 55
local UPDATE_INTERVAL = 0.25

local pinkHouseMap = workspace:WaitForChild("PinkHouseMap")
local folder = pinkHouseMap:WaitForChild("WallGrassStreamingSectors")
local parts = folder:GetChildren()

while task.wait(UPDATE_INTERVAL) do
	local roots: { BasePart } = {}
	for _, plr in Players:GetPlayers() do
		local character = plr.Character
		local root = character and character:FindFirstChild("HumanoidRootPart")
		if root and root:IsA("BasePart") then
			table.insert(roots, root)
		end
	end

	for _, part in parts do
		if part:IsA("BasePart") then
			local nearest = math.huge
			for _, root in roots do
				nearest = math.min(nearest, (part.Position - root.Position).Magnitude)
			end
			part.Transparency = if nearest < VISIBLE_RADIUS then 0 else 1
			part.CastShadow = nearest < SHADOW_RADIUS
		end
	end
end
