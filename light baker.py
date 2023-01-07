import bpy

from mathutils import *
D = bpy.data
C = bpy.context
# aaaaa
# bbbbbbb
for object in bpy.context.selected_objects:
    if object.type == 'MESH':
        for slot in object.material_slots.values():
            texture = bpy.data.images.new(name='tmp', width=1024, height=1024)
            image_node = slot.material.node_tree.nodes.new(
                'ShaderNodeTexImage')
            image_node.image = texture
            image_node.select = True

            slot.material.node_tree.nodes.active = image_node
            bpy.ops.object.bake(type='DIFFUSE', pass_filter={
                                'DIRECT', 'INDIRECT'})
            texture.save(
                filepath=f'./bakedMaps/{object.name}_{slot.material.name}.png')

        # filepath=f'//{object.name}.png', save_mode='EXTERNAL',
        # bpy.ops.object.bake( type='DIFFUSE', pass_filter={'DIRECT', 'INDIRECT'}, width=1024, height=1024)


print('=====DONE=====')
