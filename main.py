import bpy

bl_info = {
    "name": "My Hard Surface Modelling Addon",
    "category": "3D View",
    "blender": (2, 92, 0)
}

class CustomMenu(bpy.types.Menu):
    bl_label = "Custom Menu"
    bl_idname = "OBJECT_MT_.custom_menu"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("object.make_qhs_object")

class qhs_MakeQhsObject(bpy.types.Operator):
    bl_idname = "object.make_qhs_object"
    bl_label = "Make QHS Object"
    
    def execute(self, context):
        selection = bpy.context.selected_editable_objects
        for obj in selection:
            bpy.ops.object.shade_smooth()
            obj.data.use_auto_smooth = True
            bevel = obj.modifiers.new(name="Bevel", type="BEVEL")
            print(type(bevel))
            bevel.width = 0.02
            bevel.segments = 3.0
            bevel.miter_outer = 'MITER_ARC'
            bevel.use_clamp_overlap = False
            WeightedNormal = obj.modifiers.new(name="WeightedNormal", type="WEIGHTED_NORMAL")
            WeightedNormal.keep_sharp = True
        return {'FINISHED'}

def register():
    bpy.utils.register_class(CustomMenu)
    bpy.utils.register_class(qhs_MakeQhsObject)
    bpy.types.VIEW3D_MT_object.append(CustomMenu.draw)

def unregister():
    bpy.utils.unregister_class(CustomMenu)

if __name__ == "__main__":
    register()