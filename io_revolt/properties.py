"""
Re-Volt Object and mesh properties and functions for setting/getting them.
"""
if "bpy" in locals():
    import imp
    imp.reload(common)

import bpy
from . import common
from bpy.props import (
BoolProperty,
EnumProperty,
FloatProperty,
IntProperty,
StringProperty,
CollectionProperty,
IntVectorProperty,
FloatVectorProperty,
PointerProperty
)

from .common import *

"""
These property getters and setters use the bmesh from the global dict that gets
updated by the scene update handler found in init.
Creating bmeshes in the panels is bad practice as it causes unexpected behavior.
"""

def get_face_material(self):
    eo = bpy.context.edit_object
    bm = dic.setdefault(eo.name, bmesh.from_edit_mesh(eo.data))
    layer = (bm.faces.layers.int.get("revolt_material")
             or bm.faces.layers.int.new("revolt_material"))
    selected_faces = [face for face in bm.faces if face.select]
    if len(selected_faces) == 0 or any([face[layer] != selected_faces[0][layer] for face in selected_faces]):
        return -1
    else:
        return selected_faces[0][layer]

def set_face_material(self, value):
    eo = bpy.context.edit_object
    bm = dic.setdefault(eo.name, bmesh.from_edit_mesh(eo.data))
    layer = (bm.faces.layers.int.get("revolt_material")
             or bm.faces.layers.int.new("revolt_material"))
    for face in bm.faces:
        if face.select:
            face[layer] = value

def get_face_texture(self):
    eo = bpy.context.edit_object
    bm = dic.setdefault(eo.name, bmesh.from_edit_mesh(eo.data))
    layer = (bm.faces.layers.int.get("Texture Number")
             or bm.faces.layers.int.new("Texture Number"))
    selected_faces = [face for face in bm.faces if face.select]
    if len(selected_faces) == 0 or any([face[layer] != selected_faces[0][layer] for face in selected_faces]):
        return -1
    else:
        return selected_faces[0][layer]

def set_face_texture(self, value):
    eo = bpy.context.edit_object
    bm = dic.setdefault(eo.name, bmesh.from_edit_mesh(eo.data))
    layer = (bm.faces.layers.int.get("Texture Number")
             or bm.faces.layers.int.new("Texture Number"))
    for face in bm.faces:
        if face.select:
            face[layer] = value

def get_face_property(self):
    eo = bpy.context.edit_object
    bm = dic.setdefault(eo.name, bmesh.from_edit_mesh(eo.data))
    layer = bm.faces.layers.int.get("Type") or bm.faces.layers.int.new("Type")
    selected_faces = [face for face in bm.faces if face.select]
    if len(selected_faces) == 0:
        return 0
    prop = selected_faces[0][layer]
    for face in selected_faces:
        prop = prop & face[layer]
    return prop

def set_face_property(self, value, mask):
    eo = bpy.context.edit_object
    bm = dic.setdefault(eo.name, bmesh.from_edit_mesh(eo.data))
    layer = bm.faces.layers.int.get("Type") or bm.faces.layers.int.new("Type")
    for face in bm.faces:
        if face.select:
            face[layer] = face[layer] | mask if value else face[layer] & ~mask

def select_faces(context, prop):
    eo = bpy.context.edit_object
    bm = dic.setdefault(eo.name, bmesh.from_edit_mesh(eo.data))
    flag_layer = (bm.faces.layers.int.get("Type")
                  or bm.faces.layers.int.new("Type"))

    for face in bm.faces:
        if face[flag_layer] & prop:
            face.select = not face.select
    redraw()

"""
Re-Volt object and mesh properties
"""

class RVObjectProperties(bpy.types.PropertyGroup):
    light1 = EnumProperty(
        name = "Light 1",
        items = bake_lights,
        default = "SUN",
        description = "Type of light"
    )
    light2 = EnumProperty(
        name = "Light 2",
        items = bake_lights,
        default = "HEMI",
        description = "Type of light"
    )
    light_intensity1 = FloatProperty(
        name = "Intensity 1",
        min = 0.0,
        default = 1.5,
        description = "Intensity of Light 1"
    )
    light_intensity2 = FloatProperty(
        name = "Intensity 2",
        min= 0.0,
        default = .05,
        description = "Intensity of Light 2"
    )
    light_orientation = EnumProperty(
        name = "Orientation",
        items = bake_light_orientations,
        default = "Z",
        description = "Directions of the lights"
    )
    shadow_method = EnumProperty(
        name = "Method",
        items = bake_shadow_methods,
        description = "Default (Adaptive QMC):\nFaster option, recommended "
                      "for testing the shadow settings.\n\n"
                      "High Quality:\nSlower and less grainy option, "
                      "recommended for creating the final shadow."
    )
    shadow_quality = IntProperty(
        name = "Quality",
        min = 0,
        max = 32,
        default = 8,
        description = "The amount of samples the shadow is rendered with "
                      "(number of samples taken extra)."
    )
    shadow_resolution = IntProperty(
        name = "Resolution",
        min = 32,
        max = 8192,
        default = 128,
        description = "Texture resolution of the shadow.\n"
                      "Default: 128x128 pixels."
    )
    shadow_softness = FloatProperty(
        name = "Softness",
        min = 0.0,
        max = 100.0,
        default = 0.5,
        description = "Softness of the shadow "
                      "(Light size for ray shadow sampling)."
    )
    shadow_table = StringProperty(
        name = "Shadowtable",
        default = "",
        description = "Shadow coordinates for use in parameters.txt of cars.\n"
                      "Click to select all, then CTRL C to copy."
    )


class RVMeshProperties(bpy.types.PropertyGroup):
    face_material = EnumProperty(
        name = "Material",
        items = materials,
        get = get_face_material,
        set = set_face_material
    )
    face_texture = IntProperty(
        name = "Texture",
        get = get_face_texture,
        set = set_face_texture,
        default = 0,
        min = -1,
        max = 9,
        description = "Texture page number:\n-1 is none,\n"
        "0 is texture page A\n"
        "1 is texture page B\n"
        "2 is texture page C\n"
        "3 is texture page D\n"
        "4 is texture page E\n"
        "5 is texture page F\n"
        "6 is texture page G\n"
        "7 is texture page H\n"
        "8 is texture page I\n"
        "9 is texture page J\n"
        "For this number to have an effect, "
        "the \"Use Texture Number\" export settings needs to be "
        "enabled."
    )
    face_double_sided = BoolProperty(
        name = "Double sided",
        get = lambda s: bool(get_face_property(s) & FACE_DOUBLE),
        set = lambda s,v: set_face_property(s, v, FACE_DOUBLE),
        description = "The polygon will be visible from both sides in-game."
    )
    face_translucent = BoolProperty(
        name = "Translucent",
        get = lambda s: bool(get_face_property(s) & FACE_TRANSLUCENT),
        set = lambda s,v: set_face_property(s, v, FACE_TRANSLUCENT),
        description = "Renders the polyon transparent\n(takes transparency "
                      "from the \"Alpha\" vertex color layer or the alpha "
                      "layer of the texture."
    )
    face_mirror = BoolProperty(
        name = "Mirror",
        get = lambda s: bool(get_face_property(s) & FACE_MIRROR),
        set = lambda s,v: set_face_property(s, v, FACE_MIRROR),
        description = "This polygon covers a mirror area. (?)"
    )
    face_additive = BoolProperty(
        name = "Additive blending",
        get = lambda s: bool(get_face_property(s) & FACE_TRANSL_TYPE),
        set = lambda s,v: set_face_property(s, v, FACE_TRANSL_TYPE),
        description = "Renders the polygon with additive blending (black "
                      "becomes transparent, bright colors are added to colors "
                      "beneath)."
    )
    face_texture_animation = BoolProperty(
        name = "Animated",
        get = lambda s: bool(get_face_property(s) & FACE_TEXANIM),
        set = lambda s,v: set_face_property(s, v, FACE_TEXANIM),
        description = "Uses texture animation for this poly (only in .w files)."
    )
    face_no_envmapping = BoolProperty(
        name = "No EnvMap (.prm)",
        get = lambda s: bool(get_face_property(s) & FACE_NOENV),
        set = lambda s,v: set_face_property(s, v, FACE_NOENV),
        description = "Disables the environment map for this poly (.prm only)."
    )
    face_envmapping = BoolProperty(
        name = "EnvMapping (.w)",
        get = lambda s: bool(get_face_property(s) & FACE_ENV),
        set = lambda s,v: set_face_property(s, v, FACE_ENV),
        description = "Enables the environment map for this poly (.w only).\n\n"
                      "If enabled on pickup.m, sparks will appear"
                      "around the poly."
    )
    face_cloth = BoolProperty(
        name = "Cloth effect (.prm)",
        get = lambda s: bool(get_face_property(s) & FACE_CLOTH),
        set = lambda s,v: set_face_property(s, v, FACE_CLOTH),
        description = "Enables the cloth effect used on the Mystery car."
    )
    face_skip = BoolProperty(
        name = "Do not export",
        get = lambda s: bool(get_face_property(s) & FACE_SKIP),
        set = lambda s,v: set_face_property(s, v, FACE_SKIP),
        description = "Skips the polygon when exporting (not Re-Volt related)."
    )

class RVSceneProperties(bpy.types.PropertyGroup):
    ui_fold_export_settings = BoolProperty(
        name = "Export Settings",
        default = True,
        description = "Show Export Settings"
    )
    vertex_color_picker = FloatVectorProperty(
        name="Object Color",
        subtype='COLOR',
        default=(0, 0, 1.0),
        min=0.0, max=1.0,
        description="Color picker for painting custom vertex colors."
    )
    triangulate_ngons = BoolProperty(
        name = "Triangulate n-gons",
        default = True,
        description = "Triangulate n-gons when exporting.\n"
                     "Re-Volt only supports tris and quads, n-gons will not be "
                     "exported correctly.\nOnly turn this off if you know what "
                     "you're doing!"
    )
    use_tex_num = BoolProperty(
        name = "Use Number for Textures",
        default = False,
        description = "Uses the texture number from the texture layer "
                      "accessible in the tool shelf in Edit mode.\n"
                      "Otherwise, it uses the texture from the texture file."
    )
