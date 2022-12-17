import bpy
import addon_utils
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
        # Enter "Edge" select mode
        bpy.context.tool_settings.mesh_select_mode = [False, True, False]
        self.export_gltf()
        self.decimate(context)
        self.export_gltf(self.filepath.replace(".glb", "1_decimate.glb"))

        # if self.join_components:
        #     if has_booltool() or False:
        #         self.boolean_union(context)
        #     else:
        #         print("Booltool not enabled. Using join-mode")
        #         self.join_objects(context)
        #     self.export_gltf(self.filepath+"1_joined")

        self.dissolve_limit(context)
        self.export_gltf(self.filepath.replace(".glb", "2_dissolved.glb"))
        
        self.merge_by_distance(context)

        if self.simplify_mesh == "Simplify":
            # self.decimate(context)
            self.decimate2(context)
        elif self.simplify_mesh == "Convex hull":
            self.convex_hull(context)

        self.export_gltf(self.filepath.replace(".glb", "3_simplified.glb"))

        if self.random_rename:
            self.rename(context)

        bpy.ops.object.mode_set(mode='OBJECT')
        self.export_gltf(self.filepath.replace(".glb", "4_reduced.glb"))
        return {"FINISHED"}

    def export_gltf(self, filename=None):
        if filename is None:
            filename=self.filepath
        bpy.ops.export_scene.gltf(
            filepath=filename, export_copyright="pcb2blender", export_draco_mesh_compression_enable=True, export_draco_mesh_compression_level=6, export_colors=False, export_apply=True, export_yup=True)

    def decimate(self, context):

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.delete_loose(
            use_verts=True, use_edges=True, use_faces=True)
        bpy.ops.mesh.decimate(ratio=1.0, use_vertex_group=False, vertex_group_factor=1.0,
                              invert_vertex_group=False, use_symmetry=False, symmetry_axis='Y')

    def convex_hull(self, context):

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.delete_loose(
            use_verts=True, use_edges=True, use_faces=True)
        bpy.ops.mesh.decimate(ratio=1.0, use_vertex_group=False, vertex_group_factor=1.0,
                              invert_vertex_group=False, use_symmetry=False, symmetry_axis='Y')
        bpy.ops.mesh.convex_hull(delete_unused=True, use_existing_faces=True, make_holes=False, join_triangles=True,
                                 face_threshold=0.698132, shape_threshold=0.698132, uvs=False, vcols=False, seam=False, sharp=False, materials=False)

    def join_objects(self, context):
        # mesh = ob.data
        # bm = bmesh.from_edit_mesh(mesh)
        ob = bpy.data.objects[0]
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

    def boolean_union(self, context):
        # join objects

        bpy.ops.object.mode_set(mode='OBJECT')
        print("Boolean union of all parts")
        for obj in bpy.context.scene.objects:
            obj.select_set(True)
        bpy.ops.object.booltool_auto_union()

    def rename(self, context):
        for i1, ob in enumerate(bpy.data.objects):
            ob.name = f"c{i1}"
            ob.data.name = f"c{i1}_d"
            for i2, sob in enumerate(ob.children):
                sob.name = f"c{i1}_{i2}"
                sob.data.name = f"c{i1}_{i2}_d"

    def dissolve_limit(self, context):

        bpy.ops.object.mode_set(mode='OBJECT')
        print("Dissolve limit")
        angle_limit = 0.0872665
        use_dissolve_boundaries = True
        delimit = {'MATERIAL'}  # 'SEAM'
        

        meshes = set(o.data for o in bpy.data.objects
                    if o.type == 'MESH')

        bm = bmesh.new()

        for m in meshes:
            bm.from_mesh(m)
            bmesh.ops.dissolve_limit(bm, angle_limit=angle_limit, verts=bm.verts, edges=bm.edges, use_dissolve_boundaries=use_dissolve_boundaries, delimit=delimit)
            bm.to_mesh(m)
            m.update()
            bm.clear()

        bm.free()

        # obj.select_set(state=True)
        # bm = obj.data
        # verts=bm.vertices
        # edges=bm.edges
        # # Limited dissolve
        # print("Dissolve limit")
        # obj.select_set(True)
        # bpy.ops.object.select_all()
        # bmesh.ops.dissolve_limit(
        #     bm, angle_limit=angle_limit, use_dissolve_boundaries=use_dissolve_boundaries, verts=verts, edges=edges, delimit=delimit)
        # obj.data.dissolve_limited(angle_limit=angle_limit, use_dissolve_boundaries=use_dissolve_boundaries, delimit={delimit})

    def decimate2(self, context):

        bpy.ops.object.mode_set(mode='EDIT')
        modifier_name = 'DecimateMod'
        decimate_ratio = 0.4
        print("decimate geometry")
        # for obj in bpy.data.objects:
        for obj in bpy.context.scene.objects:
            if(obj.type == "MESH"):
                context.view_layer.objects.active = obj

                # Split concave faces

                # Decimate Geometry -> breaks uv-map
                # cleanAllDecimateModifiers(obj)
                modifier = obj.modifiers.new(modifier_name, 'DECIMATE')
                modifier.ratio = decimate_ratio
                modifier.use_collapse_triangulate = True

    def merge_by_distance(self, context):
        # Merge by distance -> breaks UV-map
        pass

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


def has_booltool():
    return addon_utils.check("object_boolean_tools") == (True, True)

def menu_func_export_pcb_web(self, context):
    self.layout.operator(
        PCB2BLENDER_OT_export_pcb_web.bl_idname, text="GLTF for web (.glb)")



def register():
    bpy.utils.register_class(PCB2BLENDER_OT_export_pcb_web)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export_pcb_web)


def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export_pcb_web)
    bpy.utils.unregister_class(PCB2BLENDER_OT_export_pcb_web)