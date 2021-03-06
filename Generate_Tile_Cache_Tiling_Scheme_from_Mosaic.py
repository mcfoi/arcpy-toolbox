# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Generate_Tile_Cache_Tiling_Scheme_from_Mosaic.py
# Created on: 2015-04-08 16:06:58.00000
#   (generated by ArcGIS/ModelBuilder)
# Description:
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

Milano_2012_TIF_CTR_WM_projection_defined = arcpy.GetParameterAsText(0)
tilingscheme_xml  = arcpy.GetParameterAsText(1)

# Local variables:
#Milano_2012_TIF_CTR_WM_projection_defined = "\\\\HW10196F-NB\\Cartografie (raster e vettoriali)\\2012_TIF_CTR_WM_projection_defined\\Mosaic.gdb\\Milano_2012_TIF_CTR_WM_projection_defined"
tilingscheme_xml = "\\\\HW10196F-NB\\Cartografie (raster e vettoriali)\\2012_TIF_CTR_WM_projection_defined\\tilingscheme.xml"

# Process: Generate Tile Cache Tiling Scheme
arcpy.GenerateTileCacheTilingScheme_management(Milano_2012_TIF_CTR_WM_projection_defined, tilingscheme_xml, "NEW", "16", "", "9244648,868618;4622324,434309;2311162,217155;1155581,108577;577790,554289;288895,277144;144447,638572;72223,819286;36111,909643;18055,954822;9027,977411;4513,988705;2256,994353;1128,497176;282;141", "SCALE", "-20037700 30241100", "96", "256 x 256", "MIXED", "75", "COMPACT")

