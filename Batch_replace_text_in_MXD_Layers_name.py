# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Batch_replace_text_in_MXD_Layers_name.py
# Created on: 2015-04-26 09:11:35.00000
# Description:
# Author: Marco Foi
# ---------------------------------------------------------------------------

# Import arcpy module
import os
import arcpy

# Dynamic variables:
mxdDoc = arcpy.mapping.MapDocument("CURRENT")
soughtString = arcpy.GetParameterAsText(0)
replacedString = arcpy.GetParameterAsText(1)

layerList = arcpy.mapping.ListLayers(mxdDoc)

for ly in layerList:
    prevName = ly.name
    ly.name = ly.name.replace(soughtString, replacedString)
    msg = "{0} was renamed in {1}".format(prevName, ly.name)
    print msg
    arcpy.AddMessage(msg)

arcpy.RefreshTOC()