import bpy
import json
import math
import sys


path = sys.argv[sys.argv.index("--") + 1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=path)

depsgraph = bpy.context.evaluated_depsgraph_get()
meshes = []
mins = [math.inf, math.inf, math.inf]
maxs = [-math.inf, -math.inf, -math.inf]

for obj in sorted((item for item in bpy.context.scene.objects if item.type == "MESH"), key=lambda item: item.name):
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    mesh.calc_loop_triangles()
    meshes.append(
        {
            "name": obj.name,
            "vertices": len(mesh.vertices),
            "triangles": len(mesh.loop_triangles),
            "materials": [slot.material.name for slot in obj.material_slots if slot.material],
        }
    )
    for corner in obj.bound_box:
        world = obj.matrix_world @ __import__("mathutils").Vector(corner)
        for axis in range(3):
            mins[axis] = min(mins[axis], world[axis])
            maxs[axis] = max(maxs[axis], world[axis])
    evaluated.to_mesh_clear()

result = {
    "path": path,
    "mesh_count": len(meshes),
    "total_triangles": sum(item["triangles"] for item in meshes),
    "max_triangles_per_mesh": max((item["triangles"] for item in meshes), default=0),
    "bounds_metres": [round(maxs[i] - mins[i], 4) for i in range(3)],
    "bounds_studs_at_0_28m": [round((maxs[i] - mins[i]) / 0.28, 2) for i in range(3)],
    "meshes": meshes,
}
print("GLB_VALIDATION=" + json.dumps(result, sort_keys=True))
