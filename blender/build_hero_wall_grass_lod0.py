import bpy, random
from pathlib import Path

ROOT=Path('/Users/asal/Documents/roblox dev')
BLEND=ROOT/'blender'/'pink_house_hero_wall_grass_lod0.blend'
GLB=ROOT/'exports'/'pink_house_hero_wall_grass_lod0.glb'

bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
mat=bpy.data.materials.new('HeroWallGrass')
mat.diffuse_color=(0.075,0.30,0.055,1); mat.roughness=.92

def panel(idx,seed):
    rng=random.Random(seed); w,h=7.0,14.0
    vs=[]; fs=[]
    for _ in range(900):
        x=rng.uniform(-w/2,w/2); z=rng.uniform(-h/2,h/2)
        ln=rng.uniform(.45,1.65); bw=rng.uniform(.035,.105)
        out=rng.uniform(.22,.75); sx=rng.uniform(-.22,.22)
        b=len(vs)
        vs += [(x-bw,0,z+ln*.15),(x+bw,0,z+ln*.15),
               (x+bw*.45+sx*.4,out*.68,z-ln*.42),
               (x-bw*.45+sx*.4,out*.68,z-ln*.42),(x+sx,out,z-ln)]
        fs += [(b,b+1,b+2,b+3),(b+3,b+2,b+4)]
        # Crossed ribbon makes every blade volumetric from side angles.
        b=len(vs); cw=bw*.7
        vs += [(x,-cw,z+ln*.12),(x,cw,z+ln*.12),
               (x+sx*.35,out*.68+cw,z-ln*.42),
               (x+sx*.35,out*.68-cw,z-ln*.42),(x+sx,out,z-ln)]
        fs += [(b,b+1,b+2,b+3),(b+3,b+2,b+4)]
    me=bpy.data.meshes.new(f'HeroWallGrass_LOD0_{idx:02d}_Mesh')
    me.from_pydata(vs,[],fs); me.update()
    ob=bpy.data.objects.new(f'HeroWallGrass_LOD0_{idx:02d}',me)
    bpy.context.collection.objects.link(ob); ob.data.materials.append(mat)
    return ob

mods=[panel(i,9100+i*131) for i in range(1,5)]
bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
bpy.ops.object.select_all(action='DESELECT')
for o in mods:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(GLB),export_format='GLB',use_selection=True,
                          export_apply=True,export_materials='EXPORT')
for o in mods:o.data.calc_loop_triangles()
print({'modules':4,'triangles':sum(len(o.data.loop_triangles) for o in mods)})
