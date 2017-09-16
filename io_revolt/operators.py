if "bpy" in locals():
    import imp
    imp.reload(common)
    imp.reload(properties)
    imp.reload(tools)

import bpy
import time
from . import common
from . import properties
from . import tools

from .common import *
from .properties import *

"""
Import Operator for all file types
"""
class ImportRV(bpy.types.Operator):
    bl_idname = "import_scene.revolt"
    bl_label = "Import Re-Volt Files"
    bl_description = "Import Re-Volt game files"

    filepath = bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        scene = context.scene

        format = get_format(self.filepath)

        print("Importing {}".format(self.filepath))

        if format == FORMAT_UNK:
            msg_box("Unsupported format.")
        elif format == FORMAT_PRM:
            from . import prm_in
            prm_in.import_file(self.filepath, scene)
        elif format == FORMAT_CAR:
            from . import parameters_in
            parameters_in.import_file(self.filepath, scene)
        else:
            msg_box("Unsupported format.")
        print("Import done.")
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

class ExportRV(bpy.types.Operator):
    bl_idname = "export_scene.revolt"
    bl_label = "Export Re-Volt Files"
    bl_description = "Export Re-Volt game files"

    filepath = bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        scene = context.scene
        props = context.scene.revolt

        start_time = time.time()

        # Gets the format from the file path
        frmt = get_format(self.filepath)

        if frmt == FORMAT_UNK:
            msg_box("Not supported for export: {}".format(file_formats[frmt]))
        else:
            context.window.cursor_set("WAIT")
            # Turns off undo for better performance
            use_global_undo = bpy.context.user_preferences.edit.use_global_undo
            bpy.context.user_preferences.edit.use_global_undo = False

            if bpy.ops.object.mode_set.poll():
                bpy.ops.object.mode_set(mode="OBJECT")

            # Saves filepath for re-exporting the same file
            props.last_exported_filepath = self.filepath

            if frmt == FORMAT_PRM:
                # Checks if a file can be exported
                if not tools.check_for_export(scene.objects.active):
                    return {"FINISHED"}

                from . import prm_out
                prm_out.export_file(self.filepath, scene)

            else:
                print("Format is not PRM {}".format(file_formats[frmt]))

            print("Export done.")

            # Re-enables undo
            bpy.context.user_preferences.edit.use_global_undo = use_global_undo

            context.window.cursor_set("DEFAULT")
            print(time.time() - start_time)
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def draw(self, context):
        props = context.scene.revolt
        layout = self.layout
        space = context.space_data

        layout.prop(props, "triangulate_ngons")
        layout.prop(props, "use_tex_num")

class ButtonSelectFaceProp(bpy.types.Operator):
    bl_idname = "faceprops.select"
    bl_label = "sel"
    bl_description = "Select or delesect all polygons with this property."
    prop = bpy.props.IntProperty()

    def execute(self, context):
        select_faces(context, self.prop)
        return{"FINISHED"}

# VERTEX COLORS

class ButtonVertexColorSet(bpy.types.Operator):
    bl_idname = "vertexcolor.set"
    bl_label = "Set Color"
    bl_description = "Apply color to selected faces."
    number = bpy.props.IntProperty()

    def execute(self, context):
        tools.set_vertex_color(context, self.number)
        return{"FINISHED"}

class ButtonVertexColorCreateLayer(bpy.types.Operator):
    bl_idname = "vertexcolor.create_layer"
    bl_label = "Create Vertex Color Layer"
    bl_description = "Creates a vertex color layer."

    def execute(self, context):
        create_color_layer(context)
        return{"FINISHED"}

class ButtonVertexAlphaCreateLayer(bpy.types.Operator):
    bl_idname = "alphacolor.create_layer"
    bl_label = "Create Alpha Color Layer"

    def execute(self, context):
        create_alpha_layer(context)
        return{"FINISHED"}

class ButtonEnableTextureMode(bpy.types.Operator):
    bl_idname = "helpers.enable_texture_mode"
    bl_label = "Enable Texture Mode"
    bl_description = "Enables texture mode so textures can be seen."

    def execute(self, context):
        enable_texture_mode()
        return{"FINISHED"}

class ButtonBakeShadow(bpy.types.Operator):
    bl_idname = "lighttools.bakeshadow"
    bl_label = "Bake Shadow"
    bl_description = "Creates a shadow plane beneath the selected object."

    def execute(self, context):
        tools.bake_shadow(self, context)
        return{"FINISHED"}

class ButtonBakeLightToVertex(bpy.types.Operator):
    bl_idname = "lighttools.bakevertex"
    bl_label = "Bake light"
    bl_description = "Bakes the light to the active vertex color layer."

    def execute(self, context):
        tools.bake_vertex(self, context)
        return{"FINISHED"}