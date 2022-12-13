# from gerber_renderer import Gerber

# board = Gerber.Board('./Edge_Cuts.gbr', verbose=True)
# board.render('./ga')
# import gerber
# from gerber.render.cairo_backend import GerberCairoContext

# # Read gerber and Excellon files
# top_copper = gerber.read('Edge_Cuts.gbr')
# # nc_drill = gerber.read('example.txt')

# # Rendering context
# ctx = GerberCairoContext()

# # Create SVG image
# top_copper.render(ctx, filename="out.svg")
# # nc_drill.render(ctx, 'composite.svg')

# from gerbonara import LayerStack

# stack = LayerStack.from_directory('./')
# w, h = stack.outline.size('mm')
# print(f'Board size is {w:.1f} mm x {h:.1f} mm')
import trimesh
from trimesh import load_path

edge_cut = load_path("./Edge_Cuts.svg")
extruded = edge_cut.extrude(height=10)

extruded.export('test.stl')
