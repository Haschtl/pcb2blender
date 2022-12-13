
# class Color(TypedDict):
#     invert: bool
#     base_color: Tuple[int, int, int, int]
#     metalness: int
#     roughness: int
#     emissive: int
#     specular: int
#     occlusion: int


# class PCBType(TypedDict):
#     height: float
#     material: str


# class Material(Color):
#     height: float


# Texture definition of single PCB-layers
# Materials: Dict[str, Color]
Layers = {
    "SilkS": {"invert": True, "base_color": (
        50, 50, 50, 255), "metalness": 40, "roughness":  40, "emissive": 10, "occlusion": 255, "specular": 80},
    "Paste": {"invert": True, "base_color": (
        200, 200, 200, 255), "metalness": 40, "roughness": 220, "emissive": 0, "occlusion": 255, "specular": 80},
    "Mask": {"invert": False, "base_color": (
        56, 103, 74, 240), "metalness": 40, "roughness": 153, "emissive": 0, "occlusion": 255, "specular": 190},
    "Cu": {"invert": True, "base_color": (
        255, 223, 127, 255), "metalness": 255, "roughness": 102, "emissive": 0, "occlusion": 255, "specular": 120},
    "Board": {"invert": True, "base_color": (
        200, 202, 212, 255), "metalness": 255, "roughness": 102, "emissive": 0, "occlusion": 255, "specular": 0}
}
Colors = {
    # "Black": (50, 50, 50),
    # "Blue": (72, 108, 188),
    # "Green": (56, 103, 74),
    # "Red": (92, 24, 20),
    # "White": (240, 240, 240),

    # KiCAD
    "Black": (20, 20, 20),
    "Green": (60, 150, 80),
    "Red": (128, 0, 0),
    "Blue": (0, 0, 128),
    "Violet": (80, 0, 80),
    "White": (200, 200, 200),
    "Yellow": (128, 128, 0),

    # Custom
    "Pb": (200, 200, 200),
    "Gold2": (220, 180, 30),
    "Gold": (255, 223, 127),
    "Silver": (233, 236, 242),
    "Al": (200, 202, 212),

}
# Materials = {
#     "SilkS.Black":
#         {"invert": True, "base_color": (
#             50, 50, 50, 255), "metalness": 40, "roughness":  40, "emissive": 10, "occlusion": 255, "specular": 80},
#     "SilkS.White":
#         {"invert": True, "base_color": (
#             255, 255, 255, 255), "metalness": 40, "roughness":  229, "emissive": 10, "occlusion": 255, "specular": 80},

#     "Paste.Pb":
#         {"invert": True, "base_color": (
#             200, 200, 200, 255), "metalness": 40, "roughness": 220, "emissive": 0, "occlusion": 255, "specular": 80},

#     "Mask.Blue":
#         {"invert": False, "base_color": (
#             72, 108, 188, 240), "metalness": 40, "roughness": 153, "emissive": 0, "occlusion": 255, "specular": 190},
#     "Mask.Green":
#         {"invert": False, "base_color": (
#             56, 103, 74, 240), "metalness": 40, "roughness": 153, "emissive": 0, "occlusion": 255, "specular": 190},
#     "Mask.Black":
#         {"invert": False, "base_color": (
#             72, 108, 188, 240), "metalness": 40, "roughness": 153, "emissive": 0, "occlusion": 255, "specular": 190},
#     "Mask.Red":
#         {"invert": False, "base_color": (
#             92, 24, 20, 240), "metalness": 40, "roughness": 153, "emissive": 0, "occlusion": 255, "specular": 190},
#     "Mask.White":
#         {"invert": False, "base_color": (
#             205, 205, 205, 240), "metalness": 40, "roughness": 30, "emissive": 0, "occlusion": 255, "specular": 190},

#     "Cu.Gold2":
#         {"invert": True, "base_color": (
#             220, 180, 30, 255), "metalness": 40, "roughness": 150, "emissive": 0, "occlusion": 255, "specular": 120},
#     "Cu.Gold":
#         {"invert": True, "base_color": (
#             255, 223, 127, 255), "metalness": 255, "roughness": 102, "emissive": 0, "occlusion": 255, "specular": 120},
#     "Cu.Silver":
#         {"invert": True, "base_color": (
#             233, 236, 242, 255), "metalness": 255, "roughness": 102, "emissive": 0, "occlusion": 255, "specular": 120},

#     "Board.Al":
#         {"invert": True, "base_color": (
#             200, 202, 212, 255), "metalness": 255, "roughness": 102, "emissive": 0, "occlusion": 255, "specular": 0},
# }

# materials: Definition of common PCB color combinations
# materials: Dict[str, Dict[str, PCBType]]
material_presets = {
    "White": {"SilkS": {"material": "Black", "height": 0.015},
              "Paste": {"material": "Pb", "height": 0.01},
              "Mask": {"material": "White", "height": 0.035},
              "Cu": {"material": "Gold", "height": 0.035},
              "Board": {"material": "Al", "height": 1.51}
              },
    "Green": {"SilkS": {"material": "White", "height": 0.01},
              "Paste": {"material": "Pb", "height": 0.01},
              "Mask": {"material": "Green", "height": 0.01},
              "Cu": {"material": "Gold", "height": 0.035},
              "Board": {"material": "RK4", "height": 1.51}
              },
    "Red": {"SilkS": {"material": "White", "height": 0.01},
            "Paste": {"material": "Pb", "height": 0.01},
            "Mask": {"material": "Red", "height": 0.01},
            "Cu": {"material": "Gold", "height": 0.035},
            "Board": {"material": "RK4", "height": 1.51}
            },
    "Blue": {"SilkS": {"material": "White", "height": 0.01},
             "Paste": {"material": "Pb", "height": 0.01},
             "Mask": {"material": "Blue", "height": 0.01},
             "Cu": {"material": "Gold", "height": 0.035},
             "Board": {"material": "RK4", "height": 1.51}
             },
    "Black": {"SilkS": {"material": "White", "height": 0.01},
              "Paste": {"material": "Pb", "height": 0.01},
              "Mask": {"material": "Black", "height": 0.01},
              "Cu": {"material": "Gold", "height": 0.035},
              "Board": {"material": "RK4", "height": 1.51}
              },
}


def defaultLayerStack(name):
    if "SilkS" in name:
        return material_presets["Green"]["SilkS"]
    elif "Paste" in name:
        return material_presets["Green"]["Paste"]
    elif "Mask" in name:
        return material_presets["Green"]["Mask"]
    elif "Cu" in name:
        return material_presets["Green"]["Cu"]
    else:
        return material_presets["Green"]["SilkS"]


# def select_material(layer: str, layer_types: Dict[str, PCBType]) -> Material:
def select_material(layer_id, layer_types):
    """
    Select a material based on the layer and layertypes
    """
    layer_type = layer_id.split(".")[1]
    layer_color = layer_types[layer_id]["material"]
    material = Layers[layer_type]
    if layer_color in Colors:
        material["base_color"] = Colors[layer_color]
    elif layer_color.startswith("#"):
        r = int(layer_color[1:3], 16)
        g = int(layer_color[3:5], 16)
        b = int(layer_color[5:7], 16)
        a = 255
        if len(layer_color) > 7:
            a = int(layer_color[7:9], 16)
        material["base_color"] = (r, g, b, a)
    material["height"] = layer_types[layer_id]["height"]
    if len(list(material["base_color"])) == 3:
        if "Mask" in layer_id:
            material["base_color"] = (*list(material["base_color"]), 240)
        else:
            material["base_color"] = (*list(material["base_color"]), 255)

    return material
