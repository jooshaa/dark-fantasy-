import bpy
import math
import random
from pathlib import Path
from mathutils import Vector

ROOT = Path('/Users/asal/Documents/roblox dev')
BLEND = ROOT / 'blender' / 'pink_house_cliff_grass_shell_v3.blend'
GLB = ROOT / 'exports' / 'pink_house_cliff_grass_shell_v3.glb'
PREVIEW_FRONT = ROOT / 'exports' / 'pink_house_cliff_grass_shell_v3_front.png'
PREVIEW_OBLIQUE = ROOT / 'exports' / 'pink_house_cliff_grass_shell_v3_oblique.png'

STUD = 0.28
WIDTH = 1400 * STUD
HEIGHT = 1000 * STUD
DEPTH = 620 * STUD
CHASM = 25 * STUD
FRONT_MODULES = 8
CHASM_MODULES = 4
OUTER_MODULES = 4
BLADES_PER_FRONT = 2500
BLADES_PER_CHASM = 2200
BLADES_PER_OUTER = 2200

bpy.ops.wm.read_factory_settings(use_empty=True)

grass = bpy.data.materials.new('PinkHouse_CliffGrass_v3')
grass.diffuse_color = (0.075, 0.23, 0.055, 1.0)
grass.metallic = 0.0
grass.roughness = 0.96

backing = bpy.data.materials.new('PinkHouse_CliffBacking_v3')
backing.diffuse_color = (0.035, 0.095, 0.035, 1.0)
backing.metallic = 0.0
backing.roughness = 1.0


def make_blade(verts, faces, root, normal, tangent, seed, top_factor):
    rng = random.Random(seed)
    # Reference reads as fine, mostly vertical hanging fibres. Longer strands
    # cluster near the upper third, with restrained projection from the wall.
    length = rng.uniform(1.8, 6.5) * (0.80 + 0.35 * top_factor)
    width = rng.uniform(0.055, 0.16)
    outward = rng.uniform(0.18, 0.85)
    side = rng.uniform(-0.7, 0.7)
    droop = Vector((0, 0, -1))
    root_l = root - tangent * width
    root_r = root + tangent * width
    mid = root + normal * outward * 0.7 + tangent * side * 0.35 + droop * length * 0.43
    tip = root + normal * outward + tangent * side + droop * length
    base = len(verts)
    verts.extend((root_l, root_r, mid + tangent * width * 0.48,
                  mid - tangent * width * 0.48, tip))
    faces.extend(((base, base + 1, base + 2, base + 3),
                  (base + 3, base + 2, base + 4)))


def create_mesh(name, verts, faces, mat, tags):
    mesh = bpy.data.meshes.new(name + '_Mesh')
    mesh.from_pydata(verts, [], faces)
    mesh.update(calc_edges=True)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    for key, value in tags.items():
        obj[key] = value
    return obj


def front_panel(index):
    usable = WIDTH - CHASM
    module_w = usable / FRONT_MODULES
    if index < FRONT_MODULES // 2:
        x0 = -WIDTH / 2 + index * module_w
    else:
        x0 = CHASM / 2 + (index - FRONT_MODULES // 2) * module_w
    rng = random.Random(31000 + index * 977)
    verts, faces = [], []
    for i in range(BLADES_PER_FRONT):
        x = x0 + rng.random() * module_w
        z = rng.random() * HEIGHT
        # Tiny depth breakup removes the flat-card read without creating shelves.
        y = (-DEPTH / 2 - 0.7
             + math.sin(x * 0.071 + z * 0.017) * 0.35
             + rng.uniform(-0.22, 0.22))
        root = Vector((x, y, z))
        make_blade(verts, faces, root, Vector((0, -1, 0)), Vector((1, 0, 0)),
                   810000 + index * 10000 + i, z / HEIGHT)
    return create_mesh(f'FrontGrass_{index + 1:02d}', verts, faces, grass,
                       {'surface': 'front', 'module': index + 1})


def chasm_panel(side, index):
    module_d = DEPTH / CHASM_MODULES
    y0 = index * module_d
    x = side * CHASM / 2
    rng = random.Random(52000 + (1 if side > 0 else 2) * 1000 + index * 431)
    verts, faces = [], []
    normal = Vector((-side, 0, 0))
    tangent = Vector((0, 1, 0))
    for i in range(BLADES_PER_CHASM):
        y = y0 + rng.random() * module_d
        z = rng.random() * HEIGHT
        px = x - side * (0.45 + math.sin(y * 0.055 + z * 0.021) * 0.22 + rng.uniform(-0.15, 0.15))
        root = Vector((px, y, z))
        make_blade(verts, faces, root, normal, tangent,
                   920000 + (100000 if side > 0 else 200000) + index * 10000 + i,
                   z / HEIGHT)
    label = 'Right' if side > 0 else 'Left'
    return create_mesh(f'Chasm{label}Grass_{index + 1:02d}', verts, faces, grass,
                       {'surface': 'chasm', 'side': label, 'module': index + 1})


def outer_panel(side, index):
    module_d = DEPTH / OUTER_MODULES
    y0 = index * module_d
    x = side * WIDTH / 2
    rng = random.Random(73000 + (1 if side > 0 else 2) * 1000 + index * 613)
    verts, faces = [], []
    normal = Vector((side, 0, 0))
    tangent = Vector((0, 1, 0))
    for i in range(BLADES_PER_OUTER):
        y = y0 + rng.random() * module_d
        z = rng.random() * HEIGHT
        px = x + side * (0.65 + math.sin(y * 0.049 + z * 0.018) * 0.30 + rng.uniform(-0.18, 0.18))
        make_blade(verts, faces, Vector((px, y, z)), normal, tangent,
                   1030000 + (100000 if side > 0 else 200000) + index * 10000 + i,
                   z / HEIGHT)
    label = 'Right' if side > 0 else 'Left'
    return create_mesh(f'Outer{label}Grass_{index + 1:02d}', verts, faces, grass,
                       {'surface': 'outer', 'side': label, 'module': index + 1})


production = [front_panel(i) for i in range(FRONT_MODULES)]
for side in (-1, 1):
    production.extend(chasm_panel(side, i) for i in range(CHASM_MODULES))
    production.extend(outer_panel(side, i) for i in range(OUTER_MODULES))

# Preview-only dark monolith faces make silhouette and seams readable.
def cube(name, loc, scale):
    bpy.ops.mesh.primitive_cube_add(location=loc, scale=scale)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(backing)
    return obj

left_w = (WIDTH - CHASM) / 2
cube('PREVIEW_LeftCore', (-CHASM / 2 - left_w / 2, 0, HEIGHT / 2),
     (left_w / 2, DEPTH / 2, HEIGHT / 2))
cube('PREVIEW_RightCore', (CHASM / 2 + left_w / 2, 0, HEIGHT / 2),
     (left_w / 2, DEPTH / 2, HEIGHT / 2))

def render(path, camera_pos, target):
    bpy.ops.object.camera_add(location=camera_pos)
    cam = bpy.context.object
    cam.name = 'PREVIEW_Camera'
    cam.rotation_euler = (Vector(target) - cam.location).to_track_quat('-Z', 'Y').to_euler()
    cam.data.lens = 56
    bpy.context.scene.camera = cam
    bpy.ops.object.light_add(type='SUN', location=(0, -100, HEIGHT * 1.4))
    sun = bpy.context.object
    sun.rotation_euler = (math.radians(32), math.radians(-18), math.radians(-25))
    sun.data.energy = 2.2
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_WORKBENCH'
    scene.display.shading.light = 'STUDIO'
    scene.display.shading.color_type = 'MATERIAL'
    scene.display.shading.show_shadows = True
    scene.render.resolution_x = 900
    scene.render.resolution_y = 900
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam, do_unlink=True)
    bpy.data.objects.remove(sun, do_unlink=True)

render(PREVIEW_FRONT, (0, -620, HEIGHT * 0.48), (0, 0, HEIGHT * 0.5))
render(PREVIEW_OBLIQUE, (-520, -520, HEIGHT * 0.78), (0, 30, HEIGHT * 0.48))

bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
bpy.ops.object.select_all(action='DESELECT')
for obj in production:
    obj.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(GLB), export_format='GLB', use_selection=True,
                          export_apply=True, export_materials='EXPORT')

triangles = 0
max_triangles = 0
for obj in production:
    obj.data.calc_loop_triangles()
    count = len(obj.data.loop_triangles)
    triangles += count
    max_triangles = max(max_triangles, count)
print({'objects': len(production), 'triangles': triangles,
       'max_triangles': max_triangles, 'blend': str(BLEND), 'glb': str(GLB)})
