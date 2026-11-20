import bpy
import math
import os
import random
from mathutils import Vector


ROOT = "/Users/asal/Documents/roblox dev"
BLEND = os.path.join(ROOT, "blender", "pink_house_reference_v1.blend")
GLB = os.path.join(ROOT, "exports", "pink_house_reference_v1.glb")
PREVIEW = os.path.join(ROOT, "exports", "pink_house_reference_v1_preview.png")
STUD = 0.28


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def mat(name, color, roughness=0.7, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1.0)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return m


def cube(name, location, size, material, bevel=0.0, collection=None):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.data.name = name + "_mesh"
    obj.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    if bevel:
        mod = obj.modifiers.new("EdgeSoftening", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    if collection:
        for c in list(obj.users_collection):
            c.objects.unlink(obj)
        collection.objects.link(obj)
    return obj


def roof_prism(name, center, width, depth, wall_top, ridge_height, material, axis="Y", collection=None):
    # Closed gable prism. Ridge runs along local depth.
    w, d = width / 2, depth / 2
    verts = [
        (-w, -d, wall_top), (w, -d, wall_top), (0, -d, ridge_height),
        (-w, d, wall_top), (w, d, wall_top), (0, d, ridge_height),
    ]
    faces = [(0, 1, 2), (3, 5, 4), (0, 3, 4, 1), (0, 2, 5, 3), (1, 4, 5, 2)]
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    obj.location = center
    if axis == "X":
        obj.rotation_euler.z = math.radians(90)
    obj.data.materials.append(material)
    (collection or bpy.context.scene.collection).objects.link(obj)
    bevel = obj.modifiers.new("RoofEdgeSoftening", "BEVEL")
    bevel.width = 0.12
    bevel.segments = 2
    return obj


def window(name, location, size, facing, trim, glass, collection):
    x, y, z = location
    w, h = size
    if facing == "front":
        cube(name + "_Glass", (x, y, z), (w, 0.18, h), glass, 0.03, collection)
        cube(name + "_Top", (x, y - 0.12, z + h / 2), (w + .35, .28, .22), trim, 0.03, collection)
        cube(name + "_Bottom", (x, y - 0.12, z - h / 2), (w + .35, .28, .22), trim, 0.03, collection)
        for dx in (-w / 2, 0, w / 2):
            cube(name + "_V", (x + dx, y - .12, z), (.18, .28, h), trim, 0.02, collection)
        cube(name + "_H", (x, y - .12, z), (w, .28, .16), trim, 0.02, collection)
    else:
        cube(name + "_Glass", (x, y, z), (.18, w, h), glass, 0.03, collection)
        cube(name + "_Top", (x, y, z + h / 2), (.28, w + .35, .22), trim, 0.03, collection)
        cube(name + "_Bottom", (x, y, z - h / 2), (.28, w + .35, .22), trim, 0.03, collection)


def build():
    reset()
    house = bpy.data.collections.new("HOUSE_EXPORT")
    garden = bpy.data.collections.new("GARDEN_EXPORT")
    preview = bpy.data.collections.new("PREVIEW_ONLY")
    bpy.context.scene.collection.children.link(house)
    bpy.context.scene.collection.children.link(garden)
    bpy.context.scene.collection.children.link(preview)

    pink = mat("Pink_Plaster", (0.83, 0.43, 0.49), .78)
    pink2 = mat("Pink_Gable", (0.9, 0.55, 0.6), .72)
    roof = mat("Rose_Clay_Tiles", (0.58, 0.16, 0.2), .62)
    white = mat("Warm_White_Trim", (0.91, 0.88, 0.79), .68)
    glass = mat("Window_Glass", (0.25, 0.48, 0.55), .18, .05)
    wood = mat("Painted_Door", (0.38, 0.57, 0.53), .55)
    stone = mat("Foundation_Stone", (0.31, 0.3, 0.27), .9)
    green = mat("Garden_Green", (0.18, 0.38, 0.16), .9)
    green2 = mat("Garden_Light_Green", (0.34, 0.52, 0.22), .9)
    flower = mat("Garden_Flowers", (0.93, 0.75, 0.77), .7)

    # 44 x 29 m footprint ~= 157 x 104 studs. Single-storey silhouette.
    cube("StoneFoundation", (0, 0, 1.0), (43.5, 28.0, 2.0), stone, .35, house)
    cube("MainBody", (-4.5, 1.2, 6.6), (34.5, 25.0, 11.2), pink, .22, house)
    cube("FrontWing", (13.5, -5.5, 6.2), (13.0, 14.0, 10.4), pink2, .22, house)
    cube("RearWing", (-4.0, 11.2, 6.1), (17.0, 8.0, 10.2), pink, .22, house)

    roof_prism("MainCrossGableRoof", (-4.5, 1.2, 0), 38.0, 29.0, 12.0, 19.2, roof, "Y", house)
    roof_prism("FrontGableRoof", (13.5, -5.8, 0), 16.0, 18.5, 11.5, 17.0, roof, "Y", house)
    roof_prism("RearGableRoof", (-4.0, 11.0, 0), 11.5, 21.0, 11.2, 16.6, roof, "X", house)

    cube("Chimney", (-10.5, 5.8, 18.4), (3.0, 3.2, 9.0), stone, .12, house)
    cube("ChimneyCap", (-10.5, 5.8, 23.0), (3.8, 4.0, .7), stone, .08, house)

    # Front door, shallow tiled canopy and human-scale stairs.
    cube("FrontDoor", (13.5, -12.58, 6.0), (4.1, .35, 7.8), wood, .08, house)
    cube("DoorFrameTop", (13.5, -12.85, 10.0), (5.2, .5, .35), white, .04, house)
    for x in (10.95, 16.05):
        cube("DoorFrameSide", (x, -12.85, 6.0), (.35, .5, 8.2), white, .04, house)
    roof_prism("PorchCanopy", (13.5, -13.2, 0), 8.0, 5.5, 10.8, 13.1, roof, "Y", house)
    for i in range(4):
        cube(f"FrontStep_{i+1}", (13.5, -14.0 - i * 1.0, 1.9 - i * .38), (8.2 + i * .7, 2.0, .75), stone, .12, house)

    window("FrontWindowLeft", (-12.5, -11.35, 6.5), (5.8, 7.1), "front", white, glass, house)
    window("FrontWindowMid", (1.0, -11.35, 6.4), (5.0, 6.6), "front", white, glass, house)
    window("FrontWindowRight", (19.8, -5.5, 6.2), (4.8, 6.5), "side", white, glass, house)
    window("SideWindowLeft", (-21.85, 1.5, 6.2), (5.4, 6.8), "side", white, glass, house)

    # Garden is a separate importable collection so it can be culled/replaced.
    rng = random.Random(8117)
    for i in range(34):
        angle = math.tau * i / 34 + rng.uniform(-.09, .09)
        rx, ry = rng.uniform(24, 28), rng.uniform(17, 21)
        x, y = math.cos(angle) * rx, math.sin(angle) * ry
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1, location=(x, y, rng.uniform(1.1, 1.8)))
        o = bpy.context.object; o.name = f"Shrub_{i+1:02d}"
        o.data.name = o.name + "_mesh"
        o.scale = (rng.uniform(1.6, 3.2), rng.uniform(1.4, 2.7), rng.uniform(1.2, 2.5))
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        o.data.materials.append(green if i % 3 else green2)
        for c in list(o.users_collection): c.objects.unlink(o)
        garden.objects.link(o)
    for i in range(22):
        x = rng.choice((-1, 1)) * rng.uniform(8, 20)
        y = rng.uniform(-16.5, -12.8)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=rng.uniform(.22, .45), location=(x, y, rng.uniform(.45, .8)))
        o = bpy.context.object; o.name = f"Flower_{i+1:02d}"; o.data.materials.append(flower)
        o.data.name = o.name + "_mesh"
        for c in list(o.users_collection): c.objects.unlink(o)
        garden.objects.link(o)
    for i in range(30):
        angle = math.tau * i / 30 + rng.uniform(-.07, .07)
        x, y = math.cos(angle) * rng.uniform(27.5, 30), math.sin(angle) * rng.uniform(20, 22)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1, location=(x, y, .45))
        o = bpy.context.object; o.name = f"BorderStone_{i+1:02d}"
        o.data.name = o.name + "_mesh"
        o.scale = (rng.uniform(.65, 1.35), rng.uniform(.55, 1.1), rng.uniform(.35, .7))
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        o.data.materials.append(stone)
        for c in list(o.users_collection): c.objects.unlink(o)
        garden.objects.link(o)

    # Preview environment only; excluded from GLB.
    ground = cube("PreviewGround", (0, 0, -.35), (105, 85, .7), green2, 0, preview)
    bpy.ops.object.light_add(type="SUN", location=(25, -35, 55))
    sun = bpy.context.object; sun.name = "PreviewSun"; sun.data.energy = 3.0; sun.rotation_euler = (math.radians(28), math.radians(-18), math.radians(-28))
    for c in list(sun.users_collection): c.objects.unlink(sun)
    preview.objects.link(sun)
    bpy.ops.object.camera_add(location=(68, -82, 53))
    cam = bpy.context.object; cam.name = "PreviewCamera"; cam.data.lens = 52
    direction = Vector((0, 0, 8)) - cam.location
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = cam
    for c in list(cam.users_collection): c.objects.unlink(cam)
    preview.objects.link(cam)

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 1000; scene.render.resolution_y = 750; scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"; scene.render.filepath = PREVIEW
    scene.world = bpy.data.worlds.new("PreviewWorld")
    scene.world.color = (0.42, 0.56, 0.7)
    bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    bpy.ops.render.render(write_still=True)

    bpy.ops.object.select_all(action="DESELECT")
    for coll in (house, garden):
        for obj in coll.objects:
            if obj.type == "MESH": obj.select_set(True)
    bpy.ops.export_scene.gltf(filepath=GLB, export_format="GLB", use_selection=True, export_apply=True, export_yup=True, export_materials="EXPORT")
    print({"blend": BLEND, "glb": GLB, "preview": PREVIEW, "house_objects": len(house.objects), "garden_objects": len(garden.objects)})


build()
