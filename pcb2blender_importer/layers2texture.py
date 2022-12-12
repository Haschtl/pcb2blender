# export layer-infos from kicad
# create mesh from svg
# import layer-infos in blender
# replace svg-export durch -> gerber -> svg
# from typing import List, Dict, TypedDict, Tuple

from PIL import Image, ImageFilter
import numpy as np
from pathlib import Path
import os
import argparse

try:
    from .shared import openPCB3D, svg2img, gerber2svg
    from .uv_materials import select_material
except ImportError:
    from shared import openPCB3D, svg2img, gerber2svg
    from uv_materials import select_material

def layer2img(layer):
    layer = layer.astype(np.uint8)
    layer_4d = np.dstack(
        (layer, layer, layer,  np.ones((layer.shape[0], layer.shape[1]))*255))
    layer_4d = layer_4d.astype(np.uint8)
    return layer_4d


def img2layer(layer):
    layer = np.array(layer)
    layer.astype(np.float64)
    print(layer.shape)
    return layer[:, :, 0]

# Exported additional maps
MAPS = ["metalness", "roughness", "emissive", "occlusion", "specular"]

# Order of PCB layers
LAYER_ORDER = ["SilkS", "Paste", "Mask", "Cu", "Board"]
LAYER_ORDER.reverse()


def normalizeRGB(vec):
    """a function that takes a vector - three numbers - and normalize it, i.e make it's length = 1"""
    length = np.sqrt(vec[:, :, 0]**2 + vec[:, :, 1]**2 + vec[:, :, 2]**2)
    vec[:, :, 0] = vec[:, :, 0] / length
    vec[:, :, 1] = vec[:, :, 1] / length
    vec[:, :, 2] = vec[:, :, 2] / length
    return vec


def heightMapToNormalMap(image):
    """
    Create normal map from heightmap
    """
    print(image.shape)
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


def concat_images(images, horizontal: bool):
    heights = [im.height for im in images]
    widths = [im.width for im in images]
    if horizontal:
        dst = Image.new('RGBA', (np.sum(widths), images[0].height))
    else:
        dst = Image.new('RGBA', (images[0].width, np.sum(heights)))
    pos = 0
    for image in images:
        if horizontal:
            dst.paste(image, (pos, 0))
            pos += image.width
        else:
            dst.paste(image, (0, pos))
            pos += image.height
    return dst

# def layers2texture(filepath: str, dpi: float, material: str, save: bool) -> Dict[str, Dict[str, Image.Image]]:


def layers2texture(filepath: str, dpi: float, material: str, save: bool, progress_cb=None, use_gerber=True):
    """
    Processes layers from pcb3d file, returns Images for each side  
    """
    tempdir, pcb3d_layers = openPCB3D(Path(filepath))
    # layers = [pcb3d.boards]
    # layer_paths = list(glob(os.path.join(layers_folder, '*.svg')))
    layer_paths = list(pcb3d_layers)
    print(layer_paths)
    # groups: Dict[str, List[str]] = {}
    groups = {}
    for path in sorted(layer_paths, reverse=True):
        group_name = os.path.split(path)[1].split("_")[0]
        if group_name in groups:
            groups[group_name].append(os.path.join(tempdir, path))
        else:
            groups[group_name] = [os.path.join(tempdir, path)]

    # images: Dict[str, Dict[str, Image.Image]] = {}
    images = {}
    export_dir = filepath.replace(".pcb3d", "")
    for name in groups:
        images[name] = _layers2texture(
            name, groups[name], dpi, material, save, export_dir=export_dir, progress_cb=progress_cb, use_gerber=use_gerber)

    # combine maps
    maps = {}
    for group in images:
        for map in images[group]:
            if map in maps:
                maps[map].append(images[group][map])
            else:
                maps[map] = [images[group][map]]
    for map in maps:
        p = os.path.join(export_dir, f"{map}.png")
        if not os.path.exists(os.path.dirname(p)):
            os.makedirs(os.path.dirname(p), exist_ok=True)
        concat_image = concat_images(maps[map], True)
        concat_image.save(p)
        print(f"Saving {p}")
    return images


# def _layers2texture(name: str, files: List[str], dpi: float, mat: str, save: bool = True, export_dir: str = ".", show: bool = False) -> Dict[str, Image.Image]:
def _layers2texture(name: str, files, dpi: float, mat: str, save: bool = True, export_dir: str = ".", progress_cb=None, show: bool = False, use_gerber: bool = True):
    """
    Processes one side of the PCB and returns all texture maps
    """
    # blur_normal_mask = False
    # Convert layers to bitmaps
    layers = {}
    for file in files:
        gerber_path = file.replace(".svg", ".gbr")
        if os.path.exists(gerber_path) and use_gerber:
            gerber2svg(gerber_path)
        layer = file.split("_")[-1].replace(".svg", "")
        img = svg2img(file, dpi)
        # if layer != "Mask":
        #     img = ImageOps.invert(img)
        print(f'Processing {file}')
        img.getchannel(0).save(file.replace(".svg", ".png"))
        layers[layer] = img

    # Initialize maps
    img_shape = list(np.array(layers[list(layers.keys())[0]]).shape)
    base_color = np.ones(img_shape)*50  # Default color
    heightmap = np.zeros(img_shape[:2])  # for normalmap
    _metalness = np.zeros(img_shape)
    _roughness = np.ones(img_shape)*50
    _roughness[:, :, 3] = 0
    _emissive = np.zeros(img_shape)  # Reflectivity
    _occlusion = np.ones(img_shape)*255
    _occlusion[:, :, 3] = 0
    _specular = np.zeros(img_shape)
    maps = {"metalness": _metalness, "roughness": _roughness,
            "emissive": _emissive, "occlusion": _occlusion, "specular": _specular}

    # Sort the layers
    ordered_layers = {}
    for layer in LAYER_ORDER:
        if layer in layers:
            ordered_layers[layer] = layers[layer]

    # Process each layer
    for layer in ordered_layers:
        material = select_material(layer, mat)
        print(f"Processing {layer}")

        if "Mask" in layer and dpi > 2000:
            # blur heatmap
            scale = 255/np.max(heightmap)
            heightmap = heightmap*scale
            print(heightmap.shape)
            _heightmap = layer2img(heightmap)
            image = Image.fromarray(_heightmap)
            filtered = image.filter(
                ImageFilter.GaussianBlur(radius=int(dpi/1000)))
            heightmap = img2layer(filtered)
            print(heightmap.shape)
            heightmap = heightmap/scale

        buffer2 = np.array(layers[layer], dtype=np.float64)
        if material["invert"]:
            # If layer-SVG is inverted
            buffer2[:, :, 0] = buffer2[:, :, 0]*-1+255
            buffer2[:, :, 1] = buffer2[:, :, 1]*-1+255
            buffer2[:, :, 2] = buffer2[:, :, 2]*-1+255
        buffer2[:, :, 0] *= material["base_color"][0]/255
        buffer2[:, :, 1] *= material["base_color"][1]/255
        buffer2[:, :, 2] *= material["base_color"][2]/255

        for row_idx, row in enumerate(buffer2):
            for col_idx, e in enumerate(row):
                if buffer2[row_idx, col_idx, 0] != 0 and buffer2[row_idx, col_idx, 1] != 0 and buffer2[row_idx, col_idx, 2] != 0:
                    ratio1 = (255-material["base_color"][3])/255
                    ratio2 = material["base_color"][3]/255
                    base_color[row_idx, col_idx] = base_color[row_idx,
                                                              col_idx] * ratio1+buffer2[row_idx, col_idx]*ratio2

                    for key in MAPS:
                        maps[key][row_idx, col_idx] = [
                            material[key], material[key], material[key], 255]
                    heightmap[row_idx, col_idx] += material["height"]
        if progress_cb is not None:
            progress_cb()

    # Convert heightmap to normal map
    scale = 100/np.max(heightmap)
    heightmap = heightmap*scale
    heightmap[heightmap < 0] = 0
    heightmap[heightmap > 255] = 255
    _heightmap = layer2img(heightmap)

    # Convert numpy arrays to uint8
    base_color = base_color.astype(np.uint8)

    for key in MAPS:
        maps[key] = maps[key].astype(np.uint8)

    # Convert numpy arrays to PIL.Image
    # images: Dict[str, Image.Image] = {}
    images = {}
    images["base_color"] = Image.fromarray(base_color)
    images["displacement"] = Image.fromarray(_heightmap)
    for key in MAPS:
        images[key] = Image.fromarray(maps[key])

    use_normal = True
    if use_normal:
        normal = heightMapToNormalMap(_heightmap[:, :, 0])
        normal = normal.astype(np.uint8)
        images["normal"] = Image.fromarray(normal)

    if save:
        # Save images
        for key in images:
            p = os.path.join(export_dir,
                             os.path.split(files[0])[0], name+f"_{key}.png")
            if not os.path.exists(os.path.dirname(p)):
                os.makedirs(os.path.dirname(p), exist_ok=True)
            images[key].save(p)
            print(f"Saving {p}")

    if show:
        # Show images
        for key in MAPS:
            images[key].show()

    return images


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pcb3d", help="Path to .pcb3d file")
    parser.add_argument("--dpi", default=1024, type=int,
                        help="DPI resolution of exported maps")
    parser.add_argument("--material", default="Green",
                        help="Material: Green, Red, Blue, White or Black")
    args = parser.parse_args()
    layers2texture(args.pcb3d, args.dpi, args.material, True)

    # out_dir = os.path.join(args.pcb3d.replace(".pcb3d", ""), "layers")
    # create_blender_material(out_dir)
