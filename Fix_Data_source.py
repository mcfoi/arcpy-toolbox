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

inputMxd = "C:\\geodati\\DTB_2012_MXD_per_vestizione_dati_Oracle\\DBT2012_RND2008.mxd"
#inputMxd = "CURRENT"
#inputMxdObject = arcpy.mapping.MapDocument(r"c:\geodati\a.mxd")
mxd = arcpy.mapping.MapDocument(r"C:\geodati\a.mxd")
layerList = arcpy.mapping.ListLayers(inputMxdObject)
dataFrameList = arcpy.mapping.ListDataFrames(inputMxdObject)

oracle = "Database Connections\\ESRI_SERVIZIOSIT@geodb_exat.sde"
#Feature Dataset must be omitted in Layer.replaceDataSource()
#since are just logical elements for grouping and do not have a phisical
#corrispondence
#featureDataset = ""
user = "ESRI_SERVIZIOSIT."
suffixOUT = "_RDN_TM32"
suffixIN = "_GB"

for ly in layerList:

    mxd = ""
    lycode = ""

    if (ly.name[:1] in ["A", "L", "P"] and ly.name[1:2]  in ["0", "1"]) or ("Confine_Amministrativo" in ly.name):

        if ly.name[:1] in ["A", "L", "P"] and ly.name[1:2]  in ["0", "1"]:

            '''
            lycode = ly.name[:7]
            newDataset = user+lycode+suffix
            '''
            lyDatasetName = ly.datasetName
            newLyDatasetName = lyDatasetName.replace(suffixOUT, suffixIN)
            newDataset = user+newLyDatasetName
            ly.replaceDataSource(oracle, "SDE_WORKSPACE", newDataset, False)

        if "Confine_Amministrativo" in ly.name:

            #lycode = "A090101_ComuneMilano"
            #newDataset = user+lycode+suffix
            #ly.replaceDataSource(oracle, "SDE_WORKSPACE", newDataset, False)
            pass

        msg = "Layer {0} with dataset {1} now pointing to\n   --> {2}".format(ly.name, lyDatasetName, newDataset)
        print msg
        arcpy.AddMessage(msg)


outputMxd = "C:\\geodati\\DTB_2012_MXD_per_vestizione_dati_Oracle\\DBT 2012 di Milano - Gauss-Boaga - with extra layers.mxd"
inputMxdObject.saveACopy(outputMxd)
msg = "{0} was saved with fixed Data Sources to:\n   {1}.".format(str(inputMxdObject.filePath), outputMxd)
print msg
arcpy.AddMessage(msg)

for df in dataFrameList:
    for bly in arcpy.mapping.ListBrokenDataSources(inputMxdObject):
        arcpy.mapping.RemoveLayer(df, bly)
        print "Not-DBT_2012 layer {0} was removed.".format(bly.name)

arcpy.RefreshTOC()

outputMxd = "C:\\geodati\\DTB_2012_MXD_per_vestizione_dati_Oracle\\DBT 2012 di Milano - Gauss-Boaga.mxd"
inputMxdObject.saveACopy(outputMxd)

msg = "{0} was saved as {1}.".format(str(inputMxdObject.filePath), outputMxd)
print msg
arcpy.AddMessage(msg)

