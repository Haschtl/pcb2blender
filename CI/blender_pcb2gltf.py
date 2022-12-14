import bpy
import addon_utils
import sys, os
# import shutil
import zipfile

def pcb2gltf(pcb3d_path):
    # shutil.make_archive("pcb2blender_importer", 'zip', "./pcb2blender_importer")
    
    zf = zipfile.ZipFile("pcb2blender_importer.zip", "w")
    for dirname, subdirs, files in os.walk("./pcb2blender_importer"):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()
    bpy.ops.preferences.addon_install(filepath='./pcb2blender_importer.zip', overwrite=False)
    addon_utils.modules_refresh()
    addon_utils.enable("pcb2blender")

    bpy.ops.wm.read_homefile(use_empty=True)

    pcb3d_path=pcb3d_path.replace("\\","/")
    # bpy.ops.wm.read_factory_settings(use_empty=True)
    out_path = pcb3d_path.replace(".pcb3d", "")
    print(f"Importing {pcb3d_path} to blender")
    bpy.ops.pcb2blender.import_pcb3d(filepath=pcb3d_path)
    print(f"Exporting {out_path}.glb from blender")

    bpy.ops.export_scene.fbx(filepath=out_path+".fbx")
    bpy.ops.export_scene.obj(filepath=out_path+".obj")
    bpy.ops.export_scene.x3d(filepath=out_path+".x3d")
    bpy.ops.wm.save_as_mainfile(filepath=out_path+".blend")
    bpy.ops.pcb2blender.export_pcb_web(filepath=out_path+".glb")
    # bpy.ops.export_scene.gltf(
    #     filepath=gltf_path, export_copyright=export_copyright, export_draco_mesh_compression_enable, export_draco_mesh_compression_level)

    bpy.ops.wm.read_homefile(use_empty=True)
    bpy.ops.pcb2blender.import_pcb3d(filepath=pcb3d_path, pcb_material="RASTERIZED", enhance_materials=True)
    bpy.ops.wm.save_as_mainfile(filepath=out_path+"_HD.blend")

    bpy.ops.wm.read_homefile(use_empty=True)
    bpy.ops.pcb2blender.import_pcb3d(filepath=pcb3d_path, pcb_material="3D")
    bpy.ops.wm.save_as_mainfile(filepath=out_path+"_HD2.blend")

if __name__ == "__main__":
    pcb2gltf(sys.argv[4])

# You can only run this file if the plugin is installed in blender
# You need to run it with the packaged python from blender. Windows:
# & "C:\Program Files\Blender Foundation\Blender 3.3\blender.exe" --background --python .\blender_pcb2gltf.py <PATH_TO_PCB3D_FILE>
