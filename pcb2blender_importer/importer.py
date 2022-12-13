import bpy
from bpy_extras.io_utils import ImportHelper, orientation_helper, axis_conversion
from bpy.props import *
from mathutils import Matrix

from pathlib import Path

from .materials import merge_materials, enhance_materials

from io_scene_x3d import ImportX3D, X3D_PT_import_transform, import_x3d
from io_scene_x3d import menu_func_import as menu_func_import_x3d_original

from .texture_importer import PCB2BLENDER_OT_import_pcb3d_texture, menu_func_import_pcb3d_texture
from .importer_base import PCB2BLENDER_OT_import_pcb3d, menu_func_import_pcb3d
# from .importer_step import import_step, menu_func_import_step
from .shared import FIX_X3D_SCALE

@orientation_helper(axis_forward="Y", axis_up="Z")
class PCB2BLENDER_OT_import_x3d(bpy.types.Operator, ImportHelper):
    __doc__ = ImportX3D.__doc__
    bl_idname = "pcb2blender.import_x3d"
    bl_label = ImportX3D.bl_label
    bl_options = {"PRESET", "UNDO"}

    filename_ext = ".x3d"
    filter_glob: StringProperty(default="*.x3d;*.wrl;*.wrz", options={"HIDDEN"})

    join:              BoolProperty(name="Join Shapes", default=True)
    tris_to_quads:     BoolProperty(name="Tris to Quads", default=True)
    enhance_materials: BoolProperty(name="Enhance Materials", default=True)
    scale:             FloatProperty(name="Scale", default=FIX_X3D_SCALE, precision=5)

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')

        objects_before = set(bpy.data.objects)
        matrix = axis_conversion(from_forward=self.axis_forward, from_up=self.axis_up).to_4x4()
        result = import_x3d.load(context, self.filepath, global_matrix=matrix)
        if not result == {"FINISHED"}:
            return result

        if not (objects := list(set(bpy.data.objects).difference(objects_before))):
            return {"FINISHED"}

        for obj in objects:
            obj.matrix_world = Matrix.Scale(self.scale, 4) @ obj.matrix_world
            obj.select_set(True)
        context.view_layer.objects.active = objects[0]

        bpy.ops.object.shade_smooth()
        for obj in objects:
            if obj.type == "MESH":
                obj.data.use_auto_smooth = True

        if self.join:
            meshes = {obj.data for obj in objects if obj.type == "MESH"}
            if len(objects) > 1:
                bpy.ops.object.join()
            bpy.ops.object.transform_apply()
            for mesh in meshes:
                if not mesh.users:
                    bpy.data.meshes.remove(mesh)

            joined_obj = context.object
            joined_obj.name = Path(self.filepath).name.rsplit(".", 1)[0]
            joined_obj.data.name = joined_obj.name
            objects = [joined_obj]
        else:
            bpy.ops.object.transform_apply(location=False, rotation=False)

        if self.tris_to_quads:
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_all(action="SELECT")
            bpy.ops.mesh.tris_convert_to_quads()
            bpy.ops.object.mode_set(mode="OBJECT")

        if self.enhance_materials:
            materials = sum((obj.data.materials[:] for obj in objects), [])
            merge_materials([obj.data for obj in objects])
            for material in materials[:]:
                if not material.users:
                    materials.remove(material)
                    bpy.data.materials.remove(material)
            enhance_materials(materials)

        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.prop(self, "join")
        layout.prop(self, "tris_to_quads")
        layout.prop(self, "enhance_materials")
        layout.split()
        layout.prop(self, "scale")

bases = X3D_PT_import_transform.__bases__
namespace = dict(X3D_PT_import_transform.__dict__)
del namespace["bl_rna"]
X3D_PT_import_transform_copy = type("X3D_PT_import_transform_copy", bases, namespace)
class PCB2BLENDER_PT_import_transform_x3d(X3D_PT_import_transform_copy):
    @classmethod
    def poll(cls, context):
        return context.space_data.active_operator.bl_idname == "PCB2BLENDER_OT_import_x3d"

def menu_func_import_x3d(self, context):
    self.layout.operator(PCB2BLENDER_OT_import_x3d.bl_idname,
        text="X3D Extensible 3D (.x3d/.wrl)")

classes = (
    PCB2BLENDER_OT_import_pcb3d,
    PCB2BLENDER_OT_import_pcb3d_texture,
    PCB2BLENDER_OT_import_x3d,
    PCB2BLENDER_PT_import_transform_x3d,
    # import_step
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_x3d_original)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_x3d)

    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_pcb3d)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_pcb3d_texture)
    # bpy.types.TOPBAR_MT_file_import.append(menu_func_import_step)

def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_pcb3d)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_pcb3d_texture)
    # bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_step)

    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_x3d)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_x3d_original)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
