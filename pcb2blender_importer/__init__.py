bl_info = {
    "name": "pcb2blender importer",
    "description": "Enables Blender to import .pcb3d files, exported from KiCad.",
    "author": "Bobbe",
    "version": (2, 4, 0),
    "blender": (3, 4, 0),
    "location": "File > Import",
    "category": "Import-Export",
    "support": "COMMUNITY",
    "doc_url": "https://github.com/30350n/pcb2blender",
    "tracker_url": "https://github.com/30350n/pcb2blender/issues",
}

__version__ = "2.4"

from .blender_addon_utils import add_dependencies, register_modules_factory

deps = {
    "skia-python": "skia",
    "pillow": "PIL",
    "numpy": "numpy",
    "gerber-renderer":"gerber_renderer",
    "PyYAML":"yaml"
}
add_dependencies(deps, no_extra_deps=True)

# module_names = ("importer", "materials", "solder_joints",
#                 "web_exporter", "texture_importer")


modules = ("importer", "materials", "solder_joints",
           "web_exporter", "texture_importer")
register, unregister = register_modules_factory(modules)
