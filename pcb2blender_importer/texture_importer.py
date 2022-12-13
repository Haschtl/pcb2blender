import bpy



def create_material(material_name, files):
    material = {}
    material['cancel'] = False
    material['alpha'] = False

    new_mat = bpy.data.materials.get(material_name)
    if not new_mat:
        new_mat = bpy.data.materials.new(material_name)

    if material['alpha'] == True:
        new_mat.blend_method = 'BLEND'

    new_mat.use_nodes = True
    node_tree = new_mat.node_tree

    nodes = node_tree.nodes
    nodes.clear()

    links = node_tree.links
    links.clear()
    master_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    for file in files:
        if material['cancel'] == False:
            # Begin constructing node tree for this material
            if 'base_color' in file:
                print(f"Adding base color: {file}")
                bt_node = nodes.new(type='ShaderNodeTexImage')
                bt_node.image = bpy.data.images.load(file)
                links.new(
                    master_node.inputs['Base Color'], bt_node.outputs['Color'])
                links.new(
                    master_node.inputs['Alpha'], bt_node.outputs['Alpha'])

            if 'metal' in file:
                print(f"Adding Metallic: {file}")
                bt_node = nodes.new(type='ShaderNodeTexImage')
                bt_node.image = bpy.data.images.load(file)
                links.new(
                    master_node.inputs['Metallic'], bt_node.outputs['Color'])

            if 'specular' in file:
                print(f"Adding Specular: {file}")
                bt_node = nodes.new(type='ShaderNodeTexImage')
                bt_node.image = bpy.data.images.load(file)
                links.new(
                    master_node.inputs['Specular'], bt_node.outputs['Color'])

            if 'roughness' in file:
                print(f"Adding Roughness: {file}")
                bt_node = nodes.new(type='ShaderNodeTexImage')
                bt_node.image = bpy.data.images.load(file)
                links.new(
                    master_node.inputs['Roughness'], bt_node.outputs['Color'])

            if 'emissive' in file:
                print(f"Adding Emissive: {file}")
                bt_node = nodes.new(type='ShaderNodeTexImage')
                bt_node.image = bpy.data.images.load(file)
                links.new(
                    master_node.inputs['Emission'], bt_node.outputs['Color'])

            if 'normal' in file:
                print(f"Adding Normal: {file}")
                bmi_node = nodes.new(type='ShaderNodeTexImage')
                bmi_node.image = bpy.data.images.load(file)
                # bm_node = nodes.new(type='ShaderNodeBump')

                # links.new(bm_node.inputs['Height'],
                #         bt_node.outputs['Color'])
                links.new(
                    master_node.inputs['Normal'], bmi_node.outputs['Color'])

    out_node = nodes.new(type='ShaderNodeOutputMaterial')

    links.new(master_node.outputs['BSDF'], out_node.inputs[0])

    return new_mat