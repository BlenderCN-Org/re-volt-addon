"""
PRM EXPORT
Meshes used for cars, game objects and track instances.
"""
if "bpy" in locals():
    import imp
    imp.reload(common)
    imp.reload(rvfiles)
    imp.reload(rvstruct)
    imp.reload(img_in)

import os
import bpy
import bmesh
from mathutils import Color, Vector
from . import common
from . import rvfiles
from . import rvstruct
from . import img_in

from .common import *

def export_file(filepath, scene):
    obj = scene.objects.active
    print("Exporting PRM for {}...".format(obj.name))
    meshes = []

    # Checks if other LoDs are present
    if "|q" in obj.data.name:
        print("LODs present.")
    else:
        print("No LOD present.")
        meshes.append(obj.data)

    # Exports all meshes to the PRM file
    with open(filepath, "wb") as file:
        for me in meshes:
            # Exports the mesh as a PRM object
            prm = export_mesh(me, scene, filepath)
            # Writes the PRM object to a file
            prm.write(file)

def export_mesh(me, scene, filepath):
    # Creates a bmesh from the supplied mesh
    bm = bmesh.new()
    bm.from_mesh(me)

    # Gets layers
    uv_layer = bm.loops.layers.uv.get("UVMap")
    tex_layer = bm.faces.layers.tex.get("UVMap")
    vc_layer = bm.loops.layers.color.get("Col")
    va_layer = bm.loops.layers.color.get("Alpha")
    texnum_layer = bm.faces.layers.int.get("Texture Number")
    type_layer = (bm.faces.layers.int.get("Type")
                  or bm.faces.layers.int.new("Type"))

    # Creates an empty PRM structure
    prm = rvstruct.PRM()

    prm.polygon_count = len(bm.faces)
    prm.vertex_count = len(bm.verts)

    for face in bm.faces:
        poly = rvstruct.Polygon()
        is_quad = len(face.verts) > 3

        # Sets the quad flag on the polygon
        if is_quad:
            face[type_layer] |= FACE_QUAD

        poly.type = face[type_layer]

        if tex_layer:
            poly.texture = texture_to_int(face[tex_layer].image.name)
        else:
            poly.texture = 0

        # Sets vertex indices for the polygon
        vert_order = [2, 1, 0, 3] if not is_quad else [3, 2, 1, 0]
        for i in vert_order:
            if i < len(face.verts):
                poly.vertex_indices.append(face.verts[i].index)
            else:
                # Fills up unused indices with 0s
                poly.vertex_indices.append(0)

        # write the vertex colors
        for i in vert_order:
            if i < len(face.verts):
                # Gets color from the channel or falls back to a default value
                color = face.loops[i][vc_layer] if vc_layer else Color((1,1,1))
                alpha = face.loops[i][va_layer] if va_layer else Color((1,1,1))
                col = rvstruct.Color(color=(int(color.r * 255),
                                            int(color.g * 255),
                                            int(color.b * 255)),
                                     alpha= int((alpha.v) * 255))
                poly.colors.append(col)
            else:
                # Writes opaque white
                col = rvstruct.Color(color=(255, 255, 255), alpha=255)
                poly.colors.append(col)


        # Writes the UV
        for i in vert_order:
            if i < len(face.verts) and uv_layer:
                uv = face.loops[i][uv_layer].uv
                poly.uv.append(rvstruct.UV(uv=(uv[0], 1 - uv[1])))
            else:
                poly.uv.append(rvstruct.UV())

        prm.polygons.append(poly)

    # export vertex positions and normals
    for vertex in bm.verts:
        coord = to_revolt_coord((vertex.co[0],
                                 vertex.co[1],
                                 vertex.co[2]))
        normal = to_revolt_coord((vertex.normal[0],
                                  vertex.normal[1],
                                  vertex.normal[2]))
        rvvert = rvstruct.Vertex()
        rvvert.position = rvstruct.Vector(data=coord)
        rvvert.normal = rvstruct.Vector(data=normal)
        prm.vertices.append(rvvert)

    return prm
