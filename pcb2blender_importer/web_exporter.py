import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import *
import bmesh


class PCB2BLENDER_OT_export_pcb_web(bpy.types.Operator, ImportHelper):
    """Export GLTF for web"""
    bl_idname = "pcb2blender.export_pcb_web"
    bl_label = "Export GLTF"
    bl_options = {"PRESET", "UNDO"}

    texture_dpi:       FloatProperty(name="Texture DPI",
                                     default=1016.0, soft_min=508.0, soft_max=2032.0)
    simplify_mesh: EnumProperty(name="Simplify mesh", items=(("Simplify", "Simplify", ""), (
        "Convex hull", "Convex hull", ""), ("Disabled", "Disabled", "")), default="Simplify")

    join_components: BoolProperty(name="Join components", default=True)
    random_rename: BoolProperty(name="Randomly rename objects", default=True)

    def __init__(self):
        super().__init__()


    def execute(self, context):
        # ob = bpy.context.active_object
        bpy.ops.object.mode_set(mode='EDIT')
        ob = bpy.data.objects[0]
        # Enter "Edge" select mode
        bpy.context.tool_settings.mesh_select_mode = [False, True, False]
        if self.simplify_mesh == "Simplify":
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.delete_loose(
                use_verts=True, use_edges=True, use_faces=True)
            bpy.ops.mesh.decimate(ratio=1.0, use_vertex_group=False, vertex_group_factor=1.0,
                                  invert_vertex_group=False, use_symmetry=False, symmetry_axis='Y')
        elif self.simplify_mesh == "Convex hull":
            bpy.ops.mesh.delete_loose(
                use_verts=True, use_edges=True, use_faces=True)
            bpy.ops.mesh.decimate(ratio=1.0, use_vertex_group=False, vertex_group_factor=1.0,
                                  invert_vertex_group=False, use_symmetry=False, symmetry_axis='Y')
            bpy.ops.mesh.convex_hull(delete_unused=True, use_existing_faces=True, make_holes=False, join_triangles=True,
                                     face_threshold=0.698132, shape_threshold=0.698132, uvs=False, vcols=False, seam=False, sharp=False, materials=False)
        if self.join_components:
            # mesh = ob.data
            # bm = bmesh.from_edit_mesh(mesh)

            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action="DESELECT")
            for idx, subobject in enumerate(ob.children):
                try:
                    bpy.context.view_layer.objects.active = subobject
                    bpy.ops.object.select_all()
                    bpy.ops.object.join()
                    bpy.ops.object.select_all(action="DESELECT")
                    # subobject.name = f"c{idx}"
                    # subobject.data.name = f"c{idx}_d"
                except Exception:
                    print("Joining failed")
        if self.random_rename:
            for i1, ob in enumerate(bpy.data.objects):
                ob.name = f"c{i1}"
                ob.data.name = f"c{i1}_d"
                for i2, sob in enumerate(ob.children):
                    sob.name = f"c{i1}_{i2}"
                    sob.data.name = f"c{i1}_{i2}_d"


        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.export_scene.gltf(
            filepath=self.filepath, export_copyright="pcb2blender", export_draco_mesh_compression_enable=True, export_draco_mesh_compression_level=6)
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.label(text="Reduce texture DPI")
        col.prop(self, "texture_dpi", slider=True)
        layout.split()

        col2 = layout.column()
        col2.label(text="Mesh")
        col2.prop(self, "simplify_mesh", text="")
        col2.prop(self, "join_components")

def menu_func_export_pcb_web(self, context):
    self.layout.operator(
        PCB2BLENDER_OT_export_pcb_web.bl_idname, text="GLTF for web (.glb)")



def register():
    bpy.utils.register_class(PCB2BLENDER_OT_export_pcb_web)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export_pcb_web)


def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export_pcb_web)
    bpy.utils.unregister_class(PCB2BLENDER_OT_export_pcb_web)