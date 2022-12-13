
# import gmsh
import bpy
import sys
from bpy_extras.io_utils import ImportHelper
from bpy.props import *


class import_step(bpy.types.Operator, ImportHelper):
    bl_idname = "pcb2blender.import_step"
    bl_label = "Import .step"
    bl_options = {"PRESET", "UNDO"}

    filename_ext = ".step"
    filter_glob: StringProperty(
        default="*.step;*.stp", options={"HIDDEN"})

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        # step2stl(self.filename)


def menu_func_import_step(self, context):
    self.layout.operator(
        import_step.bl_idname, text="STEP (.step,.stp)")


# def step2stl(filename):
#     gmsh.initialize()
#     gmsh.option.setNumber("General.Terminal", 1)
#     gmsh.model.add("modelo_1")

#     gmsh.merge(filename)

#     gmsh.model.mesh.generate(3)

#     gmsh.model.geo.synchronize()
#     gmsh.fltk.run()
#     gmsh.finalize()


if __name__ == "__main__":
    step2stl(sys.argv[1])
