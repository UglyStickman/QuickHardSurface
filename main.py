import bpy

bl_info = {
    "name": "Quick Hard Surface",
    "category": "3D View",
    "blender": (2, 92, 0)
}


class CustomMenu(bpy.types.Menu):
    bl_label = "Custom Menu"
    bl_idname = "OBJECT_MT_.custom_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.make_qhs_object")

class MirrorPopup(bpy.types.Operator):
    bl_idname = "object.mirror_dialog_operator"
    bl_label = "Mirror Settings"

    mirrorX: bpy.props.BoolProperty(name="X", default=True)
    mirrorY: bpy.props.BoolProperty(name="Y")
    mirrorZ: bpy.props.BoolProperty(name="Z")
    clipping: bpy.props.BoolProperty(name="Clipping")
    setObject: bpy.props.BoolProperty(name="Set active as mirror object")

    def execute(self, context):
        selection = bpy.context.selected_editable_objects
        active = bpy.context.view_layer.objects.active
        if active is not None:
            for obj in selection:
                if obj.type == "MESH":
                    mirrorMod = None
                    if not self.setObject:
                        mirrorMod = obj.modifiers.new(name="Mirror", type="MIRROR")
                    else:
                        if obj is not active:
                            mirrorMod = obj.modifiers.new(name="Mirror", type="MIRROR")
                            mirrorMod.mirror_object = active
                    if len(selection)<2 and mirrorMod is None:
                        mirrorMod = obj.modifiers.new(name="Mirror", type="MIRROR")
                    if mirrorMod is not None:
                        mirrorMod.use_axis[0] = self.mirrorX
                        mirrorMod.use_axis[1] = self.mirrorY
                        mirrorMod.use_axis[2] = self.mirrorZ
                        mirrorMod.use_clip = self.clipping
        else:
            print("please select an active object")
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class MakeQhsObject(bpy.types.Operator):
    bl_idname = "object.make_qhs_object"
    bl_label = "Make QHS Object"

    def execute(self, context):
        selection = bpy.context.selected_editable_objects
        for obj in selection:
            if obj.type == "MESH":
                bpy.ops.object.shade_smooth()
                obj.data.use_auto_smooth = True
                bevel = obj.modifiers.new(name="Bevel", type="BEVEL")
                bevel.width = 0.02
                bevel.segments = 3.0
                bevel.miter_outer = 'MITER_ARC'
                bevel.use_clamp_overlap = False
                WeightedNormal = obj.modifiers.new(name="WeightedNormal", type="WEIGHTED_NORMAL")
                WeightedNormal.keep_sharp = True
        return {'FINISHED'}

class AddQuadSphere(bpy.types.Operator):
    bl_idname = "object.quad_shere_add"
    bl_label = "Add Quad Sphere"
    bl_options = {'REGISTER', 'UNDO'}

    resolution: bpy.props.IntProperty(name="Resolution", default=2)

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add()
        cube = bpy.context.view_layer.objects.active
        subsurf = cube.modifiers.new(name="Subsurf", type="SUBSURF")
        subsurf.levels = self.resolution
        cast = cube.modifiers.new(name="Cast", type="CAST")
        cast.factor = 1.0
        bpy.ops.object.modifier_apply(modifier="Subsurf")
        bpy.ops.object.modifier_apply(modifier="Cast")
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(AddQuadSphere.bl_idname)

addon_keymaps = []
def register():
    #registrations:
    bpy.utils.register_class(CustomMenu)
    bpy.utils.register_class(MakeQhsObject)
    bpy.utils.register_class(MirrorPopup)
    bpy.utils.register_class(AddQuadSphere)
    #Menu:
    bpy.types.VIEW3D_MT_object.append(CustomMenu.draw)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)
    #Keybinds:
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
    kmi = km.keymap_items.new(MirrorPopup.bl_idname, type="M", value='PRESS', alt=True, ctrl=True)
    addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(CustomMenu)
    bpy.utils.unregister_class(MakeQhsObject)
    bpy.utils.unregister_class(MirrorPopup)
    bpy.utils.unregister_class(AddQuadSphere)


if __name__ == "__main__":
    register()
    #bpy.ops.object.mirror_dialog_operator('INVOKE_DEFAULT')
