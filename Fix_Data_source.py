# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Fix_Data_source.py
# Created on: 2015-04-26 09:11:35.00000
# Description:
# Author: Marco Foi
# ---------------------------------------------------------------------------

# Import arcpy module
import os
import arcpy

# Dynamic variables:

mxd = "C:\\geodati\\DTB_2012_MXD_per_vestizione_dati_Oracle\\DBT 2012 di Milano.mxd"
#mxd = "CURRENT"
mxdDoc = arcpy.mapping.MapDocument(mxd)
layerList = arcpy.mapping.ListLayers(mxdDoc)

oracle = "Database Connections\\ESRI_SERVIZIOSIT@geodb_exat.sde"
featureDataset = "ESRI_SERVIZIOSIT.DBT_2012_RDN_TM32\\"
featureDataset = ""
user = "ESRI_SERVIZIOSIT."
for ly in layerList:

    if ly.name[:1] in ["A", "L", "P"] and ly.name[1:2]  in ["0", "1"]:
        lycode = ly.name[:7]

        newDataset = featureDataset+user+lycode
        ly.replaceDataSource(oracle, "SDE_WORKSPACE", newDataset, False)
        #ly.save()
        '''prevName = ly.name
        ly.name = ly.name.replace(soughtString, replacedString)'''
        msg = "{0} now pointing to {1} in {2} ".format(ly.name, lycode, newDataset)
        print msg
        arcpy.AddMessage(msg)

arcpy.RefreshTOC()
mxdDoc.save()