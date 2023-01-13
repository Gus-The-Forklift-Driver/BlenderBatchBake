import bpy
from . import light_baker

bl_info = {
    'name': 'BatchLightBaker',
    'author': 'Smonking_Sheep',
    'description': 'Allows you to bake maps in batch',
    'blender': (3, 4, 1),
    'version': (0, 0, 2),
    'location': 'View3D > side panel > BLB',
    'warning': '',
    'doc_url': 'https://github.com/Gus-The-Forklift-Driver/BlenderBatchBake',
    'tracker_url': 'https://github.com/Gus-The-Forklift-Driver/BlenderBatchBake/issues',
    'category': 'MapBaking',
    'support': 'COMMUNITY',
}


class helloWorld(bpy.types.Operator):
    bl_idname = 'object.hello_world'
    bl_label = 'Print Hello World'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return {'FINISHED'}


class bake_maps(bpy.types.Operator):
    '''Bake the maps of the selected objects'''
    bl_idname = 'batch_light_bake.bake_maps'
    bl_space_type = 'VIEW_3D'
    bl_label = 'bake maps of selected objects'
    bl_options = {'REGISTER'}

    def execute(self, context):
        size = context.scene.BLB.image_size
        filepath = context.scene.BLB.filepath
        file_extension = context.scene.BLB.file_extension
        light_baker.bake_maps(image_size=(size, size), out_filepath=filepath, file_extension=file_extension)
        return {'FINISHED'}


class interface(bpy.types.Panel):
    '''create a panel'''
    bl_label = 'Blender Light Baker'
    bl_idname = 'VIEW3D_PT_settings'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BLB'

    def draw(self, context):
        if context.scene.render.engine != 'BLENDER_EEVEE':
            layout = self.layout
            scene = context.scene
            cscene = scene.cycles
            # layout.label(text='bake lights')

            layout.operator('batch_light_bake.bake_maps')
            layout.prop(scene.BLB, 'filepath')
            layout.prop(scene.BLB, 'file_extension')

            layout.prop(scene.cycles, 'device')

            # render settings
            layout.use_property_split = True
            layout.use_property_decorate = False

            heading = layout.column(align=True, heading='Noise Threshold')
            row = heading.row(align=True)
            row.prop(cscene, 'use_adaptive_sampling', text='')
            sub = row.row()
            sub.active = cscene.use_adaptive_sampling
            sub.prop(cscene, 'adaptive_threshold', text='')

            col = layout.column(align=True)
            if cscene.use_adaptive_sampling:
                col.prop(cscene, 'samples', text='Max Samples')
                col.prop(cscene, 'adaptive_min_samples', text='Min Samples')
            else:
                col.prop(cscene, 'samples', text='Samples')
            col.prop(cscene, 'time_limit')

            layout.prop(cscene, 'max_bounces')

            # denoiser

            col = layout.column()
            col.active = cscene.use_denoising
            col.prop(cscene, 'use_denoising')
            if col.active:
                col.prop(cscene, 'denoiser', text='Denoiser')

            layout.label(text='Settings :')
            layout.prop(scene.BLB, 'image_size')
            # bake type
            layout.prop(scene.cycles, 'bake_type')
            cbk = scene.render.bake

            col = layout.column()

            if cscene.bake_type == 'NORMAL':
                col.prop(cbk, 'normal_space', text='Space')

                sub = col.column(align=True)
                sub.prop(cbk, 'normal_r', text='Swizzle R')
                sub.prop(cbk, 'normal_g', text='G')
                sub.prop(cbk, 'normal_b', text='B')

            elif cscene.bake_type == 'COMBINED':

                col = layout.column(heading='Lighting', align=True)
                col.prop(cbk, 'use_pass_direct')
                col.prop(cbk, 'use_pass_indirect')

                col = layout.column(heading='Contributions', align=True)
                col.active = cbk.use_pass_direct or cbk.use_pass_indirect
                col.prop(cbk, 'use_pass_diffuse')
                col.prop(cbk, 'use_pass_glossy')
                col.prop(cbk, 'use_pass_transmission')
                col.prop(cbk, 'use_pass_emit')

            elif cscene.bake_type in {'DIFFUSE', 'GLOSSY', 'TRANSMISSION'}:
                col = layout.column(heading='Contributions', align=True)
                col.prop(cbk, 'use_pass_direct')
                col.prop(cbk, 'use_pass_indirect')
                col.prop(cbk, 'use_pass_color')

            # margin
            layout.label(text='Margin :')
            layout.prop(scene.render.bake, 'margin_type')
            layout.prop(scene.render.bake, 'margin')

        else:
            layout = self.layout
            scene = context.scene
            layout.label(text='Switch to Cycles')
            layout.prop(scene.render, 'engine')


class BLBProperties(bpy.types.PropertyGroup):
    image_size: bpy.props.IntProperty(name='image_size', default=1024)
    filepath: bpy.props.StringProperty(
        name='filepath', default='//backedMaps/')
    file_extension: bpy.props.StringProperty(name='file_extension', default='hdr')


CLASSES = [
    # operators
    helloWorld,
    bake_maps,
    interface,
    # propertyGroup
    BLBProperties
]


def register():
    print(f'**** Registring {len(CLASSES)} class')
    for c in CLASSES:
        bpy.utils.register_class(c)
    print('**** Done')
    bpy.types.Scene.BLB = bpy.props.PointerProperty(type=BLBProperties)


def unregister():
    print(f'**** Unregistring {len(CLASSES)} class')
    for c in CLASSES:
        bpy.utils.unregister_class(c)
    print('**** Done')
    del bpy.types.Scene.BLB
