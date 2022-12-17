import bpy
import addon_utils
import sys, os
# import shutil
import zipfile

def pcb2gltf(pcb3d_path, install=False):
    # shutil.make_archive("pcb2blender_importer", 'zip', "./pcb2blender_importer")
    if install:
            zf = zipfile.ZipFile("pcb2blender_importer.zip", "w")
            for dirname, subdirs, files in os.walk("./pcb2blender_importer"):
                zf.write(dirname)
                for filename in files:
                    zf.write(os.path.join(dirname, filename))
            zf.close()
            bpy.ops.preferences.addon_install(filepath='./pcb2blender_importer.zip', overwrite=False)
            addon_utils.modules_refresh()
    addon_utils.enable("pcb2blender")

    pcb3d_path=pcb3d_path.replace("\\","/")
    out_dir, filename = os.path.split(pcb3d_path)
    out_dir = os.path.join(out_dir, "exports")
    # bpy.ops.wm.read_factory_settings(use_empty=True)
    out_path = os.path.join(out_dir, filename.replace(".pcb3d", ""))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # export_web(out_path, pcb3d_path)
    # export_without_components(out_path, pcb3d_path)
    export_blender(out_path, pcb3d_path)
    
    
def export_blender(out_path, pcb3d_path):
    print(f"Exporting BLENDER in RASTERIZED mode to {pcb3d_path}")
    bpy.ops.wm.read_homefile(use_empty=True)
    bpy.ops.pcb2blender.import_pcb3d(filepath=pcb3d_path, pcb_material="RASTERIZED", enhance_materials=True, custom_material="White")
    bpy.ops.wm.save_as_mainfile(filepath=pcb3d_path.replace(".pcb3d","_RASTERIZED.blend"))

    print(f"Exporting BLENDER in 3D mode to {pcb3d_path}")
    bpy.ops.wm.read_homefile(use_empty=True)
    bpy.ops.pcb2blender.import_pcb3d(filepath=pcb3d_path, pcb_material="3D")
    bpy.ops.wm.save_as_mainfile(filepath=pcb3d_path.replace(".pcb3d","_3D.blend"))

def export_web(out_path, pcb3d_path):
    print(f"Exporting multiple web-compatible formats to {out_path}")
    bpy.ops.wm.read_homefile(use_empty=True)
    bpy.ops.pcb2blender.import_pcb3d(filepath=pcb3d_path)
    bpy.ops.wm.save_as_mainfile(
        filepath=pcb3d_path.replace(".pcb3d", ".blend"))
    multi_export(out_path)

def export_without_components(out_path, pcb3d_path):
    print(f"Exporting GLTF without components to {out_path}")
    bpy.ops.wm.read_homefile(use_empty=True)
    bpy.ops.pcb2blender.import_pcb3d(
        filepath=pcb3d_path, import_components=False)
    bpy.ops.export_scene.gltf(
        filepath=out_path+"_no_texture_components.glb", export_copyright="pcb2blender", export_draco_mesh_compression_enable=True, export_draco_mesh_compression_level=6, export_colors=False, export_texcoords=False, export_materials="NONE", export_yup=True)
    bpy.ops.export_scene.gltf(
        filepath=out_path+"_no_components.glb", export_copyright="pcb2blender", export_draco_mesh_compression_enable=True, export_draco_mesh_compression_level=6, export_colors=False, export_yup=True)


def multi_export(out_path):
    bpy.ops.export_scene.gltf(
        filepath=out_path+"_no_texture.glb", export_copyright="pcb2blender", export_draco_mesh_compression_enable=True, export_draco_mesh_compression_level=6, export_colors=False, export_texcoords=False, export_materials="NONE", export_yup=True)
    bpy.ops.export_scene.fbx(filepath=out_path+".fbx")
    bpy.ops.export_scene.obj(filepath=out_path+".obj")
    bpy.ops.export_scene.x3d(filepath=out_path+".x3d")
    bpy.ops.pcb2blender.export_pcb_web(filepath=out_path+".glb")


if __name__ == "__main__":
    pcb2gltf(sys.argv[4])

# You can only run this file if the plugin is installed in blender
# You need to run it with the packaged python from blender. Windows:
# & "C:\Program Files\Blender Foundation\Blender 3.3\blender.exe" --background --python .\blender_pcb2gltf.py <PATH_TO_PCB3D_FILE>
