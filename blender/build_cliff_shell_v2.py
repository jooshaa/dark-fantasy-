import bpy
import math
import os
import random
from mathutils import Vector, noise


ROOT = "/Users/asal/Documents/roblox dev"
BLEND_PATH = os.path.join(ROOT, "blender", "pink_house_cliff_shell_v2.blend")
GLB_PATH = os.path.join(ROOT, "exports", "pink_house_cliff_shell_v2.glb")

STUD_M = 0.28
WIDTH = 1400 * STUD_M
HEIGHT = 1000 * STUD_M
DEPTH = 620 * STUD_M
CHASM = 25 * STUD_M

FRONT_COUNT = 8
SIDE_COUNT = 4
CHASM_COUNT = 4
FRONT_X = 24
FRONT_Z = 64
SIDE_Y = 20
SIDE_Z = 64


def reset_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for blocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials):
        for block in list(blocks):
            if block.users == 0:
                blocks.remove(block)


def material():
    mat = bpy.data.materials.new("PinkHouse_CliffRock_Source")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (0.032, 0.072, 0.038, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.96
    bsdf.inputs["Metallic"].default_value = 0.0
    return mat


def layered_noise(a, b, seed):
    return (
        math.sin(a * 0.085 + seed * 1.71) * 0.42
        + math.sin(b * 0.22 + a * 0.031 + seed * 0.83) * 0.24
        + math.sin((a - b) * 0.49 + seed * 2.17) * 0.13
        + math.sin(a * 0.018 + b * 0.041 + seed) * 0.62
    )


def cliff_relief(horizontal, z, seed):
    zn = z / HEIGHT
    macro_p = Vector((horizontal * 0.0105, z * 0.0075, seed))
    medium_p = Vector((horizontal * 0.026, z * 0.019, seed * 1.73))
    crack_p = Vector((horizontal * 0.061, z * 0.038, seed * 2.41))

    macro = noise.fractal(
        macro_p, 0.82, 2.05, 4, noise_basis="PERLIN_NEW"
    )
    medium = noise.fractal(
        medium_p, 0.72, 2.13, 3, noise_basis="PERLIN_NEW"
    )
    hard = noise.turbulence(
        crack_p, 3, True, noise_basis="PERLIN_NEW", amplitude_scale=0.52,
        frequency_scale=2.1,
    )
    vector_noise = noise.noise_vector(
        Vector((horizontal * 0.017, z * 0.011, seed * 0.43)),
        noise_basis="PERLIN_NEW",
    ).x

    # Broad geological masses plus smaller fractured variation. Horizontal shelf
    # bands are locally masked so they read as broken ledges, not uniform waves.
    mass = macro * 11.0 + medium * 4.5 + vector_noise * 3.0
    fracture = (hard - 0.34) * 2.2
    vertical_channel = -abs(
        noise.fractal(
            Vector((horizontal * 0.023, seed, 0.0)),
            0.7,
            2.0,
            3,
            noise_basis="PERLIN_NEW",
        )
    ) * 4.0

    shelf_mask = max(0.0, noise.fractal(
        Vector((horizontal * 0.014, seed * 0.3, 4.0)),
        0.8,
        2.0,
        3,
        noise_basis="PERLIN_NEW",
    ) + 0.18)
    ledge_a = math.exp(-((zn - 0.24) / 0.022) ** 2) * shelf_mask * 9.0
    ledge_b = math.exp(-((zn - 0.53) / 0.032) ** 2) * shelf_mask * 11.0
    ledge_c = math.exp(-((zn - 0.79) / 0.025) ** 2) * shelf_mask * 7.0
    lower_erosion = (1.0 - zn) ** 2 * medium * 4.0
    return mass + fracture + vertical_channel + ledge_a + ledge_b + ledge_c + lower_erosion


def create_surface(name, vertices, faces, mat):
    mesh = bpy.data.meshes.new(f"{name}_mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update(calc_edges=True)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    for poly in mesh.polygons:
        poly.use_smooth = True

    solid = obj.modifiers.new("RockMass", "SOLIDIFY")
    solid.thickness = 2.8
    solid.offset = 0.45
    solid.use_even_offset = True

    bevel = obj.modifiers.new("EdgeSoftening", "BEVEL")
    bevel.width = 0.12
    bevel.segments = 2
    bevel.limit_method = "ANGLE"

    obj["roblox_surface_shell"] = True
    return obj


def grid_faces(nx, nz, reverse=False):
    row = nx + 1
    faces = []
    for zi in range(nz):
        for xi in range(nx):
            a = zi * row + xi
            b = a + 1
            c = a + row + 1
            d = a + row
            faces.append((a, b, c, d) if reverse else (a, d, c, b))
    return faces


def create_front_modules(mat):
    usable = WIDTH - CHASM
    module_w = usable / FRONT_COUNT
    left_start = -WIDTH / 2
    right_start = CHASM / 2

    for index in range(FRONT_COUNT):
        if index < FRONT_COUNT // 2:
            x0 = left_start + index * module_w
        else:
            x0 = right_start + (index - FRONT_COUNT // 2) * module_w
        verts = []
        for zi in range(FRONT_Z + 1):
            z = HEIGHT * zi / FRONT_Z
            for xi in range(FRONT_X + 1):
                x = x0 + module_w * xi / FRONT_X
                relief = cliff_relief(x, z, 10.0)
                # The face points toward negative Y; deeper relief makes the silhouette readable.
                y = -relief
                if zi == FRONT_Z:
                    y -= 1.2 * math.sin(x * 0.09)
                verts.append((x, y, z))
        obj = create_surface(
            f"FrontCliff_{index + 1:02d}", verts, grid_faces(FRONT_X, FRONT_Z), mat
        )
        obj["roblox_target_width_studs"] = module_w / STUD_M
        obj["roblox_target_height_studs"] = 1000


def create_side_modules(mat, side):
    x_base = side * WIDTH / 2
    module_d = DEPTH / SIDE_COUNT
    label = "Right" if side > 0 else "Left"
    for index in range(SIDE_COUNT):
        y0 = index * module_d
        verts = []
        for zi in range(SIDE_Z + 1):
            z = HEIGHT * zi / SIDE_Z
            for yi in range(SIDE_Y + 1):
                y = y0 + module_d * yi / SIDE_Y
                relief = cliff_relief(y + side * 31.0, z, 21.0 + side * 2.0)
                x = x_base + side * relief
                verts.append((x, y, z))
        obj = create_surface(
            f"{label}Cliff_{index + 1:02d}",
            verts,
            grid_faces(SIDE_Y, SIDE_Z, reverse=side < 0),
            mat,
        )
        obj["roblox_target_depth_studs"] = module_d / STUD_M
        obj["roblox_target_height_studs"] = 1000


def create_chasm_modules(mat, side):
    x_base = side * CHASM / 2
    module_d = DEPTH / CHASM_COUNT
    label = "ChasmRight" if side > 0 else "ChasmLeft"
    for index in range(CHASM_COUNT):
        y0 = index * module_d
        verts = []
        for zi in range(SIDE_Z + 1):
            z = HEIGHT * zi / SIDE_Z
            for yi in range(SIDE_Y + 1):
                y = y0 + module_d * yi / SIDE_Y
                relief = cliff_relief(y + side * 73.0, z, 35.0 + side * 3.0)
                # Keep the 25-stud playable opening while adding eroded inner walls.
                x = x_base - side * min(abs(relief) * 0.22, 1.35)
                verts.append((x, y, z))
        obj = create_surface(
            f"{label}_{index + 1:02d}",
            verts,
            grid_faces(SIDE_Y, SIDE_Z, reverse=side > 0),
            mat,
        )
        obj["roblox_chasm_wall"] = True
        obj["roblox_target_height_studs"] = 1000


def create_rock_mass(name, location, scale, seed, mat):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=1.0, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(mat)
    rng = random.Random(seed)
    for vertex in obj.data.vertices:
        p = vertex.co.normalized()
        sample = noise.fractal(
            Vector((p.x * 2.2 + seed, p.y * 2.2, p.z * 2.2)),
            0.78,
            2.0,
            3,
            noise_basis="PERLIN_NEW",
        )
        vertex.co *= 1.0 + sample * 0.24 + rng.uniform(-0.035, 0.035)
    for poly in obj.data.polygons:
        poly.use_smooth = False
    obj.rotation_euler = (
        math.radians(rng.uniform(-16, 16)),
        math.radians(rng.uniform(-22, 22)),
        math.radians(rng.uniform(-12, 12)),
    )
    obj["roblox_hero_rock_mass"] = True
    return obj


def create_hero_masses(mat):
    # Broken shelves and buttresses disrupt the procedural wall read. They overlap
    # the shell intentionally and remain separate reusable MeshParts in Roblox.
    front_specs = [
        (-155, 1, 48,  (24, 6, 30)),
        (-118, 0, 132, (18, 7, 24)),
        (-73, 1, 218,  (28, 6, 19)),
        (-31, 2, 78,   (15, 5, 28)),
        (34, 0, 194,   (17, 7, 31)),
        (79, 1, 61,    (25, 6, 21)),
        (126, -1, 145, (21, 8, 27)),
        (168, 1, 236,  (18, 6, 22)),
    ]
    for index, (x, y, z, scale) in enumerate(front_specs, 1):
        create_rock_mass(f"FrontHeroRock_{index:02d}", (x, y, z), scale, 500 + index, mat)

    side_specs = [
        (-WIDTH / 2 + 1, 35, 82,  (6, 21, 31)),
        (-WIDTH / 2 + 1, 118, 205, (7, 27, 22)),
        (WIDTH / 2 - 1, 48, 188,   (7, 24, 29)),
        (WIDTH / 2 - 1, 132, 73,   (6, 25, 26)),
    ]
    for index, (x, y, z, scale) in enumerate(side_specs, 1):
        create_rock_mass(f"SideHeroRock_{index:02d}", (x, y, z), scale, 700 + index, mat)


def add_orientation_markers():
    marker_mat = bpy.data.materials.new("Verification_Markers")
    marker_mat.diffuse_color = (0.8, 0.08, 0.05, 1.0)
    for name, location in (
        ("VERIFY_Front_TopLeft", (-WIDTH / 2 + 1.0, -1.0, HEIGHT - 2.0)),
        ("VERIFY_Rear_Right", (WIDTH / 2, DEPTH - 1.0, HEIGHT * 0.25)),
    ):
        bpy.ops.mesh.primitive_cube_add(location=location, scale=(0.5, 0.5, 1.0))
        marker = bpy.context.object
        marker.name = name
        marker.data.materials.append(marker_mat)
        marker.hide_render = True
        marker["verification_only"] = True


def save_and_export():
    os.makedirs(os.path.dirname(BLEND_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(GLB_PATH), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
    # Keep verification markers in the editable .blend, but never ship them to
    # Roblox. Export only production mesh objects.
    bpy.ops.object.select_all(action="DESELECT")
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH" and not obj.get("verification_only", False):
            obj.select_set(True)
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
mat = material()
create_front_modules(mat)
create_side_modules(mat, -1)
create_side_modules(mat, 1)
create_chasm_modules(mat, -1)
create_chasm_modules(mat, 1)
create_hero_masses(mat)
add_orientation_markers()
save_and_export()

mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
print(
    {
        "blend": BLEND_PATH,
        "glb": GLB_PATH,
        "mesh_objects": len(mesh_objects),
        "front_modules": FRONT_COUNT,
        "side_modules": SIDE_COUNT * 2,
        "chasm_modules": CHASM_COUNT * 2,
        "hero_rock_masses": 12,
        "exported_mesh_objects": len(
            [obj for obj in mesh_objects if not obj.get("verification_only", False)]
        ),
        "target_studs": [1400, 620, 1000],
        "chasm_studs": 25,
    }
)
