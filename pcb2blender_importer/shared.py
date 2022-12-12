from skia import SVGDOM, Stream, Surface, Color4f
import io
import tempfile
import random
import struct
from PIL import Image
from zipfile import ZipFile, BadZipFile
from typing import Tuple, List
import re
from pathlib import Path


SKIA_MAGIC = 0.282222222
PCB = "pcb.wrl"
COMPONENTS = "components"
LAYERS = "layers"
LAYERS_BOUNDS = "bounds"
BOARDS = "boards"
BOUNDS = "bounds"
STACKED = "stacked_"
PADS = "pads"

INCLUDED_LAYERS = (
    "F_Cu", "B_Cu", "F_Paste", "B_Paste", "F_SilkS", "B_SilkS", "F_Mask", "B_Mask"
)

REQUIRED_MEMBERS = {PCB, LAYERS}


INCH_TO_MM = 1 / 25.4


def openPCB3D(filepath: Path) -> Tuple[Path, List[str]]:
    """
    Copied from importer.py:PCB2BLENDER_OT_import_pcb3d.import_pcb3d()
    """
    dirname = filepath.name.replace(".", "_") + f"_{random.getrandbits(64)}"
    tempdir = Path(tempfile.gettempdir()) / "pcb2blender_tmp" / dirname
    tempdir.mkdir(parents=True, exist_ok=True)
    try:
        with ZipFile(filepath) as f:
            # MEMBERS = {path.name for path in ZipPath(f).iterdir()}
            # if missing := REQUIRED_MEMBERS.difference(MEMBERS):
            #     print(f"not a valid .pcb3d file: missing {str(missing)[1:-1]}")
            layers = [f"{LAYERS}/{layer}.svg" for layer in INCLUDED_LAYERS]
            # layers = [f"{LAYERS}/{layer}.gerb" for layer in INCLUDED_LAYERS]
            f.extractall(tempdir, layers)
            return tempdir, layers
    except BadZipFile:
        raise Exception(f"error: not a valid .pcb3d file: not a zip file")
    except (KeyError, struct.error) as e:
        raise Exception(f"pcb3d file is corrupted: {e}")


def svg2img(svg_path, dpi):
    """
    Copied from importer.py
    Converts SVG to image
    """
    svg = SVGDOM.MakeFromStream(Stream.MakeFromFile(str(svg_path)))
    width, height = svg.containerSize()
    dpmm = dpi * INCH_TO_MM * SKIA_MAGIC
    pixels_width, pixels_height = round(width * dpmm), round(height * dpmm)
    surface = Surface(pixels_width, pixels_height)

    with surface as canvas:
        canvas.clear(Color4f.kWhite)
        canvas.scale(pixels_width / width, pixels_height / height)
        svg.render(canvas)

    with io.BytesIO(surface.makeImageSnapshot().encodeToData()) as file:
        image = Image.open(file)
        image.load()

    return image

def gerber2svg(gerber_path):
    from gerber_renderer import Gerber
    board=Gerber.Board(gerber_path)
    board.render(gerber_path.replace(".gerb",".svg"))


regex_filter_components = re.compile(
    r"(?P<prefix>Transform\s*{\s*"
    r"(?:rotation (?P<r>[^\n]*)\n)?\s*"
    r"(?:translation (?P<t>[^\n]*)\n)?\s*"
    r"(?:scale (?P<s>[^\n]*)\n)?\s*"
    r"children\s*\[\s*)"
    r"(?P<instances>(?:Transform\s*{\s*"
    r"(?:rotation [^\n]*\n)?\s*(?:translation [^\n]*\n)?\s*(?:scale [^\n]*\n)?\s*"
    r"children\s*\[\s*Inline\s*{\s*url\s*\"[^\"]*\"\s*}\s*]\s*}\s*)+)"
)
