import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import *
import bmesh
from glob import glob
import os
from pathlib import Path


from .layers2texture import layers2texture
from .shared import openPCB3D
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
    create_pcb: BoolProperty(name="Create PCB mesh from Edge_Cut layer", default=True)

    def __init__(self):
        super().__init__()

    def execute(self, context):

        filepath = Path(self.filepath)
        # out_dir = os.path.join(str(filepath).replace(".pcb3d", ""), "layers")
        texture_dir = str(filepath).replace(".pcb3d", "")

        self.execute_optional()

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
        ob = bpy.context.active_object
        ob.data.materials.clear()
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
            material = {}
            material['cancel'] = False
            material['alpha'] = False
            material_name = group+"_material"

            new_mat = bpy.data.materials.get(material_name)
            if not new_mat:
                new_mat = bpy.data.materials.new(material_name)

            if material['alpha'] == True:
                new_mat.blend_method = 'BLEND'

            new_mat.use_nodes = True
            node_tree = new_mat.node_tree

            nodes = node_tree.nodes
            nodes.clear()

            links = node_tree.links
            links.clear()
            master_node = nodes.new(type='ShaderNodeBsdfPrincipled')
            for file in groups[group]:
                if material['cancel'] == False:
                    # Begin constructing node tree for this material
                    if 'base_color' in file:
                        print(f"Adding base color: {file}")
                        bt_node = nodes.new(type='ShaderNodeTexImage')
                        bt_node.image = bpy.data.images.load(file)
                        links.new(
                            master_node.inputs['Base Color'], bt_node.outputs['Color'])
                        links.new(
                            master_node.inputs['Alpha'], bt_node.outputs['Alpha'])

                    if 'metal' in file:
                        print(f"Adding Metallic: {file}")
                        bt_node = nodes.new(type='ShaderNodeTexImage')
                        bt_node.image = bpy.data.images.load(file)
                        links.new(
                            master_node.inputs['Metallic'], bt_node.outputs['Color'])

                    if 'specular' in file:
                        print(f"Adding Specular: {file}")
                        bt_node = nodes.new(type='ShaderNodeTexImage')
                        bt_node.image = bpy.data.images.load(file)
                        links.new(
                            master_node.inputs['Specular'], bt_node.outputs['Color'])

                    if 'roughness' in file:
                        print(f"Adding Roughness: {file}")
                        bt_node = nodes.new(type='ShaderNodeTexImage')
                        bt_node.image = bpy.data.images.load(file)
                        links.new(
                            master_node.inputs['Roughness'], bt_node.outputs['Color'])

                    if 'emissive' in file:
                        print(f"Adding Emissive: {file}")
                        bt_node = nodes.new(type='ShaderNodeTexImage')
                        bt_node.image = bpy.data.images.load(file)
                        links.new(
                            master_node.inputs['Emission'], bt_node.outputs['Color'])

                    if 'normal' in file:
                        print(f"Adding Normal: {file}")
                        bmi_node = nodes.new(type='ShaderNodeTexImage')
                        bmi_node.image = bpy.data.images.load(file)
                        # bm_node = nodes.new(type='ShaderNodeBump')

                        # links.new(bm_node.inputs['Height'],
                        #         bt_node.outputs['Color'])
                        links.new(
                            master_node.inputs['Normal'], bmi_node.outputs['Color'])

            out_node = nodes.new(type='ShaderNodeOutputMaterial')

            links.new(master_node.outputs['BSDF'], out_node.inputs[0])

            # Assign it to object
            # if ob.data.materials:
            #     # assign to 1st material slot
            #     ob.data.materials[0] = new_mat
            # else:
            #     # no slots
            ob.data.materials.append(new_mat)
            # out_file = os.path.join(maps_dir, material_name+".blend")
            # print(f'Saving {out_file}')

            # bpy.ops.file.pack_all()  # Tells blender to pack images into the file on save

            # data_blocks = {*bpy.data.materials, *
            #             bpy.data.textures, *bpy.data.node_groups}
            # print(bpy.data.materials['F_material'])
            # # data_blocks = {new_mat}

            # bpy.data.libraries.write(out_file, data_blocks, compress=True)
            # bpy.ops.file.unpack_all()  # Tells blender not to pack images into the file on save


# classes = (
#     PCB2BLENDER_OT_import_pcb3d_texture,
# )

def menu_func_import_pcb3d_texture(self, context):
    self.layout.operator(
        PCB2BLENDER_OT_import_pcb3d_texture.bl_idname, text="PCB-Texture (.pcb3d)")


# def register():
#     bpy.utils.register_class(PCB2BLENDER_OT_import_pcb3d_texture)
#     bpy.types.TOPBAR_MT_file_import.append(menu_func_import_pcb3d_texture)


# def unregister():
#     bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_pcb3d_texture)
#     bpy.utils.unregister_class(PCB2BLENDER_OT_import_pcb3d_texture)
