import pcbnew
from pcbnew import PLOT_CONTROLLER as PlotController, PCB_PLOT_PARAMS, PLOT_FORMAT_SVG, ToMM, PLOT_FORMAT_GERBER

import os
import tempfile
import shutil
import struct
import re
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from dataclasses import dataclass, field
from typing import List
import json

PCB = "pcb.wrl"
COMPONENTS = "components"
LAYERS = "layers"
BOARD_INFO = "board.yaml"
LAYERS_BOUNDS = "bounds"
BOARDS = "boards"
BOUNDS = "bounds"
STACKED = "stacked_"
PADS = "pads"

INCLUDED_LAYERS = (
    "F_Cu", "B_Cu", "F_Paste", "B_Paste", "F_SilkS", "B_SilkS", "F_Mask", "B_Mask", "Edge_Cuts"
)

SVG_MARGIN = 1.0  # mm


@dataclass
class StackedBoard:
    name: str
    offset: List[float]


@dataclass
class BoardDef:
    name: str
    bounds: List[float]
    stacked_boards: List[StackedBoard] = field(default_factory=list)


def export_pcb3d(filepath, boarddefs):
    init_tempdir()

    wrl_path = get_temppath(PCB)
    components_path = get_temppath(COMPONENTS)
    pcbnew.ExportVRML(wrl_path, 0.001, True, True, components_path, 0.0, 0.0)

    layers_path = get_temppath(LAYERS)
    board = pcbnew.GetBoard()
    bounds = tuple(map(ToMM, board.ComputeBoundingBox(
        aBoardEdgesOnly=True).getWxRect()))
    bounds = (
        bounds[0] - SVG_MARGIN, bounds[1] - SVG_MARGIN,
        bounds[2] + SVG_MARGIN * 2, bounds[3] + SVG_MARGIN * 2
    )
    export_layers(board, bounds, layers_path)

    board_info_path = get_temppath(BOARD_INFO)
    export_board_info(board, board_info_path)

    board_id = os.path.split(board.GetFileName())[1].replace(".kicad_pcb", "")
    with ZipFile(filepath, mode="w", compression=ZIP_DEFLATED) as file:
        # always ensure the COMPONENTS, LAYERS and BOARDS directories are created
        file.writestr(COMPONENTS + "/", "")
        file.writestr(LAYERS + "/", "")
        file.writestr(BOARDS + "/", "")

        file.write(wrl_path, PCB)
        for path in components_path.glob("**/*.wrl"):
            file.write(path, str(Path(COMPONENTS) / path.name))

        for path in layers_path.glob("**/*.svg"):
            file.write(path, str(Path(LAYERS) / path.name))
        for path in layers_path.glob("**/*.gbr"):
            file.write(path, str(Path(LAYERS) /
                       path.name.replace(board_id+"-", "")))
        file.writestr(str(Path(LAYERS) / LAYERS_BOUNDS),
                      struct.pack("!ffff", *bounds))
        file.write(board_info_path, BOARD_INFO)
        for boarddef in boarddefs.values():
            subdir = Path(BOARDS) / boarddef.name

            file.writestr(str(subdir / BOUNDS),
                          struct.pack("!ffff", *boarddef.bounds))

            for stacked in boarddef.stacked_boards:
                file.writestr(
                    str(subdir / (STACKED + stacked.name)),
                    struct.pack("!fff", *stacked.offset)
                )

        for footprint in board.Footprints():
            has_model = len(footprint.Models()) > 0
            is_tht_or_smd = bool(
                footprint.GetAttributes() & (pcbnew.FP_THROUGH_HOLE | pcbnew.FP_SMD))
            value = footprint.GetValue()
            reference = footprint.GetReference()
            for i, pad in enumerate(footprint.Pads()):
                # layers = [board.GetLayerName(id)
                #           for id in pad.GetLayerSet().Seq()]
                name = f"{value}_{reference}_{i}"
                is_flipped = pad.IsFlipped()
                has_paste = pad.IsOnLayer(pcbnew.B_Paste if is_flipped else pcbnew.F_Paste)
                data = struct.pack(
                    "!ff????BBffffBff",
                    *map(ToMM, pad.GetPosition()),
                    is_flipped,
                    has_model,
                    is_tht_or_smd,
                    has_paste,
                    pad.GetAttribute(),
                    pad.GetShape(),
                    *map(ToMM, pad.GetSize()),
                    pad.GetOrientationRadians(),
                    pad.GetRoundRectRadiusRatio(),
                    pad.GetDrillShape(),
                    *map(ToMM, pad.GetDrillSize()),
                )
                file.writestr(str(Path(PADS) / name), data)

def get_boarddefs(board):
    boarddefs = {}
    ignored = []

    tls = {}
    brs = {}
    stacks = {}
    for drawing in board.GetDrawings():
        if drawing.Type() == pcbnew.PCB_TEXT_T:
            text_obj = drawing.Cast()
            text = text_obj.GetText()

            if not text.startswith("PCB3D_"):
                continue

            pos = tuple(map(ToMM, text_obj.GetPosition()))
            if text.startswith("PCB3D_TL_"):
                tls.setdefault(text, pos)
            elif text.startswith("PCB3D_BR_"):
                brs.setdefault(text, pos)
            elif text.startswith("PCB3D_STACK_"):
                stacks.setdefault(text, pos)
            else:
                ignored.append(text)

    for tl_str in tls.copy():
        name = tl_str[9:]
        br_str = "PCB3D_BR_" + name
        if br_str in brs:
            tl_pos = tls.pop(tl_str)
            br_pos = brs.pop(br_str)

            boarddef = BoardDef(
                sanitized(name),
                (tl_pos[0], tl_pos[1], br_pos[0] -
                 tl_pos[0], br_pos[1] - tl_pos[1])
            )
            boarddefs[boarddef.name] = boarddef

    for stack_str in stacks.copy():
        try:
            other, onto, target, z_offset = stack_str[12:].split("_")
            z_offset = float(z_offset)
        except ValueError:
            continue

        if onto != "ONTO":
            continue

        other_name = sanitized(other)
        target_name = sanitized(target)

        if not other_name in set(boarddefs) | {"FPNL"} or not target_name in boarddefs:
            continue

        stack_pos = stacks.pop(stack_str)
        target_pos = boarddefs[target_name].bounds[:2]
        stacked = StackedBoard(
            other_name,
            (stack_pos[0] - target_pos[0],
             stack_pos[1] - target_pos[1], z_offset)
        )
        boarddefs[target_name].stacked_boards.append(stacked)

    ignored += list(tls.keys()) + list(brs.keys()) + list(stacks.keys())

    return boarddefs, ignored


def export_layers(board, bounds, output_directory: Path):
    plot_controller = PlotController(board)
    plot_options = plot_controller.GetPlotOptions()
    plot_options.SetOutputDirectory(output_directory)

    plot_options.SetPlotFrameRef(False)
    plot_options.SetAutoScale(False)
    plot_options.SetScale(1)
    plot_options.SetMirror(False)
    plot_options.SetUseGerberAttributes(True)
    plot_options.SetExcludeEdgeLayer(True)
    plot_options.SetDrillMarksType(PCB_PLOT_PARAMS.NO_DRILL_SHAPE)

    for layer in INCLUDED_LAYERS:
        plot_controller.SetLayer(getattr(pcbnew, layer))
        plot_controller.OpenPlotfile(layer, PLOT_FORMAT_SVG, "")
        plot_controller.PlotLayer()
        filepath = Path(plot_controller.GetPlotFileName())
        plot_controller.ClosePlot()
        filepath = filepath.rename(filepath.parent / f"{layer}.svg")

        content = filepath.read_text()
        width = f"{bounds[2] * 0.1:.6f}cm"
        height = f"{bounds[3] * 0.1:.6f}cm"
        viewBox = " ".join(str(round(v * 1e6)) for v in bounds)
        content = svg_header_regex.sub(
            svg_header_sub.format(width, height, viewBox), content)
        filepath.write_text(content)
    generate_gerbers(board, output_directory)


def export_board_info(board, output_path):
    # Stackup API is not ready yet, workaround: open kicad_pcb file and parse content
    # stackup = board.GetDesignSettings().GetStackupDescriptor()
    kicad_pcb_path = board.GetFileName()
    with open(kicad_pcb_path, "r") as f:
        kicad_pcb = f.readlines()
    layers = []
    start = False
    for line in kicad_pcb:
        if "(stackup" in line:
            start = True
            continue
        if line == '    )\n':
            break

        if start is True:
            layers.append(line.strip())
    board_info = {}

    layers_parsed = []
    for l in layers:
        if l.startswith("(layer"):
            parsed_layer = {}
            l_c = l.split("(")
            for c in l_c:
                if c.startswith("layer"):
                    parsed_layer["name"] = c.split('"')[1]
                if c.startswith("type"):
                    parsed_layer["type"] = c.split('"')[1]
                if c.startswith("color"):
                    parsed_layer["color"] = c.split('"')[1]
                if "thickness" in c:
                    parsed_layer["thickness"] = float(
                        c.replace("thickness", "").replace(")", ""))
            layers_parsed.append(parsed_layer)
        if l.startswith("(copper_finish "):
            board_info["copper_finish"] = l.split('"')[1]

    board_info = {"stackup": layers_parsed}
    with open(output_path, "w") as f:
        json.dump(board_info, f, indent=3)


def sanitized(name):
    return re.sub("[\W]+", "_", name)


def get_tempdir():
    return Path(tempfile.gettempdir()) / "pcb2blender_tmp"


def get_temppath(filename):
    return get_tempdir() / filename


def init_tempdir():
    tempdir = get_tempdir()
    if tempdir.exists():
        shutil.rmtree(tempdir)
    tempdir.mkdir()


svg_header_regex = re.compile(
    r"<svg([^>]*)width=\"[^\"]*\"[^>]*height=\"[^\"]*\"[^>]*viewBox=\"[^\"]*\"[^>]*>"
)
svg_header_sub = "<svg\g<1>width=\"{}\" height=\"{}\" viewBox=\"{}\">"


def generate_gerbers(pcb, path):
    plot_controller = pcbnew.PLOT_CONTROLLER(pcb)
    plot_options = plot_controller.GetPlotOptions()

    # Set General Options:
    plot_options.SetOutputDirectory(path)
    plot_options.SetPlotFrameRef(False)
    plot_options.SetPlotValue(True)
    plot_options.SetPlotReference(True)
    plot_options.SetPlotInvisibleText(True)
    plot_options.SetPlotViaOnMaskLayer(True)
    plot_options.SetExcludeEdgeLayer(False)
    # plot_options.SetPlotPadsOnSilkLayer(PLOT_PADS_ON_SILK_LAYER)
    # plot_options.SetUseAuxOrigin(PLOT_USE_AUX_ORIGIN)
    plot_options.SetMirror(False)
    # plot_options.SetNegative(PLOT_NEGATIVE)
    # plot_options.SetDrillMarksType(PLOT_DRILL_MARKS_TYPE)
    # plot_options.SetScale(PLOT_SCALE)
    plot_options.SetAutoScale(True)
    # plot_options.SetPlotMode(PLOT_MODE)
    # plot_options.SetLineWidth(pcbnew.FromMM(PLOT_LINE_WIDTH))

    # Set Gerber Options
    # plot_options.SetUseGerberAttributes(GERBER_USE_GERBER_ATTRIBUTES)
    # plot_options.SetUseGerberProtelExtensions(GERBER_USE_GERBER_PROTEL_EXTENSIONS)
    # plot_options.SetCreateGerberJobFile(GERBER_CREATE_GERBER_JOB_FILE)
    # plot_options.SetSubtractMaskFromSilk(GERBER_SUBTRACT_MASK_FROM_SILK)
    # plot_options.SetIncludeGerberNetlistInfo(GERBER_INCLUDE_GERBER_NETLIST_INFO)

    plot_plan = [
        ('F.Cu', pcbnew.F_Cu, 'Front Copper'),
        ('B.Cu', pcbnew.B_Cu, 'Back Copper'),
        ('F.Paste', pcbnew.F_Paste, 'Front Paste'),
        ('B.Paste', pcbnew.B_Paste, 'Back Paste'),
        ('F.SilkS', pcbnew.F_SilkS, 'Front SilkScreen'),
        ('B.SilkS', pcbnew.B_SilkS, 'Back SilkScreen'),
        ('F.Mask', pcbnew.F_Mask, 'Front Mask'),
        ('B.Mask', pcbnew.B_Mask, 'Back Mask'),
        ('Edge.Cuts', pcbnew.Edge_Cuts, 'Edges'),
        ('Eco1.User', pcbnew.Eco1_User, 'Eco1 User'),
        ('Eco2.User', pcbnew.Eco2_User, 'Eco1 User'),
    ]

    for layer_info in plot_plan:
        plot_controller.SetLayer(layer_info[1])
        plot_controller.OpenPlotfile(
            layer_info[0], pcbnew.PLOT_FORMAT_GERBER, layer_info[2])
        plot_controller.PlotLayer()

    plot_controller.ClosePlot()
