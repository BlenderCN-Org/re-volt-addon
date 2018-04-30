---
title: Import and Export Specifications
---

:insert toc

# Import


## Importing Files
Re-Volt files can be imported via the File menu (File -> Import -> Re-Volt).  
There also is a button in the Re-Volt tab of the tool shelf of the 3D view.

## PRM
## Mesh Data
### Import
An object with the mesh will be linked to the current scene. Meshes consist of quads and tris.

### Export
N-gons will be triangulate by default. This can be disabled in the export settings.

## UV Map
### Export
The UV map of the mesh can be found on the default UV layer (UVMap).

### Export
Only the uv map called *UVMap* will be exported.

## Vertex Colors
### Import
The vertex colors can be found on the Col and Alpha layers.  
On the alpha channel, white is fully transparent while black is opaque.

### Export
Only the layers *Col* and *Alpha* will be exported.

## Level of Detail (LOD)
### Import
If a PRM file includes mulitple meshes, all of them will be imported.  
A suffix will be appended to the mesh name ("|q0" is the highest quality, "|q3 is a lower quality").  
A fake user will be assigned to them so they're not lost when saving the file.

## Textures
### Import
If the imported mesh is a car mesh, the texture path will be taken from the parameters.txt.
If it's a level file, the texture name will be generated from the polygon's texture number and taken from the level folder.
If a texture file cannot be found, a 512x512 dummy texture will be generated.
If a texture with the same name already exist, it will be used instead.

The texture number is also written onto a bmesh integer layer. This layer can be used instead of the texture on the tex layer for exporting.

### Export
To set the texture using this number layer, the *Use Number for Textures* setting has to be set in the export settings.  
When exporting, the texture number will be taken from the layer instead of being determined by the texture file assigned to the face.

If there is no texture present on a face, texture page 0 (A) will be used. If you actually want to export a mesh without a texture, enable the *Use Number for Textures* and set the number to `-1`.

## Face Type

### Import
The face types can be accessed with the Mesh properties which each have setter and getter functions that operate on int layers via bmesh.  
The face type layer is called "Type".
There is a Re-Volt tab in the Tool panel of the 3D view that allows users
to set face properties in Edit mode.

### Export
All selected face type properties will be set when exporting.

## World (.w)
### Import

#### Meshes

See PRM. The only addition is the environment color list that defines a specularity color for certain polygons if the flag is enabled for them.  

The environment color is accessible on a vertex color layer called *Env*.
The alpha value of the color is only accessible via the face property editing panel since it's written to a per-face float layer (*EnvAlpha*).

Do note that environment colors are per-polygon. The average color will be sampled from the vertex color layer when an env-enabled polygon is selected.

#### Texture Animation
Animations are stored in a dictionary that can be accessed in the *Properties* editor (*Scene* section).

#### Debug
Bounding boxes, bounding spheres and "big cubes" (spheres) can be imported to selected layers. They are for debug purposes only and they will not affect the export in any way.

### Export

Nothing noteworthy. Exports files the way they have been imported.

## NCP (Collision)

### Import

NCP flags and materials are written to the integer layers "NCPFlags" and "Material". A preview color for the materials is written to the "NCPPreview" vertex color channel.

### Export

All objects of the scene will  be merged into one mesh and then exported to the file. Objects will be ignored if they're a debug object or have the *ignore* object property set (Properties Editor).  
Faces that have the material `NONE` assigned to them will not be exported.  
The vertex color layer called "NCPPreview" will be ignored since it's only for previewing purposes.

A lookup grid will be automatically exported. This can be turned off in the export settings.

## parameters.txt (Car)

### Import
The add-on currently imports the car's body and wheels and their positions.  
If a wheel file cannot be found, it will be represented with an empty object.
