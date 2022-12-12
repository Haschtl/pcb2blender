
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
Materials = {
    "SilkS_Black":
        {"invert": True, "base_color": (
            50, 50, 50, 255), "metalness": 40, "roughness":  40, "emissive": 10, "occlusion": 255, "specular": 80},
    "SilkS_White":
        {"invert": True, "base_color": (
            255, 255, 255, 255), "metalness": 40, "roughness":  229, "emissive": 10, "occlusion": 255, "specular": 80},

    "Paste_Pb":
        {"invert": True, "base_color": (
            200, 200, 200, 255), "metalness": 40, "roughness": 220, "emissive": 0, "occlusion": 255, "specular": 80},

    "Mask_Blue":
        {"invert": False, "base_color": (
            72, 108, 188, 240), "metalness": 40, "roughness": 153, "emissive": 0, "occlusion": 255, "specular": 190},
    "Mask_Green":
        {"invert": False, "base_color": (
            56, 103, 74, 240), "metalness": 40, "roughness": 153, "emissive": 0, "occlusion": 255, "specular": 190},
    "Mask_Black":
        {"invert": False, "base_color": (
            72, 108, 188, 240), "metalness": 40, "roughness": 153, "emissive": 0, "occlusion": 255, "specular": 190},
    "Mask_Red":
        {"invert": False, "base_color": (
            92, 24, 20, 240), "metalness": 40, "roughness": 153, "emissive": 0, "occlusion": 255, "specular": 190},
    "Mask_White":
        {"invert": False, "base_color": (
            205, 205, 205, 240), "metalness": 40, "roughness": 30, "emissive": 0, "occlusion": 255, "specular": 190},

    "Cu_Gold2":
        {"invert": True, "base_color": (
            220, 180, 30, 255), "metalness": 40, "roughness": 150, "emissive": 0, "occlusion": 255, "specular": 120},
    "Cu_Gold":
        {"invert": True, "base_color": (
            255, 223, 127, 255), "metalness": 255, "roughness": 102, "emissive": 0, "occlusion": 255, "specular": 120},
    "Cu_Silver":
        {"invert": True, "base_color": (
            233, 236, 242, 255), "metalness": 255, "roughness": 102, "emissive": 0, "occlusion": 255, "specular": 120},

    "Board_Al":
        {"invert": True, "base_color": (
            200, 202, 212, 255), "metalness": 255, "roughness": 102, "emissive": 0, "occlusion": 255, "specular": 0},
}
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


# def select_material(layer: str, layer_types: Dict[str, PCBType]) -> Material:
def select_material(layer, layer_material):
    """
    Select a material based on the layer and layertypes
    """
    layer_types = material_presets[layer_material]
    if layer in layer_types:
        layer_id = layer+"_"+layer_types[layer]["material"]
    else:
        layer_id = "Board_Al"
    material = Materials[layer_id]
    material["height"] = layer_types[layer]["height"]
    return material
