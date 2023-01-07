import bpy


def bake_maps(image_size=(1024, 1024)) -> None:

    # store seleced objects
    selected_object = bpy.context.selected_objects
    print(selected_object)
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

                # create  new image
                img = bpy.data.images.new(
                    name=f'{object.name}_{material.name}', width=image_size[0], height=image_size[1], alpha=True)

                # setup new image node
                img_node = nodes.new('ShaderNodeTexImage')
                img_node.name = 'Baked Image'
                img_node.image = img
                img_node.select = True
                nodes.active = img_node

                # save image
                img.filepath = f'//bakedMaps/{object.name}_{material.name}.png'
                img.save()
                # save and bake
                print(bpy.context.view_layer.objects.active)
                bpy.ops.object.bake()
                img.save()

            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = None

# bake_maps()
# print('==================DONNENENENEENE==================')
