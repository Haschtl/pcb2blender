import bpy
import sys


def pcb2gltf(pcb3d_path, export_copyright="", export_draco_mesh_compression_enable=True, export_draco_mesh_compression_level=6):
    pcb3d_path=pcb3d_path.replace("\\","/")
    # bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.wm.read_homefile(use_empty=True)
    gltf_path = pcb3d_path.replace(".pcb3d",".glb")
    print(f"Importing {pcb3d_path} to blender")
    bpy.ops.pcb2blender.import_pcb3d(filepath=pcb3d_path)
    print(f"Exporting {gltf_path} from blender")
    bpy.ops.pcb2blender.export_pcb_web(filepath=gltf_path)
    # bpy.ops.export_scene.gltf(
    #     filepath=gltf_path, export_copyright=export_copyright, export_draco_mesh_compression_enable, export_draco_mesh_compression_level)


if __name__ == "__main__":
    pcb2gltf(sys.argv[4])
