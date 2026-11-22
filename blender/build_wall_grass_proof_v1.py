import bpy
import hashlib
import json
import math
import random
from pathlib import Path

from mathutils import Vector


ROOT = Path("/Users/asal/Documents/roblox dev")
CHECKPOINT = ROOT / "blender" / "checkpoints" / "pink_house_wall_grass_proof_v1_empty.blend"
BLEND = ROOT / "blender" / "pink_house_wall_grass_proof_v1.blend"
GLB = ROOT / "exports" / "pink_house_wall_grass_proof_v1.glb"
FRONT = ROOT / "exports" / "pink_house_wall_grass_proof_v1_front.png"
OBLIQUE = ROOT / "exports" / "pink_house_wall_grass_proof_v1_oblique.png"
SIDE = ROOT / "exports" / "pink_house_wall_grass_proof_v1_side.png"
LIP = ROOT / "exports" / "pink_house_wall_grass_proof_v1_lip.png"

STUD = 0.28
WIDTH = 80 * STUD
HEIGHT = 80 * STUD
HALF_W = WIDTH * 0.5
HALF_H = HEIGHT * 0.5
GRID_PER_QUADRANT = 52
LIP_BLADES = 550


def material(name, color, roughness=0.9):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    mat.metallic = 0.0
    mat.roughness = roughness
    mat.use_backface_culling = False
    mat.use_nodes = True
    principled = mat.node_tree.nodes.get("Principled BSDF")
    principled.inputs["Base Color"].default_value = (*color, 1.0)
    principled.inputs["Roughness"].default_value = roughness
    return mat


def append_blade(verts, faces, root, length, width, depth, side, roll):
    """Create one curved ribbon rooted in the vertical XZ wall plane."""
    outward = Vector((0.0, -1.0, 0.0))
    tangent = Vector((math.cos(roll), 0.22 * math.sin(roll), 0.0)).normalized()
    p0 = root
    p1 = root + outward * depth * 0.32 + Vector((side * 0.12, 0.0, length * 0.03))
    p2 = root + outward * depth * 0.72 + Vector((side * 0.48, 0.0, -length * 0.10))
    p3 = root + outward * depth + Vector((side, 0.0, -length * 0.34))
    points = (p0, p1, p2, p3)
    widths = (width, width * 0.82, width * 0.48, 0.006)
    base = len(verts)
    for point, half_width in zip(points, widths):
        verts.append(tuple(point - tangent * half_width))
        verts.append(tuple(point + tangent * half_width))
    for index in range(3):
        a = base + index * 2
        b = a + 1
        c = a + 3
        d = a + 2
        faces.extend(((a, b, c), (a, c, d)))


def make_quadrant(index, xmin, xmax, zmin, zmax, seed, grass_mat):
    rng = random.Random(seed)
    verts, faces = [], []
    cell_x = (xmax - xmin) / GRID_PER_QUADRANT
    cell_z = (zmax - zmin) / GRID_PER_QUADRANT
    for row in range(GRID_PER_QUADRANT):
        for column in range(GRID_PER_QUADRANT):
            x = xmin + (column + 0.5 + rng.uniform(-0.43, 0.43)) * cell_x
            z = zmin + (row + 0.5 + rng.uniform(-0.43, 0.43)) * cell_z
            root = Vector((x, -0.31 + rng.uniform(-0.035, 0.035), z))
            clump = 1.0 + 0.16 * math.sin(x * 1.17 + z * 0.61) + 0.10 * math.sin(z * 1.83)
            length = rng.uniform(0.32, 0.74) * clump
            width = rng.uniform(0.042, 0.092) * clump
            depth = rng.uniform(0.24, 0.62) * clump
            side = rng.uniform(-0.18, 0.18)
            roll = rng.uniform(-1.1, 1.1)
            append_blade(verts, faces, root, length, width, depth, side, roll)

    mesh = bpy.data.meshes.new(f"WallGrass_Q{index}_Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update(calc_edges=True)
    obj = bpy.data.objects.new(f"WallGrass_Q{index}", mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(grass_mat)
    obj["roblox_size_studs"] = "40x40 quadrant of 80x80 module"
    obj["collision_owner"] = "existing Roblox cliff core"
    obj["seed"] = seed
    return obj


def make_lip(grass_mat):
    rng = random.Random(44071)
    verts, faces = [], []
    for _ in range(LIP_BLADES):
        x = rng.uniform(-HALF_W, HALF_W)
        root = Vector((x, rng.uniform(-0.18, 0.45), HEIGHT + rng.uniform(-0.11, 0.13)))
        length = rng.uniform(0.34, 0.78)
        width = rng.uniform(0.04, 0.09)
        depth = rng.uniform(0.28, 0.72)
        side = rng.uniform(-0.18, 0.18)
        append_blade(verts, faces, root, length, width, depth, side, rng.uniform(-0.65, 0.65))
    mesh = bpy.data.meshes.new("WallGrass_Lip_Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update(calc_edges=True)
    obj = bpy.data.objects.new("WallGrass_Lip", mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(grass_mat)
    obj["optional"] = True
    return obj


def audit_mesh(obj):
    mesh = obj.data
    mesh.calc_loop_triangles()
    non_finite = 0
    for vertex in mesh.vertices:
        if not all(math.isfinite(value) for value in vertex.co):
            non_finite += 1
    zero_edges = sum(
        1
        for edge in mesh.edges
        if (mesh.vertices[edge.vertices[0]].co - mesh.vertices[edge.vertices[1]].co).length <= 1e-8
    )
    zero_faces = sum(1 for polygon in mesh.polygons if polygon.area <= 1e-10)
    if non_finite or zero_edges or zero_faces:
        raise RuntimeError(
            f"Invalid mesh {obj.name}: non_finite={non_finite}, "
            f"zero_edges={zero_edges}, zero_faces={zero_faces}"
        )
    return {
        "name": obj.name,
        "vertices": len(mesh.vertices),
        "triangles": len(mesh.loop_triangles),
        "zero_edges": zero_edges,
        "zero_faces": zero_faces,
        "non_finite": non_finite,
    }


def look_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def make_preview(backing_mat, meadow_mat):
    bpy.ops.mesh.primitive_cube_add(location=(0, 0.2, HALF_H), scale=(HALF_W, 0.28, HALF_H))
    wall = bpy.context.object
    wall.name = "PREVIEW_Wall_NotExported"
    wall.data.materials.append(backing_mat)
    bpy.ops.mesh.primitive_cube_add(location=(0, 4.5, HEIGHT + 0.22), scale=(HALF_W, 4.5, 0.22))
    top = bpy.context.object
    top.name = "PREVIEW_TopMeadow_NotExported"
    top.data.materials.append(meadow_mat)


def render(path, camera_location, target, lens=54):
    bpy.ops.object.camera_add(location=camera_location)
    camera = bpy.context.object
    camera.name = "PREVIEW_Camera_NotExported"
    camera.data.lens = lens
    look_at(camera, target)
    bpy.context.scene.camera = camera

    bpy.ops.object.light_add(type="AREA", location=(-10, -13, HEIGHT + 13))
    key = bpy.context.object
    key.name = "PREVIEW_Key_NotExported"
    key.data.energy = 1300
    key.data.shape = "DISK"
    key.data.size = 10
    look_at(key, (0, 0, HALF_H))

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.display.shading.light = "STUDIO"
    scene.display.shading.color_type = "MATERIAL"
    scene.display.shading.show_shadows = True
    scene.display.shading.show_cavity = True
    scene.display.shading.cavity_type = "BOTH"
    scene.display.shading.curvature_ridge_factor = 1.6
    scene.display.shading.curvature_valley_factor = 1.2
    scene.render.resolution_x = 1100
    scene.render.resolution_y = 900
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.render.filepath = str(path)
    if scene.world is None:
        scene.world = bpy.data.worlds.new("PREVIEW_World_NotExported")
    scene.world.color = (0.055, 0.075, 0.085)
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(camera, do_unlink=True)
    bpy.data.objects.remove(key, do_unlink=True)


def bounds(objects):
    mins = Vector((math.inf, math.inf, math.inf))
    maxs = Vector((-math.inf, -math.inf, -math.inf))
    for obj in objects:
        for corner in obj.bound_box:
            point = obj.matrix_world @ Vector(corner)
            mins.x = min(mins.x, point.x)
            mins.y = min(mins.y, point.y)
            mins.z = min(mins.z, point.z)
            maxs.x = max(maxs.x, point.x)
            maxs.y = max(maxs.y, point.y)
            maxs.z = max(maxs.z, point.z)
    return mins, maxs


bpy.ops.wm.read_factory_settings(use_empty=True)
CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(CHECKPOINT))

grass = material("PinkHouse_WallGrass_Proof", (0.095, 0.34, 0.06), 0.94)
backing = material("PREVIEW_CliffBacking", (0.05, 0.17, 0.038), 1.0)
meadow = material("PREVIEW_Meadow", (0.13, 0.39, 0.08), 0.9)

quadrants = [
    make_quadrant(1, -HALF_W, 0, 0, HALF_H, 72101, grass),
    make_quadrant(2, 0, HALF_W, 0, HALF_H, 72203, grass),
    make_quadrant(3, -HALF_W, 0, HALF_H, HEIGHT, 72307, grass),
    make_quadrant(4, 0, HALF_W, HALF_H, HEIGHT, 72409, grass),
]
lip = make_lip(grass)
production = quadrants + [lip]
make_preview(backing, meadow)

audits = [audit_mesh(obj) for obj in production]
mins, maxs = bounds(production)

render(FRONT, (0, -34, HALF_H), (0, 0, HALF_H), 58)
render(OBLIQUE, (-24, -27, HEIGHT * 0.68), (0, 0, HALF_H), 55)
render(SIDE, (17, -7, HEIGHT * 0.48), (0, -0.35, HEIGHT * 0.48), 62)
render(LIP, (-15, -18, HEIGHT + 10), (0, 0, HEIGHT - 1.0), 60)

bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
bpy.ops.object.select_all(action="DESELECT")
for obj in production:
    obj.select_set(True)
bpy.context.view_layer.objects.active = production[0]
bpy.ops.export_scene.gltf(
    filepath=str(GLB),
    export_format="GLB",
    use_selection=True,
    export_apply=True,
    export_materials="EXPORT",
)

sha256 = hashlib.sha256(GLB.read_bytes()).hexdigest()
result = {
    "objects": len(production),
    "total_triangles": sum(item["triangles"] for item in audits),
    "max_triangles_per_mesh": max(item["triangles"] for item in audits),
    "bounds_metres": [round(value, 4) for value in (maxs - mins)],
    "bounds_studs": [round(value / STUD, 2) for value in (maxs - mins)],
    "blend": str(BLEND),
    "glb": str(GLB),
    "glb_bytes": GLB.stat().st_size,
    "glb_sha256": sha256,
    "meshes": audits,
}
print("WALL_GRASS_PROOF=" + json.dumps(result, sort_keys=True))
