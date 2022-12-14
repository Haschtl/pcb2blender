from PIL import Image
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
Textures = {
    "Pb": {
        "base_color": "./textures/pb/Metal032_2K_Color.png",
        "metalness": "./textures/pb/Metal032_2K_Metalness.png",
        "roughness": "./textures/pb/Metal032_2K_Roughness.png",
        "heightmap": "./textures/pb/Metal032_2K_Displacement.png",
        "dpi": 1024
        },
    "Cu": {
        "base_color": "./textures/cu/dull-copper_albedo.png", 
        "metalness": "./textures/cu/dull-copper_metallic.png", 
        "roughness": "./textures/cu/dull-copper_roughness.png", 
        "occlusion": "./textures/cu/dull-copper_ao.png", 
        "heightmap": "./textures/cu/dull-copper_displacement.png",
        "dpi": 1024
        },
    "Gold": {
        "base_color": "./textures/gold/BrushedGold02_2K_BaseColor.png",
        "metalness": "./textures/gold/BrushedGold02_2K_Metallic.png",
        "roughness": "./textures/gold/BrushedGold02_2K_Roughness.png",
        "heightmap": "./textures/gold/BrushedGold02_2K_Height.png",
        "dpi": 1024
        },
    "Silver": {
        "base_color": "./textures/silver/Metal041A_2K_Color.png",
        "metalness": "./textures/silver/Metal041A_2K_Metalness.png",
        "roughness": "./textures/silver/Metal041A_2K_Roughness.png",
        "heightmap": "./textures/silver/Metal041A_2K_Displacement.png",
        "dpi": 1024
        },
    "Al": {
        "base_color": "./textures/al/Aluminum-Scuffed_basecolor.png", 
        "metalness": "./textures/al/Aluminum-Scuffed_metallic.png", 
        "roughness": "./textures/al/Aluminum-Scuffed_roughness.png", 
        "heightmap": "./textures/al/Aluminum-Scuffed_displacement.png",
        "dpi": 1024
    },
    "SilkS.White": {
        "base_color": "./textures/plastic/scuffed-plastic5-alb.png",
        "metalness": "./textures/plastic/scuffed-plastic-metal.png",
        "roughness": "./textures/plastic/scuffed-plastic-rough.png",
        "occlusion": "./textures/plastic/scuffed-plastic-ao.png",
        "heightmap": "./textures/plastic/scuffed-plastic-displacement.png",
        "dpi": 1024
    },
    "SilkS.Black": {
        "base_color": "./textures/plastic/scuffed-plastic7-alb.png",
        "metalness": "./textures/plastic/scuffed-plastic-metal.png",
        "roughness": "./textures/plastic/scuffed-plastic-rough.png",
        "occlusion": "./textures/plastic/scuffed-plastic-ao.png",
        "heightmap": "./textures/plastic/scuffed-plastic-displacement.png",
        "dpi": 1024
    },
    "SilkS.Red": {
        "base_color": "./textures/plastic/scuffed-plastic4-alb.png",
        "metalness": "./textures/plastic/scuffed-plastic-metal.png",
        "roughness": "./textures/plastic/scuffed-plastic-rough.png",
        "occlusion": "./textures/plastic/scuffed-plastic-ao.png",
        "heightmap": "./textures/plastic/scuffed-plastic-displacement.png",
        "dpi": 1024
    },
    "SilkS.Blue": {
        "base_color": "./textures/plastic/scuffed-plastic8-alb.png",
        "metalness": "./textures/plastic/scuffed-plastic-metal.png",
        "roughness": "./textures/plastic/scuffed-plastic-rough.png",
        "occlusion": "./textures/plastic/scuffed-plastic-ao.png",
        "heightmap": "./textures/plastic/scuffed-plastic-displacement.png",
        "dpi": 1024
    },
    "SilkS.Violet": {
        "base_color": "./textures/plastic/scuffed-plastic-alb.png",
        "metalness": "./textures/plastic/scuffed-plastic-metal.png",
        "roughness": "./textures/plastic/scuffed-plastic-rough.png",
        "occlusion": "./textures/plastic/scuffed-plastic-ao.png",
        "heightmap": "./textures/plastic/scuffed-plastic-displacement.png",
        "dpi": 1024
    },
    "SilkS.Yellow": {
        "base_color": "./textures/plastic/scuffed-plastic6-alb.png",
        "metalness": "./textures/plastic/scuffed-plastic-metal.png",
        "roughness": "./textures/plastic/scuffed-plastic-rough.png",
        "occlusion": "./textures/plastic/scuffed-plastic-ao.png",
        "heightmap": "./textures/plastic/scuffed-plastic-displacement.png",
        "dpi": 1024
    },
    "SilkS.Green": {
        "base_color": "./textures/plastic/scuffed-plastic3-alb.png",
        "metalness": "./textures/plastic/scuffed-plastic-metal.png",
        "roughness": "./textures/plastic/scuffed-plastic-rough.png",
        "occlusion": "./textures/plastic/scuffed-plastic-ao.png",
        "heightmap": "./textures/plastic/scuffed-plastic-displacement.png",
        "dpi": 1024
    },
    "Mask.White": {
        "base_color": "./textures/plastic/scuffed-plastic5-alb.png",
        "metalness": "./textures/plastic/scuffed-plastic-metal.png",
        "roughness": "./textures/plastic/scuffed-plastic-rough.png",
        "occlusion": "./textures/plastic/scuffed-plastic-ao.png",
        "heightmap": "./textures/plastic/scuffed-plastic-displacement.png",
        "dpi": 1024
    },
    "Mask.Black": {
        "base_color": "./textures/plastic/scuffed-plastic7-alb.png",
        "metalness": "./textures/plastic/scuffed-plastic-metal.png",
        "roughness": "./textures/plastic/scuffed-plastic-rough.png",
        "occlusion": "./textures/plastic/scuffed-plastic-ao.png",
        "heightmap": "./textures/plastic/scuffed-plastic-displacement.png",
        "dpi": 1024
    },
    "Mask.Red": {
        "base_color": "./textures/plastic/scuffed-plastic4-alb.png",
        "metalness": "./textures/plastic/scuffed-plastic-metal.png",
        "roughness": "./textures/plastic/scuffed-plastic-rough.png",
        "occlusion": "./textures/plastic/scuffed-plastic-ao.png",
        "heightmap": "./textures/plastic/scuffed-plastic-displacement.png",
        "dpi": 1024
    },
    "Mask.Blue": {
        "base_color": "./textures/plastic/scuffed-plastic8-alb.png",
        "metalness": "./textures/plastic/scuffed-plastic-metal.png",
        "roughness": "./textures/plastic/scuffed-plastic-rough.png",
        "occlusion": "./textures/plastic/scuffed-plastic-ao.png",
        "heightmap": "./textures/plastic/scuffed-plastic-displacement.png",
        "dpi": 1024
    },
    "Mask.Violet": {
        "base_color": "./textures/plastic/scuffed-plastic-alb.png",
        "metalness": "./textures/plastic/scuffed-plastic-metal.png",
        "roughness": "./textures/plastic/scuffed-plastic-rough.png",
        "occlusion": "./textures/plastic/scuffed-plastic-ao.png",
        "heightmap": "./textures/plastic/scuffed-plastic-displacement.png",
        "dpi": 1024
    },
    "Mask.Yellow": {
        "base_color": "./textures/plastic/scuffed-plastic6-alb.png",
        "metalness": "./textures/plastic/scuffed-plastic-metal.png",
        "roughness": "./textures/plastic/scuffed-plastic-rough.png",
        "occlusion": "./textures/plastic/scuffed-plastic-ao.png",
        "heightmap": "./textures/plastic/scuffed-plastic-displacement.png",
        "dpi": 1024
    },
    "Mask.Green": {
        "base_color": "./textures/fr4/merged_material_Base_color.png",
        "metalness": "./textures/fr4/merged_material_Metallic.png",
        "roughness": "./textures/fr4/merged_material_Roughness.png",
        "emissive": "./textures/fr4/merged_material_Emissive.png",
        "occlusion": "./textures/fr4/PCB_fibers.png",
        "heightmap": "./textures/fr4/merged_material_Height.png",
        "dpi": 1024
    },
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
              "Paste": {"material": "Pb", "height": 0.02},
              "Mask": {"material": "White", "height": 0.035},
              "Cu": {"material": "Gold", "height": 0.035},
              "Board": {"material": "Al", "height": 1.51}
              },
    "Green": {"SilkS": {"material": "White", "height": 0.01},
              "Paste": {"material": "Pb", "height": 0.02},
              "Mask": {"material": "Green", "height": 0.01},
              "Cu": {"material": "Gold", "height": 0.035},
              "Board": {"material": "RK4", "height": 1.51}
              },
    "Red": {"SilkS": {"material": "White", "height": 0.01},
            "Paste": {"material": "Pb", "height": 0.02},
            "Mask": {"material": "Red", "height": 0.01},
            "Cu": {"material": "Gold", "height": 0.035},
            "Board": {"material": "RK4", "height": 1.51}
            },
    "Blue": {"SilkS": {"material": "White", "height": 0.01},
             "Paste": {"material": "Pb", "height": 0.02},
             "Mask": {"material": "Blue", "height": 0.01},
             "Cu": {"material": "Gold", "height": 0.035},
             "Board": {"material": "RK4", "height": 1.51}
             },
    "Black": {"SilkS": {"material": "White", "height": 0.01},
              "Paste": {"material": "Pb", "height": 0.02},
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
def select_material(layer_id, layer_types, dpi):
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

    for t in Textures:
        if t in layer_id+"."+layer_color:
            material.update(Textures[t])
    return Texture(material, layer_id, layer_type, layer_color, dpi)


class Texture():
    def __init__(self, material, id, layer_type, color, dpi):
        self.target_dpi=dpi
        self.material = material
        self.id=id
        self.layer_type = layer_type
        self.color=color
        print(f"Texture for {id} in {color}")
        for t in self.material:
            if type(self.material[t]) == str:
                print(f"- {t}: {self.material[t]}")
                png = Image.open(
                    self.material[t])
                # png.load()  # required for png.split()
                # background = Image.new("RGB", png.size, (255, 255, 255))
                # background.paste(png, mask=png.split()[3])  # 3 is the alpha channel
                self.material[t]=png
            else:
                print(f"- {t}: Simple")

    @property
    def invert(self):
        return self.material["invert"]

    def get_at_pixel(self, x, y):
        # {"invert": True, "base_color": (200, 202, 212, 255), "metalness": 255, "roughness": 102, "emissive": 0, "occlusion": 255, "specular": 0, "height": 1}

        output = {}
        for t in self.material:
            if t == "heightmap":
                continue
            elif t == "height":
                if "heightmap" in self.material:
                    width, height = self.material["heightmap"].size
                    x = int(x/self.target_dpi*self.material["dpi"]) % width
                    y = int(y/self.target_dpi*self.material["dpi"]) % height
                    pixel = self.material["heightmap"].getpixel((x, y))
                    if type(pixel)!=int and type(pixel)!=float:
                        pixel=pixel[0]
                    output[t] = self.material[t] * \
                        pixel/255
                else:
                    output[t] = self.material[t]
            elif type(self.material[t]) == int or type(self.material[t]) == float:
                output[t] = [self.material[t],
                             self.material[t], self.material[t], 255]
            elif type(self.material[t]) == bool:
                output[t] = self.material[t]
            elif type(self.material[t]) == tuple:
                output[t] = self.material[t]
            else:
                width, height = self.material[t].size
                x = int(x/self.target_dpi*self.material["dpi"]) % width
                y = int(y/self.target_dpi*self.material["dpi"]) % height
                pixel = self.material[t].getpixel((x, y))
                if type(pixel)==int:
                    output[t] = [pixel, pixel, pixel]
                else:
                    output[t] = list(pixel)
                if len(output[t]) == 4:
                    if self.layer_type == "Mask":
                        output[t][3]=240
                    else:
                        output[t][3]=255
                else:
                    if self.layer_type=="Mask":
                        output[t].append(240)
                    else:
                        output[t].append(255)
        return output
