
import matplotlib.image as mpimg
from skia import SVGDOM, Stream, Surface, Color4f
import io
from typing import List, Dict, TypedDict, Tuple
from PIL import Image
import sys
import numpy as np
from glob import glob
import os

SKIA_MAGIC = 0.282222222

# PCB2_LAYER_NAMES = (
#     "Board",
#     "F_Cu",
#     "F_Paste",
#     "F_Mask",
#     "B_Cu",
#     "B_Paste",
#     "B_Mask",
#     "Vias",
#     "F_Silk",
#     "B_Silk",

# ffdf7f
# e9ecf2

# Colors from here https://blog.pcb-arts.com/en/blog/blender-tutorial-2


class Color(TypedDict):
    invert: bool
    base_color: Tuple[int, int, int, int]
    metalness: int
    roughness: int
    emissive: int
    occlusion: int


class PCBType(TypedDict):
    height: float
    material: str


class Material(TypedDict):
    invert: bool
    base_color: Tuple[int, int, int, int]
    metalness: int
    roughness: int
    emissive: int
    occlusion: int
    height: float


Colors: Dict[str, Color] = {
    "SilkS_Black":
        {"invert": True, "base_color": (
            50, 50, 50, 255), "metalness": 40, "roughness":  40, "emissive": 10, "occlusion": 255, },
    "SilkS_White":
        {"invert": True, "base_color": (
            255, 255, 255, 255), "metalness": 40, "roughness":  229, "emissive": 10, "occlusion": 255, },
    "Paste_Pb":
        {"invert": True, "base_color": (
            200, 200, 200, 255), "metalness": 40, "roughness": 220, "emissive": 0, "occlusion": 255, },

    "Mask_Blue":
        {"invert": False, "base_color": (
            72, 108, 188, 240), "metalness": 40, "roughness": 153, "emissive": 0, "occlusion": 255, },
    "Mask_Green":
        {"invert": False, "base_color": (
            56, 103, 74, 240), "metalness": 40, "roughness": 153, "emissive": 0, "occlusion": 255, },
    "Mask_Black":
        {"invert": False, "base_color": (
            72, 108, 188, 240), "metalness": 40, "roughness": 153, "emissive": 0, "occlusion": 255, },
    "Mask_Red":
        {"invert": False, "base_color": (
            92, 24, 20, 240), "metalness": 40, "roughness": 153, "emissive": 0, "occlusion": 255, },
    "Mask_White":
        {"invert": False, "base_color": (
            205, 205, 205, 240), "metalness": 40, "roughness": 30, "emissive": 0, "occlusion": 255},

    "Cu_Gold2":
        {"invert": True, "base_color": (
            220, 180, 30, 255), "metalness": 40, "roughness": 150, "emissive": 0, "occlusion": 255, },
    "Cu_Gold":
        {"invert": True, "base_color": (
            255, 223, 127, 255), "metalness": 255, "roughness": 102, "emissive": 0, "occlusion": 255},
    "Cu_Silver":
        {"invert": True, "base_color": (
            233, 236, 242, 255), "metalness": 255, "roughness": 102, "emissive": 0, "occlusion": 255},
    "Board_Al":
        {"invert": True, "base_color": (
            200, 202, 212, 255), "metalness": 255, "roughness": 102, "emissive": 0, "occlusion": 255},
}

materials: Dict[str, Dict[str, PCBType]] = {
    "WhitePCB": {"SilkS": {"material": "Black", "height": 0.015},
                 "Paste": {"material": "Pb", "height": 0.01},
                 "Mask": {"material": "White", "height": 0.035},
                 "Cu": {"material": "Gold", "height": 0.035},
                 "Board": {"material": "Al", "height": 1.51}
                 },
    "GreenPCB": {"SilkS": {"material": "White", "height": 0.01},
                 "Paste": {"material": "Pb", "height": 0.01},
                 "Mask": {"material": "Green", "height": 0.01},
                 "Cu": {"material": "Gold", "height": 0.035},
                 "Board": {"material": "RK4", "height": 1.51}
                 },
    "RedPCB": {"SilkS": {"material": "White", "height": 0.01},
                 "Paste": {"material": "Pb", "height": 0.01},
                 "Mask": {"material": "Red", "height": 0.01},
                 "Cu": {"material": "Gold", "height": 0.035},
                 "Board": {"material": "RK4", "height": 1.51}
               },
    "BluePCB": {"SilkS": {"material": "White", "height": 0.01},
               "Paste": {"material": "Pb", "height": 0.01},
               "Mask": {"material": "Blue", "height": 0.01},
               "Cu": {"material": "Gold", "height": 0.035},
               "Board": {"material": "RK4", "height": 1.51}
               },
    "BlackPCB": {"SilkS": {"material": "White", "height": 0.01},
                 "Paste": {"material": "Pb", "height": 0.01},
                 "Mask": {"material": "Black", "height": 0.01},
                 "Cu": {"material": "Gold", "height": 0.035},
                 "Board": {"material": "RK4", "height": 1.51}
                 },
}
LAYER_ORDER = ["SilkS", "Paste", "Mask", "Cu", "Board"]
LAYER_ORDER.reverse()

INCH_TO_MM = 1 / 25.4


def select_material(layer: str, layer_types: Dict[str, PCBType]) -> Material:
    if layer in layer_types:
        layer_id = layer+"_"+layer_types[layer]["material"]
    else:
        layer_id = "Board_Al"
    material:Material = Colors[layer_id]
    material["height"] = layer_types[layer]["height"]
    return material

# a function that takes a vector - three numbers - and normalize it, i.e make it's length = 1


def normalizeRGB(vec):
    length = np.sqrt(vec[:, :, 0]**2 + vec[:, :, 1]**2 + vec[:, :, 2]**2)
    vec[:, :, 0] = vec[:, :, 0] / length
    vec[:, :, 1] = vec[:, :, 1] / length
    vec[:, :, 2] = vec[:, :, 2] / length
    return vec


def heightMapToNormalMap(image):

    # initialize the normal map, and the two tangents:
    normalMap = np.zeros((image.shape[0], image.shape[1], 3))
    tan = np.zeros((image.shape[0], image.shape[1], 3))
    bitan = np.zeros((image.shape[0], image.shape[1], 3))

    # we get the normal of a pixel by the 4 pixels around it, sodefine the top, buttom, left and right pixels arrays,
    # which are just the input image shifted one pixel to the corrosponding direction. We do this by padding the image
    # and then 'cropping' the unneeded sides
    B = np.pad(image, 1, mode='edge')[2:, 1:-1]
    T = np.pad(image, 1, mode='edge')[:-2, 1:-1]
    L = np.pad(image, 1, mode='edge')[1:-1, 0:-2]
    R = np.pad(image, 1, mode='edge')[1:-1, 2:]

    # to get a good scale/intensity multiplier, i.e a number that let's the R and G channels occupy most of their available
    # space between 0-1 without clipping, we will start with an overly strong multiplier - the smaller the the multiplier is, the
    # stronger it is -, to practically guarantee clipping then incrementally increase it until no clipping is happening

    scale = .05
    while True:

        # get the tangents of the surface, the normal is thier cross product
        tan[:, :, 0], tan[:, :, 1], tan[:, :, 2] = np.asarray([scale, 0, R-L])
        bitan[:, :, 0], bitan[:, :, 1], bitan[:,
                                              :, 2] = np.asarray([0, scale, B-T])
        normalMap = np.cross(tan, bitan)

        # normalize the normals to get their length to 1, they are called normals after all
        normalMap = normalizeRGB(normalMap)

        # increment the multiplier until the desired range of R and G is reached
        if scale > 2:
            break
        if np.max(normalMap[:, :, 0]) > 0.95 or np.max(normalMap[:, :, 1]) > 0.95 \
                or np.min(normalMap[:, :, 0]) < -0.95 or np.min(normalMap[:, :, 1]) < -0.95:
            scale += .05
            continue
        else:
            break

    # calculations were done for the channels to be in range -1 to 1 for the channels, however the image saving function
    # expects the range 0-1, so just divide these channels by 2 and add 0.5 to be in that range, we also flip the
    # G channel to comply with the OpenGL normal map convention
    normalMap[:, :, 0] = (normalMap[:, :, 0]/2)+.5
    normalMap[:, :, 1] = (0.5-(normalMap[:, :, 1]/2))
    normalMap[:, :, 2] = (normalMap[:, :, 2]/2)+.5
    normalMap = np.clip(normalMap, 0.0, 1.0)
    normalMap[:, :, 0] *= 255
    normalMap[:, :, 1] *= 255
    normalMap[:, :, 2] *= 255

    # normalMap[:, :, 3] = 255

    return np.dstack((normalMap, np.ones((image.shape[0], image.shape[1]))*255))


def svg2img(svg_path, dpi):
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


def layers2texture(layers_folder: str, dpi: float, material: str, ) -> None:
    layer_paths = list(glob(os.path.join(layers_folder, '*.svg')))
    groups: Dict[str, List[str]] = {}
    for path in sorted(layer_paths, reverse=True):
        group_name = os.path.split(path)[1].split("_")[0]
        if group_name in groups:
            groups[group_name].append(path)
        else:
            groups[group_name] = [path]
    for name in groups:
        _layers2texture(name, groups[name], dpi, material)


def _layers2texture(name: str, files: List[str], dpi: float, mat:str, show: bool = True) -> None:
    layers = {}
    for file in files:
        layer = file.split("_")[-1].replace(".svg", "")
        img = svg2img(file, dpi).getchannel(0)

        # if layer != "Mask":
        #     img = ImageOps.invert(img)

        img.save(file.replace(".svg", ".png"))
        layers[layer] = svg2img(file, dpi)
    print(layers.keys())

    img_shape = list(np.array(layers[list(layers.keys())[0]]).shape)
    # img_shape_1d = img_shape.copy()
    # img_shape_1d[2] = 1

    base_color = np.ones(img_shape)*50  # Default color
    metalness = np.zeros(img_shape)
    roughness = np.ones(img_shape)*50
    roughness[:, :, 3] = 0
    emissive = np.zeros(img_shape)  # Reflectivity
    occlusion = np.ones(img_shape)*255
    occlusion[:, :, 3] = 0
    heightmap = np.zeros(img_shape[:2])  # for normalmap

    ordered_layers = {}
    for layer in LAYER_ORDER:
        if layer in layers:
            ordered_layers[layer] = layers[layer]

    for layer in ordered_layers:
        material = select_material(layer, materials[mat])
        print(f"Processing {layer}")

        buffer2 = np.array(layers[layer], dtype=np.float64)
        # buffer2 = buffer2.astype(np.float64)
        if material["invert"]:
            buffer2[:, :, 0] = buffer2[:, :, 0]*-1+255
            buffer2[:, :, 1] = buffer2[:, :, 1]*-1+255
            buffer2[:, :, 2] = buffer2[:, :, 2]*-1+255
        buffer2[:, :, 0] *= material["base_color"][0]/255
        buffer2[:, :, 1] *= material["base_color"][1]/255
        buffer2[:, :, 2] *= material["base_color"][2]/255

        for row_idx, row in enumerate(buffer2):
            for col_idx, e in enumerate(row):
                if buffer2[row_idx, col_idx, 0] != 0 and buffer2[row_idx, col_idx, 1] != 0 and buffer2[row_idx, col_idx, 2] != 0:
                    if material["base_color"][3] != 255:

                        ratio1 = (255-material["base_color"][3])/255
                        ratio2 = material["base_color"][3]/255
                        base_color[row_idx, col_idx] = base_color[row_idx,
                                                                  col_idx] * ratio1+buffer2[row_idx, col_idx]*ratio2

                    else:
                        base_color[row_idx,
                                   col_idx] = buffer2[row_idx, col_idx]

                    metalness[row_idx, col_idx] = [
                        material["metalness"], material["metalness"], material["metalness"], 255]
                    roughness[row_idx][col_idx] = [
                        material["roughness"], material["roughness"], material["roughness"], 255]
                    emissive[row_idx, col_idx] = [
                        material["emissive"], material["emissive"], material["emissive"], 255]
                    occlusion[row_idx, col_idx] = [
                        material["occlusion"], material["occlusion"], material["occlusion"], 255]
                    heightmap[row_idx, col_idx] += material["height"]
                # else:
                #     base_color[row_idx, col_idx] = [0, 0, 0, 0]

            # buffer1[buffer2[:, :, :2] != [0, 0, 0]
            #         ] += buffer2[buffer2[:, :, :2] != [0, 0, 0]]
        # else:
        #     base_color = buffer2

    heightmap = heightmap/np.max(heightmap)*50
    heightmap = heightmap.astype(np.uint8)

    base_color = base_color.astype(np.uint8)
    metalness = metalness.astype(np.uint8)
    roughness = roughness.astype(np.uint8)
    emissive = emissive.astype(np.uint8)
    occlusion = occlusion.astype(np.uint8)

    height_4d = np.dstack(
        (heightmap, heightmap, heightmap, np.ones((img_shape[0], img_shape[1]))*255))
    height_4d = height_4d.astype(np.uint8)
    normal = heightMapToNormalMap(heightmap)
    normal = normal.astype(np.uint8)

    height_map_image = Image.fromarray(height_4d)
    base_color_image = Image.fromarray(base_color)
    metal_image = Image.fromarray(metalness)
    roughness_image = Image.fromarray(roughness)
    emissive_image = Image.fromarray(emissive)
    occlusion_image = Image.fromarray(occlusion)
    normal_image = Image.fromarray(normal)

    height_map_image.save(os.path.join(
        os.path.split(files[0])[0], name+"_displacement.png"))

    base_color_image.save(os.path.join(
        os.path.split(files[0])[0], name+"_base_color.png"))

    metal_image.save(os.path.join(
        os.path.split(files[0])[0], name+"_metal.png"))

    roughness_image.save(os.path.join(
        os.path.split(files[0])[0], name+"_roughness.png"))
    emissive_image.save(os.path.join(
        os.path.split(files[0])[0], name+"_emissive.png"))
    occlusion_image.save(os.path.join(
        os.path.split(files[0])[0], name+"_occlusion.png"))
    normal_image.save(os.path.join(
        os.path.split(files[0])[0], name+"_normal.png"))
    if show:
        height_map_image.show()
        base_color_image.show()
        metal_image.show()
        roughness_image.show()
        emissive_image.show()
        occlusion_image.show()
        normal_image.show()


if __name__ == "__main__":
    layers2texture(sys.argv[1], 1024, "BluePCB")
