#   ### WORLD TRANSFORM COPY ###
# https://www.blender.org/forum/viewtopic.php?t=21306

info = {
    "name": "World Position Copy",
    "author": "Forrest Smith, forrestsmith605@gmail.com",
    "version": (0, 1),
    "blender": (2, 79, 0),
    "description": "For all selected objects, set the current translation and rotation to that found in the previous frame",
    "warning": "This script is still in development. Be careful!",
    "tracker_url": "",
    "category": "Animation"
}

import bpy
from mathutils import Matrix, Vector, Euler


class WpcCopyPreviousFrame(bpy.types.Operator):
    """Create a new animated Child Of constraint"""
    bl_idname = "wpc.previous"
    bl_label = "Copy Next Frame"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = bpy.context.active_object
        if armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Selection is not a pose bone")
            return
        sbones = bpy.context.selected_pose_bones
        vec = Vector((1.0,0.0,0.0))
        scn = bpy.context.scene             # next 3 lines: get and store prev and current frame
        cframe = scn.frame_current
        scn.frame_current = cframe-1
        bdata = []
        i = 0
        #pose_bone.location = armature.matrix_world.inverted() * pose_bone.bone.matrix_local.inverted() * vec
        for cBone in sbones:
            cvector = armature.matrix_world.inverted() * cBone.bone.matrix_local.inverted() * vec
            bdata.append(cvector)
            #str = "-" + cvector.toString
            self.report({'WARNING'}, cBone.name)
            print(cvector[:])
            i += 1

        scn.frame_current = cframe
        i = 0
        self.report({'WARNING'}, '______')
        for cBone in sbones:
            self.report({'WARNING'}, cBone.name)
            cBone.location = bdata[i]
            i += 1

        return {'FINISHED'}


class WpcCopyNextFrame(bpy.types.Operator):
    """Create a new animated Child Of constraint"""
    bl_idname = "wpc.next"
    bl_label = "Copy Next Frame"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = bpy.context.active_object
        if obj.type != 'ARMATURE':
            self.report({'ERROR'}, "Selection is not a pose bone")
            return
        obj = bpy.context.selected_pose_bones

        return {'FINISHED'}


class WpcBake(bpy.types.Operator):
    """Bake Dynamic Parent animation"""
    bl_idname = "wpc.bake"
    bl_label = "Bake transformation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = bpy.context.active_object
        scn = bpy.context.scene

        if obj.type == 'ARMATURE':
            obj = bpy.context.active_pose_bone
            bpy.ops.nla.bake(frame_start=scn.frame_start,
                             frame_end=scn.frame_end, step=1,
                             only_selected=True, visual_keying=False,
                             clear_constraints=False, clear_parents=False,
                             bake_types={'POSE'})
            # Removing constraints
            for const in obj.constraints[:]:
                if const.name.startswith("DP_"):
                    obj.constraints.remove(const)
        else:
            bpy.ops.nla.bake(frame_start=scn.frame_start,
                             frame_end=scn.frame_end, step=1,
                             only_selected=True, visual_keying=False,
                             clear_constraints=False, clear_parents=False,
                             bake_types={'OBJECT'})
            # Removing constraints
            for const in obj.constraints[:]:
                if const.name.startswith("DP_"):
                    obj.constraints.remove(const)

        return {'FINISHED'}


class WpcUI(bpy.types.Panel):
    """User interface for World Position Copy addon"""
    bl_category = "World Position Copy"
    bl_label = "World Position Copy"
    bl_idname = "wpc.ui"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator("wpc.next", text="Next Frame", icon="FORWARD")
        col.operator("wpc.previous", text="Previous Frame", icon="BACK")
        col.operator("wpc.bake", text="Bake", icon="REC")
        #col.operator("dp.clear", text="Clear", icon="X")
        #col.operator("wm.call_menu", text="Clear", icon="RIGHTARROW_THIN").name="dp.clear_menu"
        #col.menu("dp.clear_menu", text="Clear")


def register():
    bpy.utils.register_class(WpcCopyNextFrame)
    bpy.utils.register_class(WpcCopyPreviousFrame)
    bpy.utils.register_class(WpcBake)
    bpy.utils.register_class(WpcUI)

    pass


def unregister():
    bpy.utils.unregister_class(WpcCopyNextFrame)
    bpy.utils.unregister_class(WpcCopyPreviousFrame)
    bpy.utils.unregister_class(WpcBake)
    bpy.utils.unregister_class(WpcUI)

    pass


if __name__ == "__main__":
    register()
