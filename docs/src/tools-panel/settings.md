# Add-On Settings

![Settings Panel](./tools-panel/img/settings.png)

Some of these settings can also be found when importing/exporting files in the bottom left.

## General Settings

**Prefer Textured Solid Mode**:  
There are two encouraged ways to view textured meshes: Texture mode and Solid mode with *Textured Solid* shading enabled.

If this setting is enabled, the add-on will switch to Textured Solid mode instead of Texture mode.  
In Textured Solid mode, objects have additional shading which makes white and untextured models a lot easier to work with.

## Import Settings

**Texture Mode after Import**:  
Switches to texture display mode when a mesh has been imported (applies to .prm
and .w).

**Check Parameters for texture**:  
Whether to read the parameters.txt from the car folder when importing a `.prm` to find out the texture path.

## Export Settings

**Triangulate n-gons**:  
Triangulates faces with more than 4 vertices (also called n-gons).  
This will only affect the exported object, the mesh itself will not be
triangulated.  
Deselecting this might result in broken exports.

**Use Number for Textures**:  
Instead of using the texture file to determine the texture number, the number
set in the face properties panel will be used for exporting.

**Apply Scale**:  
Applies the scale of the object when exporting.

**Apply Rotation**:  
Applies the rotation of the object when exporting.

**Apply Translation**:  
Applies the *position* of the object when exporting.

## Import World (.w)

**Parent .w meshes to Empty**:  
Creates an empty object with the imported file's name and parents all meshes
contained in the .w file to it. This makes the object outliner a lot less
cluttered.

**Import Bound Boxes**:  
Imports the bound box for every single mesh of the .w file.

**Import Cubes**:  
Imports the cubes for every single mesh of the .w file.

**Import Big Cubes**:  
Imports the big cubes surrounding multiple meshes of the .w file.  

**\* Import Layers**:  
This option will be given as soon as one of the above debug settings have been
enabled (boundary boxes, spheres and big cubes):  
Selector for the layer(s) the debug objects will be placed on. Multiple layers
can be selected by `Shift`-clicking or dragging.  
By default, all objects will be imported to the first layer.

When imported, the actual meshes are going to be on the first layer while the
debug objects potentially are on other layers.  
To view multiple layers at once, hold down `Shift` and press numbers, e.g.
`1` and then `2`. While doing that, make sure the mouse cursor hovers over the 3D view.

## Export Collision (.ncp)

**Only export selected**:  
When this setting is enabled, only selected objects will be exported to the NCP.
If only one object is selected, the location of the object will be ignored and the center
of the NCP will be the center of the selected object (useful for exporting NCPs for single PRM files).

**Export Collision Grid (.w)**:  
This setting is required when exporting a collision file that matches a .w file (e.g. nhood1.ncp for nhood1.w).  
NCP files can be exported without the collision grid if the .ncp is intended to be used with an object or instance (.prm).

**Grid Size**:  
Defines the size of the lookup grid that is written to the end of the NCP file. The size defines the size of the single "cells". Choosing a higher number will result in a faster export but poorer performance in-game.