--!strict

-- Lightweight visual wind for the modular cliff-wall grass panels.
-- Roblox GlobalWind does not deform ordinary static MeshParts, so only the
-- nearest panels are tilted by a very small amount on the client.

local RunService = game:GetService("RunService")
local Workspace = game:GetService("Workspace")

local MAP_NAME = "PinkHouseMap"
local GRASS_MODEL_NAME = "WallGrassProductionV1"

local ACTIVE_RANGE = 175
local MAX_ACTIVE_PANELS = 96
local ACTIVE_REFRESH_SECONDS = 0.4
local UPDATE_SECONDS = 1 / 30
local BASE_SWAY_RADIANS = math.rad(0.55)

-- Smooth distance LOD for Layer2 density panels (*_Layer2 folders):
-- Close/mid range keeps full 2x density; far range fades Layer2 seamlessly
-- into Layer1 (which stays loaded across the cliff) to save triangles with zero pop.
local LAYER2_FADE_START = 320
local LAYER2_FADE_END = 420

type PanelRecord = {
	part: MeshPart,
	base: CFrame,
	phase: number,
}

type Candidate = {
	part: MeshPart,
	distance: number,
}

local map = Workspace:WaitForChild(MAP_NAME)
local grassModel = map:WaitForChild(GRASS_MODEL_NAME)

local baseFrames: { [MeshPart]: CFrame } = setmetatable({}, { __mode = "k" }) :: any
local activePanels: { PanelRecord } = {}
local refreshClock = math.huge
local updateClock = 0

local function phaseFor(position: Vector3): number
	return (position.X * 0.071 + position.Y * 0.037 + position.Z * 0.053) % (math.pi * 2)
end

local function restorePanels(panels: { PanelRecord })
	for _, record in panels do
		local part = record.part
		if part.Parent ~= nil then
			part.CFrame = record.base
		end
	end
end

local function refreshActivePanels()
	local camera = Workspace.CurrentCamera
	if camera == nil then
		return
	end

	local cameraPosition = camera.CFrame.Position
	local candidates: { Candidate } = {}

	for _, descendant in grassModel:GetDescendants() do
		if descendant:IsA("MeshPart") then
			local part = descendant
			local base = baseFrames[part]
			if base == nil then
				base = part.CFrame
				baseFrames[part] = base
			end

			local distance = (base.Position - cameraPosition).Magnitude
			local parent = part.Parent
			if parent ~= nil and string.sub(parent.Name, -7) == "_Layer2" then
				if distance <= LAYER2_FADE_START then
					part.LocalTransparencyModifier = 0
				elseif distance >= LAYER2_FADE_END then
					part.LocalTransparencyModifier = 1
				else
					part.LocalTransparencyModifier = (distance - LAYER2_FADE_START)
						/ (LAYER2_FADE_END - LAYER2_FADE_START)
				end
			end

			if distance <= ACTIVE_RANGE then
				table.insert(candidates, {
					part = part,
					distance = distance,
				})
			end
		end
	end

	table.sort(candidates, function(a, b)
		return a.distance < b.distance
	end)

	local nextActive: { PanelRecord } = {}
	local nextSet: { [MeshPart]: boolean } = {}
	local count = math.min(#candidates, MAX_ACTIVE_PANELS)

	for index = 1, count do
		local part = candidates[index].part
		local base = baseFrames[part]
		if base ~= nil then
			table.insert(nextActive, {
				part = part,
				base = base,
				phase = phaseFor(base.Position),
			})
			nextSet[part] = true
		end
	end

	for _, record in activePanels do
		if not nextSet[record.part] and record.part.Parent ~= nil then
			record.part.CFrame = record.base
		end
	end

	activePanels = nextActive
end

RunService.PreRender:Connect(function(deltaTime: number)
	refreshClock += deltaTime
	updateClock += deltaTime

	if refreshClock >= ACTIVE_REFRESH_SECONDS then
		refreshClock = 0
		refreshActivePanels()
	end

	if updateClock < UPDATE_SECONDS then
		return
	end
	updateClock %= UPDATE_SECONDS

	local wind = Workspace.GlobalWind
	local windSpeed = wind.Magnitude
	if windSpeed < 0.05 then
		restorePanels(activePanels)
		return
	end

	local time = Workspace.DistributedGameTime
	local windDirection = wind.Unit
	local strength = math.clamp(windSpeed / 3, 0.25, 1.35)
	local maxAngle = BASE_SWAY_RADIANS * strength

	for _, record in activePanels do
		local part = record.part
		if part.Parent == nil then
			continue
		end

		local phase = record.phase
		local broadWave = math.sin(time * 1.15 + phase)
		local detailWave = math.sin(time * 2.35 + phase * 1.73) * 0.28
		local gust = math.sin(time * 0.31 + phase * 0.41) * 0.17
		local wave = broadWave * 0.62 + detailWave + gust
		local pitch = wave * maxAngle * (0.72 + math.abs(windDirection.Z) * 0.28)
		local yaw = wave * maxAngle * windDirection.X * 0.42

		-- The imported panel roots sit on the wall plane. Rotate around that plane
		-- so the base remains attached instead of visibly floating off the cliff.
		local halfDepth = part.Size.Z * 0.5
		part.CFrame = record.base
			* CFrame.new(0, 0, halfDepth)
			* CFrame.Angles(pitch, yaw, 0)
			* CFrame.new(0, 0, -halfDepth)
	end
end)
