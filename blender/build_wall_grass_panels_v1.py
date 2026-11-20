import bpy
import math
import random
from pathlib import Path
from mathutils import Vector

ROOT = Path('/Users/asal/Documents/roblox dev')
BLEND = ROOT / 'blender' / 'pink_house_wall_grass_panels_v1.blend'
GLB = ROOT / 'exports' / 'pink_house_wall_grass_panels_v1.glb'
PREVIEW = ROOT / 'exports' / 'pink_house_wall_grass_panels_v1_preview.png'

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

mat = bpy.data.materials.new('WallGrass_Foliage')
mat.diffuse_color = (0.10, 0.34, 0.075, 1.0)
mat.metallic = 0.0
mat.roughness = 0.9

def make_panel(index, seed):
    rng = random.Random(seed)
    width, height = 28.0, 56.0  # 100 x 200 studs at 0.28 m/stud
    verts, faces = [], []
    # Dense but low-poly blades rooted across the full vertical wall plane.
    for i in range(650):
        x = rng.uniform(-width * 0.5, width * 0.5)
        z = rng.uniform(-height * 0.5, height * 0.5)
        length = rng.uniform(1.0, 3.8)
        blade_w = rng.uniform(0.08, 0.23)
        out = rng.uniform(0.35, 1.35)
        side = rng.uniform(-0.55, 0.55)
        # Four points: broad root on wall, bent middle, narrow hanging tip.
        base = len(verts)
        verts.extend([
            (x-blade_w, 0.0, z+length*0.18),
            (x+blade_w, 0.0, z+length*0.18),
            (x+blade_w*0.55+side*0.35, out*0.75, z-length*0.42),
            (x-blade_w*0.55+side*0.35, out*0.75, z-length*0.42),
            (x+side, out, z-length),
        ])
        faces.append((base, base+1, base+2, base+3))
        faces.append((base+3, base+2, base+4))
        # A crossed card gives depth from oblique gameplay views.
        cross_w = blade_w * 0.7
        base = len(verts)
        verts.extend([
            (x, -cross_w, z+length*0.12),
            (x, cross_w, z+length*0.12),
            (x+side*0.35, out*0.72+cross_w, z-length*0.42),
            (x+side*0.35, out*0.72-cross_w, z-length*0.42),
            (x+side, out, z-length),
        ])
        faces.append((base, base+1, base+2, base+3))
        faces.append((base+3, base+2, base+4))
    mesh = bpy.data.meshes.new(f'WallGrassPanel_{index:02d}_Mesh')
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(f'WallGrassPanel_{index:02d}', mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    obj.location.x = (index - 2.5) * 31.0
    return obj

panels = [make_panel(i, 6300+i*101) for i in range(1, 5)]

# Preview wall and camera.
bpy.ops.mesh.primitive_cube_add(location=(0, -0.7, 0), scale=(63, 0.6, 29))
wall = bpy.context.object
wall.name = 'PREVIEW_Wall_NotExported'
wmat = bpy.data.materials.new('PreviewWall')
wmat.diffuse_color = (0.035, 0.09, 0.03, 1)
wall.data.materials.append(wmat)

bpy.ops.object.camera_add(location=(0, 58, 3))
cam = bpy.context.object
cam.name = 'PREVIEW_Camera_NotExported'
bpy.context.scene.camera = cam
cam.rotation_euler = ((Vector((0, 0, -2)) - cam.location).to_track_quat('-Z', 'Y').to_euler())
cam.data.lens = 52
bpy.ops.object.light_add(type='AREA', location=(-30, 25, 38))
key = bpy.context.object
key.name = 'PREVIEW_Key_NotExported'
key.data.energy = 1900
key.data.size = 25
key.rotation_euler = ((Vector((0, 0, 0)) - key.location).to_track_quat('-Z', 'Y').to_euler())

scene = bpy.context.scene
scene.render.engine = 'BLENDER_WORKBENCH'
scene.display.shading.light = 'STUDIO'
scene.display.shading.color_type = 'MATERIAL'
scene.display.shading.show_shadows = True
scene.render.resolution_x = 1500
scene.render.resolution_y = 850
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = str(PREVIEW)
scene.world.color = (0.025, 0.04, 0.05)
bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
bpy.ops.render.render(write_still=True)

bpy.ops.object.select_all(action='DESELECT')
for p in panels:
    p.location = (0, 0, 0)
    p.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(GLB), export_format='GLB', use_selection=True,
                          export_apply=True, export_materials='EXPORT')
for p in panels:
    p.data.calc_loop_triangles()
print({'modules': len(panels),
       'triangles': sum(len(p.data.loop_triangles) for p in panels),
       'blend': str(BLEND), 'glb': str(GLB), 'preview': str(PREVIEW)})
