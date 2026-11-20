import bpy
import math
import os
import random


ROOT = "/Users/asal/Documents/roblox dev"
EXPORT_DIR = os.path.join(ROOT, "exports")
BLEND_PATH = os.path.join(ROOT, "blender", "pink_house_cliff_modules.blend")
GLB_PATH = os.path.join(EXPORT_DIR, "pink_house_cliff_modules.glb")

# The assembled facade is approximately 1360 x 1000 studs in Roblox.
# Source dimensions are metres; 1 Roblox stud is treated as 0.28 m.
STUD_METRES = 0.28
MODULE_WIDTH = 170 * STUD_METRES
MODULE_HEIGHT = 1000 * STUD_METRES
MODULE_COUNT = 8
GRID_X = 14
GRID_Z = 42


def reset_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials):
        for block in list(datablocks):
            if block.users == 0:
                datablocks.remove(block)


def create_material():
    mat = bpy.data.materials.new("OvergrownCliff_Source")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (0.045, 0.16, 0.055, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.94
    bsdf.inputs["Metallic"].default_value = 0.0
    return mat


def displacement(seed, x_norm, z_norm):
    """Layered deterministic erosion without requiring external texture files."""
    wave_a = math.sin(x_norm * 11.0 + seed * 0.71) * 0.72
    wave_b = math.sin(z_norm * 31.0 + x_norm * 7.0 + seed) * 0.38
    wave_c = math.sin((x_norm + z_norm) * 47.0 + seed * 2.31) * 0.18
    vertical_groove = -abs(math.sin(x_norm * 19.0 + seed * 0.43)) * 0.52
    broad_bulge = math.sin(x_norm * math.pi * 2.0 + seed) * 0.45
    return (wave_a + wave_b + wave_c + vertical_groove + broad_bulge) * STUD_METRES * 6.0


def create_cliff_module(index, material):
    rng = random.Random(8100 + index)
    vertices = []
    faces = []

    x_offset = (index - (MODULE_COUNT - 1) / 2.0) * MODULE_WIDTH

    for zi in range(GRID_Z + 1):
        z_norm = zi / GRID_Z
        z = z_norm * MODULE_HEIGHT
        taper = 1.0 - 0.035 * math.sin(z_norm * math.pi)
        for xi in range(GRID_X + 1):
            x_norm = xi / GRID_X
            edge_noise = 0.0
            if xi in (0, GRID_X):
                edge_noise = rng.uniform(-0.75, 0.75) * STUD_METRES
            x = (x_norm - 0.5) * MODULE_WIDTH * taper + x_offset + edge_noise
            y = displacement(index + 1, x_norm, z_norm)
            # Heavier erosion near the bottom and a slight grassy brow at the top.
            y += (1.0 - z_norm) ** 2 * math.sin(x_norm * 17 + index) * STUD_METRES * 3.0
            if zi == GRID_Z:
                y += STUD_METRES * (2.0 + 2.5 * math.sin(x_norm * 9 + index))
            vertices.append((x, y, z))

    row = GRID_X + 1
    for zi in range(GRID_Z):
        for xi in range(GRID_X):
            a = zi * row + xi
            b = a + 1
            c = a + row + 1
            d = a + row
            # Winding faces toward +Y, which maps to the camera-facing -Z in Roblox.
            faces.append((a, d, c, b))

    mesh = bpy.data.meshes.new(f"CliffModule_{index + 1:02d}_mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update(calc_edges=True)

    obj = bpy.data.objects.new(f"CliffModule_{index + 1:02d}", mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)

    for polygon in mesh.polygons:
        polygon.use_smooth = True

    # Weighted normal-like smoothing while preserving the broad cliff silhouette.
    bevel = obj.modifiers.new("MicroBevel", "BEVEL")
    bevel.width = 0.035
    bevel.segments = 1
    bevel.limit_method = "ANGLE"

    obj["roblox_target_height_studs"] = 1000
    obj["roblox_target_width_studs"] = 170
    obj["variant_index"] = index + 1
    return obj


def add_asymmetric_marker():
    """Tiny top-left marker used only to verify import orientation."""
    bpy.ops.mesh.primitive_cube_add(
        location=(-MODULE_COUNT * MODULE_WIDTH / 2 + 0.7, 0.35, MODULE_HEIGHT - 1.0),
        scale=(0.35, 0.35, 1.0),
    )
    marker = bpy.context.object
    marker.name = "OrientationMarker_TopLeft"
    marker.hide_render = True
    marker["verification_only"] = True


def export_scene():
    os.makedirs(EXPORT_DIR, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.export_scene.gltf(
        filepath=GLB_PATH,
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_yup=True,
        export_materials="EXPORT",
        export_cameras=False,
        export_lights=False,
        export_extras=True,
    )


reset_scene()
material = create_material()
for module_index in range(MODULE_COUNT):
    create_cliff_module(module_index, material)
add_asymmetric_marker()
export_scene()

print(f"BLEND={BLEND_PATH}")
print(f"GLB={GLB_PATH}")
print(f"MODULES={MODULE_COUNT}")
print(f"EXPECTED_STUDS=1360x14x1000")
