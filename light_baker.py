import bpy


def bake_maps(image_size=(1024, 1024), out_filepath='//backedMaps/') -> None:

    # store seleced objects
    selected_object = bpy.context.selected_objects
    # print(selected_object)

    # deselect all objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = None

    # iterate over selected objects
    for object in selected_object:
        # check if object is mesh
        if object.type == 'MESH':

            object.select_set(True)
            bpy.context.view_layer.objects.active = object

            for slot in object.material_slots:
                material = slot.material
                material.use_nodes = True
                nodes = material.node_tree.nodes

                # check if there isnt image nodes already existing
                img_node = None
                for node in nodes:
                    if node.name == 'Baked_Image':
                        img_node = node

                if bpy.data.images.find(f'{object.name}_{material.name}') == -1:
                    # create  new image
                    img = bpy.data.images.new(name=f'{object.name}_{material.name}', width=image_size[0], height=image_size[1], alpha=True)
                else:
                    img = bpy.data.images.get(f'{object.name}_{material.name}')

                    # setup new image node
                if img_node == None:
                    img_node = nodes.new('ShaderNodeTexImage')
                    img_node.name = 'Baked_Image'

                img_node.image = img
                img_node.select = True
                nodes.active = img_node

                # save image
                img.filepath = f'{out_filepath}{object.name}_{material.name}.hdr'
                # img.save()
                # save and bake
                # print(bpy.context.view_layer.objects.active)

                cbs = bpy.context.scene.render.bake
                bpy.ops.object.bake(type=bpy.context.scene.cycles.bake_type,
                                    pass_filter=cbs.pass_filter,
                                    margin=cbs.margin,
                                    margin_type=cbs.margin_type,
                                    normal_space=cbs.normal_space,
                                    normal_r=cbs.normal_r,
                                    normal_g=cbs.normal_g,
                                    normal_b=cbs.normal_b)
                img.save()

            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = None

# bake_maps()
# print('==================DONNENENENEENE==================')
