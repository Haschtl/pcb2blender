import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import *
import bmesh
from glob import glob
import os
from pathlib import Path


from .uv_creator.layers2texture import layers2texture
from .uv_creator.shared import openPCB3D
from .materials import setup_pcb_eevee_material
counter = 0


class PCB2BLENDER_OT_import_pcb3d_texture(bpy.types.Operator, ImportHelper):
    """Import texture from PCB3D file"""
    bl_idname = "pcb2blender.import_pcb3d_texture"
    bl_label = "Import Texture from .pcb3d"
    bl_options = {"PRESET", "UNDO"}

    pcb_material:      EnumProperty(name="PCB Material", default="Green",
                                    items=(("Green", "Green", ""), ("Red", "Red", ""), ("Blue", "Blue", ""), ("White", "White", ""), ("Black", "Black", "")))
    texture_dpi:       FloatProperty(name="Texture DPI",
                                     default=1016.0, soft_min=508.0, soft_max=2032.0)
    use_existing: BoolProperty(name="Use existing textures", default=True)
    create_pcb: BoolProperty(
        name="Create PCB mesh from Edge_Cut layer", default=False)

    def __init__(self):
        super().__init__()

    def execute(self, context):

        filepath = Path(self.filepath)
        # out_dir = os.path.join(str(filepath).replace(".pcb3d", ""), "layers")
        texture_dir = str(filepath).replace(".pcb3d", "")

        tempdir, pcb3d_layers = openPCB3D(filepath)
        edges_path = os.path.join(tempdir, "Edge_Cuts.svg")
        if os.path.isfile(edges_path) and self.create_pcb:
            self.create_pcb_mesh(str(filepath))
        else:
            print("Cant create Mesh. File {edges_path} does not exist.")

        if not self.use_existing or not os.path.isfile(os.path.join(texture_dir, "base_color.png")):
            self.create_texture(str(filepath))
        else:
            print("Did not create new texture. Using existing ones")

        self.create_blender_material(texture_dir)

        return {"FINISHED"}

    def create_pcb_mesh(self, svg_path: str):
        bpy.ops.import_curve.svg(filepath=svg_path)

        bpy.ops.curve.primitive_bezier_circle_add()
        path = bpy.context.object
        print('Path: {path.type}')

        dg = bpy.context.evaluated_depsgraph_get()
        path = path.evaluated_get(dg)

        mesh = path.to_mesh()
        print(mesh)

        o = bpy.data.objects.new("pcb", mesh.copy())
        bpy.context.scene.collection.objects.link(o)

    def create_texture(self, pcb3d_path: str):
        wm = bpy.context.window_manager
        tot = 2*10
        wm.progress_begin(0, tot)
        wm.progress_end()
        global counter
        counter = 0

        def update_progress():
            global counter
            counter += 1
            wm.progress_update(counter)
        # update_progress = lambda: wm.progress_update(i)
        layers2texture(pcb3d_path, self.texture_dpi,
                       self.pcb_material, True, update_progress)

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.label(text="PCB Material")
        col.prop(self, "pcb_material", text="")
        col.prop(self, "texture_dpi", slider=True)
        layout.split()

        col2 = layout.column()
        col2.label(text="Use existing textures")
        col2.prop(self, "use_existing")
        col2.label(text="Create PCB Mesh from Edges_Cut layer")
        col2.prop(self, "create_pcb")

    def create_blender_material(self, maps_dir: str):
        pcb_object = bpy.context.active_object
        pcb_object.data.materials.clear()
        print("Creating blender materials")
        layer_paths = list(
            glob(os.path.join(maps_dir, '*.png'), recursive=False))
        # groups: Dict[str, List[str]] = {}
        groups = {}
        for path in sorted(layer_paths, reverse=True):
            n_split = os.path.split(path)[1].split("_")
            if len(n_split) == 1 or n_split[0] == "base":
                group_name = "merged"
            else:
                group_name = n_split[0]
            if group_name in groups:
                groups[group_name].append(path)
            else:
                groups[group_name] = [path]

        for group in groups:

            print(f"Creating material for {group}")
            new_mat = setup_pcb_eevee_material(
                group+"_material", groups[group])
            # Assign it to object
            # if pcb_object.data.materials:
            #     # assign to 1st material slot
            #     pcb_object.data.materials[0] = new_mat
            # else:
            #     # no slots
            pcb_object.data.materials.append(new_mat)

def menu_func_import_pcb3d_texture(self, context):
    self.layout.operator(
        PCB2BLENDER_OT_import_pcb3d_texture.bl_idname, text="PCB-Texture (.pcb3d)")


def register():
    bpy.utils.register_class(PCB2BLENDER_OT_import_pcb3d_texture)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_pcb3d_texture)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_pcb3d_texture)
    bpy.utils.unregister_class(PCB2BLENDER_OT_import_pcb3d_texture)
