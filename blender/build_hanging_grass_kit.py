import bpy
import math
import random
from pathlib import Path
from mathutils import Vector

ROOT = Path('/Users/asal/Documents/roblox dev')
BLEND = ROOT / 'blender' / 'pink_house_hanging_grass_v1.blend'
GLB = ROOT / 'exports' / 'pink_house_hanging_grass_v1.glb'
PREVIEW = ROOT / 'exports' / 'pink_house_hanging_grass_v1_preview.png'

random.seed(24017)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

mat = bpy.data.materials.new('Grass_Foliage')
mat.diffuse_color = (0.055, 0.22, 0.065, 1.0)
mat.metallic = 0.0
mat.roughness = 0.88

def ribbon_mesh(name, x, depth, length, width, lean, wave, segments=5):
    verts = []
    faces = []
    for i in range(segments + 1):
        t = i / segments
        y = depth + math.sin(t * math.pi * 1.7) * wave + lean * t
        z = -length * t
        taper = max(0.08, 1.0 - t * 0.88)
        half = width * taper * 0.5
        verts.extend([(x-half, y, z), (x+half, y, z)])
    for i in range(segments):
        a = i * 2
        faces.append((a, a+1, a+3, a+2))
    mesh = bpy.data.meshes.new(name + '_Mesh')
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    obj.data.materials.append(mat)
    return obj

def make_cluster(index, long_form):
    coll = bpy.data.collections.new(f'GrassModule_{index:02d}_Parts')
    bpy.context.scene.collection.children.link(coll)
    blades = 18 if long_form else 24
    span = random.uniform(4.8, 7.2)
    objects = []
    for j in range(blades):
        x = -span/2 + span * (j/(blades-1)) + random.uniform(-0.18, 0.18)
        if long_form:
            length = random.uniform(7.0, 19.0) * (0.75 + 0.25 * math.sin(j * 1.73)**2)
            width = random.uniform(0.22, 0.48)
            depth = random.uniform(-0.25, 0.35)
            lean = random.uniform(-0.5, 1.25)
            wave = random.uniform(0.12, 0.55)
        else:
            length = random.uniform(1.6, 4.8)
            width = random.uniform(0.16, 0.38)
            depth = random.uniform(-0.18, 0.25)
            lean = random.uniform(-0.35, 0.65)
            wave = random.uniform(0.08, 0.3)
        obj = ribbon_mesh(f'Blade_{index:02d}_{j:02d}', x, depth, length, width, lean, wave)
        coll.objects.link(obj)
        objects.append(obj)
    # Join each cluster into one reusable MeshPart.
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.join()
    cluster = objects[0]
    cluster.name = f'HangingGrass_{"Long" if long_form else "Edge"}_{index:02d}'
    cluster.data.name = cluster.name + '_Mesh'
    # Add a narrow top mat so the blades visually grow from the lip.
    top = ribbon_mesh(f'TopLip_{index:02d}', 0, -0.05, 0.55, span, 0.18, 0.05, 2)
    coll.objects.link(top)
    bpy.ops.object.select_all(action='DESELECT')
    cluster.select_set(True)
    top.select_set(True)
    bpy.context.view_layer.objects.active = cluster
    bpy.ops.object.join()
    cluster = bpy.context.object
    # Lay variants out only for preview; origin remains at attachment lip.
    col = (index - 1) % 4
    row = (index - 1) // 4
    cluster.location = ((col - 1.5) * 10.0, row * 5.0, 0)
    return cluster

mods = []
for i in range(1, 9):
    mods.append(make_cluster(i, long_form=i <= 4))

# Ground strip for preview only.
bpy.ops.mesh.primitive_cube_add(location=(0, 2.7, 0.45), scale=(21, 2.4, 0.45))
ground = bpy.context.object
ground.name = 'PREVIEW_Ground_NotExported'
gmat = bpy.data.materials.new('PreviewGround')
gmat.diffuse_color = (0.11, 0.18, 0.08, 1)
gmat.roughness = 1.0
ground.data.materials.append(gmat)

# Camera and soft lighting.
bpy.ops.object.camera_add(location=(0, -38, -2))
cam = bpy.context.object
cam.name = 'PREVIEW_Camera_NotExported'
bpy.context.scene.camera = cam
def point_camera(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()
point_camera(cam, (0, 1, -6))
cam.data.lens = 54
bpy.ops.object.light_add(type='AREA', location=(-14, -12, 14))
key = bpy.context.object
key.name = 'PREVIEW_Key_NotExported'
key.data.energy = 1700
key.data.shape = 'DISK'
key.data.size = 12
point_camera(key, (0, 0, -5))
bpy.ops.object.light_add(type='AREA', location=(15, -3, 3))
fill = bpy.context.object
fill.name = 'PREVIEW_Fill_NotExported'
fill.data.energy = 900
fill.data.size = 10
point_camera(fill, (0, 0, -7))

scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1400
scene.render.resolution_y = 900
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = str(PREVIEW)
scene.world.color = (0.04, 0.055, 0.07)
bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
bpy.ops.render.render(write_still=True)

# Export production modules only, reset layout so every module has an attachment origin.
bpy.ops.object.select_all(action='DESELECT')
for o in mods:
    o.location = (0, 0, 0)
    o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(GLB), export_format='GLB', use_selection=True,
                          export_apply=True, export_materials='EXPORT')
print({'blend': str(BLEND), 'glb': str(GLB), 'preview': str(PREVIEW),
       'modules': len(mods), 'triangles': sum(len(o.data.loop_triangles) for o in mods)})
